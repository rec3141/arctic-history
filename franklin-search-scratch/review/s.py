#!/usr/bin/env python3
"""s.py <file-substring> <pattern...>  -- collapse whitespace, regex search, print context."""
import sys, re, glob

fsub = sys.argv[1]
pats = sys.argv[2:]
paths = [p for p in glob.glob('db/history/franklin-search/files/*.txt') +
         glob.glob('db/history/_staging/*.txt') if fsub in p]
for p in paths:
    raw = open(p, encoding='utf-8', errors='replace').read()
    t = re.sub(r'[-‐]\s*\n\s*', '', raw)
    t = re.sub(r'\s+', ' ', t)
    for pat in pats:
        print('#### %s :: %s' % (p.split('/')[-1], pat))
        n = 0
        for m in re.finditer(pat, t, re.I):
            print('   ...' + t[max(0, m.start()-180):m.end()+180] + '...')
            n += 1
            if n >= 6:
                break
        if n == 0:
            print('   (none)')
