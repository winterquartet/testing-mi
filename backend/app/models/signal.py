from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.evidence import Evidence

class Signal(BaseModel):
    id: str = Field(..., description="Unique identifier for the signal")
    title: str = Field(..., description="Short descriptive title of the market signal")
    description: str = Field(..., description="Detailed explanation of the signal and its implications")
    category: str = Field(..., description="Thematic category of the signal (e.g., product, pricing, expansion, regulatory)")
    strength: float = Field(..., ge=0.0, le=1.0, description="Overall strength or importance of the signal")
    evidences: List[Evidence] = Field(default_factory=list, description="List of supporting evidence items")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when the signal was detected or synthesized")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata related to the signal")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "sig_f930128a",
                "title": "Competitor Expansion into Enterprise AI Analytics",
                "description": "Competitor X has launched a new AI analytics dashboard and is targeting enterprise clients based on multiple news announcements.",
                "category": "product_update",
                "strength": 0.9,
                "evidences": [
                    {
                        "id": "ev_83f9a1b2",
                        "source": "DuckDuckGo Search",
                        "content": "Competitor X launched a new generative AI analytics dashboard for enterprise users.",
                        "confidence": 0.85,
                        "timestamp": "2026-06-11T22:28:48Z",
                        "metadata": {"query": "Competitor X product updates"}
                    }
                ],
                "timestamp": "2026-06-11T22:30:00Z",
                "metadata": {"detected_by": "signals_detector"}
            }
        }
    )

