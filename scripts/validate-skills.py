#!/usr/bin/env python3
"""Validate every skill in skills/ against the Agent Skills specification.

Implements the rules from https://agentskills.io/specification plus the extra
checks `gh skill publish` enforces, so CI catches problems without needing the
GitHub CLI or any third-party package.

Usage: python3 scripts/validate-skills.py [skills_dir]
"""

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MAX_BODY_LINES = 500


def parse_frontmatter(text):
    """Return (fields, body_line_count). Values are str, or dict for `metadata`.

    Deliberately small: the spec only allows scalar fields plus a flat
    string->string `metadata` map, so a full YAML parser buys nothing.
    """
    if not text.startswith("---\n"):
        raise ValueError("file must start with a YAML frontmatter block (`---`)")
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError:
        raise ValueError("unterminated YAML frontmatter block")

    fields, key, current = {}, None, []
    for line in raw.split("\n"):
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and key == "metadata":
            k, _, v = line.strip().partition(":")
            fields.setdefault("metadata", {})[k.strip()] = v.strip().strip("\"'")
            continue
        if line.startswith((" ", "\t")):  # continuation of a folded scalar
            current.append(line.strip())
            continue
        if key is not None and key != "metadata":
            fields[key] = " ".join(current).strip()
        k, sep, v = line.partition(":")
        if not sep:
            raise ValueError(f"cannot parse frontmatter line: {line!r}")
        key, current = k.strip(), [v.strip()]
        if key == "metadata":
            fields.setdefault("metadata", {})
    if key is not None and key != "metadata":
        fields[key] = " ".join(current).strip()

    return fields, body.count("\n") + 1


def validate(skill_dir):
    errors, warnings = [], []
    rel = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"{rel}: missing SKILL.md"], []

    try:
        fields, body_lines = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{rel}/SKILL.md: {exc}"], []

    name = fields.get("name", "")
    if not name:
        errors.append(f"{rel}/SKILL.md: `name` is required")
    else:
        if not NAME_RE.fullmatch(name):
            errors.append(
                f"{rel}/SKILL.md: name {name!r} must be lowercase a-z0-9 and single "
                "hyphens, not starting or ending with a hyphen"
            )
        if len(name) > 64:
            errors.append(f"{rel}/SKILL.md: name is {len(name)} chars (max 64)")
        if name != skill_dir.name:
            errors.append(f"{rel}/SKILL.md: name {name!r} must match its directory name")

    desc = fields.get("description", "")
    if not desc:
        errors.append(f"{rel}/SKILL.md: `description` is required")
    elif len(desc) > 1024:
        errors.append(f"{rel}/SKILL.md: description is {len(desc)} chars (max 1024)")

    compat = fields.get("compatibility")
    if compat is not None and len(compat) > 500:
        errors.append(f"{rel}/SKILL.md: compatibility is {len(compat)} chars (max 500)")

    tools = fields.get("allowed-tools")
    if tools is not None and tools.startswith("["):
        errors.append(f"{rel}/SKILL.md: allowed-tools must be a space-separated string, not a list")

    for key in fields.get("metadata", {}):
        if key.startswith("github-"):
            errors.append(
                f"{rel}/SKILL.md: metadata.{key} is install-provenance written by "
                "`gh skill install`; strip it before publishing (`gh skill publish --fix`)"
            )

    for key in set(fields) - KNOWN_FIELDS:
        warnings.append(f"{rel}/SKILL.md: unknown frontmatter field {key!r} (agents ignore it)")

    if body_lines > MAX_BODY_LINES:
        warnings.append(
            f"{rel}/SKILL.md: body is {body_lines} lines (recommended max {MAX_BODY_LINES}); "
            "move detail into references/"
        )

    return errors, warnings


def check_marketplace(root, skill_names):
    """Every skill should be installable as a Claude Code plugin, and vice versa."""
    path = root / ".claude-plugin" / "marketplace.json"
    if not path.is_file():
        return [f"{path.relative_to(root)}: missing"], []

    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(root)}: invalid JSON: {exc}"], []

    errors, listed = [], set()
    for entry in catalog.get("plugins", []):
        for skill_path in entry.get("skills", []):
            listed.add(Path(skill_path).name)
            if not (root / skill_path).is_dir():
                errors.append(
                    f"marketplace.json: plugin {entry.get('name')!r} points at "
                    f"{skill_path}, which does not exist"
                )
    for missing in sorted(skill_names - listed):
        errors.append(f"marketplace.json: skill {missing!r} is not listed in any plugin entry")
    return errors, []


def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "skills"

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not skill_dirs:
        print(f"no skills found in {skills_dir}", file=sys.stderr)
        return 1

    all_errors, all_warnings = [], []
    for skill_dir in skill_dirs:
        errors, warnings = validate(skill_dir)
        all_errors += errors
        all_warnings += warnings

    errors, warnings = check_marketplace(root, {d.name for d in skill_dirs})
    all_errors += errors
    all_warnings += warnings

    for warning in all_warnings:
        print(f"warning: {warning}")
    for error in all_errors:
        print(f"error: {error}", file=sys.stderr)

    if all_errors:
        print(f"\n{len(all_errors)} error(s) in {len(skill_dirs)} skill(s)", file=sys.stderr)
        return 1

    print(f"ok: {len(skill_dirs)} skill(s) valid ({', '.join(d.name for d in skill_dirs)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
