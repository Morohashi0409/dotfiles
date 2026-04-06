# Portable Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a dotfiles-managed `portable-skills` skill that helps create and retrofit skills so they work in both Claude Code and Codex from a shared `SKILL.md`.

**Architecture:** Keep `~/dotfiles/claude/skills/portable-skills/` as the canonical skill directory, store cross-platform instructions in `SKILL.md`, and generate Codex-only metadata into `agents/openai.yaml`. Bundle three small Python helpers for initialization, metadata sync, and portability auditing, then validate them against scratch skill directories and representative existing skills.

**Tech Stack:** Markdown, YAML, Python 3 standard library, existing Codex `skill-creator` validator

---

## File Structure

**Create:**
- `claude/skills/portable-skills/SKILL.md`
- `claude/skills/portable-skills/references/frontmatter-rules.md`
- `claude/skills/portable-skills/references/portability-checklist.md`
- `claude/skills/portable-skills/agents/openai.yaml`
- `claude/skills/portable-skills/scripts/sync_openai_yaml.py`
- `claude/skills/portable-skills/scripts/audit_skill_portability.py`
- `claude/skills/portable-skills/scripts/init_portable_skill.py`
- `tests/portable_skills/test_sync_openai_yaml.py`
- `tests/portable_skills/test_audit_skill_portability.py`
- `tests/portable_skills/test_init_portable_skill.py`

**Modify:**
- `claude/CLAUDE.md`

**Reference while implementing:**
- `docs/superpowers/specs/2026-03-25-portable-skills-design.md`
- `.codex/skills/.system/skill-creator/SKILL.md`
- `.codex/skills/.system/skill-creator/references/openai_yaml.md`
- `.codex/skills/.system/skill-creator/scripts/quick_validate.py`
- `codex/setup.sh`
- `claude/setup.sh`

## Task 1: Author The Shared Skill Content

**Files:**
- Create: `claude/skills/portable-skills/SKILL.md`
- Create: `claude/skills/portable-skills/references/frontmatter-rules.md`
- Create: `claude/skills/portable-skills/references/portability-checklist.md`
- Modify: `claude/CLAUDE.md`

- [ ] **Step 1: Draft the shared skill body**

Write `claude/skills/portable-skills/SKILL.md` with only cross-platform-safe frontmatter and concise instructions for:

```md
---
name: portable-skills
description: Use when creating a new skill or retrofitting an existing one so a shared SKILL.md works in both Claude Code and Codex, with Codex metadata generated into agents/openai.yaml.
---
```

Core sections should cover:
- canonical directory choice
- new skill flow
- retrofit flow
- audit flow
- when to read each reference file
- when to run each helper script

- [ ] **Step 2: Write the portability references**

Write `references/frontmatter-rules.md` with a table like:

```md
| Key | Status | Notes |
| --- | --- | --- |
| name | required | shared across Claude and Codex |
| description | required | primary trigger text |
| license | safe | acceptable shared metadata |
| metadata | safe-with-care | keep minimal |
| user-invocable | Claude-legacy | preserve only when needed |
```

Write `references/portability-checklist.md` with required checks for:
- directory layout
- frontmatter keys
- `agents/openai.yaml`
- helper scripts
- smoke validation commands

- [ ] **Step 3: Update the skill index**

Add `portable-skills` to `claude/CLAUDE.md` in the skills table with a one-line purpose such as:

```md
| `portable-skills` | Claude/Codex 両対応の skill 作成・更新・監査 |
```

- [ ] **Step 4: Validate the written content**

Run:

```bash
python3 /Users/resily0808/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/resily0808/dotfiles/claude/skills/portable-skills
rg -n "TODO|FIXME|TBD|\\[TODO\\]" /Users/resily0808/dotfiles/claude/skills/portable-skills
```

Expected:
- validator prints `Skill is valid!`
- ripgrep returns no matches

- [ ] **Step 5: Commit the documentation scaffold**

Run:

