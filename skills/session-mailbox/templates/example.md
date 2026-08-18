# Worked round

Not copied into a mailbox — `mailbox.py new` writes `mailbox.md` only, so these headings are never
counted as real sections. Read this for the shape of an exchange, then write your own.

---

## implementer 1: adapter rejects duplicate page numbers

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

## reviewer 1: two P1s, both in the fail-closed path

Re: implementer 1

Checked HEAD: `<commit>`

### [P1] <finding>

Where: `<path>:<line>`

<what is wrong, the reproduction, and what you observed running it. Label anything you could not reproduce
as a concern>

<suggested fix>

### Verification

- Tests: <count>
- Types / lint: <result>
- CI: <result>

<If there is nothing to raise, write `LGTM` in this section.>

---

## implementer 2: both fixed, regression tests added

Re: reviewer 1

HEAD: `<commit>` (after the fix)

### [P1] <finding> → fixed / not fixing

<what you did, plus the result of walking through their reproduction steps>

<verification output>
