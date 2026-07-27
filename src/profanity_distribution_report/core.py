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
    occurrences = []
    for chapter in data.get("chapters", []):
        for passage in chapter.get("passages", []):
            text = str(passage.get("text", ""))
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
    return {
        "total": len(occurrences),
        "by_term": dict(Counter(item["term"] for item in occurrences)),
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
