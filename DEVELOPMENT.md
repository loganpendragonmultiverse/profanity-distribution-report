# Development contract

Map user-supplied profanity terms by chapter, speaker, and nearby narrative context.

Version 1.1 adds catalog coverage and normalized frequency evidence while preserving the user-supplied, non-judgmental term boundary.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## Version 1.2.0

Set `include_group_rates` to `true` to add `chapter_rates` and `speaker_rates`. Each label maps to `total_words`, matched occurrence `total`, and `per_1000_words` rounded to three decimals. Denominators count the same Unicode word tokens as the global count. Repeated chapter titles and speaker labels intentionally aggregate; every passage contributes once, including passages without hits. Empty chapters and speakers with empty passages receive zero denominators and zero rates. A speaker absent from all passages has no row. Existing global fields, literal term matching and default output are unchanged.
