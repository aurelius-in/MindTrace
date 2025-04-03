# MindTrace
MindTrace helps users reflect on emotions, reframe thoughts, and track mental patterns using LLMs, vector memory, and secure journaling—all through a clean FastAPI interface.

https://aurelius-in.github.io/MindTrace/frontend
```
MindTrace/
│
├── .gitignore
├── README.md
├── requirements.txt
├── render.yaml                    # Render deployment config
├── Dockerfile                     # Optional if using custom build
├── .env.example                   # Example env vars (for devs)
│
├── app/                           # App entry point + routing
│   ├── main.py                    # Streamlit or FastAPI app launcher
│   └── config.py                  # Settings, env loading, constants
│
├── backend/                       # All AI / processing logic
│   ├── chains/
│   │   ├── cbt_agent.py           # LangChain agent for guided sessions
│   │   └── schema_reflection.py  # RAG schema therapy module
│   │
│   ├── utils/
│   │   ├── redact.py              # Regex/Pydantic redaction logic
│   │   ├── embedding.py           # FAISS vector DB helper functions
│   │   └── summarizer.py          # Session summarizer
│   │
│   ├── models/
│   │   ├── journal.py             # Pydantic schemas for thought records
│   │   └── prompts.py             # Prompt templates and formatters
│   │
│   └── services/
│       ├── langchain_client.py    # Wrapper for LLM, RAG, memory
│       ├── db.py                  # FAISS/ChromaDB handling
│       └── analytics.py           # Trends and progress evaluation
│
├── frontend/                      # Optional (if using HTMX or minimal UI)
│   ├── templates/
│   │   └── index.html             # Journaling form
│   └── static/
│       ├── css/
│       └── js/
│
└── tests/                         # Unit + integration tests
    ├── test_redaction.py
    ├── test_prompt_logic.py
    └── test_cbt_workflow.py
```
