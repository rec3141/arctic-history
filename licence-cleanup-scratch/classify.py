"""Draft classifier: free-text licence -> controlled code.

Reads every distinct licence value from artifacts and sources, assigns a code by
ordered rules, and writes mapping.md for review. Read-only against the DB.

Codes (most permissive first):
  public-domain          out of copyright, US federal/NASA, no known restrictions,
                         compilations made for this project from open material
  cc0                    CC0 dedication
  cc-by-X / cc-by-sa-X / cc-by-nc-sa-X / cc-by-nc-nd-X   Creative Commons, version kept
  crown-expired          Canadian Crown copyright, fifty-year term run out
  crown-open             Crown copyright in force; OGL Canada, Reproduction of Federal
                         Law Order, or Government of Canada/Nunavut/Manitoba
                         non-commercial reproduction terms
  open-access            free to read at the publisher, no CC licence (Arctic pre-2016,
                         Erudit, U of T/Laval, UCalgary Press, Archivaria, DCB, finding aids)
  attribution            reusable with attribution under the holder's own terms
                         (Inuit Heritage Trust, Council of Europe, SPRI information sheet)
  permission             holder or project owner approved use for this layer
  fair-dealing           in copyright; short passage quoted or figure described under
                         fair dealing for research
  in-copyright-licensed  in copyright; file held for internal research use under a
                         University of Manitoba or publisher licence, not for republication
  in-copyright-cited     in copyright; cited only, nothing reproduced or held
  rights-reserved        holder reserves rights; use here is under their stated terms,
                         not cleared for redistribution
  not-cleared            explicitly NOT CLEARED, no file held
  unknown                status not established
"""
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "db/history/history.sqlite"
OUT = Path(__file__).with_name("mapping.md")


def cc(v):
    m = re.search(r"\bcc[ -]?(by(?:-nc)?(?:-sa|-nd)?)(?:\s+([0-9.]+))?", v, re.I)
    if not m:
        return None
    name = m.group(1).lower()
    ver = m.group(2) or ""
    return f"cc-{name}" + (f"-{ver}" if ver else "")


# (regex, code, judgement-call note or None). First match wins; order matters.
RULES = [
    (r"NOT CLEARED", "not-cleared", None),
    (r"not cleared for redistribution", "not-cleared", None),
    (r"^unknown", "unknown", None),

    (r"^CC0|\(CC0\)", "cc0", None),
    (r"CC BY-SA 4\.0 and CC BY 3\.0", "cc-by-sa-4.0", "two licences named; the stricter (SA) kept"),
    (r"Creative Commons Attribution-ShareAlike 2\.5", "cc-by-sa-2.5", None),
    (r"CC BY \(Creative Commons Attribution\)", "cc-by", None),
    (r"^Creative Commons, per file", "cc-by", "version not stated; per-file"),
    (r"^CC BY|^CC BY-SA", None, None),  # handled by cc() below

    (r"NOT expired|in force to 2041", "crown-open", None),
    (r"Government of Canada document of 1934-35", "fair-dealing", "quoted from Dick 2001, in copyright"),
    (r"request 21", "crown-expired", "public domain; the Commons use was also approved, request 21"),
    (r"approved for this layer|request 19", "permission", None),
    (r"reproduction by permission", "permission", "SPRI: reproduction is by permission of the Picture Library"),

    (r"Open Government Licence", "crown-open", None),
    (r"Reproduction of Federal Law Order", "crown-open", None),
    (r"Crown copyright.*(expired|ran out|term has expired)|Crown record.*expired|Crown term expired",
     "crown-expired", None),
    (r"public domain.*Crown copyright|Crown copyright expired", "crown-expired", None),
    (r"RCAF photograph, Crown copyright expired|RCMP photograph.*expired", "crown-expired", None),
    (r"Crown copyright, Canada; not open access", "in-copyright-cited",
     "Crown copyright in force with no reproduction terms stated"),
    (r"public domain \(Government of Canada, published 1935\)", "crown-expired", "a 1935 Crown work; term long expired"),
    (r"Crown copyright|Government of (Canada|Nunavut)|Province of Manitoba", "crown-open", None),

    (r"public domain \(a work of the United States|US federal work|United States government work"
     r"|United States, published|public domain in the United States|NASA|Library of Congress", "public-domain", None),
    (r"public domain \(Qikiqtani Inuit Association\)", "public-domain",
     "check: QIA material is elsewhere recorded as in copyright"),

    (r"^public domain|^Public domain|^photographs reproduced as public domain|^no known (copyright )?restrictions"
     r"|^no restrictions|^Crown copyright expired; public domain", "public-domain", None),
    (r"(1854 lithograph|lithographs?) (is|are)? ?public domain|public domain \(the 1854 lithographs\)",
     "public-domain", "scan under CC, underlying lithograph PD"),

    (r"^route (compiled|reconstruction|redrawn)|^compiled for this project|^compilation, public domain"
     r"|^plot: freely usable|^place record compiled", "public-domain",
     "compilation made for this project; underlying text's status goes in the note"),
    (r"^text of the record: public domain|Wallace's statement dates from 1909|Green's 1914 journal", "public-domain",
     "mixed: primary text PD, the article quoting it in copyright"),
    (r"^Krüger's own words, 1930$", "public-domain", None),
    (r"Krüger's own|the document is Krüger's own", "fair-dealing",
     "Krüger's text PD, Barr's translation in copyright; quoted"),
    (r"in copyright (to Barr )?as printed", "fair-dealing", "testimony PD in substance, Barr's printing in copyright"),

    (r"fair dealing|short (quotation|extract|passage|quotations)|quoted (for|here|under|with|only|briefly|in)"
     r"|under (80|eighty) words|quoted, extracts|quotation kept", "fair-dealing", None),

    (r"^RIGHTS RESERVED", "rights-reserved", None),
    (r"open access journal, held for study", "open-access", None),
    (r"archived here for research", "open-access", "QTC reports are published free to download"),
    (r"no University of Manitoba licence found", "in-copyright-cited", "not accessed; cited only"),
    (r"[Cc]ited, not reproduced|cited only|individual records cited|cited (under|and|with|as)|no copy held"
     r"|described from|no photograph is registered|no image obtained|not open access|cited$", "in-copyright-cited", None),

    (r"read (under|through)|held (here|locally|for)|consulted|subscription|UM licence|University of Manitoba licence"
     r"|internal (research )?use|licence, internal|library's licence|lending copy|JSTOR scan|Polar Record for research"
     r"|Lyell Collection|accessed through|reachable through|local research copy", "in-copyright-licensed", None),

    (r"open access|free to read|freely (published|readable|usable)|free to consult|open data|Arctic, open access"
     r"|finding aid published free|published free", "open-access", None),
    (r"rights reserved \(Arctic", "open-access", "Arctic pre-2016: free to read, figures not reproduced"),

    (r"Inuit Heritage Trust|Council of Europe|Scott Polar Research Institute; freely|with attribution", "attribution", None),

    (r"rights reserved|RIGHTS RESERVED|Rights Reserved|\(c\) |all rights reserved|Copyright Arktisk", "rights-reserved", None),
    (r"^archival catalogue record", "attribution", "AMNH catalogue metadata cited"),
    (r"^in copyright, |^in copyright$|^institutional copyright|^museum copyright|^object photographs? in copyright"
     r"|^copyright ", "in-copyright-cited", "in copyright, no use terms stated: check what is held"),
]


