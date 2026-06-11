from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.opportunity import Opportunity
from app.models.threat import Threat

class MarketPulse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time when the market pulse was computed")
    market_sentiment: str = Field(..., description="Overall market sentiment assessment (e.g., Bullish, Bearish, Neutral, Volatile)")
    active_signals_count: int = Field(..., description="Total number of active signals detected in the evaluation window")
    top_opportunities: List[Opportunity] = Field(default_factory=list, description="Top opportunities identified in the market")
    top_threats: List[Threat] = Field(default_factory=list, description="Top threats identified in the market")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional high-level meta metrics or indicators")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "timestamp": "2026-06-11T22:36:00Z",
                "market_sentiment": "Neutral-to-Bullish",
                "active_signals_count": 12,
                "top_opportunities": [],
                "top_threats": [],
                "metadata": {"industry": "SaaS AI Analytics", "data_quality_index": 0.88}
            }
        }
    )

