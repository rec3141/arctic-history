#!/bin/bash
# Snapshot the history database with SQLite's own backup — never by copying
# the live file, so a researcher writing at that moment cannot leave a torn
# copy. Keeps the newest 100 snapshots locally under db/history/_backups/
# (hourly from cron, that is about four days) and mirrors each one to
# dreamhost:backups/amundsen/, pruned to the newest 30, so the research
# survives this machine.
set -euo pipefail
HERE=$(cd "$(dirname "$0")/.." && pwd)
DB="$HERE/db/history/history.sqlite"
OUT="$HERE/db/history/_backups"
STAMP=$(date +%Y%m%d-%H%M)
[ -f "$DB" ] || { echo "no database at $DB" >&2; exit 1; }
mkdir -p "$OUT"
python3 - "$DB" "$OUT/history-$STAMP.sqlite" <<'EOF'
import sqlite3, sys
src = sqlite3.connect(sys.argv[1]); dst = sqlite3.connect(sys.argv[2])
src.backup(dst); dst.close(); src.close()
EOF
ls -1t "$OUT"/history-*.sqlite | tail -n +101 | xargs -r rm --
if rsync -a "$OUT/history-$STAMP.sqlite" dreamhost:backups/amundsen/ 2>/dev/null; then
  ssh dreamhost 'cd backups/amundsen && ls -1t history-*.sqlite | tail -n +31 | xargs -r rm --' 2>/dev/null || true
else
  echo "offsite copy failed; snapshot kept locally at $OUT/history-$STAMP.sqlite" >&2
fi
# the session and researcher transcripts are the project's process record;
# mirror them off-machine too (incremental, additive — nothing deleted remotely)
rsync -az "$HOME/.claude/projects/-data-dev-arctic-history/" \
  dreamhost:backups/amundsen-transcripts/ 2>/dev/null \
  || echo "transcript mirror failed; local copies remain" >&2
echo "$OUT/history-$STAMP.sqlite"
