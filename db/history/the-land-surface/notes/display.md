# Display note: the land surface

For the operator and the front end. Not a wiki page.

The land surface has one long series (the emergence record, which is a value
against *age* rather than against date), one large set of point measurements
(beach and terrace heights, by site), one small set of depth measurements
(active-layer thickness), and a large map layer (the periglacial forms). The
front end can serve all four with the six widget kinds; the static plates in
`files/` stand in for them until it does.

Everything below drives off `observations.json` fields: `subject`, `place`,
`lat`, `lon`, `date_start`, `value`, `unit`, `qualifier`, `observer`, `bibkey`,
`detail`, `method`, `confidence`.

---

## 1. The emergence record

**What it should be.** A scatter of dated samples: radiocarbon age on the x
axis, running old to young left to right (that is, reversed), and height above
present sea level on the y. One series per site, joined by a light line. This
is the single most useful thing in the topic for a scientist aboard, because it
answers "how fast is this coast rising" directly.

**The awkwardness, and how to handle it.** The x axis is not a date. Each of
these observations carries `date_start` = the year the sample was *collected or
published* (1966, 1971) and the radiocarbon age in `qualifier` and `detail` as
written ("6,820 +/- 140 years B.P."). The `value`/`unit` pair carries the
*elevation*, in metres. So a plain `series` spec with `x: date_start` would draw
the wrong plot.

Two options, in order of preference:

1. Add a `profile` variant that reads the age out of `qualifier`. `profile`
   already means "value against depth or along a line", and an emergence plot
   is a value against an axis that is not time; this is the smallest change.
2. Failing that, keep the static plate. It is
   [[artifact:the-land-surface-203]], `files/the-land-surface-fig-emergence.png`.

**Spec, on option 1:**

    {"kind": "profile", "subject": "postglacial emergence", "place": "Macdonald River delta",
     "x": "qualifier", "y": "value", "unit": "m", "display_unit": "feet",
     "since": "1960", "until": "1980",
     "compare": {"subject": "postglacial emergence", "place": "Camp Creek"},
     "title": "How fast the land rose: Tanquary Fiord against Ward Hunt Island"}

**What a scientist aboard would compare it with.** The present rate of relative
sea-level fall from the tide gauge and GPS at Alert and Resolute — a few
millimetres a year — and the modelled future rate. The point of the comparison
is that this coast is still moving, so a chart datum here is not a fixed thing.

---

## 2. Beach and terrace heights, site by site

**What it should be.** A horizontal strip per site, a mark at each measured
height, sites ordered by their highest mark. It reads as a set of staircases and
shows at a glance that the eastern fiords have high shorelines and the outer
western islands very low ones.

**Fields.** `value` and `unit` (almost all `feet`, a few `m`), `place`,
`date_start` for the year of the observation, `subject` to separate
`raised beach` from `marine limit` (the marine-limit rows should be drawn as a
distinct mark, because they mean "and nothing above this").

**Unit.** Leave the axis in feet, because that is what all but the modern
sources wrote; put metres on the opposite axis. Rows in metres are converted for
plotting only, never in the row.

**Spec:**

    {"kind": "bars", "subject": "raised beach", "y": "value", "group_by": "place",
     "unit": "feet", "display_unit": "m",
     "compare": {"subject": "marine limit"},
     "title": "Every raised beach and marine limit the record measures"}

`bars` grouped by place is close to right but wants to draw one bar per group;
what this needs is every observation drawn as its own mark within its group. If
`bars` cannot do that, the static plate stands in:
[[artifact:the-land-surface-204]], `files/the-land-surface-fig-beach-heights.png`.

---

## 3. Active-layer thickness

**What it should be.** A `bars` chart by place and year, in the unit written
(inches for Thorsteinsson 1957 and Parry 1821, cm for the modern monitoring
holes), with centimetres on the other axis. The series is short — five or six
rows at present — and its value is as a baseline: these are the *historical*
depths against which the modern monitoring numbers at Alert, Eureka and Hot
Weather Creek should be read.

