# Install AI Handy Writer

This guide installs AI Handy Writer for Codex and Pi. Codex becomes the default harness, while Pi remains available through `--pi`.

## Requirements

1. macOS with `/usr/bin/pbcopy`
2. Node.js and npm
3. Codex CLI with a ChatGPT login
4. Pi Coding Agent with an OpenAI Codex login
5. `~/.local/bin` in `PATH`

Check the installed versions and login state:

```bash
codex --version
codex login status
pi --version
```

## Update Pi

The tested Pi release that includes GPT-5.6 Luna in its model catalog is 0.83.0:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.83.0
pi --version
pi --list-models | grep 'gpt-5.6-luna'
```

## Install

From the repository:

```bash
chmod +x bin/ai-writer scripts/install.sh scripts/benchmark.zsh
./scripts/install.sh
```

The installer creates or updates:

```text
$HOME/.codex/skills/ai-handy-writer/SKILL.md
$HOME/.pi/agent/skills/ai-handy-writer/SKILL.md
$HOME/.codex/ai-handy-writer.config.toml
$HOME/.config/ai-handy-writer/config.zsh
$HOME/.config/ai-handy-writer/copy_codex_turn_to_clipboard.py
$HOME/.local/bin/ai-writer
$HOME/.local/bin/ai-handy-writer
```

Active legacy directories at `~/.codex/skills/write-skill` and `~/.pi/agent/skills/write-skill` are archived with a timestamp under:

```text
$HOME/.local/share/ai-handy-writer/backups/
```

## Remove the Legacy Shell Function

If `ai-writer` was previously defined as a function in `~/.zshrc`, remove that complete function block and reload the shell:

```bash
source ~/.zshrc
type ai-writer
```

The result should point to `$HOME/.local/bin/ai-writer`, not a shell function.

## Test the Installation

Check the defaults:

```bash
ai-writer --help
```

Test Codex as the default:

```bash
ai-writer "hallo ich wollte fragen ob das morgen passt"
/usr/bin/pbpaste
```

The German input should be returned as natural English because English is the initial language mode.

Test Pi explicitly:

```bash
ai-writer --pi "hallo ich wollte fragen ob das morgen passt"
/usr/bin/pbpaste
```

Select either harness explicitly:

```bash
ai-writer --codex
ai-writer --pi
```

Check the alias:

```bash
ai-handy-writer --help
```

## Make Pi the Default Later

Edit:

```text
$HOME/.config/ai-handy-writer/config.zsh
```

Set:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
```

Afterward, `ai-writer` starts Pi and `ai-writer --codex` still starts Codex.

## Change Model, Reasoning, or Tier

The shared runtime values are stored in `config.zsh`:

```zsh
AI_WRITER_MODEL="gpt-5.6-luna"
AI_WRITER_REASONING="low"
AI_WRITER_CODEX_SERVICE_TIER="fast"
```

The launcher passes the model and reasoning values to both harnesses. The dedicated Codex profile contains the same values as fallbacks.

Codex supports the tested `fast` and `standard` tier selections. Codex was tested with Reasoning `none` and `low`. Pi was tested with Thinking `off`, `minimal`, and `low`.

## Codex Fast Mode

Only the Codex harness uses Fast mode:

```toml
service_tier = "fast"

[features]
fast_mode = true
```

The setting lives in the dedicated Writer profile and does not affect ordinary Codex sessions.

## Benchmark

The complete timing matrix and default-mode decision are documented in [`BENCHMARKS.md`](BENCHMARKS.md).

Run a new matrix with three repetitions per mode:

```bash
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-benchmark.tsv
```

Pi Luna `off` produced the fastest raw result. Because it repeatedly changed the meaning of a negation control sentence, Codex Luna Fast `low` remains the fastest reliable default.
