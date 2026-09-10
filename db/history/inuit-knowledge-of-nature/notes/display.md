# Display note — inuit-knowledge-of-nature

For the operator and the front end. Not a wiki page.

This topic is a hub: most of its value in the tab is not a time series but a
set of **names attached to other topics' subjects**, and a set of **testimony
observations** that sit beside instrumental ones. The display problems are
therefore different from a station-record topic's, and three of them are worth
solving once for the whole layer.

---

## 1. The names belong on every subject page, in the header

Every subject row already carries `english`, `french`, `inuktitut`,
`kalaallisut` and `also`. The single highest-value change is to render those
in the **subject page header**, above the note, with the bibkey of the row that
supplied them — not buried in a metadata block. A scientist looking at
`subject/ovibos-moschatus` should see *umingmak · umimmak · musk ox · boeuf
musqué* before the species account starts.

Where a name is blank, the header should say **"no Inuktitut name recorded in
this layer yet"** rather than omitting the field. The absence is information,
and it is the work list.

`subjects.json` already carries the fields; no new data is needed.

## 2. The subject picker aboard must accept any of the names

`@doc`'s journal form matches the subject against `subjects.json`. It must
match on `name`, `english`, `french`, `inuktitut`, `kalaallisut` and every
semicolon-separated entry in `also`, case- and diacritic-insensitively. A crew
member who types *nanuq* or *umingmak* or *tuktu* should get the right row.
The resolver on grid already does this (`resolve_subject`); the ship's picker
should use the same rule.

## 3. Testimony needs to be visibly testimony

An observation with `method = testimony` is a different kind of statement from
one with `method = station-record`. On the subject page's record list, and on
the map, testimony rows should carry a distinct mark and show the **observer**
prominently, because the observer is the point: *Aua, Naujaat, 1922* is the
citation, not a footnote to it. Do not merge testimony and instrument rows into
one sorted list without distinguishing them.

Rows where `observer` is a group ("the Oqomiut of Cumberland Sound", "the
Aujuitturmiut") should render as given, not be dropped for want of a person row.

---

## Static plates already rendered

| file | what it shows | stands in for |
|---|---|---|
| `inuit-knowledge-of-nature-fig-year.png` | the round of the eastern Arctic year as arcs on a ring of months | widget 1 below |
| `inuit-knowledge-of-nature-fig-starmap.png` | the winter sky with the Inuit names, to dec −20°, with the circumpolar limit at 70° N | widget 5 below |
| `inuit-knowledge-of-nature-fig-winds.png` | the named winds of Iglulik, Cumberland Sound and Akudnirn as three compass roses | no widget: the vocabulary has no `kind` |
| `inuit-knowledge-of-nature-fig-names.png` | subjects with an Inuktitut or Kalaallisut name, against the whole, by domain | widget 6 below |

---

## Widget specs

Fixed vocabulary: `kind` is one of `series`, `bars`, `strip`, `profile`,
`track`, `layer`; fields are names from `observations.json` plus `subject`,
`place`, `since`, `until`, `group_by`, `unit`, `display_unit`, `compare`,
`title`.

**1. The hunting round as a phenology strip.** The most useful thing this topic
can give a scientist aboard: what is where, and when, in the community the ship
is off. Driven by `date_start`, `subject` and `place` on the testimony rows.

```json
{"kind": "strip", "subject": "*", "place": "Mittimatalik", "x": "date_start",
 "group_by": "subject", "since": "1900", "until": "2026",
 "title": "What is taken at Mittimatalik, and when, as the community gives it"}
```

Repeat with `place` set to `Kangiqtugaapik`, `Ausuittuq`, `Naujaat` and
`Iglulik`. The strip should read the month out of `date_start` and ignore the
year, because these are statements about the round and not about one season.
Where a row's date is a range (`1950/1975`), plot the whole span as the bar.

**2. The polar night at the ship's position.** Not from observations at all —
computed — but it belongs beside them, because half this topic's calendar rows
are about it.

```json
{"kind": "series", "subject": "siqiniq", "place": "<ship position>",
 "x": "date_start", "y": "value", "unit": "deg", "display_unit": "deg",
 "compare": {"subject": "siqiniq", "place": "Iglulik"},
 "title": "The sun's altitude at noon, here and at Iglulik"}
```

The front end should annotate the two dates the Inuit calendar names: the last
day the sun is seen and the first day it returns. Those are
[[subject:Siringilang]] and [[subject:Siriniktenga]] and they are the frame of
the whole year in this topic.

**3. Beluga and narwhal counts as bars.** The community counts are real
numbers and comparable with the surveys in `whales-and-narwhal`.

```json
{"kind": "bars", "subject": "Delphinapterus leucas", "place": "Ausuittuq",
 "x": "date_start", "y": "count", "group_by": "date_start",
 "since": "1960", "until": "1975",
 "compare": {"subject": "Delphinapterus leucas", "place": "Jones Sound"},
 "title": "Belugas through Jones Sound in July, as Ausuittuq counted them"}
```

`count` is free text in the row (`"an estimated 3,000"`), so the front end must
parse a leading number and fall back to plotting the row as a marked event with
its text when it cannot. Do not drop the row.

**4. Every testimony row as a map layer.** This is the one that makes the hub
visible on the map beside the ship.

```json
{"kind": "layer", "subject": "*", "place": "*", "since": "1820", "until": "2026",
 "group_by": "method", "title": "Inuit knowledge of nature, by where it was recorded"}
```

Filter to `method = testimony` and colour by `domain`. Clicking a point should
give the `detail` sentence and the `observer` — the sentence is written to be
read on its own.

**5. The sky, as a rotating chart.** The static plate is fixed at one moment.
A widget could take the ship's date and time and rotate the same chart, showing
which named stars are up. It is the one place in this layer where the display
can do something the page cannot.

```json
{"kind": "layer", "subject": "*", "place": "*", "group_by": "domain",
 "since": "1820", "until": "2026", "title": "The named sky"}
```

filtered to `domain = astronomy` and `kind = sky` in `subjects.json`. If the
front end will not do celestial coordinates, the static plate stands.

**6. The names held, by domain.**

```json
{"kind": "bars", "subject": "*", "x": "domain", "y": "count",
 "group_by": "domain", "title": "Subjects carrying a name in the region's languages"}
```

Driven by `subjects.json` rather than `observations.json`, so it needs the one
extension: let a `bars` spec read `subjects.json` when `y` is `count` and `x` is
a subject field. Worth it, because this chart is the topic's own work list and
it should update itself as the layer fills.

---

## What a scientist aboard compares these with

- The hunting round against the ship's own sightings log and against the
  Canadian Ice Service freeze-up and break-up dates for the same community.
  Inuit month names *are* phenological observations, and the layer's
  `the-sea-ice` rows are the instrumental series to set beside them.
- The community beluga and narwhal counts against the aerial surveys in
  `whales-and-narwhal`.
- Aua's statement that the bowheads at Naujaat stopped coming inshore against
  the catch series in `whaling`. Two independent records of one collapse.
- The Ausuittuq mean annual temperature of −16 °C against the ECCC normals for
  Grise Fiord, and the ten-month ice season against the modern chart record.

## What is not here yet, and would change the display

The several hundred sea-ice terms recorded by community studies in Iglulik,
Kinngait and Kangiqtugaapik since 2000 are the missing layer. If they come in,
the right display is not a chart but a **labelled sketch of a floe edge** with
the terms on it — an ice vocabulary diagram, one per district, because the
terms differ by district the way the wind names do. That is a drawing job, not
a widget, and it should be done with a community that agrees to it.
