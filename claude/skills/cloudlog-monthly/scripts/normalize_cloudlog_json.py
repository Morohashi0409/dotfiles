#!/usr/bin/env python3
"""
Normalize a CloudLog monthly JSON file into CloudLog-ready 5-minute increments.

Rules:
- Round all attendance times and work time block boundaries to the nearest 5 minutes.
- Recalculate each entry's minutes from the rounded time blocks.
- When attendance exists, derive clock_in/clock_out from the rounded first/last block
  so that attendance span minus lunch (60 minutes) matches the total logged minutes.
"""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path


def parse_time(value: str) -> int:
    hours, minutes = map(int, value.split(":"))
    return hours * 60 + minutes


def format_time(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def round_to_nearest_five(total_minutes: int) -> int:
    return ((total_minutes + 2) // 5) * 5


def normalize_block(block: str) -> tuple[str, int, int]:
    start_raw, end_raw = [part.strip() for part in block.split("-")]
    start = round_to_nearest_five(parse_time(start_raw))
    end = round_to_nearest_five(parse_time(end_raw))
    if end <= start:
        end = start + 5
    return f"{format_time(start)}-{format_time(end)}", start, end


def normalize_entry(entry: dict) -> tuple[dict, list[tuple[int, int]]]:
    updated = deepcopy(entry)
    normalized_blocks = []
    spans = []

    for block in entry.get("time_blocks", []):
        normalized, start, end = normalize_block(block)
        normalized_blocks.append(normalized)
        spans.append((start, end))

    updated["time_blocks"] = normalized_blocks
    updated["minutes"] = sum(end - start for start, end in spans)
    return updated, spans


def normalize_day(day: dict) -> dict:
    updated = deepcopy(day)
    normalized_entries = []
    all_spans = []

    for entry in day.get("cloudlog_entries", []):
        normalized_entry, spans = normalize_entry(entry)
        normalized_entries.append(normalized_entry)
        all_spans.extend(spans)

    updated["cloudlog_entries"] = normalized_entries

    attendance = day.get("attendance")
    if attendance is None:
        updated["attendance"] = None
        return updated

    if all_spans:
        starts = [start for start, _ in all_spans]
        ends = [end for _, end in all_spans]
        updated["attendance"] = {
            "clock_in": format_time(min(starts)),
            "clock_out": format_time(max(ends)),
        }
    else:
        normalized_attendance = deepcopy(attendance)
        for key in ("clock_in", "clock_out"):
            value = attendance.get(key)
            if value:
                normalized_attendance[key] = format_time(
                    round_to_nearest_five(parse_time(value))
                )
        updated["attendance"] = normalized_attendance

    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.json_path.read_text(encoding="utf-8"))
    normalized = [normalize_day(day) for day in data]

    if args.in_place:
        args.json_path.write_text(
            json.dumps(normalized, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print(json.dumps(normalized, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
