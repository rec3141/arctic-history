#!/usr/bin/env python3
"""Route the History tab's voyage tracks through water.

A track artifact's geometry is its waypoints joined by straight lines, and
those lines cut across islands. This routes each pair of consecutive waypoints
along the least-cost water path over a land mask, and writes the result next
to the straight line so the two can be compared.

    route_tracks.py --db db/history/history.sqlite --land land.gpkg [--land more.shp]
                    [--bbox -180,35,15,86] [--res 1000] [--gebco gebco.tif]
                    [--coarse-land GSHHS_i_L1.shp --coarse-bbox -180,-60,180,86 --coarse-res 4000]
                    [--ids id,id,...] [--out routing-out] [--geojson-dir DIR]

Two masks: a fine one (--land, --bbox, --res) over the region the voyages
worked in, and an optional coarse one (--coarse-*) for the ocean crossings
outside it. A segment is routed on the fine mask when both its ends are in
it, else on the coarse one, else left as a great circle. Land vectors are any
OGR source in any projection; they are reprojected to Web Mercator once and
rasterized (cached in --out). GEBCO is optional and only adds a small cost to
water shallower than 50 m on the fine mask.

Needs the GDAL command-line tools (ogr2ogr, gdal_rasterize, gdal_translate,
gdalwarp) and numpy, scipy, scikit-image and Pillow.

The cost of a water cell is 1, plus a penalty that fades over ~15 km from any
coast so a line stays offshore, plus 0.5 in shallow water; a land cell costs
500, so a route crosses land only to reach a waypoint that sits on it. Each
waypoint is first snapped to the nearest water cell within 20 km (harbours and
coastal camps fall in a land cell). On open water a grid's least-cost path is
a staircase of 45 and 90 degree moves that ties with the straight line, so
each segment is then pulled straight wherever a straight line touches no land
cell — within the segment only, so every waypoint stays on the line — and the
whole is simplified to 1 km. Tracks whose tags or title say sledge, overland,
drift, retreat, walk, march or ice journey are skipped: those went over ice or
land and must not be routed.

Outputs, in --out: routes.json ({id: {title, waypoints, straight, routed,
straight_land_frac, routed_land_frac, points, seconds}}), overview.png (the
fine mask with every routed track), archipelago.png (the Northwest Passage
region), summary.md (a table of the per-track land fractions) and, with
--geojson-dir, one GeoJSON LineString per routed track for history-db.py.
"""
import argparse, json, math, os, sqlite3, subprocess, sys, time
import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array
from PIL import Image, ImageDraw

M = 20037508.342789244; R = 6378137.0
SKIP_WORDS = ("sledge", "sledging", "overland", "drift", "ice-island", "ice journey", "retreat", "ski", "ride to", "across", "walk", "march")


def merc(lat, lon):
    return lon / 180 * M, R * math.log(math.tan(math.pi / 4 + math.radians(max(-85, min(85, lat))) / 2))


def unmerc(x, y):
    return math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2), x / M * 180


