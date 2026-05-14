#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Any

VAULT_ROOT = Path(
    os.environ.get(
        "AI_OS_VAULT_ROOT",
        "/Users/resily0808/Documents/Obsidian Vault/00_AI-OS",
    )
)
PROJECTS_DIR = VAULT_ROOT / "Projects"
TEMPLATE_DIR = PROJECTS_DIR / "_Template"
GLOBAL_FILE = VAULT_ROOT / "Global.md"

FEEDBACK_LINE_WARN_THRESHOLD = 200

CORRECTION_KEYWORDS = [
    "違う",
    "そうじゃなくて",
    "そうじゃない",
    "それは違う",
    "逆",
    "しないで",
    "するな",
    "やめて",
    "また同じ",
    "何度言えば",
    "何回言えば",
    "前も言った",
    "何度も言ってる",
    "ダメ",
    "NG",
    "微妙",
    "違和感",
    "雑",
    "適当",
    "記録して",
    "忘れないで",
    "次回のために残して",
]

THREAD_MEMORY_TRIGGER_KEYWORDS = [
    "整理して記録して",
    "次回に活かしたい",
    "AIメモリに書いて",
    "メモリに書いて",
    "/handover",
    "/obsidian-log",
]

THIRD_PARTY_PATTERNS = [
    "と言われ",
    "って言われ",
    "と言ってた",
    "って言ってた",
    "と言われた",
    "って言われた",
]

DIRECT_CONTEXT_HINTS = [
    "あなた",
    "君",
    "いまの",
    "今の",
    "この返答",
    "その返答",
    "この回答",
    "その回答",
    "さっき",
    "今回",
]


