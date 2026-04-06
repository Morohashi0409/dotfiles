# Portability Checklist

Use this checklist when creating or retrofitting a skill for both Claude Code and Codex.

## Required

- Skill directory lives under `~/dotfiles/claude/skills/<skill-name>/`
- Skill is installed into `~/.codex/skills/<skill-name>` so Codex can discover it
- Skill is installed into `~/.claude/skills/<skill-name>` so Claude Code can discover it
- `SKILL.md` exists
- `SKILL.md` has `name` and `description`
- `name` is lowercase hyphen-case
- `agents/openai.yaml` exists for Codex metadata

## Recommended

- `agents/openai.yaml` is generated from the current `SKILL.md`
- helper scripts live in `scripts/` when the workflow is repeated enough to automate
- larger guidance lives in `references/` instead of bloating the main skill body
- `scripts/prepare_portable_skill.py` is the default finishing command after creating or editing a portable skill
- validation commands run cleanly on a scratch skill and at least one existing skill

## Validation Commands

```bash
python3 /Users/resily0808/dotfiles/claude/skills/portable-skills/scripts/prepare_portable_skill.py /path/to/skill
```

## Common Failure Patterns

- `SKILL.md` exists but `agents/openai.yaml` is missing
- dotfiles 側には skill があるが `~/.codex/skills/` にリンクされていない
- dotfiles 側には skill があるが `~/.claude/skills/` にリンクされていない
- frontmatter contains Claude-only legacy keys with no clear reason to keep them
- `agents/openai.yaml` exists but no longer matches the current `name` or `description`
- Codex-specific UI details are mixed into shared frontmatter
- a new skill is created under `~/.codex/skills/` or `~/.claude/skills/` directly instead of dotfiles
- skill は正しくインストールされているが、現在のスレッドの候補一覧が古いままで再読込されていない
