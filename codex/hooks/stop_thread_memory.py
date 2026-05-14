#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import ai_os_memory as mem

STATE_FILE = Path.home() / ".codex" / "hooks_state" / "thread_memory_stop_seen.txt"


def load_seen_keys() -> set[str]:
    if not STATE_FILE.exists():
        return set()
    try:
        return {line.strip() for line in STATE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()}
    except OSError:
        return set()


def save_seen_key(key: str) -> None:
    existing: list[str] = []
    if STATE_FILE.exists():
        try:
            existing = [line.strip() for line in STATE_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
        except OSError:
            existing = []

    if key in existing:
        return
    existing.append(key)
    if len(existing) > 1000:
        existing = existing[-1000:]
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text("\n".join(existing) + "\n", encoding="utf-8")


def emit_continue(system_message: str | None = None) -> int:
    payload: dict[str, object] = {"continue": True}
    if system_message:
        payload["systemMessage"] = system_message
    print(json.dumps(payload, ensure_ascii=False))
    return 0


def main() -> int:
    payload = mem.read_hook_payload()
    if payload.get("hook_event_name") != "Stop":
        return emit_continue()

    if payload.get("stop_hook_active") is True:
        return emit_continue()

    session_id = str(payload.get("session_id", ""))
    turn_id = str(payload.get("turn_id", ""))
    idempotency_key = f"{session_id}:{turn_id}".strip(":")
    if idempotency_key:
        seen = load_seen_keys()
        if idempotency_key in seen:
            return emit_continue()
        save_seen_key(idempotency_key)

    transcript_path = payload.get("transcript_path")
    last_prompt = mem.latest_user_prompt(transcript_path if isinstance(transcript_path, str) else None)
    if not mem.should_run_thread_memory(last_prompt):
        return emit_continue()

    project = mem.resolve_project_name(str(payload.get("cwd", "")))
    _, feedback_path = mem.ensure_project_files(project)
    if not feedback_path:
        return emit_continue()

    prompts = mem.load_user_prompts_from_transcript(
        transcript_path if isinstance(transcript_path, str) else None,
        limit=500,
    )

    added = 0
    seen_prompt: set[str] = set()
    for prompt in prompts:
        if not mem.is_feedback_signal(prompt):
            continue
        if mem.is_third_party_mention(prompt):
            continue
        normalized = mem.normalize_line(prompt)
        if normalized in seen_prompt:
            continue
        seen_prompt.add(normalized)

        tag = mem.classify_feedback_tag(prompt)
        if mem.append_feedback_entry(
            feedback_path=feedback_path,
            tag=tag,
            original_text=prompt,
            prevention_text=mem.prevention_text_for_tag(tag),
            related_files=mem.extract_related_files(prompt),
        ):
            added += 1

    if any(word in last_prompt for word in ["学び", "気づき", "次回に活かしたい"]):
        if mem.append_feedback_entry(
            feedback_path=feedback_path,
            tag="[学び]",
            original_text=last_prompt,
            prevention_text=mem.prevention_text_for_tag("[学び]"),
            related_files=mem.extract_related_files(last_prompt),
        ):
            added += 1

    if added == 0:
        return emit_continue()
    return emit_continue(f"thread-memory: {added} 件を記録 ({feedback_path})")


if __name__ == "__main__":
    raise SystemExit(main())
