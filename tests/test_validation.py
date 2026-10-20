from copy import deepcopy

import pytest

from profanity_distribution_report.core import analyze


@pytest.mark.parametrize("terms", [None, [], "blast", [""], [" "], [None], [3]])
def test_invalid_term_catalog(terms):
    with pytest.raises((ValueError, TypeError), match="terms"):
        analyze({"terms": terms})


@pytest.mark.parametrize(
    "chapters",
    [
        None,
        {},
        "text",
        [None],
        [{"title": 2}],
        [{"passages": {}}],
        [{"passages": [None]}],
        [{"passages": [{"text": 3}]}],
        [{"passages": [{"speaker": False}]}],
    ],
)
def test_invalid_chapter_and_passage_shapes(chapters):
    with pytest.raises((ValueError, TypeError)):
        analyze({"terms": ["blast"], "chapters": chapters})


def test_unicode_literals_are_not_rewritten_before_matching():
    data = {
        "terms": ["Straße", "İ", "a+b"],
        "chapters": [{"passages": [{"text": "Straße STRASSE İ a+b xa+by"}]}],
    }
    original = deepcopy(data)
    report = analyze(data)
    assert report["by_term"] == {"strasse": 1, "i\u0307": 1, "a+b": 1}
    assert report["zero_hit_terms"] == []
    assert data == original
    with pytest.raises((ValueError, TypeError), match="unique"):
        analyze({"terms": ["Straße", "STRASSE"]})


def test_empty_text_defaults_and_punctuation_rates():
    report = analyze(
        {
            "terms": ["!"],
            "chapters": [{"passages": [{}]}, {"passages": [{"text": "!", "speaker": ""}]}],
            "include_group_rates": True,
        }
    )
    assert report["total_words"] == 0 and report["total"] == 1
    assert report["per_1000_words"] == {"!": 0}
    assert report["chapter_rates"]["Untitled"]["total"] == 1
