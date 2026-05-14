#!/usr/bin/env python3
from __future__ import annotations

import ai_os_memory as mem


def pick(values: list[str], count: int, fallback: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = mem.normalize_line(value)
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
        if len(out) >= count:
            return out
    for value in fallback:
        value = mem.normalize_line(value)
        if value and value not in seen:
            out.append(value)
            if len(out) >= count:
                return out
    return out[:count]


def main() -> int:
    payload = mem.read_hook_payload()
    if payload.get("hook_event_name") != "SessionStart":
        return 0

    source = str(payload.get("source", ""))
    if source not in {"startup", "resume", "clear"}:
        return 0

    cwd = str(payload.get("cwd", ""))
    project = mem.resolve_project_name(cwd)
    rules_path, feedback_path = mem.ensure_project_files(project)

    global_text = mem.read_text(mem.GLOBAL_FILE)
    rules_text = mem.read_text(rules_path) if rules_path else ""
    feedback_text = mem.read_text(feedback_path) if feedback_path else ""

    quality_section = mem.section_text(global_text, "## 期待品質")
    dont_section = mem.section_text(global_text, "## 絶対やらない")
    project_priority = mem.section_text(rules_text, "### 優先ルール")
    project_rules = mem.section_text(rules_text, "## 確定ルール")

    must_candidates = (
        mem.list_items(quality_section)
        + mem.list_items(project_priority)
        + mem.list_items(project_rules)
    )
    dont_candidates = mem.list_items(dont_section)

    recent_feedback = mem.parse_feedback_entries(feedback_text)
    confirm_candidates: list[str] = []
    if recent_feedback:
        top = recent_feedback[0]
        if top.get("original"):
            confirm_candidates.append(f"直近指摘: {top['original']}")
    if rules_text:
        rules_items = mem.list_items(project_priority) + mem.list_items(project_rules)
        if rules_items:
            confirm_candidates.append(f"優先ルール: {rules_items[0]}")

    must = pick(
        must_candidates,
        3,
        [
            "要件を外さない",
            "既存変更を勝手に巻き戻さない",
            "不確実な前提を断定しない",
        ],
    )
    dont = pick(
        dont_candidates,
        3,
        [
            "明示承認なしに外部書き込みをしない",
            "調査依頼で勝手に改修しない",
            "根拠なく推測で文言や実装を変えない",
        ],
    )
    checks = pick(
        confirm_candidates,
        2,
        ["プロジェクト固有ルールが未読なら Rules.md を確認する"],
    )

    lines = [
        f"【AI-OS 事前読み込み: {project}】",
        "■ 今回守る 3 点:",
        f"- {must[0]}",
        f"- {must[1]}",
        f"- {must[2]}",
        "■ やらない 3 点:",
        f"- {dont[0]}",
        f"- {dont[1]}",
        f"- {dont[2]}",
        "■ 要確認:",
    ]
    for item in checks:
        lines.append(f"- {item}")

    warn = mem.feedback_line_warning_text(feedback_text)
    if warn:
        lines.append(warn)

    print("\n".join(lines[:15]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

