from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict

class Evidence(BaseModel):
    id: str = Field(..., description="Unique identifier for the evidence")
    source: str = Field(..., description="Source URL or platform name where evidence was collected")
    content: str = Field(..., description="Extracted content or text snippet representing the evidence")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score of the evidence source or credibility")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when the evidence was collected")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata related to the evidence")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "ev_83f9a1b2",
                "source": "DuckDuckGo Search",
                "content": "Competitor X launched a new generative AI analytics dashboard for enterprise users.",
                "confidence": 0.85,
                "timestamp": "2026-06-11T22:28:48Z",
                "metadata": {"query": "Competitor X product updates", "relevance_score": 0.9}
            }
        }
    )

