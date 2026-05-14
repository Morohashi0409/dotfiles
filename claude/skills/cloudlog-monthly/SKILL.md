---
name: cloudlog-monthly
description: Prepare monthly CloudLog source files, generate month JSON, validate it, and execute automatic CloudLog entry. Use when the user needs end-to-end monthly CloudLog preparation.
---

# CloudLog Monthly

## Overview

Prepare one month of CloudLog inputs end to end. Standardize the source PDFs into fixed paths, generate `YYYY-MM_cloudlog.json`, normalize it for CloudLog's 5-minute constraints, validate it, and run the existing automation when the user wants the month entered into CloudLog.

This skill is not self-contained by design. Keep stable execution logic in this skill directory, and keep operational source-of-truth data in the external CloudLog documents under `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog`.

Those external CloudLog documents are local operator docs for this machine, not generally accessible team-shared docs.
Use them for execution when available in this environment, but do not describe them to teammates as if they are universally reachable.

Before doing work, read these files in order:
1. [docs/document-map.md](docs/document-map.md)
2. [docs/source-of-truth.md](docs/source-of-truth.md)
3. [docs/user-preparation.md](docs/user-preparation.md)
4. [docs/category-management.md](docs/category-management.md)
5. [references/path-conventions.md](references/path-conventions.md) for the fixed folder layout.
6. [references/monthly-workflow.md](references/monthly-workflow.md) for the monthly flow and escalation rules.
7. [references/automatic-entry-contract.md](references/automatic-entry-contract.md) for what the user must prepare and what "ready for automatic entry" means.
8. `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md` when you need the exact JSON contract for `validate_json.py` or the exact UI behavior of `cloudlog_automator.py`.
9. `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md` when category decisions are involved.

## Boundary Rules

- Keep execution flow, helper scripts, stopping rules, and reading order inside this skill.
- Keep project-specific category mappings such as `WellCom`, `one-platform`, and `アドモニ` in the external category guide, not in `SKILL.md`.
- Keep the exact automator UI contract and exact JSON contract in the external CloudLog documents, not in this skill.
- Keep user-facing handoff templates in the external CloudLog documents, not in this skill.
- If category mappings or my-patterns changed, ask the user instead of inventing new mappings.
- If WellCom, one-platform, or アドモニ appears in the evidence, re-read the external category guide before classifying.
- For DXP classification, use strict defaults unless the user overrides:
  - `DXP【DX開発部】 > 会議（商品付.. > 入力不要 > 企業登録なし` only for `DXP開発定例`.
  - `DXP【DX開発部】 > システム運用・作業 > 入力不要 > 企業登録なし` only when evidence explicitly says `保守`.
  - Otherwise use `【資産化】ワンプラットフォーム> DXP > 入力不要 > 企業登録なし`.
- When writing or updating team-facing docs, summarize local-only external rules inside this skill directory instead of assuming teammates can open `/Users/...` paths.

## Use This Skill

- The user wants a monthly CloudLog JSON file.
- The user wants the month to be registered in CloudLog, not just summarized.
- The user attaches attendance or Outlook calendar PDFs for a month.
- The fixed monthly source paths are missing and need to be prepared.
- The user wants to feed a generated JSON file into CloudLog automation instead of manual browser clicking.

## Fixed Paths

