# How the freshwater record should be shown

A note for the operator and the front end. Not a wiki page.

The freshwater half of this layer is small in row count and wide in span: a hundred and thirty observations across 1821 to 2010, in feet, inches, fathoms, centimetres, metres, Fahrenheit and Celsius. Almost nothing here is a dense time series; nearly everything is a scattered set of single readings that only becomes a series when it is put beside its neighbours. That shapes what is worth drawing.

Four static plates are already in and registered as artifacts. Where a widget would beat one, the spec is given below.

## 1. Ice thickness on fresh water — the flagship

The record's spine. Fifteen measurements from 1823 to 1987, every one of them a hole somebody cut. It works as a plate because the labels carry the story (`a deep lake`, `the aufeis on the flood plain`, `the pan that survived the summer`), and it works better still as a widget, because a reader aboard wants to filter it by subject and see the ship's own latitude band.

Fields: `subject` in (`lake ice`, `river ice`, `aufeis`), `value`, `unit`, `date_start`, `place`, `observer`. The unit is mixed and must be converted for the axis and printed as written in the label. Conversions: feet 0.3048, inches 0.0254, cm 0.01.

Compare with: nothing in the modern record is directly comparable, which is itself worth saying. The Canadian Ice Service charts the sea, not the lakes. If the ship carries a lake-ice figure from anywhere, put it beside these.

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-009]].

    {"kind": "bars", "subject": "lake ice", "group_by": "place", "y": "value",
     "unit": "m", "display_unit": "ft", "since": "1820", "until": "2026",
     "title": "Every measured thickness of Arctic lake and river ice"}

## 2. Tuborg Lake, temperature and salinity against depth

A profile in the strict sense and the best single plate in the topic: two variables against one depth axis, from one cast, 2 and 3 June 1963. It needs no interaction. Leave it as a static plate.

Fields: `depth`, `value`, `unit`, `subject` (`lake water temperature` and `salinity`), `place` = `Tuborg Lake`.

A scientist aboard would compare it with a CTD cast in any fiord of the Greely Fiord system: the same shape, but continuous, and with the halocline where the mixing is rather than where a glacier put it.

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-010]].

    {"kind": "profile", "subject": "lake water temperature", "place": "Tuborg Lake",
     "x": "value", "y": "depth", "unit": "C", "display_unit": "C",
     "since": "1963-06-02", "until": "1963-06-03",
     "compare": {"subject": "salinity", "place": "Tuborg Lake", "since": "1963-06-02", "until": "1963-06-03"},
     "title": "Tuborg Lake through 2.7 m of ice, June 1963"}

## 3. Fresh-water temperature, ranked

Ten readings, four of them Greely's in Fahrenheit. Ranked coldest first rather than plotted against time, because there is no trend in ten scattered points and pretending otherwise would be a lie. What the plate shows is range, and the range is the finding: 32.6 F where the Ruggles leaves Lake Hazen against 15.7 C in a pond four kilometres away.

Fields: `subject` = `lake water temperature`, `value`, `unit`, `place`, `observer`, `date_start`. Convert F to C for the axis; print the original.

Compare with: the ship's own surface sea temperature. Fresh water in July in a shallow Arctic pond is warmer than the sea anywhere the Amundsen will be, and that surprises people.

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-011]].

## 4. Lake Hazen in section

A conceptual diagram, not a data plate. It exists because no photograph and no plate in the sources shows how the lake works: the silt-laden underflow, the winter drawdown, the outflow that never freezes, the char over the deep water. Keep it static; there is nothing to filter.

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-012]].

## 5. Break-up and freeze-up as a strip — worth building, not yet drawn

The single most useful freshwater widget for a scientist aboard, and the one this run could not draw well because the record is thin: seven or eight dated statements about whether a lake cleared its ice in a given summer. The value is not in the seven; it is in what happens when the ship's own seasons and the Canadian Ice Service record are laid alongside. Build the widget and it fills itself over the years.

