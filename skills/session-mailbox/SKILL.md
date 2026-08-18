---
name: session-mailbox
description: Run an asynchronous review or decision loop between two AI sessions through a single append-only Markdown file, so nothing depends on inter-process messaging that reports success but silently drops messages. The pair can be implementer × reviewer (code review) or implementer × strategist (design decisions). Use this when handing a PR to a second session for review, asking another session for a design decision, waiting on a reply from another session, or resuming a mailbox loop after a restart. Both sides read this same file, whichever agent they run on.
license: MIT
---

# Session Mailbox

Two sessions exchange reviews and decisions by **appending to one Markdown file**. Session-to-session
messaging APIs can return success and still not deliver, so the filesystem is the only channel.

**Declare the pair of roles at the top of the mailbox file.** `implementer` × `reviewer` for code review,
`implementer` × `strategist` for design decisions. Below, read them as `<your role>` / `<their role>`.

Which side you are on flips per turn: you are **asking** when your append requests a review or a decision,
and **answering** when it responds to one. Decide from what you are about to write.

## File rules (both roles)

- **One topic, one file, append-only.** Default location `~/.claude/mailbox/<topic>.md`. A reply written to
  a new file is never read. Never rewrite or delete existing lines — that erases what the other side already acted on.
- **Never keep a second copy.** Two copies mean hand-syncing, and one of them is always stale. If the other
  session cannot read outside a repo, *move* the file to `<repo>/.claude/mailbox/<topic>.md` and gitignore it.
  Pick one location. Live mailboxes carry PR contents and internal discussion, so they do not belong in a
  published repo — only this skill and its template do.
- **Fixed heading shape.** Every append starts with `## <role> <n>: <one-line summary>`, numbered per role
  (implementer 1 → reviewer 1 → implementer 2 …). Without a fixed shape you cannot count new arrivals.
- **Count to detect, read to decide.** `grep -c '^## <their role>'` tells you *whether* something arrived;
  always read the body to decide what it says. Judging by mtime or the last line loses an LGTM.
- **Append at the end of the file.** Anything inserted mid-file is missed by a reader who only looks at the tail.
- **Re-count right before you write.** The other side may have appended while you were drafting. If the count
  grew, read that section first and answer both in one append. Replying to a stale section leaves the order
  out of step with the conversation, and every later reader has to reconstruct what answers what.
- **Name the section you are answering** on the first line of your own (`Re: reviewer 1`, or `New` for a new topic).
  Tail order alone does not carry that, so the section has to.

## Polling

`scripts/mailbox.py status <file>` prints the absolute path, the header, per-role section counts, and a
ready-to-paste cron prompt. Run it to start a loop **and to resume one** — resuming is just re-reading the
current counts, which is exactly what the wrong-file mistakes come from doing by memory.

- **Put the absolute path in the cron prompt, literally.** When the job fires, none of the conversation is
  left; the prompt is the only context. A topic name alone sends you to a similarly named mailbox
  (`<topic>-strategy.md` vs `<topic>-strategy-mailbox.md`, `<topic>.md` vs `<topic>.archive.md`).
- **Put all four in the prompt**: absolute path, topic name, the other role's heading prefix, and the count at
  the time you armed it. One session may watch several mailboxes at once (a 1-minute PR review and a
  10-minute strategy thread), and prompts that cannot be told apart get answered into the wrong file.
- **Check the header before writing.** If the topic name and role declaration at the top are not what you
  expect, **stop and ask the human instead of appending**. Cross-posting makes both sides reason from a
  mixed transcript, and append-only means you cannot take it back.
- **Arm it** with `CronCreate`: `cron: "*/1 * * * *"`, `recurring: true`, `durable: false`. Keep the job ID.
- **Keep watching after LGTM, at a lower rate.** `CronDelete` the 1-minute job and re-arm at `*/10 * * * *`.
  Follow-up review of a later diff, or a corrected assumption, does arrive after an LGTM.
- **`CronDelete` when the topic closes** — merged, landed, or the human says so. Recurring jobs otherwise keep
  firing until they expire on their own after 7 days.

## Asking (requesting a review or a decision)

1. **Write the request at the top of the file.** `scripts/mailbox.py new` fills in the three required lines:
   the **role pair**, the **exit condition** (`reviewer appends a section containing LGTM`, `strategist answers
   A/B/C`) — a condition agreed only in chat disappears with the session, so only what is in the file counts —
   and the **subject** (PR number, URL, HEAD commit, or the question). Then add the substance: what changed,
   what you want looked at, and where you already think it is weak.
2. **A human starts the other session by hand.** Do not automate that. "Read this file" is enough of a prompt;
   the request itself is in the file.
3. **Wait** — arm the loop as described under Polling.
4. **Read the new sections in full**, then append `## <your role> <n>: …` with what you changed, the result of
   walking through their reproduction steps, real command output (test counts), and the current HEAD commit.
   They cannot confirm anything without looking at the same commit.
5. **When the exit condition is met**, append a short acknowledgement and drop the poll to the lower rate.

## Answering (returning a review or a decision)

1. **Read the whole file**, starting with the exit condition and subject. Past rounds matter: do not repeat a
   finding, and check whether the last fix opened something new.
2. **Separate what you verified from what you did not.** For review, report as findings only what you
   reproduced, and label the rest as concerns. For decisions, separate what was already settled from what you
   are deciding now. The other side acts on this file alone, so a blend costs them real work.
3. **Append `## <your role> <n>: <one-line summary>`** with the HEAD commit you checked, the findings (file and
   line, reproduction, suggested fix), and your verification (types, test count, CI) — or, for a decision, the
   conclusion, the reasoning, and the constraints. **Write the exit words (`LGTM`, the conclusion) in the body**,
   or the other side keeps waiting.
4. **If you are the one waiting next**, poll the same way, counting `^## <their role>`.

## Several open topics at once (common for implementer × strategist)

Put the topic in the heading summary (`## strategist 2: decision on the "not applicable" verdict`). Do **not**
move handled sections elsewhere — moving breaks append-only and erases the position the other side read from.
State which topics you handled on the first line of your own section instead.

## Closing a mailbox

`scripts/mailbox.py close <file>` appends a `CLOSED` line and moves the file to `~/.claude/mailbox/archive/`.

- **Archive, do not delete.** The file is usually the only record of *why* a change ended up the way it did;
  the PR keeps the diff, not the argument. Delete only once that reasoning is written down somewhere else.
- **Archive into a separate directory.** A sibling like `<topic>.archive.md` next to the live file is exactly
  what a resumed poll reads by mistake.

## Template

`templates/mailbox.md` — `scripts/mailbox.py new <path> --asking <role> --answering <role>` copies it into place.
