# Display note: the small and the microbial

For the operator and the front end. Not a wiki page. It says, for every series or subject in
this topic worth showing, what the figure or widget should be, which fields of
`observations.json` drive it, the units, what a scientist aboard would compare it with, and
which static figure stands in for it now.

## The four static figures already in

| figure | artifact | what it is | what it stands in for |
|---|---|---|---|
| `-fig-hazen-list.png` | `the-small-and-the-microbial-011` | bars: species by order in Oliver's 1961 Hazen Camp collection | the `bars` widget below, once the observation rows carry per-order counts rather than one row per order |
| `-fig-insect-year.png` | `the-small-and-the-microbial-012` | phenology strip: every dated insect observation on its day of the year, banded by group | the `strip` widget below. This one is the priority: it is built entirely from rows and will improve every time a row is added |
| `-fig-tuborg-profile.png` | `the-small-and-the-microbial-013` | depth profile of Bowman's Tuborg Lake tows, 1966-67 | the `profile` widget below |
| `-fig-ice-algae-diagram.png` | `the-small-and-the-microbial-014` | schematic section through first-year ice: the algal layer and what eats it | nothing; a diagram, permanent |

## Widgets, in the fixed vocabulary

**1. The arctic insect year.** The single most useful thing this topic can show a scientist
aboard, because it answers "is anything flying yet, and is that early?" from two centuries
of rows.

    {"kind": "strip", "subject": "Insecta", "x": "date_start", "group_by": "subject",
     "since": "1818", "until": "2026",
     "title": "Every dated record of an insect in the archipelago, by day of the year"}

Notes for the implementation: the x axis is day-of-year, not date; the year is the colour or
the tooltip. Rows whose `date_text` gives only a month should be drawn at mid-month and
marked as such (a hollow marker), because a third of the historical rows are month-only. The
grouping wanted is coarser than `subject`: bees and wasps, butterflies and moths, mosquitoes,
other flies and midges, spiders and mites and springtails. If `group_by` can only take a
field name, add a `group` column to the subject rows for this purpose rather than
special-casing it here. What a scientist aboard compares it with: the ship's own date for the
first insect of the season at whatever landing they make.

**2. Chlorophyll against depth.** The standard cast plot, which the layer can seed with the
historical numbers so a new cast has something behind it.

    {"kind": "profile", "subject": "chlorophyll a", "x": "value", "y": "depth",
     "unit": "ug/L", "display_unit": "mg/m3", "title": "Chlorophyll a with depth"}

Note that a microgram per litre and a milligram per cubic metre are the same number, so the
conversion is the identity and the label should say so rather than silently doubling up.
Compare with: the ship's own fluorometer profile from the current cast.

**3. The Tuborg and Disraeli tows.**

    {"kind": "profile", "subject": "Drepanopus bungei", "place": "Tuborg Lake",
     "x": "count", "y": "depth", "unit": "specimens",
     "title": "Two copepods in a lake shut off from the sea for three thousand years"}

Each tow was made *from* the depth shown *to* the surface, so a count belongs to the whole
column above it, not to the depth point. The widget must say so or draw it as a bar from the
surface to the tow depth. Rows with `count` "present" and no number need a distinct marker.

**4. What lives at 81 degrees 49 minutes north.**

    {"kind": "bars", "subject": "Insecta", "place": "Hazen Camp", "group_by": "subject",
     "y": "count", "unit": "species", "since": "1961", "until": "1962",
     "title": "Species taken in one season at Hazen Camp, by order"}

At present the counts live in the `count` field as text ("189 species", "11 species",
"about 40 species"). Either the widget parses a leading integer out of `count`, or these
rows want a numeric `value` with `unit` "species" beside the text count. The second is
cleaner and I would rather add it than have the front end guess.

**5. The record on the map.** The most valuable thing after the strip, and it needs no new
work: the topic's 300-odd observations are points with dates, and about 260 of them are
photographs with a position.

    {"kind": "layer", "subject": "Arthropoda", "domain": "biology",
     "since": "1818", "until": "2026",
     "title": "Every record of an insect, spider, springtail or mite in this layer"}

    {"kind": "layer", "subject": "Bacillariophyceae", "domain": "biology",
     "since": "1818", "until": "2026",
     "title": "Diatoms and algae recorded in the archipelago and Baffin Bay"}

The layer should walk the subject tree from the named subject downward, or these two are
almost empty: nearly every row is at species level. That tree-walk is the one piece of
machinery this topic needs most from the front end.

**6. Red snow through time.** Small but striking, and it runs from 1818 to now.

    {"kind": "track", "subject": "red snow", "x": "date_start",
     "since": "1818", "until": "2026",
     "title": "Where red snow has been recorded, 1818 to now"}

Four rows at present: Ross at the Crimson Cliffs in 1818, Kane there again in 1853, Greely's
people at the Carey Islands in 1881 and at Distant Cape in 1883. A `layer` would do as well;
`track` is right only if the intent is to show the ships' passages past the same cliffs.

## What the subject pages need from the front end

The subject page is generated from the note and then lays out the record. For this topic
that works well for the species with a handful of dated observations
(`Bombus polaris`, `Aedes nigripes`, `Drepanopus bungei`) and badly for the two hundred
higher-rank rows that exist only so the tree can be walked (`Arthropoda`, `Diptera`,
`Calanoida`). Those should show, instead of an empty record, **the records of everything
below them in the tree**, with the child subject named on each line. Without that, half the
subject pages in this topic are a paragraph and a blank.

## Units, so nothing is converted twice

- `chlorophyll a`: rows carry `ug/L` as written; the subject's unit is `mg/m3`; the two are
  numerically identical.
- soundings and tow depths: metres, as the papers give them.
- Bowman's counts: specimens, integers, and "present" where the paper gives no number.
- Oliver's counts: species, as printed, with the paper's own stated total (189) noted on the
  figure because the printed list adds to fewer.
- salinity in the Disraeli Fiord row: parts per thousand, as written, with a `qualifier` of
  "less than".
- Nothing in this topic is in a historical unit needing conversion, which is unusual for the
  layer: the small was measured in metric from the start, except Wollaston's globules, which
  are in fractions of an inch and are stored that way with the fraction in the qualifier.
