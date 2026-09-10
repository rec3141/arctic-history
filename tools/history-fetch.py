#!/usr/bin/env python3
"""Fetch a file for the history layer.

    history-fetch.py URL --topic frobisher --name frobisher-best-1578.pdf
    history-fetch.py URL --topic whaling --name scoresby-1820-v1.txt --ezproxy
    history-fetch.py --probe URL              # size and type without downloading
    history-fetch.py --scholarsportal /ebooks/ebooks0/gibson_crkn/2009-12-01/1/400057 \
        --pages 94-146 --topic posts-rcmp-missions --name posts-rcmp-missions-grant2002-pp72-124.pdf

What it does for you:

* ``--ezproxy`` rewrites a publisher URL into the university library's EZproxy
  form and carries the session cookie, which the library issues to this
  machine's campus address without a password. JSTOR, Cambridge Core, Taylor
  and Francis, Wiley, Springer, Elsevier and Project MUSE are proxied
  automatically. Open archives (Internet Archive, Gutenberg, HathiTrust public
  domain, Wikimedia) need no proxy and get none. A proxied fetch that comes
  back as a login page means the library has no subscription: file a
  ``history-db.py request --kind access``.
* Checks what came back: the type against the name, and a size that is not an
  error page. A bad file is deleted and reported, never left to be registered.
* Wikimedia rate-limits this shared campus address: send Commons queries one
  at a time, and check the cached lookups in ``_staging/`` first.
* ``--scholarsportal URI --pages FROM-TO`` (researcher-only: never run by a
  Sonnet helper or Haiku reader) pulls a page range of a licensed
  e-book from Scholars Portal Books (the "Canadian Electronic Library" the
  catalogue lists; ``tools/library-search.py`` prints the URI). The platform
  allows 53 pages per session and the person allows one session per platform
  per hour for the whole crew; the tool enforces both through
  ``_ledger/platform-sessions.json`` and tells you when the next slot opens.
  Pages are the reader's numbering: printed page + the front matter count
  (``--pages`` of 1-20 shows you the contents and the offset).

The file lands in ``db/history/<topic>/files/<name>`` and the path to give
``history-db.py --local-file`` is printed.
"""

from __future__ import annotations

import argparse
import base64
import os
import tempfile
import time
from urllib.parse import quote
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import arctic_history as H          # noqa: E402

EZPROXY = "uml.idm.oclc.org"
JAR = H.HISTORY_DIR / "_ledger" / "ezproxy-cookies.txt"
UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0 underway-history-research"

# hosts the library proxies; anything else is fetched as is
PROXIED = ("jstor.org", "cambridge.org", "tandfonline.com", "wiley.com", "springer.com",
           "sciencedirect.com", "muse.jhu.edu", "oup.com", "academic.oup.com", "sagepub.com",
           "degruyter.com", "brill.com", "utpjournals.press", "erudit.org", "proquest.com")

TYPES = {".pdf": ("PDF",), ".jpg": ("JPEG",), ".jpeg": ("JPEG",), ".png": ("PNG",), ".gif": ("GIF",),
         ".tif": ("TIFF",), ".tiff": ("TIFF",), ".webp": ("Web/P", "RIFF"), ".txt": ("text", "ASCII", "UTF-8"),
         ".html": ("HTML",), ".xml": ("XML",), ".json": ("JSON", "text", "ASCII", "UTF-8"),
         ".zip": ("Zip",), ".epub": ("EPUB", "Zip"), ".djvu": ("DjVu",), ".mp4": ("MP4", "ISO Media"),
         ".csv": ("CSV", "text", "ASCII", "UTF-8"), ".bib": ("text", "ASCII", "UTF-8"), ".md": ("text", "ASCII", "UTF-8")}


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


PACED = {"upload.wikimedia.org": 4.0, "commons.wikimedia.org": 4.0, "archive.org": 2.0,
         "iiif.archive.org": 2.0, "www.biodiversitylibrary.org": 2.0, "api.nb.no": 1.0, "www.nb.no": 1.0}


