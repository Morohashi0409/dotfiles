# Automatic Entry Contract

Use this reference when the user wants the skill to go beyond JSON generation and actually register the month in CloudLog.

For the exact field contract consumed by `validate_json.py` and the exact UI behavior executed by `cloudlog_automator.py`, also read `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/AUTOMATION_AND_JSON_CONTRACT.md`.

## What The Skill Does

This skill is responsible for the full monthly path:

1. identify the month
2. collect the monthly source files
3. build the monthly JSON
4. normalize all times to 5-minute increments
5. validate that the JSON is CloudLog-safe
6. run the automatic entry script
7. report which days were saved and which days still need user confirmation

Treat automatic entry as the default destination for this skill unless the user explicitly asks for JSON generation only.

## What The User Must Prepare

The user should provide or already have the following:

- the target month in `YYYY-MM`
- Daily notes for the month under `/Users/resily0808/Documents/Obsidian Vault/01_Daily/`
- one attendance PDF for the month
- one Outlook or Teams calendar PDF for the month
- any category or my-pattern changes that affect CloudLog category selection

For automatic entry, the user must also prepare:

- Chrome started with remote debugging enabled
- a logged-in CloudLog session
- the CloudLog timesheet page open

The user does not need to rename the PDFs manually. The skill should prefer attached file paths first, then canonical monthly files, then `~/Downloads`.

## Minimum User Checklist

Before automatic entry, the minimum checklist is:

- month is known
- Daily notes are filled enough to classify each working day
- attendance PDF exists
- calendar PDF exists
- CloudLog category mapping has not silently changed
- CloudLog is open and logged in

If any item is missing, stop and ask instead of guessing.

## What Counts As Ready

The month is ready for automatic entry only when all of the following are true:

- the canonical source PDFs exist under `monthly-sources/YYYY-MM/`
- `monthly-json/YYYY-MM_cloudlog.json` exists
- every `attendance` time is 5-minute aligned
- every `time_blocks` boundary is 5-minute aligned
- each entry's `minutes` matches the rounded block totals
- each attendance day satisfies the validator's total-time rules
- `needs_confirmation` days are isolated and intentionally skipped
- the CloudLog readiness check passes

## Default Agent Behavior

When this skill triggers, follow this default behavior:

1. prepare or verify canonical PDFs
2. build or refresh the monthly JSON
3. normalize the JSON for CloudLog
4. validate the JSON
5. if the user asked for automatic entry, run the readiness check and then run the automator
6. if only a subset of days fails during automatic entry, fix recoverable automation issues and retry
7. ask the user only for missing evidence, category ambiguity, or unrecoverable UI changes

## Stop And Ask

Stop and ask the user when:

- the required PDF is missing after checking both attachments and `~/Downloads`
- multiple PDFs look plausible for the same month
- Daily notes and GitHub history still do not justify a category split
- a category path no longer matches the current CloudLog UI or my-pattern list
- CloudLog UI changed enough that the automator cannot safely proceed

## Completion Criteria

When automatic entry is requested, do not stop at "JSON was generated." Completion means:

- the JSON is validated
- the automator has run
- saved days are reported explicitly
- failed or skipped days are listed explicitly with the reason

If the current session still does not show the skill in a candidate list after installation, explain that the app may need a skill-list refresh or a new thread.
