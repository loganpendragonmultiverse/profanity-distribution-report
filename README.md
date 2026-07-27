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
