# Display note: polar bear

For the operator and the front end. What the polar-bear record should look like on
the tab, which fields drive it, and which static plate stands in for it now.

## What is in the rows

About 640 observations, all of subject `Ursus maritimus`. Four populations of row,
and they want different treatment:

1. **Narrative encounters, 1818-1944** (about 75 rows). `method` is `hunt`,
   `sighting` or `testimony`; most carry `count` as written rather than a number,
   and `behaviour`, `stage`, `sex` where the text gave them. These are points on a
   map and lines in a log, not a series.
2. **Survey and assessment rows** (about 25). `method` `aerial-survey`, `survey`
   or `catch-record`; these carry `value` and `unit` (`bears`, `bears per year`)
   and are the only rows the arithmetic should touch.
3. **Knowledge rows** (about 45). `method` `testimony`, the observer an elder, a
   hunter or a named community group rather than the ethnographer who wrote it
   down: Aua and Ivaluardjuk at Iglulik, Maisanguaq and Sorqaq among the Inughuit,
   Manelaq, Nakasuk and Sammik among the Netsilingmiut, the Qikiqtani communities,
   COSEWIC's Indigenous Knowledge chapter. They carry a date range or a year of
   recording rather than a date of sighting, and several have no useful position
   beyond the district. They belong beside the prose on
   [[page:nanuq-the-hunt-and-the-knowledge]], not on a chart; where a widget shows
   them at all it should be the map layer, drawn as a district and not a point.
4. **Occurrence photographs** (about 350). `method` `camera`, each paired with the
   image artifact it came from and each carrying a real position and date. These
   are the only rows dense enough for a modern-distribution layer, and they must
   never be mixed into the historical encounter counts: they are observer effort,
   not abundance.

Nine rows are `sensitive` (dens). They must publish coarsened, and no widget may
group or label by place for those rows.

## Widgets

    {"kind": "layer", "subject": "Ursus maritimus", "domain": "biology",
     "since": "1818", "until": "2026",
     "group_by": "method", "title": "Every bear in the record, and how it was recorded"}

The first thing a scientist aboard should get. The map layer for this topic,
coloured by `method` so that a kill, a sighting, a track and a survey point read
differently, with the date slider running the whole two centuries. Standing in for
it now: [[artifact:polar-bear-520]].

    {"kind": "bars", "subject": "Ursus maritimus", "y": "value", "unit": "bears",
     "group_by": "place", "since": "1992", "until": "2026",
     "title": "The subpopulation estimates, newest first"}

Bars of the seven archipelago and Baffin Bay stocks from the `survey` rows, each
labelled with the year its estimate refers to — the year matters more than the
number here, because Lancaster Sound's is 1997 and Baffin Bay's is 2013. The
`compare` block should hold the 1997 COSEWIC management figures so the two sit
together:

    {"kind": "bars", "subject": "Ursus maritimus", "y": "value", "unit": "bears",
     "group_by": "place", "since": "2010", "until": "2026",
     "compare": {"subject": "Ursus maritimus", "since": "1997", "until": "1997"},
     "title": "What a survey found where a guess had stood"}

Standing in for it now: [[artifact:polar-bear-521]].

    {"kind": "strip", "subject": "Ursus maritimus", "x": "date_start",
     "group_by": "method", "since": "1818", "until": "1961",
     "title": "Two centuries of encounters, by month and by kind"}

The phenology strip: every dated encounter placed on the month axis, banded by
method. It carries a caution that must be shown with it — the shape is the
expeditions' travelling year, not the bear's year, and the November-to-February
gap is the polar night, not an absence of bears. Standing in for it now:
[[artifact:polar-bear-522]].

    {"kind": "bars", "subject": "Ursus maritimus", "y": "value", "unit": "bears",
     "x": "date_start", "since": "1780", "until": "2026",
     "title": "Bears taken, as the catch records give them"}

The `catch-record` rows only: Scoresby's Hull fleet of 1788, Milne's SS Esquimaux
of 1885, 1887 and 1888, the First Grinnell Expedition's nine of twenty-six seen,
Osborn's eight of 1850, the Canadian quota of 1995-96 and the 2016-17 removal.
Sparse and heterogeneous: it must be drawn as separate dated marks with their
sources, never as a continuous series, because these are different fleets and
different geographies and the gaps are not zeroes.

