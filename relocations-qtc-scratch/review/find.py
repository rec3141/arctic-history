#!/usr/bin/env python3
"""Verbatim phrase search across the QTC/RCAP texts on disk, whitespace-normalised."""
import sys, re, glob, os

FILES = {}
for p in glob.glob('db/history/_staging/qtc-*.txt') + glob.glob('db/history/_staging/rcap-*.txt') + \
         glob.glob('db/history/relocations-qtc/files/*.txt') + \
         glob.glob('db/history/relocations-qtc/files/*.html'):
    try:
        FILES[p] = open(p, encoding='utf-8', errors='replace').read()
    except Exception as e:
        print('ERR', p, e)

def norm(s):
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-').replace('‐', '-')
    s = s.replace(' ', ' ').replace('ﬁ', 'fi').replace('ﬂ', 'fl')
    s = re.sub(r'\s+', ' ', s)
    return s.lower()

NORM = {p: norm(t) for p, t in FILES.items()}

def find(phrase, only=None):
    q = norm(phrase)
    hits = []
    for p, t in NORM.items():
        if only and only not in p:
            continue
        i = t.find(q)
        while i >= 0:
            hits.append((p, i))
            i = t.find(q, i + 1)
    return hits

if __name__ == '__main__':
    phrase = sys.argv[1]
    only = sys.argv[2] if len(sys.argv) > 2 else None
    h = find(phrase, only)
    if not h:
        print('NOT FOUND:', phrase[:90])
    for p, i in h:
        print('HIT', p, i)
        print('   ...', NORM[p][max(0, i-200):i+len(norm(phrase))+200])
