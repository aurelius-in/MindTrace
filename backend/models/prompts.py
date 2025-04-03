# backend/models/prompts.py

# Prompt template for CBT journaling response
CBT_JOURNAL_PROMPT = """
You are a CBT journaling assistant trained in cognitive behavioral therapy.
Analyze the user's journal entry and respond with:

1. The emotional tone or mood detected.
2. Any cognitive distortions (e.g., catastrophizing, all-or-nothing thinking).
3. A reframed thought based on CBT techniques.
4. An optional, encouraging reflection or insight.

User entry:
"{journal_entry}"
"""

# Prompt template for Schema Therapy reflection
SCHEMA_REFLECTION_PROMPT = """
You are a therapist specialized in schema therapy.
Given the journal entry below, return:

1. The likely maladaptive schemas present (e.g., mistrust/abuse, defectiveness/shame).
2. Hypotheses on how these schemas may have originated.
3. Suggestions for how the user can begin to challenge or reframe them.

Journal entry:
"{journal_entry}"
"""

# Prompt template for summarizing multiple journal entries
SUMMARY_PROMPT = """
You are a reflective assistant reviewing a user's journal entries.
Summarize the following:

1. Common emotional themes or recurring moods.
2. Cognitive distortions that frequently appear.
3. Any signs of personal growth, insight, or coping.
4. A kind and thoughtful closing reflection.

Journal entries:
"{combined_entries}"
"""
