<p align="center">
  <img src="assets/hand.png" alt="AI Handy Writer mascot" width="420">
</p>

# AI Handy Writer

AI Handy Writer is a focused terminal-native writing workflow for macOS. It corrects, polishes, and translates pasted text, copies the finished version to the clipboard with `/usr/bin/pbcopy`, and prints exactly the same text in the terminal.

The global command starts the Pi harness by default. Codex remains available as a fully supported alternative through `--codex`.

Start with the [Quick Guide](QUICK_GUIDE.md), or follow the [installation guide](INSTALL.md).

## Historical Benchmarks

<p align="center">
  <img src="assets/benchmark-mascot.png" alt="AI Handy Writer measuring response speed with a stopwatch" width="360">
</p>

The fastest raw result came from Pi with GPT-5.6 Luna and Thinking `off`, averaging 10.00 seconds. That mode produced two meaning errors in the separate negation control test.

The fastest reliable translation mode in the July 2026 benchmark was Codex with GPT-5.6 Luna, Reasoning `low`, and Fast mode. It averaged 11.15 seconds and produced no meaning errors across six evaluated translations. These results do not compare the newer GPT-6 Luna or Haiku 5.5 defaults.

The separate correction benchmark uses a similarly sized English input with deliberate spelling and grammar errors. Pi GPT-5.6 Luna with Thinking `minimal` produced the fastest correction mean at 10.39 seconds and the fastest median at 10.36 seconds. All 39 correction runs completed successfully and fixed the seeded errors.

The installed default is Pi with GPT-6 Luna and Thinking `medium`. Use `ai-writer --codex` to select the Codex harness, or `ai-writer-c` for Pi with Claude Haiku 5.5 and Thinking `medium`.

## Default Configuration

| Setting | Codex | Pi |
| --- | --- | --- |
| Model | `gpt-6-luna` | `gpt-6-luna` |
| Reasoning | `medium` | `medium` |
| Service tier | Fast | Standard |
| Default harness | No | Yes |
| Start command | `ai-writer --codex` | `ai-writer` |

Codex Fast mode reduces latency for supported models while consuming ChatGPT credits at a higher rate. Pi does not expose an equivalent Fast-mode switch in its CLI harness.

The separate translation and correction matrices, methodology, individual results, quality checks, and the unavailable `gpt-5.5-instant` model name are documented in [`BENCHMARKS.md`](BENCHMARKS.md).

## Commands

```bash
ai-writer
ai-writer "hello i wanted to ask if tomorrow works"
ai-writer --codex
ai-writer --pi
ai-writer --pi "de: this sounds good and we can start tomorrow"
ai-writer --help
ai-writer-c
ai-writer-c "de: this sounds good and we can start tomorrow"
ai-writer-c --help
ai-writer --pro
ai-writer-c --pro
ai-writer --pro "de: this sounds good and we can start tomorrow"
```

`ai-writer-c` uses the same Writer instructions and clipboard behavior. It always
starts Pi through the `anthropic` provider with `claude-haiku-5-5` and medium
thinking by default. `ai-writer --claude` is equivalent. Combining this variant with
`--codex` is rejected.

