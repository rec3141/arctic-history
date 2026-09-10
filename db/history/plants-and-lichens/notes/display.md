# Display note: plants and lichens

For the operator and the front end, not a wiki page. What in this topic is worth showing,
what shape it should take, which fields of `observations.json` drive it, and which static
figure stands in for it now.

## 1. The first flower of the year, by species and place

The topic's central series. Every observation with `qualifier` beginning "first flower of
the season" carries a subject, a date and a place; the value that matters is the **day of
the year**, which the front end derives from `date_start` and must not round to a month.

A `strip` is the right widget: dated events by category, one row per subject, one mark per
observation, coloured by place or by latitude band. The reader wants to see six weeks of
arctic June compressed into one row per species and to compare 1883 with 1962.

    {"kind": "strip", "subject": "Saxifraga oppositifolia", "x": "date_start",
     "group_by": "place", "since": "1820", "until": "1970",
     "title": "The first purple saxifrage of the year, 1820 to 1962"}

    {"kind": "strip", "place": "Hazen Camp", "x": "date_start", "group_by": "subject",
     "since": "1962-06", "until": "1962-08",
     "title": "Twenty-six species come into flower in six weeks at Lake Hazen, 1962"}

Axis: date, plotted as day of year with the year as the category, never as an absolute
timestamp — 1820 and 1962 must fall on the same June. No unit conversion.
A scientist aboard compares these with the ship's own first-flower sightings entered
through the journal, and with the ECCC melt-onset dates for Alert and Eureka in
[[topic:the-weather-and-the-climate]].
Standing in for both now: **plants-and-lichens-900** (Hazen Camp 1962) and
**plants-and-lichens-901** (purple saxifrage, 1820-1962).

## 2. Fort Conger 1883 against Hazen Camp 1962

The same twelve species, two observers, eighty years. This is a `strip` with two rows per
species, or a `bars` grouped by subject with the day of year as the value. The `compare`
field is what it is for:

    {"kind": "strip", "place": "Fort Conger", "x": "date_start", "group_by": "subject",
     "since": "1883-06", "until": "1883-08",
     "compare": {"place": "Hazen Camp", "since": "1962-06", "until": "1962-08"},
     "title": "Fort Conger in 1883 and Lake Hazen in 1962: the same twelve plants"}

Caveat the front end should print with it: the sites differ in aspect and continentality
and 1962 was a warm year, so this is not a climate signal.
Standing in for it now: **plants-and-lichens-902**.

## 3. The species count of each historical collection

Eight observations carry `count` as a number of species and `method` of `survey`: Brown's
Melville Island list, Sutherland's fifty-four, Hart and Feilden's sixty-nine, Greely's
sixty-four, Simmons's hundred for Ellesmere and seventy for Foulke Fiord, Savile's
hundred and fifteen for the Lake Hazen basin, Powell's thirty-five above 1,060 m. A `bars`
by year tells the story of the flora being counted, not of the flora changing:

    {"kind": "bars", "subject": "Tracheophyta", "x": "date_start", "y": "count",
     "group_by": "place", "since": "1820", "until": "1970",
     "title": "How many species each expedition brought home"}

`count` here is free text ("about 100 species"); the front end must parse the leading
number and keep the words as the label. No static figure stands in for this yet.

## 4. The map layer

The obvious one, and the one @doc will use most: every plant observation as a point,
filterable by subject and by domain.

    {"kind": "layer", "domain": "biology", "since": "1820", "until": "2026",
     "group_by": "subject", "title": "Plant and lichen records"}

Two things it must do. First, filter on subject through **any** of the subject's names, so
that a query for *umingmak* or *aupilattunnguat* or *purple saxifrage* reaches the same
layer. Second, distinguish the historical collections (`method` of `specimen`, `hunt`,
`sighting`, `survey`) from the modern photographs (`method` of `camera`), because they
have completely different position accuracy: a nineteenth-century record is good to a
place name and a GBIF photograph is good to a GPS fix. Colour or symbol by `method`, and
say so in the legend.

## 5. Per-subject record

No widget needed: the generated subject page already lays out the record in date order.
What would improve it for this topic is that the record be shown **by day of year rather
than by year** for any subject whose observations are mostly phenological — purple
saxifrage, arctic willow, mountain avens, mountain sorrel — with the year as a label. That
is the same transformation as item 1 and could be one setting on the subject page.

## 6. What the ship should enter

The single most valuable thing a scientist aboard can add to this topic is a dated first
flowering with a position. The journal line is:

    {"kind": "observation", "id": "amundsen-2026-06-14-001", "subject": "Saxifraga oppositifolia",
     "date": "2026-06-14T09:20Z", "lat": 76.2, "lon": -81.4, "qualifier": "first flower of the season",
     "method": "sighting", "observer": "<crew name>", "origin": "ship",
     "detail": "First purple saxifrage seen ashore at ..."}

Second most valuable: a photograph of a plant with its position, entered as an image
artifact with the scientific name in `tags`, which joins it to the subject page.

## Units

There are none to convert in this topic. Dates are the measurement. Where a source gives
altitude in feet (Greely's ranges: "from the coast to 1,800 feet") the observation carries
`height` in metres as the schema requires and the prose keeps the figure as written; the
front end should print metres with the original in parentheses where the detail names it.