def great_circle(a, b, step_km=50.0):
    """Points along the great circle from a to b, (lat, lon), every step_km."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
    n = max(1, int(d * 6371 / step_km))
    out = []
    for i in range(n + 1):
        f = i / n
        if d == 0:
            out.append(a); continue
        A = math.sin((1 - f) * d) / math.sin(d); B = math.sin(f * d) / math.sin(d)
        x = A * math.cos(la1) * math.cos(lo1) + B * math.cos(la2) * math.cos(lo2)
        y = A * math.cos(la1) * math.sin(lo1) + B * math.cos(la2) * math.sin(lo2)
        z = A * math.sin(la1) + B * math.sin(la2)
        out.append((math.degrees(math.atan2(z, math.hypot(x, y))), math.degrees(math.atan2(y, x))))
    return out


class Grid:
    """A land mask on a Web Mercator grid, its cost field, and the
    conversions between (lat, lon) and (row, col)."""

    def __init__(self, out, name, lands, bbox, res, gebco=None):
        self.res = res; self.km = res / 1000.0
        x0, y0 = merc(bbox[1], bbox[0]); x1, y1 = merc(bbox[3], bbox[2])
        ncols = int(round((x1 - x0) / res)); nrows = int(round((y1 - y0) / res))
        x1 = x0 + ncols * res; y1 = y0 + nrows * res
        te = ["-te", f"{x0:.1f}", f"{y0:.1f}", f"{x1:.1f}", f"{y1:.1f}", "-tr", str(res), str(res)]
        self.x0, self.y1 = x0, y1
        gpkg = os.path.join(out, f"{name}-land3857.gpkg")
        if not os.path.exists(gpkg):
            # the clip is given in the destination's metres: the sources may be in any projection
            for i, src in enumerate(lands):
                subprocess.run(["ogr2ogr", "-q", "-t_srs", "EPSG:3857", "-nlt", "PROMOTE_TO_MULTI", "-clipdst", f"{x0:.1f}", f"{y0:.1f}", f"{x1:.1f}", f"{y1:.1f}"]
                               + (["-update"] if i else []) + [gpkg, src, "-nln", f"land{i}"], check=True)
        tif = os.path.join(out, f"{name}-land.tif")
        if not os.path.exists(tif):
            for i in range(len(lands)):
                subprocess.run(["gdal_rasterize", "-q", "-burn", "1", "-l", f"land{i}"] + ([] if i else te + ["-ot", "Byte", "-a_srs", "EPSG:3857", "-co", "COMPRESS=DEFLATE"]) + [gpkg, tif], check=True)
        raw = os.path.join(out, f"{name}-land.bin")
        if not os.path.exists(raw):
            subprocess.run(["gdal_translate", "-q", "-of", "ENVI", tif, raw], check=True)
        self.land = np.fromfile(raw, dtype=np.uint8).reshape(nrows, ncols).astype(bool)
        if not self.land.any():
            sys.exit(f"{name}: the land mask is empty; the land vectors did not rasterize into {bbox}")
        elev = None
        if gebco:
            ebin = os.path.join(out, f"{name}-elev.bin")
            if not os.path.exists(ebin):
                subprocess.run(["gdalwarp", "-q", "-t_srs", "EPSG:3857"] + te + ["-r", "bilinear", "-ot", "Int16", "-of", "ENVI", "-multi", gebco, ebin], check=True)
            elev = np.fromfile(ebin, dtype=np.int16).reshape(nrows, ncols)
        dist = ndimage.distance_transform_edt(~self.land) * self.km
        self.cost = (1.0 + 3.0 * np.exp(-dist / 15.0)).astype(np.float32)
        if elev is not None:
            self.cost += np.where(elev > -50, 0.5, 0.0).astype(np.float32)
        self.cost[self.land] = 500.0
        del dist
        _, self.nearest_water = ndimage.distance_transform_edt(self.land, return_indices=True)
        print(f"{name}: {ncols}x{nrows} at {res:.0f} m, land fraction {self.land.mean():.2f}", file=sys.stderr)

    def rc(self, lat, lon):
        x, y = merc(lat, lon)
        return int((self.y1 - y) / self.res), int((x - self.x0) / self.res)

    def ll(self, r, c):
        return unmerc(self.x0 + (c + 0.5) * self.res, self.y1 - (r + 0.5) * self.res)

    def inside(self, r, c):
        return 0 <= r < self.land.shape[0] and 0 <= c < self.land.shape[1]

    def snap(self, r, c):
        """The nearest water cell within 20 km, for a waypoint on land."""
        nr, nc = int(self.nearest_water[0][r, c]), int(self.nearest_water[1][r, c])
        return (nr, nc) if math.hypot(nr - r, nc - c) * self.km <= 20 else (r, c)

    def clear(self, a, b):
        """True when the straight line between two (lat, lon) points touches no land cell."""
        (r0, c0), (r1, c1) = self.rc(*a), self.rc(*b)
        n = int(max(abs(r1 - r0), abs(c1 - c0))) + 1
        for f in np.linspace(0, 1, n + 1):
            r, c = int(round(r0 + f * (r1 - r0))), int(round(c0 + f * (c1 - c0)))
            if self.inside(r, c) and self.land[r, c]:
                return False
        return True

    def land_along(self, pts):
        """(land cells, cells) sampled every cell along a polyline."""
        h = n = 0
        for a, b in zip(pts, pts[1:]):
            (r0, c0), (r1, c1) = self.rc(*a), self.rc(*b)
            for f in np.linspace(0, 1, int(max(abs(r1 - r0), abs(c1 - c0))) + 2):
                r, c = int(round(r0 + f * (r1 - r0))), int(round(c0 + f * (c1 - c0)))
                if self.inside(r, c): n += 1; h += int(self.land[r, c])
        return h, n

    def route(self, p, q):
        """The water path from p to q, (lat, lon) points, p and q included."""
        (r0, c0), (r1, c1) = self.snap(*self.rc(*p)), self.snap(*self.rc(*q))
        seg_km = self.km * math.hypot(r1 - r0, c1 - c0)
        m = int(max(400, 0.6 * seg_km) / self.km)
        ra, rb = max(0, min(r0, r1) - m), min(self.land.shape[0], max(r0, r1) + m + 1)
        ca, cb = max(0, min(c0, c1) - m), min(self.land.shape[1], max(c0, c1) + m + 1)
        idx, _ = route_through_array(self.cost[ra:rb, ca:cb], (r0 - ra, c0 - ca), (r1 - ra, c1 - ca), fully_connected=True, geometric=True)
        return self.line_of_sight([p] + [self.ll(r + ra, c + ca) for r, c in idx] + [q])

    def line_of_sight(self, pts):
        """Pull the route straight wherever it can be: from each kept point,
        jump to the farthest later point whose straight line touches no land."""
        out = [pts[0]]; i = 0
        while i < len(pts) - 1:
            j = len(pts) - 1
            while j > i + 1 and not self.clear(pts[i], pts[j]):
                j -= 1
            out.append(pts[j]); i = j
        return out


def simplify(pts, tol_km):
    """Douglas-Peucker on (lat, lon) points, tolerance in km (flat, local)."""
    if len(pts) < 3:
        return pts
    def dist(p, a, b):
        ky = 111.0; kx = 111.0 * math.cos(math.radians(p[0]))
        ax, ay = (a[1] - p[1]) * kx, (a[0] - p[0]) * ky; bx, by = (b[1] - p[1]) * kx, (b[0] - p[0]) * ky
        dx, dy = bx - ax, by - ay
        if dx == dy == 0:
            return math.hypot(ax, ay)
        t = max(0.0, min(1.0, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
        return math.hypot(ax + t * dx, ay + t * dy)
    keep = [0, len(pts) - 1]; stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        k, d = max(((k, dist(pts[k], pts[i], pts[j])) for k in range(i + 1, j)), key=lambda t: t[1])
        if d > tol_km:
            keep.append(k); stack += [(i, k), (k, j)]
    return [pts[k] for k in sorted(keep)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True); ap.add_argument("--land", action="append", required=True)
    ap.add_argument("--bbox", default="-180,35,15,86", help="lon,lat,lon,lat of the fine mask")
    ap.add_argument("--res", type=float, default=1000.0); ap.add_argument("--gebco")
    ap.add_argument("--coarse-land", action="append"); ap.add_argument("--coarse-bbox", default="-180,-60,180,86")
    ap.add_argument("--coarse-res", type=float, default=4000.0)
    ap.add_argument("--ids"); ap.add_argument("--out", default="routing-out"); ap.add_argument("--geojson-dir")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fine = Grid(a.out, "fine", a.land, [float(v) for v in a.bbox.split(",")], a.res, a.gebco)
    coarse = Grid(a.out, "coarse", a.coarse_land, [float(v) for v in a.coarse_bbox.split(",")], a.coarse_res) if a.coarse_land else None

    def grid_for(p, q):
        for g in (fine, coarse):
            if g is not None and g.inside(*g.rc(*p)) and g.inside(*g.rc(*q)):
                return g
        return None

    db = sqlite3.connect(a.db); db.row_factory = sqlite3.Row
    rows = db.execute("select id, title, tags, waypoints from artifacts where type='track' order by id").fetchall()
    if a.ids:
        want = set(a.ids.split(",")); rows = [r for r in rows if r["id"] in want]
    results = {}
    for r in rows:
        words = (r["title"] + " " + (r["tags"] or "")).lower()
        if any(w in words for w in SKIP_WORDS):
            print(f"skip {r['id']}: {r['title'][:60]}", file=sys.stderr); continue
        wps = json.loads(r["waypoints"] or "[]")
        pts = [(float(w["lat"]), float(w["lon"])) for w in wps if w.get("lat") is not None and w.get("lon") is not None]
        if len(pts) < 2:
            continue
        t0 = time.time(); routed = []; how = {"fine": 0, "coarse": 0, "great circle": 0}
        for p, q in zip(pts, pts[1:]):
            g = grid_for(p, q)
            if g is None:
                routed += great_circle(p, q); how["great circle"] += 1
            else:
                routed += g.route(p, q); how["fine" if g is fine else "coarse"] += 1
        routed = simplify(routed, 1.0)
        s_land, s_n = fine.land_along(pts); r_land, r_n = fine.land_along(routed)
        results[r["id"]] = {"title": r["title"], "waypoints": wps, "straight": pts, "routed": routed, "segments": how,
                            "straight_land_frac": round(s_land / max(1, s_n), 3), "routed_land_frac": round(r_land / max(1, r_n), 3),
                            "points": len(routed), "seconds": round(time.time() - t0, 1)}
        print(f"{r['id']}: {len(pts)} waypoints -> {len(routed)} points, land {s_land/max(1,s_n):.0%} -> {r_land/max(1,r_n):.0%}, "
              f"{how}, {time.time()-t0:.1f}s", file=sys.stderr)
        if a.geojson_dir:
            os.makedirs(a.geojson_dir, exist_ok=True)
            with open(os.path.join(a.geojson_dir, f"{r['id']}.geojson"), "w") as fh:
                json.dump({"type": "LineString", "coordinates": [[round(lon, 5), round(lat, 5)] for lat, lon in routed]}, fh)
    json.dump(results, open(os.path.join(a.out, "routes.json"), "w"))

    # figures: the fine mask with every routed track (yellow) over its straight line (red)
    def draw(k, crop, name):
        img = Image.fromarray(np.where(fine.land[::k, ::k], 70, 20).astype(np.uint8)).convert("RGB"); d = ImageDraw.Draw(img)
        for v in results.values():
            d.line([(c / k, rr / k) for rr, c in (fine.rc(*p) for p in v["straight"])], fill=(220, 60, 60), width=1)
        for v in results.values():
            d.line([(c / k, rr / k) for rr, c in (fine.rc(*p) for p in v["routed"])], fill=(255, 220, 60), width=2)
        if crop:
            (r0, c0), (r1, c1) = fine.rc(crop[3], crop[0]), fine.rc(crop[1], crop[2])
            img = img.crop((c0 // k, r0 // k, c1 // k, r1 // k))
        img.save(os.path.join(a.out, name))
    draw(max(1, int(round(8000 / fine.res)) * 2), None, "overview.png")
    draw(max(1, int(round(4000 / fine.res)) * 2), (-130, 60, -60, 78), "archipelago.png")
    with open(os.path.join(a.out, "summary.md"), "w") as fh:
        fh.write(f"Land along the line, sampled every {fine.km:g} km cell, for the {len(results)} tracks routed.\n\n")
        fh.write("| track | waypoints | routed points | on land, straight | on land, routed | segments | s |\n|---|---|---|---|---|---|---|\n")
        for k, v in sorted(results.items(), key=lambda kv: -kv[1]["routed_land_frac"]):
            seg = ", ".join(f"{n} {w}" for w, n in v["segments"].items() if n)
            fh.write(f"| {k} | {len(v['straight'])} | {v['points']} | {v['straight_land_frac']:.0%} | {v['routed_land_frac']:.0%} | {seg} | {v['seconds']} |\n")


if __name__ == "__main__":
    main()
