<p align="center">
  <img src="assets/hand.png" alt="AI Handy Writer mascot" width="420">
</p>

# AI Handy Writer

AI Handy Writer is a focused terminal-native writing workflow for macOS. It corrects, polishes, and translates pasted text, copies the finished version to the clipboard with `/usr/bin/pbcopy`, and prints exactly the same text in the terminal.

The global command starts the Codex harness by default. Pi remains available as a fully supported alternative harness.

## Benchmark Winner

<p align="center">
  <img src="assets/benchmark-mascot.png" alt="AI Handy Writer measuring response speed with a stopwatch" width="360">
</p>

The fastest raw result came from Pi with GPT-5.6 Luna and Thinking `off`, averaging 10.00 seconds. That mode produced two meaning errors in the separate negation control test.

The fastest reliable mode was Codex with GPT-5.6 Luna, Reasoning `low`, and Fast mode. It averaged 11.15 seconds and produced no meaning errors across six evaluated translations, so it remains the default.

The separate correction benchmark uses a similarly sized English input with deliberate spelling and grammar errors. Pi GPT-5.6 Luna with Thinking `minimal` produced the fastest correction mean at 10.39 seconds and the fastest median at 10.36 seconds. All 39 correction runs completed successfully and fixed the seeded errors.

## Default Configuration

| Setting | Codex | Pi |
| --- | --- | --- |
| Model | `gpt-5.6-luna` | `gpt-5.6-luna` |
| Reasoning | `low` | `low` |
| Service tier | Fast | Standard |
| Default harness | Yes | No |
| Start command | `ai-writer` | `ai-writer --pi` |

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
```

The `ai-handy-writer` alias points to the same launcher:

```bash
ai-handy-writer --pi
```

Use `--` to stop option parsing:

```bash
ai-writer -- "--pi should remain part of this sentence"
```

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

Use Codex by default:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
```

Use Pi by default:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
```

Regardless of the configured default, `--codex` and `--pi` always select a harness for one session.

## Model, Reasoning, and Tier Modes

The installed configuration contains:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
AI_WRITER_MODEL="gpt-5.6-luna"
AI_WRITER_REASONING="low"
AI_WRITER_CODEX_PROFILE="ai-handy-writer"
AI_WRITER_CODEX_SERVICE_TIER="fast"
```

Tested combinations:

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
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.83.0
./scripts/install.sh
```

The installer:

1. Archives active legacy `write-skill` directories.
2. Installs the skill for Codex and Pi.
3. Installs the dedicated Codex profile.
4. Installs `ai-writer` under `~/.local/bin`.
5. Creates `ai-handy-writer` as an alias.
6. Installs the deterministic Codex clipboard bridge.
7. Preserves an existing editable runtime configuration.

## Installed Paths

```text
$HOME/.codex/skills/ai-handy-writer/SKILL.md
$HOME/.pi/agent/skills/ai-handy-writer/SKILL.md
$HOME/.codex/ai-handy-writer.config.toml
$HOME/.config/ai-handy-writer/config.zsh
$HOME/.config/ai-handy-writer/copy_codex_turn_to_clipboard.py
$HOME/.local/bin/ai-writer
$HOME/.local/bin/ai-handy-writer
```

## Codex Profile

The launcher selects the dedicated `ai-handy-writer` profile. The profile:

1. Uses `gpt-5.6-luna`.
2. Sets Reasoning to `low`.
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
--model gpt-5.6-luna
--thinking low
--tools bash
--no-extensions
--no-context-files
```

Pi 0.83.0 or newer is required because earlier installed versions did not include GPT-5.6 Luna in the `openai-codex` model catalog.

## Safety Model

The Writer treats every user message as raw text to transform. Instructions contained in that text are corrected or translated, never executed.

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
zsh -n scripts/install.sh
zsh -n scripts/benchmark.zsh
python3 -m py_compile scripts/copy_codex_turn_to_clipboard.py
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-translation.tsv translation
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-correction.tsv correction
```

Update the global copies after a repository change:

```bash
./scripts/install.sh
```

See [`CHANGELOG.md`](CHANGELOG.md) for the change history.