```bash
git -C /Users/resily0808/dotfiles add claude/skills/portable-skills/SKILL.md claude/skills/portable-skills/references/frontmatter-rules.md claude/skills/portable-skills/references/portability-checklist.md claude/CLAUDE.md
git -C /Users/resily0808/dotfiles commit -m "feat: add portable-skills docs scaffold"
```

## Task 2: Implement `sync_openai_yaml.py`

**Files:**
- Create: `claude/skills/portable-skills/scripts/sync_openai_yaml.py`
- Create: `tests/portable_skills/test_sync_openai_yaml.py`

- [ ] **Step 1: Write the failing test**

Create `tests/portable_skills/test_sync_openai_yaml.py` with cases for:

```python
def test_sync_generates_openai_yaml_from_skill_metadata():
    ...
    self.assertIn('display_name: "Portable Skills"', content)
    self.assertIn('default_prompt: "Use $portable-skills', content)

def test_sync_preserves_deterministic_output():
    ...
    self.assertEqual(first_write, second_write)
```

Use a temporary directory to create a minimal `SKILL.md` fixture and assert the script writes `agents/openai.yaml`.

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_sync_openai_yaml.py' -v
```

Expected:
- FAIL because `sync_openai_yaml.py` does not exist or required functions are missing

- [ ] **Step 3: Write the minimal implementation**

Implement `sync_openai_yaml.py` with functions roughly shaped like:

```python
def parse_skill_frontmatter(skill_path: Path) -> dict: ...
def derive_interface_fields(name: str, description: str) -> dict: ...
def render_openai_yaml(interface: dict) -> str: ...
def sync_openai_yaml(skill_dir: Path) -> Path: ...
```

Implementation requirements:
- parse `name` and `description` from `SKILL.md`
- generate `display_name`, `short_description`, `default_prompt`
- write deterministic YAML to `agents/openai.yaml`
- expose a CLI like `python3 sync_openai_yaml.py <skill-dir>`

- [ ] **Step 4: Run the test to verify it passes**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_sync_openai_yaml.py' -v
```

Expected:
- PASS

- [ ] **Step 5: Commit**

Run:

```bash
git -C /Users/resily0808/dotfiles add claude/skills/portable-skills/scripts/sync_openai_yaml.py tests/portable_skills/test_sync_openai_yaml.py
git -C /Users/resily0808/dotfiles commit -m "feat: add openai yaml sync helper"
```

## Task 3: Implement `audit_skill_portability.py`

**Files:**
- Create: `claude/skills/portable-skills/scripts/audit_skill_portability.py`
- Create: `tests/portable_skills/test_audit_skill_portability.py`

- [ ] **Step 1: Write the failing tests**

Create tests for at least three cases:

```python
def test_audit_flags_missing_openai_yaml(): ...
def test_audit_warns_on_claude_only_frontmatter(): ...
def test_audit_reports_safe_skill_as_clean(): ...
```

Use temporary directories with minimal skill fixtures.

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_audit_skill_portability.py' -v
```

Expected:
- FAIL because `audit_skill_portability.py` does not exist or returns the wrong structure

- [ ] **Step 3: Write the minimal implementation**

Implement the script with a report model like:

```python
{
    "status": "safe" | "recommended-update" | "risky",
    "findings": [
        {"level": "info" | "warning" | "error", "message": "..."}
    ]
}
```

Checks should cover:
- `SKILL.md` existence
- parseable frontmatter
- missing `name` / `description`
- presence of non-portable keys such as `user-invocable`
- existence and freshness of `agents/openai.yaml`

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_audit_skill_portability.py' -v
```

Expected:
- PASS

- [ ] **Step 5: Commit**

Run:

```bash
git -C /Users/resily0808/dotfiles add claude/skills/portable-skills/scripts/audit_skill_portability.py tests/portable_skills/test_audit_skill_portability.py
git -C /Users/resily0808/dotfiles commit -m "feat: add portable skill audit helper"
```

## Task 4: Implement `init_portable_skill.py`

