from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.signal import Signal

class Threat(BaseModel):
    id: str = Field(..., description="Unique identifier for the threat")
    title: str = Field(..., description="Descriptive title of the market threat")
    description: str = Field(..., description="Details about the risk and potential negative impact on the business")
    risk_score: float = Field(..., ge=0.0, le=10.0, description="Risk or severity score from 0 to 10")
    signals: List[Signal] = Field(default_factory=list, description="Supporting signals that led to identifying this threat")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when the threat was identified")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata related to the threat")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "th_a8b9c0d1",
                "title": "Loss of Enterprise Accounts to Competitor X AI Tooling",
                "description": "Enterprise clients might migrate to Competitor X due to their newly released analytics offering if we do not respond.",
                "risk_score": 7.8,
                "signals": [],
                "timestamp": "2026-06-11T22:35:00Z",
                "metadata": {"risk_level": "Major"}
            }
        }
    )

