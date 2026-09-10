"""Tags to the canonical form: one per element, lowercase, hyphenated, singular.

Reads every tag on artifacts and events, puts it through the library's
normaliser (shape, then the TAG_ALIASES table), and reports every tag that
changes. Read-only unless --apply is given.

    python3 tag-cleanup-scratch/normalise_tags.py            # dry run, writes mapping.md
    python3 tag-cleanup-scratch/normalise_tags.py --apply    # backs up, then rewrites

The dry run also lists the tags used only once, so the long tail can be read
alongside the merges: that is where a near-copy of an established tag hides.
"""
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arctic_history as H  # noqa: E402

OUT = Path(__file__).with_name("mapping.md")
TABLES = (("artifacts", "id"), ("events", "id"))


def survey(c):
    """Every stored tag, with how often it is used and what it becomes."""
    uses = Counter()                        # raw element -> times stored
    tag_uses = Counter()                    # tag as it stands -> times used
    canon_uses = Counter()                  # tag after normalising -> times used
    rows = 0
    split_rows = 0
    for t, key in TABLES:
        for r in c.execute(f"SELECT {key} AS k, tags FROM {t}"):
            rows += 1
            stored = H.stored_tags(r["tags"])
            if any(len(H.normalise_tags(e)) > 1 for e in stored):
                split_rows += 1
            for e in stored:
                uses[e] += 1
                for part in str(e).split(","):
                    part = part.strip()
                    if part:
                        tag_uses[part] += 1
                        canon_uses[H.normalise_tag(part)] += 1
    return uses, tag_uses, canon_uses, rows, split_rows


def report(c):
    uses, tag_uses, canon_uses, rows, split_rows = survey(c)
    changed = {t: H.normalise_tag(t) for t in tag_uses if H.normalise_tag(t) != t}
    groups = defaultdict(list)
    for t, canon in changed.items():
        groups[canon].append(t)

    lines = ["# Tags: what the normaliser changes", "",
             f"{rows} rows on artifacts and events hold {len(tag_uses)} distinct tags in "
             f"{sum(tag_uses.values())} uses. {split_rows} rows hold a comma-joined string that "
             "becomes one element per tag.", "",
             f"{len(changed)} tags change, folding into {len(groups)} canonical tags; "
             f"{len(canon_uses)} distinct tags remain.", "",
             "A tag is lowercase, its words hyphenated at the boundary, and singular unless the "
             "plural is the name itself (`queen-elizabeth-islands`). `leads`, the open water in "
             "the ice, is left alone: `lead` is already the metal in the Franklin bones.", "",
             "| canonical | uses after | folded from | uses |", "|---|---:|---|---:|"]
    for canon in sorted(groups):
        variants = sorted(groups[canon], key=lambda t: -tag_uses[t])
        lines.append(f"| `{canon}` | {canon_uses[canon]} | " +
                     ", ".join(f"`{v}`" for v in variants) + " | " +
                     ", ".join(str(tag_uses[v]) for v in variants) + " |")
    singles = sorted(t for t, n in canon_uses.items() if n == 1)
    lines += ["", f"## The long tail: {len(singles)} tags used once", "",
              "Nothing here is wrong; `check` reports them as notes so a near-copy of an "
              "established tag can be spotted and merged by hand.", "",
              ", ".join(f"`{t}`" for t in singles), ""]
    OUT.write_text("\n".join(lines))
    print(f"{len(tag_uses)} tags, {len(changed)} change into {len(groups)} canonical tags; "
          f"{len(canon_uses)} remain, {len(singles)} used once")
    print(f"{split_rows} of {rows} rows hold a comma-joined string to split")
    w = max([len(t) for t in changed] + [8])
    for t in sorted(changed, key=lambda t: (changed[t], t)):
        print(f"  {t:{w}s} -> {changed[t]:{w}s} {tag_uses[t]:5d} use(s)")
    print(f"mapping: {OUT}")


def apply(c):
    """Rewrite every tags column in the canonical form. Backs up first."""
    import shutil
    from datetime import datetime
    db = Path(H.HISTORY_DB)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    bak = db.parent / "_backups" / f"history-{stamp}-pre-tag-normalise.sqlite"
    bak.parent.mkdir(parents=True, exist_ok=True)
    c.execute("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(db, bak)
    print("backup:", bak)
    n = 0
    for t, key in TABLES:
        for k, raw in c.execute(f"SELECT {key}, tags FROM {t}").fetchall():
            fixed = json.dumps(H.normalise_tags(raw), ensure_ascii=False)
            if fixed != (raw or "[]"):
                c.execute(f"UPDATE {t} SET tags=? WHERE {key}=?", (fixed, k))
                n += 1
    c.commit()
    print(f"{n} rows rewritten")


def read_only():
    """The dry run never touches the database, not even to open the log."""
    p = Path(H.HISTORY_DB)
    if not p.exists():
        raise SystemExit(f"no history database at {p}")
    try:
        c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        c.execute("SELECT COUNT(*) FROM artifacts")
    except sqlite3.OperationalError:                    # a busy write-ahead log
        c = sqlite3.connect(f"file:{p}?mode=ro&immutable=1", uri=True)
    c.row_factory = sqlite3.Row
    return c


def main():
    if "--apply" in sys.argv:
        apply(H.connect(H.HISTORY_DB, create=False))
    else:
        report(read_only())


if __name__ == "__main__":
    main()
