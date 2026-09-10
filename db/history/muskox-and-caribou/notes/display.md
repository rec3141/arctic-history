# Display note: muskox and caribou

For the operator and the front end. What in this topic is worth drawing, why, which
fields drive it, and which static plate stands in for it now.

## What the data actually is

Almost every row in this topic carries a `count`, not a `value`. The counts are text,
because the sources are text: "a herd of seventeen", "over two hundred and fifty",
"none seen", "about 200". Only a handful of rows carry a numeric `value` with a `unit`
(dressed weights in pounds, from Nares, Greely and Joy). So the natural x-axis here is
time and the natural y-axis is a **count parsed out of the count string**, and the front
end must be prepared for a count that will not parse. Where a widget below needs a
number, the observation whose count is a bare integer or a "N,NNN" is usable; everything
else belongs on a map or a strip, not on a value axis.

Three counts are of different kinds and must never be summed or plotted on one axis:

- **a sighting count** — what one party saw on one day ("a herd of eleven");
- **a catch record** — what an expedition killed over a season or a wintering
  (`method` = `catch-record`);
- **a survey estimate** — an extrapolated island or range population
  (`method` = `aerial-survey` or `survey`, and the `qualifier` says "estimated" or
  "provisional").

`method` is the field that separates them, and every widget below filters on it.

## The record, subject by subject

### 1. The Peary caribou population, 1961 to now
The single most important series in the topic, and the one a scientist aboard will ask
about. Four points from COSEWIC 2015 plus Tener's 1961 figure on a different geographic
footing. It is short enough that a static plate serves it well, and
[[artifact:muskox-and-caribou-522]] is that plate. A widget is still worth having,
because a later run will add the Nunavut and GN surveys island by island and the series
will grow.

    {"kind": "series", "subject": "Rangifer tarandus pearyi", "x": "date_start", "y": "count",
     "unit": "animals", "display_unit": "animals", "since": "1955", "until": "2026",
     "title": "The Peary caribou since counting began"}

Compare, aboard, with: nothing in the ship's own data — this is a land series. The
comparison that matters is with the weather record, specifically winter rain-on-snow
events at Resolute and Eureka; if `the-weather-and-the-climate` enters those as
observations, a second panel under this one is the strongest thing the natural half
could show.

### 2. Tener's 1961 island counts
A bars widget by island, split by species, is the right shape, and the west-to-east
ordering is what makes it say something. The static plate
[[artifact:muskox-and-caribou-521]] carries it now.

    {"kind": "bars", "subject": "Rangifer tarandus pearyi", "y": "count", "group_by": "place",
     "since": "1961-06", "until": "1961-09", "unit": "animals",
     "compare": {"subject": "Ovibos moschatus", "since": "1961-06", "until": "1961-09"},
     "title": "Caribou and muskoxen island by island, the survey of 1961"}

Filter to `method = aerial-survey` and to rows whose `qualifier` contains "estimated" or
"calculated" or "provisional", or the transect counts and the island estimates will be
mixed. Order the islands by the longitude of the `place` row, not alphabetically.

### 3. The hunting return of the wintering parties
Bars by expedition, from the `catch-record` rows. Plate:
[[artifact:muskox-and-caribou-520]]. As a widget it wants grouping by observer rather
than by place, because Nares's two ships wintered two hundred miles apart and are two
bars.

    {"kind": "bars", "subject": "Ovibos moschatus", "y": "count", "group_by": "observer",
     "since": "1819", "until": "1910", "unit": "muskoxen killed",
     "title": "What each wintering party took"}

Restrict to `method = catch-record`. This is the one widget where the sum has a meaning:
the total is roughly what European wintering removed from the eastern archipelago
before the 1917 law.

### 4. Every sighting on the map
The most useful thing of all, and the cheapest: a map layer of the whole topic, filtered
by species and playable by date. The record runs from September 1819 on the beach of
Melville Island to August 1961, and the geographic pattern — muskoxen east, caribou west
— is visible without any arithmetic.

    {"kind": "layer", "subject": "Ovibos moschatus", "since": "1819", "until": "2026",
     "title": "Every recorded muskox, 1819 to now"}

    {"kind": "layer", "subject": "Rangifer tarandus", "since": "1819", "until": "2026",
     "title": "Every recorded caribou, 1819 to now"}

`Rangifer tarandus` should pull its subspecies rows in through `parent`; if the resolver
does not walk the tree, the front end needs three layers rather than one, and the
subspecies are `Rangifer tarandus pearyi` and `Rangifer tarandus groenlandicus`.

Colour the two species apart and keep them apart: this is a topic where a reader will
want to see the two distributions at once, which is why the static plate is a butterfly
rather than two panels.

### 5. Calving, as a phenology strip
Thin, but real: Joy's calving observations at Bear Peninsula on 2 May 1927, Tener's
ground counts of calves at Bracebridge Inlet on 18, 23 and 27 June 1961, Tener's Fosheim
count of 10-14 May 1960. Worth a strip once a later run adds the modern calving dates.

    {"kind": "strip", "subject": "Ovibos moschatus", "x": "date_start", "group_by": "place",
     "since": "1900", "until": "2026", "title": "When calves were recorded"}

Filter to rows whose `stage` or `behaviour` names a calf. Under ten rows today; do not
publish it until there are thirty.

