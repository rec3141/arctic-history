import sys,os
D='place-names-scratch/pages/'
def fix(slug, *pairs):
    p=D+slug+'.md'; t=open(p).read(); orig=t
    for old,new in pairs:
        if old not in t:
            print('  !! NOT FOUND in %s: %r' % (slug, old[:70])); continue
        if t.count(old)>1: print('  !! %d occurrences in %s: %r' % (t.count(old),slug,old[:50]))
        t=t.replace(old,new,1)
    open(p,'w').write(t)
    print('%s %s' % (slug, 'changed' if t!=orig else 'UNCHANGED'))
