from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import settings

# Initialize the LLM (use GPT-4o for quality + speed)
llm = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.5,
    openai_api_key=settings.openai_api_key,
    request_timeout=20
)

# Schema therapy prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are an AI trained in schema therapy. Given the journal entry below, analyze and return:

1. The most likely maladaptive schemas (e.g., abandonment, mistrust, failure, emotional deprivation).
2. How these schemas may have formed, based on the language used.
3. Suggestions for how the user could begin to challenge or reframe these beliefs.

Journal entry:
"{journal_entry}"
""")

def generate_schema_reflection(journal_entry: str) -> str:
    """
    Analyzes a journal entry for possible maladaptive schemas and offers insight.
    """
    prompt = prompt_template.format_messages(journal_entry=journal_entry)
    response = llm(prompt)
    return response.content
