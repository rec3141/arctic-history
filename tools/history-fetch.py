#!/usr/bin/env python3
"""Fetch a file for the history layer, the way the ship's network wants it done.

    history-fetch.py URL --topic frobisher --name frobisher-best-1578.pdf
    history-fetch.py URL --topic whaling --name scoresby-1820-v1.txt --ezproxy
    history-fetch.py --budget                 # how much of today's allowance is used
    history-fetch.py --probe URL              # size and type without downloading

What it does for you:

* Routes through the grid tunnel (a SOCKS proxy on 127.0.0.1:1080) whenever it
  is up. That path leaves the University of Manitoba's network, so publishers
  see a campus address, and it is several times faster than the ship's direct
  link for large files. It falls back to the direct link when the tunnel is down.
* ``--ezproxy`` rewrites a publisher URL into the university library's EZproxy
  form and carries the session cookie, which the library issues to the campus
  address without a password. Use it for JSTOR, Cambridge Core, Taylor and
  Francis, Wiley, Springer, Elsevier, Project MUSE and the like. Open archives
  (Internet Archive, Gutenberg, HathiTrust public domain, Wikimedia) need no
  proxy and get none.
* Asks the server for the size first. Anything up to 50 MB is fetched on the
  spot. Anything larger is not fetched: a request is filed in the history
  database for a person to approve, and you carry on with other work.
* Keeps a ledger of bytes per day under ``db/history/_ledger/``; the allowance
  is 10 GB a day across the whole crew, and the tool refuses when it is spent.
* Checks what came back: the type against the name, and a size that is not an
  error page. A bad file is deleted and reported, never left to be registered.

The file lands in ``db/history/<topic>/files/<name>`` and the path to give
``history-db.py --local-file`` is printed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from arctic_history import *  # noqa: F401,F403
import arctic_history as H          # noqa: E402

SOCKS = "127.0.0.1:1080"
EZPROXY = "uml.idm.oclc.org"
LIMIT_MB = float(os.environ.get("HISTORY_FETCH_LIMIT_MB", 50))
BUDGET_GB = float(os.environ.get("HISTORY_FETCH_BUDGET_GB", 10))
LEDGER = H.HISTORY_DIR / "_ledger"
JAR = H.HISTORY_DIR / "_ledger" / "ezproxy-cookies.txt"
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0 underway-history-research"

# hosts the library proxies; anything else is fetched as is
PROXIED = ("jstor.org", "cambridge.org", "tandfonline.com", "wiley.com", "springer.com",
           "sciencedirect.com", "muse.jhu.edu", "oup.com", "academic.oup.com", "sagepub.com",
           "degruyter.com", "brill.com", "utpjournals.press", "erudit.org", "proquest.com")

# hosts that rate-limit the shared campus address, so they are fetched direct
DIRECT = ("wikimedia.org", "wikipedia.org", "wikidata.org")

TYPES = {".pdf": ("PDF",), ".jpg": ("JPEG",), ".jpeg": ("JPEG",), ".png": ("PNG",), ".gif": ("GIF",),
         ".tif": ("TIFF",), ".tiff": ("TIFF",), ".webp": ("Web/P", "RIFF"), ".txt": ("text", "ASCII", "UTF-8"),
         ".html": ("HTML",), ".xml": ("XML",), ".json": ("JSON", "text", "ASCII", "UTF-8"),
         ".zip": ("Zip",), ".epub": ("EPUB", "Zip"), ".djvu": ("DjVu",), ".mp4": ("MP4", "ISO Media"),
         ".csv": ("CSV", "text", "ASCII", "UTF-8"), ".bib": ("text", "ASCII", "UTF-8"), ".md": ("text", "ASCII", "UTF-8")}


_campus: bool | None = None


def on_campus() -> bool:
    """True when this machine's own address is one the library trusts: the
    EZproxy answers a bare login with a session redirect instead of a sign-in
    page. On grid that is so; on the ship it is not, and the tunnel supplies it."""
    global _campus
    if _campus is None:
        try:
            r = subprocess.run(["curl", "-s", "--max-time", "15", "-o", "/dev/null", "-w", "%{redirect_url}",
                                f"https://{EZPROXY}/login?url=https://www.jstor.org/"],
                               capture_output=True, text=True, timeout=20)
            _campus = "/connect?session=" in r.stdout
        except (subprocess.TimeoutExpired, OSError):
            _campus = False
    return _campus


def tunnel_up() -> bool:
    try:
        r = subprocess.run(["curl", "-s", "--max-time", "8", "--socks5-hostname", SOCKS, "-o", "/dev/null",
                            "-w", "%{http_code}", "https://archive.org/"], capture_output=True, text=True, timeout=12)
        return r.stdout.strip().startswith(("2", "3"))
    except (subprocess.TimeoutExpired, OSError):
        return False


def ezproxy_url(url: str) -> str:
    """``https://www.jstor.org/stable/123`` -> the library's proxied form."""
    u = urlsplit(url)
    if u.hostname and u.hostname.endswith(EZPROXY):
        return url
    host = u.hostname.replace(".", "-")
    return f"{u.scheme}://{host}.{EZPROXY}{u.path}{'?' + u.query if u.query else ''}"


