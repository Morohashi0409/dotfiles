#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


DEFAULT_CLOUDLOG_ROOT = Path("/Users/resily0808/Documents/Obsidian Vault/04_Document/2_Process/CloudLog")
DEFAULT_DAILY_ROOT = Path("/Users/resily0808/Documents/Obsidian Vault/01_Daily")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether the canonical monthly CloudLog inputs exist."
    )
    parser.add_argument("month", help="Target month in YYYY-MM")
    parser.add_argument(
        "--cloudlog-root",
        default=str(DEFAULT_CLOUDLOG_ROOT),
        help="CloudLog root directory",
    )
    parser.add_argument(
        "--daily-root",
        default=str(DEFAULT_DAILY_ROOT),
        help="Daily note root directory",
    )
    return parser.parse_args()


def ensure_month(month: str) -> str:
    if not MONTH_RE.match(month):
        raise ValueError("month must use YYYY-MM")
    return month


def main() -> int:
    args = parse_args()

    try:
        month = ensure_month(args.month)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    cloudlog_root = Path(args.cloudlog_root).expanduser().resolve()
    daily_root = Path(args.daily_root).expanduser().resolve()
    month_dir = cloudlog_root / "monthly-sources" / month

    checks = {
        "attendance_pdf": month_dir / f"{month}_attendance.pdf",
        "outlook_calendar_pdf": month_dir / f"{month}_outlook-calendar.pdf",
        "monthly_json_dir": cloudlog_root / "monthly-json",
        "category_guide": cloudlog_root / "クラウドログ分類と運用ガイド.md",
        "validator": cloudlog_root / "validate_json.py",
        "automator": cloudlog_root / "cloudlog_automator.py",
        "daily_root": daily_root,
    }

    report = {
        "month": month,
        "status": "ready",
        "paths": {key: str(path) for key, path in checks.items()},
        "daily_notes_found": len(list(daily_root.glob(f"{month}-*.md"))) if daily_root.exists() else 0,
        "missing": [],
    }

    for key, path in checks.items():
        if not path.exists():
            report["missing"].append({"key": key, "path": str(path)})

    if report["daily_notes_found"] == 0:
        report["missing"].append({"key": "daily_notes_for_month", "path": f"{daily_root}/{month}-*.md"})

    if report["missing"]:
        report["status"] = "missing"

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
