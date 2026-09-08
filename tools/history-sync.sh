#!/bin/bash
# Pull the history layer from grid, the research machine on the university
# network, to the ship. Grid owns the database and the fetched files; the
# ship is read-only toward grid and only pulls. Code moves through the git
# repository (rec3141/arctic-history), never through this script.
#
#   history-sync.sh pull              grid -> ship: the database and every file
#                                     up to 100 MB; larger objects are held on
#                                     grid and listed, to be fetched by name
#   history-sync.sh pull <relpath>..  fetch named objects regardless of size,
#                                     e.g. pull davis-baffin-hudson/files/big-map.png
#   history-sync.sh status            row counts on both sides
#
# The database is copied as a snapshot made with SQLite's own backup, never as
# the live file, and installed automatically: the ship never writes, so there
# is nothing local to lose. Files are rsynced; nothing is deleted on either
# side. Transfers are compressed and resumable, sized for a Starlink link —
# run pull from cron daily, or whenever the tab should catch up.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
GRID=grid
REMOTE=/data/dev/arctic-history
PY=${PY:-$(command -v /opt/miniforge3/bin/python3 || command -v python3)}
MAX=${HISTORY_SYNC_MAX:-100m}
RSYNC="rsync -avz --partial --timeout=120"

case "${1:-}" in
  pull)
    shift
    if [ $# -gt 0 ]; then                 # named large objects, no size gate
      for rel in "$@"; do
        $RSYNC "$GRID:$REMOTE/db/history/$rel" "$HERE/db/history/$rel"
      done
      exit 0
    fi
    ssh "$GRID" "cd $REMOTE && python3 - <<'EOF'
import sqlite3
src = sqlite3.connect('db/history/history.sqlite'); dst = sqlite3.connect('db/history/history.snapshot.sqlite')
src.backup(dst); dst.close(); src.close()
print('grid: snapshot taken')
EOF"
    $RSYNC --max-size="$MAX" \
      --exclude 'history.sqlite' --exclude 'history.sqlite-wal' --exclude 'history.sqlite-shm' \
      --exclude '_staging' --exclude '_ledger' --exclude '_backups' \
      "$GRID:$REMOTE/db/history/" "$HERE/db/history/"
    mv "$HERE/db/history/history.snapshot.sqlite" "$HERE/db/history/history.sqlite"
    echo "ship: database installed"
    findmax=$(echo "$MAX" | sed 's/m$/M/; s/g$/G/')      # rsync says 100m, find says 100M
    held=$(ssh "$GRID" "find $REMOTE/db/history -path '*/files/*' -type f -size +$findmax -printf '%s\t%P\n' 2>/dev/null | sort -rn" || true)
    if [ -n "$held" ]; then
      echo "held on grid (over $MAX; fetch one with: history-sync.sh pull <relpath>):"
      echo "$held" | awk -F'\t' '{printf "  %6.0f MB  %s\n", $1/1e6, $2}'
    fi
    ;;
  status)
    echo "--- ship"; "$PY" "$HERE/tools/history-db.py" stats
    echo "--- grid"; ssh "$GRID" "cd $REMOTE && python3 tools/history-db.py stats"
    ;;
  push)
    echo "push is gone: grid owns the database, and code moves through git" >&2
    exit 1
    ;;
  *) echo "usage: history-sync.sh {pull [relpath...]|status}"; exit 1 ;;
esac
