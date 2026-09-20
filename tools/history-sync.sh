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
#   history-sync.sh push-journal      ship -> grid: the ship's natural-history
#                                     journal (db/history/_journal/) goes up to
#                                     grid's _journal/incoming/, where grid
#                                     ingests it (see db/history/JOURNAL.md);
#                                     the one thing the ship sends
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
from pathlib import Path
if Path('db/history/translations.sqlite').is_file():
    src = sqlite3.connect('file:db/history/translations.sqlite?mode=ro', uri=True)
    dst = sqlite3.connect('db/history/translations.snapshot.sqlite')
    src.backup(dst); dst.close(); src.close()
    print('grid: reviewed translation snapshot taken')
EOF"
    $RSYNC --max-size="$MAX" \
      --exclude 'history.sqlite' --exclude 'history.sqlite-wal' --exclude 'history.sqlite-shm' \
      --exclude 'translations.sqlite*' --exclude 'translations.snapshot.sqlite*' \
      --exclude '_staging' --exclude '_ledger' --exclude '_backups' \
      "$GRID:$REMOTE/db/history/" "$HERE/db/history/"
    mv "$HERE/db/history/history.snapshot.sqlite" "$HERE/db/history/history.sqlite"
    # Translation releases are databases, not optional large media: transfer
    # them independently of MAX. Absence preserves existing ship installation;
    # use an empty reviewed release to revoke all French publication.
    if ssh "$GRID" "test -f $REMOTE/db/history/translations.sqlite"; then
      $RSYNC "$GRID:$REMOTE/db/history/translations.snapshot.sqlite" "$HERE/db/history/translations.snapshot.sqlite"
      mv "$HERE/db/history/translations.snapshot.sqlite" "$HERE/db/history/translations.sqlite"
    fi
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
  push-journal)
    if [ ! -d "$HERE/db/history/_journal" ]; then
      echo "no journal at $HERE/db/history/_journal" >&2; exit 1
    fi
    ssh "$GRID" "mkdir -p $REMOTE/db/history/_journal/incoming"
    $RSYNC "$HERE/db/history/_journal/" "$GRID:$REMOTE/db/history/_journal/incoming/"
    echo "journal pushed; grid ingests it with: tools/history-db.py ingest --journal db/history/_journal/incoming/<file>.jsonl"
    ;;
  push)
    echo "push is gone: grid owns the database, and code moves through git; the journal goes up with push-journal" >&2
    exit 1
    ;;
  *) echo "usage: history-sync.sh {pull [relpath...]|status|push-journal}"; exit 1 ;;
esac
