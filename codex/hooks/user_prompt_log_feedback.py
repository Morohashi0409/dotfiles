#!/usr/bin/env python3
from __future__ import annotations

import ai_os_memory as mem


def main() -> int:
    payload = mem.read_hook_payload()
    if payload.get("hook_event_name") != "UserPromptSubmit":
        return 0

    prompt = str(payload.get("prompt", ""))
    if not mem.is_feedback_signal(prompt):
        return 0
    if mem.is_third_party_mention(prompt):
        return 0

    project = mem.resolve_project_name(str(payload.get("cwd", "")))
    _, feedback_path = mem.ensure_project_files(project)
    if not feedback_path:
        return 0

    tag = mem.classify_feedback_tag(prompt)
    prevention = mem.prevention_text_for_tag(tag)
    related = mem.extract_related_files(prompt)
    mem.append_feedback_entry(
        feedback_path=feedback_path,
        tag=tag,
        original_text=prompt,
        prevention_text=prevention,
        related_files=related,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

