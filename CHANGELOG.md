# Changelog

## 2026-07-31 - Instant macOS Launcher

### Added

- Optional locally compiled `AI Writer.app` that opens the standard macOS Terminal and starts the configured Writer immediately.
- Double-clickable `AI Writer.command` fallback using the installed launcher instead of the obsolete shell function.
- Dedicated `scripts/install-macos-launcher.zsh` installer with recoverable backups.
- Setup documentation for a global macOS Shortcuts hotkey, Dock access, and the one-time Automation permission.

### Changed

- Existing legacy `Desktop/AI Writer.command` launchers are archived and updated when the optional installer runs.
- The generated app remains local and is built from versioned AppleScript source, avoiding DMG packaging and committed app bundles.

## 2026-07-31 - Correction Benchmark

### Added

- Separate correction and polishing benchmark for the Writer's second primary use case.
- Character-matched English correction fixture with deliberate spelling and grammar errors.
- Raw timing and output data for 39 successful Codex and Pi correction runs.
- Reproducible `translation` and `correction` scenarios in `scripts/benchmark.zsh`.

### Changed

- Reorganized the benchmark documentation into distinct translation and correction performance sections.
- Expanded the README and installation guide with both benchmark scenarios.
- Replaced the incomplete correction dataset after renewing authentication and rerunning the complete 39-run matrix.
- Kept Codex GPT-5.6 Luna with Reasoning `low` and Fast mode as the default because the translation quality controls remain the strongest reliability signal.

## 2026-07-31 - English Repository and Runtime

### Changed

- Translated all repository documentation, skill instructions, runtime prompts, and benchmark analysis into English.
- Changed the initial persistent Writer language from German to English.
- Non-English input without a language prefix is now translated into English.
- Preserved explicit language-prefix switching, multilingual examples, the German benchmark fixture, and the published benchmark data.
- Kept Codex GPT-5.6 Luna with Reasoning `low` and Fast mode as the default.

## 2026-07-31 - Codex Modes and Benchmarks

### Added

- Dedicated Codex harness with its own `ai-handy-writer` profile.
- Harness selection through `--codex` and `--pi`.
- Shared model and reasoning configuration for both harnesses.
- Configurable Codex service tier with `fast` and `standard`.
- Tested GPT-5.6 Luna and GPT-5.5 modes.
- Reproducible benchmark script covering 13 harness, model, reasoning, and tier combinations.
- Complete benchmark documentation and raw TSV data.
- Benchmark mascot with a stopwatch and finish flag.
- Deterministic Codex clipboard bridge using the turn-completed notification.
- Installer for the skill, profile, launcher, configuration, and legacy backups.

### Changed

- Both harnesses use GPT-5.6 Luna with Reasoning `low` by default.
- Codex uses Fast mode while Pi uses the Standard tier.
- Codex Luna Fast `low` remains the default after the speed and quality comparison.
- Updated Pi to version 0.83.0 for GPT-5.6 Luna support.
- Replaced the former shell function with an installed global launcher.

### Removed

- Active legacy `write-skill` installations. The installer archives them with a timestamp.
- The obsolete generic clipboard helper script.
