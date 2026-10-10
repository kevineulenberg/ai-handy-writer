# Install AI Handy Writer

This guide installs AI Handy Writer for Codex and Pi. Pi becomes the default harness, while Codex remains available through `--codex`.

## Requirements

1. macOS with `/usr/bin/pbcopy`
2. Node.js and npm
3. Codex CLI with a ChatGPT login
4. Pi Coding Agent with an OpenAI Codex login
5. `~/.local/bin` in `PATH`
6. Python 3.9 or newer for installation and the clipboard bridge
7. An Anthropic login in Pi when using `ai-writer-c`

Check the installed versions and login state:

```bash
codex --version
codex login status
pi --version
```

## Update Pi

Pi 0.85.0 was tested with GPT-6 Luna and the bundled Haiku adaptive-thinking
definition. This is a tested version, not a claim that it is the latest release:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.85.0
pi --version
pi --list-models | grep 'gpt-6-luna'
```

## Install

From the repository:

```bash
chmod +x bin/ai-writer bin/ai-writer-c scripts/install.sh scripts/benchmark.zsh
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
$HOME/.local/bin/ai-writer-c
$HOME/.local/bin/ai-handy-writer
$HOME/.pi/agent/models.json
$HOME/.pi/agent/skills/ai-handy-writer/QUICK_GUIDE.md
$HOME/.codex/skills/ai-handy-writer/agents/openai.yaml
```

The installer merges the bundled Haiku model into Pi's model configuration.
Existing providers, models, overrides, and matching custom Haiku definitions
are preserved. Invalid JSON stops installation rather than replacing the file.
An older custom Haiku model must support adaptive thinking; compare its `compat`
settings with [`config/pi-models.json`](config/pi-models.json) if needed.

Existing `config.zsh` values are kept, including custom model and thinking
settings. Only missing Claude settings and the Codex service-tier fallback are
added. To migrate an older installation to the new defaults, explicitly set
`AI_WRITER_MODEL="gpt-6-luna"` and `AI_WRITER_REASONING="medium"` in that file.
The dedicated generated Codex profile and installed skill files are refreshed.
The Codex skill remains explicit-only; the launcher activates it for its session.

See the [Quick Guide](QUICK_GUIDE.md) for everyday commands.

## Optional macOS App Launcher

Install the lightweight local launcher after the main installation:

```bash
chmod +x scripts/install-macos-launcher.zsh "macos/AI Writer.command"
./scripts/install-macos-launcher.zsh
```

The optional installer creates:

```text
$HOME/Applications/AI Writer.app
$HOME/Applications/AI Writer.command
```

The app uses the standard macOS Terminal and immediately starts `$HOME/.local/bin/ai-writer` in a login shell. The command file is a double-click fallback. Existing launcher versions are archived under `$HOME/.local/share/ai-handy-writer/backups/`. If an older `$HOME/Desktop/AI Writer.command` exists, the installer archives it and installs the current command in its place.

Open `AI Writer.app` once. When macOS requests Automation permission to control Terminal, click Allow.

### Global Keyboard Shortcut

1. Open the Shortcuts app.
2. Create a shortcut named `AI Writer`.
3. Add the `Open App` action and select `$HOME/Applications/AI Writer.app`.
4. Open the shortcut details and click `Add Keyboard Shortcut`.
5. Choose a free combination, for example Control-Option-Command-W.
6. Optionally use `File > Add to Dock` or drag the generated app into the Dock.

The global key assignment is a one-time manual step because Apple's `shortcuts` CLI cannot create shortcuts or assign their keyboard combinations. No DMG, Xcode project, signing workflow, or package installer is needed.

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
ai-writer --pro --help
ai-writer-c --help
ai-writer-c --pro --help
```

Test Pi as the default:

```bash
ai-writer "hallo ich wollte fragen ob das morgen passt"
/usr/bin/pbpaste
```

The German input should be returned as natural English because English is the initial language mode.

Test Codex explicitly:

```bash
ai-writer --codex "hallo ich wollte fragen ob das morgen passt"
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

## Make Codex the Default Later

Edit:

```text
$HOME/.config/ai-handy-writer/config.zsh
```

Set:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
```

Afterward, `ai-writer` starts Codex and `ai-writer --pi` still starts Pi.

## Change Model, Reasoning, or Tier

The shared runtime values are stored in `config.zsh`:

```zsh
AI_WRITER_MODEL="gpt-6-luna"
AI_WRITER_REASONING="medium"
AI_WRITER_CODEX_SERVICE_TIER="fast"
AI_WRITER_C_MODEL="claude-haiku-5-5"
AI_WRITER_C_REASONING="medium"
```

The launcher passes the model and reasoning values to both harnesses. The dedicated Codex profile contains the same values as fallbacks.

The installed `ai-writer-c` command starts Pi with the Anthropic provider,
`claude-haiku-5-5`, and medium thinking. It uses the same Writer skill and
clipboard behavior as `ai-writer`. The local `~/.pi/agent/models.json` entry
enables adaptive thinking, which Haiku 5.5 requires instead of a thinking-token
budget. The equivalent long command is `ai-writer --claude`.

Add `--pro` before any text to enable stronger editing with high thinking:

```zsh
ai-writer --pro
ai-writer-c --pro
ai-writer --pro "de: please improve this text"
```

This keeps Luna for `ai-writer` and Haiku for `ai-writer-c`. The launcher
selects pro editing in trusted instructions, while the skill defines the
stronger rewriting rules. Saved defaults stay at medium thinking. A literal
`--pro` in pasted text or after `--` does not change the mode.

If Pi reports an expired Anthropic refresh token, start `pi`, run `/login`,
select Anthropic, and complete authentication. This is required for a live
Haiku request; local launcher checks do not validate provider access.

Codex supports the tested `fast` and `standard` tier selections. Live smoke
tests passed for Pi Luna and Haiku at medium and high thinking. Older benchmark
results for lower thinking levels remain documented separately.

## Codex Fast Mode

Only the Codex harness uses Fast mode:

```toml
service_tier = "fast"

[features]
fast_mode = true
```

The setting lives in the dedicated Writer profile and does not affect ordinary Codex sessions.

## Benchmark

The separate translation and correction timing matrices and the default-mode decision are documented in [`BENCHMARKS.md`](BENCHMARKS.md).

Run new matrices with three repetitions per mode:

```bash
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-translation.tsv translation
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-correction.tsv correction
```

Pi Luna `off` produced the fastest raw translation result, while Pi Luna `minimal` won the correction benchmark. Those are historical benchmark results. The installed default now uses Pi Luna with `medium` thinking, and `ai-writer-c` selects Claude Haiku 5.5 with `medium` thinking. Both original harness switches remain available.
