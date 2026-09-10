# Display note: the sea ice

For the operator and the front end. What the sea-ice record should look like on the tab, which fields drive it,
and which of the static plates stands in until a widget exists.

## 1. The winter's ice growth  (the centrepiece)

Bernier's weekly gauge at Albert Harbour, Mittimatalik, 1906-07 is the only fine-grained ice-growth series in the
layer, and it is exactly the shape a scientist aboard already has in their head. It should be a widget, because
the interesting act is comparing one winter with another and with a modelled or measured present-day curve.

- Drives on: `subject = "sea-ice thickness"`, `date_start`, `value`, `unit`, `lat`/`lon`, `observer`, `qualifier`.
- Axis: inches on the left as written, centimetres on the right. Never convert in the row.
- The x axis is the **ice year**, 1 October to 30 September, not the calendar year, or the winters do not overlay.
- What a scientist aboard compares it with: the ship's own ice-thickness readings, and the CIS ice climate normals
  for the same waters. Neither is in the layer yet.
- Stands in now: `the-sea-ice-fig-001`.

    {"kind": "series", "subject": "sea-ice thickness", "place": "Albert Harbour",
     "x": "date_start", "y": "value", "unit": "inches", "display_unit": "cm",
     "since": "1906-10", "until": "1907-08",
     "compare": {"subject": "sea-ice thickness", "place": "Arctic Bay", "since": "1910-09", "until": "1911-08"},
     "title": "Bernier's winter of ice at Pond Inlet against his winter at Arctic Bay"}

## 2. Freeze-up and break-up as a strip

Every freeze-up and break-up date in the layer, by year and by place, on one line each. This is the widget the
question "is this late?" wants, and it is the one that will improve most as later runs add dates.

- Drives on: `subject in ("freeze-up", "break-up")`, `date_start`, `place`/`lat`/`lon`, `observer`, `qualifier`.
- The strip's x axis is day of the ice year; the row is the place; the colour is which of the two events it is.
- Compare with: the CIS 1991-2020 normals for that water, once those are entered as observations.
- Stands in now: `the-sea-ice-fig-003`, which draws the five winterings where both ends are known.

    {"kind": "strip", "subject": "freeze-up", "x": "date_start", "group_by": "place",
     "since": "1818", "until": "2026",
     "compare": {"subject": "break-up", "group_by": "place"},
     "title": "When the sea took its ice and when it broke, by place"}

## 3. The besetments as bars

Duration, not date, is the quantity: a besetment of three days and one of two hundred and fifty-one are different
kinds of event. Ordered by date so the reader can see the century pass.

- Drives on: `subject = "besetment"`, `date_start`, `date_end`, `vessel`, `observer`, `detail`.
- The bar length is `date_end - date_start` in days; a besetment with no end date is drawn as one day and flagged.
- Stands in now: `the-sea-ice-fig-002`.

    {"kind": "bars", "subject": "besetment", "y": "date_end", "x": "date_start",
     "group_by": "vessel", "unit": "days", "since": "1818", "until": "1950",
     "title": "How long the ice held each ship"}

## 3b. The satellite extent record

All 95 monthly means of the passive-microwave record are now observations: March and September for every year
from 1979. This is the one continuous, evenly sampled series in the topic, so it is the natural spine to hang the
historical points on, and the natural thing for the ship's own ice observations to be placed against.

- Drives on: `subject = "sea-ice extent"`, `date_start`, `value`, `unit` (million km2), `qualifier` (which month).
- Two series on one axis: March, the maximum, and September, the minimum. Never average them.
- The comparison a scientist aboard wants is not another curve but the historical points: a freeze-up date or a
  besetment from the narratives, annotated on the same time axis, so that 1857 and 2026 are on one page.
- Stands in now: `the-sea-ice-fig-006`.

    {"kind": "series", "subject": "sea-ice extent", "x": "date_start", "y": "value",
     "unit": "million km2", "since": "1979-01", "until": "2026-12",
     "group_by": "qualifier",
     "title": "The Arctic maximum and minimum, 1979 to 2026"}

## 4. The ice observations as a map layer

The most useful thing on the map is not any one series but all of it at once, filtered by kind of ice and played
through the season. An ice edge met on 24 July at 79 degrees north is a datum a navigator can use directly.

