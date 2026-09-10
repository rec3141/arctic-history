# Display note: fossils and deep time

A note for the operator and the front end, not a wiki page. It says what this
topic's record should look like on screen, which fields of `observations.json`
drive each view, and which static figure stands in for it now.

## What this topic's data actually is

127 observations, almost all of them **undated in geological time and dated in
human time**. That is the thing to understand before designing anything: an
observation here carries two clocks.

- `date_start` is when a **person** found, collected, mined or determined the
  thing: 1819-05-13, 1901-06, 2004-07.
- the **age of the fossil** is not a field. It lives in `tags`
  (`cambrian`, `ordovician`, `silurian`, `devonian`, `carboniferous`,
  `triassic`, `cretaceous`, `tertiary`, `eocene`, `miocene`, `pliocene`) and in
  the subject's `parent` chain up to a formation, group or basin row.

So every view of this topic is either a **collecting history** (human time) or a
**deep-time view** (the tag or the subject's parent). The front end should not
try to put both on one axis.

Values are rare and heterogeneous: seam thicknesses in feet, coal in tons,
pounds and bushels, one temperature anomaly in degrees Celsius, counts of
specimens and species as free text. Do not build a numeric series over
`value` across this topic; it means a different thing in almost every row.

## Widgets worth building

### 1. The localities layer (the primary view)

```json
{"kind": "layer", "subject": "fossil", "place": "", "since": "1819", "until": "2026",
 "group_by": "tags", "title": "Fossil localities of the archipelago, coloured by the age of what was found"}
```

Filter `observations.json` to `topic == "fossils-and-deep-time"`; colour each
point by the first geological-period tag it carries, in the fixed order
Cambrian, Ordovician, Silurian, Devonian, Carboniferous, Triassic, Cretaceous,
Palaeogene, Neogene; grey for a row with none. The map should let the reader
scrub `date_start` to watch the collecting spread outward from Barrow Strait
in the 1850s to Ellesmere in 1900 and to the Fosheim Peninsula after 1955.
Rows with `sensitive = 1` (the Tiktaalik quarry, the Beaver Pond, the Fyles
Leaf Bed) publish at 0.5-degree rounding and with a blank place, and their
popups must not name the ground.

**Stands in for it now:** `[[artifact:fossils-and-deep-time-300]]`.

### 2. Collecting by decade

```json
{"kind": "bars", "subject": "fossil", "x": "date_start", "y": "count",
 "group_by": "method", "since": "1810", "until": "2030",
 "title": "Two centuries of Arctic fossil collecting, by decade"}
```

Bucket `date_start` by decade, stack by `method` (`specimen`, `sample`,
`sighting`, `survey`, `testimony`). This is the view that shows the shape of
the record rather than the shape of the rock: who was looking, when, and how.
The `testimony` segment is deliberately visible, because it is nearly empty and
should be.

**Stands in for it now:** `[[artifact:fossils-and-deep-time-303]]`.

### 3. The column

Not a chart: a **diagram widget**, and the one thing a scientist aboard will
want most, because it answers "what is under me". Given the ship's position,
the front end should be able to show the column for that part of the
archipelago with the fossil subjects hung on it. It is driven by the
`subjects` table, not by `observations`: walk `parent` from a `fossil` subject
up through `formation` to `group` to `basin`, and order the units by the ages
written in their notes.

Until the front end can walk that tree, a static plate stands in:
`[[artifact:fossils-and-deep-time-301]]`.

### 4. The warm Arctic

```json
{"kind": "bars", "subject": "air temperature", "place": "Eureka",
 "x": "qualifier", "y": "value", "unit": "C", "display_unit": "C",
 "compare": {"subject": "air temperature", "place": "Eureka", "since": "1981", "until": "2010"},
 "title": "Nineteen degrees: how warm the High Arctic has been"}
```

This is the one number from this topic that belongs beside the ship's own
instruments, and it should be shown wherever the weather topic shows a normal.
It has to be rendered with its uncertainty stated in words, because the two
fossil rows are reconstructions with several degrees of error and the station
rows are published normals. The row that drives it is observation
`fossils-and-deep-time-119`; the comparison values come from
[[topic:the-weather-and-the-climate]].

**Stands in for it now:** `[[artifact:fossils-and-deep-time-302]]`.

### 5. The subject page's own record

No widget needed: the generated subject page already lays out every
observation of a subject in date order. For this topic that reads well for the
site subjects (`Geodetic Hills fossil forest`, `Store Bjornekap Carboniferous
limestone`) because the log is a history of visits to one place. It reads less
well for the taxon subjects, where the log is a list of determinations. If a
second layout is ever wanted, sort a taxon's record by **locality** rather than
by date.

## What would improve the data

1. **A geological-age field.** The period tag works but is a convention, not a
   contract. If `subjects` ever gains `age_start_ma` / `age_end_ma` on unit and
   fossil rows, every deep-time view above becomes exact instead of
   approximate, and the column widget can be drawn to scale.
2. **Formation parents on every fossil subject.** Most have one; a few
   nineteenth-century localities (the Cape Cracroft bed, the Fossil Mount
   summit) do not, because the sources never named a unit. Those are honest
   gaps and should stay blank rather than be guessed.
3. **The Paleobiology Database join.** `pbdb2026database` is entered as a
   dataset. A future run can pull the PBDB collections inside the archipelago's
   bounding box and match them to these subjects, which would turn a
   nineteenth-century species list into modern occurrence records with
   coordinates.
