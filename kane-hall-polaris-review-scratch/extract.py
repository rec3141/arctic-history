#!/usr/bin/env python3
import re, sys, glob, os
out = []
for f in sorted(glob.glob('/data/dev/arctic-history/kane-hall-polaris-review-scratch/*.txt')):
    base = os.path.basename(f)[:-4]
    txt = open(f, encoding='utf-8').read()
    lines = txt.split('\n')
    for i, line in enumerate(lines, 1):
        # strip wikilinks to their display text
        l = re.sub(r'\[\[[^\]|]*\|([^\]]*)\]\]', r'\1', line)
        l = re.sub(r'\[\[([a-z]+):([^\]]*)\]\]', r'\2', l)
        for m in re.finditer(r'"([^"]{25,})"', l):
            out.append((f'{base}:{i}', m.group(1)))
        # italic quote lines
        for m in re.finditer(r'^>\s*\*([^*]{25,})\*', l):
            out.append((f'{base}:{i}', m.group(1)))
for label, q in out:
    print(label)
    print(q)
    print('@@')
