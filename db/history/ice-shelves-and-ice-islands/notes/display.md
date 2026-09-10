# Display note: ice shelves and ice islands

A note for the operator and the front end, not a wiki page. It says how the rows of
this topic should be shown, what drives each view, and which static figure stands in
for it now.

The topic's rows are unusual in one way worth stating up front: almost every
observation is a **single measurement of a slow-changing thing**, decades apart, not
a dense series. There are four measurements of the epishelf lake in thirty-five
years and seven thicknesses of the Ward Hunt shelf in fifty. The right display is
therefore usually a sparse annotated series or a bar of discrete events, never a
smoothed line, and every point wants its observer and its method visible.

## 1. The calving record

**What to show.** Each recorded loss of shelf ice as a bar in the year it happened,
with the shelf named. This is the topic's headline: the shelves go in single
summers, not steadily.

**Fields.** `subject = "ice-shelf calving"`, `date_start` for x, `value` for y,
`unit` (all `km2` except the 1946 slab, which the source gives in miles and which is
entered as square miles in `unit`), `detail` for the label, `place` for the shelf.

**Units.** Square kilometres on the axis, square miles on the right; the sources
before 1970 wrote miles and after 1980 kilometres, and the rows keep what was
written.

**What a scientist aboard would compare it with.** The Canadian Ice Service weekly
charts for the same summers, and the September Arctic sea-ice minimum: the argument
of Copland, Mueller and Weir is that the shelves go when the sea ice in front of
them goes, so the two series belong on one screen.

**Stands in now:** `ice-shelves-and-ice-islands-091` (fig-losses).

    {"kind": "bars", "subject": "ice-shelf calving", "x": "date_start", "y": "value",
     "unit": "km2", "display_unit": "km2", "group_by": "place",
     "since": "1940", "until": "2012",
     "title": "What the Ellesmere ice shelves have lost, calving by calving"}

## 2. The epishelf lake of Disraeli Fiord

**What to show.** Depth of the fresh layer against date, four points, depth
increasing downward, each point labelled with its volume. The 2002 point is the
story and should be annotated, not merely plotted.

**Fields.** `subject = "epishelf lake"`, `date_start` for x, `value` for y, `unit`
`m`, `place = "Disraeli Fiord"`, `observer` for the label, `detail` for the volume.

**Units.** Metres on the left, feet on the right.

**Compare with.** The one remaining epishelf lake, in Milne Fiord, when its rows
exist; and the ship's own CTD casts, since this is the same measurement the Amundsen
makes every day.

**Stands in now:** `ice-shelves-and-ice-islands-092` (fig-epishelf).

    {"kind": "series", "subject": "epishelf lake", "place": "Disraeli Fiord",
     "x": "date_start", "y": "value", "unit": "m", "display_unit": "m",
     "since": "1962", "until": "2005",
     "title": "The lake drains: fresh water behind the Ward Hunt Ice Shelf"}

## 3. Ice-shelf thickness through the century

**What to show.** Every published thickness against the year, coloured by `method`
(seismic and radar, core, survey and freeboard), because the disagreement between
methods is as informative as the trend. Do not join the points with a trend line
without saying that the methods differ.

**Fields.** `subject = "ice-shelf thickness"`, `date_start`, `value`, `unit`
(`feet` before 1960, `m` after), `method`, `observer`, `place`.

**Units.** Metres on the left, feet on the right. The rows keep the written unit, so
the widget must convert on read: `feet` and `m` both occur under one subject.

**Compare with.** The ship's own ice-thickness measurements, and the sea-ice
thickness rows of `the-sea-ice`: the point that lands is that shelf ice is an order
of magnitude thicker than any floe.

**Stands in now:** `ice-shelves-and-ice-islands-093` (fig-thickness).

    {"kind": "series", "subject": "ice-shelf thickness", "place": "Ward Hunt Ice Shelf",
     "x": "date_start", "y": "value", "unit": "m", "display_unit": "m",
     "group_by": "method", "since": "1900", "until": "2012",
     "title": "A century of measuring the Ward Hunt Ice Shelf"}

## 4. The drifts of the ice islands

**What to show.** The dated positions of an ice island on a map, one island at a
time, with the shelf it calved from marked. Three tracks exist as artifacts already
(`-004` WH-5, `-005` the Ayles ice island, `-006` T-3), but the observations carry
the same positions and a `track` widget over them lets the reader pick a date range
and see where the island was.

**Fields.** `subject = "ice island"`, `date_start`, `lat`, `lon`, `place` for the
island, `detail`, `confidence` — and `confidence` matters here: many of Nutt's
WH-5 longitudes are inferred from a place name and the rows say `probable`. A track
widget should draw an inferred position hollow and a fixed one filled.

