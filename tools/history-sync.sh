#!/bin/bash
# Pull the history layer from grid, the research machine on the university
# network, to the ship. Grid owns the database and the fetched files; the
# ship is read-only toward grid and only pulls. Code moves through the git
# repository (rec3141/arctic-history), never through this script.
#
#   history-sync.sh pull      grid -> ship: a consistent database snapshot and
#                             the files the researchers fetched, for the
#                             dashboard build
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

case "${1:-}" in
  pull)
    ssh "$GRID" "cd $REMOTE && python3 - <<'EOF'
import sqlite3
src = sqlite3.connect('db/history/history.sqlite'); dst = sqlite3.connect('db/history/history.snapshot.sqlite')
src.backup(dst); dst.close(); src.close()
print('grid: snapshot taken')
EOF"
    rsync -av --exclude 'history.sqlite' --exclude 'history.sqlite-wal' --exclude 'history.sqlite-shm' \
      --exclude '_staging' --exclude '_ledger' "$GRID:$REMOTE/db/history/" "$HERE/db/history/"
    echo "ship: snapshot at db/history/history.snapshot.sqlite; install it with"
    echo "  mv db/history/history.snapshot.sqlite db/history/history.sqlite"
    ;;
  status)
    echo "--- ship"; "$PY" "$HERE/tools/history-db.py" stats
    echo "--- grid"; ssh "$GRID" "cd $REMOTE && python3 tools/history-db.py stats"
    ;;
  push)
    echo "push is gone: grid owns the database, and code moves through git" >&2
    exit 1
    ;;
  *) echo "usage: history-sync.sh {pull|status}"; exit 1 ;;
esac