Fields: `subject` in (`lake-ice break-up`, `lake-ice freeze-up`), `date_start`, `place`, `qualifier` — the qualifier carries the state (`completely ice-free`, `about three tenths ice cover`, `the lake did not clear`) and must be shown as the strip's category, because the fact here is categorical, not numeric.

    {"kind": "strip", "subject": "lake-ice break-up", "place": "Lake Hazen",
     "x": "date_start", "group_by": "qualifier", "since": "1880", "until": "2026",
     "compare": {"subject": "lake-ice break-up", "place": "Colour Lake", "since": "1959", "until": "2026"},
     "title": "The summers the lakes cleared, and the summers they did not"}

## 6. The Ruggles River's year — a series the layer does not hold

The Water Survey of Canada has gauged the Ruggles River since August 1997 at station 10VK001, and the whole daily and monthly series lives with them, not here; it is reachable without a login through the GeoMet API at api.weather.gc.ca (collections `hydrometric-monthly-mean` and `hydrometric-daily-mean`, `STATION_NUMBER=10VK001`). The layer now holds the station as a `dataset` source and eight milestone observations from it: the opening of the gauge, the five largest months, and the two smallest. That is the right division: do not import the series.

One thing whoever draws this must not do. The discharge record is broken — the gauge reported in 1997, 2009-2012, 2017-2019 and 2022-2024 and nothing in between — so a line joining the monthly means draws a decade-long rising ramp through a gap where there is simply no data, and reads as a trend that was never measured. Break the line at every gap, or draw bars per year with the missing years labelled. [[artifact:freshwater-rivers-and-lakes-397]] does the latter and stands in for this now.

What the front end should do is show the two numbers as the ends of a bar and link out. If the ship ever carries the gauge data, the spec is:

    {"kind": "series", "subject": "river discharge", "place": "Ruggles River",
     "x": "date_start", "y": "value", "unit": "m3/s", "display_unit": "m3/s",
     "since": "1996", "until": "2026",
     "title": "The Ruggles River, the one outflow of Lake Hazen"}

## 7. The freshwater layer on the map

Every observation in this topic has a position, and about a third of them are in one basin. A map layer filtered by domain is the right way in for a reader who does not know the topic exists.

    {"kind": "layer", "subject": "", "place": "", "since": "1820", "until": "2026",
     "group_by": "subject", "title": "Fresh water: every lake, river and pond in the record"}

Two cautions for whoever implements it. First, several positions in the Greely material are approximate and say so in the detail; the map must not imply a fix it does not have. Second, `Lake Hazen` as a `place` is a single point for a lake 78 km long, so an observation attached to the place row lands in the middle of the water rather than where it was made. Where a row's own `lat`/`lon` are set, prefer them.

## What a reader aboard should be able to ask

- How thick is the ice on a lake here, and how does that compare with the sea ice we are in?
- Did Lake Hazen clear this year? Has it cleared before?
- Is there a lake anywhere near us with sea water at the bottom of it?
- How warm does fresh water get up here, and is it warmer than the sea?
- What is in the char, and who has been measuring it?

---

## Added after the second research run

The rows behind these are now in the database; the specs below are what the front end should build from them.

### 8. Water on its way from the ice to the lake — a profile along a path, not a depth

The one plate that explains the ecology of Lake Hazen in a glance. Six stages: the glacier snouts, the ice-fed Abbe, the rivers off bare ground (Very, Turnabout), the deltas, the open lake, the Ruggles leaving it. `subject` in (`river water temperature`, `lake water temperature`), `value`, `unit` C, `qualifier` carrying which stage the row is. This is a `profile` in the vocabulary — value along a line rather than against depth — and the line here is the path the water takes, which the six `place` values give in order.

    {"kind": "profile", "subject": "river water temperature", "place": "",
     "x": "place", "y": "value", "unit": "C", "display_unit": "C",
     "since": "1997", "until": "2026",
     "compare": {"subject": "lake water temperature", "place": "Lake Hazen", "since": "2015", "until": "2016"},
     "title": "Water warms on its way from the ice to the lake, and cools again in it"}

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-390]]. What a scientist aboard would compare it with: the ship's own surface temperature in Nares Strait and the temperature of any glacier-fed fiord being worked.

