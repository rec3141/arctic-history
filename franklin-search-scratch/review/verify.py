#!/usr/bin/env python3
"""Verify quoted strings against the OCR texts on disk."""
import os, re, sys, glob, unicodedata

FILES = {}
paths = sorted(glob.glob('db/history/franklin-search/files/*.txt')) + \
        sorted(glob.glob('db/history/_staging/*.txt')) + \
        sorted(glob.glob('db/history/franklin-1845/files/*.txt'))

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-').replace('‐','-')
    s = s.replace('…', ' ... ')
    s = re.sub(r'[̀-ͯ]', '', s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' ' + s.strip() + ' '

for p in paths:
    try:
        raw = open(p, encoding='utf-8', errors='replace').read()
        FILES[p] = norm(raw)
        # de-hyphenated variant: join words broken across lines
        FILES[p + '#dehyph'] = norm(re.sub(r'[-‐‑]\s*\n\s*', '', raw))
    except Exception as e:
        print('SKIP', p, e)

def find(q):
    parts = [x for x in re.split(r'\s*(?:\.\.\.|…)\s*', q) if x.strip()]
    hits = []
    for p, txt in FILES.items():
        ok = all(norm(part).strip() in txt for part in parts)
        if ok:
            hits.append(os.path.basename(p))
    return hits

if __name__ == '__main__':
    data = sys.stdin.read()
    for line in data.split('\n'):
        line = line.rstrip()
        if not line.strip():
            continue
        if line.startswith('#'):
            print(line); continue
        h = find(line)
        print(('OK   ' if h else 'MISS ') + ('|'.join(h[:3]) if h else '') + ' :: ' + line[:100])
