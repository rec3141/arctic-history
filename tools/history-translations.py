#!/usr/bin/env python3
"""Explicit review, translator selection and reviewed-only release snapshots."""
import argparse
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from arctic_history.localization import snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    review = sub.add_parser('review')
    review.add_argument('candidate_id', nargs='+')
    review.add_argument('--status', choices=['approved', 'rejected', 'unreviewed'], required=True)
    review.add_argument('--reviewer', required=True)
    review.add_argument('--note', required=True)
    default = sub.add_parser('default')
    default.add_argument('locale'); default.add_argument('profile')
    select = sub.add_parser('select')
    select.add_argument('locale'); select.add_argument('candidate_id')
    release = sub.add_parser('release')
    release.add_argument('destination', type=Path)
    args = parser.parse_args()
    if not args.store.is_file():
        parser.error('store must already exist; initialize it with the translation pipeline')
    if args.command == 'release':
        if args.store.resolve() == args.destination.resolve():
            parser.error('release must not replace the working translation store')
        args.destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.translation-release-', dir=args.destination.parent) as directory:
            staged = Path(directory) / 'translations.sqlite'
            snapshot(args.store, staged)
            conn = sqlite3.connect(staged)
            try:
                ineligible = "(review_status<>'approved' OR validation_status<>'valid' OR trim(reviewer)='' OR translated_text IS NULL OR trim(translated_text)='')"
                conn.execute('DELETE FROM candidates WHERE ' + ineligible + ' AND candidate_id NOT IN (SELECT candidate_id FROM field_selections)')
                # Preserve explicit pin metadata (and referential integrity),
                # never the unapproved translation. Removing the pin would
                # wrongly allow a default translator to take its place.
                conn.execute('UPDATE candidates SET translated_text=NULL WHERE ' + ineligible)
                conn.execute('DELETE FROM source_fields')
                conn.execute('DELETE FROM runs WHERE run_id NOT IN (SELECT run_id FROM candidates)')
                conn.commit()
                conn.execute('PRAGMA journal_mode=DELETE')
                conn.execute('VACUUM')
                count = conn.execute('SELECT count(*) FROM candidates WHERE NOT ' + ineligible).fetchone()[0]
            finally:
                conn.close()
            os.replace(staged, args.destination)
        print(f'Released {count} approved candidates to {args.destination}; source hashes are rechecked at publish time')
        return
    conn = sqlite3.connect(args.store, timeout=30)
    conn.row_factory = sqlite3.Row
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    try:
        with conn:
            if args.command == 'review':
                if not args.reviewer.strip() or not args.note.strip():
                    parser.error('reviewer and review note must not be blank')
                for ident in args.candidate_id:
                    row = conn.execute('SELECT * FROM candidates WHERE candidate_id=?', (ident,)).fetchone()
                    if not row:
                        raise ValueError(f'unknown candidate: {ident}')
                    if args.status == 'approved' and (row['validation_status'] != 'valid' or not (row['translated_text'] or '').strip()):
                        raise ValueError(f'cannot approve invalid/empty candidate: {ident}')
                    conn.execute('UPDATE candidates SET review_status=?,reviewer=?,review_note=? WHERE candidate_id=?',
                                 (args.status, args.reviewer, stamp + ': ' + args.note, ident))
            elif args.command == 'default':
                row = conn.execute('SELECT target_locale FROM translator_profiles WHERE profile_id=?', (args.profile,)).fetchone()
                if not row or row[0] != args.locale:
                    raise ValueError('profile must exist and match the locale')
                conn.execute('INSERT OR REPLACE INTO locale_defaults VALUES (?,?,?,?)', (args.locale, args.profile, stamp, 'explicit CLI selection'))
            else:
                row = conn.execute('SELECT target_locale,source_key FROM candidates WHERE candidate_id=?', (args.candidate_id,)).fetchone()
                if not row or row['target_locale'] != args.locale:
                    raise ValueError('candidate must exist and match the locale')
                conn.execute('INSERT OR REPLACE INTO field_selections VALUES (?,?,?,?,?)',
                             (args.locale, row['source_key'], args.candidate_id, stamp, 'explicit CLI selection'))
    finally:
        conn.close()
    print('Updated explicit review/selection policy; nothing published')


if __name__ == '__main__':
    main()
