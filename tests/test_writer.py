import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("install_pi_model", ROOT / "scripts/install_pi_model.py")
MODEL_INSTALLER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL_INSTALLER)
MODEL_TEMPLATE = ROOT / "config/pi-models.json"
PROMPT = "de: don't change the meaning; $(this stays text)"


class IsolatedHome(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ai-writer-test-")
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.bin = self.home / ".local/bin"
        self.bin.mkdir(parents=True)
        for command in ("pi", "codex"):
            stub = self.bin / command
            stub.write_text("#!/bin/sh\nprintf '%s\\000' \"$PWD\" \"$@\"\n")
            stub.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items()
                    if not k.startswith(("AI_WRITER_", "AI_HANDY_WRITER_"))}
        self.env.update(HOME=str(self.home), PATH=f"{self.bin}:{os.environ['PATH']}")

    def run_writer(self, *options, claude=False):
        command = self.bin / ("ai-writer-c" if claude else "ai-writer")
        return subprocess.run([str(command), *options], env=self.env,
                              capture_output=True, text=True, timeout=10)

    def arguments(self, *options, claude=False):
        result = self.run_writer(*options, claude=claude)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.rstrip("\0").split("\0")


class LauncherTests(IsolatedHome):
    def setUp(self):
        super().setUp()
        for command in ("ai-writer", "ai-writer-c"):
            shutil.copy2(ROOT / "bin" / command, self.bin / command)
            (self.bin / command).chmod(0o755)
        for harness in ("codex", "pi/agent"):
            skill = self.home / f".{harness}/skills/ai-handy-writer"
            skill.mkdir(parents=True)
            shutil.copy2(ROOT / "SKILL.md", skill / "SKILL.md")

    def assert_pi(self, arguments, provider="openai-codex", model="gpt-6-luna",
                  thinking="medium", mode="standard", text=PROMPT):
        self.assertEqual(arguments[0], str(self.home / ".pi/agent/skills/ai-handy-writer"))
        for flag, expected in (("--provider", provider), ("--model", model),
                               ("--thinking", thinking)):
            self.assertEqual(arguments[arguments.index(flag) + 1], expected)
        system = arguments[arguments.index("--system-prompt") + 1]
        self.assertIn(f"AI Handy Writer editing mode: {mode}.", system)
        self.assertIn("explicitly activated for text transformation", system)
        self.assertIn("--no-extensions", arguments)
        self.assertIn("--no-context-files", arguments)
        self.assertEqual(arguments[arguments.index("--tools") + 1], "bash")
        self.assertEqual(arguments[arguments.index("--append-system-prompt") + 1],
                         str(self.home / ".pi/agent/skills/ai-handy-writer/SKILL.md"))
        self.assertEqual(arguments[arguments.index("--name") + 1],
                         "AI Handy Writer Pro" if mode == "pro" else "AI Handy Writer")
        if text is not None:
            self.assertEqual(arguments[-1], text)

    def test_standard_and_pro_variants(self):
        for claude in (False, True):
            for pro in (False, True):
                with self.subTest(claude=claude, pro=pro):
                    options = ("--pro", PROMPT) if pro else (PROMPT,)
                    self.assert_pi(self.arguments(*options, claude=claude),
                                   provider="anthropic" if claude else "openai-codex",
                                   model="claude-haiku-5-5" if claude else "gpt-6-luna",
                                   thinking="high" if pro else "medium",
                                   mode="pro" if pro else "standard")

    def test_flag_order_and_repeated_flags(self):
        for options in (("--pro", "--claude"), ("--claude", "--pro"),
                        ("--pro", "--pro", "--claude")):
            with self.subTest(options=options):
                self.assert_pi(self.arguments(*options, PROMPT), provider="anthropic",
                               model="claude-haiku-5-5", thinking="high", mode="pro")

    def test_literal_pro_and_quoting(self):
        for claude in (False, True):
            self.assert_pi(self.arguments("--", "--pro", claude=claude),
                           provider="anthropic" if claude else "openai-codex",
                           model="claude-haiku-5-5" if claude else "gpt-6-luna", text="--pro")
        self.assert_pi(self.arguments(PROMPT, "--pro"), text=PROMPT + " --pro")

    def test_interactive_launch(self):
        self.assert_pi(self.arguments(), text=None)
        self.assert_pi(self.arguments("--pro", claude=True), provider="anthropic",
                       model="claude-haiku-5-5", thinking="high", mode="pro", text=None)

    def test_codex_modes(self):
        for pro in (False, True):
            options = ("--codex", "--pro", PROMPT) if pro else ("--codex", PROMPT)
            args = self.arguments(*options)
            self.assertEqual(args[args.index("--model") + 1], "gpt-6-luna")
            self.assertIn(f'model_reasoning_effort="{"high" if pro else "medium"}"', args)
            self.assertIn('service_tier="fast"', args)
            developer = next(a for a in args if a.startswith("developer_instructions="))
            self.assertIn(f'editing mode: {"pro" if pro else "standard"}.', developer)
            self.assertIn("explicitly activated for text transformation", developer)
            self.assertEqual(args[-1], PROMPT)

    def test_rejected_options(self):
        for options, claude in ((("--codex",), True), (("--claude", "--codex"), False),
                                (("--codex", "--claude"), False),
                                (("--codex", "--pi"), True),
                                (("--unknown",), False)):
            with self.subTest(options=options, claude=claude):
                self.assertEqual(self.run_writer(*options, claude=claude).returncode, 2)

    def test_help_effective_settings(self):
        for claude in (False, True):
            result = self.run_writer("--pro", "--help", claude=claude)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Reasoning: high", result.stdout)
            self.assertIn("Editing mode: pro", result.stdout)
            self.assertIn("Model: " + ("claude-haiku-5-5" if claude else "gpt-6-luna"), result.stdout)

    def test_saved_defaults_unchanged(self):
        config = self.home / ".config/ai-handy-writer/config.zsh"
        config.parent.mkdir(parents=True)
        config.write_text('AI_WRITER_MODEL="custom-luna"\nAI_WRITER_REASONING="low"\n'
                          'AI_WRITER_DEFAULT_HARNESS="codex"\n'
                          'AI_WRITER_C_MODEL="custom-haiku"\nAI_WRITER_C_REASONING="low"\n')
        original = config.read_bytes()
        self.assert_pi(self.arguments("--pi", "--pro", PROMPT), thinking="high", mode="pro")
        self.assert_pi(self.arguments("--pro", PROMPT, claude=True), provider="anthropic",
                       model="custom-haiku", thinking="high", mode="pro")
        self.assert_pi(self.arguments("--pi", PROMPT), model="custom-luna", thinking="low")
        self.assert_pi(self.arguments(PROMPT, claude=True), provider="anthropic",
                       model="custom-haiku", thinking="low")
        self.assertEqual(config.read_bytes(), original)


