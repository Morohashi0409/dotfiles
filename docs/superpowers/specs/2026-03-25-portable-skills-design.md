# Portable Skills Design

## Purpose

Create a dotfiles-managed skill for authoring and updating skills that work in both Claude Code and Codex.
The skill should treat a shared `SKILL.md` as the canonical source, keep Codex-specific UI metadata in `agents/openai.yaml`, and support both new skill creation and retrofitting existing skills.

## Context

The current repository already treats `~/dotfiles/claude/skills/` as the source of truth for Claude skills, and `codex/setup.sh` mirrors those skill directories into `~/.codex/skills/`.
That means a single skill directory can carry both the shared skill body and Codex-only metadata, as long as the structure remains safe for both environments.

## Goals

- Create one reusable skill that helps build Claude/Codex-compatible skills.
- Support both new skill creation and updating existing skills.
- Keep Codex assets managed inside dotfiles rather than as ad hoc files under `~/.codex/skills/`.
- Reduce repeated manual work by bundling helper scripts.
- Preserve compatibility with existing skill directories and setup scripts.

## Non-Goals

- Do not redesign the entire Claude or Codex setup flow.
- Do not force an immediate migration of every existing skill to a stricter format.
- Do not maintain separate Claude and Codex copies of the same skill body.

## Skill Name

Recommended skill name: `portable-skills`

Reasoning:

- Short and easy to invoke explicitly.
- Broad enough to cover both creation and retrofit work.
- Maps well to the main concern: portability across Claude Code and Codex.

## Canonical Location

The skill will live at:

`~/dotfiles/claude/skills/portable-skills/`

This directory becomes the canonical source for:

- shared `SKILL.md`
- Codex `agents/openai.yaml`
- helper scripts
- portability references

The existing setup scripts can continue linking the entire directory into:

- `~/.claude/skills/portable-skills`
- `~/.codex/skills/portable-skills`

## Directory Structure

```text
~/dotfiles/claude/skills/portable-skills/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── init_portable_skill.py
│   ├── sync_openai_yaml.py
│   └── audit_skill_portability.py
└── references/
    ├── frontmatter-rules.md
    └── portability-checklist.md
```

## Core Design

### Shared Skill Body

`SKILL.md` is the canonical skill body and should be written so both Claude Code and Codex can use it without duplicating content.

The skill will teach this model:

- keep shared operational guidance in `SKILL.md`
- keep Codex UI metadata in `agents/openai.yaml`
- avoid mixing machine-facing UI config into the main skill body
- prefer incremental updates for existing skills rather than destructive rewrites

### Codex Metadata

`agents/openai.yaml` is treated as Codex-specific metadata.
It is recommended for every portable skill and should be generated or refreshed from the shared `SKILL.md`.

The portable skill will guide users to include at least:

- `interface.display_name`
- `interface.short_description`
- `interface.default_prompt`

### Compatibility Model

The portability rule is:

- put the cross-platform skill logic in `SKILL.md`
- put Codex UI metadata in `agents/openai.yaml`
- keep optional references and scripts next to the skill in the same directory

This avoids duplicated skill bodies while staying compatible with the current `claude/setup.sh` and `codex/setup.sh` directory-link approach.

## Supported Workflows

### 1. New Portable Skill

When the user wants a brand new skill:

1. identify the skill name, use cases, and trigger language
2. create the new skill directory under `~/dotfiles/claude/skills/`
3. generate a shared `SKILL.md`
4. generate `agents/openai.yaml`
5. optionally create `scripts/`, `references/`, and `assets/` if needed
6. validate the resulting structure

### 2. Retrofit Existing Skill

When the user already has a Claude-oriented skill:

1. inspect the existing `SKILL.md`
2. detect Codex portability gaps
3. add or refresh `agents/openai.yaml`
4. flag frontmatter or structure that may be risky for Codex
5. preserve compatibility unless the user asks for a stricter cleanup

### 3. Audit Skill Portability

When the user wants a portability review:

1. inspect the skill directory
2. verify required files and recommended files
3. check shared frontmatter safety
4. check whether `agents/openai.yaml` exists and looks current
5. emit findings as:
   - safe
   - recommended update
   - risky or incompatible

## Script Responsibilities

### `scripts/init_portable_skill.py`

Purpose:

- initialize a new portable skill in `~/dotfiles/claude/skills/<name>/`

Responsibilities:

- normalize the skill name
- create the target directory
- create `SKILL.md`
- create `agents/openai.yaml`
- optionally create resource directories
- avoid overwriting existing files unless explicitly requested

### `scripts/sync_openai_yaml.py`

Purpose:

- generate or refresh `agents/openai.yaml` from an existing `SKILL.md`

Responsibilities:

- parse `name` and `description`
- derive human-facing Codex metadata
- write a deterministic `agents/openai.yaml`
- support repeated updates without creating noisy diffs

### `scripts/audit_skill_portability.py`

Purpose:

- audit a new or existing skill for Claude/Codex portability

Responsibilities:

- inspect directory layout
- inspect frontmatter keys
- verify presence and basic quality of `agents/openai.yaml`
- flag unsupported or high-risk portability issues
- output actionable remediation suggestions

## Frontmatter Rules

The portability baseline for shared `SKILL.md` is:

- required: `name`, `description`
- generally safe: `license`, `metadata`
- needs caution: Claude-oriented extras such as `user-invocable`

The portable skill should not assume every existing Claude-only frontmatter key is invalid, but it should teach users to prefer the smallest cross-platform-safe frontmatter where possible.

Codex-specific information should be moved into `agents/openai.yaml` instead of growing the shared frontmatter.

## References

### `references/frontmatter-rules.md`

Should document:

- safe shared frontmatter patterns
- risky or tool-specific keys
- migration guidance for existing skills

### `references/portability-checklist.md`

Should document:

- required files
- recommended files
- naming rules
- validation steps
- common failure patterns

## Error Handling

The skill and scripts should handle:

- missing `SKILL.md`
- invalid or unparsable frontmatter
- invalid skill names
- missing `agents/openai.yaml`
- attempts to overwrite existing files
- partial portability where a skill is usable in Claude but not yet well-formed for Codex

For retrofit work, default behavior should be conservative:

- report before rewriting
- preserve existing content unless the user asked for normalization

## Testing and Validation

Validation should cover:

- new skill initialization
- `agents/openai.yaml` generation from a valid `SKILL.md`
- audit output for a healthy skill
- audit output for a Claude-only legacy skill
- audit output for malformed frontmatter

Preferred validation flow:

1. run the portable skill's helper scripts on a scratch skill directory
2. run Codex `quick_validate.py` against generated skill folders where applicable
3. manually inspect generated `agents/openai.yaml`
4. manually inspect diffs for retrofit operations

## Implementation Notes

- Reuse Codex `skill-creator` conventions where possible instead of inventing a parallel standard.
- Keep scripts small and deterministic.
- Keep `SKILL.md` concise and move detailed compatibility guidance into `references/`.
- Preserve the current setup model where dotfiles is the canonical store and setup scripts symlink entire skill directories.

## Open Decisions Already Resolved

- Canonical directory: `~/dotfiles/claude/skills/`
- Skill body strategy: shared `SKILL.md`
- Codex metadata strategy: `agents/openai.yaml`
- Supported scope: new skills, retrofit of existing skills, and portability audits
- Automation level: helper scripts included

## Recommended Next Step

Implement `portable-skills` under `~/dotfiles/claude/skills/`, then validate the generated structure and helper scripts locally before using it on additional skills.
