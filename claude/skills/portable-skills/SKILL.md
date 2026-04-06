---
name: portable-skills
description: Create or retrofit a skill so a shared SKILL.md works in both Claude Code and Codex. Use when adding a new skill under dotfiles, generating Codex agents/openai.yaml metadata, or auditing portability of an existing Claude-oriented skill.
---

# Portable Skills

Create and maintain skills that use one shared `SKILL.md` while still supporting Codex-specific metadata and validation.

## Overview

Treat `~/dotfiles/claude/skills/<skill-name>/` as the canonical skill directory.
Keep cross-platform instructions in `SKILL.md`, keep Codex UI metadata in `agents/openai.yaml`, keep helper automation in `scripts/`, and install the finished skill into both `~/.codex/skills/` and `~/.claude/skills/` so Codex and Claude Code can discover it.
Use `scripts/prepare_portable_skill.py` as the default finish step after creating or editing a portable skill.

Read [references/frontmatter-rules.md](references/frontmatter-rules.md) when you need to decide which frontmatter keys are safe to share.
Read [references/portability-checklist.md](references/portability-checklist.md) when you need a quick audit or validation flow.

## Use This Workflow

### New Skill

Use this flow when the user wants a new skill that should work in both Claude Code and Codex.

1. Confirm the skill name, the trigger situations, and whether the skill needs `scripts/`, `references/`, or `assets/`.
2. Create the skill under `~/dotfiles/claude/skills/<skill-name>/`.
3. Write one shared `SKILL.md` with cross-platform-safe frontmatter.
4. Run `scripts/init_portable_skill.py` if you need a starter layout.
5. Run `scripts/prepare_portable_skill.py` on the skill directory.
6. If the current thread still does not show the skill as a candidate, refresh the skill list or start a new thread before treating that as a bug.

### Retrofit Existing Skill

Use this flow when a skill already exists under `~/dotfiles/claude/skills/` and needs Codex support.

1. Read the existing `SKILL.md`.
2. Run `scripts/prepare_portable_skill.py` on the skill directory unless the user asked for a read-only audit.
3. Preserve existing behavior unless the user asked for cleanup or normalization.
4. If the audit flags risky frontmatter, reduce it only as far as the user requested.

### Audit Skill Portability

Use this flow when the user wants a readiness check without changing the skill yet.

1. Run `scripts/audit_skill_portability.py <skill-dir>`.
2. Classify findings as `safe`, `recommended-update`, or `risky`.
3. Explain whether the skill is already portable, needs Codex metadata, or still carries Claude-only assumptions.
4. If the audit is clean but the skill still is not visible in the current thread, explain that the skill registry list may need a refresh or a new session.

## Shared Rules

- Keep one canonical `SKILL.md`.
- Keep Codex UI metadata in `agents/openai.yaml`.
- Install dotfiles-managed skills into both `~/.codex/skills/` and `~/.claude/skills/` before expecting them to appear in Codex or Claude Code.
- Prefer `scripts/prepare_portable_skill.py` over manually running sync, install, and audit as separate commands.
- Prefer small shared frontmatter: `name` and `description` are the baseline.
- Preserve existing Claude-oriented keys only when compatibility or explicit user intent requires them.
- Do not create separate Claude and Codex copies of the skill body.

## Helper Scripts

### `scripts/init_portable_skill.py`

Use when creating a new skill directory under dotfiles.

Responsibilities:
- normalize the skill name
- create the directory structure
- write a starter `SKILL.md`
- create optional resource directories
- call the metadata sync helper

### `scripts/sync_openai_yaml.py`

Use when a skill already has a `SKILL.md` and needs Codex metadata.

Responsibilities:
- read `name` and `description`
- derive `display_name`, `short_description`, and `default_prompt`
- write deterministic `agents/openai.yaml`

### `scripts/install_skill_link.py`

Use when a dotfiles-managed skill should become discoverable in Codex and Claude Code.

Responsibilities:
- create or refresh both `~/.codex/skills/<skill-dir-name>` and `~/.claude/skills/<skill-dir-name>` as symlinks to the dotfiles skill
- preserve existing matching symlinks
- fail loudly when a conflicting non-symlink path already exists

### `scripts/prepare_portable_skill.py`

Use when a portable skill should be made ready for Codex after creation or editing.

Responsibilities:
- run the standard validation from `skill-creator`
- sync `agents/openai.yaml`
- install or refresh both the `~/.codex/skills/` and `~/.claude/skills/` symlinks
- audit the final result and fail if the skill is not yet safe

### `scripts/audit_skill_portability.py`

Use when checking portability or before updating an existing skill.

Responsibilities:
- inspect directory layout
- inspect frontmatter keys
- detect missing or stale `agents/openai.yaml`
- detect when a dotfiles-managed skill is not installed into `~/.codex/skills/` or `~/.claude/skills/`
- report whether the skill is safe, recommended for update, or risky

## Validation

Use the following checks after creating or retrofitting a skill:

```bash
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/prepare_portable_skill.py /path/to/skill
```

Use the lower-level scripts only when you intentionally want a partial step such as a read-only audit.
