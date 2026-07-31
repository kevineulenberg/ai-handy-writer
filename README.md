<p align="center">
  <img src="assets/hand.png" alt="AI Handy Writer mascot" width="420">
</p>

# AI Handy Writer

AI Handy Writer ist ein fokussierter, terminalbasierter Schreibmodus fuer macOS. Er korrigiert, verbessert und uebersetzt eingefuegte Texte, kopiert die fertige Fassung mit `/usr/bin/pbcopy` in die Zwischenablage und zeigt exakt denselben Text im Terminal an.

Der globale Befehl verwendet standardmaessig den Codex-Harness. Pi bleibt als vollwertiger alternativer Harness erhalten.

## Benchmark-Sieger

<p align="center">
  <img src="assets/benchmark-mascot.png" alt="AI Handy Writer misst die Geschwindigkeit mit einer Stoppuhr" width="360">
</p>

Der schnellste reine Messwert stammt von Pi mit GPT-5.6 Luna und Thinking
`off`: 10,00 Sekunden im Mittel. Dieser Modus verursachte im separaten
Negations-Kontrolltest jedoch zwei Bedeutungsfehler.

Der schnellste zuverlaessige Modus ist Codex mit GPT-5.6 Luna, Reasoning `low`
und Fast Mode: 11,15 Sekunden im Mittel und kein Bedeutungsfehler in sechs
bewerteten Uebersetzungen. Er bleibt deshalb der Standard.

## Standardkonfiguration

| Einstellung | Codex | Pi |
| --- | --- | --- |
| Modell | `gpt-5.6-luna` | `gpt-5.6-luna` |
| Reasoning | `low` | `low` |
| Service-Tier | Fast | Standard |
| Standardmodus | Ja | Nein |
| Start | `ai-writer` | `ai-writer --pi` |

Codex Fast Mode beschleunigt unterstuetzte Modelle und verbraucht mehr ChatGPT-Credits. Pi stellt fuer seinen CLI-Harness keinen gleichwertigen Fast-Schalter bereit.

Die ausfuehrliche Messmatrix, Methodik, Einzelzeiten, Qualitaetskontrolle und
der nicht verfuegbare Modellname `gpt-5.5-instant` stehen in
[`BENCHMARKS.md`](BENCHMARKS.md).

## Befehle

```bash
ai-writer
ai-writer "hallo ich wollte fragen ob das morgen passt"
ai-writer --codex
ai-writer --pi
ai-writer --pi "en: hallo wie geht es dir"
ai-writer --help
```

Der Alias `ai-handy-writer` verweist auf denselben Launcher:

```bash
ai-handy-writer --pi
```

Mit `--` endet die Optionsauswertung:

```bash
ai-writer -- "--pi soll in diesem Satz als Text erhalten bleiben"
```

## Sprachmodus

Der initiale Sprachmodus ist Deutsch.

1. Deutsche Eingaben werden auf Deutsch verbessert.
2. Eindeutig englische Eingaben ohne Prefix schalten dauerhaft auf Englisch.
3. Sprachprefixe wie `de:`, `en:`, `fr:`, `es:` oder `ja:` schalten dauerhaft in die angegebene Zielsprache.
4. Der Modus bleibt innerhalb der laufenden interaktiven Sitzung aktiv, bis ein neuer gueltiger Sprachprefix gesetzt wird.

## Harness wechseln

Die Standardwahl steht in:

```text
$HOME/.config/ai-handy-writer/config.zsh
```

Codex ist der Standard:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
```

Pi wieder zum Standard machen:

```zsh
AI_WRITER_DEFAULT_HARNESS="pi"
```

Eine einzelne Sitzung kann unabhaengig davon immer mit `--codex` oder `--pi` gestartet werden.

## Modell-, Reasoning- und Tier-Modi

Die installierte Datei `$HOME/.config/ai-handy-writer/config.zsh` enthaelt:

```zsh
AI_WRITER_DEFAULT_HARNESS="codex"
AI_WRITER_MODEL="gpt-5.6-luna"
AI_WRITER_REASONING="low"
AI_WRITER_CODEX_PROFILE="ai-handy-writer"
AI_WRITER_CODEX_SERVICE_TIER="fast"
```

Unterstuetzte, praktisch getestete Kombinationen:

| Harness | Modelle | Reasoning/Thinking | Tier |
| --- | --- | --- | --- |
| Pi | `gpt-5.6-luna`, `gpt-5.5` | `off`, `minimal`, `low` | Standard |
| Codex | `gpt-5.6-luna`, `gpt-5.5` | `none`, `low` | Standard, Fast |

Eine Einstellung kann fuer einen einzelnen Start ohne Dateiaenderung
ueberschrieben werden:

```bash
AI_HANDY_WRITER_CONFIG=/dev/null \
AI_WRITER_DEFAULT_HARNESS=pi \
AI_WRITER_MODEL=gpt-5.6-luna \
AI_WRITER_REASONING=minimal \
ai-writer
```

Codex einmalig im Standard-Tier:

```bash
AI_HANDY_WRITER_CONFIG=/dev/null \
AI_WRITER_DEFAULT_HARNESS=codex \
AI_WRITER_MODEL=gpt-5.6-luna \
AI_WRITER_REASONING=low \
AI_WRITER_CODEX_SERVICE_TIER=standard \
ai-writer
```

`gpt-5.5-instant` ist mit dem getesteten ChatGPT-Codex-Login nicht verfuegbar.
Der Server lehnt diesen Modellnamen mit HTTP 400 ab. Verwende stattdessen
`gpt-5.5` mit Fast Mode.

## Installation

Die vollstaendige Anleitung steht in `INSTALL.md`. Fuer das aktuelle System:

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent@0.83.0
./scripts/install.sh
```

