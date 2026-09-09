#!/usr/bin/env python3
"""Normalised substring search in an OCR text: collapse whitespace, unify quotes/dashes."""
import re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("‘", "'").replace("’", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("—", "-").replace("–", "-").replace("‑", "-")
    s = re.sub(r"[^A-Za-z0-9'\".,;:!?()\[\]/&%$#*+=<>-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

path, needle = sys.argv[1], sys.argv[2]
hay = norm(open(path, encoding="utf-8", errors="replace").read())
hay = re.sub(r"(\w)- (\w)", r"\1\2", hay)  # join words broken across lines
n = norm(needle)
i = hay.find(n)
if i < 0:
    print("NOT FOUND:", n[:120])
    # try progressively shorter prefixes to locate where it diverges
    lo, hi = 0, len(n)
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if hay.find(n[:mid]) >= 0:
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    print("longest matching prefix (%d chars): %r" % (best, n[:best]))
    j = hay.find(n[:best]) if best else -1
    if j >= 0:
        print("context:", hay[max(0, j-100):j+best+250])
else:
    print("FOUND at %d" % i)
    print("context:", hay[max(0, i-160):i+len(n)+160])
