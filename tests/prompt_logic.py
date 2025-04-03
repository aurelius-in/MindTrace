import pytest
from backend.models import prompts


def test_cbt_prompt_structure():
    assert "{journal_entry}" in prompts.CBT_JOURNAL_PROMPT
    assert "emotional tone" in prompts.CBT_JOURNAL_PROMPT.lower()
    assert "cognitive distortions" in prompts.CBT_JOURNAL_PROMPT.lower()


def test_schema_prompt_structure():
    assert "{journal_entry}" in prompts.SCHEMA_REFLECTION_PROMPT
    assert "maladaptive schemas" in prompts.SCHEMA_REFLECTION_PROMPT.lower()
    assert "reframe" in prompts.SCHEMA_REFLECTION_PROMPT.lower()


def test_summary_prompt_structure():
    assert "{combined_entries}" in prompts.SUMMARY_PROMPT
    assert "themes" in prompts.SUMMARY_PROMPT.lower()
    assert "progress" in prompts.SUMMARY_PROMPT.lower()
    assert "closing reflection" in prompts.SUMMARY_PROMPT.lower()


def test_prompt_rendering_does_not_crash():
    # Make sure formatting doesn't raise exceptions
    formatted = prompts.CBT_JOURNAL_PROMPT.format(journal_entry="I feel overwhelmed.")
    assert "I feel overwhelmed." in formatted

    formatted = prompts.SCHEMA_REFLECTION_PROMPT.format(journal_entry="I always get rejected.")
    assert "I always get rejected." in formatted

    formatted = prompts.SUMMARY_PROMPT.format(combined_entries="Entry 1\nEntry 2")
    assert "Entry 1" in formatted
    assert "Entry 2" in formatted
