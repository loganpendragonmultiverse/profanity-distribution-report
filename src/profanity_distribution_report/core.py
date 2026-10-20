from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

PROJECT = "profanity-distribution-report"


def _profanity(data: dict[str, Any]) -> dict[str, Any]:
    raw_terms = data.get("terms")
    if not isinstance(raw_terms, list) or not raw_terms:
        raise ValueError("terms must be a non-empty list of non-empty strings")
    if any(not isinstance(term, str) or not term.strip() for term in raw_terms):
        raise ValueError("terms must be a non-empty list of non-empty strings")
    literals = [term.strip() for term in raw_terms]
    terms = [term.casefold() for term in literals]
    if len(terms) != len(set(terms)):
        raise ValueError("terms must be unique ignoring case")
    chapters = data.get("chapters", [])
    if not isinstance(chapters, list):
        raise TypeError("chapters must be a list of objects")
    for chapter in chapters:
        if not isinstance(chapter, dict):
            raise TypeError("each chapter must be an object")
        if "title" in chapter and not isinstance(chapter["title"], str):
            raise TypeError("chapter title must be a string")
        passages = chapter.get("passages", [])
        if not isinstance(passages, list):
            raise TypeError("passages must be a list of objects")
        for passage in passages:
            if not isinstance(passage, dict):
                raise TypeError("each passage must be an object")
            if any(
                key in passage and not isinstance(passage[key], str) for key in ("text", "speaker")
            ):
                raise ValueError("passage text and speaker must be strings")
    include_rates = data.get("include_group_rates", False)
    if not isinstance(include_rates, bool):
        raise TypeError("include_group_rates must be a boolean")
    chapter_words: Counter[str] = Counter()
    speaker_words: Counter[str] = Counter()
    occurrences = []
    total_words = 0
    for chapter in chapters:
        chapter_label = str(chapter.get("title", "Untitled"))
        chapter_words[chapter_label] += 0
        for passage in chapter.get("passages", []):
            text = str(passage.get("text", ""))
            word_count = len(re.findall(r"\b\w+\b", text))
            total_words += word_count
            chapter_words[chapter_label] += word_count
            speaker_words[str(passage.get("speaker", "Narration"))] += word_count
            for term, literal in zip(terms, literals):
                for match in re.finditer(
                    f"(?<!\\w){re.escape(literal)}(?!\\w)", text, re.IGNORECASE
                ):
                    occurrences.append(
                        {
                            "term": term,
                            "chapter": str(chapter.get("title", "Untitled")),
                            "speaker": str(passage.get("speaker", "Narration")),
                            "context": text[max(0, match.start() - 30) : match.end() + 30].strip(),
                        }
                    )
    by_term = Counter(item["term"] for item in occurrences)
    report = {
        "total": len(occurrences),
        "total_words": total_words,
        "terms_requested": len(terms),
        "terms_matched": sum(term in by_term for term in terms),
        "zero_hit_terms": [term for term in terms if term not in by_term],
        "by_term": dict(by_term),
        "per_1000_words": {
            term: round(count * 1000 / total_words, 3) if total_words else 0
            for term, count in by_term.items()
        },
        "by_chapter": dict(Counter(item["chapter"] for item in occurrences)),
        "by_speaker": dict(Counter(item["speaker"] for item in occurrences)),
        "occurrences": occurrences,
    }

    if include_rates:
        for group, denominators in [("chapter", chapter_words), ("speaker", speaker_words)]:
            hits = Counter(item[group] for item in occurrences)
            report[f"{group}_rates"] = {
                label: {
                    "total_words": words,
                    "total": hits[label],
                    "per_1000_words": round(hits[label] * 1000 / words, 3) if words else 0,
                }
                for label, words in denominators.items()
            }
    return report


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise TypeError("input must be a JSON object")
    return {"version": 1, "project": PROJECT, **_profanity(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
