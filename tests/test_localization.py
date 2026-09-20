"""Reviewed wiki publishing, fallbacks and stable scientific identifiers."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import arctic_history as H
from arctic_history.localization import sha


class LocalizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'history.sqlite'
        c = H.connect(self.source)
        H.add_topic(c, 'voyage', 'The voyage')
        H.add_source(c, 'archive', 'Test archive', author='Test author', year='1900', licence='public-domain')
        H.add_page(c, 'intro', 'Introduction', 'See [[A plate]].', topic='voyage')
        H.add_artifact(c, 'plate', 'voyage', 'image', 'A plate', description='The ice.', credit='Test archive', bibkey='archive', licence='public-domain', lat=74.2, lon=-80.1)
        c.close()
        self.store = self.root / 'translations.sqlite'
        self.c = sqlite3.connect(self.store)
        self.addCleanup(self.c.close)
        self.c.executescript('''
            CREATE TABLE locale_defaults(target_locale TEXT, profile_id TEXT);
            CREATE TABLE field_selections(target_locale TEXT, source_key TEXT, candidate_id TEXT);
            CREATE TABLE candidates(candidate_id TEXT, profile_id TEXT, target_locale TEXT,
                source_key TEXT,table_name TEXT,record_id TEXT,field_name TEXT,source_text TEXT,
                source_sha256 TEXT,translated_text TEXT,attempt INTEGER,created_at TEXT,
                validation_status TEXT,review_status TEXT,reviewer TEXT);
            INSERT INTO locale_defaults VALUES ('fr-CA','gemma');
        ''')
        self.env = patch.dict(os.environ, {'ARCTIC_HISTORY_TRANSLATIONS': str(self.store)})
        self.env.start(); self.addCleanup(self.env.stop)
        self.web = self.root / 'web'

    def candidate(self, ident='title', table='pages', record='intro', field='title', source='Introduction',
                  translated='Présentation', status='approved', validation='valid', profile='gemma'):
        key = f'{table}:{record}:{field}'
        self.c.execute('INSERT INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (ident, profile, 'fr-CA', key, table, record, field, source, sha(source),
                        translated, 1, '2026-09-19', validation, status, 'editor'))
        self.c.commit()

    def read(self, entry, file):
        return json.loads((self.web / entry['locales']['fr-CA']['base'] / file).read_text())

    def test_unreviewed_not_advertised_and_source_untouched(self):
        self.candidate(status='unreviewed')
        before = self.source.read_bytes()
        result = H.publish(self.web, self.source)
        self.assertNotIn('locales', result)
        self.assertEqual(before, self.source.read_bytes())
        self.assertEqual(json.loads((self.web/'data/history/pages/intro.json').read_text())['title'], 'Introduction')

    def test_generated_pages_indexes_links_and_coordinates(self):
        self.candidate()
        self.candidate('plate-title', 'artifacts', 'plate', 'title', 'A plate', 'Une planche')
        self.candidate('plate-body', 'artifacts', 'plate', 'description', 'The ice.', 'La glace.')
        result = H.publish(self.web, self.source)
        index = self.read(result, 'index.json')
        self.assertEqual(next(p['title'] for p in index['pages'] if p['slug']=='intro'), 'Présentation')
        self.assertIn('artifact/plate', self.read(result, 'pages/intro.json')['html'])
        page = self.read(result, 'pages/artifact__plate.json')
        self.assertEqual(page['title'], 'Une planche'); self.assertIn('La glace.', page['html'])
        self.assertIn('intro', page['backlinks'])
        art = self.read(result, 'artifacts.json')['artifacts'][0]
        self.assertEqual((art['id'],art['lat'],art['lon']), ('plate',74.2,-80.1))
        repeat = H.publish(self.web, self.source)
        self.assertEqual(result['locales'], repeat['locales'])

    def test_stale_and_rejected_pinned_candidates_fall_back(self):
        self.candidate()
        self.candidate('stale', 'artifacts', 'plate', 'description', 'Old ice.', 'Ancienne glace.')
        self.candidate('bad-pin', profile='other', status='rejected')
        self.c.execute("INSERT INTO field_selections VALUES ('fr-CA','pages:intro:title','bad-pin')")
        self.c.commit()
        self.assertNotIn('locales', H.publish(self.web, self.source))

    def test_field_override_revision_and_revocation(self):
        self.candidate()
        first = H.publish(self.web, self.source)
        self.candidate('other', profile='other', translated='Introduction française')
        self.c.execute("INSERT INTO field_selections VALUES ('fr-CA','pages:intro:title','other')")
        self.c.commit()
        second = H.publish(self.web, self.source)
        self.assertNotEqual(first['locales'], second['locales'])
        self.assertEqual(self.read(second,'pages/intro.json')['title'], 'Introduction française')
        self.c.execute("UPDATE candidates SET review_status='rejected'"); self.c.commit()
        self.assertNotIn('locales', H.publish(self.web, self.source))

    def test_machine_fields_and_invalid_translations_are_not_published(self):
        self.candidate(field='slug', source='intro', translated='nouveau')
        self.candidate('invalid', validation='invalid')
        self.assertNotIn('locales', H.publish(self.web, self.source))

    def test_missing_store_remains_english(self):
        with patch.dict(os.environ, {'ARCTIC_HISTORY_TRANSLATIONS': str(self.root/'absent.sqlite')}):
            self.assertNotIn('locales', H.publish(self.web, self.source))

    def test_review_cli_and_reviewed_only_release(self):
        self.candidate(status='unreviewed')
        self.candidate('other', profile='other', status='unreviewed')
        self.c.executescript('''
            ALTER TABLE candidates ADD COLUMN review_note TEXT DEFAULT '';
            ALTER TABLE candidates ADD COLUMN run_id TEXT DEFAULT 'run';
            CREATE TABLE runs(run_id TEXT);
            INSERT INTO runs VALUES ('run');
            CREATE TABLE source_fields(source_key TEXT);
            INSERT INTO source_fields VALUES ('private-source');
        ''')
        cli = Path(H.__file__).resolve().parents[1] / 'tools/history-translations.py'
        def run(*args):
            return subprocess.run([sys.executable,str(cli),'--store',str(self.store),*args],check=True,capture_output=True,text=True)
        run('review','title','--status','approved','--reviewer','editor','--note','Compared with source')
        destination = self.root/'release.sqlite'
        run('release',str(destination))
        released = sqlite3.connect(destination)
        try:
            self.assertEqual(released.execute('SELECT candidate_id FROM candidates').fetchall(), [('title',)])
            self.assertEqual(released.execute('SELECT count(*) FROM source_fields').fetchone()[0], 0)
        finally:
            released.close()
        self.assertEqual(self.c.execute('SELECT count(*) FROM candidates').fetchone()[0],2)
        run('review','title','--status','rejected','--reviewer','editor','--note','Withdrawn after recheck')
        run('release',str(destination))
        with sqlite3.connect(destination) as released:
            self.assertEqual(released.execute('SELECT count(*) FROM candidates').fetchone()[0],0)


if __name__ == '__main__':
    unittest.main()
