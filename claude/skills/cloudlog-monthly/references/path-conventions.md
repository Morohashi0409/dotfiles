# Path Conventions

Use these fixed paths for monthly CloudLog preparation.

## Canonical Layout

```text
/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog/
├── monthly-sources/
│   └── YYYY-MM/
│       ├── YYYY-MM_attendance.pdf
│       └── YYYY-MM_outlook-calendar.pdf
├── monthly-json/
│   └── YYYY-MM_cloudlog.json
├── cloudlog_automator.py
├── validate_json.py
└── クラウドログ分類と運用ガイド.md
```

## Source Priority

1. File paths explicitly attached or pasted in the current thread
2. Existing canonical files under `monthly-sources/YYYY-MM/`
3. Candidate PDFs under `/Users/resily0808/Downloads/`

If step 3 is used, copy the file into the canonical monthly folder and rename it to the canonical filename before reading it.

## Canonical Names

- Attendance PDF: `YYYY-MM_attendance.pdf`
- Outlook calendar PDF: `YYYY-MM_outlook-calendar.pdf`
- Monthly JSON: `YYYY-MM_cloudlog.json`

## Related Inputs

- Daily notes root: `/Users/resily0808/Documents/Obsidian Vault/01_Daily`
- CloudLog root: `/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog`

## Missing Data Rule

If the canonical monthly PDFs are missing after checking attached paths and `~/Downloads`, stop and ask the user for the missing file instead of guessing.