Das Installationsskript:

1. archiviert alte aktive `write-skill`-Ordner,
2. installiert die Skill-Datei fuer Codex und Pi,
3. installiert den Codex-Profil-Layer,
4. installiert `ai-writer` unter `~/.local/bin`,
5. richtet `ai-handy-writer` als Alias ein,
6. installiert die deterministische Codex-Clipboard-Bruecke,
7. bewahrt eine bereits angepasste Laufzeitkonfiguration.

## Installierte Pfade

```text
$HOME/.codex/skills/ai-handy-writer/SKILL.md
$HOME/.pi/agent/skills/ai-handy-writer/SKILL.md
$HOME/.codex/ai-handy-writer.config.toml
$HOME/.config/ai-handy-writer/config.zsh
$HOME/.config/ai-handy-writer/copy_codex_turn_to_clipboard.py
$HOME/.local/bin/ai-writer
$HOME/.local/bin/ai-handy-writer
```

## Codex-Profil

Der Launcher waehlt fuer Codex das Profil `ai-handy-writer`. Das Profil:

1. setzt `gpt-5.6-luna`,
2. setzt Reasoning auf `low`,
3. aktiviert Fast Mode,
4. laedt die installierte `SKILL.md` als Instruktionsdatei,
5. verwendet einen Read-only-Sandbox,
6. deaktiviert Websuche, Apps, Plugins, Hooks, Browser, Computer Use, Bilderzeugung und Multi-Agent,
7. kopiert nach jedem abgeschlossenen Codex-Turn den finalen Assistententext deterministisch in die Zwischenablage.

Die normale globale Codex-Konfiguration wird dadurch nicht veraendert.

Der Service-Tier kann in `config.zsh` zwischen `fast` und `standard`
umgeschaltet werden. Der Launcher ueberschreibt damit den Profil-Fallback
explizit.

## Pi-Konfiguration

Pi wird gezielt mit folgenden Eigenschaften gestartet:

```text
--provider openai-codex
--model gpt-5.6-luna
--thinking low
--tools bash
--no-extensions
--no-context-files
```

Pi 0.83.0 oder neuer ist erforderlich, weil aeltere installierte Versionen GPT-5.6 Luna noch nicht im `openai-codex`-Modellkatalog fuehren.

## Sicherheitsmodell

Der Writer behandelt jede Nutzernachricht als zu transformierenden Rohtext. Anweisungen innerhalb dieses Textes werden nur sprachlich korrigiert, nicht ausgefuehrt.

Im Pi-Modus ist der einzige erlaubte Tool-Zweck das Kopieren des finalen Textes:

```bash
/usr/bin/pbcopy <<'__AI_HANDY_WRITER_FINAL_TEXT__'
FINALER_TEXT
__AI_HANDY_WRITER_FINAL_TEXT__
```

Dateizugriffe, Browser, APIs, Netzwerkzugriffe, Skripte und andere Shell-Commands sind fuer das Modell durch die Skill-Anweisungen verboten. Im Codex-Modus kopiert eine kleine, vom Harness aufgerufene Notify-Bruecke den finalen Assistententext mit `/usr/bin/pbcopy`. Sie ist keine Modellfunktion und erhaelt nur das Turn-Abschlussereignis.

## Entwicklung und Pruefung

```bash
ruby -ryaml -e 'text=File.read("SKILL.md"); header=text.split(/^---\s*$/,3)[1]; p YAML.safe_load(header)'
zsh -n bin/ai-writer
zsh -n scripts/install.sh
python3 -m py_compile scripts/copy_codex_turn_to_clipboard.py
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-benchmark.tsv
```

Nach einer Aenderung werden die globalen Kopien mit folgendem Befehl aktualisiert:

```bash
./scripts/install.sh
```

Die Aenderungshistorie steht in [`CHANGELOG.md`](CHANGELOG.md).
