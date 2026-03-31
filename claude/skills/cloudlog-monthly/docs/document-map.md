# Document Map

`cloudlog-monthly` is split between skill-local documents and external CloudLog documents.

## Skill-Local Documents

| Document | Role | Reader |
|---|---|---|
| `README.md` | Human-facing overview and responsibility split | monthly requester, teammates |
| `SKILL.md` | Agent entrypoint, read order, execution boundary | skill executor |
| `docs/document-map.md` | Map of the whole document system | maintainer, skill executor |
| `docs/source-of-truth.md` | Priority order when sources conflict | maintainer, skill executor |
| `docs/user-preparation.md` | Preparation checklist by role | requester, environment owner, maintainer |
| `docs/conversation-guide.md` | Chat-based request patterns and attachment-first usage | requester, teammates |
| `docs/category-management.md` | Why category ownership stays outside the skill | maintainer, skill executor |
| `references/path-conventions.md` | Canonical filenames and folder layout | skill executor |
| `references/monthly-workflow.md` | Monthly orchestration flow | skill executor |
| `references/automatic-entry-contract.md` | What “automatic entry ready” means inside the skill | skill executor |

## Local Operator Documents

The following documents are authoritative for execution on this machine, but they are not assumed to be readable by teammates outside this local environment.

| Document | Role | Reader |
|---|---|---|
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/INDEX.md` | External document index | local operator |
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md` | Exact JSON and automator contract | skill executor |
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md` | Detailed automator usage and troubleshooting | environment owner, skill executor |
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/QUICKSTART.md` | Quick runtime setup | environment owner |
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/別スレッド用_月次入力テンプレート.md` | Short handoff prompt for another thread | requester, maintainer |
| `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md` | Category source of truth | skill executor, maintainer |

## Responsibility Split

- Skill-local docs own orchestration, read order, and escalation policy.
- Local operator docs own JSON contract, UI contract, runtime usage, and category truth for this environment.
- External scripts own actual behavior.

For team sharing, prefer skill-local docs. Do not assume teammates can open the local operator docs.

If two sources disagree, use `docs/source-of-truth.md`.
