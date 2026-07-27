from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any

PROJECT = "profanity-distribution-report"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _profanity(data: dict[str, Any]) -> dict[str, Any]:
    terms = [str(term).casefold().strip() for term in _require(data, "terms") if str(term).strip()]
    if len(terms) != len(set(terms)):
        raise ValueError("terms must be unique ignoring case")
    occurrences = []
    total_words = 0
    for chapter in data.get("chapters", []):
        for passage in chapter.get("passages", []):
            text = str(passage.get("text", ""))
            total_words += len(re.findall(r"\b\w+\b", text))
            for term in terms:
                for match in re.finditer(f"(?<!\\w){re.escape(term)}(?!\\w)", text, re.IGNORECASE):
                    occurrences.append(
                        {
                            "term": term,
                            "chapter": str(chapter.get("title", "Untitled")),
                            "speaker": str(passage.get("speaker", "Narration")),
                            "context": text[max(0, match.start() - 30) : match.end() + 30].strip(),
                        }
                    )
    by_term = Counter(item["term"] for item in occurrences)
    return {
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


def analyze(data: dict[str, Any]) -> dict[str, Any]:
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
