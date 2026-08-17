# Working in this repository

This repo publishes Agent Skills through four install routes (`npx skills`,
`gh skill`, the Claude Code plugin marketplace, and plain `.zip` files). They all
read from one place: `skills/<name>/SKILL.md`. Never add a second copy of a skill
to satisfy an installer — the layout is already what each of them discovers.

## Invariants

- `name` in the frontmatter must equal the skill's directory name.
- `description` must cover what the skill does *and* when to use it. It is the
  only thing an agent reads before deciding to activate the skill.
- `allowed-tools`, if present, is a space-separated string — not a YAML list.
  `gh skill publish` rejects the list form.
- Never commit `metadata.github-*` fields. `gh skill install` writes those into
  a SKILL.md as install provenance; `gh skill publish --fix` strips them.
- Every skill needs a matching plugin entry in `.claude-plugin/marketplace.json`,
  using `"source": "./"` with `"skills": ["./skills/<name>"]` and
  `"strict": false`. The validator fails the build if one is missing.

## Before committing

```bash
python3 scripts/validate-skills.py
```

## Writing skills

Keep `SKILL.md` under ~500 lines; move detail into `references/` inside the skill
folder, since agents load those files only when a task needs them. Start from
`templates/SKILL.md.template`.
