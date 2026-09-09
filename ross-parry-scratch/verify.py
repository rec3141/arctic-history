#!/usr/bin/env python3
"""Verify quotations verbatim against the staged OCR texts.

Normalises whitespace, quotes, dashes and the long s so that a phrase can be
found across line breaks; reports the surrounding context for eyeballing.
"""
import re
import sys
import unicodedata

STAGE = "/data/dev/arctic-history/db/history/_staging/txt/"

FILES = {
    "ross": "voyageofdiscover00ross.txt",
    "parry1": "journalofvoyagef00inparr.txt",
    "parry2": "journalofsecondv00parr.txt",
    "parry3": "gut26509.txt",
    "lyonpriv": "privatejournalc01lyongoog.txt",
    "lyonbrief": "briefnarrativeof00lyon_0.txt",
    "fisher": "journalofvoyageo00fishrich.txt",
    "gazette": "northgeorgiagaze00unse.txt",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("ſ", "s")           # long s
    s = re.sub(r"[‘’'`ʼ]", "'", s)
    s = re.sub(r"[“”\"]", '"', s)
    s = re.sub(r"[‐-―−-]+", "-", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)    # drop punctuation entirely
    s = re.sub(r"\s+", " ", s)
    return s


CACHE = {}


def text(key):
    if key not in CACHE:
        with open(STAGE + FILES[key], encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        CACHE[key] = (raw, norm(raw))
    return CACHE[key]


def squash(s):
    """letters and digits only - defeats OCR word splits like 'coun cil'."""
    return re.sub(r"[^a-z0-9]+", "", s)


def find(key, phrase, ctx=160):
    raw, n = text(key)
    p = norm(phrase)
    i = n.find(p)
    if i >= 0:
        return i, n[max(0, i - ctx):i + len(p) + ctx], "exact"
    # second pass: ignore all spacing, to survive OCR word splits
    ns, ps = squash(n), squash(p)
    j = ns.find(ps)
    if j >= 0:
        # map back approximately: count non-space chars
        return j, "(spacing-insensitive match)", "spaced"
    return -1, "", "no"


def main():
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        key, phrase = line.split("\t", 1)
        i, ctx, how = find(key, phrase)
        if i >= 0:
            print("OK(%s) [%s] %s" % (how[:5], key, phrase[:70]))
        else:
            print("MISS  [%s] %s" % (key, phrase))
            # try to locate the longest matching prefix, to show where it diverges
            raw, n = text(key)
            p = norm(phrase)
            lo, hi = 0, len(p)
            best = 0
            while lo <= hi:
                mid = (lo + hi) // 2
                if n.find(p[:mid]) >= 0:
                    best = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            j = n.find(p[:best])
            print("      matched %d/%d chars: ...%s..." % (best, len(p), n[max(0, j - 40):j + best + 120]))


if __name__ == "__main__":
    main()