**Spec:**

    {"kind": "bars", "subject": "the active layer", "y": "value",
     "group_by": "place", "unit": "inches", "display_unit": "cm",
     "since": "1819", "until": "2026",
     "title": "How deep the ground thaws, as each observer measured it"}

**Wanted, and not yet here.** The Alert, Eureka and Hot Weather Creek
active-layer and ground-temperature series from the Canadian permafrost
monitoring network. Those are a `dataset` source with milestone observations,
not a re-entry of the whole series. Until they are in, this widget is thin, and
a `compare` block pointing at them is what would make it worth showing.

---

## 4. Ground temperature

Same shape as the weather topic's air-temperature series and should be drawn the
same way, so the two can sit side by side: a `series` in the unit written, with
the reader's unit on the right.

    {"kind": "series", "subject": "ground temperature", "place": "CFS Alert",
     "x": "date_start", "y": "value", "unit": "C", "display_unit": "C",
     "since": "1950", "until": "2026",
     "compare": {"subject": "air temperature", "place": "Alert", "since": "1950", "until": "2026"},
     "title": "Ground temperature at Alert against the air above it"}

At present the topic holds one historical ground-temperature row (Parry's
thermometer buried two or three inches in the sand, August 1819, 35.5 F). The
widget is for when the borehole series are in. The comparison with air
temperature is the whole point: the ground damps and lags the air, and the depth
at which it stops swinging is the number that says whether the permafrost is
warming.

---

## 5. The periglacial forms as a map layer

**What it should be.** The most useful thing after the emergence plot: a map
layer of every landform observation, filterable by subject, so a scientist
looking at a coast can ask "is there ice in the ground behind this shore?" The
answer is usually yes if there are polygons.

    {"kind": "layer", "subject": "patterned ground", "since": "1819", "until": "2026",
     "title": "Where frost patterns the ground"}

    {"kind": "layer", "subject": "raised beach", "since": "1819", "until": "2026",
     "title": "Where the sea has left its beaches behind"}

Subjects worth their own layer: `patterned ground` (which should include its
children — `ice-wedge polygon`, `sorted circle`, `sorted stripe`,
`earth hummock`, `mud boil` — so the layer should resolve down the subject
tree), `raised beach`, `permafrost`, `solifluction`, `pingo`, `thermokarst`.

**The tree matters here.** A layer filtered on `patterned ground` that returned
only rows whose subject is literally "patterned ground" would return five rows
instead of fifteen. Subject filtering should walk `parent`.

---

## 6. Static plates now in `files/`

| file | artifact | what it is |
|---|---|---|
| `the-land-surface-fig-emergence.png` | 203 | the dated emergence record, Tanquary Fiord and Ward Hunt Island |
| `the-land-surface-fig-beach-heights.png` | 204 | every measured beach and marine-limit height, site by site |
| `the-land-surface-fig-ground-section.png` | 205 | a conceptual section through the ground, with the measured depths on it |
| `the-land-surface-hs1967-fig1-tanquary-air-photo.jpg` | 001 | the 1959 air photograph of the Tanquary delta terraces |
| `the-land-surface-hs1967-fig2-raised-beaches-terrace-outlier.jpg` | 002 | Brassard's 1964 photograph of the beaches on the terrace outlier |
| `the-land-surface-hs1967-fig3-uplift-curve.jpg` | 003 | the original 1967 uplift curve |
| `the-land-surface-thorsteinsson1961-plate4-frost-table.jpg` | 200 | a pick head resting on the frost table, Meighen Island, 1957 |
| `the-land-surface-thorsteinsson1961-plate6-nivation-solifluction.jpg` | 201 | nivation scarps and solifluction terraces from the air, 1950 |

Plate 200 is the one to open the [[subject:permafrost]] and
[[subject:the active layer]] pages on: it is a photograph of the thing itself,
which is rare.

---

## 7. What the next run should add for the display

- The ECCC and permafrost-network borehole series as `dataset` sources, with
  milestone observations, so widgets 3 and 4 have something to draw.
- The GSC surficial geology sheets as `map` artifacts, so the layer can show the
  mapped extent of marine deposits behind a coast rather than only point
  observations.
