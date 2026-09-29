"""The terrain router's regions: which grid a track is routed in, the grids'
scale, and (when the mosaics are on disk) a leg routed east of 30 W and one in
Svalbard.  Needs the routing venv (.route-venv: numpy, scipy, scikit-image,
pyproj); skipped under a Python without it."""

import importlib.util
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    _spec = importlib.util.spec_from_file_location("digitize_tracks", ROOT / "tools" / "digitize-tracks.py")
    DT = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(DT)
except ImportError as e:          # numpy, scikit-image or pyproj missing
    DT, _WHY = None, str(e)


def geometry_only():
    return [DT.Terrain(r, load=False) for r in DT.REGIONS]


def built(name):
    d = DT.REGION_BY_NAME[name]["dir"]
    return (d / "meta.json").exists() and all((d / f"{n}.npy").exists() for n in ("dem", "slope", "land", "ice"))


# the Sledge Patrol: Eskimonæs, Sabine Island, Ella Island, Scoresbysund
EAST_GREENLAND = [(74.10, -21.30), (74.60, -18.80), (74.10, -21.30), (72.85, -25.00), (70.49, -21.97)]
# Nordenskiöld over Nordaustlandet, 1873, much simplified
NORDAUSTLANDET = [(80.20, 18.20), (80.00, 20.50), (79.85, 23.00), (80.35, 24.20)]
# Nenets on Yamal, spring
YAMAL = [(66.50, 66.60), (67.80, 68.40), (69.40, 69.20), (70.60, 68.60)]
# Ellesmere, well inside the grid of 2026-09-10
ELLESMERE = [(79.00, -80.00), (79.60, -82.50), (80.20, -85.00), (80.80, -88.00)]


@unittest.skipIf(DT is None, "needs the routing venv")
class RegionChoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.G = geometry_only()

    def choose(self, wps):
        return DT.choose_region(wps, self.G).name

    def test_regions_cover_everything_north_of_40(self):
        for lat in (40.0, 45.0, 55.0, 66.0, 75.0, 84.0, 89.9):
            for lon in range(-180, 180, 5):
                self.assertTrue(any(T.holds((lat, float(lon))) for T in self.G), (lat, lon))

    def test_the_canadian_arctic_grid_holds_only_its_own_tiles(self):
        ca = self.G[0]
        self.assertEqual(ca.name, "canada-arctic")
        self.assertTrue(ca.holds((75.0, -80.0)))
        self.assertFalse(ca.holds((75.0, -20.0)))      # east of 30 W: in the rectangle, but no tiles
        self.assertFalse(ca.holds((58.0, -80.0)))      # south of 60 N: the same

    def test_a_track_it_holds_stays_in_the_canadian_arctic_grid(self):
        # the sector about 90 W holds it too; the old grid wins the tie so its
        # tracks route as they did
        self.assertTrue(all(self.G[1].holds(p) for p in ELLESMERE))
        self.assertEqual(self.choose(ELLESMERE), "canada-arctic")

    def test_east_greenland_goes_to_a_sector_not_the_old_grid(self):
        # 18 to 25 W: past the old grid's tiles; the sectors about 45 W and 0 (and,
        # their rectangles running over the pole, others) hold it; the nearest wins
        self.assertFalse(any(self.G[0].holds(p) for p in EAST_GREENLAND))
        both = [T for T in self.G[1:] if all(T.holds(p) for p in EAST_GREENLAND)]
        self.assertTrue({"sector-000e", "sector-045w"} <= {T.name for T in both})
        nearest = min(both, key=lambda T: max(T.centre_deg(p) for p in EAST_GREENLAND))
        self.assertEqual(self.choose(EAST_GREENLAND), nearest.name)

    def test_svalbard_and_siberia_go_to_a_sector_that_holds_every_leg(self):
        for wps in (NORDAUSTLANDET, YAMAL):
            name = self.choose(wps)
            T = next(t for t in self.G if t.name == name)
            self.assertTrue(name.startswith("sector-"), name)
            self.assertTrue(all(T.holds(p) for p in wps), name)

    def test_a_track_over_the_old_edge_goes_where_most_of_its_legs_are(self):
        # Koch and Wegener's line to 24.5 W: three legs in the old grid, all
        # four in the sector about 45 W
        wps = [(76.8, -45.0), (76.9, -40.0), (77.0, -35.0), (77.0, -30.5), (77.1, -24.5)]
        self.assertEqual(sum(1 for a, b in zip(wps, wps[1:]) if self.G[0].holds(a) and self.G[0].holds(b)), 3)
        self.assertEqual(self.choose(wps), "sector-045w")

    def test_a_track_across_the_date_line(self):
        wps = [(71.0, 179.0), (70.5, -179.5), (69.8, -177.0)]
        name = self.choose(wps)
        T = next(t for t in self.G if t.name == name)
        self.assertTrue(all(T.holds(p) for p in wps), name)

    def test_a_sector_cell_is_250_m_on_the_ground_within_4_per_cent(self):
        for T in self.G[1:]:
            for lat, dlon in ((40.0, 0.0), (40.0, 29.0), (65.0, 0.0), (89.0, 0.0), (55.0, -20.0)):
                p = (lat, T.region["centre"][1] + dlon)
                r, c = T.rc(*p)
                self.assertTrue(T.inside(r, c), (T.name, p))
                g = float(T.ground_km(r, r + 1, c, c + 1, step=1)[0, 0])
                self.assertLess(abs(g - 0.25) / 0.25, 0.04, (T.name, p, g))

    def test_long_polygon_edges_are_filled_in(self):
        # GSHHG cuts Eurasia at the date line with a 4-degree meridian edge
        # through Chukotka; in a sector whose meridians bend it must follow
        # the meridian, so the edge is filled in every 0.1 degree
        np = DT.np
        xy = np.array([[180.0, 68.99], [180.0, 65.03], [179.95, 65.03], [180.0, 68.99]])
        d = DT.densify_ll(xy)
        self.assertEqual(tuple(d[0]), tuple(xy[0]))
        self.assertEqual(tuple(d[-1]), tuple(xy[-1]))
        self.assertLessEqual(float(np.abs(np.diff(d, axis=0)).max()), 0.1 + 1e-9)
        self.assertTrue(np.allclose(d[:40, 0], 180.0))
        short = np.array([[0.0, 0.0], [0.05, 0.0], [0.0, 0.05], [0.0, 0.0]])
        self.assertIs(DT.densify_ll(short), short)

    def test_the_old_grid_is_the_grid_it_was(self):
        ca = self.G[0]
        self.assertEqual(ca.proj, DT.PROJ)
        self.assertEqual((ca.nrows, ca.ncols), (13326, 24610))
        meta = ca.dir / "meta.json"
        if meta.exists():
            self.assertEqual(json.loads(meta.read_text())["shape"], [ca.nrows, ca.ncols])


