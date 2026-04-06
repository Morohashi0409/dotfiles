import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path("/Users/resily0808/dotfiles/claude/skills/portable-skills/scripts")
    / "audit_skill_portability.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("audit_skill_portability", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load audit_skill_portability.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditSkillPortabilityTests(unittest.TestCase):
    def test_audit_flags_missing_openai_yaml(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "portable-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: portable-skills\n"
                "description: Create portable skills. Use when adding Codex metadata.\n"
                "---\n"
            )

            report = module.audit_skill_portability(skill_dir)

            self.assertEqual(report["status"], "recommended-update")
            self.assertTrue(
                any("agents/openai.yaml" in finding["message"] for finding in report["findings"])
            )

    def test_audit_warns_on_claude_only_frontmatter(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "legacy-skill"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: legacy-skill\n"
                "description: Keep a legacy skill working. Use when auditing portability.\n"
                "user-invocable: true\n"
                "---\n"
            )
            (skill_dir / "agents").mkdir()
            (skill_dir / "agents" / "openai.yaml").write_text("interface:\n")

            report = module.audit_skill_portability(skill_dir)

            self.assertEqual(report["status"], "recommended-update")
            self.assertTrue(
                any("user-invocable" in finding["message"] for finding in report["findings"])
            )

    def test_audit_reports_safe_skill_as_clean(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "portable-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: portable-skills\n"
                "description: Create portable skills for Claude Code and Codex. Use when keeping one shared SKILL.md.\n"
                "---\n"
            )
            (skill_dir / "agents").mkdir()
            (skill_dir / "agents" / "openai.yaml").write_text(
                'interface:\n'
                '  display_name: "Portable Skills"\n'
                '  short_description: "Create portable skills for Claude Code and Codex"\n'
                '  default_prompt: "Use $portable-skills to create portable skills for Claude Code and Codex."\n'
            )

            report = module.audit_skill_portability(skill_dir)

            self.assertEqual(report["status"], "safe")
            self.assertEqual(report["findings"], [])


if __name__ == "__main__":
    unittest.main()
