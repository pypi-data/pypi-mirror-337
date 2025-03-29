"""Test loading intents for available languages."""

import pytest

from home_assistant_intents import get_intents, get_languages, get_language_scores


@pytest.mark.parametrize("language", get_languages())
def test_load_intents(language: str) -> None:
    """Test that we can load intents for every supported language."""
    lang_intents = get_intents(language)
    assert lang_intents


# TODO
# def test_language_scores() -> None:
#     """Test that all supported languages are in language scores."""
#     scores = get_language_scores()
#     lang_families = {lang.split("-", maxsplit=1)[0] for lang in scores}

#     for lang in get_languages():
#         assert (lang in scores) or (lang in lang_families)