- Dyke's and England's isobase maps of Holocene emergence, which would let the
  front end shade the whole archipelago by how fast it is rising, instead of
  showing two curves at two sites.

---

## 8. Added in the second run (2026-09-10)

The modern record is now in the rows, and three things follow for the display.

### 8.1 A third plate

| file | artifact | what it is |
|---|---|---|
| `the-land-surface-fig-three-coasts.png` | 232 | every dated sample from Devon Island, Melville Island and the Melville Peninsula, age against height, one colour per coast |
| `the-land-surface-fig-marine-limits.png` | 234 | the marine limit at every place this record measures one, against latitude, with the original feet and metres printed beside each point |

This is the plate to open [[subject:postglacial emergence]] on. The earlier
plate (203) shows two sites on one island; this one shows why the curves differ
between islands, which is the thing worth understanding. Keep both: 203 is the
close view, 232 the regional one.

### 8.2 Two widgets the rows can now drive

The retreat of a thaw slump headwall, day by day, is the only true time series
this topic holds at daily resolution, and it is the most vivid thing here — a
hillside going back six centimetres a day. It is currently three summary rows
(178-183) rather than the full daily record, because the daily numbers live in
Ward Jones and Pollard's figures rather than in a table; if that series is ever
digitised the spec below draws it as it stands.

    {"kind": "bars", "subject": "retrogressive thaw slump", "place": "Eureka Sound Lowlands",
     "y": "value", "unit": "cm per day", "group_by": "qualifier",
     "since": "2017-06", "until": "2017-09",
     "title": "How fast three thaw-slump headwalls went back in one High Arctic summer"}

Marine limit by place is the other. It is a single number per locality, it is
comparable across the whole archipelago, and it is the clearest possible picture
of the vanished ice: bars ordered by height say more than a map of dots.

    {"kind": "bars", "subject": "marine limit", "y": "value", "unit": "m",
     "group_by": "place", "title": "How high the sea once stood, island by island"}

Plate 234 now stands in for that widget, drawn against latitude rather than as
bars, because latitude carries the story the bars would only imply.

Note the unit trap: the marine-limit rows are in metres for the modern surveys
and in feet for the nineteenth-century and Resolute observations. The widget
must convert on the display side from `unit`, not assume one unit, and should
say in its label which rows were written in feet.

### 8.2a A real series arrived: Ward Hunt Island

Rows 234-242 are the annual maximum depth of thaw read by the Centre d'etudes
nordiques' thermistor string at the SILA station on Ward Hunt Island, one row a
year from 2006 to 2014, each with the exact date the maximum fell on. That is a
true series, in one unit, at one place, and it is the first thing in this topic
that a `series` widget can draw honestly:

    {"kind": "series", "subject": "the active layer", "place": "Ward Hunt Island",
     "x": "date_start", "y": "value", "unit": "cm", "display_unit": "cm",
     "since": "2006", "until": "2015",
     "title": "How deep the ground thawed each summer on the northernmost land in Canada"}

Nine points is few, and the reader should be told so; the label should say that
2011 (106 cm) is the deepest and 2006 (65 cm) the shallowest, and that the run
is short enough that no trend should be read off it. A scientist aboard would
want it against the summer thawing index for the same years, which rows 247 and
248 give as a range rather than a series.

### 8.3 The series still missing

Unchanged from section 7, and now more clearly worth having:

- The permafrost thermal monitoring boreholes at Alert, Eureka and Hot Weather
  Creek as `dataset` sources with milestone observations. The topic now holds a
  single ground temperature (row 175, minus 16.5 C at 15.4 m at Eureka) where it
  should hold a warming trend. That row is the anchor a series would hang on.
- Active-layer depth by year at the Circumpolar Active Layer Monitoring sites in
  the archipelago, which would turn the scattered thaw depths of rows 191-194,
  210 and 216 into the series a scientist aboard would actually want.
- The GSC surficial geology sheets as `map` artifacts. GEOSCAN does not resolve
  from this machine at all, so these need a person to fetch them.