### 6. Dressed weights
`value` and `unit` are populated in pounds on a handful of rows (Moss's lean bull of 212
lb at Floeberg Beach in 1876; Brainard's running average of 243 lb through 1882; Greely's
autumn average of 360 lb; Joy's caribou of about 60 lb at Goose Fiord). Too few for a
series, but they are the only numeric values in the topic and they carry the condition of
the animals, which is what a biologist reads them for. A `series` spec is written here so
a later run has somewhere to put more of them.

    {"kind": "series", "subject": "Ovibos moschatus", "x": "date_start", "y": "value",
     "unit": "lb", "display_unit": "kg", "since": "1819", "until": "1965",
     "title": "Dressed weight of the muskoxen killed"}

Conversion: kg = lb x 0.45359237. Show the pound scale on the left, as the sources give
it, and the kilogram scale on the right.

## The diagram

[[artifact:muskox-and-caribou-523]] is a conceptual section, not data: it explains why a
warm winter kills a herd. It is the piece that makes the population series intelligible,
so the front end should place it beside figure 1 wherever the caribou decline is shown,
not in a separate gallery.

## Added in the second run

### 7. The island series (now the topic's principal figure)

[[artifact:muskox-and-caribou-525]] is the plate item 1 was waiting for: every published
Peary caribou estimate for the Bathurst Island complex (1961, 1973, 1974, 1981, 1985,
1988, 1993, 1994, 1996, 1997, 1998), for Prince of Wales, Somerset and Russell (1974,
1975, 1980, 1995), for Axel Heiberg (2007, 2019) and for the western Queen Elizabeth
Islands entire (1961, 1997), drawn on a log scale. It replaces the four-point curve as
the thing to show a scientist who asks what happened to the Peary caribou.

As a widget it is three `series` in one frame, filtered by place; the front end should
render it with the log scale, because a linear one hides the 1998 and 2019 points
entirely:

    {"kind": "series", "subject": "Rangifer tarandus pearyi", "place": "Bathurst Island",
     "x": "date_start", "y": "value", "unit": "animals", "since": "1961", "until": "2019",
     "compare": {"subject": "Rangifer tarandus pearyi", "place": "Prince of Wales Island",
                 "since": "1974", "until": "1995"},
     "title": "The Peary caribou counted island by island"}

The rows carry the estimate in `value` and the interval or standard error in `count` as
the papers print it; the axis label should say animals estimated, not animals.

### 8. Banks Island, the two curves

[[artifact:muskox-and-caribou-526]] puts the muskox and the caribou of one island on one
log scale, 1970 to 1989, and they cross about 1978. It is the plate for the competition
question, and it should be shown wherever the muskox's increase is discussed. As a
widget:

    {"kind": "series", "subject": "Ovibos moschatus", "place": "Banks Island",
     "x": "date_start", "y": "value", "unit": "animals", "since": "1970", "until": "1989",
     "compare": {"subject": "Rangifer tarandus pearyi", "place": "Banks Island",
                 "since": "1972", "until": "1989"},
     "title": "Banks Island: where the two curves cross"}

The March 1979 and March 1980 surveys cover half the island each and must be filtered out
of any island-wide series; they are kept as rows because they carry the densities by
river valley, which nothing else does.

### 9. One hunter's return

[[artifact:muskox-and-caribou-524]] is a different kind of figure: not a population but a
record, every musk-ox and caribou entry in Hans Hendrik's own memoirs across four
expeditions, grouped by ship. It belongs beside the Inuit and Inughuit knowledge page. As
a widget it is a `bars` by entry rather than by year, which the fixed vocabulary does not
express; keep the static plate.

### 10. The layer of Indigenous observations

The topic now holds testimony and hunt rows whose observer is an Inuk or Inughuit person:
Hans Hendrik, Nukapinguaq, Oodee, Ahkeeoo, Etukishook, Arklio, Piugaattoq, Panikpah,
Koo-loo-ting-wah, Merqusaq, Qisunguaq, Qilerneq, Ajunge, Lisbeth, Ojuvainath, Panigpak,
Piuaitsoq, Samwillie Elijasialak, John Amagoalik, Simeonie Amarualik, Abraham Etungat,
Equaluk Nungusuituk, Novayuk Ipeelie, Ejeetsiak Peter, Paulassie Pootoogook, Sandy Akavak
and Simonie Alainga. A map layer filtered on those rows shows where the Indigenous record
of these two animals actually is - Smith Sound, southern Ellesmere, Axel Heiberg, the
Foxe Peninsula, Meta Incognita, Nettilling - and it is a different map from the survey
one:

    {"kind": "layer", "subject": "Rangifer tarandus", "since": "1820", "until": "1996",
     "group_by": "observer", "title": "The caribou as Inuit and Inughuit hunters recorded it"}

Render the same for Ovibos moschatus. The front end should show the observer's name on
the point, not the expedition's.

## What is missing, for whoever comes next

The island-by-island surveys since 1961 are now in, from the open-access run of Arctic:
items 7 and 8 above. What is still wanting is the muskox's own status - COSEWIC appears
never to have assessed Ovibos moschatus in Canada, and the subject row's status field is
deliberately blank until a COSEWIC document says so one way or the other - and the
Government of Nunavut and GNWT survey reports of the 2000s and 2010s, which would carry
the Bathurst and Prince of Wales series past 1998. The calving strip (item 5) and the
dressed weights (item 6) are still under their thresholds.