- CloudLog root: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog`
- Daily notes root: `/Users/resily0808/Documents/Obsidian Vault/01_Daily`
- Monthly source root: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-sources`
- Monthly JSON root: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json`
- Category guide: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/クラウドログ分類と運用ガイド.md`
- Automation and JSON contract: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`
- Document index: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/INDEX.md`
- Automator README: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/README_cloudlog_automator.md`
- Quickstart: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/QUICKSTART.md`
- Thread handoff template: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/別スレッド用_月次入力テンプレート.md`
- JSON validator: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py`
- Auto entry script: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py`

## Workflow

1. Determine the target month in `YYYY-MM`.
2. Prepare the source PDFs.
   - Prefer file paths explicitly attached or pasted in the thread.
   - If they are not provided, use `scripts/prepare_monthly_sources.py` to search `~/Downloads`, copy the files into the fixed monthly folder, and rename them to the canonical names.
   - If attendance or Outlook calendar PDFs are still missing or ambiguous, stop and ask the user.
3. Check readiness with `scripts/check_monthly_inputs.py`.
4. Generate or update `monthly-json/YYYY-MM_cloudlog.json`.
   - Use Daily notes, the attendance PDF, the Outlook calendar PDF, GitHub activity, and the category guide.
   - Even if the user does not provide ticket numbers, fetch GitHub day activity per workday before final classification:
     - `python3 scripts/fetch_github_day_activity.py YYYY-MM-DD`
     - Default scope is `Resily/dxp` and `Resily/WellCom` for actor `Morohashi0409`.
   - If the fetched GitHub activity shows WellCom PR merge/update on the day, allocate a WellCom block unless stronger contradictory evidence exists.
   - Do not invent project category strings inside this skill. Read them from the category guide.
   - Keep the input JSON minimal, but preserve `time_blocks`.
   - Before handing the JSON to CloudLog, normalize it to CloudLog-ready 5-minute increments.
   - Both `attendance` and every `time_blocks` boundary must be 5-minute aligned.
   - Recalculate `minutes` from the rounded `time_blocks`.
   - When `attendance` is present, keep the day total consistent with the rounded blocks so CloudLog summary totals match.
   - Exclude legal holidays unless the user says otherwise.
   - Keep `attendance: null` for full-leave days when no attendance time should be entered.
5. Validate the JSON with `validate_json.py`.
6. If the user wants automatic entry, use `cloudlog_automator.py`.
   - Start Chrome with remote debugging automatically using the full path (do NOT ask the user to do this):
     ```bash
     bash "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/open_cloudlog_debug_chrome.sh" &
     ```
     Wait ~8 seconds, then run the readiness check. The script is NOT in PATH; always use the full path.
   - If the readiness check shows the login page, ask the user to log in, then wait for confirmation.
   - Read the automation and JSON contract if there is any doubt about field meaning or automator behavior.
   - **Before running the automator, always filter out already-entered dates.**
     - Run `scripts/filter_pending_dates.py YYYY-MM --out monthly-json/YYYY-MM_pending.json`.
     - If the pending file is empty (all done), skip the automator entirely.
     - Run the automator against `YYYY-MM_pending.json`, not the full monthly JSON.
   - Run the readiness check before the automation.
   - After the automator completes, record the successfully entered dates:
     - Run `scripts/filter_pending_dates.py YYYY-MM --mark-done DATE1 DATE2 ...` for each success.
     - On a clean full-month run, mark all non-failed dates as done.
   - Confirm that the month saved successfully, or isolate the failed days and ask the user only when the automation cannot recover.
   - Do not fall back to manual browser clicking unless the user explicitly asks.

## User Must Prepare

- The target month in `YYYY-MM`.
- Daily notes under `/Users/resily0808/Documents/Obsidian Vault/01_Daily/` for the month.
- One attendance PDF for that month.
- One Outlook or Teams calendar PDF for that month.
- Any category or my-pattern changes that happened since the previous run.
- For automatic entry, a logged-in CloudLog session (Chrome is started automatically by the skill).

See [docs/user-preparation.md](docs/user-preparation.md) for a role-based breakdown of what the monthly requester, environment owner, and CloudLog maintainer should each keep up to date.

If the user attaches the PDFs in the thread, use those first. If not, look in `~/Downloads`. If both are missing or ambiguous, stop and ask.

## Expected Outputs

- `monthly-sources/YYYY-MM/YYYY-MM_attendance.pdf`
- `monthly-sources/YYYY-MM/YYYY-MM_outlook-calendar.pdf`
- `monthly-json/YYYY-MM_cloudlog.json`
- A validated, 5-minute-aligned month that can be passed to `cloudlog_automator.py`
- If automatic entry was requested, a completion result that states which days were saved and which, if any, still need confirmation

## Ask The User When

- The attached files and the fixed monthly source folder both lack the required PDF.
- `~/Downloads` contains multiple plausible PDFs and the correct one is not obvious.
- A working day has thin Daily notes and GitHub or repo history still does not justify the category split.
- The category list or my-pattern setup has changed and the JSON category no longer maps cleanly.
- The target month still has an unfinished last day.

## Commands

```bash
# Chrome をデバッグモードで起動（フルパス必須・PATHに存在しない）
bash "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/open_cloudlog_debug_chrome.sh" &
# ↑ 実行後 ~8秒待ってから readiness check を行う

python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/prepare_monthly_sources.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/check_monthly_inputs.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/normalize_cloudlog_json.py "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json" --in-place
python3 "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py" "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json"
python3 "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/check_cloudlog_automator_ready.py" 2026-03

# 未入力分のみ抽出してから実行（再実行時も同様）
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/filter_pending_dates.py 2026-03 --out "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_pending.json"
python3 "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py" "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_pending.json"

# 成功した日付を完了記録に追記
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/filter_pending_dates.py 2026-03 --mark-done 2026-03-01 2026-03-02  # ...成功日を列挙

# 完了済み日付の確認
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/filter_pending_dates.py 2026-03 --show-done
```
