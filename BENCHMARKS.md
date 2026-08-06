# AI Handy Writer Benchmarks

Recorded on July 31, 2026.

## Scope and Methodology

AI Handy Writer has two primary use cases:

1. Translate text into the active target language.
2. Correct and polish text that is already in the active target language.

The benchmark therefore contains a separate performance section for each use case. Every reported row is based on three fresh one-shot runs. Round 2 used the reverse order so short-lived server load would not consistently affect the same modes.

Each time measures the complete real workflow from process start to the fully visible response. CLI startup, model response, and clipboard handling are included.

The inputs were deliberately matched by character count:

| Use case | Words | Characters |
| --- | ---: | ---: |
| Translation | 50 | 373 |
| Correction | 60 | 352 |

## Overall Result

For translation, Pi with GPT-5.6 Luna and Thinking disabled produced the fastest raw mean at 10.00 seconds. It also changed the meaning of a negation in two of three dedicated control runs.

For correction, Pi with GPT-5.6 Luna and Thinking `minimal` produced both the fastest mean at 10.39 seconds and the fastest median at 10.36 seconds.

Codex with GPT-5.6 Luna, Reasoning `low`, and Fast mode remains the quality-focused translation recommendation. It was the fastest reliable translation mode, preserved the intended meaning in all six evaluated translations, and corrected every seeded error in the correction benchmark. Pi Luna `minimal` won the correction test, but it produced one meaning error in the six-run translation quality sample.

The installed harness default was changed to Pi with GPT-5.6 Luna and Thinking `low` on August 6, 2026, prioritizing the responsive correction workflow. This runtime preference does not change the recorded benchmark results or the translation-quality recommendation. Codex remains available through `ai-writer --codex`, and Pi can always be selected explicitly with `ai-writer --pi`.

## Translation Performance

### Timing Results

| Rank | Harness | Model | Reasoning | Tier | Mean | Median | Range |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | Pi | GPT-5.6 Luna | `off` | Standard | 10.00 s | 9.39 s | 9.26-11.35 s |
| 2 | Pi | GPT-5.6 Luna | `minimal` | Standard | 10.57 s | 10.62 s | 9.53-11.54 s |
| 3 | Codex | GPT-5.6 Luna | `low` | Fast | 11.15 s | 11.08 s | 11.03-11.35 s |
| 4 | Codex | GPT-5.5 | `none` | Fast | 11.41 s | 12.01 s | 10.01-12.20 s |
| 5 | Pi | GPT-5.6 Luna | `low` | Standard | 11.59 s | 10.57 s | 10.01-14.19 s |
| 6 | Pi | GPT-5.5 | `low` | Standard | 11.98 s | 11.15 s | 10.21-14.59 s |
| 7 | Pi | GPT-5.5 | `off` | Standard | 12.36 s | 11.32 s | 10.54-15.21 s |
| 8 | Codex | GPT-5.5 | `none` | Standard | 13.77 s | 13.50 s | 13.00-14.80 s |
| 9 | Codex | GPT-5.5 | `low` | Fast | 13.88 s | 14.69 s | 12.00-14.95 s |
| 10 | Codex | GPT-5.6 Luna | `none` | Standard | 14.02 s | 14.43 s | 12.74-14.91 s |
| 11 | Codex | GPT-5.6 Luna | `none` | Fast | 14.58 s | 11.15 s | 10.72-21.88 s |
| 12 | Codex | GPT-5.6 Luna | `low` | Standard | 14.87 s | 15.11 s | 13.86-15.65 s |
| 13 | Codex | GPT-5.5 | `low` | Standard | 20.24 s | 21.16 s | 16.33-23.24 s |

All 39 translation runs exited with status `0` and returned a complete, meaning-preserving English translation.

The raw data, including every individual answer, is stored in [`benchmarks/2026-07-31-tree-canopy.tsv`](benchmarks/2026-07-31-tree-canopy.tsv).

### Translation Input

The German input is intentionally preserved because this benchmark measures translation into English:

```text
en: Baumwipfelpfade bieten eine einzigartige Möglichkeit, den Wald aus einer völlig neuen Perspektive zu entdecken. Während man sich normalerweise auf den Waldboden konzentriert, führen diese erhöhten Wege Besucherinnen und Besucher direkt in die Baumkronen. Dort eröffnet sich eine faszinierende Welt, die sonst vor allem Vögeln und anderen Waldbewohnern vorbehalten ist.
```

### Meaning Control Test

A second translation input contained the phrase "longer than 10 seconds." It detects meaning errors where a mode accidentally returns "less than 10 seconds."

| Mode | Correct | Meaning errors |
| --- | ---: | ---: |
| Codex Luna Fast `low` | 6/6 | 0 |
| Codex Luna Fast `none` | 6/6 | 0 |
| Codex GPT-5.5 Fast `low` | 6/6 | 0 |
| Pi GPT-5.5 `off` | 6/6 | 0 |
| Pi Luna `minimal` | 5/6 | 1 |
| Pi Luna `low` | 5/6 | 1 |
| Pi Luna `off` | 4/6 | 2 |

