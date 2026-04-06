import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path("/Users/resily0808/dotfiles/claude/skills/portable-skills/scripts")
    / "init_portable_skill.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("init_portable_skill", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load init_portable_skill.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InitPortableSkillTests(unittest.TestCase):
    def test_init_creates_expected_directory_structure(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "skills"
            result = module.initialize_skill("Portable Skills", root)

            self.assertEqual(result.name, "portable-skills")
            self.assertTrue((result / "SKILL.md").exists())
            self.assertTrue((result / "agents" / "openai.yaml").exists())

    def test_init_does_not_overwrite_existing_skill_without_flag(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "skills"
            existing = root / "portable-skills"
            existing.mkdir(parents=True)
            (existing / "SKILL.md").write_text("do not overwrite")

            with self.assertRaises(FileExistsError):
                module.initialize_skill("portable-skills", root)

    def test_init_can_create_optional_resource_directories(self):
        module = load_module()

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "skills"
            result = module.initialize_skill(
                "portable-skills",
                root,
                resources=["scripts", "references", "assets"],
            )

            self.assertTrue((result / "scripts").is_dir())
            self.assertTrue((result / "references").is_dir())
            self.assertTrue((result / "assets").is_dir())


if __name__ == "__main__":
    unittest.main()
