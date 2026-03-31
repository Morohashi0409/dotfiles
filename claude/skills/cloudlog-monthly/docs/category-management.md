# Category Management

Project-specific CloudLog categories stay outside this skill.

## Why They Stay Outside

- Category strings are operational data, not stable skill logic.
- CloudLog categories and my-patterns can change without a skill release.
- Duplicating category tables in the skill creates drift and unsafe ambiguity.
- The automator needs exact category strings, not approximate summaries.
- WellCom, one-platform, and アドモニ are business-specific classifications that belong to the external operations guide.

## What The Skill Owns

The skill owns:

- when to consult the category source of truth
- when to stop and ask for clarification
- how category decisions fit into monthly JSON generation

The skill does not own:

- the full category catalog
- the exact category strings for each project
- the canonical examples for project classification

## External Source Of Truth

Use `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md` as the primary category source.

This is required for:

- WellCom
- one-platform / ワンプラ
- アドモニ

If the skill and the external guide disagree, the external guide wins.

That guide is a local operator source, not a guaranteed team-readable document.
Shared skill docs should explain the policy and boundaries, while the exact category table stays in the local operator guide.
