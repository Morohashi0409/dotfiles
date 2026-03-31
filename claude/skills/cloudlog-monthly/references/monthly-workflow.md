# Monthly Workflow

Use this flow when the user asks for monthly CloudLog preparation.

## 1. Standardize Inputs

- Confirm the month in `YYYY-MM`.
- Prefer attached files from the current thread.
- If attached files are not available, search `~/Downloads`.
- Copy the chosen PDFs into `monthly-sources/YYYY-MM/` with canonical names.
- If multiple candidates match, ask the user instead of choosing silently.

## 2. Build Monthly JSON

- Read Daily notes for the month.
- Read the canonical attendance PDF.
- Read the canonical Outlook calendar PDF.
- Check GitHub activity when notes are thin.
- Apply the category guide.
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

- Use the validated monthly JSON as the input to `cloudlog_automator.py`.
- The user should log into CloudLog in a Chrome debug window first.
- Automatic entry is the default path for this workflow.
- Manual browser clicking is fallback only when the user explicitly asks for it.

## Questions To Surface

- Which month should be prepared if the month is not explicit
- Which PDF is correct if multiple download candidates exist
- How to classify a day when evidence is too weak
- Whether the month-end incomplete day should be excluded or marked for later
