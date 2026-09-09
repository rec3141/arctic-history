#!/usr/bin/env python3
import json, sqlite3, sys
sys.path.insert(0, "/data/dev/arctic-history/karluk-cae-review-scratch")
from edit_artifacts import edit

c = sqlite3.connect("db/history/history.sqlite")
c.row_factory = sqlite3.Row


def wps(aid):
    return json.loads(c.execute("SELECT waypoints FROM artifacts WHERE id=?", (aid,)).fetchone()[0])


def setnote(w, date, **over):
    for p in w:
        if p["date"] == date:
            p.update(over)
            return w
    raise SystemExit(f"no waypoint {date}")


# ---- 001: Rodgers Harbour longitude brought into line with the island's own
w = wps("karluk-cae-001")
setnote(w, "1914-09-07", lat=70.98, lon=-178.5)
edit("karluk-cae-001", waypoints=json.dumps(w, ensure_ascii=False))

# ---- 002: the ten-mile estimate belongs to 23 June, not to the 22nd
w = wps("karluk-cae-002")
setnote(w, "1914-06-22", note="soundings down to about 50 metres; from a low hummock Stefansson sees "
        "'something dark and uniform in outline' beyond a pressure ridge, and his companions are "
        "not convinced; position inferred")
w.append({"date": "1914-06-23", "lat": 73.67, "lon": -125.3,
          "note": "the diary is certain: 'The land is no longer problematic. It is in plain sight in "
                  "the form of three hills'; the distance is 'not less than ten miles and may be a "
                  "good deal more'. Position inferred"})
w.sort(key=lambda p: p["date"])
edit("karluk-cae-002", waypoints=json.dumps(w, ensure_ascii=False))

# ---- 003: title and description without the discovery framing
edit("karluk-cae-003",
     title="Stefansson's 1915 ice journey: the new land north of Prince Patrick Island",
     description=(
         "Four men - Stefansson, Storkerson, Andreasen and Karl Thomsen - from Cape Kellett on Banks "
         "Island out into the polar sea, onto Prince Patrick Island, past McClintock's farthest of "
         "1853, and on 18 to 20 June 1915 to the first land added to the map of the Queen Elizabeth "
         "Islands since Sverdrup. No position was fixed at the sighting itself: the party could get "
         "no noon sight and 'could not wait longer'. The coordinates for 18-22 June are the modern "
         "positions of the places the narrative names, chiefly Cape Murray and Leffingwell Crags; "
         "those for 13-15 June are interpolated along the Prince Patrick Island coast. The farthest "
         "north and the Prince Patrick landing are Stefansson's own figures from his 16 June cairn "
         "record."))

# ---- 004: description without the discovery framing; waypoint note likewise
w = wps("karluk-cae-004")
setnote(w, "1916-05-15", note="back on the west coast of the land first mapped in 1915; position approximate")
edit("karluk-cae-004", waypoints=json.dumps(w, ensure_ascii=False), description=(
    "The Northern Party's longest journey: 229 days from the ship base at Cape Kellett, out along the "
    "north coast of Banks Island, across M'Clure Strait to Melville Island, north to Brock Island, "
    "over the polar ice to Cape Isachsen on Ellef Ringnes Island, then northeast to the sighting and "
    "first landing on Meighen Island on 12-15 June, south through Hassel Sound past King Christian "
    "Island to a summer camp on Lougheed Island, and back over Borden Island to Melville Island in "
    "October. Coordinates on Meighen, Hassel Sound and King Christian Island are Stefansson's own "
    "observed latitudes; longitudes were reckoned as meridian distance from Cape Isachsen and are "
    "approximate. The intermediate dates in April are inferred from the narrative."))

# ---- 005: the drift's real shape, from Storkerson's own longitudes
w = wps("karluk-cae-005")
setnote(w, "1918-06-15", lat=73.2, lon=-146.5,
        note="by midsummer 42 seals and 4 polar bears killed, about three tons of boneless meat, and "
             "the food brought from shore still untouched; the floe is drifting east before the wind. "
             "Position inferred")
w = [p for p in w if p["date"] != "1918-08-15"]
w += [
    {"date": "1918-07-13", "lat": 73.4, "lon": -144.5,
     "note": "the east end of the drift: three months of easterly drift from 14 April brought the floe "
             "to longitude 144 and a half west. Storkerson's own longitude; latitude inferred"},
    {"date": "1918-08-25", "lat": 73.8, "lon": -151.0,
     "note": "the wind changed on 14 July and in about six weeks carried the floe northwest to the "
             "151st meridian, straight through the water where Keenan Land was drawn on the map of "
             "1912; the sounding line found no bottom at 1,600 fathoms. Storkerson's own longitude; "
             "latitude inferred"},
    {"date": "1918-09-08", "lat": 74.0, "lon": -150.0,
     "note": "farthest north, latitude 74; longitude inferred"},
]
setnote(w, "1918-10-09", note="after 184 days adrift, counted from 8 April, the party starts for shore "
        "from latitude 73.9 north, a little over 200 miles out, with 55 days' rations left of the 101 "
        "they began with")
w.sort(key=lambda p: p["date"])
edit("karluk-cae-005", waypoints=json.dumps(w, ensure_ascii=False), description=(
    "The last journey of the Canadian Arctic Expedition. Five men - Storkerson, August Masik, "
    "Adelbert Gumaer, E. Lorne Knight and Martin Kilian - went out from Cross Island in Alaska with "
    "101 days' rations, camped on a floe at 73 degrees north, and stayed on it for six months living "
    "on seals and bears, taking soundings and meteorological records, to test whether there was a "
    "permanent current in the Beaufort Sea and whether Keenan Land existed. There was not, and it did "
    "not: the floe went east until 13 July, northwest until the end of August, then northeast to a "
    "farthest north of latitude 74 on 8 September, following the wind each time. The April positions "
    "and the three summer longitudes are Storkerson's own; the summer latitudes are inferred. His "
    "narrative as printed gives the return as 5 November 1919, which must be a misprint for 1918: he "
    "started on 15 March 1918 and counted 238 days on the ice, which ends on 8 November 1918."))

# ---- 006: Cape North is west of the 180th meridian, not east
w = wps("karluk-cae-006")
setnote(w, "1914-03-20", lon=-178.5)
setnote(w, "1914-04-08", lon=-179.37,
        note="reach Cape North, the Chukchi Irkaipij and the modern Cape Schmidt, travelling east "
             "along the Chukchi shore from village to village; the cape lies just west of the 180th "
             "meridian, and Bartlett reckoned afterwards that they had landed about sixty miles west "
             "of it")
edit("karluk-cae-006", waypoints=json.dumps(w, ensure_ascii=False),
     tags=["karluk", "siberia", "east-verified"], description=(
    "Two men and seven dogs from Wrangel Island across the moving ice of the Chukchi Sea to the "
    "Siberian coast, then some four hundred miles east along the shore of the Chukchi Peninsula to "
    "East Cape and Emma Harbour, and across to Alaska by ship. The track crosses the 180th meridian "
    "twice: the landfall near Cape Yakan is in east longitude, given here as positive, and Cape North "
    "- the Chukchi Irkaipij, the modern Cape Schmidt - is a degree and a half back to the west of it. "
    "Coordinates are the modern positions of the named places; the book gives none."))
