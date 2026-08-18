#!/usr/bin/env python3
"""Helpers for the session-mailbox loop: create a mailbox, read its state, close it.

    mailbox.py new <path> --asking implementer --answering reviewer [--topic "PR #99 review"]
    mailbox.py status <path> [--watch <role>]
    mailbox.py close <path>

`status` is what you run both to start polling and to resume it: it prints the
absolute path, the header, the per-role section counts, and a cron prompt that
carries all of them. Resuming from memory instead is how a session ends up
reading a similarly named mailbox and answering into the wrong conversation.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

HEADING = re.compile(r"^## (?P<role>.+?) (?P<n>\d+):", re.MULTILINE)
ROLES_LINE = re.compile(r"^\*\*Roles\*\*:\s*(?P<a>.+?)\s*=.*?/\s*(?P<b>.+?)\s*=", re.MULTILINE)
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "mailbox.md"

CRON_PROMPT = """Mailbox poll for "{topic}" — read ONLY {path}
Count the sections matching '^## {role} ' in that file. The count was {count} when this job was armed.
If it is still {count}, do nothing and end the turn.
If it grew: first check that the file's header still names the topic "{topic}". If it does not, you are in the
wrong mailbox — stop and ask the human rather than writing anything.
Then read the new sections in full and follow the session-mailbox skill: reply by appending one section at the
end of this same file, re-counting right before you write."""


def read(path: Path) -> str:
    if not path.is_file():
        sys.exit(f"no such mailbox: {path}")
    return path.read_text()


def roles(text: str) -> list[str]:
    """Roles declared in the header, falling back to whatever headings exist."""
    m = ROLES_LINE.search(text)
    if m:
        return [m.group("a"), m.group("b")]
    seen = []
    for h in HEADING.finditer(text):
        if h.group("role") not in seen:
            seen.append(h.group("role"))
    return seen


def topic(path: Path, text: str) -> str:
    first = text.lstrip().split("\n", 1)[0]
    return first.lstrip("# ").strip() or path.stem


def cmd_new(args) -> None:
    path = Path(args.path).expanduser().resolve()
    if path.exists():
        sys.exit(f"refusing to overwrite an existing mailbox: {path}")
    text = TEMPLATE.read_text()
    text = text.replace("<asking role>", args.asking).replace("<answering role>", args.answering)
    text = text.replace("<topic>", args.topic or path.stem)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"created {path}")
    print("Fill in Roles / Done when / Subject before handing the file to the other session.")


def cmd_status(args) -> None:
    path = Path(args.path).expanduser().resolve()
    text = read(path)
    counts: dict[str, int] = {}
    for h in HEADING.finditer(text):
        counts[h.group("role")] = counts.get(h.group("role"), 0) + 1
    headings = [h.group(0).rstrip(":") for h in HEADING.finditer(text)]

    print(f"path:  {path}")
    print(f"topic: {topic(path, text)}")
    for line in text.split("\n"):
        if line.startswith(("**Roles**", "**Done when**", "**Subject**")):
            print(f"  {line}")
    print("sections:")
    for role, n in counts.items() or [("(none yet)", 0)]:
        print(f"  {role}: {n}")
    if headings:
        print(f"last:  {headings[-1]}")

    watched = [args.watch] if args.watch else roles(text) or list(counts)
    if not watched:
        print("\nno '## <role> <n>:' headings and no Roles line — this mailbox does not follow the skill's shape.")
        print("Pass --watch <role> to still get a cron prompt (the count will start from 0).")
    for role in watched:
        print(f"\ncron prompt for watching '{role}' "
              '(CronCreate: cron "*/1 * * * *", recurring true, durable false; '
              '*/10 after LGTM, CronDelete when the topic closes):')
        print("-" * 78)
        print(CRON_PROMPT.format(topic=topic(path, text), path=path,
                                 role=role, count=counts.get(role, 0)))
        print("-" * 78)


def cmd_close(args) -> None:
    path = Path(args.path).expanduser().resolve()
    text = read(path)
    archive = path.parent / "archive"
    archive.mkdir(exist_ok=True)
    target = archive / path.name
    if target.exists():
        sys.exit(f"already archived: {target}")
    with path.open("a") as f:
        f.write(f"\n---\n\nCLOSED — {args.reason}\n")
    shutil.move(str(path), str(target))
    print(f"archived to {target}")
    print("CronDelete the poll for this mailbox.")
    print("Kept rather than deleted: this file is usually the only record of why the change ended up this way.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a mailbox from the template")
    p_new.add_argument("path")
    p_new.add_argument("--asking", required=True, help="role that requests the review or decision")
    p_new.add_argument("--answering", required=True, help="role that returns it")
    p_new.add_argument("--topic")
    p_new.set_defaults(func=cmd_new)

    p_status = sub.add_parser("status", help="print state and a cron prompt (use to start and to resume)")
    p_status.add_argument("path")
    p_status.add_argument("--watch", help="only print the prompt for this role")
    p_status.set_defaults(func=cmd_status)

    p_close = sub.add_parser("close", help="append a CLOSED line and move the file to archive/")
    p_close.add_argument("path")
    p_close.add_argument("--reason", default="exit condition met")
    p_close.set_defaults(func=cmd_close)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