def classify(v):
    for pat, code, note in RULES:
        if re.search(pat, v):
            if code is None:
                return cc(v), None
            return code, note
    c = cc(v)
    if c:
        return c, None
    return "UNMATCHED", None


def redundant(old, code):
    """The old text says no more than the code's label: no note needed."""
    import sys
    sys.path.insert(0, str(DB.parents[2]))
    import arctic_history as H
    o = old.strip().lower()
    return o in (code, H.licence_label(code).lower()) or re.fullmatch(r"cc by[-a-z]* [0-9.]+( dk)?", o) is not None


def apply(c):
    """Move the free text to rights_note and put the code in licence. Backs up first."""
    import shutil
    from datetime import datetime
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    bak = DB.parent / "_backups" / f"history-{stamp}-pre-licence-codes.sqlite"
    c.execute("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(DB, bak)
    print("backup:", bak)
    n = 0
    for t, key in (("artifacts", "id"), ("sources", "bibkey")):
        cols = {r[1] for r in c.execute(f"PRAGMA table_info({t})")}
        if "rights_note" not in cols:
            c.execute(f"ALTER TABLE {t} ADD COLUMN rights_note TEXT DEFAULT ''")
        for k, old in c.execute(f"SELECT {key}, licence FROM {t} WHERE licence<>''").fetchall():
            code, _ = classify(old)
            if code == "UNMATCHED":
                raise SystemExit(f"unmatched: {old!r}")
            note = "" if redundant(old, code) else old
            c.execute(f"UPDATE {t} SET licence=?, rights_note=? WHERE {key}=?", (code, note, k))
            n += 1
    c.commit()
    print(f"{n} rows recoded")


def main():
    import sys
    c = sqlite3.connect(DB)
    if "--apply" in sys.argv:
        apply(c)
        return
    counts = defaultdict(lambda: [0, 0])
    for t, i in (("artifacts", 0), ("sources", 1)):
        for v, n in c.execute(f"SELECT licence, count(*) FROM {t} GROUP BY licence"):
            counts[v][i] += n
    by_code = defaultdict(list)
    for v, (na, ns) in counts.items():
        code, note = classify(v)
        by_code[code].append((na + ns, na, ns, v, note))

    lines = ["# Licence field: draft mapping for review", "",
             f"{len(counts)} distinct values across artifacts and sources, mapped to {len(by_code)} codes.",
             "Proposed: `licence` takes the code; the original text moves unchanged to a new `rights_note` column",
             "so nothing is lost. Rows marked ◆ are judgement calls; please check those first.", ""]
    order = ["public-domain", "cc0"] + sorted(k for k in by_code if k.startswith("cc-")) + \
            ["crown-expired", "crown-open", "open-access", "attribution", "permission", "fair-dealing",
             "in-copyright-licensed", "in-copyright-cited", "rights-reserved", "not-cleared", "unknown", "UNMATCHED"]
    order += [k for k in by_code if k not in order]
    lines += ["| code | values | artifact rows | source rows |", "|---|---:|---:|---:|"]
    for code in order:
        if code in by_code:
            rows = by_code[code]
            lines.append(f"| {code} | {len(rows)} | {sum(r[1] for r in rows)} | {sum(r[2] for r in rows)} |")
    lines.append("")
    for code in order:
        if code not in by_code:
            continue
        rows = sorted(by_code[code], key=lambda r: -r[0])
        lines += [f"## {code}", "", "| art | src | value | note |", "|---:|---:|---|---|"]
        for tot, na, ns, v, note in rows:
            vv = v.replace("|", "\\|").replace("\n", " ")
            if len(vv) > 160:
                vv = vv[:157] + "..."
            lines.append(f"| {na} | {ns} | {vv} | {'◆ ' + note if note else ''} |")
        lines.append("")
    OUT.write_text("\n".join(lines))
    print(f"{len(counts)} values -> {len(by_code)} codes; UNMATCHED: {len(by_code.get('UNMATCHED', []))}")
    for r in by_code.get("UNMATCHED", []):
        print("  ", r[3])


if __name__ == "__main__":
    main()
