#!/usr/bin/env python3
"""Search the University of Manitoba Libraries catalogue from grid, no login.

RESEARCHER-ONLY: the Opus researcher runs this, never a Sonnet helper or a
Haiku reader (the brief, "Helpers and the web"). If you are a helper, stop
and report the need to your researcher instead.

    library-search.py "Arctic Justice Grant Pond Inlet"
    library-search.py --isbn 9780773523371
    library-search.py "Coats remarks Hudson's Bay 1852" --limit 8

For each record it prints what a researcher needs before filing a
``request --kind access``: the shelf copies (library, floor, call number,
available or not) and the electronic platforms the library licenses, each
marked with whether grid can reach it:

    reachable   fetch it with tools/history-fetch.py (Scholars Portal has its
                own mode there: see --scholarsportal in that tool's --help)
    browser     only the person's browser session can get at it (Canada
                Commons sits behind a bot check; EBSCO wants a login)
    no          the library lists it but the licence does not cover the
                text (De Gruyter chapters 303 to "unauthorized")

The data comes from Primo's public search API and Alma's link resolver, the
same calls the catalogue's own pages make. A record's electronic services
sometimes show fully only when signed in; if the shelf copy is there but no
platform is listed, say so in the request rather than concluding there is
no e-copy.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request

PRIMO = "https://search.lib.umanitoba.ca/primaws/rest/pub/pnxs"
RESOLVER = "https://ca01.alma.exlibrisgroup.com/view/uresolver/01UMB_INST/openurl"
VID, INST = "01UMB_INST:UMB", "01UMB_INST"
UA = "Mozilla/5.0 (X11; Linux x86_64) arctic-history library-search"

# what grid can do with each platform, learned the hard way on 2026-09-08
PLATFORMS = [
    ("scholarsportal", "Scholars Portal eBooks", "reachable", "53 pages per session; history-fetch.py --scholarsportal"),
    ("canadacommons", "Canada Commons", "browser", "10% of the title per download; needs the person's browser"),
    ("ebsco", "EBSCOhost eBooks", "browser", "needs a login"),
    ("proquest", "ProQuest Ebook Central", "browser", "needs a personal library login"),
    ("degruyter", "De Gruyter", "no", "front matter only; chapters unlicensed"),
    ("jstor", "JSTOR", "reachable", "through the proxy"),
    ("cambridge", "Cambridge Core", "reachable", "through the proxy"),
    ("tandfonline", "Taylor & Francis", "reachable", "through the proxy"),
    ("muse.jhu", "Project MUSE", "no", "login page through the proxy"),
    ("archive.org", "Internet Archive", "reachable", "open"),
    ("hathitrust", "HathiTrust", "reachable", "public-domain volumes only"),
    ("canadiana", "Canadiana", "reachable", "open"),
]


def get(url: str, timeout: int = 40) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json, text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def classify(name_or_url: str) -> tuple[str, str]:
    s = name_or_url.lower()
    for key, label, status, note in PLATFORMS:
        if key in s or label.lower() in s:
            return status, note
    return "unknown", "not seen before; try history-fetch.py --probe --ezproxy on the link"


def search(q: str, limit: int) -> list[dict]:
    qs = urllib.parse.urlencode({"vid": VID, "tab": "Everything", "scope": "MyInst_and_CI",
                                 "q": f"any,contains,{q}", "limit": limit, "offset": 0,
                                 "lang": "en", "inst": INST})
    return json.loads(get(f"{PRIMO}?{qs}")).get("docs", [])


def resolver_services(mms: str) -> list[tuple[str, str]]:
    """(service name, link) pairs Alma's link resolver shows without a login."""
    qs = urllib.parse.urlencode({"rft.mms_id": mms, "svc_dat": "viewit", "u.ignore_date_coverage": "true",
                                 "rfr_id": "info:sid/primo.exlibrisgroup.com", "req.skin": VID})
    try:
        page = get(f"{RESOLVER}?{qs}").decode("utf-8", "ignore")
    except Exception as e:                      # the resolver is a courtesy, not the point
        return [("(link resolver unreachable: %s)" % e, "")]
    text = re.sub(r"<script.*?</script>", "", page, flags=re.S)
    names = re.findall(r"Full text available at:\s*(?:<[^>]+>\s*)*([^<]{3,120})", text)
    return [(html.unescape(n).strip(), "") for n in names]


def show(doc: dict) -> None:
    p, d = doc["pnx"], doc.get("delivery", {})
    disp = p.get("display", {})
    rid = p.get("control", {}).get("recordid", [""])[0]
    title = (disp.get("title") or [""])[0]
    who = (disp.get("creator") or disp.get("contributor") or [""])[0].split("$$")[0]
    year = (disp.get("creationdate") or [""])[0]
    kind = (disp.get("type") or [""])[0]
    print(f"\n{title}\n  {who} | {year} | {kind} | {rid}")
    ids = disp.get("identifier") or []
    if ids:
        print("  " + "; ".join(i for i in ids if "ISBN" in i or "ISSN" in i)[:160])
    for h in d.get("holding") or []:
        print(f"  shelf: {h.get('mainLocation')}, {h.get('subLocation')}, {h.get('callNumber')} — {h.get('availabilityStatus')}")
    seen = set()
    for l in d.get("link") or []:
        if l.get("linkType") == "linktorsrc" and l.get("linkURL"):
            url = html.unescape(l["linkURL"])
            status, note = classify(url)
            seen.add(status + url)
            print(f"  online [{status}]: {url}\n      {note}")
    if rid.startswith("alma"):
        for name, _ in resolver_services(rid[4:]):
            status, note = classify(name)
            print(f"  licensed [{status}]: {name}\n      {note}")
    if not d.get("holding") and not any(l.get("linkType") == "linktorsrc" for l in d.get("link") or []) and not rid.startswith("alma"):
        avail = ",".join(d.get("availability") or [])
        print(f"  index record only ({avail or 'no availability given'}); the matching alma record, if any, is the one that counts")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="library-search.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?", help="words from the title, author, place")
    ap.add_argument("--isbn", help="search by ISBN instead")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--json", action="store_true", help="dump the raw records")
    a = ap.parse_args(argv)
    q = a.isbn or a.query
    if not q:
        ap.error("give a query or --isbn")
    try:
        docs = search(q, a.limit)
    except Exception as e:
        sys.exit(f"catalogue search failed: {e}")
    if a.json:
        json.dump(docs, sys.stdout, indent=1)
        return 0
    if not docs:
        print("nothing found")
        return 1
    print(f"{len(docs)} records for {q!r} (alma records are the library's own holdings; cdi records are index entries)")
    for doc in docs:
        show(doc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