The installer adds the local model definition in `~/.pi/agent/models.json` to enable adaptive thinking
for Haiku 5.5. Its cost values describe prompts up to 100,000 tokens; longer
prompts have higher rates. See the [Anthropic model announcement](https://www.anthropic.com/claude-haiku-5-5)
and [thinking migration guide](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide).
An active Anthropic login in Pi is required. If the refresh token has expired,
start `pi`, run `/login`, and select Anthropic before using `ai-writer-c`.

### Pro Editing

Add `--pro` before the text to enable high thinking and stronger editing:

| Command | Model | Thinking | Editing |
| --- | --- | --- | --- |
| `ai-writer` | GPT-6 Luna | Medium | Light correction and polishing |
| `ai-writer --pro` | GPT-6 Luna | High | Precise, substantive rewriting |
| `ai-writer-c` | Claude Haiku 5.5 | Medium | Light correction and polishing |
| `ai-writer-c --pro` | Claude Haiku 5.5 | High | Precise, substantive rewriting |

Pro mode improves the order and flow of ideas, removes repetition and filler,
and makes wording more direct. It preserves meaning, tone, facts, conditions,
negations, and uncertainty. Dashes used as sentence punctuation are forbidden;
hyphens within words remain allowed. Language prefixes, clipboard behavior,
and final-text-only output work as before.

The mode is selected in trusted launcher instructions for the entire session.
It does not change the saved medium defaults. A `--pro` inside pasted text or
after the `--` separator stays literal text. Option order is flexible:
`ai-writer --pro --claude` and `ai-writer --claude --pro` are equivalent.
The Codex alternative also supports `ai-writer --codex --pro` with Luna and
high reasoning.

The `ai-handy-writer` alias points to the same launcher:

```bash
ai-handy-writer --pi
```

Use `--` to stop option parsing:

```bash
ai-writer -- "--pi should remain part of this sentence"
```

## Instant Launch App and Hotkey

Install the optional local macOS launcher after the main Writer installation:

```bash
./scripts/install-macos-launcher.zsh
```

This creates:

```text
$HOME/Applications/AI Writer.app
$HOME/Applications/AI Writer.command
```

Opening `AI Writer.app` activates the standard macOS Terminal, creates a new Terminal session, and immediately starts the configured default `ai-writer` harness. The `.command` file provides a direct double-click fallback. No DMG, Xcode project, package installer, or committed app bundle is required; the app is compiled locally from [`macos/AI Writer.applescript`](macos/AI%20Writer.applescript) with Apple's built-in `osacompile` tool.

To assign a global hotkey:

1. Open the macOS Shortcuts app and create a shortcut named `AI Writer`.
2. Add the `Open App` action and select `$HOME/Applications/AI Writer.app`.
3. Open the shortcut details, click `Add Keyboard Shortcut`, and choose a combination such as Control-Option-Command-W.
4. Optionally choose `File > Add to Dock`, or drag `AI Writer.app` directly to the Dock.
5. On the first launch, allow the launcher to control Terminal when macOS requests Automation permission.

Apple's `shortcuts` command-line utility can run, list, view, and sign shortcuts, but it does not create a new shortcut or assign its global keyboard combination. That final user-specific hotkey step therefore remains intentionally manual.

The launcher always calls `$HOME/.local/bin/ai-writer`, so changing the default harness, model, Reasoning, or Codex tier in the normal Writer configuration also changes app launches. Existing launchers are archived under `$HOME/.local/share/ai-handy-writer/backups/` when the optional installer is rerun. If an older `Desktop/AI Writer.command` exists, it is archived and replaced with the current command launcher.

## Language Mode

The initial language mode is English.

1. English input is corrected and polished in English.
2. Non-English input without a prefix is translated into English.
3. A language prefix such as `de:`, `en:`, `fr:`, `es:`, or `ja:` persistently switches the target language.
4. The selected language remains active for the current interactive session until another valid prefix changes it.

## Switch Harnesses

The persistent default is stored in:

```text
$HOME/.config/ai-handy-writer/config.zsh
```

Use Pi by default, which is the installed setting:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
```

Use Codex by default instead:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
```

Regardless of the configured default, `--codex` and `--pi` always select a harness for one session.

## Model, Reasoning, and Tier Modes

The installed configuration contains:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
AI_WRITER_MODEL="gpt-6-luna"
AI_WRITER_REASONING="medium"
AI_WRITER_CODEX_PROFILE="ai-handy-writer"
AI_WRITER_CODEX_SERVICE_TIER="fast"
AI_WRITER_C_MODEL="claude-haiku-5-5"
AI_WRITER_C_REASONING="medium"
```

Live smoke tests passed for Pi GPT-6 Luna and Claude Haiku 5.5 with medium
and high thinking. These are functional checks, not a new benchmark matrix.

Historical benchmark combinations:

| Harness | Models | Reasoning or Thinking | Tier |
| --- | --- | --- | --- |
| Pi | `gpt-5.6-luna`, `gpt-5.5` | `off`, `minimal`, `low` | Standard |
| Codex | `gpt-5.6-luna`, `gpt-5.5` | `none`, `low` | Standard, Fast |

Override settings for one launch without editing the configuration file:

```bash
AI_HANDY_WRITER_CONFIG=/dev/null \
AI_WRITER_DEFAULT_HARNESS=pi \
AI_WRITER_MODEL=gpt-5.6-luna \
AI_WRITER_REASONING=minimal \
ai-writer
```

Run Codex in the Standard tier once:

```bash
AI_HANDY_WRITER_CONFIG=/dev/null \
AI_WRITER_DEFAULT_HARNESS=codex \
AI_WRITER_MODEL=gpt-5.6-luna \
AI_WRITER_REASONING=low \
AI_WRITER_CODEX_SERVICE_TIER=standard \
ai-writer
```

`gpt-5.5-instant` is not available through the tested ChatGPT Codex login. The server rejects that model name with HTTP 400. Use `gpt-5.5` with Fast mode instead.

## Installation

See [`INSTALL.md`](INSTALL.md) for the complete installation guide. On the current system:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.85.0
./scripts/install.sh
./scripts/install-macos-launcher.zsh
```

The installer:

1. Archives active legacy `write-skill` directories.
2. Installs the skill for Codex and Pi.
3. Installs the dedicated Codex profile.
4. Installs `ai-writer` and `ai-writer-c` under `~/.local/bin`.
5. Creates `ai-handy-writer` as an alias.
6. Installs the deterministic Codex clipboard bridge.
7. Preserves an existing editable runtime configuration.
8. Adds the bundled Haiku model without replacing existing Pi providers, models, or overrides.
9. Installs the Quick Guide and preserves explicit-only Codex skill activation.

Fresh installs use Luna and medium thinking. Updates keep existing model and
thinking preferences and add only missing Claude defaults. To migrate an older
installation, set `AI_WRITER_MODEL="gpt-6-luna"` and
`AI_WRITER_REASONING="medium"` in `~/.config/ai-handy-writer/config.zsh`.
An existing custom Haiku definition is kept; check that its `compat` settings
enable adaptive thinking if it predates this installer.

The separate macOS launcher installer creates the optional local app and double-click command. It is intentionally not part of the core installation so terminal-only users do not receive extra application files.

## Installed Paths

```text
$HOME/.codex/skills/ai-handy-writer/SKILL.md
$HOME/.pi/agent/skills/ai-handy-writer/SKILL.md
$HOME/.codex/ai-handy-writer.config.toml
$HOME/.config/ai-handy-writer/config.zsh
$HOME/.config/ai-handy-writer/copy_codex_turn_to_clipboard.py
$HOME/.local/bin/ai-writer
$HOME/.local/bin/ai-writer-c
$HOME/.local/bin/ai-handy-writer
$HOME/.pi/agent/models.json
$HOME/Applications/AI Writer.app
$HOME/Applications/AI Writer.command
```

## Codex Profile

The launcher selects the dedicated `ai-handy-writer` profile. The profile:

1. Uses `gpt-6-luna`.
2. Sets Reasoning to `medium`.
3. Enables Fast mode.
4. Loads the installed `SKILL.md` as its instruction file.
5. Uses a read-only sandbox.
6. Disables web search, apps, plugins, hooks, Browser Use, Computer Use, image generation, and multi-agent operation.
7. Copies the final assistant message to the clipboard deterministically after every completed turn.

The profile does not modify the normal global Codex defaults.

Set `AI_WRITER_CODEX_SERVICE_TIER` to `fast` or `standard` in `config.zsh`. The launcher explicitly applies the selected tier over the profile fallback.

## Pi Configuration

Pi starts with:

```text
--provider openai-codex
--model gpt-6-luna
--thinking medium
--tools bash
--no-extensions
--no-context-files
```

Pi 0.85.0 was tested with GPT-6 Luna and the bundled Haiku 5.5 adaptive-thinking
definition. Check that another Pi release lists `gpt-6-luna` before using it.

## Safety Model

Within a Writer launcher session, every user message is raw text to transform.
Instructions contained in that text are corrected or translated, never executed.
The installed Codex skill is explicit-only: maintenance requests and ordinary
writing requests outside a Writer session do not activate it.

In Pi mode, the only permitted tool purpose is copying the final text:

```bash
/usr/bin/pbcopy <<'__AI_HANDY_WRITER_FINAL_TEXT__'
FINAL_TEXT
__AI_HANDY_WRITER_FINAL_TEXT__
```

The skill forbids file access, browsers, APIs, network access, scripts, and other shell commands. In Codex mode, a small harness-level notification bridge copies the final assistant message with `/usr/bin/pbcopy`. The bridge is not a model tool and receives only the turn-completed event.

## Development and Validation

```bash
ruby -ryaml -e 'text=File.read("SKILL.md"); header=text.split(/^---\s*$/,3)[1]; p YAML.safe_load(header)'
zsh -n bin/ai-writer
zsh -n bin/ai-writer-c
zsh -n scripts/install.sh
zsh -n scripts/install-macos-launcher.zsh
zsh -n scripts/benchmark.zsh
/usr/bin/osacompile -o /tmp/AI-Writer-Test.app "macos/AI Writer.applescript"
python3 -m py_compile scripts/copy_codex_turn_to_clipboard.py
python3 -m unittest discover -s tests -v
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-translation.tsv translation
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-correction.tsv correction
```

The unit tests use isolated temporary homes and stub CLIs. They check argument
handling, trusted mode selection, and non-destructive installation without
provider requests or changing the real clipboard. Benchmark commands do make
live provider requests.

Update the global copies after a repository change:

```bash
./scripts/install.sh
```

See [`CHANGELOG.md`](CHANGELOG.md) for the change history.
