from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.signal import Signal

class Opportunity(BaseModel):
    id: str = Field(..., description="Unique identifier for the opportunity")
    title: str = Field(..., description="Descriptive title of the market opportunity")
    description: str = Field(..., description="Details regarding the opportunity and strategic actions to capture it")
    value_score: float = Field(..., ge=0.0, le=10.0, description="Potential value or impact score from 0 to 10")
    signals: List[Signal] = Field(default_factory=list, description="Supporting signals that led to identifying this opportunity")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when the opportunity was identified")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata related to the opportunity")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "opp_38f29d1a",
                "title": "Develop Mid-Market Enterprise AI Analytics Features",
                "description": "With Competitor X focusing heavily on high-end enterprise AI analytics, there is a gap in the mid-market segment that can be target-marketed.",
                "value_score": 8.5,
                "signals": [],
                "timestamp": "2026-06-11T22:35:00Z",
                "metadata": {"strategic_priority": "High"}
            }
        }
    )

