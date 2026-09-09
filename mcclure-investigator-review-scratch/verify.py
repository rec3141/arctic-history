#!/usr/bin/env python3
"""Normalised phrase search in the on-disk texts."""
import re, sys, unicodedata, pathlib

BASE = pathlib.Path('/data/dev/arctic-history/db/history/mcclure-investigator/files')
FILES = {
    'osborn':      'mcclure-investigator-osborn1856-mcclure.txt',
    'armstrong':   'mcclure-investigator-armstrong1857.txt',
    'collinson':   'mcclure-investigator-collinson1889.txt',
    'bluebook':    'mcclure-investigator-bluebook1855.txt',
    'mcdougall':   'mcclure-investigator-mcdougall1857.txt',
    'miertsching': 'mcclure-investigator-miertsching1855-de.txt',
}
_cache = {}

def norm(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace('—', '-').replace('–', '-').replace('‐', '-')
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def load(key):
    if key not in _cache:
        raw = (BASE / FILES[key]).read_text(errors='replace')
        _cache[key] = (raw, norm(raw))
    return _cache[key]

def find(key, phrase, ctx=160):
    raw, n = load(key)
    p = norm(phrase)
    hits = [m.start() for m in re.finditer(re.escape(p), n)]
    return p, hits, n

if __name__ == '__main__':
    key = sys.argv[1]
    phrase = sys.argv[2]
    p, hits, n = find(key, phrase)
    print(f'[{key}] {len(hits)} hit(s) for: {p[:90]}')
    for h in hits[:3]:
        print('   ...', n[max(0, h-100):h+len(p)+100], '...')
