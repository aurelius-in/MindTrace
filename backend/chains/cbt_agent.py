from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings


# Initialize LLM (you can switch to gpt-3.5-turbo for faster response)
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.6,
    openai_api_key=settings.openai_api_key,
    request_timeout=15,
)


# Define reusable prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are a CBT journaling assistant trained in cognitive behavioral therapy and schema therapy.
Analyze the user's journal entry and respond with:

1. Identified emotional tone or mood.
2. Possible cognitive distortions (e.g., catastrophizing, black-and-white thinking).
3. A reframed thought based on cognitive restructuring.
4. Optional reflection or supportive note.

User journal entry:
"{journal_entry}"
""")


def generate_cbt_response(journal_entry: str) -> str:
    """
    Generates a structured CBT-style reflection based on the user's journal entry.
    """
    prompt = prompt_template.format_messages(journal_entry=journal_entry)
    response = llm(prompt)
    return response.content
