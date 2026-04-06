# Frontmatter Rules

Use these rules when one `SKILL.md` needs to work in both Claude Code and Codex.

| Key | Status | Notes |
| --- | --- | --- |
| `name` | required | Use lowercase letters, digits, and hyphens only. |
| `description` | required | Primary trigger text. Include what the skill does and when to use it. |
| `license` | safe | Acceptable shared metadata when needed. |
| `metadata` | safe-with-care | Keep minimal and tool-agnostic. |
| `allowed-tools` | Codex-safe | Use only when the restriction is intentional and current. |
| `user-invocable` | Claude-legacy | Preserve only when existing Claude workflows still depend on it. |

## Recommended Baseline

Prefer this minimum shape:

```yaml
---
name: example-skill
description: Create or update example artifacts. Use when the user needs...
---
```

## Migration Guidance

- Start from the existing frontmatter. Do not delete keys blindly.
- Treat `name` and `description` as the portability baseline.
- Keep `license` and minimal `metadata` if they add real value.
- Move Codex UI details into `agents/openai.yaml` instead of expanding shared frontmatter.
- If a key exists only for Claude-specific invocation behavior, classify it as legacy and confirm whether it still needs to remain.

## Risk Signals

Treat these as audit warnings:

- frontmatter keys that are unrelated to skill triggering or shared metadata
- verbose metadata that duplicates the body
- machine-facing UI configuration in `SKILL.md` instead of `agents/openai.yaml`
- stale Claude-only compatibility keys that nobody still needs
