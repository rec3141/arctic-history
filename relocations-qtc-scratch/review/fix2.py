import sqlite3, textwrap, subprocess, sys
sys.path.insert(0, 'relocations-qtc-scratch/review')
from patch import patch

c = sqlite3.connect('db/history/history.sqlite')


def body(slug):
    return c.execute("select body from pages where slug=?", (slug,)).fetchone()[0]


def write(slug, b):
    open('relocations-qtc-scratch/review/bodies/%s.md' % slug, 'w').write(b)


# --- overview: restore the QTC's exact wording of saimaqatigiingniq, and reflow ---
s = body('relocations-overview')
old = ('- **saimaqatigiingniq** — "when past opponents get back together, meet in the\n'
       '  middle, and are at peace." It is the Commission\'s name for what it was\n'
       '  trying to reach, and the title of its final report is *Achieving\n'
       '  Saimaqatigiingniq*.')
new = ('- **saimaqatigiingniq** — "when past opponents get back together, meet in the\n'
       '  middle, are at peace." It is the Commission\'s name for what it was trying to\n'
       '  reach, and the title of its final report is *Achieving Saimaqatigiingniq*.')
assert old in s, 'overview saimaq'
s = s.replace(old, new)

old = ('and Reconciliation Commission of Canada. The QTC\'s community histories for Ausuittuq and Qausuittuq tell the\n'
       'relocation story anyway, because it is their founding story, but the weight on\n'
       'the 1953-55 material here rests on\n'
       '[[source:rcap1994high|RCAP\'s 1994 report]] and the testimony given to it.')
assert old in s, 'overview reflow'
s = s.replace(old, textwrap.fill(' '.join(old.split()), 78))

old = ('south, and in 1956, the QTC reckons, one Inuk in seven was in a hospital in\n'
       'southern Canada. Some were away for years; some\n'
       'never came back, and their families were not told where they were buried. See')
assert old in s, 'overview tb reflow'
s = s.replace(old, ('south, and in 1956, the QTC reckons, one Inuk in seven was in a hospital in\n'
                    'southern Canada. Some were away for years; some never came back, and their\n'
                    'families were not told where they were buried. See'))
write('relocations-overview', s)

# --- 1953-55: the plaque's own spelling of the assistant sculptor, and a reflow ---
s = body('relocations-the-1953-and-1955-high-arctic-relocations')
assert 'with Matt Pijamini' in s
s = s.replace('with Matt Pijamini', 'with Matthew Pijamini')
old = ('the detachment to Grise Fiord in 1956. It was badly supplied. [[person:Rynee Flaherty]], who came\n'
       'in 1955, told RCAP how she had tried to feed her infant son on flour and water')
assert old in s, '1953 reflow'
s = s.replace(old, ('the detachment to Grise Fiord in 1956. It was badly supplied.\n'
                    '[[person:Rynee Flaherty]], who came in 1955, told RCAP how she had tried to\n'
                    'feed her infant son on flour and water'))
write('relocations-the-1953-and-1955-high-arctic-relocations', s)

print('bodies written')

patch('relocations-qtc-041', description=c.execute(
    "select description from artifacts where id='relocations-qtc-041'").fetchone()[0]
    .replace('with Matt Pijamini as apprentice', 'with Matthew Pijamini as assistant sculptor'))
