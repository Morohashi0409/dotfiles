---
name: cloudlog-monthly
description: Prepare monthly CloudLog source files, generate month JSON, validate it, and execute automatic CloudLog entry. Use when the user needs end-to-end monthly CloudLog preparation.
---

# CloudLog Monthly

## Overview

Prepare one month of CloudLog inputs end to end. Standardize the source PDFs into fixed paths, generate `YYYY-MM_cloudlog.json`, normalize it for CloudLog's 5-minute constraints, validate it, and run the existing automation when the user wants the month entered into CloudLog.

Read [references/path-conventions.md](references/path-conventions.md) for the fixed folder layout.
Read [references/monthly-workflow.md](references/monthly-workflow.md) for the monthly flow and escalation rules.
Read [references/automatic-entry-contract.md](references/automatic-entry-contract.md) for what the user must prepare and what "ready for automatic entry" means.
Read `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md` when you need the exact JSON contract for `validate_json.py` or the exact UI behavior of `cloudlog_automator.py`.

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
   - Keep the input JSON minimal, but preserve `time_blocks`.
   - Before handing the JSON to CloudLog, normalize it to CloudLog-ready 5-minute increments.
   - Both `attendance` and every `time_blocks` boundary must be 5-minute aligned.
   - Recalculate `minutes` from the rounded `time_blocks`.
   - When `attendance` is present, keep the day total consistent with the rounded blocks so CloudLog summary totals match.
   - Exclude legal holidays unless the user says otherwise.
   - Keep `attendance: null` for full-leave days when no attendance time should be entered.
5. Validate the JSON with `validate_json.py`.
6. If the user wants automatic entry, use `cloudlog_automator.py`.
   - The user must already be logged into CloudLog in a Chrome debug session and have the timesheet page available.
   - Read the automation and JSON contract if there is any doubt about field meaning or automator behavior.
   - Run the readiness check before the automation.
   - Run the automation against the generated monthly JSON.
   - Confirm that the month saved successfully, or isolate the failed days and ask the user only when the automation cannot recover.
   - Do not fall back to manual browser clicking unless the user explicitly asks.

## User Must Prepare

- The target month in `YYYY-MM`.
- Daily notes under `/Users/resily0808/Documents/Obsidian Vault/01_Daily/` for the month.
- One attendance PDF for that month.
- One Outlook or Teams calendar PDF for that month.
- Any category or my-pattern changes that happened since the previous run.
- For automatic entry, a logged-in Chrome debug session on CloudLog's timesheet page.

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
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/prepare_monthly_sources.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/check_monthly_inputs.py 2026-03
python3 /Users/resily0808/dotfiles/claude/skills/cloudlog-monthly/scripts/normalize_cloudlog_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json --in-place
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/validate_json.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/check_cloudlog_automator_ready.py 2026-03
python3 /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/cloudlog_automator.py /Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/monthly-json/2026-03_cloudlog.json
```
