# AI Handy Writer installieren

Diese Anleitung installiert AI Handy Writer fuer Codex und Pi. Codex ist danach der Standard-Harness. Pi bleibt ueber `--pi` erreichbar.

## Voraussetzungen

1. macOS mit `/usr/bin/pbcopy`
2. Node.js und npm
3. Codex CLI mit ChatGPT-Login
4. Pi Coding Agent mit OpenAI-Codex-Login
5. `~/.local/bin` im `PATH`

Versionen und Login pruefen:

```bash
codex --version
codex login status
pi --version
```

## Pi aktualisieren

GPT-5.6 Luna wird im Pi-Modellkatalog ab der hier getesteten Version 0.83.0 gefuehrt:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.83.0
pi --version
pi --list-models | grep 'gpt-5.6-luna'
```

## Installieren

Im Repository:

```bash
chmod +x bin/ai-writer scripts/install.sh
./scripts/install.sh
```

Das Skript installiert:

```text
$HOME/.codex/skills/ai-handy-writer/SKILL.md
$HOME/.pi/agent/skills/ai-handy-writer/SKILL.md
$HOME/.codex/ai-handy-writer.config.toml
$HOME/.config/ai-handy-writer/config.zsh
$HOME/.config/ai-handy-writer/copy_codex_turn_to_clipboard.py
$HOME/.local/bin/ai-writer
$HOME/.local/bin/ai-handy-writer
```

Vorhandene alte Verzeichnisse unter `~/.codex/skills/write-skill` und `~/.pi/agent/skills/write-skill` werden mit Zeitstempel hier archiviert:

```text
$HOME/.local/share/ai-handy-writer/backups/
```

## Alte Shell-Funktion entfernen

Falls `ai-writer` bisher als Funktion in `~/.zshrc` definiert war, entferne den gesamten alten Funktionsblock und lade die Shell neu:

```bash
source ~/.zshrc
type ai-writer
```

Die Ausgabe soll auf `$HOME/.local/bin/ai-writer` zeigen und nicht mehr auf eine Shell-Funktion.

## Tests

Hilfe und Standardwerte:

```bash
ai-writer --help
```

Codex als Standard:

```bash
ai-writer "hallo ich wollte fragen ob das morgen passt"
/usr/bin/pbpaste
```

Pi explizit:

```bash
ai-writer --pi "hallo ich wollte fragen ob das morgen passt"
/usr/bin/pbpaste
```

Harness explizit waehlen:

```bash
ai-writer --codex
ai-writer --pi
```

Alias pruefen:

```bash
ai-handy-writer --help
```

## Standard spaeter auf Pi umstellen

Oeffne:

```text
$HOME/.config/ai-handy-writer/config.zsh
```

Setze:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
```

Danach startet `ai-writer` Pi. Codex bleibt mit `ai-writer --codex` erreichbar.

## Modell oder Reasoning aendern

Die gemeinsamen Laufzeitwerte stehen ebenfalls in `config.zsh`:

```zsh
AI_WRITER_MODEL="gpt-5.6-luna"
AI_WRITER_REASONING="low"
AI_WRITER_CODEX_SERVICE_TIER="fast"
```

Der Launcher uebergibt diese Werte an beide Harnesses. Das installierte Codex-Profil enthaelt dieselben Werte als sichere Fallbacks.

Fuer Codex sind `fast` und `standard` gueltige Service-Tier-Werte. Reasoning
`none` und `low` wurden mit Codex getestet. Pi wurde mit Thinking `off`,
`minimal` und `low` getestet.

## Codex Fast Mode

Nur der Codex-Modus verwendet Fast:

```toml
service_tier = "fast"

[features]
fast_mode = true
```

Die Einstellung liegt im dedizierten Writer-Profil und beeinflusst normale Codex-Sitzungen nicht.

## Benchmark

Die vollstaendige Messmatrix und der begruendete Standardmodus stehen in
`BENCHMARKS.md`. Ein neuer Lauf mit drei Wiederholungen pro Modus:

```bash
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-benchmark.tsv
```

Der schnellste reine Messwert stammt von Pi Luna `off`. Wegen wiederholter
Bedeutungsfehler im Negations-Kontrolltest bleibt Codex Luna Fast `low` als
schnellster zuverlaessiger Modus der Standard.
