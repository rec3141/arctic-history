import sqlite3, textwrap, sys
sys.path.insert(0, 'relocations-qtc-scratch/review')
from patch import patch

c = sqlite3.connect('db/history/history.sqlite')
OUT = 'relocations-qtc-scratch/review/bodies/%s.md'


def get(slug):
    return c.execute("select body from pages where slug=?", (slug,)).fetchone()[0]


def sub(s, old, new, tag):
    assert old in s, tag
    return s.replace(old, new, 1)


def flow(t, w=78):
    return textwrap.fill(' '.join(t.split()), w)


# ---------------- qimmiit ----------------
s = get('relocations-the-killing-of-the-qimmiit')
s = sub(s, ('places the qimmiit inside the larger pattern — "government domination and\n'
            'interference with Inuit decision-making" — and its Commissioner recommended\n'
            'that Canada formally acknowledge that today\'s rates of suicide, substance abuse\n'
            'and incarceration among Inuit are in part symptoms of intergenerational trauma\n'
            'caused by historical wrongs.'),
        flow('places the qimmiit inside the larger pattern — "government domination and '
             'interference with Inuit decision-making" — and it ends on the Commissioner\'s '
             'recommendation that the Government of Canada formally acknowledge "that the '
             'high rates of suicide, substance abuse, incarceration, and social dysfunction '
             'among Inuit are in part symptoms of intergenerational trauma caused by '
             'historical wrongs."'), 'qimmiit rec')
open(OUT % 'relocations-the-killing-of-the-qimmiit', 'w').write(s)

# ---------------- tb ----------------
s = get('relocations-the-ships-that-took-people-south')
s = sub(s, ('National Health and Welfare — which had, in the whole of what is now Nunavut,\n'
            'two hospitals and forty-eight beds for a little under four thousand people. The Eastern Arctic Patrol, which had been\n'
            'running since 1922 as a sovereignty and supply voyage, became the instrument.'),
        flow('National Health and Welfare — which had, in the whole of what is now Nunavut, '
             'two hospitals and forty-eight beds for a little under four thousand people. '
             'The Eastern Arctic Patrol, which had been running since 1922 as a sovereignty '
             'and supply voyage, became the instrument.'), 'tb reflow')
s = sub(s, ('six beds, and radar, echo sounding and a helicopter for moving people between\n'
            'ship and shore. Her route is\n'
            '[[artifact:relocations-qtc-028]].'),
        flow('six beds, and radar, echo sounding and a helicopter for moving people between '
             'ship and shore. Her route is [[artifact:relocations-qtc-028]].'), 'tb howe reflow')
open(OUT % 'relocations-the-ships-that-took-people-south', 'w').write(s)

# ---------------- settlements ----------------
s = get('relocations-moving-into-the-settlements')
s = sub(s, ('times as many people lived in just thirteen of them. The QTC\'s\n'
            'thematic report on the moves, [[source:qtc2013nuutauniq|*Nuutauniq*]], is about'),
        ('times as many people lived in just thirteen of them. The QTC\'s thematic report on\n'
         'the moves, [[source:qtc2013nuutauniq|*Nuutauniq*]], is about'), 'set reflow 1')
s = sub(s, ('wages, and they believed it. [[person:Gene Rheaume]], active in the North as both civil\n'
            'servant and politician, put it: "It was [sometimes] a subtle pressure, but it was\n'
            'coming at you from everywhere."'),
        flow('wages, and they believed it. [[person:Gene Rheaume]], active in the North as '
             'both civil servant and politician, put it: "It was [sometimes] a subtle '
             'pressure, but it was coming at you from everywhere."'), 'set reflow 2')
open(OUT % 'relocations-moving-into-the-settlements', 'w').write(s)

# ---------------- saimaqatigiingniq ----------------
s = get('relocations-saimaqatigiingniq')
s = sub(s, ('decision taken in Ottawa in 1953. The people who were carried there are named in\n'
            '[[artifact:relocations-qtc-016]] and some of them are still alive;'),
        ('decision taken in Ottawa in 1953. The families put ashore at Qausuittuq are named\n'
         'one by one in [[artifact:relocations-qtc-016]], and some of them are still alive;'),
        'saimaq 016')
open(OUT % 'relocations-saimaqatigiingniq', 'w').write(s)

