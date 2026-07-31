# Changelog

## 2026-07-31

### Hinzugefuegt

- Dedizierter Codex-Harness mit eigenem `ai-handy-writer`-Profil.
- Umschaltung zwischen Codex und Pi mit `--codex` und `--pi`.
- Gemeinsame Modell- und Reasoning-Konfiguration fuer beide Harnesses.
- Konfigurierbarer Codex-Service-Tier `fast` oder `standard`.
- Unterstuetzung fuer GPT-5.6 Luna und GPT-5.5 in den dokumentierten Modi.
- Reproduzierbares Benchmark-Skript mit 13 Harness-, Modell-, Reasoning- und
  Tier-Kombinationen.
- Vollstaendige Benchmark-Dokumentation und TSV-Rohdaten.
- Neues Benchmark-Maskottchen mit Stoppuhr und Zielflagge.
- Deterministische Codex-Clipboard-Bruecke ueber das Turn-Abschlussereignis.
- Installationsskript fuer Skill, Profil, Launcher, Konfiguration und Backups.

### Geaendert

- Der initiale Sprachmodus ist Deutsch; eindeutig englischer Text schaltet
  weiterhin automatisch und dauerhaft auf Englisch.
- Beide Harnesses verwenden standardmaessig GPT-5.6 Luna mit Reasoning `low`.
- Codex verwendet Fast Mode, Pi den Standard-Tier.
- Codex Luna Fast `low` bleibt nach Geschwindigkeits- und Qualitaetsvergleich
  der Standardmodus.
- Pi wurde fuer GPT-5.6-Luna-Unterstuetzung auf Version 0.83.0 aktualisiert.
- Der globale Befehl ist jetzt ein installierter Launcher statt einer
  Shell-Funktion.

### Entfernt

- Alte aktive `write-skill`-Installationen; sie werden beim Installieren
  zeitgestempelt archiviert.
- Das nicht mehr benoetigte generische Clipboard-Hilfsskript.
