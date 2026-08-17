# chezou/skills

[Agent Skills](https://agentskills.io) I use and maintain. Each skill is a plain
`SKILL.md` folder that follows the open [Agent Skills specification](https://agentskills.io/specification),
so it runs unmodified in Claude, Claude Code, Codex, opencode, Cursor, Copilot,
Gemini CLI, and the other agents that have adopted the format.

## Skills

| Skill | What it does |
| --- | --- |
| [`resume-tailor`](skills/resume-tailor/SKILL.md) | Tailors an existing resume to a specific job description, sourcing concrete evidence from an episode bank (brag doc, STAR notes, project inventory). Also covers cover letters, application questions, and the different bar that design roles are held to. |
| [`company-research`](skills/company-research/SKILL.md) | Researches a company before you apply or interview, and produces a sourced one-page brief: what they sell, how they make money, who runs the team, what the hiring pattern gives away, the flags, and the questions worth asking. |

## Install

Pick whichever route matches your agent. All four install the same files.

### 1. `npx skills` — works with ~70 agents

```bash
# every skill in this repo, into every agent it detects
npx skills add chezou/skills --all

# one skill, into specific agents
npx skills add chezou/skills --skill resume-tailor --agent claude-code --agent opencode

# user-level instead of project-level
npx skills add chezou/skills --skill resume-tailor --global

# see what's here without installing
npx skills add chezou/skills --list
```

### 2. `gh skill` — GitHub CLI (v2.90+)

```bash
gh skill preview chezou/skills resume-tailor    # read it before you trust it
gh skill install chezou/skills resume-tailor
gh skill install chezou/skills resume-tailor --agent codex
gh skill install chezou/skills resume-tailor --scope user   # default is project
gh skill update --all
```

### 3. Claude Code plugin marketplace

```
/plugin marketplace add chezou/skills
/plugin install resume-tailor@chezou-skills
```

Each skill is exposed as its own plugin, so you install only what you want.
Run `/plugin marketplace update chezou-skills` to pull later changes.

### 4. Plain files (claude.ai, or any agent)

Build the archives:

```bash
python3 scripts/package-skills.py     # writes dist/<skill>.zip
```

Or download a `.zip` from the [releases page](https://github.com/chezou/skills/releases).

- **claude.ai** — Settings → Capabilities → Skills → upload the `.zip`.
- **Anywhere else** — unzip so that `<skills-dir>/resume-tailor/SKILL.md` exists:

  | Agent | User-level | Project-level |
  | --- | --- | --- |
  | Claude Code | `~/.claude/skills/` | `.claude/skills/` |
  | Codex | `~/.agents/skills/` | `.agents/skills/` |
  | opencode | `~/.config/opencode/skills/` | `.opencode/skills/` |

  Cloning the repo and symlinking a skill directory into one of those paths works
  equally well, and keeps it updating with `git pull`.

## Repository layout

```
skills/<name>/SKILL.md          the single source of truth for every skill
.claude-plugin/marketplace.json Claude Code catalog; one plugin entry per skill
scripts/validate-skills.py      spec validation, run in CI
scripts/package-skills.py       builds dist/<name>.zip for the file route
```

`skills/<name>/SKILL.md` is deliberately the only copy of a skill. It is the
layout `gh skill` and `npx skills` both discover, and the marketplace entries
point back into it via `"source": "./"` plus `"skills": ["./skills/<name>"]`
with `"strict": false` — so nothing is duplicated and the four install routes
can never drift apart.

## Adding a skill

1. `mkdir -p skills/<name>` and write `SKILL.md`. The `name` in the frontmatter
   must match the directory name; `description` must say both what the skill
   does and when to use it, since that is all an agent sees until it activates.
2. Add a plugin entry to `.claude-plugin/marketplace.json` mirroring the existing
   one.
3. Validate:

   ```bash
   python3 scripts/validate-skills.py
   gh skill publish --dry-run     # optional: the same checks GitHub enforces
   ```

Keep `SKILL.md` under ~500 lines and push detail into `references/`, `scripts/`,
or `assets/` inside the skill folder — agents load those only when they need them.

## Releasing

Tag a version and push it; CI validates, packages, and publishes the release
with the zips attached.

```bash
git tag v0.1.0 && git push origin v0.1.0
```

Version pinning in `gh skill install --pin` and update checks both read these
release tags, so cut one whenever a skill changes meaningfully.

## License

MIT. See [LICENSE](LICENSE).
