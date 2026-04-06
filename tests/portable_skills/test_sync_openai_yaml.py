import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path("/Users/resily0808/dotfiles/claude/skills/portable-skills/scripts")
    / "sync_openai_yaml.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("sync_openai_yaml", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load sync_openai_yaml.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SyncOpenAIYamlTests(unittest.TestCase):
    def test_sync_generates_openai_yaml_from_skill_metadata(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "portable-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: portable-skills\n"
                'description: Create or retrofit a skill so a shared SKILL.md works in both Claude Code and Codex. Use when adding a new skill, generating Codex agents/openai.yaml metadata, or auditing portability of an existing Claude-oriented skill.\n'
                "---\n"
            )

            output_path = module.sync_openai_yaml(skill_dir)
            content = output_path.read_text()

            self.assertEqual(output_path, skill_dir / "agents" / "openai.yaml")
            self.assertIn('display_name: "Portable Skills"', content)
            self.assertIn('short_description: "', content)
            self.assertIn("Create or retrofit a skill", content)
            self.assertIn('default_prompt: "Use $portable-skills', content)

    def test_sync_preserves_deterministic_output(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "portable-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: portable-skills\n"
                "description: Create or retrofit skills for Claude Code and Codex. Use when refreshing agents/openai.yaml or checking portability.\n"
                "---\n"
            )

            first_path = module.sync_openai_yaml(skill_dir)
            first_write = first_path.read_text()

            second_path = module.sync_openai_yaml(skill_dir)
            second_write = second_path.read_text()

            self.assertEqual(first_path, second_path)
            self.assertEqual(first_write, second_write)

    def test_sync_avoids_dangling_trailing_words_in_generated_copy(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = Path(tmpdir) / "portable-skills"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: portable-skills\n"
                'description: Create or retrofit a skill so a shared SKILL.md works in both Claude Code and Codex. Use when adding a new skill, generating Codex metadata, or auditing an existing skill.\n'
                "---\n"
            )

            output_path = module.sync_openai_yaml(skill_dir)
            content = output_path.read_text()

            self.assertNotIn('short_description: "Create or retrofit a skill so a shared SKILL.md works in"', content)
            self.assertNotIn('default_prompt: "Use $portable-skills to create or retrofit a skill so a shared SKILL.md works in."', content)


if __name__ == "__main__":
    unittest.main()
