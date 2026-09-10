# Display note: meteorites and minerals

For the operator and the front end. What in this topic's record is worth showing, what the widget should be, which fields of `observations.json` drive it, and which static plate stands in for it now.

## The six static plates already in

| artifact | file | what it shows | built from |
|---|---|---|---|
| `meteorites-and-minerals-002` | `-fig-nickel.png` | nickel per cent by analysed specimen, 1819-2015, with the meteoritic and telluric bands shaded | the observation rows with `unit` "per cent nickel" plus the XRF ranges in `qualifier` |
| `meteorites-and-minerals-003` | `-fig-masses.png` | the recovered Cape York masses by weight, with the year taken and the present holder | the `Cape York meteorite` subject's children and their `value`/`unit` tonnes rows |
| `meteorites-and-minerals-004` | `-fig-coal-seams.png` | recorded coal seam thickness by locality, feet with metres across the top | the `coal` and `lignite` observations with `unit` feet |
| `meteorites-and-minerals-005` | `-fig-quarry.png` | schematic section of the hammerstone quarry at Saveruluup Itilliapalua | the `greenstone hammerstone` observations |
| `meteorites-and-minerals-007` | `-fig-conger-coal.png` | every quantity of coal Greely's report puts a number to at Fort Conger, October 1881 to August 1883, in pounds with long tons on the right | the `coal` and `lignite` observations with bibkey `greely1888report` and a value in pounds or tons |
| `meteorites-and-minerals-008` | `-fig-strewnfield.png` | the Cape York masses on the Melville Bay coast, circle area by mass, on the OpenStreetMap Arctic coastline | the observations with bibkey `metbull2026capeyork`, their `lat`/`lon` and their `value`/`unit` |

## Widget specs

Five things in this topic want a widget rather than a plate. In the fixed vocabulary, one object per widget.

**1. The nickel test.** The single most useful thing a scientist aboard can be shown from this topic: a value against a category, with two reference bands. `bars` is the nearest kind in the vocabulary; the front end should sort by value and colour by whether the row's subject resolves to `meteoritic iron` or `telluric iron of Disko`.

    {"kind": "bars", "subject": "meteoritic iron", "group_by": "observer",
     "y": "value", "unit": "per cent nickel", "since": "1819", "until": "2015",
     "compare": {"subject": "telluric iron of Disko", "group_by": "observer"},
     "title": "Nickel per cent: the sky iron of Cape York against the earth iron of Disko"}

**2. The masses of the fall.** A bar per named mass, ordered by weight, with the year in the label. The subject tree does the grouping: every child of `Cape York meteorite` with a tonnes value.

    {"kind": "bars", "subject": "Cape York meteorite", "group_by": "subject",
     "y": "value", "unit": "tonnes", "title": "The recovered masses of the Cape York fall"}

**3. The removals, as a dated strip.** The best single view of the topic's human half: 1818 Ross is told of the iron; 1894 Tellikotinah guides Peary; 1895 the Woman and the Dog; 1897 Ahnighito; 1913 Koodlooktoo finds Savik; 1922-25 Savik to Copenhagen; 1963 Agpalilik; 2026 the agreement to return it. Category is the mass.

    {"kind": "strip", "subject": "Cape York meteorite", "group_by": "subject",
     "x": "date_start", "since": "1818", "until": "2026",
     "title": "Two hundred years of the Cape York irons"}

**4. The coal seams.** Value against category, one bar per measurement, feet on the axis and metres beside it. The front end must not convert the row: `unit` is feet as written and `display_unit` is metres.

    {"kind": "bars", "subject": "coal", "group_by": "place",
     "y": "value", "unit": "feet", "display_unit": "m",
     "since": "1819", "until": "1956",
     "compare": {"subject": "lignite", "group_by": "place"},
     "title": "Coal seam thickness as the observers wrote it"}

**5a. The strewnfield as a map.** The plate `meteorites-and-minerals-008` stands in for this. As a widget it is a `layer` restricted to the subject tree under `Cape York meteorite`, with the marker sized by the row's `value` converted to tonnes; the Woman and the Dog share a position in the Bulletin, as do Savik I and Savik II, so the front end must jitter or cluster rather than draw one over the other.

    {"kind": "layer", "subject": "Cape York meteorite", "group_by": "subject",
     "since": "1818", "until": "1963",
     "title": "The Cape York strewnfield"}

**5. The map layer.** Everything in this topic has a position and most of the positions are places a ship can see from the deck. A `layer` filtered on the geology domain, with the mineral subjects as the legend, is the form.

    {"kind": "layer", "subject": "meteoritic iron", "since": "1818", "until": "2026",
     "title": "Where the metal, the coal and the ore were found"}

## Units and conversions

- Nickel and iron percentages are per cent by weight and need no conversion.
- Seam thickness is in feet as written; metres = feet x 0.3048. Show both.
- Coal quantities are as written and are of three kinds that must not be summed: bushels (Parry), pounds and tons (Greely, Bernier, the Proteus), and bags (Bernier's Salmon River). Label the unit on every bar.
- Meteorite masses are given here in tonnes; Peary's own figures are in pounds and short tons and are kept as written in the rows, with the modern figure in the subject note.
- Temperature: one row only, Ekblaw's -52 F on Ironstone Mountain in January 1914. C = (F - 32) x 5/9.

## What a scientist aboard would compare these with

- **The nickel plate** against the ship's own XRF or ICP work on any metal artefact: the six-to-nine per cent band is a field test for Cape York provenance, and it is the reason iron in a Thule house pit on Devon Island can be traced to a Greenland hillside.
- **The coal plate** against the Eureka Sound Group outcrops in `rock-and-the-sverdrup-basin` and the leaf floras in `fossils-and-deep-time`: the same beds, and the seam thickness is a proxy for how long the Palaeogene forest stood.
- **The masses plate** against the repatriation record: five of the ten fragments are abroad and one is coming home.
- **The map layer** against the ship's track: Innaanganeq, Savissivik, Stenkul Fiord, Bache Peninsula, Watercourse Bay, Bent Horn, Nanisivik and Polaris are all within a season's steaming.

## The Fort Conger coal, as a widget

The plate `meteorites-and-minerals-007` stands in for this now. As a widget it is a `bars` by date rather than a `series`, because the report gives quantities at irregular moments and not a monthly total; the front end must not interpolate between them.

    {"kind": "bars", "subject": "lignite", "place": "Fort Conger", "group_by": "date_start",
     "y": "value", "unit": "pounds", "display_unit": "long tons",
     "since": "1881-10", "until": "1883-08",
     "compare": {"subject": "coal", "place": "Fort Conger"},
     "title": "What the Watercourse Bay seam gave Fort Conger, 1881 to 1883"}

Two cautions for whoever renders it. The rows carry the unit Greely wrote, so some are `pounds` and some are `tons`, and the widget must convert on display and label which is which; the long ton here is 2,240 pounds. And the hundred and forty tons the Proteus landed in August 1881 is twenty times the largest of the others: it belongs in the caption, not in the bars.

## What is missing and would earn a figure once entered

- Coal *consumed* month by month at Fort Conger. The report gives it only once, in April 1883, as within a third of a ton of what was hauled; the rest would have to come from the station's own fuel returns, which are not in the volume held.
- The masses and positions of the Cape York fragments the Meteoritical Bulletin does not list - Thule (1955) and Tunorput (1984) - which rest on Buchwald 1975 volume 2, still in the pickup queue.
- The Nanisivik and Polaris production records, year by year, which would make a proper `bars` of the two mines' twenty-six and twenty years. GEOSCAN gives nothing to a plain fetch and the reports are queued.