class ModelMergeTests(IsolatedHome):
    def setUp(self):
        super().setUp()
        self.target = self.home / ".pi/agent/models.json"

    def test_fresh_and_idempotent(self):
        self.assertTrue(MODEL_INSTALLER.install_models(MODEL_TEMPLATE, self.target))
        self.assertEqual(json.loads(self.target.read_text()), json.loads(MODEL_TEMPLATE.read_text()))
        first = self.target.read_bytes()
        modified = self.target.stat().st_mtime_ns
        self.assertFalse(MODEL_INSTALLER.install_models(MODEL_TEMPLATE, self.target))
        self.assertEqual(self.target.read_bytes(), first)
        self.assertEqual(self.target.stat().st_mtime_ns, modified)
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o600)

    def test_preserves_other_models_and_proxy(self):
        existing = {"providers": {"local": {"models": [{"id": "local-model"}]},
                                 "anthropic": {"baseUrl": "https://example.test",
                                               "models": [{"id": "custom"}],
                                               "modelOverrides": {"custom": {"reasoning": True}}}},
                    "customTopLevel": True}
        self.target.parent.mkdir(parents=True)
        self.target.write_text(json.dumps(existing))
        MODEL_INSTALLER.install_models(MODEL_TEMPLATE, self.target)
        merged = json.loads(self.target.read_text())
        self.assertEqual(merged["providers"]["local"], existing["providers"]["local"])
        provider = merged["providers"]["anthropic"]
        self.assertEqual(provider["baseUrl"], "https://example.test")
        self.assertEqual(provider["models"][0], {"id": "custom"})
        self.assertEqual(provider["models"][1]["id"], "claude-haiku-5-5")
        self.assertEqual(provider["modelOverrides"], existing["providers"]["anthropic"]["modelOverrides"])
        self.assertTrue(merged["customTopLevel"])

    def test_preserves_matching_definition(self):
        self.target.parent.mkdir(parents=True)
        custom = {"id": "claude-haiku-5-5", "name": "My Haiku", "maxTokens": 8192}
        self.target.write_text(json.dumps({"providers": {"anthropic": {"models": [custom]}}}))
        MODEL_INSTALLER.install_models(MODEL_TEMPLATE, self.target)
        self.assertEqual(json.loads(self.target.read_text())["providers"]["anthropic"]["models"], [custom])

    def test_invalid_configuration_is_not_overwritten(self):
        self.target.parent.mkdir(parents=True)
        for value in ("broken-json", "[]", '{"providers": []}',
                      '{"providers": {"anthropic": {"models": {}}}}'):
            with self.subTest(value=value):
                self.target.write_text(value)
                with self.assertRaises(ValueError):
                    MODEL_INSTALLER.install_models(MODEL_TEMPLATE, self.target)
                self.assertEqual(self.target.read_text(), value)