# ---------------- qausuittuq ----------------
s = get('relocations-qausuittuq')
s = sub(s, ('and had to beg accommodation and cartage off the RCAF. Ottawa\'s answer came from [[person:James Cantley]], an advisor for the\n'
            'relocation experiment ([[artifact:relocations-qtc-049]]): the families had been\n'
            'living in those tents before, so conditions could not be worse than what they\n'
            'had left.'),
        flow('and had to beg accommodation and cartage off the RCAF. Ottawa\'s answer came '
             'from [[person:James Cantley]], an advisor for the relocation experiment '
             '([[artifact:relocations-qtc-049]]): the families had been living in those tents '
             'before, so conditions could not be worse than what they had left.'), 'qau cantley')

s = sub(s, ('[[person:Levi Nungak]] and [[person:Alacee Nungaq]] with their four\n'
            'children,'),
        ('[[person:Levi Nungak]] and his wife Alici — [[person:Alacee Nungaq]] in Library\n'
         'and Archives Canada\'s caption — with their four children,'), 'qau nungak')

s = sub(s, ('by 1964. Gar Lunney photographed one of the 1955 households outside in March 1956 —\n'
            'Alici Nungak, whom Library and Archives Canada\'s caption calls\n'
            '[[person:Alacee Nungaq]], in an amauti with three of her children, the\n'
            'scrap-built houses behind her ([[artifact:relocations-qtc-045]]).\n'
            '[[person:Martha Flaherty]] told RCAP what the same years felt like:'),
        flow('by 1964. Gar Lunney photographed the Nungak household outside in March 1956 — '
             'Alici in an amauti with three of her children, the scrap-built houses behind '
             'her ([[artifact:relocations-qtc-045]]). [[person:Martha Flaherty]] told RCAP '
             'what the same years felt like:'), 'qau lunney')

s = sub(s, ('([[artifact:relocations-qtc-053]]). The community was then about thirty-five\n'
            'people. In\n'
            '1957 the ship arrived with measles aboard, put the infected passengers ashore\n'
            'near the settlement, and infected it.'),
        flow('([[artifact:relocations-qtc-053]]). Twenty-two people had been landed in 1953, '
             'so that was a large fraction of the community. In 1957 the ship arrived with '
             'measles aboard, put the infected passengers ashore near the settlement, and '
             'infected it.'), 'qau tb')

s = sub(s, ('built. In the summer of 1975 every useful building except those in the airport area\n'
            'was hauled roughly three kilometres from the west shore of the bay to the east. The old site was left with\n'
            'the cemetery. [[person:Saroomie Manik]] told the Commission she was sorry they'),
        flow('built. In the summer of 1975 every useful building except those in the airport '
             'area was hauled roughly three kilometres from the west shore of the bay to the '
             'east. The old site was left with the cemetery and a few unusable buildings. '
             '[[person:Saroomie Manik]] told the Commission she was sorry they'), 'qau 1975')

s = sub(s, ('that produced Nunavut; [[person:Simeonie Amagoalik]] spoke for the community against the seismic\n'
            'testing and mining near Resolute, and the political engagement of Qausuitturmiut\n'
            'and of Inuit organizations delayed the opening of Cominco\'s Avarik (Polaris)\n'
            'mine until 1980. In 1974\n'
            '[[person:Simeonie Amarualik]], [[person:Walter Audla]] and'),
        flow('that produced Nunavut; [[person:Simeonie Amagoalik]] spoke for the community '
             'against the seismic testing and mining near Resolute, and the political '
             'engagement of Qausuitturmiut and of Inuit organizations delayed the opening of '
             'Cominco\'s Avarik (Polaris) mine until 1980. In 1974 '
             '[[person:Simeonie Amarualik]], [[person:Walter Audla]] and'), 'qau politics')
open(OUT % 'relocations-qausuittuq', 'w').write(s)

# ---------------- artifact 053 ----------------
patch('relocations-qtc-053', description=(
    'John Amagoalik on the tuberculosis years at Qausuittuq. The C. D. Howe called once a year to '
    'x-ray and vaccinate and to decide who would go south. In his memoir, quoted by the Qikiqtani '
    'Truth Commission: "[Tuberculosis] was a scourge in our communities then. Many of our parents '
    'ended up getting back on the ship and getting shipped out to recover in southern hospitals. I '
    'think in the first two years, about five or six adults and some children were taken on the ship '
    'and sent south. My older brother was one of them, and my mother was another . . . My younger '
    'brother Jimmy was away for two years. Later I was also treated at the Charles Camsell Hospital '
    'in Edmonton for two years." Twenty-two people were landed at Qausuittuq in 1953, so five or six '
    'adults and some children is a large fraction of the community he is describing. The date is the '
    'second year after the landing, as the passage says.'))

print('done')
