"""The history layer: the schema, the atomic dates, the wiki links, the publish."""

import json
import tempfile
import unittest
from pathlib import Path

import arctic_history as H


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.db = self.root / "history.sqlite"
        self.c = H.connect(self.db)
        self.addCleanup(self.c.close)
        H.add_topic(self.c, "franklin-1845", "The Franklin expedition")
        H.add_source(self.c, "mcclintock1859voyage", "The Voyage of the Fox",
                     author="McClintock", year="1859", url="https://example.invalid/fox",
                     licence="public domain", primary=True, entry_type="book")

    def artifact(self, **kw):
        base = dict(id="franklin-1845-001", topic="franklin-1845", type="image",
                    title="A plate", credit="Royal Museums Greenwich",
                    bibkey="mcclintock1859voyage", licence="public domain", lat=74.7, lon=-91.8)
        base.update(kw)
        ident = base.pop("id")
        return H.add_artifact(self.c, ident, base.pop("topic"), base.pop("type"),
                              base.pop("title"), **base)

    # ---------------------------------------------------------------- writing
    def test_artifact_requires_credit_and_source(self):
        with self.assertRaises(ValueError):
            self.artifact(credit="")
        with self.assertRaises(ValueError):
            self.artifact(bibkey="")
        with self.assertRaises(ValueError):
            self.artifact(type="postcard")

    def test_artifact_needs_a_position_or_a_geometry(self):
        with self.assertRaises(ValueError):
            self.artifact(lat=None, lon=None)
        self.artifact(lat=None, lon=None, type="track",
                      geometry={"type": "LineString", "coordinates": [[-91, 74], [-92, 75]]})

    def test_out_of_range_coordinates_are_refused(self):
        with self.assertRaises(ValueError):
            self.artifact(lat=91)
        with self.assertRaises(ValueError):
            self.artifact(lon=-200)

    def test_writing_twice_updates_rather_than_duplicates(self):
        self.artifact(title="First wording")
        self.artifact(title="Second wording")
        rows = self.c.execute("SELECT title FROM artifacts").fetchall()
        self.assertEqual([r["title"] for r in rows], ["Second wording"])

    def test_an_event_written_twice_stays_one_row(self):
        a = H.add_event(self.c, "franklin-1845", "1847-06-11", "Franklin dies", lat=70.08, lon=-98.4)
        b = H.add_event(self.c, "franklin-1845", "1847-06-11", "Franklin dies", detail="added later")
        self.assertEqual(a, b)
        self.assertEqual(self.c.execute("SELECT COUNT(*) AS n FROM events").fetchone()["n"], 1)

    # ---------------------------------------------------------------- dates
    def test_a_plain_date_is_one_atomic_point(self):
        H.add_event(self.c, "franklin-1845", "1847-06-11", "Franklin dies")
        rows = self.c.execute("SELECT date, role, precision, span FROM dates").fetchall()
        self.assertEqual([tuple(r) for r in rows], [("1847-06-11", "point", "day", "")])

    def test_a_time_limited_activity_becomes_two_atomic_rows_sharing_a_span(self):
        H.add_event(self.c, "franklin-1845", "1845-09", "Beechey Island wintering",
                    date_end="1846-08", lat=74.71, lon=-91.85)
        rows = self.c.execute("SELECT date, role, span, precision FROM dates ORDER BY date").fetchall()
        self.assertEqual([r["role"] for r in rows], ["start", "end"])
        self.assertEqual([r["date"] for r in rows], ["1845-09", "1846-08"])
        self.assertEqual(rows[0]["span"], rows[1]["span"])
        self.assertNotEqual(rows[0]["span"], "")
        self.assertEqual({r["precision"] for r in rows}, {"month"})

    def test_an_artifact_date_range_is_stored_atomically_too(self):
        self.artifact(type="track", date="1845/1848",
                      geometry={"type": "LineString", "coordinates": [[-91, 74], [-92, 75]]})
        rows = self.c.execute("SELECT date, role FROM dates ORDER BY date").fetchall()
        self.assertEqual([tuple(r) for r in rows], [("1845", "start"), ("1848", "end")])

    def test_precision_is_read_off_the_shape_and_can_be_overridden(self):
        self.assertEqual(H.date_precision("1848-04-25"), "day")
        self.assertEqual(H.date_precision("1848-04"), "month")
        self.assertEqual(H.date_precision("1848"), "year")
        H.add_date(self.c, "event", "x", "1848", precision="season", label="the summer")
        r = self.c.execute("SELECT precision FROM dates").fetchone()
        self.assertEqual(r["precision"], "season")

    def test_bad_dates_precisions_and_qualifiers_are_refused(self):
        with self.assertRaises(ValueError):
            H.add_date(self.c, "event", "x", "not a date")
        with self.assertRaises(ValueError):
            H.add_date(self.c, "event", "x", "1848", precision="fortnight")
        with self.assertRaises(ValueError):
            H.add_date(self.c, "event", "x", "1848", qualifier="maybe")
        with self.assertRaises(ValueError):
            H.add_date(self.c, "event", "x", "1848", role="middle")

    def test_the_same_date_twice_updates_rather_than_duplicating(self):
        H.add_date(self.c, "artifact", "a1", "1859-05-06", label="found by Hobson")
        H.add_date(self.c, "artifact", "a1", "1859-05-06", label="found by Hobson", qualifier="circa")
        rows = self.c.execute("SELECT qualifier FROM dates").fetchall()
        self.assertEqual([r["qualifier"] for r in rows], ["circa"])

    def test_each_span_end_keeps_its_own_precision(self):
        H.add_event(self.c, "franklin-1845", "1612-08-15", "Button winters at Port Nelson",
                    date_end="1613-07")
        rows = {r["role"]: r["precision"] for r in self.c.execute("SELECT role, precision FROM dates")}
        self.assertEqual(rows, {"start": "day", "end": "month"})

    def test_redating_an_artifact_replaces_its_timeline_row(self):
        self.artifact(date="1822-02")
        self.artifact(date="1822-03")
        rows = self.c.execute("SELECT date FROM dates WHERE entity_kind='artifact'").fetchall()
        self.assertEqual([r["date"] for r in rows], ["1822-03"])
        # a date attached separately with `date` survives the re-dating
        H.add_date(self.c, "artifact", "franklin-1845-001", "1859-05-06", label="found by Hobson")
        self.artifact(date="1822-04")
        dates = sorted(r["date"] for r in self.c.execute("SELECT date FROM dates WHERE entity_kind='artifact'"))
        self.assertEqual(dates, ["1822-04", "1859-05-06"])

    def test_a_shared_person_keeps_their_home_topic(self):
        H.add_person(self.c, "Tulluahiu", indigenous=True, topic="inuit-oral-history")
        H.add_person(self.c, "Tulluahiu", topic="ross-victory", note="the wooden leg")
        r = self.c.execute("SELECT topic, note, indigenous FROM people").fetchone()
        self.assertEqual(r["topic"], "inuit-oral-history")   # enriched, not moved
        self.assertEqual(r["note"], "the wooden leg")
        self.assertEqual(r["indigenous"], 1)                 # and never quietly un-flagged

    def test_forget_removes_a_row_and_its_attached_dates(self):
        H.add_person(self.c, "Duplicate Person")
        H.add_date(self.c, "person", "Duplicate Person", "1876", label="died")
        r = H.forget(self.c, "person", "Duplicate Person")
        self.assertEqual(r["dates"], 1)
        self.assertIsNone(self.c.execute("SELECT 1 FROM people WHERE name='Duplicate Person'").fetchone())
        with self.assertRaises(ValueError):
            H.forget(self.c, "person", "Duplicate Person")

    def test_a_span_ending_before_it_starts_is_reported(self):
        H.span_dates(self.c, "event", "backwards", "1850", "1840", label="impossible")
        problems = H.validate(self.c)["problems"]
        self.assertTrue(any("before it starts" in p["detail"] for p in problems))

    def test_a_half_open_span_is_reported(self):
        H.add_date(self.c, "event", "lonely", "1850", role="start", span="lonely:1850")
        problems = H.validate(self.c)["problems"]
        self.assertTrue(any("endpoint" in p["detail"] for p in problems))

    # ---------------------------------------------------------------- wiki
    def test_wikilinks_resolve_by_kind_and_by_title(self):
        self.artifact(title="A plate")
        H.add_person(self.c, "Tookoolito", indigenous=True, role="interpreter")
        H.add_place(self.c, "Beechey Island", lat=74.71, lon=-91.85)
        H.add_page(self.c, "the-march", "The march",
                   "See [[artifact:franklin-1845-001]], [[person:Tookoolito]], "
                   "[[place:Beechey Island]] and [[source:mcclintock1859voyage]]; "
                   "also [[The Voyage of the Fox]] by title.", topic="franklin-1845")
        info = H.reindex_links(self.c)
        self.assertEqual(info["wanted"], {})
        html = H.render_markdown(
            self.c.execute("SELECT body FROM pages WHERE slug='the-march'").fetchone()["body"],
            H.index_targets(self.c))
        self.assertIn("(artifact/franklin-1845-001)", html)
        self.assertIn("(person/tookoolito)", html)
        self.assertIn("(place/beechey-island)", html)
        self.assertIn("(source/mcclintock1859voyage)", html)

    def test_pages_are_drafts_by_default_and_keep_their_versions(self):
        H.add_page(self.c, "the-march", "The march", "First wording.", topic="franklin-1845")
        self.assertEqual(self.c.execute("SELECT status FROM pages").fetchone()["status"], "draft")
        H.add_page(self.c, "the-march", "The march", "Second wording.", topic="franklin-1845")
        hist = self.c.execute("SELECT body FROM page_history ORDER BY id").fetchall()
        self.assertEqual([h["body"] for h in hist], ["First wording."])
        H.add_page(self.c, "the-march", "The march", "Second wording.", status="good")
        self.assertEqual(self.c.execute("SELECT status FROM pages").fetchone()["status"], "good")
        H.add_page(self.c, "the-march", "The march", "Third wording.")
        # a rewrite keeps the status it had unless told otherwise
        self.assertEqual(self.c.execute("SELECT status FROM pages").fetchone()["status"], "good")
        self.assertEqual(self.c.execute("SELECT COUNT(*) AS n FROM page_history").fetchone()["n"], 2)
        with self.assertRaises(ValueError):
            H.add_page(self.c, "x", "X", "body", status="perfect")

    def test_an_unwritten_link_is_kept_and_listed_as_wanted(self):
        H.add_page(self.c, "the-march", "The march", "See [[person:John Rae]].", topic="franklin-1845")
        info = H.reindex_links(self.c)
        self.assertIn("person:John Rae", info["wanted"])
        self.assertEqual(info["wanted"]["person:John Rae"], ["the-march"])
        html = H.render_markdown("[[person:John Rae]]", H.index_targets(self.c))
        self.assertIn('class="wanted"', html)

    def test_a_link_label_can_be_given_and_defaults_to_the_title(self):
        self.artifact(title="A plate")
        targets = H.index_targets(self.c)
        self.assertIn("[A plate]", H.render_markdown("[[artifact:franklin-1845-001]]", targets))
        self.assertIn("[my wording]",
                      H.render_markdown("[[artifact:franklin-1845-001|my wording]]", targets))

    def test_place_links_resolve_through_historic_and_inuktitut_names(self):
        H.add_place(self.c, "Mittimatalik", historic="Pond Inlet", inuktitut="Mittimatalik",
                    lat=72.7, lon=-77.96)
        targets = H.index_targets(self.c)
        self.assertIn("(place/mittimatalik)", H.render_markdown("[[place:Pond Inlet]]", targets))

    def test_backlinks_are_recorded(self):
        H.add_person(self.c, "Tookoolito")
        H.add_page(self.c, "one", "One", "[[person:Tookoolito]]")
        H.add_page(self.c, "two", "Two", "[[person:Tookoolito]]")
        H.reindex_links(self.c)
        srcs = [r["src"] for r in self.c.execute(
            "SELECT src FROM links WHERE target='person/tookoolito' ORDER BY src")]
        self.assertEqual(srcs, ["one", "two"])

    def test_slugify_keeps_arctic_spellings_legible(self):
        self.assertEqual(H.slugify("Gjøa Haven"), "gjoa-haven")
        self.assertEqual(H.slugify("Grœnlendinga saga"), "gr-nlendinga-saga")
        self.assertEqual(H.slugify("Qausuittuq (Resolute)"), "qausuittuq-resolute")

    # ---------------------------------------------------------------- bibtex
    def test_bibtex_round_trips(self):
        text = H.to_bibtex(self.c.execute("SELECT * FROM sources"))
        self.assertIn("@book{mcclintock1859voyage,", text)
        self.assertIn("keywords = {primary}", text)
        parsed = H.parse_bib(text)
        self.assertEqual(parsed[0]["bibkey"], "mcclintock1859voyage")
        self.assertEqual(parsed[0]["title"], "The Voyage of the Fox")
        self.assertTrue(parsed[0]["primary"])

    def test_importing_a_bib_file_adds_sources(self):
        keys = H.import_bib(self.c, """
            @book{parry1821journal,
              author = {Parry, William Edward},
              title = {Journal of a Voyage for the Discovery of a North-West Passage},
              year = {1821}, publisher = {John Murray},
              keywords = {primary}
            }
        """, topic="ross-parry")
        self.assertEqual(keys, ["parry1821journal"])
        r = self.c.execute("SELECT * FROM sources WHERE bibkey='parry1821journal'").fetchone()
        self.assertEqual(r["primary_src"], 1)
        self.assertEqual(r["publisher"], "John Murray")

    # ---------------------------------------------------------------- checks
    def test_validate_catches_a_missing_source_and_a_stray_licence(self):
        self.artifact(bibkey="nosuchkey", licence="")
        problems = H.validate(self.c)["problems"]
        self.assertTrue(any("is in no source entry" in p["detail"] for p in problems))
        self.assertTrue(any("no licence" in p["detail"] for p in problems))

    def test_validate_flags_a_dropped_minus_sign_but_allows_europe(self):
        # the Beard daguerreotypes were taken at Greenhithe, genuinely 0.28 east
        self.artifact(id="greenhithe", lat=51.45, lon=0.28)
        self.assertFalse(any(p["what"] == "greenhithe" for p in H.validate(self.c)["problems"]))
        self.artifact(id="mirror", lon=98.55)
        self.assertTrue(any(p["what"] == "mirror" and "minus sign" in p["detail"]
                            for p in H.validate(self.c)["problems"]))

    def test_validate_allows_a_biographical_place_south_of_the_arctic(self):
        # Tookoolito lived and died in Groton, Connecticut
        H.add_place(self.c, "Groton", lat=41.3498, lon=-72.0784, kind="community")
        self.assertFalse(any(p["what"] == "Groton" for p in H.validate(self.c)["problems"]))
        H.add_place(self.c, "Flipped", lat=70.0, lon=98.4)
        self.assertTrue(any(p["what"] == "Flipped" for p in H.validate(self.c)["problems"]))

    def test_validate_checks_every_waypoint_and_geometry_point(self):
        self.artifact(id="flip", type="track", lat=None, lon=None,
                      waypoints=[{"date": "1845-05-19", "lat": 51.45, "lon": 0.28},
                                 {"date": "1846-09-12", "lat": 70.08, "lon": 98.4}],
                      geometry={"type": "LineString", "coordinates": [[0.28, 51.45], [98.4, 70.08]]})
        problems = H.validate(self.c)["problems"]
        self.assertTrue(any(p["what"] == "flip" and "waypoint 1" in p["detail"] for p in problems))
        self.assertTrue(any(p["what"] == "flip" and "geometry point" in p["detail"] for p in problems))

    def test_a_request_too_thin_for_a_person_to_act_on_is_refused(self):
        with self.assertRaises(ValueError):
            H.add_request(self.c, "franklin-1845", "api_key", "Flickr key", why="need images")
        with self.assertRaises(ValueError):    # download without the page to start from
            H.add_request(self.c, "franklin-1845", "download", "the 1859 chart",
                          why="McClintock's chart of the search, wanted as the base layer for the track map.")
        ident = H.add_request(self.c, "franklin-1845", "download", "the 1859 chart",
                              why="McClintock's chart of the search, wanted as the base layer for the track map.",
                              url="https://example.invalid/chart.jpg")
        self.assertEqual(H.list_requests(self.c)[0]["id"], ident)

    def test_validate_notices_a_missing_local_file(self):
        self.artifact(local_file="franklin-1845/files/not-there.jpg")
        self.assertTrue(any("local_file missing" in p["detail"] for p in H.validate(self.c)["problems"]))

    # ---------------------------------------------------------------- publish
    def test_publish_writes_the_wiki_the_map_and_the_timeline(self):
        self.artifact(title="A plate", local_file="")
        self.artifact(id="franklin-1845-002", type="track", title="Erebus and Terror",
                      date="1845/1848", lat=None, lon=None,
                      waypoints=[{"date": "1845-05-19", "lat": 51.45, "lon": 0.28, "note": "leaves"},
                                 {"date": "1846-09-12", "lat": 70.08, "lon": -98.4, "note": "beset"}],
                      geometry={"type": "LineString", "coordinates": [[0.28, 51.45], [-98.4, 70.08]]})
        H.add_event(self.c, "franklin-1845", "1845-09", "Beechey wintering", date_end="1846-08")
        H.add_person(self.c, "Tookoolito", indigenous=True)
        H.add_page(self.c, "the-march", "The march", "See [[artifact:franklin-1845-001]].",
                   topic="franklin-1845", ordering=10)

        web = self.root / "web"
        out = H.publish(web, self.db)
        self.assertEqual(out["artifacts"], 2)
        self.assertEqual(out["topics"], 1)
        self.assertGreaterEqual(out["pages"], 5)          # one written, four generated

        arts = json.loads((web / "data/history/artifacts.json").read_text())["artifacts"]
        track = next(a for a in arts if a["type"] == "track")
        self.assertEqual(track["geometry"]["type"], "LineString")
        self.assertEqual(len(track["waypoints"]), 2)
        self.assertEqual(track["page"], "artifact/franklin-1845-002")

        # the timeline collapses each span into one row carrying both ends
        tl = json.loads((web / "data/history/timeline.json").read_text())["timeline"]
        wintering = next(t for t in tl if t["label"] == "Beechey wintering")
        self.assertEqual((wintering["date"], wintering["date_end"]), ("1845-09", "1846-08"))
        self.assertEqual(wintering["role"], "start")

        index = json.loads((web / "data/history/index.json").read_text())
        self.assertTrue(any(p["slug"] == "person/tookoolito" for p in index["pages"]))
        self.assertEqual(index["topics"][0]["artifacts"], 2)

        page = json.loads((web / "data/history/pages/the-march.json").read_text())
        self.assertIn("(artifact/franklin-1845-001)", page["html"])
        gen = json.loads((web / "data/history/pages/artifact__franklin-1845-001.json").read_text())
        self.assertIn("Royal Museums Greenwich", gen["html"])
        self.assertIn("the-march", gen["backlinks"])
        self.assertIn("@book{mcclintock1859voyage,", (web / "data/history/references.bib").read_text())

    def test_publish_copies_an_artifact_file_and_links_it(self):
        files = H.HISTORY_DIR / "franklin-1845" / "files"
        # the module's own directory is the real repository one, so use a name
        # that cannot collide with a researcher's work
        files.mkdir(parents=True, exist_ok=True)
        f = files / "zz-test-artifact-file.jpg"
        f.write_bytes(b"x" * 5000)
        self.addCleanup(f.unlink)
        self.artifact(local_file="franklin-1845/files/zz-test-artifact-file.jpg")
        web = self.root / "web"
        H.publish(web, self.db)
        arts = json.loads((web / "data/history/artifacts.json").read_text())["artifacts"]
        self.assertEqual(arts[0]["url"], "data/history/files/zz-test-artifact-file.jpg")
        self.assertTrue((web / "data/history/files/zz-test-artifact-file.jpg").is_file())

    def test_publish_without_a_database_is_quiet(self):
        self.assertIsNone(H.publish(self.root / "web", self.root / "missing.sqlite"))


    def test_dateline_longitudes_are_honest(self):
        self.assertIsNone(H._off_map(69.72, 176.72))      # Siberian coast, the Karluk's survivors
        self.assertIsNotNone(H._off_map(74.7, 91.8))      # a dropped minus sign
        self.assertIsNotNone(H._off_map(74.7, -200))

    def test_foreign_topic_only_fills_blanks_on_a_person(self):
        H.add_person(self.c, "Robert Bartlett", role="master of the Roosevelt", topic="sverdrup-bernier-peary")
        H.add_person(self.c, "Robert Bartlett", role="schooner captain at Frobisher Bay", born="1875",
                     topic="hudson-strait-south-baffin")
        r = self.c.execute("SELECT role, born, topic FROM people WHERE name='Robert Bartlett'").fetchone()
        self.assertEqual(r["role"], "master of the Roosevelt")
        self.assertEqual(r["born"], "1875")                # a blank the home topic had left
        self.assertEqual(r["topic"], "sverdrup-bernier-peary")


    def test_platform_gate_allows_one_session_per_hour_for_the_crew(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            ledger = Path(d) / "platform-sessions.json"
            self.assertEqual(H.platform_session_gate(ledger, "scholarsportal", 1000.0), 0.0)   # first use: go
            self.assertAlmostEqual(H.platform_session_gate(ledger, "scholarsportal", 1600.0), 3000.0)  # 10 min later: wait 50
            self.assertEqual(H.platform_session_gate(ledger, "canadacommons", 1600.0), 0.0)     # another platform: go
            self.assertEqual(H.platform_session_gate(ledger, "scholarsportal", 4601.0), 0.0)    # after the hour: go


if __name__ == "__main__":
    unittest.main()