def needs_proxy(url: str) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return any(host == p or host.endswith("." + p) for p in PROXIED)


def prefers_direct(url: str) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return any(host == p or host.endswith("." + p) for p in DIRECT)


def curl(args: list[str], via_tunnel: bool, jar: bool = False, timeout: int = 600) -> subprocess.CompletedProcess:
    cmd = ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA]
    if via_tunnel:
        cmd += ["--socks5-hostname", SOCKS]
    if jar:
        JAR.parent.mkdir(parents=True, exist_ok=True)
        cmd += ["-c", str(JAR), "-b", str(JAR)]
    return subprocess.run(cmd + args, capture_output=True, text=True, timeout=timeout + 30)


def probe(url: str, via_tunnel: bool, jar: bool) -> dict:
    r = curl(["-I", "-o", "/dev/null", "-w", "%{http_code}\t%{content_type}\t%{size_download}\t%{url_effective}\t%{redirect_url}", url],
             via_tunnel, jar, timeout=60)
    code, ctype, _, final, _ = (r.stdout.strip().split("\t") + ["", "", "", "", ""])[:5]
    # HEAD often lies about size; ask again with a range and read Content-Range
    r2 = curl(["-r", "0-0", "-o", "/dev/null", "-D", "-", url], via_tunnel, jar, timeout=60)
    m = re.search(r"content-range:\s*bytes\s+\d+-\d+/(\d+)", r2.stdout, re.I)
    m2 = re.search(r"content-length:\s*(\d+)", r.stdout + "\n" + r2.stdout, re.I)
    size = int(m.group(1)) if m else (int(m2.group(1)) if m2 and int(m2.group(1)) > 1 else None)
    return {"code": code, "type": ctype, "size": size, "final": final}


def ledger_path(day: dt.date | None = None) -> Path:
    LEDGER.mkdir(parents=True, exist_ok=True)
    return LEDGER / f"{(day or dt.date.today()).isoformat()}.tsv"


def used_today() -> int:
    p = ledger_path()
    if not p.exists():
        return 0
    return sum(int(line.split("\t")[1]) for line in p.read_text().splitlines() if "\t" in line)


def record(size: int, url: str, dest: str, topic: str) -> None:
    with ledger_path().open("a") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')}\t{size}\t{topic}\t{dest}\t{url}\n")


