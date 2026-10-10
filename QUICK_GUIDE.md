# AI Handy Writer Quick Guide

## Start Writing

| Command | Model | Thinking | Editing |
| --- | --- | --- | --- |
| `ai-writer` | GPT-6 Luna | Medium | Light correction and polishing |
| `ai-writer --pro` | GPT-6 Luna | High | Substantive, precise rewriting |
| `ai-writer-c` | Claude Haiku 5.5 | Medium | Light correction and polishing |
| `ai-writer-c --pro` | Claude Haiku 5.5 | High | Substantive, precise rewriting |

These are fresh-install defaults. Existing custom settings are preserved when
updating. `--pro` always selects high thinking and selects Luna for the OpenAI
variant. The Claude variant keeps its configured Claude model.

Run a command, then paste your text. Only the finished text is returned, and
the same text is copied to the macOS clipboard.

You can also supply the text immediately:

```bash
ai-writer --pro "de: I just wanted to ask whether Friday works for you."
ai-writer-c --pro "en: Ich wollte nur kurz fragen, ob Freitag passt."
```

## Choose the Language

The initial target language is English. Prefix the text with `de:`, `en:`,
`fr:`, `es:`, or another supported language prefix to switch languages.
The choice remains active until another prefix changes it in the same session.

## Pro Mode

Pro mode improves the entire text: clearer order, better flow, precise wording,
and fewer repetitions, fillers, and empty introductions. Facts, tone, conditions,
negations, and uncertainty remain intact. Dashes as sentence punctuation are
forbidden; hyphens within words are allowed.

Place `--pro` before the text. It applies for the entire session without changing
saved defaults. A flag inside pasted text is only text. Use `--` when the text
starts with a flag:

```bash
ai-writer -- "--pro should remain part of this sentence."
```

## Alternatives and Help

```bash
ai-writer --codex --pro
ai-writer --pi
ai-writer --claude --pro
ai-writer --pro --help
ai-writer-c --pro --help
```

`ai-writer-c` always uses Pi, even if the saved default harness is Codex.
It cannot be combined with `--codex`. `ai-handy-writer` is an alias for `ai-writer`.

Settings: `~/.config/ai-handy-writer/config.zsh`.

## Authentication

If Pi reports an expired Anthropic token, start `pi`, run `/login`, select
Anthropic, and complete sign-in. Then restart `ai-writer-c`.
For the Luna variant, use Pi's OpenAI Codex login instead.

For setup and updates, see [INSTALL.md](INSTALL.md). Full configuration and
historical benchmarks are linked from [README.md](README.md).