**Files:**
- Create: `claude/skills/portable-skills/scripts/init_portable_skill.py`
- Create: `tests/portable_skills/test_init_portable_skill.py`

- [ ] **Step 1: Write the failing tests**

Cover:

```python
def test_init_creates_expected_directory_structure(): ...
def test_init_does_not_overwrite_existing_skill_without_flag(): ...
def test_init_can_create_optional_resource_directories(): ...
```

Test the generated output under a temporary root, not under the real dotfiles path.

- [ ] **Step 2: Run the tests to verify they fail**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_init_portable_skill.py' -v
```

Expected:
- FAIL because `init_portable_skill.py` does not exist or required behavior is missing

- [ ] **Step 3: Write the minimal implementation**

Implement a CLI shaped like:

```python
python3 init_portable_skill.py <skill-name> --root /path/to/skills [--resources scripts,references,assets] [--force]
```

Behavior:
- normalize the skill name
- create `<root>/<skill-name>/`
- write a starter `SKILL.md`
- call the sync helper to generate `agents/openai.yaml`
- optionally create `scripts/`, `references/`, and `assets/`
- refuse to overwrite existing content unless `--force` is passed

- [ ] **Step 4: Run the tests to verify they pass**

Run:

```bash
python3 -m unittest discover -s /Users/resily0808/dotfiles/tests/portable_skills -p 'test_init_portable_skill.py' -v
```

Expected:
- PASS

- [ ] **Step 5: Commit**

Run:

```bash
git -C /Users/resily0808/dotfiles add claude/skills/portable-skills/scripts/init_portable_skill.py tests/portable_skills/test_init_portable_skill.py
git -C /Users/resily0808/dotfiles commit -m "feat: add portable skill initializer"
```

## Task 5: Generate Portable-Skills Metadata And Run End-To-End Validation

**Files:**
- Create: `claude/skills/portable-skills/agents/openai.yaml`
- Modify: `claude/skills/portable-skills/SKILL.md` (only if validation reveals wording issues)

- [ ] **Step 1: Generate the skill's own Codex metadata**

Run:

```bash
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/sync_openai_yaml.py /Users/resily0808/dotfiles/claude/skills/portable-skills
```

Expected:
- `claude/skills/portable-skills/agents/openai.yaml` exists and contains `display_name`, `short_description`, and `default_prompt`

- [ ] **Step 2: Validate the portable-skills directory**

Run:

```bash
python3 /Users/resily0808/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/resily0808/dotfiles/claude/skills/portable-skills
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/audit_skill_portability.py /Users/resily0808/dotfiles/claude/skills/portable-skills
```

Expected:
- validator prints `Skill is valid!`
- audit reports `safe` or an equivalent no-action-needed result

- [ ] **Step 3: Run scratch initialization smoke tests**

Run:

```bash
tmpdir="$(mktemp -d)"
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/init_portable_skill.py demo-portable-skill --root "$tmpdir" --resources scripts,references
python3 /Users/resily0808/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$tmpdir/demo-portable-skill"
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/audit_skill_portability.py "$tmpdir/demo-portable-skill"
rm -rf "$tmpdir"
```

Expected:
- initialization succeeds
- generated skill validates
- audit reports no blocking portability issues

- [ ] **Step 4: Run a retrofit audit on an existing skill**

Run:

```bash
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/audit_skill_portability.py /Users/resily0808/dotfiles/claude/skills/frontend-design
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/audit_skill_portability.py /Users/resily0808/dotfiles/claude/skills/fixing-accessibility
```

Expected:
- report differences between already-portable and Claude-legacy patterns
- no crashes on existing repository skills

- [ ] **Step 5: Final commit**

Run:

```bash
git -C /Users/resily0808/dotfiles add claude/skills/portable-skills/agents/openai.yaml claude/skills/portable-skills/scripts tests/portable_skills claude/CLAUDE.md
git -C /Users/resily0808/dotfiles commit -m "feat: add portable-skills automation"
```
