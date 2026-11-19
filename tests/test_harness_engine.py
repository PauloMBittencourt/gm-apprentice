#!/usr/bin/env python3
"""The harness (harness/) stays in step with the skills it conducts, and its own tests pass.

The harness conducts each skill by the steps in harness/flows/<skill>.json. A flow names
reference files to read ("campaign-qa/references/checks/canon-audit.md"); when a skill renames
or drops one, the flow would wait forever for a read that can no longer happen. These checks
fail first. The harness's script tests (harness/tests/test_*.py) run here so CI runs them too.

Run: python3 -m pytest tests/test_harness_engine.py
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARNESS = ROOT / "harness"
SKILLS = ROOT / "skills"
LOCAL_SKILLS = {"qa-passo"}   # a vault's own skill, conducted by the same engine


def flows():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((HARNESS / "flows").glob("*.json"))}


def atoms(spec):
    for steps in spec["modes"].values():
        for step in steps:
            yield from step["evidence"]


class FlowsMatchSkillsTests(unittest.TestCase):
    def test_every_skill_has_a_flow(self):
        skills = {p.parent.name for p in SKILLS.glob("*/SKILL.md")} - {"shared"}
        self.assertEqual(sorted(skills - set(flows())), [])

    def test_every_flow_names_a_skill(self):
        for name, spec in flows().items():
            self.assertEqual(spec["skill"], name)
            if name not in LOCAL_SKILLS:
                self.assertTrue((SKILLS / name / "SKILL.md").is_file(), name)

    def test_skill_files_a_flow_reads_exist(self):
        skill_dirs = {p.name for p in SKILLS.iterdir() if p.is_dir()}
        gone = [(name, path) for name, spec in flows().items() for a in atoms(spec)
                for path in a.get("read", [])
                if path.split("/")[0] in skill_dirs and not (SKILLS / path).exists()]
        self.assertEqual(gone, [])

    def test_no_control_characters_in_harness_code(self):
        # A regex written through a shell heredoc once lost "\\b" to a real backspace and never matched.
        bad = [p.relative_to(ROOT).as_posix() for p in HARNESS.rglob("*") if p.suffix in (".py", ".json")
               and any(ord(c) < 32 and c not in "\n\r\t" for c in p.read_text(encoding="utf-8"))]
        self.assertEqual(bad, [])

    def test_step_ids_are_unique_per_mode(self):
        for name, spec in flows().items():
            for mode, steps in spec["modes"].items():
                ids = [s["id"] for s in steps]
                self.assertEqual(len(ids), len(set(ids)), f"{name}:{mode}")


class PluginHooksTests(unittest.TestCase):
    def test_every_hook_command_names_a_shipped_script(self):
        cfg = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
        cmds = [h["command"] for groups in cfg["hooks"].values() for g in groups for h in g["hooks"]]
        launcher = ROOT / "harness" / "bin" / "hook"
        self.assertTrue(launcher.is_file())
        ignored = subprocess.run(["git", "check-ignore", "-q", str(launcher)], cwd=str(ROOT))
        self.assertNotEqual(ignored.returncode, 0, "harness/bin/hook is gitignored and would not ship")
        for cmd in cmds:
            self.assertIn('"${CLAUDE_PLUGIN_ROOT}/harness/bin/hook" ', cmd)
            name = cmd.rsplit(" ", 1)[-1]
            self.assertTrue((HARNESS / "hooks" / f"{name}.py").is_file(), name)


class HarnessScriptTests(unittest.TestCase):
    def test_harness_scripts_pass(self):
        env = {k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"}
        env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
        env.pop("GMA_VAULT", None)              # the golden test needs a real vault: skipped here
        for script in sorted((HARNESS / "tests").glob("test_*.py")):
            with self.subTest(script=script.name):
                r = subprocess.run([sys.executable, str(script)], cwd=str(script.parent), env=env,
                                   capture_output=True, timeout=600)
                out = r.stdout.decode("utf-8", "replace")
                self.assertEqual(r.returncode, 0, out[-3000:] + r.stderr.decode("utf-8", "replace")[-2000:])


if __name__ == "__main__":
    unittest.main()
