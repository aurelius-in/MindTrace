from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ThoughtRecordInput(BaseModel):
    text: str = Field(..., min_length=10, max_length=5000, description="User's journal entry text")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Time of entry")

    class Config:
        schema_extra = {
            "example": {
                "text": "I feel like I failed that meeting today. Everyone probably thinks I’m incompetent.",
                "timestamp": "2024-04-01T15:30:00Z"
            }
        }
