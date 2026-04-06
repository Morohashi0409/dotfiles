#!/usr/bin/env python3

import argparse
import json
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from audit_skill_portability import audit_skill_portability  # noqa: E402
from install_skill_link import install_skill_link  # noqa: E402
from sync_openai_yaml import sync_openai_yaml  # noqa: E402


QUICK_VALIDATE = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"


def run_quick_validate(skill_dir: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(QUICK_VALIDATE), str(skill_dir)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "quick_validate failed")
    return (result.stdout or "Skill is valid!").strip()


def prepare_portable_skill(skill_dir: Path) -> dict[str, object]:
    skill_dir = skill_dir.expanduser().resolve()
    validation_output = run_quick_validate(skill_dir)
    openai_yaml = sync_openai_yaml(skill_dir)
    link_paths = install_skill_link(skill_dir)
    audit = audit_skill_portability(skill_dir)
    return {
        "skill_dir": str(skill_dir),
        "validation": validation_output,
        "openai_yaml": str(openai_yaml),
        "link_paths": {name: str(path) for name, path in link_paths.items()},
        "audit": audit,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate, sync, install, and audit a dotfiles-managed portable skill"
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args(argv)

    try:
        report = prepare_portable_skill(Path(args.skill_dir))
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["audit"]["status"] == "safe" else 1


if __name__ == "__main__":
    raise SystemExit(main())