def read_hook_payload() -> dict[str, Any]:
    raw = ""
    try:
        raw = os.sys.stdin.read()
    except Exception:
        return {}
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def normalize_line(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\r", " ").replace("\n", " / ")).strip()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def list_project_names() -> list[str]:
    if not PROJECTS_DIR.exists():
        return []
    names: list[str] = []
    for child in PROJECTS_DIR.iterdir():
        if child.is_dir() and child.name != "_Template":
            names.append(child.name)
    return sorted(names)


def resolve_project_name(cwd: str | None) -> str:
    projects = list_project_names()
    if not projects:
        return "unknown"
    if not cwd:
        return "unknown"

    cwd_path = Path(cwd)
    candidates: list[str] = []
    for node in [cwd_path, *list(cwd_path.parents)[:6]]:
        if node.name:
            candidates.append(node.name)
    seen = set()
    ordered = [x for x in candidates if not (x in seen or seen.add(x))]

    by_lower = {p.lower(): p for p in projects}
    for name in ordered:
        if name in projects:
            return name
        lowered = name.lower()
        if lowered in by_lower:
            return by_lower[lowered]

    cwd_lower = str(cwd_path).lower()
    hits = [p for p in projects if f"/{p.lower()}/" in cwd_lower or cwd_lower.endswith(f"/{p.lower()}")]
    if len(hits) == 1:
        return hits[0]
    return "unknown"


def project_paths(project_name: str) -> tuple[Path | None, Path | None]:
    if project_name == "unknown":
        return None, None
    project_dir = PROJECTS_DIR / project_name
    return project_dir / "Rules.md", project_dir / "Feedback.md"


def _default_rules_template(project_name: str) -> str:
    return (
        f"# Project: {project_name}\n\n"
        "## 概要\n"
        "-\n\n"
        "## 重視すること\n"
        "-\n\n"
        "## 絶対やらない（プロジェクト固有）\n"
        "-\n\n"
        "## 確定ルール\n"
        "-\n"
    )


def _default_feedback_template(project_name: str) -> str:
    return (
        f"# Feedback: {project_name}\n\n"
        "新しい指摘は **最上部** に追加（newest-on-top）。\n"
        "3回以上再発したら → `Rules.md` に行を移動して昇格。\n"
        f"**警告閾値: {FEEDBACK_LINE_WARN_THRESHOLD}行**。\n\n"
        "カテゴリタグ: `[コード]` `[UI]` `[テスト]` `[チケット]` `[コミュ]`\n\n"
        "---\n"
    )


def ensure_project_files(project_name: str) -> tuple[Path | None, Path | None]:
    rules_path, feedback_path = project_paths(project_name)
    if rules_path is None or feedback_path is None:
        return None, None

    rules_path.parent.mkdir(parents=True, exist_ok=True)

    if not rules_path.exists():
        template = TEMPLATE_DIR / "Rules.md"
        if template.exists():
            write_text(rules_path, read_text(template))
        else:
            write_text(rules_path, _default_rules_template(project_name))

    if not feedback_path.exists():
        template = TEMPLATE_DIR / "Feedback.md"
        if template.exists():
            write_text(feedback_path, read_text(template))
        else:
            write_text(feedback_path, _default_feedback_template(project_name))

    return rules_path, feedback_path


def section_text(content: str, heading: str) -> str:
    lines = content.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith(heading):
            start = i + 1
            break
    if start is None:
        return ""

    level = len(heading) - len(heading.lstrip("#"))
    end = len(lines)
    for i in range(start, len(lines)):
        raw = lines[i].strip()
        if raw.startswith("#"):
            next_level = len(raw) - len(raw.lstrip("#"))
            if next_level <= level:
                end = i
                break
    return "\n".join(lines[start:end]).strip()


def list_items(content: str) -> list[str]:
    items: list[str] = []
    for line in content.splitlines():
        match = re.match(r"^\s*(?:-|\*|\d+\.)\s+(.+?)\s*$", line)
        if match:
            item = normalize_line(match.group(1))
            if item:
                items.append(item)
    return items


def parse_feedback_entries(content: str) -> list[dict[str, str]]:
    lines = content.splitlines()
    starts: list[int] = []
    for i, line in enumerate(lines):
        if re.match(r"^###\s+\d{4}-\d{2}-\d{2}\s+\[[^\]]+\]\s*$", line.strip()):
            starts.append(i)

    entries: list[dict[str, str]] = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        block = lines[start:end]
        head = block[0].strip()
        match = re.match(r"^###\s+(\d{4}-\d{2}-\d{2})\s+\[([^\]]+)\]\s*$", head)
        if not match:
            continue
        entry_date, tag = match.group(1), match.group(2)
        original = ""
        for line in block[1:]:
            if line.strip().startswith("- 指摘(原文):"):
                original = normalize_line(line.split(":", 1)[1] if ":" in line else "")
                break
        entries.append(
            {
                "date": entry_date,
                "tag": tag,
                "original": original,
            }
        )
    return entries


def feedback_duplicate_exists(content: str, entry_date: str, original_text: str) -> bool:
    original_norm = normalize_line(original_text)
    for entry in parse_feedback_entries(content):
        if entry["date"] == entry_date and entry["original"] == original_norm:
            return True
    return False


def _insert_after_separator(existing: str, block: str) -> str:
    lines = existing.splitlines(keepends=True)
    idx = None
    for i, line in enumerate(lines):
        if line.strip() == "---":
            idx = i
            break

    clean_block = block.strip("\n")
    if idx is None:
        base = existing.rstrip("\n")
        if base:
            base += "\n\n---\n\n"
        else:
            base = "---\n\n"
        return f"{base}{clean_block}\n"

    head = "".join(lines[: idx + 1]).rstrip("\n") + "\n\n"
    tail = "".join(lines[idx + 1 :]).lstrip("\n")
    if tail:
        return f"{head}{clean_block}\n\n{tail.rstrip()}\n"
    return f"{head}{clean_block}\n"


def build_feedback_entry(
    entry_date: str,
    tag: str,
    original_text: str,
    prevention_text: str,
    related_files: str,
) -> str:
    original = normalize_line(original_text)
    prevention = normalize_line(prevention_text)
    related = normalize_line(related_files) if related_files else "-"
    return (
        f"### {entry_date} {tag}\n"
        f"- 指摘(原文): {original}\n"
        f"- 再発防止: {prevention}\n"
        f"- 関連ファイル: {related}"
    )


def append_feedback_entry(
    feedback_path: Path,
    tag: str,
    original_text: str,
    prevention_text: str,
    related_files: str = "-",
    entry_date: str | None = None,
) -> bool:
    if not feedback_path:
        return False
    if entry_date is None:
        entry_date = date.today().isoformat()

    current = read_text(feedback_path)
    if feedback_duplicate_exists(current, entry_date, original_text):
        return False

    block = build_feedback_entry(
        entry_date=entry_date,
        tag=tag,
        original_text=original_text,
        prevention_text=prevention_text,
        related_files=related_files,
    )
    updated = _insert_after_separator(current, block)
    write_text(feedback_path, updated)
    return True


def is_third_party_mention(prompt: str) -> bool:
    if not prompt:
        return False
    if not any(pat in prompt for pat in THIRD_PARTY_PATTERNS):
        return False
    return not any(hint in prompt for hint in DIRECT_CONTEXT_HINTS)


def is_feedback_signal(prompt: str) -> bool:
    text = normalize_line(prompt)
    if len(text) < 3:
        return False
    for kw in CORRECTION_KEYWORDS:
        if kw in text:
            return True
    if re.search(r"\b(?:wrong|dont|don't|stop)\b", text, re.IGNORECASE):
        return True
    return False


def should_run_thread_memory(last_prompt: str) -> bool:
    text = normalize_line(last_prompt)
    if not text:
        return False
    for kw in THREAD_MEMORY_TRIGGER_KEYWORDS:
        if kw.lower() in text.lower():
            return True
    return False


def classify_feedback_tag(prompt: str) -> str:
    text = prompt.lower()
    ticket_words = [
        "issue",
        "pr",
        "pull request",
        "コミット",
        "commit",
        "push",
        "ブランチ",
        "起票",
        "マージ",
    ]
    test_words = ["テスト", "検証", "回帰", "動作確認", "e2e", "unit", "integration", "spec"]
    ui_words = ["ui", "見た目", "レイアウト", "配置", "余白", "色", "配色", "グラフ", "文言", "フォント"]
    comm_words = ["説明", "報告", "確認", "出典", "根拠", "言い方", "語調", "トーン", "コミュ"]

    if any(w in text for w in ticket_words):
        return "[チケット]"
    if any(w in text for w in test_words):
        return "[テスト]"
    if any(w in text for w in ui_words):
        return "[UI]"
    if any(w in text for w in comm_words):
        return "[コミュ]"
    return "[コード]"


def prevention_text_for_tag(tag: str) -> str:
    table = {
        "[コード]": "実装前に要件と差分を明示し、同じ誤りを避けるチェックを入れる。",
        "[UI]": "変更前に期待レイアウトを言語化し、反映後に見た目を再確認する。",
        "[テスト]": "修正後は関連テストと回帰確認を実行し、結果を明示してから完了にする。",
        "[チケット]": "Issue/PR/コミット操作は依頼範囲を明示確認してから実行する。",
        "[コミュ]": "回答は要点先出しで、不要な前置きや内部事情を省いて伝える。",
        "[学び]": "次回開始時に read-project-memory でこの学びを確認してから着手する。",
    }
    return table.get(tag, "次回同じ条件で再発しないよう、事前チェックに追加する。")


def extract_related_files(text: str) -> str:
    found: list[str] = []
    for path in re.findall(r"`([^`]+)`", text):
        if "/" in path or path.endswith((".md", ".ts", ".tsx", ".js", ".py", ".json")):
            found.append(path)
    for path in re.findall(r"/Users/[^\s,;:]+", text):
        found.append(path)
    if not found:
        return "-"
    unique: list[str] = []
    seen: set[str] = set()
    for item in found:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
        if len(unique) >= 3:
            break
    return ", ".join(unique)


def load_user_prompts_from_transcript(transcript_path: str | None, limit: int = 400) -> list[str]:
    if not transcript_path:
        return []
    path = Path(transcript_path)
    if not path.exists():
        return []

    prompts: list[str] = []
    try:
        with path.open("r", encoding="utf-8") as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    rec = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if rec.get("type") != "event_msg":
                    continue
                payload = rec.get("payload", {})
                if not isinstance(payload, dict):
                    continue
                if payload.get("type") != "user_message":
                    continue
                msg = payload.get("message")
                if isinstance(msg, str) and msg.strip():
                    prompts.append(msg)
    except OSError:
        return []

    if len(prompts) > limit:
        return prompts[-limit:]
    return prompts


def latest_user_prompt(transcript_path: str | None) -> str:
    prompts = load_user_prompts_from_transcript(transcript_path, limit=50)
    return prompts[-1] if prompts else ""


def feedback_line_warning_text(feedback_content: str) -> str:
    lines = len(feedback_content.splitlines())
    if lines <= FEEDBACK_LINE_WARN_THRESHOLD:
        return ""
    return (
        f"⚠ Feedback.md が {lines} 行に達しています。"
        "古いエントリの Rules.md 昇格・削除を検討してください。"
    )

