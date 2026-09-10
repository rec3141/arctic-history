# Birds: what to show, and how

A note for the operator and the front end. Three static plates are in the database
now; below each is the widget that should replace it once the front end can render
the six kinds. Everything here is driven by `observations.json` for topic `birds`.

## 1. First arrivals — the phenology strip

This is the topic's most valuable series and the one a scientist aboard is most
likely to want to compare against. Twenty-eight dated first-of-the-season records
run from Parry at Winter Harbour in 1820 to Tener on the Fosheim Peninsula in
1961, twenty-two of them with a day of the year and so plottable; the rows carry `qualifier` values beginning "first", the species in
`subject`, the place in `place` or `lat`/`lon`, and the observer.

The static plate is `birds-010`. As a widget it should be a `strip`, one lane per
species, x the day of the year rather than the absolute date, so that 1820 and
1961 fall on the same axis; the year, the place and the latitude belong in the
point's label. What the reader wants to do with it is add a point: the ship's own
first fulmar, first murre, first snow bunting of the season, entered from the
journal, dropping into the same lane.

    {"kind": "strip", "subject": "Aves", "x": "date_start", "group_by": "subject",
     "since": "1818", "until": "2026", "title": "The first bird of the year, 1820 to now"}

    {"kind": "strip", "subject": "Plectrophenax nivalis", "x": "date_start", "group_by": "place",
     "since": "1818", "until": "2026",
     "title": "When the snow bunting arrived, station by station"}

The snow bunting is the one species with enough records to compare places:
Winter Island (66.2 N) 27 April 1822, Fort Conger (81.7 N) 14 April 1882 and
24 April 1883, Ellesmere Island (78.8 N) 14 April 1935, Winter Harbour (74.8 N)
2 June 1820. Note that the two earliest dates are the two highest latitudes,
which is the interesting part and should not be smoothed away.

Units: none. Day of year on the x axis, with month rules rather than tick labels.

## 2. The colony counts — bars by site