### 9. The Ruggles River and the residence time — bars against a line

    {"kind": "bars", "subject": "river discharge", "place": "Ruggles River",
     "x": "date_start", "y": "value", "unit": "km3/yr", "display_unit": "km3/yr",
     "group_by": "qualifier", "since": "1996", "until": "2026",
     "compare": {"subject": "water residence time", "place": "Lake Hazen", "since": "1949", "until": "2026"},
     "title": "A lake being flushed three and a half times faster than it was"}

Standing in for it now: [[artifact:freshwater-rivers-and-lakes-391]]. The two series carry different units (cubic kilometres a year, and years), so the `compare` must go to a second axis. If the front end cannot do that, draw the discharge bars alone and put the residence time in the title.

### 10. The lake's ice by decade — bars, and the strip's numeric companion

Section 5 above wants a strip of dated break-up statements. There is now also a numeric series worth showing as bars: the percentage of years in each period in which Lake Hazen went ice-free for a month or more (60 per cent 1985-1995, 80 per cent 1996-2005, 88 per cent 2006-2012), with the trends in break-up (0.9 d/yr earlier) and freeze-up (0.3 d/yr later) as annotations.

    {"kind": "bars", "subject": "lake ice", "place": "Lake Hazen",
     "x": "date_start", "y": "value", "unit": "percent of years", "display_unit": "percent of years",
     "since": "1985", "until": "2012",
     "title": "The years Lake Hazen lost its ice for a month or more"}

Filter on `qualifier` containing "ice-free for a month or more": the `lake ice` subject also carries the ice-free-area rows in km2/yr, which must not be mixed into the same bars.

### 11. The tagged char — a track that is really sixteen pairs of points

Sixteen fish tagged in May 1995 or 1996 at a named place on Lake Hazen and relocated weeks or years later at another, with the distance in kilometres. It is the single most legible piece of evidence in the topic that this stock does not go to sea, and it wants a map, not a chart: sixteen short lines inside one lake, and two silent listening stations on the outflow.

The rows carry `place` "Lake Hazen" rather than per-creek positions, because the paper names the creeks but does not print their coordinates; the creek is in `detail` and in `qualifier`. Whoever builds this should first give Mesa Creek, Traverse Creek, Cuesta Creek and Johns Island `place` rows with positions from the topographic sheet, then re-point the rows. Until then a `bars` of distance moved per fish is honest and a map is not.

    {"kind": "bars", "subject": "Salvelinus alpinus", "place": "Lake Hazen",
     "x": "qualifier", "y": "value", "unit": "km", "display_unit": "km",
     "since": "1995", "until": "2000",
     "title": "How far the tagged char of Lake Hazen moved, and that none of them left"}

### 12. The ponds against the lake — bars by group

Eight ponds and Skeleton Lake against the Lake Hazen shore, on three variables that all say the same thing in different units: `lake water temperature` (C), `total dissolved solids` (mg/L), `chlorophyll a` (ug/L). Three small bar plates side by side, grouped by water body, would carry the argument of [[page:the-ponds-of-the-hazen-oasis]] better than any prose.

    {"kind": "bars", "subject": "total dissolved solids", "place": "",
     "x": "place", "y": "value", "unit": "mg/L", "display_unit": "mg/L",
     "group_by": "qualifier", "since": "2005", "until": "2012",
     "compare": {"subject": "total dissolved solids", "place": "Lake Hazen", "since": "2005", "until": "2012"},
     "title": "The ponds behind the shore carry twenty times what the lake carries"}

The pond rows carry their own `lat`/`lon` and no `place` row, on purpose: Pond 01 and the rest are research site codes, not names on the land, and should not enter the gazetteer.
