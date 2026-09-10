# Display note: the weather and the climate

For the operator and the front end. What each series in this topic should look
like on the tab, which fields of `observations.json` drive it, and which of the
static plates stands in for it until the widget exists.

The observation rows here carry two unit systems on purpose. Everything before
1947 is written as the observer wrote it — Fahrenheit, inches of mercury,
Beaufort force, miles an hour — and everything from the weather stations is
Celsius, hectopascals and km/h. Nothing is converted in the row. So **every
widget that plots temperature must convert at render time from
`observations.unit`, not assume a unit from the subject.** The subject's `unit`
field (`C` for air temperature, `hPa` for pressure) is the unit the page should
convert *to*; a plate should carry the original on one axis and the converted
on the other, as the static figures do.

## 1. The trend, station by station — the most valuable widget on the tab

The one a scientist aboard will actually use: the ship's underway air
temperature against the nearest station's record.

```json
{"kind": "series", "subject": "air temperature", "place": "Eureka", "x": "date_start", "y": "value",
 "unit": "C", "display_unit": "F", "since": "1948", "until": "2026",
 "compare": {"subject": "air temperature", "place": "Alert", "since": "1948", "until": "2026"},
 "title": "Annual mean temperature at Eureka and Alert since the stations opened"}
```

Only the thirty-year means, the trends and the record years are in the database
as observations — the daily series is not, and should not be. The widget draws
the rows it has; the full daily record lives at Environment and Climate Change
Canada and the sources `eccc2026climate`, `eccc2026alert`, `eccc2026resolute`,
`eccc2026isachsen` and `eccc2026mouldbay` give the station numbers and the API.

**Standing in for it now:** `the-weather-and-the-climate-011`, which draws all
three stations' annual means with ten-year running means, built outside the
database from the ECCC daily record.

## 2. Every wintering's coldest reading — a strip, not a series

Sixteen readings two hundred years apart is not a time series; it is a set of
dated marks whose interest is the gap between them and the instrument behind
each one.

```json
{"kind": "strip", "subject": "air temperature", "x": "date_start", "group_by": "place",
 "unit": "F", "display_unit": "C", "since": "1819", "until": "2026",
 "title": "The coldest reading of every wintering and station"}
```

Colour the mark by `unit`: an F row was read on a ship's or a post's spirit
thermometer, a C row on a station instrument. `confidence` should be visible —
Nares's -73.75 F and Kane's -66.4 F are `probable`, not `certain`, and the tab
should say so rather than let the reader take them as facts.

**Standing in for it now:** `the-weather-and-the-climate-010`.

## 3. Station extremes — bars, one row per station

```json
{"kind": "bars", "subject": "air temperature", "group_by": "place",
 "unit": "C", "display_unit": "F", "since": "1947", "until": "2026",
 "title": "From each station's coldest reading to its warmest"}
```

The rows to draw are those tagged `station-record` with `qualifier` beginning
"the lowest" or "the highest". A reader comparing the ship's own reading wants
the thirty-year mean on the same axis: those are the rows tagged
`thirty-year-mean`, two per station.

**Standing in for it now:** `the-weather-and-the-climate-012`.

## 4. Wind — bars by station, and a caution

```json
{"kind": "bars", "subject": "wind", "group_by": "place",
 "unit": "km/h", "display_unit": "km/h", "since": "1947", "until": "2026",
 "title": "The strongest gust recorded at each weather station"}
```

Do not put the historical wind rows on the same axis. Greely's anemometer read
miles an hour, Sverdrup's read feet per second, Parry and Nares recorded force
on Beaufort's scale and no speed at all, and Jackson's Lake Hazen figures are
counts of observations rather than speeds. Those belong in the subject page's
record list, not in a bar chart with the station gusts.

## 5. Fog, blizzard and cloud — a map layer, not a chart

These subjects carry frequencies over a region rather than readings at a point,
so the honest display is a layer with the value in the label.

```json
{"kind": "layer", "subject": "fog", "since": "1819", "until": "2026",
 "unit": "days per year", "display_unit": "days per year",
 "title": "Fog: where it is recorded and how often"}
```

The same for `blizzard` and `cloud`. Everything from Dunbar and Greenaway 1956
is a regional figure pinned at a representative position; the tab should show
the `detail` sentence rather than the number alone, because the number without
its region is meaningless.

## 6. The inversion — a diagram, and it should stay a diagram

There is no series here worth plotting: the evidence is Nares's two readings of
4 March 1876, Jackson's counts of days and calms, and Dunbar's prediction from
the air. `the-weather-and-the-climate-013` carries all of it, and a widget would
not improve on it. Link it from the subject page for
`temperature inversion` and from `air temperature`.