## The community rows, and how not to chart them

The fifteen rows from the 2005 Baffin Bay community study (`bibkey`
`dowsley2005inuit`) carry percentages in `count` rather than in `value`, on
purpose: they are proportions of the people who answered a question in one of
three communities, not measurements of bears. Nothing should average them,
put them on a time axis, or draw them beside the survey estimates as though the
two were the same kind of number. They belong beside the prose, and beside the
sea-ice series where a scientist aboard can see what they line up with:

    {"kind": "layer", "subject": "Ursus maritimus", "place": "Baffin Bay polar bear subpopulation",
     "since": "2005", "until": "2005", "group_by": "place",
     "title": "What the three harvesting communities said in 2005"}

The comparisons worth making are stated in the rows themselves and should be
shown as text: 84.78 per cent of forty-six elders and hunters said the bears had
increased over the previous ten to fifteen years, while the model of the same
years had the subpopulation falling from 2,074 to about 1,700; and the ice
statements (the floe edge closer, the ice thinner, break-up two weeks earlier and
freeze-up two weeks later) can be put against whatever series
[[topic:the-sea-ice]] holds for the same water and the same years. Where the two
disagree, the tab should show both and say who said which.

## Units and conversions

Numbers are entered as written. Three units appear: `bears` (a count or an
estimate), `bears per year` (a quota or a removal), and the physical measurements
`lbs`, `feet` and `inches` on the two bears that were measured (Ross 1818, Bellot
1851). For the physical rows the display should show the original with the metric
beside it: 1,131 lb = 513 kg; 7 ft 8 in = 2.34 m; 8 ft 6 in = 2.59 m. Nothing else
needs converting.

## What a scientist aboard would compare it with

- The ship's own bear sightings, journalled from the bridge, dropped onto the same
  map layer beside Parry's and Kane's. That is the comparison the layer exists for.
- The Baffin Bay sea-ice metrics: spring retreat 5.6 days per decade earlier,
  autumn advance 4.1 days per decade later, summer area down 21.5 per cent per
  decade since 1979. If [[topic:the-sea-ice]] holds a series for the ship's
  current position, the bear layer should be able to sit on top of it.
- The seal record in [[topic:walrus-and-seals]]: the bear's numbers are the seals'
  numbers with a lag, and the two topics should be layerable together.
- The subpopulation boundary the ship is currently inside, named on the tab beside
  the position, with the stock's estimate, its year and its quota.

## Static plates now registered

- [[artifact:polar-bear-520]] the map of every narrative encounter, 1818-1944.
- [[artifact:polar-bear-521]] the 1997 management figures against the modern estimates.
- [[artifact:polar-bear-522]] encounters by month of the year.
- [[artifact:polar-bear-523]] a diagram of the bear's year against the ice year.
- [[artifact:polar-bear-525]] how old each subpopulation estimate is, against the
  one- and two-generation marks. This is the plate to show beside any quota
  number: three of the seven stocks are managed on field work more than two bear
  generations old.
- [[artifact:polar-bear-526]] the seven stocks drawn on the chart, sized by estimate
  and labelled with the survey year and the quota. This is the plate the tab should
  show beside the ship's position until the `layer` widget can draw the
  subpopulation places themselves.
- [[artifact:polar-bear-540]], [[artifact:polar-bear-541]] the two Hayes 1867 plates,
  and [[artifact:polar-bear-542]], [[artifact:polar-bear-543]], [[artifact:polar-bear-544]]
  the three from Kane 1856: the bears at the wrecked cache, the bear reared among the
  dogs, and the vignette head. A subject page should open on one of these rather than
  on a modern photograph.

## The seven stocks as places

The subpopulations are now place rows of kind `subpopulation`, named with that
word so that they do not collide with the strait and basin rows of the same names:
`Lancaster Sound polar bear subpopulation` and its six neighbours, each with the
2024 estimate, the year of the last field season, the quota and the sea-ice trend
in its note. A `layer` widget can draw them as the labelled regions the quota is
set in, and the tab should name the one the ship is inside.
