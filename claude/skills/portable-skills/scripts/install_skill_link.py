#!/usr/bin/env python3

import argparse
import os
import sys
from pathlib import Path


def ensure_skill_symlink(skill_dir: Path, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists() or destination.is_symlink():
        if destination.is_symlink():
            current = destination.resolve()
            if current == skill_dir:
                return destination
            destination.unlink()
        else:
            raise FileExistsError(
                f"Cannot install skill link because {destination} already exists and is not a symlink"
            )

    destination.symlink_to(skill_dir, target_is_directory=True)
    return destination


def install_skill_link(skill_dir: Path, codex_home: Path | None = None) -> dict[str, Path]:
    skill_dir = skill_dir.expanduser().resolve()
    if not (skill_dir / "SKILL.md").exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    codex_home = (codex_home or Path(os.environ.get("CODEX_HOME", "~/.codex"))).expanduser().resolve()
    claude_home = Path.home() / ".claude"

    destinations = {
        "codex": codex_home / "skills" / skill_dir.name,
        "claude": claude_home / "skills" / skill_dir.name,
    }
    return {
        name: ensure_skill_symlink(skill_dir, destination)
        for name, destination in destinations.items()
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install a dotfiles-managed skill into both ~/.codex/skills and ~/.claude/skills"
    )
    parser.add_argument("skill_dir", help="Path to the skill directory under dotfiles")
    parser.add_argument("--codex-home", help="Override CODEX_HOME for testing")
    args = parser.parse_args(argv)

    try:
        destinations = install_skill_link(
            Path(args.skill_dir),
            Path(args.codex_home) if args.codex_home else None,
        )
    except (FileNotFoundError, FileExistsError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    for name in ("codex", "claude"):
        print(f"{name}:{destinations[name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
