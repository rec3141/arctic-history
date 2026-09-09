#!/usr/bin/env python3
"""Build an edits file that makes every flagged artifact's description name
the people the row claims it is about."""
import json
import sqlite3

DB = "/data/dev/arctic-history/db/history/history.sqlite"

# a sentence to append, per artifact, that names the people in plain prose
APPEND = {
    "ross-parry-012": " William Edward Parry set every officer and man in both ships to the saws; "
        "the plate was engraved after a sketch by Lieutenant Frederick William Beechey, "
        "who was aboard the Hecla.",
    "ross-parry-025": " William Edward Parry took the survey of the wreck himself, with "
        "Captain Henry Parkyns Hoppner, who had commanded the Fury, and Hoppner was the last "
        "officer but one to leave her.",
    "ross-parry-031": " John Ross wrote this at the head of Lancaster Sound on 31 August 1818, "
        "and it cost him his career: the mountains he named after John Wilson Croker are not there.",
    "ross-parry-032": " John Ross wrote this off the northwest coast of Greenland on "
        "17 August 1818, of the red snow on what his charts call the Crimson Cliffs.",
    "ross-parry-210": " The chart was engraved for John Ross's published narrative of the voyage.",
    "ross-parry-121": " The views were drawn by Lieutenant Frederick William Beechey of the Hecla, "
        "who made the coastal profiles for the published chart.",
    "ross-parry-126": " The survey was made under William Edward Parry's direction during the "
        "ships' ten months in the harbour.",
}

# people-naming clause for the long runs of appendix and register pages
PARRY = (" The observations were made under William Edward Parry's direction and printed "
         "as an appendix to his published journal.")
PARRY_MET = (" The register was kept aboard the ship William Edward Parry commanded and "
             "printed as an appendix to his journal of the second voyage.")
PARRY_MET1 = (" The register was kept aboard the ship William Edward Parry commanded and "
              "printed with his journal of the first voyage.")
VOCAB = (" William Edward Parry compiled the vocabulary with George Francis Lyon over the "
         "two winterings, checking words with Iglulingmiut speakers as they were written down.")


def main():
    ids = [l.strip() for l in open("/data/dev/arctic-history/ross-parry-scratch/flagged.txt")
           if l.strip()]
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    out = {}
    for aid in ids:
        row = con.execute("select description from artifacts where id=?", (aid,)).fetchone()
        desc = (row[0] or "").rstrip()
        n = int(aid.rsplit("-", 1)[1])
        if aid in APPEND:
            extra = APPEND[aid]
        elif 247 <= n <= 268:
            extra = PARRY_MET
        elif n == 40:
            extra = PARRY_MET1
        elif 269 <= n <= 282:
            extra = VOCAB
        else:
            extra = PARRY
        out[aid] = {"description": desc + extra}
    json.dump(out, open("/data/dev/arctic-history/ross-parry-scratch/edits-desc.json", "w"),
              indent=1)
    print("wrote", len(out), "edits")


if __name__ == "__main__":
    main()