## 7. Fort Conger's year against a modern normal — the second-most useful widget

Added in the second run: the topic now holds mean monthly air temperature for
four complete high-Arctic years at two stations a hundred kilometres apart —
Discovery Bay 1875-76 (the British Arctic Expedition), Fort Conger 1881-82 and
1882-83 (Greely), Floeberg Beach 1875-76 (Nares's Alert), Greely's three-year
mean for the Fort Conger site, and the 1991-2020 monthly normals at Alert
computed from the ECCC homogenized record. That is enough for a real seasonal
march, and the seasonal march is what a scientist aboard in any given month
actually wants.

```json
{"kind": "series", "subject": "air temperature", "place": "Fort Conger", "x": "date_start", "y": "value",
 "unit": "F", "display_unit": "C", "since": "1881-08", "until": "1883-08",
 "compare": {"subject": "air temperature", "place": "CFS Alert", "since": "1991", "until": "2020"},
 "title": "Greely's two winters against the Alert normals"}
```

The rows are those with `qualifier` "the monthly mean of the hourly register"
(48 rows, four station-years) and "the mean for <month> over three years of
observation at the same spot" (12 rows). The comparison rows are the twelve
tagged `normal` at CFS Alert, which are in Celsius: this is the widget that
proves the conversion rule matters, because one side of it is Fahrenheit and the
other is not. Plot the months in the polar order, August round to July, not
January to December: a wintering runs from one summer to the next and cutting it
at New Year splits every winter in half.

**Standing in for it now:** `the-weather-and-the-climate-014`, and beside it
`the-weather-and-the-climate-015`, which sets the same station's mean monthly
cloudiness against its mean monthly temperature. That pairing is worth a widget
of its own wherever a place has both series, because it is the mechanism behind
every extreme minimum in the topic:

```json
{"kind": "series", "subject": "cloud", "place": "Fort Conger", "x": "date_start", "y": "value",
 "unit": "fraction of sky", "display_unit": "per cent", "since": "1881-08", "until": "1883-08",
 "compare": {"subject": "air temperature", "place": "Fort Conger", "since": "1881-08", "until": "1883-08"},
 "title": "Cloud and cold at Fort Conger"}
```

## 8. Inuit and Inughuit knowledge — a layer of dated statements, never a chart

The topic holds 28 rows with `method` of `testimony`: Qaqortingneq on sila and
pErsoq, the Netsilingmiut on Narssuk, Hans Hendrik on his first dark winter, the
1953 relocatees on the cold and the dark of the High Arctic, and fifteen from
the 2004-05 Unikkaaqatigiit workshops in Arctic Bay, Kugaaruk and Repulse Bay.
Only one of them carries a number.

```json
{"kind": "layer", "subject": "sila", "since": "1819", "until": "2026",
 "unit": "", "display_unit": "",
 "title": "What Inuit and Inughuit have recorded of the weather, by place"}
```

Rules for this layer, which matter more than the geometry:

- the label is `observer` and then `detail`, never the number; where `observer`
  is a community workshop rather than a person, the participants are named in
  `detail` and in the source's rights note, and the tab should show them;
- do not merge these rows into the temperature series. A testimony row and a
  thermometer row are different kinds of statement about the same world and a
  reader who sees them on one axis will read the first as a worse version of the
  second;
- the one testimony row that carries a value is the Repulse Bay thermometer that
  must be taken indoors below -37 degrees, brought in twice in 2004 against many
  times in earlier years. It belongs beside the trend, not in it: it is a
  frequency, not a temperature.

Link the page `the-weather-inuit-knowledge` from every weather subject that
carries an Inuktitut name, and link `[[topic:inuit-knowledge-of-nature]]` from
the tab, because the named winds, the thirteen moons and the sky live there.

## What a scientist aboard would compare things with

- an underway air temperature, against the nearest station's 1981-2010 normal
  (Eureka -18.75 C, Resolute -15.67 C) rather than against its extremes;
- an underway pressure, against the historical rows only as a curiosity — the
  old barometer rows are in inches and their interest is the storm they
  preceded, which is in the `detail`, not the number;
- a gale on deck, against the station gust records: 158 km/h at Resolute is the
  regional ceiling and almost nothing reaches it;
- summer precipitation, against Eureka's 79 mm a year, which is the fact most
  people aboard will not believe.

## Two things the front end should not do

1. Do not average across a subject's observations. The rows mix single readings,
   daily means, monthly means, thirty-year means and linear trends, all in the
   `value` column, distinguished only by `qualifier` and by the shape of
   `date_text`. A mean of them is nonsense.
2. Do not silently convert Fahrenheit to Celsius in a label. The layer's rule is
   that the number is as written; show it as written and put the conversion
   beside it.
