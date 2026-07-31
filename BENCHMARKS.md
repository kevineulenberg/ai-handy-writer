# AI Handy Writer Benchmarks

Stand: 31. Juli 2026

## Ergebnis

Der schnellste reine Messwert stammt von Pi mit GPT-5.6 Luna und deaktiviertem
Thinking. Dieser Modus benoetigte im Mittel 10,00 Sekunden. Im separaten
Negations-Kontrolltest veraenderte er jedoch in zwei von drei Laeufen die
Bedeutung von "laenger als 10 Sekunden" zu "less than 10 seconds".

Als Standard bleibt deshalb Codex mit GPT-5.6 Luna, Reasoning `low` und Fast
Mode aktiv. Dieser Modus war mit 11,15 Sekunden im Mittel nur 1,16 Sekunden
langsamer als der reine Geschwindigkeitssieger und lieferte in allen sechs
bewerteten Uebersetzungen ein bedeutungstreues Ergebnis.

## Hauptmessung

Alle Zeiten messen den kompletten realen Workflow vom Prozessstart bis zur
vollstaendigen sichtbaren Antwort. CLI-Start, Modellantwort und Clipboard-
Schritt sind enthalten.

| Rang | Harness | Modell | Reasoning | Tier | Mittel | Median | Bereich |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | Pi | GPT-5.6 Luna | `off` | Standard | 10,00 s | 9,39 s | 9,26-11,35 s |
| 2 | Pi | GPT-5.6 Luna | `minimal` | Standard | 10,57 s | 10,62 s | 9,53-11,54 s |
| 3 | Codex | GPT-5.6 Luna | `low` | Fast | 11,15 s | 11,08 s | 11,03-11,35 s |
| 4 | Codex | GPT-5.5 | `none` | Fast | 11,41 s | 12,01 s | 10,01-12,20 s |
| 5 | Pi | GPT-5.6 Luna | `low` | Standard | 11,59 s | 10,57 s | 10,01-14,19 s |
| 6 | Pi | GPT-5.5 | `low` | Standard | 11,98 s | 11,15 s | 10,21-14,59 s |
| 7 | Pi | GPT-5.5 | `off` | Standard | 12,36 s | 11,32 s | 10,54-15,21 s |
| 8 | Codex | GPT-5.5 | `none` | Standard | 13,77 s | 13,50 s | 13,00-14,80 s |
| 9 | Codex | GPT-5.5 | `low` | Fast | 13,88 s | 14,69 s | 12,00-14,95 s |
| 10 | Codex | GPT-5.6 Luna | `none` | Standard | 14,02 s | 14,43 s | 12,74-14,91 s |
| 11 | Codex | GPT-5.6 Luna | `none` | Fast | 14,58 s | 11,15 s | 10,72-21,88 s |
| 12 | Codex | GPT-5.6 Luna | `low` | Standard | 14,87 s | 15,11 s | 13,86-15,65 s |
| 13 | Codex | GPT-5.5 | `low` | Standard | 20,24 s | 21,16 s | 16,33-23,24 s |

Jede Zeile basiert auf drei frischen Einzellaeufen. Runde 2 lief in umgekehrter
Reihenfolge, damit kurzfristige Serverlast nicht immer dieselben Modi trifft.
Alle 39 Hauptlaeufe endeten mit Status `0` und lieferten eine vollstaendige,
bedeutungstreue englische Uebersetzung.

Die Rohdaten inklusive jeder einzelnen Antwort liegen in
[`benchmarks/2026-07-31-tree-canopy.tsv`](benchmarks/2026-07-31-tree-canopy.tsv).

## Testtext

```text
en: Baumwipfelpfade bieten eine einzigartige Möglichkeit, den Wald aus einer völlig neuen Perspektive zu entdecken. Während man sich normalerweise auf den Waldboden konzentriert, führen diese erhöhten Wege Besucherinnen und Besucher direkt in die Baumkronen. Dort eröffnet sich eine faszinierende Welt, die sonst vor allem Vögeln und anderen Waldbewohnern vorbehalten ist.
```

## Bedeutungs-Kontrolltest

Ein zweiter Testtext enthielt die Formulierung "laenger als 10 Sekunden". Sie
deckt Bedeutungsfehler auf, bei denen ein Modus versehentlich "less than 10
seconds" erzeugt.

| Modus | Korrekt | Bedeutungsfehler |
| --- | ---: | ---: |
| Codex Luna Fast `low` | 6/6 | 0 |
| Codex Luna Fast `none` | 6/6 | 0 |
| Codex GPT-5.5 Fast `low` | 6/6 | 0 |
| Pi GPT-5.5 `off` | 6/6 | 0 |
| Pi Luna `minimal` | 5/6 | 1 |
| Pi Luna `low` | 5/6 | 1 |
| Pi Luna `off` | 4/6 | 2 |

Die sechs Bewertungen kombinieren drei Laeufe des Haupttests mit drei Laeufen
des Negations-Kontrolltests. Fuer Modi, die nicht in dieser Tabelle stehen,
wurde keine gleich grosse Kontrollstichprobe ausgefuehrt.

## Nicht verfuegbarer Modellname

Der direkte Aufruf mit `codex -m gpt-5.5-instant` wurde getestet und vom
Codex-Server fuer den ChatGPT-Login mit HTTP 400 abgelehnt:

```text
The 'gpt-5.5-instant' model is not supported when using Codex with a ChatGPT account.
```

Der gueltige Codex-Modellname ist `gpt-5.5`. Fuer niedrige Latenz kann er mit
Fast Mode und einem niedrigen Reasoning-Wert kombiniert werden.

## Benchmark erneut ausfuehren

Voraussetzung ist eine aktuelle globale Installation des Writers:

```bash
./scripts/install.sh
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-benchmark.tsv
```

Das Skript verwendet den festgehaltenen Testtext, fuehrt die 13 Modi in
wechselnder Reihenfolge aus und schreibt TSV-Rohdaten an den angegebenen Pfad.

## Einordnung

Die Messwerte sind eine Momentaufnahme des lokalen Systems, des Netzwerks und
der damaligen Serverauslastung. Drei Laeufe reichen fuer eine praktische
Entscheidung, aber nicht fuer eine allgemeingueltige Aussage ueber die
Modellinfrastruktur. Fuer spaetere Entscheidungen sollten die Messungen erneut
ausgefuehrt und Median, Ausreisser sowie Bedeutungsfehler gemeinsam bewertet
werden.
