#!/bin/bash
# Move the history layer between the ship and grid, the research machine on
# the university network.
#
#   history-sync.sh push      ship -> grid: the code, the brief, the files, a
#                             consistent snapshot of the database
#   history-sync.sh pull      grid -> ship: the database snapshot and the files
#                             the researchers fetched, for the dashboard build
#   history-sync.sh status    row counts on both sides
#
# The database is copied as a snapshot made with SQLite's own backup, never as
# the live file, so a researcher writing at that moment cannot leave a torn
# copy. Files are rsynced; nothing is deleted on either side.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
GRID=grid
REMOTE=/data/dev/arctic-history
PY=${PY:-$(command -v /opt/miniforge3/bin/python3 || command -v python3)}
DB="$HERE/db/history/history.sqlite"
SNAP="$HERE/db/history/history.snapshot.sqlite"

snapshot() {            # $1 python, $2 live db, $3 snapshot path
  "$1" - "$2" "$3" <<'EOF'
import sqlite3, sys
src = sqlite3.connect(sys.argv[1]); dst = sqlite3.connect(sys.argv[2])
src.backup(dst); dst.close(); src.close()
EOF
}

case "${1:-}" in
  push)
    [ -f "$DB" ] && snapshot "$PY" "$DB" "$SNAP"
    ssh "$GRID" "mkdir -p $REMOTE/db/history"
    rsync -av --relative \
      "$HERE/./arctic_history/__init__.py" \
      "$HERE/./tools/history-db.py" "$HERE/./tools/history-fetch.py" "$HERE/./tools/history-sync.sh" \
      "$HERE/./tests/test_history.py" "$HERE/./README.md" \
      "$GRID:$REMOTE/"
    rsync -av --exclude 'history.sqlite' --exclude 'history.sqlite-wal' --exclude 'history.sqlite-shm' \
      "$HERE/db/history/" "$GRID:$REMOTE/db/history/"
    # the snapshot becomes grid's live database only if grid has none yet;
    # otherwise it lands beside it for a person to merge
    ssh "$GRID" "cd $REMOTE/db/history && if [ ! -f history.sqlite ]; then mv history.snapshot.sqlite history.sqlite && echo 'grid: database installed from snapshot'; else echo 'grid: already has a database; snapshot left as history.snapshot.sqlite'; fi"
    ;;
  pull)
    ssh "$GRID" "cd $REMOTE && python3 - <<'EOF'
import sqlite3
src = sqlite3.connect('db/history/history.sqlite'); dst = sqlite3.connect('db/history/history.snapshot.sqlite')
src.backup(dst); dst.close(); src.close()
print('grid: snapshot taken')
EOF"
    rsync -av --exclude 'history.sqlite' --exclude 'history.sqlite-wal' --exclude 'history.sqlite-shm' \
      --exclude '_staging' "$GRID:$REMOTE/db/history/" "$HERE/db/history/"
    echo "ship: snapshot at db/history/history.snapshot.sqlite; install it with"
    echo "  mv db/history/history.snapshot.sqlite db/history/history.sqlite"
    echo "after checking nothing local is newer (tools/history-db.py stats on both)."
    ;;
  status)
    echo "--- ship"; "$PY" "$HERE/tools/history-db.py" stats
    echo "--- grid"; ssh "$GRID" "cd $REMOTE && python3 tools/history-db.py stats"
    ;;
  *) echo "usage: history-sync.sh {push|pull|status}"; exit 1 ;;
esac
