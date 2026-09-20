# Reviewed wiki language variants

The English research database remains authoritative. `publish()` freezes it
using SQLite backup, exports English, and overlays approved prose on separate
temporary copies before exporting each selected locale. It never writes
translated text or rebuilt links into the research database.

## Review and release

The working sidecar is produced by the field translation pipeline. Its
`candidates`, `translator_profiles`, `locale_defaults` and `field_selections`
tables allow concurrent languages and translators. Completing a model batch
does not approve or publish it.

Current release policy: structurally valid output is published, and wording is
corrected from the feedback flags as readers report it. These candidates carry
reviewer `user-authorized-structural-publication-v1`, which records structural
approval rather than a language review. Release snapshots still require approval
metadata and current source hashes, so later batch output is not published
automatically.

Review, select and release with explicit candidate IDs:

```sh
python3 tools/history-translations.py --store /path/to/working/translations.sqlite review CANDIDATE_ID --status approved --reviewer REVIEWER --note 'Review findings'
python3 tools/history-translations.py --store /path/to/working/translations.sqlite default fr-CA PROFILE_ID
python3 tools/history-translations.py --store /path/to/working/translations.sqlite select fr-CA CANDIDATE_ID
python3 tools/history-translations.py --store /path/to/working/translations.sqlite release db/history/translations.sqlite
```

The `select` step is optional: it pins a field to a candidate, overriding the
locale default. A bad, withdrawn or stale pin falls back to English; it does
not quietly select another translator. Defaults choose the newest approved,
structurally valid candidate. The publisher rechecks its exact English source
and SHA-256 against the frozen research database. Missing translations remain
English. Machine kinds, scientific numbers, dates, names, slugs, citations,
URLs, coordinates and record IDs are never overlaid. Generated page boilerplate
and untranslated source fields retain English; this is not an HTML translator.

`release` uses SQLite backup (including committed WAL data), strips unapproved
candidates (retaining only redacted metadata for explicit pins) and source-field staging data, then atomically installs a compact
reviewed-only bundle. The working sidecar remains untouched. An empty release
revokes all locale publication. Set `ARCTIC_HISTORY_TRANSLATIONS` to override
the default `db/history/translations.sqlite` release location. Do not point
production at the actively edited working sidecar.

Revise review status with the same `review` command (`rejected` or `unreviewed`)
and release again to withdraw a candidate. Review notes include the action
timestamp; translation text and older translator profiles are not overwritten.

## Publishing and transport

English URLs remain `data/history/...`. French exports are complete JSON trees
under `data/history/locales/fr-CA/<content-revision>/`; article slugs and media
URLs remain identical. Immutable revision trees are installed before the
manifest advertises them. `history.locales[locale]` contains `base`, `stamp`,
`translated_fields`, and selected `profiles`. Content and selection provenance
both contribute to the revision, so translator replacements refresh caches.
`translation.json` records the chosen candidate IDs/source hashes. Older trees
are retained for rollback; withdrawing them from the manifest is not access
revocation of previously public text.

No locale is advertised until at least one eligible field is available.
Missing/malformed review stores fail closed to English. Provenance narrative
and bibliography downloads remain English/shared, as do user-authored journal
entries. Localized generated links use the original English resolution table
and backlinks, including bare English-title links, so translated titles cannot
break existing references.

Deploy code in both arctic-history and underway aboard. Then the normal
`tools/history-sync.sh pull` transfers a SQLite snapshot of the reviewed release
as well as the research database. The translation database is exempt from the
media size limit. No raw active WAL files are copied. If no release exists on
grid, an existing ship installation is retained; send an empty release to
disable it explicitly. After a pull, the normal dashboard build publishes
available locale trees and their manifest entries. French assets must arrive
before the updated manifest, as with the existing data publication sequence.

Checks: `python3 -m unittest discover -s tests -p test_localization.py` and
`python3 -m unittest discover -s tests -p test_history.py`. These exercise review
gates, stale/pinned fallback, immutable English, generated content, links,
coordinates, revision changes, revocation and reviewed-only release snapshots.
