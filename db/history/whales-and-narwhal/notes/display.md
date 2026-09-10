# Display note: whales and narwhal

For the operator and the front end. What the record of this topic wants to look like, which
fields drive it, and which static plate stands in for it until the widget exists.

## 1. The catch by year and ground

The spine of the topic. 47 catch-record observations carry the year in `date_text`, the ground
in `place` (Davis Strait, Hudson Bay), and the number of whales in `count` as a string
("44", "1,632", "28,394" for the grand totals). A reader should be able to slide across
two centuries and see the fishery rise and collapse, and to click a year and get the row.

Axis: whales secured in the year, a plain count; no conversion. The x axis is the year.
The grand-total rows (ids 045, 046, 047) carry a `/` date range and must be excluded from a
by-year chart or they swamp it — filter on `date_text` not containing "/".

What a scientist aboard would compare it with: the modern abundance estimates. About 6,000
Eastern Canada-West Greenland bowhead in 2009 against a recorded kill of 28,394 in Davis
Strait alone is the comparison that makes the topic worth reading.

Static plate now: `whales-and-narwhal-020`.

    {"kind": "bars", "subject": "Balaena mysticetus", "x": "date_start", "y": "count",
     "group_by": "place", "since": "1719", "until": "1915",
     "title": "Bowhead secured, by year and whaling ground"}

## 2. The last years, by species

Five ship-seasons between 1884 and 1888 in which the species composition of a whaler's catch
is the whole story: bowhead against narwhal, beluga and bottlenose. Drives off `vessel`,
`date_text`, `subject` and `count`. Note that a plain query on vessel picks up individual
kills as well as season totals; the season totals are ids 089-094, 120, 121, 123.

    {"kind": "bars", "subject": "Balaena mysticetus", "x": "date_start", "y": "count",
     "group_by": "vessel", "since": "1884", "until": "1888",
     "compare": {"subject": "Monodon monoceros", "since": "1884", "until": "1888"},
     "title": "What a Dundee whaler killed in her last seasons"}

Static plate now: `whales-and-narwhal-021`. The widget as specified compares two subjects;
a four-species version would need `group_by: "subject"`, which the vocabulary allows.

## 3. The record itself, by species and year

A strip of every dated observation, one lane per subject, ticks for catch records and dots for
sightings. Its purpose is honesty: the bowhead lane is dense because ships counted bowhead,
and the thinness of the narwhal and beluga lanes before 1870 is a fact about ships, not about
whales. Anyone reading a run of years in this topic as a trend should see this first.

    {"kind": "strip", "subject": "Cetacea", "x": "date_start", "group_by": "subject",
     "since": "1600", "until": "1930", "title": "Every cetacean record in the layer, by species"}

(`subject: "Cetacea"` here means the whole clade: the front end should resolve a subject to
itself and its descendants through `parent` when it is above species rank. If that is not
wanted, list the seven species instead.)

Static plate now: `whales-and-narwhal-022`.

## 4. Where the whales were, month by month

A seasonal cycle rather than a time series: Low's 1904 account of the bowhead's year on the
two grounds. There is no observation series behind it — it is a synthesis of statements — so
it is a diagram, not a widget, and it should stay one.

Static plate now: `whales-and-narwhal-023`.

## 5. The map layer

The most useful thing on the tab is probably not a chart at all but the observations on the
map with a date slider. 165 rows, all positioned, from 1616 to 1915, filterable by subject.
Watching the bowhead points move from Disko to Pond Inlet to Lancaster Sound as the slider
runs through a season, and watching the whole cloud thin out after 1840, is the topic.

    {"kind": "layer", "subject": "Cetacea", "since": "1616", "until": "1915",
     "group_by": "subject", "title": "Whales, narwhal and beluga, 1616-1915"}

A second layer worth having, filtered on method:

    {"kind": "layer", "subject": "Balaena mysticetus", "group_by": "place",
     "since": "1719", "until": "1915", "title": "The whaling grounds, by catch record"}

## 6. What is missing, for a later run

- **The full Ross series.** Only 30 of the 193 Davis Strait years and 14 of the Hudson Bay
  years are entered, being the firsts, peaks and failures. If the front end wants a smooth
  century-long curve rather than a stem plot, the remaining years are in Ross 1979 Tables 3
  and 4 and would need entering; the brief's rule on time series is why they are not.
