# Profanity Distribution Report

[![CI](https://github.com/loganpendragonmultiverse/profanity-distribution-report/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/profanity-distribution-report/actions/workflows/ci.yml)

Map user-supplied profanity terms by chapter, speaker, and nearby narrative context. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
profanity-distribution examples/sample.json
profanity-distribution examples/sample.json --format json --output report.json
```

The example documents the complete input shape. Version 1.1 adds total word counts, per-1,000-word rates, matched-term coverage, and a zero-hit list so an intentionally broad custom catalog can be audited. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All manuscript text and custom term lists stay local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

No universal word list is bundled. Users provide exact terms appropriate to their audience; matching is literal and does not judge offensiveness or intent.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0: chapter and speaker rates

Set `include_group_rates` to `true` to add `chapter_rates` and `speaker_rates`. Each label maps to `total_words`, matched occurrence `total`, and `per_1000_words` rounded to three decimals. Denominators count the same Unicode word tokens as the global count. Repeated chapter titles and speaker labels intentionally aggregate; every passage contributes once, including passages without hits. Empty chapters and speakers with empty passages receive zero denominators and zero rates. A speaker absent from all passages has no row. Existing global fields, literal term matching and default output are unchanged.

Try the synthetic example:

```bash
profanity-distribution examples/feature.json --format json
```

## Version 1.2.1: unicode term matching and checked input

Catalog entries must be non-empty strings in a non-empty `terms` list; chapters and passages must be lists of objects, and supplied titles, speakers and text must be strings. Missing chapter/passages lists and missing text retain their empty defaults. Matching uses the original trimmed literal with Python Unicode case-insensitive regex semantics and word-edge guards, while report keys and duplicate checks retain case-folded catalog labels. This fixes terms such as `Straße` and `İ` without treating every multi-character case-fold expansion as an equivalent match.

Invalid JSON shapes and option types produce a concise `error:` diagnostic and exit status 2. A report is created exclusively: existing files, directories and symbolic links (including dangling links) are refused, and the input is never overwritten. Output parent directories must already exist. This prevents replacing an existing output leaf; it does not promise protection against hostile concurrent replacement of parent directories.
