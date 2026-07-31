# AI Handy Writer Benchmarks

Recorded on July 31, 2026.

## Result

The fastest raw result came from Pi with GPT-5.6 Luna and Thinking disabled. It averaged 10.00 seconds. In the separate negation control test, however, it changed the meaning of "longer than 10 seconds" to "less than 10 seconds" in two of three runs.

Codex with GPT-5.6 Luna, Reasoning `low`, and Fast mode therefore remains the default. It averaged 11.15 seconds, only 1.16 seconds slower than the raw speed winner, and preserved the intended meaning in all six evaluated translations.

## Main Measurement

Each time measures the complete real workflow from process start to the fully visible response. CLI startup, model response, and clipboard handling are included.

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

Each row contains three fresh one-shot runs. Round 2 used the reverse order so short-lived server load would not consistently affect the same modes. All 39 main runs exited with status `0` and returned a complete, meaning-preserving English translation.

The raw data, including every individual answer, is stored in [`benchmarks/2026-07-31-tree-canopy.tsv`](benchmarks/2026-07-31-tree-canopy.tsv).

## Test Input

The German input is intentionally preserved because the benchmark measures translation into English:

```text
en: Baumwipfelpfade bieten eine einzigartige Möglichkeit, den Wald aus einer völlig neuen Perspektive zu entdecken. Während man sich normalerweise auf den Waldboden konzentriert, führen diese erhöhten Wege Besucherinnen und Besucher direkt in die Baumkronen. Dort eröffnet sich eine faszinierende Welt, die sonst vor allem Vögeln und anderen Waldbewohnern vorbehalten ist.
```

## Meaning Control Test

A second test input contained the phrase "longer than 10 seconds". It detects meaning errors where a mode accidentally returns "less than 10 seconds".

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

## Unsupported Model Name

The exact command using `codex -m gpt-5.5-instant` was tested and rejected by the Codex server for the ChatGPT login with HTTP 400:

```text
The 'gpt-5.5-instant' model is not supported when using Codex with a ChatGPT account.
```

The valid Codex model name is `gpt-5.5`. Combine it with Fast mode and a low reasoning value when lower latency is required.

## Reproduce the Benchmark

Install the current Writer configuration first:

```bash
./scripts/install.sh
./scripts/benchmark.zsh 3 /tmp/ai-handy-writer-benchmark.tsv
```

The script uses the preserved German test input, runs all 13 combinations in alternating order, and writes raw TSV data to the selected path.

## Baseline Status

These timings are retained as the dated baseline produced before the repository and runtime instructions were translated into English. The harnesses, models, reasoning levels, service tiers, and explicit `en:` test input remain unchanged. The full 39-run matrix was not repeated for the language-only source conversion.

The results are a snapshot of one machine, network, and period of server load. Three runs are sufficient for a practical local decision but not for a universal claim about model infrastructure. Future comparisons should rerun the matrix and evaluate median, outliers, and meaning errors together.
