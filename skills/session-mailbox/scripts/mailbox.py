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

HEADING = re.compile(r"^## (?P<role>.+?) \d+:", re.MULTILINE)
ROLES_LINE = re.compile(r"^\*\*Roles\*\*:(?P<rest>.+)$", re.MULTILINE)
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "mailbox.md"

CRON_PROMPT = """Mailbox poll for "{topic}" — read ONLY {path}
Count the sections matching '^## {role} ' in that file. The count was {count} when this job was armed.
If it is still {count}, do nothing and end the turn.
If it grew: first check that the file's header still names the topic "{topic}". If it does not, you are in the
wrong mailbox — stop and ask the human rather than writing anything.
Then read the new sections in full and follow the session-mailbox skill: reply by appending one section at the
end of this same file, re-counting right before you write."""


def mailbox_path(value: str) -> Path:
    """argparse type: one place to resolve a mailbox path for every subcommand."""
    return Path(value).expanduser().resolve()


def read(path: Path) -> str:
    if not path.is_file():
        sys.exit(f"no such mailbox: {path}")
    return path.read_text()


def header(text: str) -> str:
    """The block before the first horizontal rule — everything that is not a section."""
    return text.split("\n---", 1)[0].strip()


def roles(text: str) -> list[str]:
    """The two roles declared in the header, in order."""
    m = ROLES_LINE.search(header(text))
    if not m:
        return []
    return [seg.split("=")[0].strip() for seg in m.group("rest").split(" / ")]


def topic(path: Path, text: str) -> str:
    return text.split("\n", 1)[0].lstrip("# ").strip() or path.stem


def cmd_new(args) -> None:
    if args.path.exists():
        sys.exit(f"refusing to overwrite an existing mailbox: {args.path}")
    text = TEMPLATE.read_text()
    text = text.replace("<asking role>", args.asking).replace("<answering role>", args.answering)
    text = text.replace("<topic>", args.topic or args.path.stem)
    args.path.parent.mkdir(parents=True, exist_ok=True)
    args.path.write_text(text)
    print(f"created {args.path}")
    print("Fill in Done when / Subject, then write your request as the first section.")


def cmd_status(args) -> None:
    text = read(args.path)
    counts: dict[str, int] = {}
    last = None
    for h in HEADING.finditer(text):
        counts[h.group("role")] = counts.get(h.group("role"), 0) + 1
        last = h.group(0).rstrip(":")

    print(f"path: {args.path}")
    print(header(text))
    print("\nsections:")
    for role, n in counts.items():
        print(f"  {role}: {n}")
    if not counts:
        print("  (none yet)")
    if last:
        print(f"last: {last}")

    subject = topic(args.path, text)
    watched = [args.watch] if args.watch else roles(text) or list(counts)
    if not watched:
        print("\nno '## <role> <n>:' headings and no Roles line — this mailbox does not follow the skill's shape.")
        print("Pass --watch <role> to still get a cron prompt (the count will start from 0).")
    for role in watched:
        print(f"\ncron prompt for watching '{role}' "
              '(CronCreate: cron "*/1 * * * *", recurring true, durable false; '
              '*/10 after LGTM, CronDelete when the topic closes):')
        print("-" * 78)
        print(CRON_PROMPT.format(topic=subject, path=args.path, role=role, count=counts.get(role, 0)))
        print("-" * 78)


def cmd_close(args) -> None:
    if not args.path.is_file():
        sys.exit(f"no such mailbox: {args.path}")
    archive = args.path.parent / "archive"
    archive.mkdir(exist_ok=True)
    target = archive / args.path.name
    if target.exists():
        sys.exit(f"already archived: {target}")
    with args.path.open("a") as f:
        f.write("\n---\n\nCLOSED\n")
    shutil.move(str(args.path), str(target))
    print(f"archived to {target}")
    print("CronDelete the poll for this mailbox.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a mailbox from the template")
    p_new.add_argument("path", type=mailbox_path)
    p_new.add_argument("--asking", required=True, help="role that requests the review or decision")
    p_new.add_argument("--answering", required=True, help="role that returns it")
    p_new.add_argument("--topic")
    p_new.set_defaults(func=cmd_new)

    p_status = sub.add_parser("status", help="print state and a cron prompt (use to start and to resume)")
    p_status.add_argument("path", type=mailbox_path)
    p_status.add_argument("--watch", help="only print the prompt for this role")
    p_status.set_defaults(func=cmd_status)

    p_close = sub.add_parser("close", help="append a CLOSED line and move the file to archive/")
    p_close.add_argument("path", type=mailbox_path)
    p_close.set_defaults(func=cmd_close)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
