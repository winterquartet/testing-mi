from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.threat import Threat
from app.models.market_pulse import MarketPulse

class AnalysisRequest(BaseModel):
    topic: str = Field(..., description="The main market topic, competitor, or sector to analyze")
    focus_areas: List[str] = Field(default_factory=list, description="Specific focus areas (e.g., pricing, technical-stack, expansion, customer-reviews)")
    collectors: List[str] = Field(
        default_factory=lambda: ["ddgs", "news", "competitor"],
        description="List of collectors to activate for this analysis session (options: 'ddgs', 'news', 'competitor')"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "Generative AI Agent platforms",
                "focus_areas": ["pricing", "product-features"],
                "collectors": ["ddgs", "news"]
            }
        }
    )

class AnalysisResponse(BaseModel):
    request_id: str = Field(..., description="UUID or identifier for the analysis session")
    status: str = Field(..., description="Analysis operation status (e.g., completed, failed, processing)")
    signals_found: List[Signal] = Field(default_factory=list, description="List of signals detected during the analysis")
    opportunities_found: List[Opportunity] = Field(default_factory=list, description="List of opportunities synthesized")
    threats_found: List[Threat] = Field(default_factory=list, description="List of threats synthesized")
    pulse: Optional[MarketPulse] = Field(None, description="Integrated Market Pulse from the findings")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "request_id": "req_84f931d2",
                "status": "completed",
                "signals_found": [],
                "opportunities_found": [],
                "threats_found": [],
                "pulse": None
            }
        }
    )

class CollectionRequest(BaseModel):
    query: str = Field(..., description="Search query or target entity to collect data for")
    sources: List[str] = Field(default_factory=lambda: ["ddgs", "news", "competitor"], description="Specific sources to collect from")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "Competitor X pricing tier change",
                "sources": ["news", "ddgs"]
            }
        }
    )
