# <topic>

**Roles**: <asking role> = <which session> / <answering role> = <which session>

**Done when**: <answering role> appends a section containing `LGTM`. (Only a condition written here counts.)

**Subject**: PR <number> <URL> / HEAD `<commit>` / base `<branch>` — or the question to decide.

**This file is the only channel**: reply by appending here, at the end of the file — never a new file, chat, or
a messaging API. Start every append with `## <role> <n>: <one-line summary>` and never edit existing lines.
Re-count the other side's sections right before you write; if the count grew, read those first and answer in one append.

---

## <asking role> 1: <one-line summary>

Re: New

### What changed

<the substance — a table of files and their roles works well>

### What to look at

1. <a point; if you already think something is weak, say so here>
2. ...

### Verification

- Tests: <count / real output>
- Types / lint: <result>
- CI: <result>

---

## <answering role> 1: <one-line summary>

Re: <asking role> 1

Checked HEAD: `<commit>`

### [P1] <finding>

Where: `<path>:<line>`

<what is wrong, the reproduction, and what you observed running it. Label anything you could not reproduce as a concern>

<suggested fix>

### Verification

- Tests: <count>
- Types / lint: <result>
- CI: <result>

<If there is nothing to raise, write `LGTM` in this section.>

---

## <asking role> 2: <one-line summary>

Re: <answering role> 1

HEAD: `<commit>` (after the fix)

### [P1] <finding> → fixed / not fixing

<what you did, plus the result of walking through their reproduction steps>

<verification output>
