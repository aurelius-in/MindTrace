import pytest
from backend.chains import cbt_agent


def test_process_journal_entry_returns_response():
    entry = "I messed up at work today and now I feel like a total failure."
    result = cbt_agent.process_journal_entry(entry)
    
    assert isinstance(result, str)
    assert len(result) > 20  # Ensure something substantial came back

    # Look for CBT-related keywords (rough heuristic check)
    keywords = ["emotion", "distortion", "reframe", "encouragement"]
    assert any(word in result.lower() for word in keywords)


def test_empty_journal_entry_raises_error():
    with pytest.raises(ValueError):
        cbt_agent.process_journal_entry("")
