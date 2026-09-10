# Display note: the water column

What a scientist aboard the Amundsen would want to see from this topic's rows,
what should be a widget and what a static plate, and which of the four registered
figures stands in for each until the widget exists.

The observation rows here are unusual for this layer in one way: almost every
number is in a historical unit (fathoms, feet, inches, degrees Fahrenheit,
specific gravity against distilled water) and none of them is converted in the
row. Every widget below therefore needs `unit` and `display_unit` and must show
the original somewhere, because the original is the citable quantity.

## 1. The soundings as a map layer

The most useful single thing. A scientist looking at the ship's position wants
to know what anybody ever measured near it, and the answer for most of this
region is "one cast, in eighteen-something". Points filtered by subject, with the
depth in the tooltip in fathoms and metres, and the "no bottom at" casts
distinguished, because a "no bottom at 260 fathoms" row is a lower bound and not
a depth.

    {"kind": "layer", "subject": "sounding", "unit": "fathoms", "display_unit": "m",
     "since": "1818", "until": "1960",
     "title": "Every sounding in the record, 1818 to 1960"}

Drives from `lat`, `lon`, `value`, `unit`, `date_text`, `qualifier`, `vessel`,
`bibkey`, `pages`. The `qualifier` field carries "no bottom at" and should change
the symbol, not be buried in a tooltip.
Compare with: the ship's own echo sounder reading, and the IBCAO cell value.
Stands in for now: `the-water-column-900`.

## 2. Tide range against latitude

The clearest result in the topic and it is one plot. Range in feet as written,
metres on the second axis, latitude on the x. It is not a time series, so
`bars` grouped by place is the closest kind in the vocabulary; a `profile` with
latitude as the ordinate would also serve.

    {"kind": "bars", "subject": "tide range", "y": "value", "group_by": "place",
     "unit": "feet", "display_unit": "m", "since": "1820", "until": "1908",
     "title": "The rise and fall of the tide, station by station"}

Note for whoever builds it: rows whose `unit` is `inches` (Haughton's reductions
of the Alert and Discovery registers) and `hours` (lunitidal intervals, which are
times and not heights) must be handled separately. The `hours` rows are not a
range at all and should be excluded from any height axis.
Compare with: the CHS predicted range for the nearest modern station.
Stands in for now: `the-water-column-901`.

## 3. Temperature against depth: the historical profiles

The single most scientifically live thing here, because it is the only
pre-twentieth-century evidence of the Atlantic layer in these channels.

    {"kind": "profile", "subject": "water temperature", "x": "value", "y": "depth",
     "unit": "F", "display_unit": "C", "since": "1818", "until": "1885",
     "compare": {"subject": "Atlantic layer", "since": "1818", "until": "1885"},
     "title": "Temperature against depth as the expeditions read it"}

Drives from `depth` (metres, which the writer filled from the fathom figure) and
`value` with `unit` F. Depth should be shown in fathoms as well, because the
observers chose their depths in fathoms and the round numbers are meaningful.
The rows carrying a full profile rather than a single point are
`the-water-column-116` (Moss's five-depth table), `-114` (Cape Frazer),
`-185` (Cape York) and `-111` (Cary Islands); their `detail` fields hold the
intermediate values, which is a limitation of one-row-per-observation and would
be worth revisiting if the schema ever grows a profile kind.
Compare with: the ship's own CTD cast at the nearest station. That comparison is
the reason to build this at all - a modern cast beside Moss's 1876 table, on the
same axes, at the same place.
Stands in for now: `the-water-column-902` and the section diagram `-903`.

## 4. The deep soundings as a credibility strip

A small, honest widget: the handful of casts over five hundred fathoms, each with
what its own observer said about whether he believed it. Ross's 1,050 fathoms,
Parry's 2,010 fathoms of line for 809 fathoms of water, Kane's 1,900 fathoms
which cannot be right, Bernier's 605 fathoms on three wires bent together.

    {"kind": "strip", "subject": "sounding", "x": "date_start", "group_by": "vessel",
     "unit": "fathoms", "display_unit": "m", "since": "1818", "until": "1910",
     "title": "The deep casts, and what their observers thought of them"}

Filter to `value >= 500` at build time. The `confidence` field is the payload:
`doubtful` on Kane's row is the whole point, and the strip should show it.
No static figure stands in for this one yet.

## 5. Currents

Too few rows to be worth a widget of its own (seven, and three of them carry no
rate). They belong in the map layer of item 1 as a second subject, with the
direction from `qualifier` drawn as a short arrow where a set is given. Revisit
if a later run enters the whaling and Franklin-search current observations.

## 6. What Inuit and Inughuit knew: the testimony layer

Twenty-eight of this topic's rows carry `method: testimony`, and they are not
numbers. They are statements about where the current runs, where the tide is
strong enough to keep the water open, where the ice will not hold, and how the
tide governs sealing and travel - Boas's Oqomiut on the entrance of Cumberland
Sound and the tideways of the fiords, Rasmussen's Netsilik place names for the
current, Sorqaq on being carried off the land by the ice, Hans Hendrik on the
water off Thank God Harbor, the Inughuit of Etah on the range of the open water
off Cape Alexander, Koo-loo-a on the winter open water south of Cape Englefield,
and the three Iglulingmiut who gave Bernier the only tide range this record holds
for the Fury and Hecla Strait.

They belong on the map beside the soundings, not in a separate tab, because their
whole value is that they are about the same water. A layer filtered on method:

    {"kind": "layer", "subject": "current", "since": "1829", "until": "1923",
     "title": "Where the current runs, as Inuit and Inughuit described it"}

    {"kind": "layer", "subject": "sikuiqsuilaq", "since": "1854", "until": "1884",
     "title": "Water that does not freeze, as the record was told"}

Drives from `lat`, `lon`, `observer`, `date_text`, `detail`, `bibkey`, `pages`.
Two rules for whoever builds it. First, the `observer` field is the point and must
be shown on the point itself, not hidden in a tooltip: these rows are somebody's
knowledge and the somebody is named. Second, several of these positions are
approximate and say so in `detail`; the symbol should be soft-edged rather than a
hard point, and the `confidence` field (`probable` on eight of them) should drive
that.

A scientist aboard would compare this layer with the ship's own ice chart and with
the Canadian Ice Service climatology of where polynyas open: the Inuit account of
which passages stay open through the winter is a testable statement about the
modern record, and in every case this topic has checked it holds.

The subject pages for `current`, `tide range` and `salinity` now carry the
Inuktitut names (sarvaq, tiniq, tariuq) with their glosses and sources, and the
front end should show the names strip on those pages as it does for a species.

## Units and conversions, for whoever implements the above

| as written | convert to | factor |
|---|---|---|
| fathoms | metres | x 1.8288 |
| feet | metres | x 0.3048 |
| inches | metres | x 0.0254 |
| degrees Fahrenheit | degrees Celsius | (F - 32) x 5/9 |
| knots, miles per hour | m/s | x 0.5144, x 0.4470 |
| specific gravity at 60 F | no clean conversion | show as written; it is density against distilled water, not practical salinity, and the sample temperature is part of the reading |

The last row matters. A specific gravity of 1.02567 should never be printed as a
salinity: the reduction depends on the temperature the hydrometer was read at,
which the sources give and which the row carries in `qualifier`. Show the number
and the temperature together or not at all.
