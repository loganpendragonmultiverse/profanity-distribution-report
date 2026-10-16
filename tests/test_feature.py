from copy import deepcopy

import pytest

from profanity_distribution_report.core import analyze


def test_group_denominators_duplicates_empty_and_arithmetic():
    data = {
        "terms": ["blast", "a+b", "absent"],
        "chapters": [
            {
                "title": "Short",
                "passages": [
                    {"speaker": "Mara", "text": "blast a+b"},
                    {"speaker": "Mara", "text": "a calm day"},
                ],
            },
            {
                "title": "Long",
                "passages": [{"speaker": "Ivo", "text": "blast a very calm quiet long day"}],
            },
            {"title": "Short", "passages": [{"speaker": "Mara", "text": "blast"}]},
            {"title": "Empty", "passages": [{"speaker": "Silent", "text": ""}]},
            {"title": "No passages"},
        ],
    }
    original = deepcopy(data)
    baseline = analyze(data)
    result = analyze({**data, "include_group_rates": True})
    assert data == original
    chapters = result.pop("chapter_rates")
    speakers = result.pop("speaker_rates")
    assert result == baseline
    assert chapters["Short"] == {"total_words": 7, "total": 3, "per_1000_words": 428.571}
    assert chapters["Long"] == {"total_words": 7, "total": 1, "per_1000_words": 142.857}
    assert speakers["Mara"] == chapters["Short"]
    assert speakers["Silent"] == {"total_words": 0, "total": 0, "per_1000_words": 0}
    assert chapters["No passages"] == chapters["Empty"] == speakers["Silent"]
    assert sum(row["total_words"] for row in chapters.values()) == result["total_words"]
    assert sum(row["total"] for row in speakers.values()) == result["total"]
    assert result["by_term"]["a+b"] == 1 and result["zero_hit_terms"] == ["absent"]
    assert baseline == analyze({**data, "include_group_rates": False})


def test_no_groups_and_invalid_option():
    assert analyze({"terms": ["blast"], "include_group_rates": True})["chapter_rates"] == {}
    assert (
        analyze(
            {
                "terms": ["blast"],
                "chapters": [{"passages": [{"text": "é calm"}]}],
                "include_group_rates": True,
            }
        )["speaker_rates"]["Narration"]["total_words"]
        == 2
    )
    with pytest.raises(TypeError, match="boolean"):
        analyze({"terms": ["blast"], "include_group_rates": 1})