- **Modern abundance as a series.** The 2013 High Arctic Cetacean Survey, the DFO aerial
  surveys and the NAMMCO assessments would give a handful of dated points that could sit on
  the same axis as the catch and make the recovery visible. None are entered yet.
- **No image of any of the three animals** is held. The whaling topic's plates show bone and
  boats, not whales. *(Answered in run 2: photographs, plates and objects of all three animals
  are now held, fetched from Wikimedia Commons and registered as artifacts from 500 up.)*

## 7. What Inuit and Inughuit knowledge looks like on a screen (added run 2)

52 of the topic's observations now carry `method: "testimony"`, and they are not points on a
chart. Most have no number in `count` at all: what they carry is a season, a place and a rule,
with the elder or the hunter in `observer`. Three ways to show them, in order of usefulness.

**7a. The seasonal round, as a strip.** The most quantitative thing in the testimony is the
month. Pond Inlet gives January to August for narwhal and beluga; Kimmirut gives March at the
floe edge and again the fall; Grise Fiord gives July; Cumberland Sound gives "once the ice
goes out of the head of the sound in July"; Aningat gives spring at the ice edge for the white
whale. Those are ranges, and `date_text` holds them as written. A strip with one lane per
community, ticks where the animal is said to be there, would put the twelve months of the
eastern Arctic on one page — and it would show at a glance that the narwhal season runs long
in the north and short in the south.

    {"kind": "strip", "subject": "Monodon monoceros", "x": "date_start", "group_by": "place",
     "since": "1900", "until": "1975",
     "compare": {"subject": "Delphinapterus leucas", "since": "1900", "until": "1975"},
     "title": "When the narwhal and the beluga are there, community by community"}

This one needs something the vocabulary does not yet have: the rows are recurring seasons, not
dated events, and `date_start` on a row written "1950/1975" is the start of a period of record,
not of a season. Until the front end can take a month range out of `qualifier` or `detail`, the
honest thing is a table, not a strip. Flagged for the operator rather than built badly.

**7b. The knowledge-holders, as a layer.** Every testimony row has a position and a named
observer. A map layer filtered on `method: "testimony"`, labelled by `observer`, would show
where the knowledge in this topic comes from — and would show honestly that it clusters at
Iglulik, Repulse Bay, Cumberland Sound, Pond Inlet and the Thule district, and that there is
nothing from Arctic Bay, Clyde River or Qikiqtarjuaq except through the community histories.

    {"kind": "layer", "subject": "Cetacea", "since": "1616", "until": "1975",
     "group_by": "observer", "title": "Who the whale knowledge in this topic comes from"}

**7c. The names, as a table beside the subject.** Every subject row now carries `inuktitut`,
`kalaallisut` and a semicolon list in `also` holding the dialect forms with their source in
brackets. The subject page should print them as a short table — dialect, spelling, source —
rather than as a sentence, and it should print the sentence in `note` that says when no name
is recorded. Six of this topic's subjects say exactly that, and it is a finding, not a gap:
the fin, humpback and bottlenose whales have Kalaallisut names and no Inuktitut ones, because
they reach the Canadian side late, in small numbers, and in deep water.

## 8. The status reports' own figures (added run 2)

Nineteen figures cropped out of the three COSEWIC PDFs by `tools/ocr.sh` are now artifacts
450-468. Two of them do work no widget in this topic can do:

- `whales-and-narwhal-458`, the Eastern Canada-West Greenland bowhead's seasonal round, is
  the modern counterpart of `whales-and-narwhal-023`, the same year as Low understood it in
  1904. Showing the two side by side is the single best argument this topic can make that the
  whalers' working knowledge was sound.
- `whales-and-narwhal-452`, the narwhal summer concentrations lettered A to F, should sit
  beside the Pond Inlet testimony row: the aerial survey and the community name the same water.

The seven beluga population maps (460, 462-468) are a set and should be shown as one strip of
small maps, not one at a time.

## 9. Still missing after run 2

- **The full Ross series** (see section 6) is still only the milestone years.
- **A seasonal-range kind.** Sections 4 and 7a both want the same thing the vocabulary lacks:
  a recurring annual cycle rather than a dated series. If a seventh `kind` is ever added, make
  it `cycle`: a value or a presence against month-of-year, with `group_by` for the lane.
