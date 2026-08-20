#!/usr/bin/env python3
"""Helpers for the session-mailbox loop: create a mailbox, read its state, write to it, close it.

    mailbox.py new <path> --asking implementer --answering reviewer [--topic "PR #99 review"]
    mailbox.py status <path> [--watch <role>]
    mailbox.py append <path> --role reviewer --re 'implementer 1' --summary '...' --body-file -
    mailbox.py close <path>

`append` is the enforcing one: it numbers your section, refuses a role the header
does not declare, refuses to answer a section the other side has already moved
past, optionally refuses a mailbox whose topic is not the one you expected, and
writes at the end without touching a byte that is already there.

`status` is what you run both to start polling and to resume it: it prints the
absolute path, the header, the per-role section counts, and a poll prompt that
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
POLL_LINE = re.compile(r"^\*\*Poll\*\*: start (?P<start>.+?)(?:,|$)", re.MULTILINE)
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "mailbox.md"

POLL_PROMPT = """Mailbox poll for "{topic}" — read ONLY {path}
Count the sections matching '^## {role} ' in that file. The count was {count} when this job was armed.
If it is still {count}, do nothing and end the turn.
If it grew: first check that the file's header still names the topic "{topic}". If it does not, you are in the
wrong mailbox — stop and ask the human rather than writing anything.
Then set this schedule back to {start} — the round is active again — and read the new sections in
full before replying with:
  python3 {script} append {path} --role {you} --re '{role} <n>' --summary '<one line>' --body-file -
It derives your section number, refuses a stale reply, and writes at the end without touching earlier bytes."""


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


def poll_start(text: str) -> str:
    """The mailbox's own starting interval: a review loop wants 1 minute, a strategy thread 10."""
    m = POLL_LINE.search(header(text))
    return m.group("start").strip() if m else "1 minute"


def topic(path: Path, text: str) -> str:
    return text.split("\n", 1)[0].lstrip("# ").strip() or path.stem


def cmd_new(args) -> None:
    if args.path.exists():
        sys.exit(f"refusing to overwrite an existing mailbox: {args.path}")
    text = TEMPLATE.read_text()
    text = text.replace("<asking role>", args.asking).replace("<answering role>", args.answering)
    text = text.replace("<topic>", args.topic or args.path.stem)
    text = text.replace("<poll start>", args.poll_start)
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
    start = poll_start(text)
    watched = [args.watch] if args.watch else roles(text) or list(counts)
    if not watched:
        print("\nno '## <role> <n>:' headings and no Roles line — this mailbox does not follow the skill's shape.")
        print("Pass --watch <role> to still get a poll prompt (the count will start from 0).")
    for role in watched:
        you = next((r for r in (roles(text) or list(counts)) if r != role), '<your role>')
        print(f"\npoll prompt for watching '{role}' — schedule it every {start} "
              "(Claude Code: CronCreate with recurring true, durable false; Codex: a heartbeat automation). "
              "After LGTM, follow this mailbox's exit condition: stop the schedule if the loop ends there, "
              "otherwise back off toward 60 minutes:")
        print("-" * 78)
        print(POLL_PROMPT.format(topic=subject, path=args.path, role=role, count=counts.get(role, 0),
                                 script=Path(__file__).resolve(), you=you, start=start))
        print("-" * 78)


def cmd_append(args) -> None:
    """Write one section at the end, enforcing what the skill otherwise only asks for."""
    text = read(args.path)
    declared = roles(text)
    if args.expect_topic and args.expect_topic != topic(args.path, text):
        sys.exit(f"wrong mailbox: header says {topic(args.path, text)!r}, expected {args.expect_topic!r}\n"
                 "Stop and ask the human — do not write into a mailbox you did not mean to open.")
    if declared and args.role not in declared:
        sys.exit(f"unknown role {args.role!r}; this mailbox declares {declared}\n"
                 "A role nobody counts is a section nobody reads.")

    counts: dict[str, int] = {}
    for h in HEADING.finditer(text):
        counts[h.group("role")] = counts.get(h.group("role"), 0) + 1

    if args.re:
        answered_role, _, answered_n = args.re.rpartition(" ")
        if not answered_n.isdigit():
            sys.exit(f"--re must be '<role> <n>' or use --new; got {args.re!r}")
        latest = counts.get(answered_role, 0)
        if latest == 0:
            sys.exit(f"no sections from {answered_role!r} to answer")
        if int(answered_n) < latest:
            unread = range(int(answered_n) + 1, latest + 1)
            which = str(unread[0]) if len(unread) == 1 else f"{unread[0]}-{unread[-1]}"
            sys.exit(f"{answered_role} is at {latest}, you are answering {answered_n}\n"
                     f"Read {answered_role} {which} first, then answer in one append.")

    body = sys.stdin.read() if args.body_file == "-" else \
        Path(args.body_file).expanduser().read_text() if args.body_file else args.body
    n = counts.get(args.role, 0) + 1
    heading = f"## {args.role} {n}: {args.summary}"
    section = f"\n---\n\n{heading}\n\nRe: {args.re or 'New'}\n\n{body.strip()}\n"
    with args.path.open("a") as f:
        f.write(("" if text.endswith("\n") else "\n") + section)
    print(f"appended {heading}")
    print(f"{args.role} is now at {n}. Leave the poll armed — replies arrive after LGTM too.")


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
    print("Stop the schedule watching this mailbox.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_new = sub.add_parser("new", help="create a mailbox from the template")
    p_new.add_argument("path", type=mailbox_path)
    p_new.add_argument("--asking", required=True, help="role that requests the review or decision")
    p_new.add_argument("--answering", required=True, help="role that returns it")
    p_new.add_argument("--topic")
    p_new.add_argument("--poll-start", default="1 minute",
                       help="starting poll interval for this mailbox (review loop 1 minute, strategy 10 minutes)")
    p_new.set_defaults(func=cmd_new)

    p_status = sub.add_parser("status", help="print state and a poll prompt (use to start and to resume)")
    p_status.add_argument("path", type=mailbox_path)
    p_status.add_argument("--watch", help="only print the prompt for this role")
    p_status.set_defaults(func=cmd_status)

    p_append = sub.add_parser("append", help="write one section at the end, with the skill's rules enforced")
    p_append.add_argument("path", type=mailbox_path)
    p_append.add_argument("--role", required=True, help="your role; must be one the header declares")
    p_append.add_argument("--summary", required=True, help="the one-line summary in the heading")
    answering = p_append.add_mutually_exclusive_group(required=True)
    answering.add_argument("--re", metavar="'<role> <n>'", help="the section you are answering")
    answering.add_argument("--new", dest="re", action="store_const", const=None,
                           help="this starts a topic rather than answering one")
    body = p_append.add_mutually_exclusive_group(required=True)
    body.add_argument("--body", help="section body")
    body.add_argument("--body-file", help="read the body from a file, or '-' for stdin")
    p_append.add_argument("--expect-topic", help="refuse to write if the header names a different topic")
    p_append.set_defaults(func=cmd_append)

    p_close = sub.add_parser("close", help="append a CLOSED line and move the file to archive/")
    p_close.add_argument("path", type=mailbox_path)
    p_close.set_defaults(func=cmd_close)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
