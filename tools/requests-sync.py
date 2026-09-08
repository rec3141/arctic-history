#!/usr/bin/env python3
"""Move the request queue between grid and the human validator's review page
at https://cryomics.org/amundsen/requests/ (Dreamhost, ssh host ``dreamhost``).

    requests-sync.py deploy       install or update the page itself
    requests-sync.py push         send the queue to the page as requests.json
    requests-sync.py pull         collect decisions from answers.json, apply
                                  them to the database, then push the fresh
                                  queue back

``pull`` is the one cron runs. A decision applies only to a request that is
still open here; applied and stale entries are then removed from the remote
answers.json so the page shows only what grid has not yet collected.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import arctic_history as H          # noqa: E402

REMOTE = "dreamhost"
RDIR = "cryomics.org/amundsen/requests"
PAGE = ROOT / "tools" / "requests-page"


def ssh(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["ssh", REMOTE, cmd], capture_output=True, text=True, timeout=60)


def rsync(src: str, dst: str) -> None:
    subprocess.run(["rsync", "-a", src, dst], check=True, timeout=120)


def push(c) -> None:
    rows = [dict(r) for r in c.execute(
        "SELECT * FROM requests ORDER BY status='open' DESC, id DESC")]
    feed = {"generated": H.now(), "requests": rows}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(feed, f, indent=1)
    rsync(f.name, f"{REMOTE}:{RDIR}/requests.json")
    Path(f.name).unlink()
    print(f"pushed {len(rows)} requests ({sum(r['status'] == 'open' for r in rows)} open)")


def pull(c) -> None:
    r = ssh(f"cat {RDIR}/answers.json 2>/dev/null || echo {{}}")
    try:
        answers = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        print(f"answers.json is not JSON; left in place: {r.stdout[:200]!r}", file=sys.stderr)
        answers = {}
    applied, keep = [], {}
    for ident, a in answers.items():
        row = c.execute("SELECT status FROM requests WHERE id=?", (ident,)).fetchone()
        if row and row["status"] == "open" and a.get("status") in ("approved", "denied", "done"):
            H.answer_request(c, int(ident), a["status"], a.get("answer", ""))
            applied.append(ident)
        elif row and row["status"] == "open":
            keep[ident] = a           # malformed; leave for a second look
    if applied or (answers and not keep):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(keep, f, indent=1)
        rsync(f.name, f"{REMOTE}:{RDIR}/answers.json")
        Path(f.name).unlink()
    print(f"applied {len(applied)} decisions" + (f": #{', #'.join(applied)}" if applied else ""))
    push(c)


def deploy() -> None:
    ssh(f"mkdir -p {RDIR}")
    rsync(str(PAGE / "index.php"), f"{REMOTE}:{RDIR}/index.php")
    rsync(str(PAGE / ".htaccess"), f"{REMOTE}:{RDIR}/.htaccess")
    print(f"deployed to {REMOTE}:{RDIR} — the password lives in ~/.amundsen-htpasswd there")


def main(argv=None) -> int:
    cmd = (argv or sys.argv[1:] or ["-"])[0]
    if cmd == "deploy":
        deploy()
        return 0
    if cmd not in ("push", "pull"):
        print(__doc__, file=sys.stderr)
        return 2
    c = H.connect()
    try:
        push(c) if cmd == "push" else pull(c)
    finally:
        c.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
