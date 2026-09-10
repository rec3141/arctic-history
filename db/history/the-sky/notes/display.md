# The sky: how this topic should be shown

A note for the operator and the front end, not a wiki page.

The sky topic is unusual among the nature topics in that most of its rows carry
no number. An aurora on a given night is a fact with a date and a place and no
value; a mock sun is a fact with an angle. So the two useful display forms here
are **dated events by category over time and space** (`strip`, `layer`) and **a
small number of genuinely measured quantities** (`series`, `bars`). Nothing in
this topic wants a `profile`, and only one thing wants a `track`.

The four static figures already registered stand in for the widgets below until
the front end implements the six kinds.

---

## 1. The polar night, station by station — the signature display

**What it should be.** A horizontal interval chart: one row per wintering,
ordered by latitude, each row the span from the last sight of the sun to the
first, drawn against a day-of-year axis running October to March. Mark the winter
solstice. Annotate rows where the source says something about the horizon.

**Why.** It is the one display that makes the topic's central point visible in a
second: the length of a station's darkness is a property of the place, not just
of the latitude. Camp Clay at 78.7 N loses the sun for a shorter interval than
Rensselaer Harbour at 78.6 N because of a ridge.

**Fields.** `observations.json`, filtered to `subject in ("the polar night",
"the return of the sun")`, using `date_start`, `place`, and the station latitude
from `places.json`. The pairing of a departure row with the following return row
at the same place is the only computation.

**Axis and units.** Day of year on x; no unit conversion. The interval in days is
a derived label, and where the source states its own count (Parry's
eighty-four days, Ross's fifty, the Polaris's hundred and thirty-two) that
figure is in `value` with `unit` = `days` and should be shown in preference to
the computed one, because the two sometimes disagree and the source's is the
record.

**What a scientist aboard compares it with.** The ship's own position and date:
"how long would the sun be gone where we are now, and how does that compare with
Fort Conger". A computed sunrise/sunset for the ship's latitude is the natural
overlay.

**Stands in for now.** `the-sky-601`, the-sky-fig-polar-night.png.

    {"kind": "strip", "subject": "the polar night", "x": "date_start",
     "group_by": "place", "since": "1818", "until": "1890",
     "title": "How long the sun was gone, station by station"}

---

## 2. The measured halo and parhelion angles

**What it should be.** A one-dimensional dot plot: every observation whose `unit`
is `deg` and whose subject is in the halo family, laid out against a degree axis
with a rule at 22, one row per measurement, labelled with date, place and the
figure as the source printed it.

**Why.** These are real measurements taken with a sextant between 1819 and 1872,
and they are good ones. Showing them against the theoretical 22 degrees is the
cleanest demonstration in the layer that the nineteenth-century Arctic record is
quantitative and usable.

**Fields.** `value`, `unit` (`deg`), `subject`, `date_start`, `place`, `detail`
(which carries the as-printed degrees-and-minutes form), `observer`.

**Axis and units.** Degrees, no conversion. **Note for the front end:** the row's
`value` is decimal degrees while the source printed degrees and minutes; the
as-printed form is in `detail` and in `qualifier` where it exists, and the label
should use the printed form, not the decimal.

**Compare with.** 22.0 degrees (minimum deviation of a 60-degree ice prism) and
46.0 degrees (the 90-degree prism). Both are constants, not data.

**Stands in for now.** `the-sky-602`, the-sky-fig-halo-angles.png.

    {"kind": "bars", "subject": "solar halo", "y": "value", "unit": "deg",
     "group_by": "date_start", "since": "1819", "until": "1875",
     "title": "What the navigators measured when they measured a halo"}

(`bars` is the nearest of the six kinds; a `strip` laid on a value axis rather
than a date axis would be better, and is worth a seventh kind if one is ever
added.)

---

## 3. The auroral record as a map layer

**What it should be.** A map layer of every aurora observation, filtered by
subject and date range, with the point's date shown and the map able to play
through the years. Colour by `confidence`, or by whether the source calls the
display coloured or colourless — that distinction is the one Greely found to
matter.

**Why.** The gradient is spatial. Plotted on a map the thinning of the aurora
northward from Boothia to Ellesmere Island is obvious, and it is the auroral
oval. Overlay the modern oval (a fixed ring in geomagnetic coordinates) and the
nineteenth-century record explains itself.

