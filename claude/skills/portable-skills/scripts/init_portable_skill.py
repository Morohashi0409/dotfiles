#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from install_skill_link import install_skill_link  # noqa: E402
from sync_openai_yaml import sync_openai_yaml  # noqa: E402


ALLOWED_RESOURCES = {"scripts", "references", "assets"}


def normalize_skill_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", name.strip().lower())
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not normalized:
        raise ValueError("Skill name must contain at least one letter or digit")
    return normalized


def title_case_skill_name(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def starter_skill_md(skill_name: str) -> str:
    title = title_case_skill_name(skill_name)
    return (
        "---\n"
        f"name: {skill_name}\n"
        f"description: Create or update {skill_name} workflows. Use when the user needs this skill's domain-specific process or tooling.\n"
        "---\n\n"
        f"# {title}\n\n"
        "## Overview\n\n"
        "Replace this starter content with the shared instructions that should work in both Claude Code and Codex.\n"
    )


def parse_resources(resources: list[str] | None) -> list[str]:
    if not resources:
        return []
    invalid = sorted(set(resources) - ALLOWED_RESOURCES)
    if invalid:
        raise ValueError(
            f"Unknown resource types: {', '.join(invalid)}. Allowed: {', '.join(sorted(ALLOWED_RESOURCES))}"
        )
    return resources


def initialize_skill(
    skill_name: str,
    root: Path,
    resources: list[str] | None = None,
    force: bool = False,
    install: bool = True,
) -> Path:
    normalized_name = normalize_skill_name(skill_name)
    selected_resources = parse_resources(resources)
    root = root.expanduser().resolve()
    skill_dir = root / normalized_name

    if skill_dir.exists() and not force:
        raise FileExistsError(f"Skill directory already exists: {skill_dir}")

    skill_dir.mkdir(parents=True, exist_ok=force)
    (skill_dir / "SKILL.md").write_text(starter_skill_md(normalized_name))

    for resource in selected_resources:
        (skill_dir / resource).mkdir(exist_ok=True)

    sync_openai_yaml(skill_dir)
    if install:
        install_skill_link(skill_dir)
    return skill_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize a dotfiles-managed portable skill")
    parser.add_argument("skill_name", help="Skill name or title")
    parser.add_argument("--root", required=True, help="Root directory that contains skill folders")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated optional resource directories: scripts,references,assets",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing skill directory")
    parser.set_defaults(install=True)
    parser.add_argument(
        "--install",
        dest="install",
        action="store_true",
        help="Install the skill into both ~/.codex/skills and ~/.claude/skills",
    )
    parser.add_argument(
        "--no-install",
        dest="install",
        action="store_false",
        help="Skip installing the skill into both ~/.codex/skills and ~/.claude/skills",
    )
    args = parser.parse_args(argv)

    resources = [item.strip() for item in args.resources.split(",") if item.strip()]
    try:
        skill_dir = initialize_skill(
            args.skill_name,
            Path(args.root),
            resources=resources,
            force=args.force,
            install=args.install,
        )
    except (FileExistsError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
