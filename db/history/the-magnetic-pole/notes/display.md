# How the magnetic record should be shown

A note for the operator and the front end. Not a wiki page.

The magnetic half of this layer has an advantage nothing else here has: **the units
have not changed in two hundred years.** A dip in degrees read by Edward Sabine in
1820 and a dip in degrees read by the Alert magnetometer today are the same quantity,
measured the same way, with no correction between them. So the display should lean
hard on direct comparison across the whole span, and should never hide the original
number behind a conversion.

Two rules for every widget in this topic:

1. **Degrees stay degrees.** The only conversion worth offering is degrees-and-decimal-
   minutes as the sources print them (`89 deg 59.465 min`) beside decimal degrees
   (`89.9911`), and for dips near the vertical, **minutes short of the vertical**
   (`(90 - value) * 60`), which is the number that actually carries information up
   there. Use that as the right-hand axis wherever dip is plotted.
2. **Say whether a position was measured or computed.** Every `North Magnetic Pole`
   observation in this topic carries either `method: instrument` (Ross 1831,
   Amundsen 1904) or `method: chart` (the gufm1 and IGRF model positions), and its
   `qualifier` says so in words. A widget that draws them the same way is lying. The
   two measured fixes should be a different mark, and the model line should be
   visibly a line and not a set of observations.

---

## 1. The pole's wander — the headline widget

The single thing a scientist aboard will want to see. A dated track on a polar map,
scrubbable by year, with the two ground fixes called out.

    {"kind": "track", "subject": "North Magnetic Pole", "x": "date_start",
     "since": "1590", "until": "2025",
     "group_by": "method",
     "title": "Where the North Magnetic Pole has been since 1590"}

Notes for the implementation:

- The geometry is already in the layer as track artifact `the-magnetic-pole-003`
  (waypoints at ten-year steps, 1590-2020); the widget should draw that as the line
  and the `North Magnetic Pole` observations as the marks on top of it.
- **Projection matters here and nowhere else in this layer.** The track runs from
  70 N to 86 N and crosses the date line. In any cylindrical projection it is
  nonsense. Use a north polar stereographic or azimuthal equidistant centred near
  100 W.
- `group_by: method` separates `instrument` (Ross 1831, Amundsen 1904) from `chart`
  (model). Draw `instrument` as a filled star with the observer's name; `chart` as
  small open circles.
- A ship's-position marker would earn its place: the great-circle bearing and
  distance from the ship to the current modelled pole, updated from the GPS, is a
  question people actually ask on the bridge.
- **Static stand-in now:** `the-magnetic-pole-004`.

## 2. The pole's speed

Shows the one genuinely surprising fact in the topic — three centuries of near-stillness,
then a sprint after 1990.

    {"kind": "bars", "subject": "North Magnetic Pole", "x": "date_start", "y": "value",
     "unit": "km/yr", "since": "1600", "until": "2025", "group_by": "date_start",
     "title": "How fast the pole has moved, kilometres a year"}

This one does **not** come straight out of `observations.json`: the speed is a
derived quantity, the great-circle distance between successive track waypoints
divided by the interval. Either the publish step should compute it from
`the-magnetic-pole-003` and emit it as a series, or the front end should. It is not
worth entering forty derived observations to make a bar chart out of.

**Static stand-in now:** `the-magnetic-pole-007`.

## 3. Ross's journey to the pole, dip against date

A short, dense, self-contained series: fifteen readings over thirteen days that go
up to the vertical and come back down. It is the best small story in the topic.

    {"kind": "series", "subject": "magnetic dip", "x": "date_start", "y": "value",
     "unit": "deg", "display_unit": "minutes short of vertical",
     "since": "1831-05-28", "until": "1831-06-09",
     "title": "James Clark Ross's dips on the march to the magnetic pole"}

- `display_unit` here means `(90 - value) * 60`. Nothing else makes the shape legible:
  the whole series lives inside 0.9 of a degree.
- Draw the 90-degree line. Two of the readings sit above it, and that is not an error
  — it is the daily variation carrying the point of vertical dip past the observer,
  and it is the reason Ross refused to claim he had stood on the exact spot.
- Each point should show the reading as printed (`89 deg 58.52 min`), the time of day
  from the `detail`, and the page.

**Static stand-in now:** `the-magnetic-pole-005`.

## 4. Dip as a function of distance from the pole

The cross-expedition plate: every numbered dip in the topic against its great-circle
distance from Ross's 1831 position, coloured by expedition. It shows what the
instrument was actually measuring and it puts Parry, Ross, Kane, Hayes and Amundsen
on one axis.

    {"kind": "profile", "subject": "magnetic dip", "y": "value", "unit": "deg",
     "display_unit": "minutes short of vertical",
     "group_by": "observer", "since": "1819", "until": "1904",
     "title": "The dip is a distance from the pole"}

`profile` is the right kind (value against a spatial coordinate rather than time),
but the x here is **distance from a named point**, which the vocabulary does not
express. Either add a computed `distance_from` field to `observations.json` at
publish, keyed to a reference position given in the spec, or leave this one as a
static plate. It is not urgent: the static plate says it.

**Static stand-in now:** `the-magnetic-pole-006`.

## 5. Declination as a map layer

Declination is a field, not a series, and its natural display is spatial: every
observation dropped where it was made, labelled with the value and the year.

    {"kind": "layer", "subject": "magnetic declination", "since": "1819", "until": "1905",
     "unit": "deg", "group_by": "observer",
     "title": "Every recorded variation of the compass, 1819 to 1905"}

