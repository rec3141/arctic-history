#!/usr/bin/env python3
"""Verify quotations against the texts on disk (normalised, elision-aware)."""
import re, sys, unicodedata, os, glob

FILES = sorted(glob.glob('/data/dev/arctic-history/db/history/kane-hall-polaris/files/*.txt'))
FILES += sorted(glob.glob('/data/dev/arctic-history/db/history/_staging/khp/*.txt'))

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-').replace('‐', '-')
    s = s.replace('°', ' deg ').replace('′', ' min ').replace("´", ' min ')
    s = re.sub(r'-\s*\n\s*', '', s)
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    s = re.sub(r'\b(deg|min|degrees|minutes)\b', ' ', s)   # ° / ' notation varies
    return re.sub(r'\s+', ' ', s).strip()

CORPUS = {}
for f in FILES:
    CORPUS[os.path.basename(f)] = norm(open(f, encoding='utf-8', errors='replace').read())

def segments(q):
    q = re.sub(r'\[[^\]]*\]', ' ... ', q)          # editorial insertions
    parts = re.split(r'\.\.\.|…', q)
    return [p for p in (norm(x) for x in parts) if len(p.split()) >= 3]

def check(q):
    segs = segments(q)
    if not segs:
        return None, []
    bad = []
    files_ok = None
    for s in segs:
        hits = set(k for k, v in CORPUS.items() if s in v)
        if not hits:
            bad.append(s)
        else:
            files_ok = hits if files_ok is None else (files_ok & hits) or files_ok
    return files_ok, bad

def localise(s):
    words = s.split()
    lo, hi, best = 0, len(words), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        probe = ' '.join(words[:mid])
        if any(probe in v for v in CORPUS.values()):
            best = mid; lo = mid + 1
        else:
            hi = mid - 1
    return best, words

if __name__ == '__main__':
    data = sys.stdin.read()
    nok = nbad = 0
    for block in data.split('\n@@\n'):
        block = block.strip()
        if not block:
            continue
        label, _, q = block.partition('\n')
        files_ok, bad = check(q)
        if files_ok is None and not bad:
            continue
        if not bad:
            nok += 1
            print(f'OK    {label}  -> {", ".join(sorted(files_ok)[:2])}')
        else:
            nbad += 1
            print(f'FAIL  {label}')
            for s in bad:
                best, words = localise(s)
                print(f'      seg: {s[:110]}')
                print(f'      matched {best}/{len(words)}; breaks at: {" ".join(words[best:best+10])}')
    print(f'\n{nok} ok, {nbad} failing', file=sys.stderr)
