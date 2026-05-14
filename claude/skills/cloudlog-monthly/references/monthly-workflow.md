# Monthly Workflow

Use this flow when the user asks for monthly CloudLog preparation.

## 1. Standardize Inputs

- Confirm the month in `YYYY-MM`.
- Prefer attached files from the current thread.
- If attached files are not available, search `~/Downloads`.
- Copy the chosen PDFs into `monthly-sources/YYYY-MM/` with canonical names.
- If multiple candidates match, ask the user instead of choosing silently.
- Make sure Daily notes for the month already exist under `01_Daily/`.

## 2. Build Monthly JSON

- Read Daily notes for the month.
- Read the canonical attendance PDF.
- Read the canonical Outlook calendar PDF.
- Always check GitHub day activity before final classification, even when ticket numbers are not provided:
  - `python3 scripts/fetch_github_day_activity.py YYYY-MM-DD`
  - Default repos: `Resily/dxp`, `Resily/WellCom`; default actor: `Morohashi0409`
  - If a day includes merged or updated WellCom PR activity, reserve a matching block for `WellCom` classification.
  - Do not rely only on manually provided ticket numbers.
- Apply the category guide.
- For DXP categories, apply strict defaults:
  - Use `DXP【DX開発部】 > 会議（商品付.. > 入力不要 > 企業登録なし` only for events explicitly labeled `DXP開発定例`.
  - Use `DXP【DX開発部】 > システム運用・作業 > 入力不要 > 企業登録なし` only when evidence explicitly contains `保守`.
  - Otherwise classify into `【資産化】ワンプラットフォーム> DXP > 入力不要 > 企業登録なし`.
- Keep `time_blocks` in every entry.
- Round `attendance` and every `time_blocks` boundary to 5-minute increments before CloudLog entry.
- Recalculate each entry's `minutes` after rounding.
- Keep attendance days internally consistent so `attendance span - 60 minutes == total entry minutes`.
- Keep `attendance: null` on full-leave days that should not receive attendance times.
- Exclude legal holidays unless the user overrides that rule.

## 3. Validate

- Run the JSON validator.
- Treat non-5-minute times as blocking errors because CloudLog will not save them.
- Fix time-block mismatches or unsupported shapes before claiming readiness.
- If category uncertainty remains after notes, calendar, and GitHub review, ask the user.

## 4. Automatic Entry

- Before running the automator, always filter already-entered dates:
  - Run `scripts/filter_pending_dates.py YYYY-MM --out monthly-json/YYYY-MM_pending.json`.
  - If the pending list is empty, skip the automator and report "全日入力済み".
  - Run the automator on `YYYY-MM_pending.json`, not the full monthly JSON.
- Start Chrome with remote debugging automatically:
  ```
  bash "/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/open_cloudlog_debug_chrome.sh" &
  ```
  Wait ~8 seconds, then run the readiness check. Do not ask the user to start Chrome.
- If the readiness check shows CloudLog is on the login page, ask the user to log in and wait for confirmation before proceeding.
- Run `check_cloudlog_automator_ready.py` before the automator.
- After the automator finishes, record succeeded dates:
  - Run `scripts/filter_pending_dates.py YYYY-MM --mark-done DATE ...` for each success.
- Automatic entry is the default path for this workflow.
- Manual browser clicking is fallback only when the user explicitly asks for it.
- Completion means saved days are confirmed, not just that the script was started.

## Questions To Surface

- Which month should be prepared if the month is not explicit
- Which PDF is correct if multiple download candidates exist
- How to classify a day when evidence is too weak
- Whether the month-end incomplete day should be excluded or marked for later
- Whether CloudLog categories or my-patterns changed since the previous month
