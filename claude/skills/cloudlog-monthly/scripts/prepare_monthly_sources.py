#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


DEFAULT_CLOUDLOG_ROOT = Path("/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog")
DEFAULT_DOWNLOADS_DIR = Path("/Users/resily0808/Downloads")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy and rename monthly CloudLog source PDFs into the canonical folder layout."
    )
    parser.add_argument("month", help="Target month in YYYY-MM")
    parser.add_argument("--attendance", help="Explicit attendance PDF path")
    parser.add_argument("--calendar", help="Explicit Outlook calendar PDF path")
    parser.add_argument(
        "--cloudlog-root",
        default=str(DEFAULT_CLOUDLOG_ROOT),
        help="CloudLog root directory",
    )
    parser.add_argument(
        "--downloads-dir",
        default=str(DEFAULT_DOWNLOADS_DIR),
        help="Downloads directory used when explicit file paths are omitted",
    )
    parser.add_argument(
        "--move",
        action="store_true",
        help="Move files instead of copying them",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite canonical destination files if they already exist",
    )
    return parser.parse_args()


def ensure_month(month: str) -> str:
    if not MONTH_RE.match(month):
        raise ValueError("month must use YYYY-MM")
    return month


def canonical_paths(cloudlog_root: Path, month: str) -> dict[str, Path]:
    month_dir = cloudlog_root / "monthly-sources" / month
    return {
        "month_dir": month_dir,
        "attendance": month_dir / f"{month}_attendance.pdf",
        "calendar": month_dir / f"{month}_outlook-calendar.pdf",
    }


def list_pdfs(downloads_dir: Path) -> list[Path]:
    if not downloads_dir.exists():
        return []
    return sorted(
        [path for path in downloads_dir.iterdir() if path.is_file() and path.suffix.lower() == ".pdf"],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def find_attendance_candidates(downloads_dir: Path, month: str) -> list[Path]:
    compact = month.replace("-", "")
    results = []
    for path in list_pdfs(downloads_dir):
        name = path.name.lower()
        if compact not in name:
            continue
        if any(keyword in name for keyword in ("teams", "calendar", "outlook")):
            continue
        results.append(path)
    return results


def find_calendar_candidates(downloads_dir: Path) -> list[Path]:
    results = []
    for path in list_pdfs(downloads_dir):
        name = path.name.lower()
        if any(keyword in name for keyword in ("teams", "calendar", "outlook")):
            results.append(path)
    return results


def copy_or_move(src: Path, dest: Path, move: bool) -> None:
    if move:
        shutil.move(str(src), str(dest))
        return
    shutil.copy2(src, dest)


def resolve_source(explicit_path: str | None, candidates: list[Path]) -> tuple[Path | None, list[str]]:
    if explicit_path:
        explicit = Path(explicit_path).expanduser().resolve()
        if not explicit.exists():
            return None, [f"explicit path not found: {explicit}"]
        return explicit, []

    if not candidates:
        return None, ["no candidate found"]

    if len(candidates) > 1:
        return None, [str(candidate) for candidate in candidates]

    return candidates[0], []


def main() -> int:
    args = parse_args()

    try:
        month = ensure_month(args.month)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    cloudlog_root = Path(args.cloudlog_root).expanduser().resolve()
    downloads_dir = Path(args.downloads_dir).expanduser().resolve()
    paths = canonical_paths(cloudlog_root, month)
    paths["month_dir"].mkdir(parents=True, exist_ok=True)

    attendance_src, attendance_issue = resolve_source(
        args.attendance,
        find_attendance_candidates(downloads_dir, month),
    )
    calendar_src, calendar_issue = resolve_source(
        args.calendar,
        find_calendar_candidates(downloads_dir),
    )

    report = {
        "month": month,
        "destination_dir": str(paths["month_dir"]),
        "resolved": {
            "attendance": str(attendance_src) if attendance_src else None,
            "calendar": str(calendar_src) if calendar_src else None,
        },
        "written": {},
        "missing_or_ambiguous": {},
    }

    for key, src, issues in (
        ("attendance", attendance_src, attendance_issue),
        ("calendar", calendar_src, calendar_issue),
    ):
        dest = paths[key]
        if src is None:
            report["missing_or_ambiguous"][key] = issues
            continue

        if dest.exists() and not args.force:
            report["written"][key] = f"exists: {dest}"
            continue

        copy_or_move(src, dest, args.move)
        report["written"][key] = str(dest)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["missing_or_ambiguous"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
