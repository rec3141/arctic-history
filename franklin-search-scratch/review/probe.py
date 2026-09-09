#!/usr/bin/env python3
import sys, re, os
sys.path.insert(0, 'franklin-search-scratch/review')
from verify import FILES, norm

def probe(q, ctx=260):
    parts = [x for x in re.split(r'\s*(?:\.\.\.|…)\s*', q) if x.strip()]
    print('=== ' + q[:120])
    for part in parts:
        n = norm(part).strip()
        words = n.split()
        found = False
        # try longest prefix that matches somewhere
        for L in range(len(words), 2, -1):
            frag = ' ' + ' '.join(words[:L]) + ' '
            hit = [(p, t.find(frag)) for p, t in FILES.items() if frag in t]
            if hit:
                p, i = hit[0]
                print('  matched %d/%d words in %s' % (L, len(words), os.path.basename(p)))
                print('  ...' + FILES[p][max(0, i-40):i+len(frag)+ctx] + '...')
                found = True
                break
        if not found:
            print('  NOTHING for: ' + part[:80])

for line in sys.stdin.read().split('\n'):
    if line.strip():
        probe(line)
