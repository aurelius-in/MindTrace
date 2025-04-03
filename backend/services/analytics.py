from collections import Counter
from datetime import datetime
from typing import List, Dict
import re


def extract_emotions(journals: List[str]) -> Dict[str, int]:
    """
    Naively extract and count emotional words from a list of journal entries.
    Can be swapped out later for more advanced NLP/emotion models.
    """
    # Basic emotion lexicon (expand as needed)
    emotion_keywords = {
        "anger", "anxiety", "sadness", "fear", "joy", "shame", "guilt", "hope", "frustration", "loneliness", "stress"
    }
    word_freq = Counter()

    for entry in journals:
        words = re.findall(r'\b\w+\b', entry.lower())
        for word in words:
            if word in emotion_keywords:
                word_freq[word] += 1

    return dict(word_freq)


def detect_distortions(journals: List[str]) -> Dict[str, int]:
    """
    Detect and count mentions of common cognitive distortions using keyword matching.
    """
    distortions = {
        "catastrophizing", "mind reading", "overgeneralization",
        "black-and-white", "should statements", "personalization",
        "labeling", "emotional reasoning", "filtering"
    }

    pattern = re.compile("|".join([re.escape(d) for d in distortions]), re.IGNORECASE)
    freq = Counter()

    for entry in journals:
        matches = pattern.findall(entry)
        for match in matches:
            freq[match.lower()] += 1

    return dict(freq)


def track_journal_frequency(timestamps: List[datetime]) -> Dict[str, int]:
    """
    Returns a breakdown of journal entry frequency by day of week.
    """
    freq = Counter()
    for ts in timestamps:
        day = ts.strftime("%A")
        freq[day] += 1
    return dict(freq)


def summarize_progress(journals: List[str]) -> Dict[str, str]:
    """
    Placeholder: Analyze for signs of progress based on patterns like 'I realized', 'I'm trying', 'I coped'.
    Could be replaced with LLM-based scoring later.
    """
    progress_signals = ["i noticed", "i realized", "i coped", "i managed", "i was able", "i chose", "i practiced"]
    count = sum(1 for j in journals for signal in progress_signals if signal in j.lower())
    return {
        "growth_signals_detected": str(count),
        "interpretation": (
            "Positive self-reflection and coping strategies appear "
            "frequently, suggesting growth and emotional insight."
            if count > 5 else "Limited signs of self-directed reflection were found."
        )
    }
