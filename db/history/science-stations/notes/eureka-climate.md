# The Eureka climate record: figures pulled from ECCC, run 2, 2026-09-08

Source: Environment and Climate Change Canada historical climate data, through the
open GeoMet-OGC API at `https://api.weather.gc.ca` (collections `climate-stations`,
`climate-daily`, `climate-normals`). Retrieved 8 September 2026. Licence: Open
Government Licence - Canada.

## The stations called Eureka

| STN_ID | climate id | name | first | last | normals |
| --- | --- | --- | --- | --- | --- |
| 1750 | 2401200 | EUREKA A | 1947-01-01 | 2016-02-25 | Y (1981-2010) |
| 50737 | 2401199 | EUREKA CLIMATE | 2013-12-10 | current | N |
| 53598 | 2401203 | EUREKA A | 2016-02-22 | current | N |
| 53599 | 2401208 | EUREKA A | 2016-02-25 | current | N |

The station identifier changed in 2016, so no single ECCC series runs the whole way.
Everything below marked *derived* was computed here from station 1750 unless said
otherwise, and is not an ECCC published figure.

Earliest daily row in the archive for station 1750: **1 May 1947**. The station was
founded on 7 April 1947, so the first three weeks are not in the digital archive.
28,986 daily rows for station 1750, 1947 to 2016.

## Extremes (highest MAX_TEMPERATURE / lowest MIN_TEMPERATURE per station)

| | value | date | station |
| --- | --- | --- | --- |
| highest daily maximum | **21.4 °C** | 27 June 2020 | 53599 EUREKA A |
| (previous) | 20.9 °C | 14 July 2009 | 1750 EUREKA A |
| | 20.7 °C | 23 July 2007 | 1750 |
| | 20.6 °C | 30 June 2019 | 53599 |
| lowest daily minimum | **−55.3 °C** | 15 February 1979 | 1750 |
| (equalled) | −55.3 °C | 18 February 1987 | 1750 |
| | −54.3 °C | 14 February 1979 | 1750 |
| lowest since 2016 | −50.7 °C | 9 March 2017 | 50737 EUREKA CLIMATE |

## Normals 1981-2010, station 1750 (published by ECCC)

- annual mean daily temperature **−18.75 °C** (mean of the twelve monthly normals)
- January mean −36.5 °C; July mean +6.1 °C
- total annual precipitation **79.1 mm**; total annual snowfall 60.3 cm
- (79 mm a year is a polar desert; the driest place in Canada with a long record)

## Derived: annual mean temperature by decade, station 1750

Computed here. A month counts only with at least 25 valid daily means; a year counts
only with all twelve months. 66 complete years between 1948 and 2015.

| decade | mean annual temperature (°C) | complete years |
| --- | --- | --- |
| 1940s | −19.78 | 2 |
| 1950s | −19.22 | 9 |
| 1960s | −19.32 | 10 |
| 1970s | −20.49 | 10 |
| 1980s | −19.85 | 10 |
| 1990s | −18.84 | 9 |
| 2000s | −17.97 | 10 |
| 2010-2015 | −17.86 | 6 |

Warmest years: 2010 (−15.88), 2006 (−16.69), 1998 (−16.93), 2005 (−17.23),
2011 (−17.30), 2012 (−17.48).
Coldest years: 1972 (−21.78), 1979 (−21.49), 1974 (−21.26), 1984 (−21.24),
1987 (−21.17), 1986 (−20.83).

Read plainly: the 1970s were the coldest decade in the record and the 2000s the
warmest, about 2.5 °C apart, and the single warmest year, 2010, is nearly 6 °C
above the single coldest, 1972. This is one station's raw archive with no
homogenisation for instrument or site changes, so it is an indication and not a
trend estimate.

## Not obtained

- ECCC's own published record-extreme tables (climate.weather.gc.ca normals pages)
  returned an empty body from this host; the extremes above are the maxima and
  minima of the daily archive, which should agree but were not cross-checked.
- No series spanning 1947-2026 as one homogeneous record.
