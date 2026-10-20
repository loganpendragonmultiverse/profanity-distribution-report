# Development contract

Map user-supplied profanity terms by chapter, speaker, and nearby narrative context.

Version 1.1 adds catalog coverage and normalized frequency evidence while preserving the user-supplied, non-judgmental term boundary.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## Version 1.2.0

Set `include_group_rates` to `true` to add `chapter_rates` and `speaker_rates`. Each label maps to `total_words`, matched occurrence `total`, and `per_1000_words` rounded to three decimals. Denominators count the same Unicode word tokens as the global count. Repeated chapter titles and speaker labels intentionally aggregate; every passage contributes once, including passages without hits. Empty chapters and speakers with empty passages receive zero denominators and zero rates. A speaker absent from all passages has no row. Existing global fields, literal term matching and default output are unchanged.

## Version 1.2.1: unicode term matching and checked input

Catalog entries must be non-empty strings in a non-empty `terms` list; chapters and passages must be lists of objects, and supplied titles, speakers and text must be strings. Missing chapter/passages lists and missing text retain their empty defaults. Matching uses the original trimmed literal with Python Unicode case-insensitive regex semantics and word-edge guards, while report keys and duplicate checks retain case-folded catalog labels. This fixes terms such as `Straße` and `İ` without treating every multi-character case-fold expansion as an equivalent match.

Invalid JSON shapes and option types produce a concise `error:` diagnostic and exit status 2. A report is created exclusively: existing files, directories and symbolic links (including dangling links) are refused, and the input is never overwritten. Output parent directories must already exist. This prevents replacing an existing output leaf; it does not promise protection against hostile concurrent replacement of parent directories.
