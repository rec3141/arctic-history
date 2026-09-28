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
                     licence="public-domain", primary=True, entry_type="book")

    def artifact(self, **kw):
        base = dict(id="franklin-1845-001", topic="franklin-1845", type="image",
                    title="A plate", credit="Royal Museums Greenwich",
                    bibkey="mcclintock1859voyage", licence="public-domain", lat=74.7, lon=-91.8)
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

    def test_routing_codes(self):
        line = {"type": "LineString", "coordinates": [[-91, 74], [-92, 75]]}
        for code in H.ROUTING:
            self.artifact(type="track", geometry=line, routing=code)
        self.assertIn("terrain", H.ROUTING)
        row = self.c.execute("SELECT routing FROM artifacts").fetchone()
        self.assertEqual(row["routing"], "terrain")
        with self.assertRaises(ValueError):
            self.artifact(type="track", geometry=line, routing="overland")

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

    def test_a_rerun_keeps_the_fields_it_does_not_pass(self):
        self.artifact(title="A plate", date="1859-05-06", tags="franklin,record", people="Hobson")
        self.artifact(title="A plate, reworded")
        row = self.c.execute("SELECT * FROM artifacts").fetchone()
        self.assertEqual(row["title"], "A plate, reworded")
        self.assertEqual((row["date_text"], row["date_start"]), ("1859-05-06", "1859-05-06"))
        self.assertEqual(json.loads(row["tags"]), ["franklin", "record"])
        self.assertEqual(json.loads(row["people"]), ["Hobson"])
        self.assertEqual((row["lat"], row["lon"]), (74.7, -91.8))
        # an explicit empty string clears
        self.artifact(title="A plate, reworded", tags="", people="")
        row = self.c.execute("SELECT * FROM artifacts").fetchone()
        self.assertEqual((json.loads(row["tags"]), json.loads(row["people"])), ([], []))
        self.assertEqual(row["date_start"], "1859-05-06")

    def test_a_replaced_artifact_is_kept_with_its_message(self):
        self.artifact(title="A plate", tags="franklin")
        self.artifact(title="A plate", tags="franklin")          # nothing changes: no version
        self.assertEqual(H.artifact_versions(self.c, "franklin-1845-001"), [])
        self.artifact(title="A plate, reworded", message="the caption named the wrong ship")
        vs = H.artifact_versions(self.c, "franklin-1845-001")
        self.assertEqual(len(vs), 1)
        self.assertEqual(vs[0]["row"]["title"], "A plate")
        self.assertEqual(vs[0]["message"], "the caption named the wrong ship")
        self.assertEqual(vs[0]["changed"], ["title"])

    def test_a_page_rerun_keeps_its_ordering_and_summary(self):
        H.add_page(self.c, "a-page", "A page", "body", topic="franklin-1845", summary="one line", ordering=30)
        H.add_page(self.c, "a-page", "A page", "body, revised", topic="franklin-1845", status="good")
        row = self.c.execute("SELECT summary, ordering, status FROM pages WHERE slug='a-page'").fetchone()
        self.assertEqual((row["summary"], row["ordering"], row["status"]), ("one line", 30, "good"))

    def test_an_unlabelled_topic_link_shows_the_topic_title(self):
        H.add_topic(self.c, "franklin-1845", "The Franklin expedition", summary="x")
        html = H.render_markdown("told in [[topic:franklin-1845]] and [[topic:franklin-1845|here]]",
                                 H.index_targets(self.c))
        self.assertIn("[The Franklin expedition]", html)
        self.assertIn("[here]", html)
        self.assertNotIn("[franklin-1845]", html)

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
    def test_an_entry_naming_its_people_only_in_the_title_is_flagged(self):
        H.add_person(self.c, "Tookoolito")
        self.artifact(id="t1", title="Tookoolito at Repulse Bay",
                      description="A portrait taken during the second expedition.",
                      people="Tookoolito")
        self.assertTrue(any(p["what"] == "t1" and "only in the title" in p["detail"]
                            for p in H.validate(self.c)["problems"]))
        self.artifact(id="t1", title="Tookoolito at Repulse Bay",
                      description="Tookoolito, photographed during the second expedition.",
                      people="Tookoolito")
        self.assertFalse(any(p["what"] == "t1" and "only in the title" in p["detail"]
                             for p in H.validate(self.c)["problems"]))

    def test_bare_mentions_and_page_people_reach_the_links_table(self):
        H.add_person(self.c, "Tookoolito", indigenous=True)
        H.add_person(self.c, "Hans Hendrik", indigenous=True)
        H.add_page(self.c, "the-march", "The march",
                   "Tookoolito interpreted throughout.", topic="franklin-1845",
                   people=["Hans Hendrik"])
        H.reindex_links(self.c)
        rows = {(r["kind"], r["target"]) for r in self.c.execute(
            "SELECT kind, target FROM links WHERE src='the-march'")}
        self.assertIn(("person", "person/tookoolito"), rows)      # bare mention
        self.assertIn(("person", "person/hans-hendrik"), rows)    # people field
        # a mention is never "wanted": it only points at what exists
        self.assertEqual(H.reindex_links(self.c)["wanted"], {})

    def test_events_get_generated_pages_and_are_linkable(self):
        ident = H.add_event(self.c, "franklin-1845", "1847-06-11", "Franklin dies",
                            lat=70.08, lon=-98.4, people="Crozier", bibkey="mcclintock1859voyage")
        pages = {p["slug"]: p for p in H.generated_pages(self.c)}
        self.assertIn(f"event/{ident}", pages)
        self.assertEqual(pages[f"event/{ident}"]["body"], "")     # prose only: the row carries the fields
        H.add_page(self.c, "one", "One", f"See [[event:{ident}]].")
        self.assertEqual(H.reindex_links(self.c)["wanted"], {})

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

    def test_generated_pages_link_by_their_row_fields(self):
        H.add_person(self.c, "Tookoolito")
        H.add_place(self.c, "Beechey Island", lat=74.71, lon=-91.85)
        self.artifact(people="Tookoolito")
        ev = H.add_event(self.c, "franklin-1845", "1845-09", "Wintering", people="Tookoolito",
                         place="Beechey Island", bibkey="mcclintock1859voyage")
        H.reindex_links(self.c)
        rows = {(r["src"], r["target"]) for r in self.c.execute("SELECT src, target FROM links")}
        self.assertIn(("artifact/franklin-1845-001", "person/tookoolito"), rows)
        self.assertIn(("artifact/franklin-1845-001", "source/mcclintock1859voyage"), rows)
        self.assertIn((f"event/{ev}", "person/tookoolito"), rows)
        self.assertIn((f"event/{ev}", "place/beechey-island"), rows)
        self.assertIn((f"event/{ev}", "source/mcclintock1859voyage"), rows)
        # a row field never makes a wanted link; check reports a bibkey with no source
        self.artifact(id="franklin-1845-002", bibkey="nosuchkey")
        self.assertEqual(H.reindex_links(self.c)["wanted"], {})

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

    def test_bibtex_carries_the_licence_phrase_but_not_the_rights_note(self):
        H.add_source(self.c, "mcclintock1859voyage", "The Voyage of the Fox", licence="crown-expired",
                     rights_note="Crown copyright of 1859 expired; internal wording for the crew")
        text = H.to_bibtex(self.c.execute("SELECT * FROM sources"))
        self.assertIn("Crown copyright expired; public domain", text)
        self.assertNotIn("internal wording", text)

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

    def test_licence_is_a_code_and_the_detail_lives_in_the_rights_note(self):
        with self.assertRaises(ValueError):
            self.artifact(licence="public domain (Crown copyright expired)")
        with self.assertRaises(ValueError):
            H.add_source(self.c, "x", "X", licence="CC BY 4.0")
        self.artifact(licence="crown-expired", rights_note="Crown copyright of 1961 expired 2011")
        r = self.c.execute("SELECT * FROM artifacts WHERE id='franklin-1845-001'").fetchone()
        self.assertEqual(r["licence"], "crown-expired")
        self.assertEqual(H.rights_text(r), "Crown copyright expired; public domain. Crown copyright of 1961 expired 2011")
        self.assertNotIn("Crown", H.artifact_body(r))          # the page body is prose only
        for code in ("cc-by-4.0", "cc-by-sa-2.5", "cc-by-nc-nd-4.0", "cc-by", "cc0", "not-cleared"):
            self.assertTrue(H.is_licence_code(code), code)
        self.assertEqual(H.licence_label("cc-by-sa-4.0"), "CC BY-SA 4.0")
        self.assertEqual(H.licence_label("cc-by-nc-nd-4.0"), "CC BY-NC-ND 4.0")
        self.assertFalse(H.is_licence_code("cc-by-sa-nd-4.0"))
        # a legacy free-text row is reported by check, not hidden
        self.c.execute("UPDATE artifacts SET licence='public domain' WHERE id='franklin-1845-001'")
        self.assertTrue(any("not a code" in p["detail"] for p in H.validate(self.c)["problems"]))

    def test_tags_are_stored_one_per_element_in_the_canonical_form(self):
        # a comma-joined string is taken apart, the shape is fixed, the repeats go
        self.artifact(tags="Nares, alert,DISCOVERY , plate,plate, ,fort conger")
        r = self.c.execute("SELECT tags FROM artifacts WHERE id='franklin-1845-001'").fetchone()
        self.assertEqual(json.loads(r["tags"]),
                         ["nares", "alert", "discovery", "plate", "fort-conger"])
        # a list comes through the same way, and an underscore is a word boundary
        self.artifact(id="franklin-1845-002", tags=["Musk_Ox", "ice shelf"])
        r = self.c.execute("SELECT tags FROM artifacts WHERE id='franklin-1845-002'").fetchone()
        self.assertEqual(json.loads(r["tags"]), ["musk-ox", "ice-shelf"])
        self.assertEqual(H.normalise_tags(""), [])

    def test_a_known_variant_is_mapped_to_its_canonical_tag(self):
        # hyphenated at the word boundary, and singular
        self.artifact(tags="stroch,dogs,fulltext,crockerland,vessels,queenelizabethislands")
        r = self.c.execute("SELECT tags FROM artifacts WHERE id='franklin-1845-001'").fetchone()
        self.assertEqual(json.loads(r["tags"]),
                         ["st-roch", "dog", "full-text", "crocker-land", "vessel",
                          "queen-elizabeth-islands"])
        # events take the same route
        H.add_event(self.c, "franklin-1845", "1848-04-25", "The record is left",
                    tags="wrecks,muskox", lat=69.97, lon=-98.55)
        r = self.c.execute("SELECT tags FROM events WHERE title='The record is left'").fetchone()
        self.assertEqual(json.loads(r["tags"]), ["wreck", "musk-ox"])
        # `leads` is the open water in the ice, not the metal in the bones
        self.assertEqual(H.normalise_tag("leads"), "leads")

    def test_check_flags_a_legacy_tag_and_notes_the_long_tail(self):
        self.artifact(tags="plate,nares")
        self.artifact(id="franklin-1845-002", tags="plate")
        self.artifact(id="franklin-1845-003", tags="plate")
        # a row written before the vocabulary settled
        self.c.execute("UPDATE artifacts SET tags='[\"stroch,ICE SHELF\"]' "
                       "WHERE id='franklin-1845-001'")
        v = H.validate(self.c)
        self.assertTrue(any("is not in the canonical form" in p["detail"] and "st-roch" in p["detail"]
                            for p in v["problems"]))
        self.c.execute("UPDATE artifacts SET tags='[\"fulltext\"]' WHERE id='franklin-1845-001'")
        v = H.validate(self.c)
        self.assertTrue(any("is a variant of 'full-text'" in p["detail"] for p in v["problems"]))
        # `plate` is used twice and stays quiet; `full-text` is the long tail
        self.assertIn(("tag", "full-text"), [(n["kind"], n["what"]) for n in v["notes"]])
        self.assertNotIn("plate", [n["what"] for n in v["notes"]])

    def test_a_known_archive_variant_is_canonicalised_on_write(self):
        H.add_source(self.c, "ross1983penny", "William Penny", licence="open-access",
                     url="https://pubs.aina.ucalgary.ca/arctic/Arctic36-4-380.pdf",
                     container="Arctic", volume="36", archive="Arctic (AINA)", entry_type="article")
        r = self.c.execute("SELECT * FROM sources WHERE bibkey='ross1983penny'").fetchone()
        self.assertEqual(r["archive"], "Arctic Institute of North America")
        # an archive nobody has spelt before is taken as written
        H.add_source(self.c, "x1", "X", licence="unknown", archive="Musee de la Gaspesie")
        self.assertEqual(self.c.execute("SELECT archive FROM sources WHERE bibkey='x1'").fetchone()[0],
                         "Musee de la Gaspesie")

    def test_the_archive_field_gives_up_its_identifiers_and_its_citation(self):
        self.assertEqual(H.normalise_archive("Internet Archive (CIHM microform 22431)"),
                         ("Internet Archive", "CIHM microform 22431", ""))
        self.assertEqual(H.normalise_archive("Dictionary of Canadian Biography, vol. 10"),
                         ("Dictionary of Canadian Biography", "", "vol. 10"))
        self.assertEqual(H.normalise_archive("Arctic 36(4): 380-381 (Arctic Profiles)"),
                         ("Arctic Institute of North America", "", "36(4): 380-381 (Arctic Profiles)"))
        self.assertEqual(H.normalise_archive("Naval History and Heritage Command, photograph H-2875"),
                         ("Naval History and Heritage Command", "photograph H-2875", ""))
        self.assertEqual(H.normalise_archive("Royal Museums Greenwich, via Wikimedia Commons"),
                         ("Royal Museums Greenwich", "", "via Wikimedia Commons"))
        # an institution whose own name has a comma or a translation in it is left alone
        for whole in ("Nasjonalbiblioteket (National Library of Norway)",
                      "Library of Congress, Prints and Photographs Division",
                      "Bodleian Libraries, University of Oxford"):
            self.assertEqual(H.normalise_archive(whole), (whole, "", ""))

    def test_check_flags_a_legacy_archive_and_notes_the_ones_used_once(self):
        H.add_source(self.c, "legacy", "A paper", licence="open-access", url="https://example.invalid/a",
                     archive="ARCTIC journal", entry_type="article", container="Arctic")
        self.c.execute("UPDATE sources SET archive='ARCTIC journal' WHERE bibkey='legacy'")
        v = H.validate(self.c)
        self.assertTrue(any("is a variant of 'Arctic Institute of North America'" in p["detail"]
                            for p in v["problems"]))
        self.assertTrue(any(n["kind"] == "archive" and "one source only" in n["detail"] for n in v["notes"]))
        self.assertFalse(any(n["kind"] == "archive" for n in v["problems"]))

    def test_entry_type_is_one_of_ours_and_a_bibtex_synonym_lands_on_it(self):
        self.assertEqual(H.entry_type_code("techreport"), "report")
        self.assertEqual(H.entry_type_code("PhDThesis"), "thesis")
        self.assertEqual(H.entry_type_code("inbook"), "incollection")
        self.assertEqual(H.entry_type_code(""), "misc")
        with self.assertRaises(ValueError):
            H.add_source(self.c, "y1", "Y", entry_type="chapter")
        H.import_bib(self.c, "@techreport{dreo1971winter, title = {Winter ice reconnaissance},"
                             " year = {1971}, institution = {Defence Research Establishment Ottawa},"
                             " library = {Publications du gouvernement du Canada}}")
        r = self.c.execute("SELECT * FROM sources WHERE bibkey='dreo1971winter'").fetchone()
        self.assertEqual(r["entry_type"], "report")
        self.assertEqual(r["archive"], "Government of Canada Publications")

    def test_the_container_is_a_journal_for_an_article_and_a_book_for_a_chapter(self):
        H.add_source(self.c, "a1", "A paper", entry_type="article", container="Polar Record",
                     licence="open-access", url="https://example.invalid/1")
        H.add_source(self.c, "a2", "A chapter", entry_type="incollection", container="A big book",
                     licence="open-access", url="https://example.invalid/2")
        H.add_source(self.c, "a3", "A story", entry_type="online", container="Nunatsiaq News",
                     licence="fair-dealing", url="https://example.invalid/3")
        text = H.to_bibtex(self.c.execute("SELECT * FROM sources WHERE bibkey IN ('a1','a2','a3') ORDER BY bibkey"))
        self.assertIn("journal = {Polar Record}", text)
        self.assertIn("booktitle = {A big book}", text)
        self.assertIn("journal = {Nunatsiaq News}", text)

    def test_the_migration_reads_the_type_off_a_row(self):
        import importlib.util
        path = Path(__file__).resolve().parents[1] / "tools" / "migrations" / "normalise_sources.py"
        spec = importlib.util.spec_from_file_location("normalise_sources", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        row = dict(title="", container="", publisher="", url="", volume="", note="", archive="", year="")

        def kind(**kw):
            return mod.infer_entry_type(dict(row, **kw))[0]
        self.assertEqual(kind(container="Arctic", volume="36(4)", title="Penny"), "article")
        self.assertEqual(kind(container="Report of the Fifth Thule Expedition 1921-24, Vol. V",
                              title="The Caribou Eskimos"), "incollection")
        self.assertEqual(kind(publisher="King's Printer", year="1927",
                              title="Report of the Royal Canadian Mounted Police"), "report")
        self.assertEqual(kind(publisher="John Murray", year="1859", title="The Voyage of the Fox"), "book")
        self.assertEqual(kind(publisher="Nunatsiaq News", url="https://nunatsiaq.com/stories/article/x",
                              title="Taissumani"), "online")
        self.assertEqual(kind(url="https://biographi.ca/en/bio/penny_william_12E.html", title="PENNY, WILLIAM"),
                         "incollection")
        # an artwork, and a paper whose journal is in the wrong column, are left for a person
        self.assertIsNone(kind(title="Sir Martin Frobisher (oil on canvas)"))
        self.assertIsNone(kind(publisher="American Association for the Advancement of Science",
                               url="https://archive.org/details/jstor-1638239", title="The Crocker Land Expedition"))

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
        self.assertNotIn("Royal Museums Greenwich", gen["html"])   # the credit is a row field, not body text
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


    def test_bc_dates_sort_in_calendar_order(self):
        for d, label in (("1850", "ad"), ("-1900", "late"), ("-2500", "early")):
            H.add_date(self.c, "event", label, d, role="point", label=label, topic="thule-dorset")
        order = [r["label"] for r in self.c.execute(
            f"SELECT label FROM dates WHERE topic='thule-dorset' ORDER BY {H.date_order('date')}")]
        self.assertEqual(order, ["early", "late", "ad"])

    def test_forget_source_refuses_while_cited(self):
        H.add_source(self.c, "stray2003", "A stray entry", year="2003")
        self.artifact(id="cites-stray", bibkey="stray2003")
        with self.assertRaises(ValueError):
            H.forget(self.c, "source", "stray2003")
        H.add_source(self.c, "orphan2003", "An orphan entry", year="2003")
        self.assertEqual(H.forget(self.c, "source", "orphan2003")["deleted"], "source orphan2003")


    def test_small_real_image_is_not_suspicious(self):
        import tempfile
        d = Path(tempfile.mkdtemp())
        (d / "a.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        (d / "b.png").write_bytes(b"<html>login</html>")
        self.assertTrue(H._small_real_image(d / "a.png"))
        self.assertFalse(H._small_real_image(d / "b.png"))


    def test_setting_topic_status_keeps_title_and_summary(self):
        H.add_topic(self.c, "qei-test", "A test topic", summary="What it covers.")
        H.add_topic(self.c, "qei-test", status="drafted")
        r = self.c.execute("SELECT title, summary, status FROM topics WHERE slug='qei-test'").fetchone()
        self.assertEqual((r["title"], r["summary"], r["status"]), ("A test topic", "What it covers.", "drafted"))
        with self.assertRaises(ValueError):
            H.add_topic(self.c, "brand-new", status="open")


    def test_request_text_turns_literal_backslash_n_into_newlines(self):
        rid = H.add_request(self.c, "franklin-1845", "access", "A title\\nwith a break", url="https://example.org/x",
                            why="Line one of a reason that is long enough to pass the guard.\\nLine two, also long enough to count.")
        r = self.c.execute("SELECT what, why FROM requests WHERE id=?", (rid,)).fetchone()
        self.assertEqual(r["what"], "A title\nwith a break")        # short first line: the break stays
        self.assertNotIn("\\n", r["why"])
        self.assertNotIn("\n", r["why"])                            # two wrapped prose lines become one


    def test_hard_wrapped_request_text_is_unwrapped_but_structure_kept(self):
        raw = ("The single most important document this topic still lacks. Inspector Joy's\n"
               "1929 sledge patrol - Dundas Harbour on Devon Island to Winter Harbour on\n"
               "Melville Island - is described only in the annual report.\n"
               "\n"
               "FORWARD TO: reproduction@example.org\n"
               "Subject: Reference question - Joy's patrol\n"
               "\n"
               "Dear Reference Services,\n"
               "I am writing about the report for the year ended 30 September 1929, which\n"
               "is not online anywhere I can reach.\n"
               "- pages 62-71, the patrol report\n"
               "- the sketch map that accompanies it\n"
               "https://example.org/report-1929\n")
        out = H.unwrap_hard_wraps(raw)
        paras = out.split("\n\n")
        self.assertEqual(len(paras), 3)
        self.assertNotIn("\n", paras[0])                        # the wrapped prose is one line
        self.assertEqual(paras[1].split("\n"), ["FORWARD TO: reproduction@example.org",
                                                 "Subject: Reference question - Joy's patrol"])
        lines = paras[2].split("\n")
        self.assertEqual(lines[0], "Dear Reference Services,")   # short salutation kept
        self.assertTrue(lines[1].startswith("I am writing") and lines[1].endswith("can reach."))
        self.assertEqual(lines[2:], ["- pages 62-71, the patrol report", "- the sketch map that accompanies it",
                                     "https://example.org/report-1929"])


    def test_faces_keywords_and_ontology_round_trip(self):
        self.artifact(id="crew-photo", type="image", people="James Mutch", local_file="x/files/crew.jpg")
        H.add_person(self.c, "James Mutch", role="whaling agent")
        H.add_face(self.c, "crew-photo", 1, "x/files/faces/crew-photo-1.jpg", box=[1, 2, 30, 30],
                   person="James Mutch", confidence=0.9, method="yunet; single-name")
        H.add_face(self.c, "crew-photo", 1, "x/files/faces/crew-photo-1.jpg", box=[1, 2, 31, 31])   # re-run replaces
        self.assertEqual(self.c.execute("SELECT COUNT(*) FROM faces").fetchone()[0], 1)
        with self.assertRaises(ValueError):
            H.add_face(self.c, "crew-photo", 2, "x/files/faces/crew-photo-2.jpg", person="Nobody Known")
        H.add_keywords(self.c, "crew-photo", ["Ships & boats > Whalers > Dundee fleet", "Ice > Besetment"], source="llm:test")
        H.add_keywords(self.c, "crew-photo", ["People & portraits > Crews"], source="crew")
        self.assertEqual(H.artifact_keywords(self.c, "crew-photo")[0], "People & portraits > Crews")
        H.add_keywords(self.c, "crew-photo", ["Ice > Besetment"], source="llm:test")             # replace drops the old
        self.assertEqual(H.artifact_keywords(self.c, "crew-photo"), ["People & portraits > Crews", "Ice > Besetment"])
        H.set_ontology(self.c, {"Ice": {"Besetment": []}}, model="test")
        self.assertEqual(H.get_ontology(self.c)["tree"], {"Ice": {"Besetment": []}})

    def test_check_wants_a_raster_for_a_map_in_a_pdf(self):
        self.artifact(id="chart-pdf", type="map", local_file="x/files/chart.pdf")
        self.assertTrue(any(p["what"] == "chart-pdf" and "raster" in p["detail"] for p in H.validate(self.c)["problems"]))
        self.artifact(id="chart-pdf", type="map", local_file="x/files/chart.pdf", view_file="x/files/chart-view.png")
        self.assertFalse(any(p["what"] == "chart-pdf" and "raster" in p["detail"] for p in H.validate(self.c)["problems"]))


    def test_animals_and_vessels_are_first_class(self):
        H.add_animal(self.c, "Mike", kind="dog", role="Natkusiak's dog on the 1916 ice journey", topic="karluk-cae")
        H.add_vessel(self.c, "HMS Investigator", kind="barque", built="1848, Greenock", lost="abandoned in Mercy Bay, 1853",
                     also="Investigator", topic="mcclure-investigator")
        H.add_vessel(self.c, "HMS Investigator", role="McClure's ship", topic="franklin-search")   # foreign run: fills blanks only
        r = self.c.execute("SELECT topic, role, kind FROM vessels WHERE name='HMS Investigator'").fetchone()
        self.assertEqual((r["topic"], r["role"], r["kind"]), ("mcclure-investigator", "McClure's ship", "barque"))
        idx = H.index_targets(self.c)
        self.assertEqual(idx["idx"][("vessel", "investigator")], "vessel/hms-investigator")
        self.assertEqual(idx["idx"][("animal", "mike")], "animal/mike")
        kinds = {p["kind"] for p in H.generated_pages(self.c)}
        self.assertTrue({"animal", "vessel"} <= kinds)
        self.artifact(id="dog-photo", type="image", local_file="x/files/dog.jpg")
        H.add_face(self.c, "dog-photo", 1, "x/files/faces/dog-photo-1.jpg", kind="animal", person="Mike")
        with self.assertRaises(ValueError):
            H.add_face(self.c, "dog-photo", 2, "x/files/faces/dog-photo-2.jpg", kind="vessel", person="Mike")
        self.assertEqual(self.c.execute("SELECT kind, person FROM faces WHERE n=1").fetchone()[1], "Mike")

    def test_a_vessels_kind_is_a_code_and_the_detail_lives_in_the_kind_note(self):
        with self.assertRaises(ValueError):
            H.add_vessel(self.c, "HMS Resolute", kind="barque, purchased into the Navy")
        with self.assertRaises(ValueError):
            H.add_vessel(self.c, "USS Seadragon", kind="nuclear submarine")
        H.add_vessel(self.c, "USCGC Northwind", kind="icebreaker", kind_note="Wind class",
                     affiliation="United States Coast Guard", topic="science-stations")
        r = self.c.execute("SELECT * FROM vessels WHERE name='USCGC Northwind'").fetchone()
        self.assertEqual((r["kind"], r["kind_note"]), ("icebreaker", "Wind class"))
        self.assertEqual(H.vessel_kind_text(r), "icebreaker, Wind class")
        self.assertEqual(H.vessel_body(r), "")
        self.assertEqual(H.vessel_kind_label("umiak"), "umiak, an open skin boat")
        self.assertTrue(H.is_vessel_kind("steam-whaler"))
        self.assertFalse(H.is_vessel_kind("steam whaler"))
        # a legacy free-text row is reported by check, not hidden
        self.c.execute("UPDATE vessels SET kind='icebreaker, Wind class' WHERE name='USCGC Northwind'")
        problems = H.validate(self.c)["problems"]
        self.assertTrue(any(p["what"] == "USCGC Northwind" and "not a code" in p["detail"] for p in problems))


if __name__ == "__main__":
    unittest.main()


class NatureTests(unittest.TestCase):
    """The natural half: subjects, observations, the journal, the publish."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.c = H.connect(self.root / "history.sqlite")
        self.addCleanup(self.c.close)
        H.add_topic(self.c, "muskox-and-caribou", "Muskox and caribou", domain="nature")
        H.add_source(self.c, "sverdrup1904new", "New Land", author="Sverdrup", year="1904",
                     url="https://example.invalid/newland", licence="public-domain", primary=True, entry_type="book")
        H.add_subject(self.c, "Bovidae", kind="taxon", domain="biology", rank="family", backbone_id="gbif:9614",
                      topic="muskox-and-caribou")
        H.add_subject(self.c, "Ovibos moschatus", kind="taxon", domain="biology", rank="species", parent="Bovidae",
                      english="muskox", french="boeuf musqué", inuktitut="umingmak", also="musk-ox; musk ox",
                      backbone_id="gbif:2441090", topic="muskox-and-caribou", bibkey="sverdrup1904new",
                      note="The muskox is the archipelago's one large grazer.")
        H.add_subject(self.c, "air temperature", kind="weather", domain="meteorology", unit="C",
                      note="The air temperature as the expeditions read it.", topic="muskox-and-caribou")
        H.add_place(self.c, "Eureka", lat=79.99, lon=-85.94, kind="weather-station")

    def obs(self, ident="muskox-and-caribou-001", **kw):
        base = dict(date="1900-04-13", lat=78.6, lon=-95.2, count="a herd of 17", method="hunt",
                    observer="Otto Sverdrup", bibkey="sverdrup1904new", pages="v. 1 p. 412",
                    detail="Sverdrup's party shot four of a herd of seventeen muskoxen.")
        base.update(kw)
        subject = base.pop("subject", "muskox")
        return H.add_observation(self.c, ident, "muskox-and-caribou", subject, **base)

    def test_topic_domain_is_a_code(self):
        self.assertEqual(self.c.execute("SELECT domain FROM topics").fetchone()["domain"], "nature")
        with self.assertRaises(ValueError):
            H.add_topic(self.c, "x", "X", domain="science")
        H.add_topic(self.c, "franklin-1845", "Franklin")
        self.assertEqual(self.c.execute("SELECT domain FROM topics WHERE slug='franklin-1845'").fetchone()["domain"], "history")

    def test_subject_kind_and_domain_are_codes(self):
        with self.assertRaises(ValueError):
            H.add_subject(self.c, "aurora", kind="light", domain="astronomy")
        with self.assertRaises(ValueError):
            H.add_subject(self.c, "aurora", kind="sky", domain="skies")
        H.add_subject(self.c, "aurora", kind="sky", domain="astronomy", note="The northern lights.")
        # a re-run without kind keeps the kind
        H.add_subject(self.c, "aurora", english="northern lights")
        r = self.c.execute("SELECT kind, english FROM subjects WHERE name='aurora'").fetchone()
        self.assertEqual((r["kind"], r["english"]), ("sky", "northern lights"))

    def test_any_name_resolves(self):
        for name in ("Ovibos moschatus", "ovibos moschatus", "muskox", "umingmak", "musk ox", "Musk-ox", "boeuf musqué"):
            self.assertEqual(H.resolve_subject(self.c, name), "Ovibos moschatus", name)
        self.assertEqual(H.resolve_subject(self.c, "narwhal"), "")
        self.assertEqual(self.c.execute("SELECT parent FROM subjects WHERE name='Ovibos moschatus'").fetchone()["parent"], "Bovidae")

    def test_observation_is_refused_without_its_parts(self):
        with self.assertRaises(ValueError):
            self.obs(subject="narwhal")
        with self.assertRaises(ValueError):
            self.obs(bibkey="")
        with self.assertRaises(ValueError):
            self.obs(date="spring")
        with self.assertRaises(ValueError):
            self.obs(lat=None, lon=None)
        with self.assertRaises(ValueError):
            self.obs(lat=None, lon=None, place="Nowhere")
        with self.assertRaises(ValueError):
            self.obs(detail="")
        with self.assertRaises(ValueError):
            self.obs(method="guess")
        with self.assertRaises(ValueError):
            self.obs(confidence="sure")
        # a variable wants its number and unit as written
        with self.assertRaises(ValueError):
            self.obs(subject="air temperature", count="")
        with self.assertRaises(ValueError):
            self.obs(subject="air temperature", value=-58.5)
        self.obs(subject="air temperature", value=-58.5, unit="F", method="instrument", count="")
        r = self.c.execute("SELECT value, unit FROM observations").fetchone()
        self.assertEqual((r["value"], r["unit"]), (-58.5, "F"))

    def test_a_place_supplies_the_position_and_the_timeline_gets_a_row(self):
        self.obs(lat=None, lon=None, place="Eureka", subject="air temperature", value=-40, unit="C",
                 method="station-record", count="", qualifier="coldest of the winter")
        r = self.c.execute("SELECT lat, lon, subject FROM observations").fetchone()
        self.assertAlmostEqual(r["lat"], 79.99)
        self.assertEqual(r["subject"], "air temperature")
        d = self.c.execute("SELECT * FROM dates WHERE entity_kind='observation'").fetchone()
        self.assertEqual(d["date"], "1900-04-13")
        self.assertEqual(d["label"], "air temperature, -40 C, coldest of the winter")
        self.assertEqual(d["place"], "Eureka")
        # re-dating replaces the timeline row
        self.obs(lat=None, lon=None, place="Eureka", subject="air temperature", value=-40, unit="C",
                 method="station-record", count="", qualifier="coldest of the winter", date="1901-02-04")
        rows = self.c.execute("SELECT date FROM dates WHERE entity_kind='observation'").fetchall()
        self.assertEqual([r["date"] for r in rows], ["1901-02-04"])

    def test_forget_guards_a_subject_with_a_record(self):
        self.obs()
        with self.assertRaises(ValueError):
            H.forget(self.c, "subject", "Ovibos moschatus")
        r = H.forget(self.c, "observation", "muskox-and-caribou-001")
        self.assertEqual(r["dates"], 1)
        H.forget(self.c, "subject", "Ovibos moschatus")

    def test_check_finds_what_is_wrong(self):
        H.add_subject(self.c, "Rangifer tarandus", kind="taxon", domain="biology", topic="muskox-and-caribou")
        self.obs()
        self.c.execute("UPDATE observations SET subject='Nobody', bibkey='nokey'")
        self.c.commit()
        v = H.validate(self.c)
        whats = {(p["kind"], p["what"], p["detail"][:24]) for p in v["problems"]}
        self.assertIn(("subject", "Rangifer tarandus", "no backbone id (GBIF, Wo"), whats)
        self.assertIn(("observation", "muskox-and-caribou-001", "subject 'Nobody' is no s"), whats)
        self.assertIn(("observation", "muskox-and-caribou-001", "bibkey nokey is in no so"), whats)
        self.assertEqual(v["stats"]["subjects"], 4)
        self.assertEqual(v["stats"]["observations"], 1)

    def test_links_resolve_subjects_by_any_name_and_mentions_by_proper_name(self):
        H.add_page(self.c, "muskox-overview", "The muskox", "Sverdrup fed his dogs on [[subject:umingmak]]; "
                   "the herds of Ovibos moschatus and the air temperature. [[subject:muskox|the beast]]",
                   topic="muskox-and-caribou")
        info = H.reindex_links(self.c)
        self.assertEqual(info["wanted"], {})
        rows = self.c.execute("SELECT kind, name, target FROM links WHERE src='muskox-overview' ORDER BY name").fetchall()
        targets = {(r["kind"], r["name"]): r["target"] for r in rows}
        self.assertEqual(targets[("subject", "umingmak")], "subject/ovibos-moschatus")
        self.assertEqual(targets[("subject", "muskox")], "subject/ovibos-moschatus")
        self.assertNotIn(("subject", "air temperature"), targets)   # a bare common noun does not auto-link
        # the observation ties the subject page to its observer and source
        H.add_person(self.c, "Otto Sverdrup", role="leader")
        self.obs()
        H.reindex_links(self.c)
        back = {r["kind"] + ":" + r["name"] for r in self.c.execute(
            "SELECT kind, name FROM links WHERE src='subject/ovibos-moschatus'")}
        self.assertIn("person:Otto Sverdrup", back)
        self.assertIn("source:sverdrup1904new", back)

    def test_journal_photographs_resolve_beside_the_journal(self):
        inc = self.root / "_journal" / "incoming"
        (inc / "img").mkdir(parents=True)
        (inc / "img" / "2026-09-11-007.jpg").write_bytes(b"\xff\xd8\xff" + b"0" * 5000)
        j = inc / "2026-09.jsonl"
        j.write_text("\n".join([
            json.dumps({"id": "amundsen-2026-09-11-007", "subject": "muskox", "date": "2026-09-11",
                        "lat": 76.1, "lon": -92.4, "count": "2", "method": "camera", "observer": "A. Crew",
                        "detail": "Two on the beach.", "artifact_file": "_journal/img/2026-09-11-007.jpg"}),
            json.dumps({"id": "amundsen-2026-09-11-008", "subject": "muskox", "date": "2026-09-11",
                        "lat": 76.1, "lon": -92.4, "count": "1", "method": "camera", "observer": "A. Crew",
                        "detail": "No picture.", "artifact_file": "_journal/img/missing.jpg"}),
        ]) + "\n")
        old = H.HISTORY_DIR
        H.HISTORY_DIR = self.root
        try:
            r = H.ingest_journal(self.c, j)
        finally:
            H.HISTORY_DIR = old
        self.assertEqual(len(r["done"]), 1)
        self.assertEqual(len(r["failed"]), 1)
        self.assertIn("not found beside the journal", r["failed"][0]["error"])
        a = self.c.execute("SELECT local_file, credit FROM artifacts WHERE id='amundsen-2026-09-11-007-img'").fetchone()
        self.assertEqual(a["local_file"], "_journal/incoming/img/2026-09-11-007.jpg")
        self.assertIn("A. Crew", a["credit"])
        self.assertEqual(self.c.execute("SELECT artifact_id FROM observations WHERE id='amundsen-2026-09-11-007'").fetchone()["artifact_id"],
                         "amundsen-2026-09-11-007-img")

    def test_journal_ingest_is_idempotent_and_reports_failures(self):
        j = self.root / "journal.jsonl"
        j.write_text("\n".join([
            json.dumps({"kind": "observation", "id": "amundsen-2026-09-11-003", "subject": "muskox",
                        "date": "2026-09-11", "lat": 76.104, "lon": -92.41, "count": "3", "method": "sighting",
                        "observer": "the bridge watch", "vessel": "CCGS Amundsen",
                        "detail": "Three muskoxen on the shore off the port bow."}),
            json.dumps({"kind": "observation", "id": "amundsen-2026-09-11-004", "subject": "narwhal",
                        "date": "2026-09-11", "lat": 76.2, "lon": -92.6, "detail": "no such subject"}),
            json.dumps({"kind": "observation", "id": "amundsen-2026-09-11-005", "subject": "Ovibos moschatus",
                        "date": "2026-09-12", "lat": 76.3, "lon": -92.7, "sensitive": 1, "method": "sighting",
                        "detail": "A cow with a calf, bedded down.", "place": "Eureka"}),
        ]) + "\n")
        r = H.ingest_journal(self.c, j)
        self.assertEqual(len(r["done"]), 2)
        self.assertEqual(len(r["failed"]), 1)
        self.assertIn("narwhal", r["failed"][0]["error"])
        row = self.c.execute("SELECT topic, origin, bibkey FROM observations WHERE id='amundsen-2026-09-11-003'").fetchone()
        self.assertEqual((row["topic"], row["origin"], row["bibkey"]), ("ship-journal", "ship", "amundsenjournal"))
        self.assertTrue(self.c.execute("SELECT 1 FROM sources WHERE bibkey='amundsenjournal'").fetchone())
        # a corrected line replaces the row
        j.write_text(json.dumps({"kind": "observation", "id": "amundsen-2026-09-11-003", "subject": "muskox",
                                 "date": "2026-09-11", "lat": 76.104, "lon": -92.41, "count": "4", "method": "sighting",
                                 "observer": "the bridge watch", "detail": "Four, on a second look."}) + "\n")
        H.ingest_journal(self.c, j)
        self.assertEqual(self.c.execute("SELECT COUNT(*) AS n FROM observations").fetchone()["n"], 2)
        self.assertEqual(self.c.execute("SELECT count FROM observations WHERE id='amundsen-2026-09-11-003'").fetchone()["count"], "4")
        # the sensitive one publishes coarsened, with its place blank
        out = self.root / "pub"
        m = H.publish(out, self.root / "history.sqlite")
        self.assertEqual(m["observations"], 2)
        self.assertEqual(m["subjects"], 3)
        pub = json.loads((out / "data/history/observations.json").read_text())["observations"]
        sens = [o for o in pub if o["id"] == "amundsen-2026-09-11-005"][0]
        self.assertEqual((sens["lat"], sens["lon"], sens["place"]), (76.5, -92.5, ""))
        self.assertEqual(sens["domain"], "biology")
        full = self.c.execute("SELECT lat, place FROM observations WHERE id='amundsen-2026-09-11-005'").fetchone()
        self.assertEqual((full["lat"], full["place"]), (76.3, "Eureka"))
        subs = json.loads((out / "data/history/subjects.json").read_text())["subjects"]
        musk = [s for s in subs if s["name"] == "Ovibos moschatus"][0]
        self.assertEqual(musk["observations"], 2)
        self.assertEqual(musk["page"], "subject/ovibos-moschatus")
        bov = [s for s in subs if s["name"] == "Bovidae"][0]
        self.assertEqual(bov["children"], ["Ovibos moschatus"])
        page = json.loads((out / "data/history/pages/subject__ovibos-moschatus.json").read_text())
        self.assertEqual(page["kind"], "subject")
        self.assertIn("one large grazer", page["html"])
        excerpt = (out / "data/history/excerpts/subject__ovibos-moschatus.txt").read_text()
        self.assertIn("## The record", excerpt)
        self.assertIn("2026-09-11: Ovibos moschatus, 4", excerpt)
        self.assertNotIn("Eureka", excerpt)     # the sensitive row's place stays on grid
        topics = json.loads((out / "data/history/index.json").read_text())["topics"]
        self.assertEqual({t["slug"]: t["domain"] for t in topics}["muskox-and-caribou"], "nature")
        timeline = json.loads((out / "data/history/timeline.json").read_text())["timeline"]
        kinds = {t["entity_kind"] for t in timeline}
        self.assertIn("observation", kinds)
        # an artifact carries its topic's domain and the natural domains of the
        # observations it is evidence for
        H.add_source(self.c, "amundsenjournal", "journal", url="x", licence="attribution", entry_type="dataset")
        H.add_artifact(self.c, "muskox-and-caribou-001", "muskox-and-caribou", "image", "a muskox", credit="c",
                       bibkey="sverdrup1904new", licence="public-domain", lat=78.6, lon=-95.2, tags="ovibos-moschatus")
        self.obs(artifact_id="muskox-and-caribou-001")
        H.publish(out, self.root / "history.sqlite")
        arts = {a["id"]: a for a in json.loads((out / "data/history/artifacts.json").read_text())["artifacts"]}
        self.assertEqual(arts["muskox-and-caribou-001"]["domain"], "nature")
        self.assertEqual(arts["muskox-and-caribou-001"]["domains"], ["biology"])