The six evaluations combine three main-test translations with three negation-control translations. Modes omitted from this table did not receive an equally sized control sample.

## Correction Performance

### Timing Results

| Rank | Harness | Model | Reasoning | Tier | Mean | Median | Range |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: |
| 1 | Pi | GPT-5.6 Luna | `minimal` | Standard | 10.39 s | 10.36 s | 10.09-10.73 s |
| 2 | Pi | GPT-5.5 | `off` | Standard | 10.50 s | 10.68 s | 9.90-10.93 s |
| 3 | Pi | GPT-5.5 | `low` | Standard | 11.42 s | 12.02 s | 10.20-12.04 s |
| 4 | Pi | GPT-5.6 Luna | `off` | Standard | 11.50 s | 10.48 s | 10.37-13.63 s |
| 5 | Codex | GPT-5.6 Luna | `none` | Fast | 12.28 s | 11.51 s | 11.49-13.84 s |
| 6 | Pi | GPT-5.6 Luna | `low` | Standard | 12.48 s | 13.32 s | 10.16-13.96 s |
| 7 | Codex | GPT-5.5 | `none` | Fast | 12.83 s | 11.09 s | 10.75-16.64 s |
| 8 | Codex | GPT-5.5 | `none` | Standard | 12.91 s | 13.15 s | 11.73-13.85 s |
| 9 | Codex | GPT-5.6 Luna | `none` | Standard | 13.40 s | 13.24 s | 12.67-14.29 s |
| 10 | Codex | GPT-5.5 | `low` | Fast | 14.51 s | 15.25 s | 11.52-16.77 s |
| 11 | Codex | GPT-5.6 Luna | `low` | Standard | 14.97 s | 14.24 s | 14.07-16.60 s |
| 12 | Codex | GPT-5.5 | `low` | Standard | 15.65 s | 14.98 s | 14.09-17.88 s |
| 13 | Codex | GPT-5.6 Luna | `low` | Fast | 18.72 s | 12.51 s | 12.24-31.40 s |

All 39 correction runs exited with status `0`. Every output corrected the seeded spelling, grammar, and agreement errors while preserving the intended meaning. Minor stylistic differences included `treetop` versus `tree-top` and different pronoun choices.

The complete raw data is stored in [`benchmarks/2026-07-31-english-correction.tsv`](benchmarks/2026-07-31-english-correction.tsv).

### Correction Input

The correction input is already English and contains several deliberate errors:

```text
en: Tree top walks are one of the most interessting ways to explore a forest from a completly different perspective. Instead of walking on the ground, visitors can move along wooden or steel pathways that are build high above the forest floor. From there, you can see old trees, nesting birds and wild animals that visitors would normaly never notice.
```

### Translation versus Correction

The correction task was not uniformly faster than translation. Across the four Codex configurations without Reasoning, correction averaged 12.85 seconds. The four Codex configurations with Reasoning `low` averaged 15.96 seconds, making the no-Reasoning group 3.11 seconds faster in this sample.

Fast mode beat its matching Standard configuration in three of four correction comparisons. The default Codex Luna Fast `low` mode averaged 18.72 seconds for correction versus 11.15 seconds for translation, but its correction median was 12.51 seconds. A single 31.40-second outlier substantially increased its mean. This illustrates why task type should not be treated as the only latency driver and why median, range, server load, model, Reasoning, and service tier should be evaluated together.

## Unsupported Model Name

The exact command using `codex -m gpt-5.5-instant` was tested and rejected by the Codex server for the ChatGPT login with HTTP 400:

```text
The 'gpt-5.5-instant' model is not supported when using Codex with a ChatGPT account.
```

The valid Codex model name is `gpt-5.5`. Combine it with Fast mode and a low Reasoning value when lower latency is required.

## Reproduce the Benchmarks

Install the current Writer configuration first:

```bash
./scripts/install.sh
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-translation.tsv translation
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-correction.tsv correction
```

The third argument selects the use case. Omitting it keeps `translation` as the backward-compatible default. Both scenarios run the same 13 mode combinations in alternating order and write raw TSV data to the selected path.

## Interpretation

The translation timings are retained as the dated baseline produced before the repository and runtime instructions were translated into English. The correction timings were recorded after that language-only source conversion. The harnesses, models, Reasoning levels, service tiers, and explicit `en:` target-language prefix are otherwise comparable.

These results are snapshots of one machine, network, authentication state, and period of server load. Three runs are sufficient for a practical local comparison but not for a universal claim about model infrastructure. Future comparisons should rerun both matrices and evaluate median, outliers, failures, and meaning preservation together.