@unittest.skipIf(DT is None, "needs the routing venv")
class RoutingInTheNewRegionsTests(unittest.TestCase):
    def route(self, wps, month=4):
        T = DT.choose_region(wps, geometry_only())
        if not built(T.name):
            self.skipTest(f"{T.name} mosaic not built (tools/digitize-tracks.py dem)")
        T = DT.terrain(T.name)
        R = DT.Router(T)
        out = []
        for p, q in zip(wps, wps[1:]):
            seg, info = R.route_leg(p, q, month, False)
            out.append((seg, info))
        return T, out

    def check(self, wps):
        T, legs = self.route(wps)
        for (p, q), (seg, info) in zip(zip(wps, wps[1:]), legs):
            self.assertNotIn("fallback", info, info)
            self.assertEqual(seg[0], p)
            self.assertEqual(seg[-1], q)
            chord = DT.gc_km(p, q)
            self.assertGreaterEqual(DT.line_km(seg), chord * 0.98)
            self.assertLess(DT.line_km(seg), chord * 3.0)
        return T, legs

    def test_a_sledge_patrol_leg_east_of_30_w(self):
        T, legs = self.check(EAST_GREENLAND)
        # Wollaston Foreland and Clavering are land, and the terrain is there
        r, c = T.rc(74.4, -19.6)
        self.assertTrue(bool(T.land[r, c]))
        self.assertGreater(float(T.dem[r - 40:r + 40, c - 40:c + 40].max()), 500.0)

    def test_a_leg_over_nordaustlandet(self):
        T, legs = self.check(NORDAUSTLANDET)
        r, c = T.rc(79.85, 23.0)
        self.assertTrue(bool(T.ice[r, c]))          # Austfonna
        self.assertTrue(any(info["ice_km"] > 0 or info["land_km"] > 0 for _, info in legs))

    def test_a_leg_on_yamal(self):
        self.check(YAMAL)

    def test_chukotka_is_land_on_both_sides_of_the_date_line(self):
        for name in ("sector-180", "sector-135e", "sector-135w"):
            if not built(name):
                continue
            T = DT.terrain(name)
            for p in ((67.0, 179.9), (67.0, -179.9), (67.0, 180.0)):
                r, c = T.rc(*p)
                self.assertTrue(bool(T.land[r, c]), (name, p))


if __name__ == "__main__":
    unittest.main()