- Values run from 48 degrees west at Repulse Bay to 165 degrees **east** at Byam
  Martin Island. The sign is the whole point — the observations carry it in
  `qualifier` as the word "easterly" or "westerly", not in the number, because that
  is how the sources print it. **A widget that plots the raw `value` without reading
  the qualifier will put Byam Martin Island on the wrong side of the pole.** If the
  publish step can normalise to signed degrees east-positive it should, and should
  keep the printed form in the tooltip.
- The natural comparison a scientist aboard would want: the modern declination at
  the ship's position from the World Magnetic Model, beside the nineteenth-century
  value at the nearest historical station. The difference at some of these places is
  tens of degrees.

## 6. The storms

Nine rows, no time series behind them, because the Fort Conger magnetograms were
never digitised. A dated strip is honest about that; a line chart would not be.

    {"kind": "strip", "subject": "magnetic storm", "x": "date_start",
     "group_by": "place", "since": "1875", "until": "1884",
     "compare": {"subject": "aurora", "since": "1875", "until": "1884"},
     "title": "Magnetic disturbance and aurora at the polar-year stations"}

The `compare` block is the useful part and it crosses topics: the aurora
observations belong to `the-sky`, and laying the two strips against each other is
exactly the comparison Greely made by eye and wrote up as the station's general
result. Entries where the magnet stayed quiet under a bright aurora (Floeberg Beach,
28 November 1875; Fort Conger, January 1883) must be shown, not filtered out as
null: the absences carry the finding.

## 7. What is missing, and what would fill it

The topic has no real time series in it yet, only extremes and milestones, because
the two great continuous records were never entered in a machine-readable form:

- **Fort Conger, 1 July 1882 to 30 June 1883.** Hourly declination on Gottingen
  time, plus term-day sequences at twenty-second intervals. Reduced and printed as
  an appendix to `greely1888report`; the rest went to the US Coast and Geodetic
  Survey. If a run digitises that appendix it becomes a `series` widget with
  something like eight thousand points, and the storm of 17 November 1882 becomes a
  curve instead of a sentence.
- **Gjoahavn, 2 November 1903 to June 1905.** Nineteen months of continuous
  registration, published in the Norwegian scientific results of the Gjoa
  expedition, which this layer does not hold. It is the longest early record
  anywhere near the pole.
- **Resolute and Alert, 1950 to now.** Already open, already digital, from the NRCan
  Geomagnetic Laboratory. A `series` of the daily declination or the hourly
  horizontal component at those two observatories, with the ship's own position
  marked on it, is the widget that would tie the whole topic to the present cruise —
  and it is the one that a run with network time should build next.

Until any of those exist, the five static plates above are the topic's display.

## 8. Added since: the observatory network, and the knowledge that is not a number

Two things went into the record after the sections above were written, and both
want display.

**The Canadian magnetic observatory network is now in the database as places**, not
just as a sentence: Alert (IAGA code ALE), Eureka (EUA), Resolute (RES), Cambridge
Bay (CBB) and the closed station at Mould Bay (MBC), each with its position, all of
kind `magnetic-station`, plus the four named field stations round Gjoahavn that
Amundsen's men called Edler's Høi, Scott Hansen's Høi, Aksel Steen's Høi and
Bauer's Høi. `the-magnetic-pole-218` is the static plate that shows them against the
pole's track, and it is the picture the topic should open on. The widget that would
replace it:

    {"kind": "track", "subject": "North Magnetic Pole", "x": "date_start",
     "since": "1590", "until": "2025",
     "compare": {"subject": "North Magnetic Pole", "place": "Resolute magnetic observatory"},
     "title": "The pole's track, with the observatories that watch it"}

A `layer` spec does the stations on their own, and is the cheaper thing to build
first, because every station is already a `place` row with a natural kind:

    {"kind": "layer", "subject": "North Magnetic Pole", "place": "",
     "since": "1819", "until": "2026",
     "group_by": "method",
     "title": "Every magnetic observation in the archipelago, by how it was made"}

`group_by: "method"` is the useful part. The topic's rows now carry five methods -
`instrument`, `station-record`, `survey`, `chart` and `testimony` - and colouring
the map by them separates a dip circle on a beach from an observatory trace from a
sledge station from a thing somebody was told.

**Testimony rows are now in the topic and they do not carry numbers.** Ten of them:
Boas's rule of steering by sun, wind and snowdrift; Rasmussen's compass useless off
King William Land and Alurniq holding the course without one; Qaqortingneq's line of
seal skulls; the Netsilingmiut drawing the coast on the ice for John Ross in 1831;
Talurnakto and Ugpi on the magnetic boat journey of 1904; Navya's pen across Wiik's
journal. A `series` or `bars` widget cannot show any of them, and they must not be
dropped for having no `value`. The right form is the strip, keyed on the observer:

    {"kind": "strip", "subject": "North Magnetic Pole", "x": "date_start",
     "group_by": "observer", "since": "1829", "until": "1938",
     "title": "What was known of the magnetic country, and who knew it"}

The front end should treat a null `value` as a fact about the row and not as missing
data: a testimony observation is displayed by its `detail` and its observer, and the
observer's name is the label, because the point of the row is who held the
knowledge. Where an observation's `--sensitive` flag is set the position is already
coarsened before it reaches the tab; none of this topic's rows is sensitive.

**Still missing, unchanged:** the Fort Conger hourly declination of 1882-83 and the
Gjoahavn photograms of 1903-05, neither of which exists in machine-readable form,
and the open Resolute and Alert minute data, which does exist but whose yearly-mean
pages did not answer from this network. Those three are what would turn section 7's
list into working `series` widgets.