def check_file(path: Path, suffix: str) -> str | None:
    """None when the file looks like what its intended name says; otherwise
    the problem. ``suffix`` is the final name's, since the download lands in a
    ``.part`` file first."""
    if not path.exists():
        return "nothing was written"
    size = path.stat().st_size
    if size < 4096:
        head = path.read_bytes()[:200]
        return f"only {size} bytes; starts {head!r}"
    kind = subprocess.run(["file", "-b", str(path)], capture_output=True, text=True).stdout.strip()
    want = TYPES.get(suffix.lower())
    if want and not any(w.lower() in kind.lower() for w in want):
        if "HTML" in kind and suffix.lower() != ".html":
            return f"an HTML page came back instead of {suffix}: probably a login or error page ({kind[:60]})"
        return f"file says '{kind[:70]}', not {suffix}"
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="history-fetch.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    ap.add_argument("--topic", help="the topic slug; the file lands in db/history/<topic>/files/")
    ap.add_argument("--name", help="the file name: <topic>-<short>.<ext>, lowercase, no spaces")
    ap.add_argument("--ezproxy", action="store_true", help="go through the university library's EZproxy (publishers)")
    ap.add_argument("--direct", action="store_true", help="skip the tunnel even if it is up")
    ap.add_argument("--why", default="", help="what the file is for (carried into a request if one is filed)")
    ap.add_argument("--who", default="", help="the run filing any request")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    ap.add_argument("--probe", action="store_true", help="report size and type only")
    ap.add_argument("--budget", action="store_true", help="report today's usage and stop")
    a = ap.parse_args(argv)

    if a.budget:
        used = used_today()
        print(f"{used / 1e9:.2f} GB of {BUDGET_GB} GB used today ({used / 1e6:.0f} MB); "
              + ("on campus, no tunnel needed" if on_campus() else f"tunnel {'up' if tunnel_up() else 'down'}"))
        return 0
    if not a.url:
        ap.error("a URL is needed")

    url = a.url
    proxied = a.ezproxy or needs_proxy(url)
    if proxied:
        url = ezproxy_url(url)
    campus = on_campus()
    via = not a.direct and not campus and not prefers_direct(url) and tunnel_up()
    if proxied and not via and not campus:
        print("the library proxy only works from the campus address, and the grid tunnel is down; "
              "run `~/bin/grid-tunnel up`, or fetch without --ezproxy", file=sys.stderr)
        return 2
    info = probe(url, via, proxied)
    route = ("ezproxy via tunnel" if proxied else "tunnel") if via else ("ezproxy, campus" if proxied else "direct" + (", campus" if campus else ""))
    if a.probe:
        print(json.dumps({**info, "route": route}, indent=1))
        return 0
    if not (a.topic and a.name):
        ap.error("--topic and --name are needed to download")
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", a.name):
        ap.error("--name must be lowercase letters, digits, dots, hyphens")
    dest = H.HISTORY_DIR / H.slugify(a.topic) / "files" / a.name
    rel = str(dest.relative_to(H.HISTORY_DIR))
    if dest.exists() and not a.force:
        print(f"already here: {rel} ({dest.stat().st_size / 1e6:.1f} MB); --force to refetch")
        return 0

    size = info["size"]
    if size and size > LIMIT_MB * 1e6:
        c = H.connect()
        try:
            ident = H.add_request(c, a.topic, "download", f"{a.name} ({size / 1e6:.0f} MB) from {urlsplit(a.url).hostname}",
                                  why=a.why, url=a.url, size_mb=size / 1e6, dest=rel, who=a.who)
        finally:
            c.close()
        print(f"{size / 1e6:.0f} MB is over the {LIMIT_MB} MB limit: filed request #{ident} for a person to approve. "
              f"Carry on; check `history-db.py requests --topic {a.topic}` later, and record the artifact now with "
              f"--download-url and no --local-file.")
        return 3
    used = used_today()
    if used + (size or 0) > BUDGET_GB * 1e9:
        print(f"today's {BUDGET_GB} GB allowance is spent ({used / 1e9:.2f} GB); try tomorrow or file a request", file=sys.stderr)
        return 4

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = curl(["-o", str(tmp), "-w", "%{http_code}\t%{size_download}\t%{speed_download}", url], via, proxied)
    code, got, speed = (r.stdout.strip().split("\t") + ["", "0", "0"])[:3]
    if code == "429" and not proxied:
        # rate-limited on this route: the other one has a different address
        via = not via
        route = "tunnel" if via else "direct"
        r = curl(["-o", str(tmp), "-w", "%{http_code}\t%{size_download}\t%{speed_download}", url], via, proxied)
        code, got, speed = (r.stdout.strip().split("\t") + ["", "0", "0"])[:3]
    if r.returncode != 0 or not code.startswith("2"):
        tmp.unlink(missing_ok=True)
        print(f"fetch failed ({route}): HTTP {code or '?'} {r.stderr.strip()[:200]}", file=sys.stderr)
        return 1
    problem = check_file(tmp, dest.suffix)
    if problem:
        tmp.unlink(missing_ok=True)
        print(f"discarded: {problem}", file=sys.stderr)
        if proxied:
            print("through the proxy that usually means the library has no subscription to this title, "
                  "or the page needs a browser; file a `request --kind access` if it matters", file=sys.stderr)
        return 1
    tmp.replace(dest)
    n = int(got or dest.stat().st_size)
    record(n, a.url, rel, a.topic)
    print(f"{rel}  {n / 1e6:.1f} MB  {float(speed) / 1e3:.0f} kB/s  {route}")
    print(f"--local-file {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
