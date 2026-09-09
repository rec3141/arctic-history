#!/usr/bin/env python3
"""Verify quoted phrases against staged source texts, tolerant of OCR line noise.

Strategy: strip everything but [a-z0-9], then look for the quote as a subsequence
window; report the source window so a human can judge the differences.
"""
import re, unicodedata, difflib

BASE = '/data/dev/arctic-history/db/history/frobisher/files/'
FILES = {
    'best': 'frobisher-best-1578-true-discourse.txt',
    'coll': 'frobisher-collinson-1867-three-voyages.txt',
    'hall2': 'frobisher-hall-1864-life-with-the-esquimaux.txt',
    'rgs': 'frobisher-hall-1862-rgs-frobisher-strait.txt',
    'chesh': 'frobisher-cheshire1980-eskimos-in-england.txt',
    'neatby': 'frobisher-neatby1983-arctic-profile.txt',
    'blackstone': 'frobisher-arctic-1987-blackstone.txt',
}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    for a, b in [('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'),
                 ('—', ' '), ('–', ' ')]:
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s.lower())

def squash(s):
    return re.sub(r'[^a-z0-9]', '', norm(s))

RAW, SQ, MAP = {}, {}, {}
for k, f in FILES.items():
    try:
        t = open(BASE + f, encoding='utf-8', errors='replace').read()
    except FileNotFoundError:
        continue
    RAW[k] = t
    n = norm(t)
    sq = []
    idx = []
    for i, ch in enumerate(n):
        if ch.isalnum():
            sq.append(ch)
            idx.append(i)
    SQ[k] = ''.join(sq)
    MAP[k] = idx
    globals().setdefault('NORM', {})[k] = n

def best_window(k, q):
    """Return (ratio, source_excerpt) for the best matching window in file k."""
    sq = SQ[k]
    # anchor on the first 24 squashed chars if possible, else 12
    for alen in (30, 20, 12, 8):
        anchor = q[:alen]
        starts = [m.start() for m in re.finditer(re.escape(anchor), sq)]
        if starts:
            break
    else:
        starts = []
    best = (0.0, '')
    if not starts:
        # fall back: slide with difflib on chunks
        return (0.0, '')
    for s in starts:
        for pad in (0, 40, 80, 140):
            w = sq[s:s + len(q) + pad]
            r = difflib.SequenceMatcher(None, q, w).ratio()
            if r > best[0]:
                lo = MAP[k][s]
                hi = MAP[k][min(s + len(q) + pad, len(MAP[k]) - 1)]
                best = (r, NORM[k][lo:hi])
    return best

def check(label, phrase, keys, thresh=0.985):
    q = squash(phrase)
    results = []
    for k in keys:
        if k not in SQ:
            continue
        if q in SQ[k]:
            print('EXACT   %-28s [%s]' % (label, k))
            return True
        results.append((best_window(k, q) + (k,)))
    results.sort(reverse=True)
    if not results or results[0][0] == 0.0:
        print('NOTFOUND %-27s in %s' % (label, keys))
        return False
    r, win, k = results[0]
    tag = 'OCRVAR' if r >= thresh else 'DIFF  '
    print('%s  %-28s [%s] ratio=%.4f' % (tag, label, k, r))
    if r < 0.999:
        sm = difflib.SequenceMatcher(None, q, squash(win))
        ops = [o for o in sm.get_opcodes() if o[0] != 'equal']
        for op, i1, i2, j1, j2 in ops[:12]:
            print('        %-8s quoted=%r source=%r' % (op, q[max(0,i1-12):i2+12], squash(win)[max(0,j1-12):j2+12]))
    return r >= thresh
