#!/usr/bin/env python3
"""Show Claude Code plan usage: the same numbers as the /usage slash command.

    usage.py                  five-hour and weekly utilization, with reset times
    usage.py --json           the raw response
    usage.py --max 70         exit 1 if the five-hour window is above 70 percent

The ceiling defaults to 80: the standing rule is that a wave uses no more than
80 percent of the five-hour window, so a plain run exits 1 when it is time to stop
launching researchers and wait for the reset.

Reads the OAuth token Claude Code keeps in ~/.claude/.credentials.json and
calls api.anthropic.com/api/oauth/usage, the endpoint /usage itself uses. It
is not a documented API, so treat a change in its shape as expected, not as a
fault. The token is refreshed by any running Claude Code session; if it has
expired and nothing has refreshed it, this exits 3 and says so.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CREDS = Path.home() / ".claude" / ".credentials.json"
URL = "https://api.anthropic.com/api/oauth/usage"
CEILING = 80.0      # percent of the five-hour window a wave may use (raised from 50 on 2026-09-08)


def fetch() -> dict:
    try:
        token = json.loads(CREDS.read_text())["claudeAiOauth"]["accessToken"]
    except (OSError, KeyError, json.JSONDecodeError) as e:
        sys.exit(f"no OAuth token in {CREDS}: {e}")
    req = urllib.request.Request(URL, headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": "oauth-2025-04-20",
        "User-Agent": "arctic-history usage.py",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("token expired or rejected (401); any Claude Code session refreshes it",
                  file=sys.stderr)
            sys.exit(3)
        sys.exit(f"HTTP {e.code} from {URL}: {e.read()[:300]!r}")


def when(iso: str | None) -> str:
    if not iso:
        return "n/a"
    t = datetime.fromisoformat(iso).astimezone()
    left = t - datetime.now(timezone.utc)
    h, m = divmod(max(int(left.total_seconds()) // 60, 0), 60)
    return f"resets {t:%a %H:%M} (in {h}h{m:02d}m)"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="print the raw response")
    ap.add_argument("--max", type=float, metavar="PCT", default=CEILING,
                    help=f"exit 1 if five-hour utilization exceeds PCT (default {CEILING})")
    a = ap.parse_args(argv)
    d = fetch()
    if a.json:
        json.dump(d, sys.stdout, indent=1)
        print()
        return 0
    five, week = d.get("five_hour") or {}, d.get("seven_day") or {}
    print(f"five-hour  {five.get('utilization', 0):5.1f}%  {when(five.get('resets_at'))}")
    print(f"weekly     {week.get('utilization', 0):5.1f}%  {when(week.get('resets_at'))}")
    for lim in d.get("limits") or []:
        if lim.get("kind") == "weekly_scoped":
            name = ((lim.get("scope") or {}).get("model") or {}).get("display_name") or "model"
            print(f"weekly {name.lower():<7}{lim.get('percent', 0):5.1f}%")
    if five.get("utilization", 0) > a.max:
        print(f"over the {a.max:g}% five-hour ceiling", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
