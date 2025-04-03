from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from backend.models.journal import ThoughtRecordInput
from backend.chains.cbt_agent import generate_cbt_response
from backend.utils.redact import redact_sensitive_info

app = FastAPI(title="MindTrace: AI Cognitive Therapy Assistant")

# CORS config (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/healthz")
def health_check():
    return {"status": "ok"}

# CBT journaling endpoint
@app.post("/api/cbt")
async def handle_thought_record(record: ThoughtRecordInput):
    # Redact sensitive content (optional, can be moved earlier)
    clean_input = redact_sensitive_info(record.text)

    # Generate CBT reflection using LangChain agent
    reflection = generate_cbt_response(clean_input)

    return {
        "input": clean_input,
        "reflection": reflection,
    }
