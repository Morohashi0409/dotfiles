# Source of Truth

This skill is an orchestration layer. It is not the final authority for runtime behavior or category taxonomy.

The external authorities referenced here are local operator documents for this machine.
They are authoritative for execution, but they are not automatically shareable team documents.

## Priority Order

1. Explicit user instructions and current-thread facts
2. External runtime scripts
3. External CloudLog documents
4. Skill-local execution documents
5. Human-facing overview text

## External Runtime Scripts

These are authoritative for actual execution behavior:

- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/check_cloudlog_automator_ready.py`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py`

If the skill summary disagrees with a script, trust the script.

## External CloudLog Documents

These are authoritative for operational truth:

- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md`
- `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md`

Use these for:

- exact JSON field meaning
- validator guarantees and warning semantics
- automator UI behavior
- exact category strings
- category decisions for WellCom, one-platform, and アドモニ

When writing team-facing documentation, do not require readers to open these local paths.
Instead, summarize the necessary rule in the skill-local docs and keep the local path as an operator-only reference.

## Skill-Local Documents

Skill-local docs are authoritative only for:

- read order
- role preparation
- monthly orchestration sequence
- escalation rules
- what belongs inside the skill vs outside it

They must not become a parallel runtime contract or category catalog.

## Conflict Rules

- Category conflict: external category guide wins
- JSON contract conflict: external contract and validator win
- UI behavior conflict: automator script and external automator README win
- Workflow conflict: `SKILL.md` and skill references win unless higher-priority sources say otherwise
- Human summary conflict: `README.md` loses to all higher-priority sources

## Sharing Rule

- For execution on this machine: local external docs are valid and authoritative.
- For department sharing: skill-local docs are the readable layer.
- Never treat `/Users/resily0808/Documents/...` paths as universally reachable documentation.
