#!/usr/bin/env python3
"""Forward a request's drafted email through the lab Gmail for a person to
edit and send on from their own address.

    mail-draft.py --id 4                # request #4's draft -> the person's inbox
    mail-draft.py --id 4 --dry-run      # print what would be sent
    mail-draft.py --file letter.txt --subject "..."   # any drafted letter

The draft is the text after "Draft, ready to send:" in the request's why
(the whole why if that marker is absent); its own "Subject:" line becomes
the subject. The mail is prefaced with a note saying which request it came
from, so the receiving person's part is: read, edit, and forward to the
real recipient.

Addresses and credentials are never in the repository. They live in
``~/.amundsen-mail.conf`` (chmod 600), three lines:

    from = the sending Gmail address
    to = the person's inbox
    password = a Gmail app password for the sending address, made at
               https://myaccount.google.com/apppasswords (needs 2-step
               verification); spaces in it are ignored

The mail goes out over smtp.gmail.com:465 (SSL).
"""

from __future__ import annotations

import argparse
import re
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import arctic_history as H          # noqa: E402

CONF = Path.home() / ".amundsen-mail.conf"


def conf() -> dict:
    if not CONF.is_file():
        sys.exit(f"no {CONF}: three lines, `from = <gmail address>`, `to = <inbox>`, "
                 "`password = <gmail app password>`; chmod 600")
    out = {}
    for line in CONF.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip().lower()] = v.strip()
    for k in ("from", "to"):
        if not out.get(k):
            sys.exit(f"{CONF} is missing `{k} = ...`")
    return out


def draft_from_request(ident: int) -> tuple[str, str, str]:
    c = H.connect(create=False)
    try:
        r = c.execute("SELECT * FROM requests WHERE id=?", (ident,)).fetchone()
    finally:
        c.close()
    if not r:
        sys.exit(f"no request #{ident}")
    text = r["why"]
    if "Draft, ready to send:" in text:
        text = text.split("Draft, ready to send:", 1)[1].strip()
    m = re.search(r"^To:\s*(.+)$", text, re.M)
    forward_to = m.group(1).strip() if m else ""
    if m:
        text = (text[:m.start()] + text[m.end():]).strip()
    m = re.search(r"^Subject:\s*(.+)$", text, re.M)
    subject = m.group(1).strip() if m else f"Draft from history request #{ident}"
    if m:
        text = (text[:m.start()] + text[m.end():]).strip()
    preface = (f"Draft from history request #{ident} ({r['kind']}, {r['topic']}): {r['what']}\n"
               + (f"FORWARD TO: {forward_to}\n" if forward_to else
                  "Forward to: (no To: line in the draft; the request's own text names the recipient)\n")
               + f"Edit as you see fit; the queue is at https://cryomics.org/amundsen/requests/\n"
               + "-" * 60 + "\n\n")
    return subject, preface + text, f"request #{ident}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="mail-draft.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", type=int, help="the request whose draft to forward")
    ap.add_argument("--file", help="a file holding the letter instead")
    ap.add_argument("--subject", default="", help="subject when --file is used")
    ap.add_argument("--to", default="", help="override the configured recipient")
    ap.add_argument("--dry-run", action="store_true", help="print, do not send")
    a = ap.parse_args(argv)

    cfg = conf()
    if a.id:
        subject, body, origin = draft_from_request(a.id)
        if a.subject:
            subject = a.subject
    elif a.file:
        body, origin = Path(a.file).read_text(encoding="utf-8"), a.file
        subject = a.subject or f"Draft letter ({Path(a.file).name})"
    else:
        ap.error("--id or --file is needed")

    msg = EmailMessage()
    msg["From"] = cfg["from"]
    msg["To"] = a.to or cfg["to"]
    msg["Subject"] = subject
    msg.set_content(body)

    if a.dry_run:
        print(msg.as_string())
        return 0
    if not cfg.get("password"):
        sys.exit(f"{CONF} is missing `password = ...`: a Gmail app password for {cfg['from']}, "
                 "made at https://myaccount.google.com/apppasswords")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=60) as s:
        s.login(cfg["from"], cfg["password"].replace(" ", ""))
        s.send_message(msg)
    print(f"sent {origin} to {msg['To']} as {cfg['from']}: {subject}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