def pace(url: str) -> float:
    """Crew-wide pacing for the hosts that rate-limit this campus address.
    Seven researchers fetching from Wikimedia Commons at once got the whole
    address 429-locked; one shared clock keeps the crew under the limit.
    Blocks until the host's slot opens, stamps the ledger, returns the wait."""
    import fcntl
    host = (urlsplit(url).hostname or "").lower()
    gap = next((g for h, g in PACED.items() if host == h or host.endswith("." + h)), 0)
    if not gap:
        return 0.0
    ledger = H.HISTORY_DIR / "_ledger" / "pacing.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    lock = ledger.with_suffix(".lock")
    with open(lock, "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        try:
            data = json.loads(ledger.read_text())
        except (OSError, ValueError):
            data = {}
        last = float(data.get(host, 0))
        wait = max(0.0, last + gap - time.time())
        if wait:
            time.sleep(wait)
        data[host] = time.time()
        ledger.write_text(json.dumps(data, indent=1))
    return wait


def curl(args: list[str], jar: bool = False, timeout: int = 600) -> subprocess.CompletedProcess:
    url = next((x for x in args if x.startswith("http")), "")
    if url:
        pace(url)
    cmd = ["curl", "-sS", "-L", "--max-time", str(timeout), "-A", UA]
    if jar:
        JAR.parent.mkdir(parents=True, exist_ok=True)
        cmd += ["-c", str(JAR), "-b", str(JAR)]
    return subprocess.run(cmd + args, capture_output=True, text=True, timeout=timeout + 30)


def probe(url: str, jar: bool) -> dict:
    r = curl(["-I", "-o", "/dev/null", "-w", "%{http_code}\t%{content_type}\t%{size_download}\t%{url_effective}\t%{redirect_url}", url],
             jar, timeout=60)
    code, ctype, _, final, _ = (r.stdout.strip().split("\t") + ["", "", "", "", ""])[:5]
    # HEAD often lies about size; ask again with a range and read Content-Range
    r2 = curl(["-r", "0-0", "-o", "/dev/null", "-D", "-", url], jar, timeout=60)
    m = re.search(r"content-range:\s*bytes\s+\d+-\d+/(\d+)", r2.stdout, re.I)
    m2 = re.search(r"content-length:\s*(\d+)", r.stdout + "\n" + r2.stdout, re.I)
    size = int(m.group(1)) if m else (int(m2.group(1)) if m2 and int(m2.group(1)) > 1 else None)
    return {"code": code, "type": ctype, "size": size, "final": final}


def check_file(path: Path, suffix: str) -> str | None:
    """None when the file looks like what its intended name says; otherwise
    the problem. ``suffix`` is the final name's, since the download lands in a
    ``.part`` file first."""
    if not path.exists():
        return "nothing was written"
    size = path.stat().st_size
    kind = subprocess.run(["file", "-b", str(path)], capture_output=True, text=True).stdout.strip()
    want = TYPES.get(suffix.lower())
    # a genuine small image (a line cut from a scanned book) is fine; anything
    # else under 4 kB is an error page or an empty reply
    small_image_ok = want and suffix.lower() in (".png", ".jpg", ".jpeg", ".gif") \
        and any(w.lower() in kind.lower() for w in want) and size > 0
    if size < 4096 and not small_image_ok:
        head = path.read_bytes()[:200]
        return f"only {size} bytes; starts {head!r}"
    if want and not any(w.lower() in kind.lower() for w in want):
        if "HTML" in kind and suffix.lower() != ".html":
            return f"an HTML page came back instead of {suffix}: probably a login or error page ({kind[:60]})"
        return f"file says '{kind[:70]}', not {suffix}"
    return None


SP = "https://books-scholarsportal-info.uml.idm.oclc.org"
SP_LIMIT = 53


def scholarsportal(uri: str, pages: str, dest: Path) -> int:
    ranges = []
    for part in pages.split(","):
        m = re.fullmatch(r"\s*(\d+)-(\d+)\s*", part)
        if not m or int(m.group(2)) < int(m.group(1)):
            print("--pages must be FROM-TO ranges in the reader's numbering, e.g. 94-146 or 209-228,287-297", file=sys.stderr)
            return 2
        ranges.append((int(m.group(1)), int(m.group(2))))
    total = sum(hi - lo + 1 for lo, hi in ranges)
    if total > SP_LIMIT:
        print(f"Scholars Portal serves at most {SP_LIMIT} pages per session; {pages} is {total}", file=sys.stderr)
        return 2
    left = curl(["-o", "-", f"{SP}/api/pagesLeft?uri={uri}"], jar=True, timeout=60).stdout
    try:
        left_n = json.loads(left).get("pagesLeft")
    except ValueError:
        left_n = None
    if left_n is not None and int(left_n) < total:
        print(f"Scholars Portal has {left_n} pages left in today's allowance for this campus address "
              f"({total} asked). The allowance is daily, not hourly: try tomorrow, or take the pages another way.", file=sys.stderr)
        return 3
    ledger = H.HISTORY_DIR / "_ledger" / "platform-sessions.json"
    try:
        previous = json.loads(ledger.read_text()).get("scholarsportal")
    except (OSError, ValueError):
        previous = None
    wait = H.platform_session_gate(ledger, "scholarsportal", time.time())
    if wait:
        print(f"Scholars Portal was used {int((H.PLATFORM_GAP - wait) / 60)} min ago by this crew; "
              f"the next session opens in {int(wait / 60) + 1} min. Do something else meanwhile.", file=sys.stderr)
        return 3
    meta = curl(["-o", "-", f"{SP}/api/meta?id={uri}"], jar=True, timeout=60).stdout
    try:
        bm = json.loads(meta)[0]["book-meta"]
        title = bm["book-title-group"]["book-title"]
        year = bm["pub-date"][0]["year"]
    except (ValueError, KeyError, IndexError, TypeError):
        print(f"Scholars Portal did not describe {uri}: {meta[:200]!r}", file=sys.stderr)
        return 1
    sess = curl(["-o", "-", f"{SP}/api/session/{os.urandom(6).hex()}"], jar=True, timeout=60).stdout
    try:
        pem = base64.b64decode(json.loads(sess)["pk"])
    except (ValueError, KeyError):
        print(f"no session key from Scholars Portal: {sess[:200]!r}", file=sys.stderr)
        return 1
    with tempfile.NamedTemporaryFile("wb", suffix=".pem", delete=False) as kf:
        kf.write(pem)
    m2 = quote(json.dumps({"title": title, "pubYear": year}), safe="")
    parts = []
    try:
        for lo, hi in ranges:
            enc = subprocess.run(["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", kf.name],
                                 input=f"{uri}&{lo}&{hi}".encode(), capture_output=True, check=True).stdout
            token = quote(base64.b64encode(enc).decode(), safe="")
            part = dest.with_suffix(f".{lo}-{hi}.part")
            r = curl(["-o", str(part), "-w", "%{http_code}\t%{content_type}", f"{SP}/api/extract/{token}?meta={m2}"], jar=True, timeout=300)
            code, ctype = (r.stdout.strip().split("\t") + ["", ""])[:2]
            problem = None if "pdf" in ctype else f"HTTP {code}: {part.read_text(errors='ignore')[:200]!r}" if part.exists() else f"HTTP {code}"
            problem = problem or check_file(part, ".pdf")
            if problem:
                print(f"Scholars Portal refused pages {lo}-{hi}: {problem}", file=sys.stderr)
                for p in parts + [part]:
                    p.unlink(missing_ok=True)
                if not parts:
                    H.platform_session_release(ledger, "scholarsportal", previous)
                return 1
            parts.append(part)
        if len(parts) == 1:
            parts[0].replace(dest)
        else:                      # one PDF, in order; each part keeps its cover sheet
            subprocess.run(["pdfunite", *map(str, parts), str(dest)], check=True)
            for p in parts:
                p.unlink(missing_ok=True)
    finally:
        Path(kf.name).unlink(missing_ok=True)
    rel = str(dest.relative_to(H.HISTORY_DIR))
    print(f"{rel}  {dest.stat().st_size / 1e6:.1f} MB  reader pages {pages} of {title!r} ({year}); each range opens with a cover sheet")
    print(f"--local-file {rel}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="history-fetch.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    ap.add_argument("--topic", help="the topic slug; the file lands in db/history/<topic>/files/")
    ap.add_argument("--name", help="the file name: <topic>-<short>.<ext>, lowercase, no spaces")
    ap.add_argument("--ezproxy", action="store_true", help="go through the university library's EZproxy (publishers)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing file")
    ap.add_argument("--probe", action="store_true", help="report size and type only")
    ap.add_argument("--scholarsportal", metavar="URI", help="Scholars Portal book URI (/ebooks/...), with --pages")
    ap.add_argument("--pages", metavar="FROM-TO", help="reader page range for --scholarsportal, at most 53 pages")
    a = ap.parse_args(argv)

    if a.scholarsportal:
        if not (a.pages and a.topic and a.name):
            ap.error("--scholarsportal needs --pages, --topic and --name")
        if not a.name.endswith(".pdf"):
            ap.error("--name must end in .pdf")
        dest = H.HISTORY_DIR / H.slugify(a.topic) / "files" / a.name
        if dest.exists() and not a.force:
            print(f"already here: {dest.relative_to(H.HISTORY_DIR)}; --force to refetch")
            return 0
        dest.parent.mkdir(parents=True, exist_ok=True)
        return scholarsportal(a.scholarsportal, a.pages, dest)
    if not a.url:
        ap.error("a URL is needed")

    url = a.url
    proxied = a.ezproxy or needs_proxy(url)
    if proxied:
        url = ezproxy_url(url)
    if a.probe:
        print(json.dumps({**probe(url, proxied), "route": "ezproxy" if proxied else "direct"}, indent=1))
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

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    r = curl(["-o", str(tmp), "-w", "%{http_code}\t%{size_download}\t%{speed_download}", url], proxied)
    code, got, speed = (r.stdout.strip().split("\t") + ["", "0", "0"])[:3]
    if code == "429":
        # the host's limit on this address: one long wait and one more try
        # is cheaper than a researcher stopping its run
        time.sleep(60)
        r = curl(["-o", str(tmp), "-w", "%{http_code}\t%{size_download}\t%{speed_download}", url], proxied)
        code, got, speed = (r.stdout.strip().split("\t") + ["", "0", "0"])[:3]
    if r.returncode != 0 or not code.startswith("2"):
        tmp.unlink(missing_ok=True)
        print(f"fetch failed: HTTP {code or '?'} {r.stderr.strip()[:200]}", file=sys.stderr)
        if code == "429":
            print("the host is rate-limiting this campus address; this tool paces the whole crew, so wait a "
                  "minute and fetch again rather than looping, and fetch Commons files ONLY through this tool",
                  file=sys.stderr)
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
    print(f"{rel}  {n / 1e6:.1f} MB  {float(speed) / 1e3:.0f} kB/s")
    print(f"--local-file {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
