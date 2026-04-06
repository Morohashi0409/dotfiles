#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sync_openai_yaml import (  # noqa: E402
    FrontmatterError,
    derive_interface_fields,
    parse_skill_frontmatter,
    render_openai_yaml,
)


SAFE_SHARED_KEYS = {"name", "description", "license", "metadata", "allowed-tools"}
CLAUDE_LEGACY_KEYS = {"user-invocable"}


def make_finding(level: str, message: str) -> dict[str, str]:
    return {"level": level, "message": message}


def compute_status(findings: list[dict[str, str]]) -> str:
    levels = {finding["level"] for finding in findings}
    if "error" in levels:
        return "risky"
    if "warning" in levels:
        return "recommended-update"
    return "safe"


def codex_skill_link_target(skill_dir: Path) -> Path:
    codex_home = Path.home() / ".codex"
    return codex_home / "skills" / skill_dir.name


def claude_skill_link_target(skill_dir: Path) -> Path:
    return Path.home() / ".claude" / "skills" / skill_dir.name


def audit_link_target(skill_dir: Path, link_path: Path, product_name: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not link_path.exists():
        findings.append(
            make_finding(
                "warning",
                f"Skill is not installed into {link_path}; run install_skill_link.py so {product_name} can discover it.",
            )
        )
    elif not link_path.is_symlink():
        findings.append(
            make_finding(
                "warning",
                f"Expected {link_path} to be a symlink to the dotfiles skill, but it is a regular path.",
            )
        )
    else:
        resolved = link_path.resolve()
        if resolved != skill_dir:
            findings.append(
                make_finding(
                    "warning",
                    f"{link_path} points to {resolved}, not {skill_dir}; refresh it with install_skill_link.py.",
                )
            )
    return findings


def audit_skill_portability(skill_dir: Path) -> dict[str, object]:
    skill_dir = skill_dir.expanduser().resolve()
    findings: list[dict[str, str]] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        findings.append(make_finding("error", f"Missing SKILL.md in {skill_dir}"))
        return {"status": compute_status(findings), "findings": findings}

    try:
        frontmatter = parse_skill_frontmatter(skill_dir)
    except FileNotFoundError as exc:
        findings.append(make_finding("error", str(exc)))
        return {"status": compute_status(findings), "findings": findings}
    except FrontmatterError as exc:
        findings.append(make_finding("error", str(exc)))
        return {"status": compute_status(findings), "findings": findings}

    raw_lines = skill_md.read_text().splitlines()
    frontmatter_keys: list[str] = []
    inside_frontmatter = False
    for line in raw_lines:
        if line.strip() == "---":
            if not inside_frontmatter:
                inside_frontmatter = True
                continue
            break
        if not inside_frontmatter:
            continue
        if not line.strip() or line.startswith(" ") or line.startswith("\t") or ":" not in line:
            continue
        frontmatter_keys.append(line.split(":", 1)[0].strip())

    for key in frontmatter_keys:
        if key in CLAUDE_LEGACY_KEYS:
            findings.append(
                make_finding(
                    "warning",
                    f"Frontmatter key '{key}' is Claude-legacy; keep it only if current workflows still require it.",
                )
            )
        elif key not in SAFE_SHARED_KEYS:
            findings.append(
                make_finding(
                    "warning",
                    f"Frontmatter key '{key}' is not part of the recommended shared portability baseline.",
                )
            )

    interface = derive_interface_fields(frontmatter["name"], frontmatter["description"])
    expected_openai_yaml = render_openai_yaml(interface)
    openai_yaml_path = skill_dir / "agents" / "openai.yaml"

    if not openai_yaml_path.exists():
        findings.append(
            make_finding(
                "warning",
                "Missing agents/openai.yaml; run sync_openai_yaml.py to generate Codex metadata.",
            )
        )
    else:
        current_content = openai_yaml_path.read_text()
        if current_content != expected_openai_yaml:
            findings.append(
                make_finding(
                    "warning",
                    "agents/openai.yaml does not match the current SKILL.md metadata; regenerate it with sync_openai_yaml.py.",
                )
            )

    try:
        skill_dir.relative_to(Path.home() / "dotfiles" / "claude" / "skills")
        findings.extend(audit_link_target(skill_dir, codex_skill_link_target(skill_dir), "Codex"))
        findings.extend(audit_link_target(skill_dir, claude_skill_link_target(skill_dir), "Claude Code"))
    except ValueError:
        pass

    return {"status": compute_status(findings), "findings": findings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a skill for Claude/Codex portability")
    parser.add_argument("skill_dir", help="Path to the skill directory")
    args = parser.parse_args(argv)

    report = audit_skill_portability(Path(args.skill_dir))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["status"] == "risky" else 0


if __name__ == "__main__":
    raise SystemExit(main())
