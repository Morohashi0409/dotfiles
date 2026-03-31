# User Preparation

Preparation differs by role.

## Monthly Requester

The monthly requester should provide:

- the target month in `YYYY-MM`
- one attendance PDF for the month
- one Outlook or Teams calendar PDF for the month
- enough daily notes or other evidence to classify each working day
- any category or my-pattern changes since the previous run
- whether the request stops at JSON generation or continues through automatic entry

The requester does not need to:

- rename PDFs
- move files into `monthly-sources/YYYY-MM/`
- normalize times to 5-minute increments
- run validator or automator manually

The requester also does not need access to the local operator docs under `/Users/resily0808/Documents/Obsidian Vault/...`.
Those are execution-side references, not prerequisites for making a monthly request.

If the requester wants to operate mainly by chat, see `docs/conversation-guide.md`.

## Environment Owner

The environment owner should keep ready:

- Chrome started with remote debugging enabled
- a logged-in CloudLog session
- the CloudLog timesheet page open
- Playwright and Chromium installed when required
- the external runtime scripts available and runnable

## Operations Maintainer

The maintainer should keep current:

- external CloudLog contract documents
- external category guide
- runtime scripts
- any known CloudLog UI changes
- any known category or my-pattern changes

The maintainer also updates the skill summaries when the external source of truth changes.