**Fields.** `subject` = `aurora`, `lat`, `lon`, `date_start`, `observer`,
`detail`, `bibkey`.

**Compare with.** The modern auroral oval, and the ship's own space-weather feed
if one is available. A scientist aboard asking "is tonight a good night" is
asking the same question as Greely's observers.

**Stands in for now.** `the-sky-603`, the-sky-fig-record.png (which uses latitude
rather than a map, and covers all subjects, not only the aurora).

    {"kind": "layer", "subject": "aurora", "since": "1818", "until": "1890",
     "title": "Every aurora logged from the ice, 1818-1884"}

---

## 4. Aurora frequency against station latitude

**What it should be.** Bars: the count of aurora observations per wintering,
grouped by place, with the place's latitude on the label.

**Why not yet.** This is the display the topic most wants and the one the data
cannot honestly support. The rows here are a sample of what the narratives set
down, not a complete register: Parry logged aurora on many more nights than are
entered, and the Fort Conger register is summarised in the report by the month
rather than by the night. A bar chart of the counts would be a chart of how much
each researcher extracted, not of how much aurora there was.

**What would fix it.** Two things exist and are not yet in: Greely's own monthly
auroral counts in the Lady Franklin Bay report, which are real counts and can be
entered as observations with `unit` = `auroras` and `count`; and Parry's and
Ross's meteorological abstracts, which give a nightly aurora column. A run that
enters those turns this into an honest figure. Until then the caption must say
what the counts are counts of.

    {"kind": "bars", "subject": "aurora", "group_by": "place",
     "since": "1818", "until": "1890",
     "title": "Nights with aurora, by station"}

---

## 5. The sun's return date against latitude

**What it should be.** A series: observed date of the sun's return against the
station's latitude, with the geometric (flat-horizon) date as a comparison curve.

**Why.** The gap between the two is the combined effect of refraction and the
local horizon, and it is measurable from this record: Parry's twelve days at
Winter Harbour, Greely's two days at Fort Conger, the Alert's hilltop against its
deck. It turns a set of anecdotes into a quantity.

**Fields.** `subject` = `the return of the sun`, `date_start`, `place`, and
latitude from `places.json`. The comparison curve is computed, not stored.

**Compare with.** The modern computed sunrise for each station, which the ship's
own almanac can supply.

    {"kind": "series", "subject": "the return of the sun", "place": "Fort Conger",
     "x": "date_start", "y": "value", "unit": "days",
     "since": "1818", "until": "1890",
     "compare": {"subject": "the return of the sun", "place": "Winter Harbour"},
     "title": "How many days refraction and the horizon give back"}

---

## 6. The Inuit sky as a calendar, not a chart

**What it should be.** Not a figure. The Inuit constellation subjects
(`Inuit constellations` and its sixteen children) should be laid out as a wheel
or a strip of the year showing what marks what: Aagjuuk at the solstice,
Sivulliik and Kingulliq with the returning light, Ullaktut and Akuttujuuk with
the turn of the seasons, Tukturjuit and Quturjuuk as the hour hand of the night.

**Why.** The point of the system is that it is a calendar and a clock, and a
scatter plot destroys that. Set beside the polar-night chart of display 1 it
makes the comparison the topic exists to make: the ships computed the sun's
return from tables and were often wrong by days; the Iglulingmiut read it off the
eastern sky.

**Fields.** `subjects.json` filtered to `parent = "Inuit constellations"`, with
the season each marks taken from `note`. There is no dated observation behind
most of them, and there should not be a fake one.

**Not yet drawn.** It wants the seasons stated per subject as structured data
rather than in prose, which in turn wants MacDonald's own pages (request 61).

---

## Things deliberately not shown

- **A halo or aurora photograph gallery keyed to the historical rows.** The
  Commons images registered here illustrate the phenomena; almost none of them
  are of the archipelago, and their positions are nominal. They should be shown
  on the subject pages as illustration and kept off the map, or the map will fill
  with points at 74.7 N 94.9 W that mean nothing. **The front end should filter
  the map on `tags` and exclude artifacts whose description says the position is
  nominal.**
- **Anything about the transit of Venus of 1882 plotted at Fort Conger.** It was
  not observable there. The subject page says so; there is no observation row and
  there must not be one.