- Drives on: every observation with `domain = "sea-ice"`: `lat`, `lon`, `date_start`, `subject`, `detail`, `vessel`.
- The filter that matters is the **month**, not the year: the archipelago's ice is a seasonal cycle, and two
  centuries of July observations laid on one map is a climatology.

    {"kind": "layer", "subject": "pack ice", "since": "1818", "until": "2026",
     "group_by": "subject", "title": "Where the ships met the ice, by month"}

## 5. The drifts as tracks

Two of the three are now in as track artifacts with dated waypoints: `the-sea-ice-trk-001`, the Fox from Melville
Bay to the Atlantic (17 August 1857 to 26 April 1858, 242 days and 1194 geographical miles), and
`the-sea-ice-trk-002`, the Polaris floe party from Smith Sound to the Labrador Sea (15 October 1872 to 30 April
1873). Plate `the-sea-ice-fig-005` draws both on one map with their milestones. Greely's six weeks down Kane
Basin in August and September 1883 is the third and is still only a scatter of points.

**The thing the front end must not lose is that these are latitudes, not positions.** Both journals give latitude
after latitude and almost no longitude: one longitude in Tyson's whole drift, none in McClintock's. The
longitudes in the waypoints are set on the axis of the drift and are declared as such in each artifact's
description. A track widget should therefore draw the line thin or dashed, and where it can, put the honest
quantity on the axis instead: latitude against date, which is what the record actually holds.

    {"kind": "track", "subject": "besetment", "x": "date_start", "since": "1857-08", "until": "1858-04",
     "title": "The Fox in the pack, Melville Bay to the Atlantic"}

    {"kind": "series", "subject": "besetment", "x": "date_start", "y": "lat", "unit": "degrees north",
     "since": "1857-08", "until": "1858-05",
     "compare": {"subject": "floe", "since": "1872-10", "until": "1873-05"},
     "title": "How fast the ice carried them south: latitude against date, the Fox and the floe party"}

Tyson's January reckoning of latitude 72 cannot be reconciled with his December positions; it is kept as an
observation and left off the line. That disagreement is worth showing rather than smoothing.

## 6. What Inuit and Inughuit said, as a layer and as a strip

The testimony rows are observations like any other and belong on the map with the rest, but they answer a
different question, so they want their own filter: `method = "testimony"`. Fifty of them now carry a named
Inuk or Inughuit observer, a place and a date, and the useful thing about them is that they are statements
about how the ice behaves rather than readings of it - the wind that parts the moving ice, the moon that
opens a crack, the animal that says the freezing is over. A scientist aboard should be able to put them on
the same map as the ships' ice observations and see that they are describing the same coast.

- Drives on: `method = "testimony"`, `observer`, `place`/`lat`/`lon`, `date_start`, `subject`, `detail`, `bibkey`.
- The observer is the point: show the name, the community and the source on the pin, never an anonymous dot.
- Two dates matter and are not the same: the date of the statement and the date of what is described. Where
  the source gives only the interview year, that is what the row carries, and the pin should say so.
- Nothing stands in for this now; it is a layer, not a plate.

    {"kind": "layer", "subject": "fast ice", "since": "1900", "until": "2026",
     "group_by": "observer", "title": "What Inuit and Inughuit said of the ice, by who said it"}

The one series in this material is the change the communities state themselves - the floe edge at
Pikialasorsuaq moved about forty kilometres, the ice bridge of Ikeq forming later or not at all. Those are
two points, not a series, and they should be drawn against the NSIDC extent record rather than on their own,
as an annotation on plate 4's timeline: a sentence in words beside a curve in numbers, which is the pairing
this whole topic is for.

## 7. What is deliberately not a widget

The Inuktitut vocabulary. It is a picture, not a series: the section drawing `the-sea-ice-fig-004` labels the ice
in both vocabularies at once, and the subject pages carry the names as fields. A table of words would lose the
thing that matters, which is where on the ice each word applies.

## Units, once, for all of the above

Thickness is entered in the unit written - Parry's and Bernier's inches, Greely's inches, Nares's feet - and
converted only on the axis. Concentration is in tenths where a source gives it and in words where it does not;
never invent tenths from a narrative's "close pack". Extent is in million square kilometres. Dates are as written,
and a date given as a month is drawn at the month's end for a break-up and its start for a freeze-up.
