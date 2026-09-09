#!/usr/bin/env python3
"""Verify quoted phrases verbatim against the staged source texts."""
import re, sys, unicodedata, difflib, os

BASE = '/data/dev/arctic-history/db/history/frobisher/files/'
FILES = {
    'best': 'frobisher-best-1578-true-discourse.txt',
    'coll': 'frobisher-collinson-1867-three-voyages.txt',
    'hall2': 'frobisher-hall-1864-life-with-the-esquimaux.txt',
    'rgs': 'frobisher-hall-1862-rgs-frobisher-strait.txt',
    'chesh': 'frobisher-cheshire1980-eskimos-in-england.txt',
    'neatby': 'frobisher-neatby1983-arctic-profile.txt',
}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', ' ').replace('–', ' ').replace('-', ' ')
    s = s.lower()
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

TEXT = {}
for k, f in FILES.items():
    TEXT[k] = norm(open(BASE + f, encoding='utf-8', errors='replace').read())

def check(label, phrase, keys):
    n = norm(phrase)
    for k in keys:
        if n in TEXT[k]:
            print('OK      %-28s [%s]' % (label, k))
            return True
    # partial: find longest matching prefix
    best = (0, None, 0)
    for k in keys:
        t = TEXT[k]
        lo, hi = 0, len(n)
        # binary search longest prefix present
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if n[:mid] in t:
                lo = mid
            else:
                hi = mid - 1
        if lo > best[0]:
            best = (lo, k, 0)
    print('FAIL    %-28s longest prefix %d/%d chars in [%s]' % (label, best[0], len(n), best[1]))
    if best[0] > 20:
        k = best[1]
        i = TEXT[k].find(n[:best[0]])
        print('        source: ...%s' % TEXT[k][i:i+min(len(n)+80, 400)])
        print('        quoted: %s' % n)
    return False

if __name__ == '__main__':
    pass