**Compare with.** The ship's own position, and the modern ice-island fragments the
Canadian Ice Service still charts in Baffin Bay: an ice island off Labrador is not a
historical curiosity.

**Stands in now:** `ice-shelves-and-ice-islands-094` (fig-wh5-track), and the three
track artifacts on the map.

    {"kind": "track", "subject": "ice island", "place": "Ice island WH-5",
     "x": "date_start", "y": "value", "unit": "km",
     "since": "1962-06", "until": "1964-08",
     "title": "The drift of ice island WH-5, 1962 to 1964"}

    {"kind": "track", "subject": "ice island", "place": "Ayles ice island",
     "x": "date_start", "y": "value", "unit": "km",
     "since": "2005-08", "until": "2007-06",
     "title": "The Ayles ice island, from the hour it broke free"}

## 5. The rolls, as a profile

**What to show.** The ridge-and-trough profile across the shelf, as Crary's transit
line of 1954 gives it: 11.9 miles of shelf, about seventy-five ridge systems, mean
wavelength 760 feet, greatest trough-to-crest 21.2 feet, ridges about 24 feet above
sea level near land. The layer does not hold the levelled points themselves — only
the summary numbers — so a true `profile` widget waits on someone digitising Fig. 2
of Hattersley-Smith 1957, which is held as artifact
`ice-shelves-and-ice-islands-033`.

**Until then**, show the rolls as a bars view of wavelength and trough depth by
place, which is what the rows support: near Ward Hunt 200 to 300 yards and 5 to 20
feet; near Point Moss about 100 yards and not more than 5 feet; on T-3 300 to 1,000
yards and about 10 feet; on the RADARSAT image of 1999, 235 m and 3.5 m.

**Stands in now:** panel two of the diagram,
`ice-shelves-and-ice-islands-095`.

    {"kind": "bars", "subject": "the rolls", "x": "date_start", "y": "value",
     "unit": "yards", "display_unit": "m", "group_by": "place",
     "since": "1876", "until": "2003",
     "title": "The rolls: wavelength and relief, where they were measured"}

## 6. Everything, on the map

**What to show.** A layer of every observation of this topic, filtered by subject and
by date range, so a reader can watch the fringe empty. Slide the date range from
1876 to 2008 and the points move from Aldrich's sledge tracks to satellite scenes,
and the coast goes from continuous shelf to six remnants.

    {"kind": "layer", "subject": "ice shelf", "since": "1876", "until": "2021",
     "title": "The Ellesmere ice shelf, observation by observation"}

    {"kind": "layer", "subject": "ice island", "since": "1946", "until": "2021",
     "title": "Every recorded ice island, from T-1 to the Milne islands of 2020"}

## What a widget cannot do here, and needs a person for

Two things this topic wants and cannot get from its own rows:

- **The area of the whole fringe by year.** The published figures are on
  inconsistent bases — 443 square kilometres is the Ward Hunt remnant in 1982, 1,043
  is all six shelves in 2004, 720 is all six after 2008 — and a bar chart that put
  them side by side would lie. A proper area series needs the shelf outlines
  digitised from the 1959 air-photograph mosaic, the 1984 mosaic and the modern
  satellite record, which is a mapping job, not a reading job.
- **The rolls as a real profile.** See section 5.


## Added in the second run, 2026-09-10

**The end of the series must run to 2020, not 2008.** The rows now carry the Ward
Hunt ice island of 18 August 2010 and the Milne calving of 30 to 31 July 2020 (the
shelf from 187 to 106 square kilometres, ice islands of 55 and 24 square
kilometres, the last epishelf lake in the northern hemisphere gone with it), so
every `since`/`until` in this note has been extended and the losses plate
(`ice-shelves-and-ice-islands-091`) is now out of date at its right-hand end: it
stops at 2008 and should be redrawn with the 2010 and 2020 bars. That redraw is
the first figure job for the next run.

**A before-and-after pair is worth a widget of its own.** The strongest thing the
topic now holds is matched satellite views of the same coast on two dates:
`ice-shelves-and-ice-islands-136` and `-137` (22 July and 29 August 2008),
`-138` and `-139` (22 August 2002 and 18 August 2010), `-156` and `-157`
(30 July and 11 August 2020), and `-131` and `-132` (the Ayles in 2002 and 2006).
The front end has no `pair` kind and should not gain one for this; the honest
fallback is a `layer` filtered to `satellite-image` with the date slider, or a
static plate that sets two of them side by side with a scale bar. Say in the
caption which instrument each came from, because the resolutions differ by two
orders of magnitude between ASTER and MODIS.

**The Milne rows are a series with two points and should not be plotted as one.**
187 and 106 square kilometres are the same shelf four days apart and belong in the
text, not on an axis.
