#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---(?:\n|$)", re.DOTALL)
TRAILING_CONNECTORS = {"a", "an", "and", "as", "at", "both", "for", "in", "of", "or", "so", "the", "to", "with"}
DISPLAY_TOKEN_OVERRIDES = {
    "cloudlog": "CloudLog",
    "github": "GitHub",
}


class FrontmatterError(ValueError):
    pass


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def extract_frontmatter_block(content: str) -> str:
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise FrontmatterError("No YAML frontmatter found")
    return match.group(1)


def parse_frontmatter_text(content: str) -> dict[str, str]:
    block = extract_frontmatter_block(content)
    data: dict[str, str] = {}
    multiline_key: str | None = None
    multiline_buffer: list[str] = []

    for line in block.splitlines():
        if multiline_key is not None:
            if line.startswith(" ") or line.startswith("\t"):
                multiline_buffer.append(line.lstrip())
                continue
            data[multiline_key] = "\n".join(multiline_buffer).strip()
            multiline_key = None
            multiline_buffer = []

        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            continue

        if value in {"|", ">"}:
            multiline_key = key
            multiline_buffer = []
            continue

        data[key] = strip_quotes(value)

    if multiline_key is not None:
        data[multiline_key] = "\n".join(multiline_buffer).strip()

    return data


def parse_skill_frontmatter(skill_path: Path) -> dict[str, str]:
    skill_md = skill_path if skill_path.name == "SKILL.md" else skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_md}")

    frontmatter = parse_frontmatter_text(skill_md.read_text())
    for required_key in ("name", "description"):
        value = frontmatter.get(required_key, "").strip()
        if not value:
            raise FrontmatterError(f"Missing required frontmatter key: {required_key}")
        frontmatter[required_key] = value
    return frontmatter


def title_case_skill_name(name: str) -> str:
    words = []
    for part in name.split("-"):
        words.append(DISPLAY_TOKEN_OVERRIDES.get(part, part.capitalize()))
    return " ".join(words)


def shorten_text(text: str, max_len: int = 60) -> str:
    compact = " ".join(text.replace("\n", " ").split()).strip().rstrip(".")
    if len(compact) <= max_len:
        return trim_trailing_connectors(compact)
    candidate = compact[: max_len + 1].rsplit(" ", 1)[0].rstrip(" ,;:-")
    if len(candidate) >= max(20, max_len // 2):
        return trim_trailing_connectors(candidate)
    return trim_trailing_connectors(compact[:max_len].rstrip(" ,;:-"))


def trim_trailing_connectors(text: str) -> str:
    words = text.split()
    while len(words) > 1 and words[-1].lower() in TRAILING_CONNECTORS:
        words.pop()
    return " ".join(words)


def action_phrase(description: str) -> str:
    first_sentence = description.split(". Use when", 1)[0].strip()
    if not first_sentence:
        first_sentence = description.split(".", 1)[0].strip()
    return first_sentence.rstrip(".")


def derive_interface_fields(name: str, description: str) -> dict[str, str]:
    display_name = title_case_skill_name(name)
    summary = action_phrase(description)
    short_description = shorten_text(summary)
    if summary:
        prompt_action = summary[0].lower() + summary[1:]
    else:
        prompt_action = f"use {name}"

    return {
        "display_name": display_name,
        "short_description": short_description,
        "default_prompt": f"Use ${name} to {prompt_action}.",
    }


def render_openai_yaml(interface: dict[str, str]) -> str:
    lines = ["interface:"]
    for key in ("display_name", "short_description", "default_prompt"):
        lines.append(f"  {key}: {json.dumps(interface[key], ensure_ascii=False)}")
    lines.append("")
    return "\n".join(lines)


def sync_openai_yaml(skill_dir: Path) -> Path:
    frontmatter = parse_skill_frontmatter(skill_dir)
    interface = derive_interface_fields(frontmatter["name"], frontmatter["description"])
    output_path = skill_dir / "agents" / "openai.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_openai_yaml(interface))
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate or refresh Codex agents/openai.yaml from SKILL.md"
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args(argv)

    try:
        output_path = sync_openai_yaml(Path(args.skill_dir).expanduser().resolve())
    except (FileNotFoundError, FrontmatterError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
