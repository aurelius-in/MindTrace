from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings

# Initialize LLM
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.4,
    openai_api_key=settings.openai_api_key,
    request_timeout=20
)

# Prompt to summarize journal entries
summary_prompt_template = ChatPromptTemplate.from_template("""
You are a therapeutic assistant that summarizes a user's journaling history.
Given the journal entries below, return:

1. Key emotional patterns or recurring moods.
2. Common thought distortions or themes.
3. Notable signs of progress, self-awareness, or breakthroughs.
4. A supportive, encouraging closing reflection.

Journal entries:
"{combined_entries}"
""")


def summarize_journal_entries(entry_texts: list[str]) -> str:
    """
    Combines multiple journal entries and generates a reflective summary.
    """
    combined = "\n\n---\n\n".join(entry_texts)
    prompt = summary_prompt_template.format_messages(combined_entries=combined)
    response = llm(prompt)
    return response.content
