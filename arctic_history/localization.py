"""Reviewed field overlays for offline wiki exports; never modify source DBs."""
from __future__ import annotations

import hashlib
import json
import logging
import re
import shutil
import sqlite3
import tempfile
from pathlib import Path

log = logging.getLogger(__name__)
VERSION = 'reviewed-overlay-v1'
# Only prose. Machine classifications, names, numbers, dates and lookup keys
# remain authoritative English even if an experimental translator collected them.
FIELDS = {
    'pages': ('slug', ('title', 'summary', 'body')),
    'topics': ('slug', ('title', 'summary')),
    'artifacts': ('id', ('title', 'description')),
    'events': ('id', ('title', 'detail')),
    'people': ('name', ('role', 'affiliation', 'note')),
    'places': ('name', ('note',)),
    'animals': ('name', ('role', 'affiliation', 'note')),
    'vessels': ('name', ('kind_note', 'role', 'affiliation', 'note')),
    'subjects': ('name', ('note',)),
    'sources': ('bibkey', ('note',)),
    'observations': ('id', ('qualifier', 'stage', 'behaviour', 'detail')),
    'dates': ('id', ('label',)),
}


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def readonly(path):
    conn = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True, timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def snapshot(source, destination):
    """SQLite backup includes committed WAL pages, unlike a file copy."""
    src, dst = readonly(source), sqlite3.connect(destination)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()


def selected(store, locale):
    default = store.execute('SELECT profile_id FROM locale_defaults WHERE target_locale=?', (locale,)).fetchone()
    overrides = {r['source_key']: r['candidate_id'] for r in store.execute(
        'SELECT source_key,candidate_id FROM field_selections WHERE target_locale=?', (locale,))}
    # An explicit override is a pin: if invalid/stale/unreviewed, fall back to
    # English, not silently to a different translator or older candidate.
    rows = store.execute('''SELECT * FROM candidates WHERE target_locale=?
        AND (profile_id=? OR candidate_id IN
          (SELECT candidate_id FROM field_selections WHERE target_locale=?))
        ORDER BY attempt DESC, created_at DESC, candidate_id DESC''',
        (locale, default['profile_id'] if default else '', locale))
    chosen = {}
    for row in rows:
        key = row['source_key']
        if key in chosen or (key in overrides and row['candidate_id'] != overrides[key]):
            continue
        # Review older approved attempts only when there is no explicit pin.
        if row['validation_status'] != 'valid' or row['review_status'] != 'approved':
            continue
        if not row['reviewer'].strip() or not row['translated_text'] or not row['translated_text'].strip():
            continue
        chosen[key] = dict(row)
    return chosen


def overlay(db, candidates):
    conn = sqlite3.connect(db)
    accepted, skipped = [], {}
    try:
        for key, row in sorted(candidates.items()):
            table, field, record = row['table_name'], row['field_name'], row['record_id']
            spec = FIELDS.get(table)
            reason = None
            if not spec or field not in spec[1] or key != f'{table}:{record}:{field}':
                reason = 'unsupported_field'
            else:
                source = conn.execute(f'SELECT "{field}" FROM "{table}" WHERE "{spec[0]}"=?', (record,)).fetchone()
                if source is None:
                    reason = 'missing_record'
                elif sha(str(source[0] or '')) != row['source_sha256'] or str(source[0] or '') != row['source_text']:
                    reason = 'stale_source'
            if reason:
                skipped[reason] = skipped.get(reason, 0) + 1
                continue
            conn.execute(f'UPDATE "{table}" SET "{field}"=? WHERE "{spec[0]}"=?', (row['translated_text'], record))
            accepted.append({k: row[k] for k in ('candidate_id', 'profile_id', 'source_key', 'source_sha256')})
        conn.commit()
    finally:
        conn.close()
    return accepted, skipped


def publish_locales(root, source, exporter, store_path):
    if not source.is_file():
        return None
    # Always freeze the source before reindexing/export; the research DB is
    # never rewritten and English/French see the same committed input.
    with tempfile.TemporaryDirectory(prefix='history-publish-') as temp:
        frozen = Path(temp) / 'source.sqlite'
        snapshot(source, frozen)
        english = exporter(root, frozen)
        if not store_path.is_file():
            return english
        store = None
        try:
            store = readonly(store_path)
            store.execute('BEGIN')  # one coherent view of approvals/selections
            locales = [r[0] for r in store.execute('SELECT target_locale FROM locale_defaults UNION SELECT target_locale FROM field_selections')]
            from . import connect, reindex_links, index_targets
            conn = connect(frozen, create=False)
            try:
                context = (reindex_links(conn), index_targets(conn))
            finally:
                conn.close()
            for locale in sorted(locales):
                if not re.fullmatch(r'[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*', locale) or locale == 'en':
                    continue
                localized = Path(temp) / (locale + '.sqlite')
                snapshot(frozen, localized)
                applied, skipped = overlay(localized, selected(store, locale))
                if not applied:
                    continue  # Do not advertise an entirely unreviewed locale.
                output = Path(temp) / locale
                output.mkdir()
                exporter(root, localized, _out=output, _link_context=context)
                provenance = {'locale': locale, 'pipeline': VERSION, 'translated_fields': len(applied),
                              'profiles': sorted({c['profile_id'] for c in applied}), 'candidates': applied,
                              'skipped': skipped, 'fallback': 'en'}
                (output / 'translation.json').write_text(json.dumps(provenance, ensure_ascii=False, sort_keys=True))
                digest = hashlib.sha256()
                for file in sorted(output.rglob('*')):
                    if file.is_file():
                        digest.update(str(file.relative_to(output)).encode()); digest.update(b'\0'); digest.update(file.read_bytes())
                revision = digest.hexdigest()[:24]
                base = root / 'data' / 'history' / 'locales' / locale
                base.mkdir(parents=True, exist_ok=True)
                final = base / revision
                if not final.exists():
                    # Completed immutable tree first, manifest entry afterwards.
                    with tempfile.TemporaryDirectory(prefix='.stage-', dir=base) as stage:
                        prepared = Path(stage) / 'content'
                        shutil.copytree(output, prepared)
                        prepared.rename(final)
                english.setdefault('locales', {})[locale] = {
                    'base': f'data/history/locales/{locale}/{revision}/', 'stamp': revision,
                    'translated_fields': len(applied), 'profiles': provenance['profiles']}
        except Exception as error:
            # Never retain a previously approved locale after a failed review
            # read: approvals may have been revoked. English remains available.
            log.warning('localized wiki unavailable; publishing English: %s', error)
            english.pop('locales', None)
        finally:
            if store is not None:
                store.close()
        return english