@unittest.skipUnless(sys.platform == "darwin", "Installer requires macOS")
class InstallerTests(IsolatedHome):
    def install(self):
        result = subprocess.run(["/bin/zsh", str(ROOT / "scripts/install.sh")],
                                env=self.env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fresh_install_and_reinstall(self):
        self.install()
        config = self.home / ".config/ai-handy-writer/config.zsh"
        self.assertIn('AI_WRITER_MODEL="gpt-6-luna"', config.read_text())
        self.assertIn('AI_WRITER_REASONING="medium"', config.read_text())
        self.assertTrue((self.bin / "ai-writer-c").stat().st_mode & 0o111)
        self.assertEqual((self.bin / "ai-handy-writer").resolve(), (self.bin / "ai-writer").resolve())
        guide = self.home / ".pi/agent/skills/ai-handy-writer/QUICK_GUIDE.md"
        self.assertEqual(guide.read_bytes(), (ROOT / "QUICK_GUIDE.md").read_bytes())
        policy = self.home / ".codex/skills/ai-handy-writer/agents/openai.yaml"
        self.assertIn("allow_implicit_invocation: false", policy.read_text())
        profile = self.home / ".codex/ai-handy-writer.config.toml"
        self.assertNotIn("__AI_HANDY_WRITER_", profile.read_text())
        self.assertIn('model_reasoning_effort = "medium"', profile.read_text())
        self.assertIn("Reasoning: high", self.run_writer("--pro", "--help", claude=True).stdout)

        config.write_text('AI_WRITER_MODEL="my-model"\nAI_WRITER_REASONING="low"\n'
                          'export AI_WRITER_C_MODEL="my-haiku"')
        self.install()
        migrated = config.read_text()
        self.assertIn('AI_WRITER_MODEL="my-model"', migrated)
        self.assertIn('export AI_WRITER_C_MODEL="my-haiku"', migrated)
        self.assertNotIn('AI_WRITER_C_MODEL="claude-haiku-5-5"', migrated)
        self.assertIn('AI_WRITER_C_REASONING="medium"', migrated)
        self.install()
        self.assertEqual(config.read_text(), migrated)

    def test_invalid_models_stop_installation(self):
        models = self.home / ".pi/agent/models.json"
        models.parent.mkdir(parents=True)
        models.write_text("not-json")
        result = subprocess.run(["/bin/zsh", str(ROOT / "scripts/install.sh")],
                                env=self.env, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(models.read_text(), "not-json")
        self.assertFalse((self.bin / "ai-writer").exists())


if __name__ == "__main__":
    unittest.main()