**Now numeric.** Forty-three of the modern rows carry `value` and `unit` as well as
the source's own words in `count`: `breeding pairs` for a colony, `apparently
occupied sites` where the surveyors counted sites rather than pairs, `individuals`
for a national total, `mature individuals` for the COSEWIC figure. The text in
`count` is still the authority - "13,150 birds, 10,520 apparently occupied sites,
8,679 breeding pairs" is what Cape Vera's row says - and `value` is the one number
of that set a chart can use. Never mix the units on one axis: a bars widget must
filter on `unit` first. The static plate `birds-013` is what this looks like now,
on a log scale.

The modern rows (`birds-220` to `birds-236`) carry colony estimates as text in
`count`, not as numbers in `value`, because the sources give them as "10,520
apparently occupied sites, 8,679 breeding pairs" and the unit matters. A widget
that plots them must be told which of the two numbers to take; the honest
answer is to show breeding pairs and name the counting unit in the caption.

The static plate is `birds-011`, drawn from table 5 of Gaston, Mallory, Gilchrist
and O'Donovan 2006. As a widget:

    {"kind": "bars", "subject": "Fulmarus glacialis", "y": "value", "unit": "breeding pairs",
     "group_by": "place", "since": "1970", "until": "2010",
     "title": "Northern fulmar colonies of Nunavut, breeding pairs"}

This one needs the `value`/`unit` fields populated, which means a later run should
re-enter the colony rows with the pair count in `value` and the full wording kept
in `count` and `detail`. Until then the static plate stands in.

What a scientist would compare it with: the ship's own passage counts off Cape
Vera, Coburg Island and Prince Leopold Island, and the caution in the caption —
attendance varies so much day to day that one visit can count half or twice what
another does, so a single pass is not a census.

## 3. The cliff section — a diagram, not a widget

`birds-012` is a conceptual section showing which species holds which part of a
cliff and why the open water at the foot is the thing that makes the colony
possible. There is no series behind it and no widget should be built for it. It
belongs beside the bird-cliff places on the map and at the head of
`the-bird-cliffs` page.

## 4. Worth building, not yet drawn

**Camp Clay, spring 1884, as a strip.** Greely's game record at Cape Sabine is a
handful of dated rows (`birds-055` to `birds-061`) and it is the most affecting
thing in the topic: the first raven on 20 February, three ptarmigan on 15 March,
thirty-eight dovekies on 27 March, eleven dovekies and two ptarmigan on 1 April,
a raven used for shrimp bait on 18 May. Seven rows is too few for a plate on its
own but exactly right for a strip beside the party's own timeline.

    {"kind": "strip", "place": "Camp Clay", "x": "date_start", "group_by": "subject",
     "since": "1884-02", "until": "1884-06",
     "title": "What the hunters brought in at Camp Clay, 1884"}

**Tener's 1961 survey as a map layer.** The nineteen counts from the Queen
Elizabeth Islands Game Survey (`birds-170` to `birds-179`) are the only
systematic pre-1970 coverage of the archipelago's birds, and they are spread
across a dozen islands. They want a map, not a chart.

    {"kind": "layer", "subject": "Aves", "since": "1961-06", "until": "1961-08",
     "group_by": "subject", "title": "The Queen Elizabeth Islands game survey, 1961"}

**Every observation as a map layer**, filtered by species. This is the default
view a scientist would want: show me every record of the ivory gull in this
database, or of the thick-billed murre, on the chart beside the ship.

    {"kind": "layer", "subject": "Pagophila eburnea", "since": "1818", "until": "2026",
     "title": "Every ivory gull in the record"}

## 7. The Inuit and Inughuit knowledge, as its own layer

Forty-three observations now carry `method` `testimony`, and they are a different
kind of row from a sighting: the position is where the knowledge is held or where
the thing spoken of happens, the `observer` is the elder, hunter or community who
holds it, and the `detail` is the statement. They should not be mixed silently
into a sightings layer, because a reader who filters for "records of the raven"
would otherwise get a raven amulet and a raven shot from the rigging side by side
with nothing to tell them apart.

Give them their own toggle on the map, in a second colour, and label the pin with
the observer rather than the species. Where the observer is a named person the
pin should link to that person's page; where it is a community it should link to
the community's place.

    {"kind": "layer", "subject": "Aves", "since": "1820", "until": "2026",
     "group_by": "observer", "title": "What Inuit and Inughuit hold about the birds"}

The one series among them worth a chart rather than a map is the ivory gull's
decline as the four communities describe it (`birds-761` to `birds-764`), which
should sit directly beside the survey counts on the same axis, because the two
records are about the same fall in numbers and were made in different ways.

    {"kind": "strip", "subject": "Pagophila eburnea", "x": "date_start",
     "group_by": "observer", "since": "1970", "until": "2026",
     "title": "The ivory gull: what was counted and what was remembered"}

**The names are not a widget.** Every subject row now carries its Inuktitut and
Kalaallisut names with the source of each in the note, and the front end should
lay all of them out at the head of the subject page, each language labelled, with
the Inughuit forms that MacMillan and Rasmussen recorded shown as what they are -
one man's spelling of a spoken word - and not silently normalised to the
Nunavut orthography.

## Cautions for whatever renders these

- Four observations are marked `sensitive` (nests and colonies: `birds-031`,
  `birds-035`, `birds-037`, `birds-062`, `birds-070`, `birds-092`, `birds-112`,
  `birds-113`, `birds-132`, `birds-141`, `birds-176`, `birds-190`). Their
  positions must be coarsened and their places blanked in anything published, and
  no widget should let a reader zoom to a nest.
- Counts are text, deliberately: "about nine hundred", "myriads", "eight thousand
  birds a week", "a countless number". A widget that needs a number must skip the
  rows that have none rather than guess at them.
- Historical latitudes are as the source gives them and some longitudes are
  approximate (Knot Harbour, the Sabine Islands, the Fram's shooting grounds).
  Do not draw them to a precision they do not have.
