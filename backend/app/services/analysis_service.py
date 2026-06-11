import uuid
from datetime import datetime, timezone
from typing import List, Tuple
from app.collectors.ddgs_collector import DDGSCollector
from app.collectors.news_collector import NewsCollector
from app.collectors.competitor_collector import CompetitorCollector
from app.intelligence.signals import SignalDetector
from app.intelligence.opportunities import OpportunityEvaluator
from app.models.evidence import Evidence
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.threat import Threat
from app.models.market_pulse import MarketPulse
from app.models.analysis import AnalysisRequest, AnalysisResponse

class AnalysisService:
    """
    AnalysisService orchestrates data collection, signal detection, and opportunity evaluation.
    Maintains an in-memory state of collected intelligence to simulate a clean storage layer.
    """

    def __init__(
        self,
        ddgs_collector: DDGSCollector,
        news_collector: NewsCollector,
        competitor_collector: CompetitorCollector,
        signal_detector: SignalDetector,
        opportunity_evaluator: OpportunityEvaluator
    ):
        self.ddgs_collector = ddgs_collector
        self.news_collector = news_collector
        self.competitor_collector = competitor_collector
        self.signal_detector = signal_detector
        self.opportunity_evaluator = opportunity_evaluator

        # In-memory storage for detected structures
        self._evidences: List[Evidence] = []
        self._signals: List[Signal] = []
        self._opportunities: List[Opportunity] = []
        self._threats: List[Threat] = []

    async def collect_evidence(self, query: str, active_collectors: List[str]) -> List[Evidence]:
        """
        Gathers evidence from active collectors.
        """
        all_evidence: List[Evidence] = []

        if "ddgs" in active_collectors:
            all_evidence.extend(await self.ddgs_collector.collect(query))
        if "news" in active_collectors:
            all_evidence.extend(await self.news_collector.collect(query))
        if "competitor" in active_collectors:
            all_evidence.extend(await self.competitor_collector.collect(query))

        # Append to our internal database state
        self._evidences.extend(all_evidence)
        return all_evidence

    async def analyze_topic(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Runs full analysis flow: Collects evidence -> Detects signals -> Identifies opportunities & threats -> Computes Market Pulse.
        """
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        # 1. Collect
        evidences = await self.collect_evidence(request.topic, request.collectors)

        # 2. Detect Signals
        new_signals = await self.signal_detector.detect_signals(evidences)
        self._signals.extend(new_signals)

        # 3. Evaluate Opportunities and Threats
        new_opps, new_threats = await self.opportunity_evaluator.evaluate_opportunities(new_signals)
        self._opportunities.extend(new_opps)
        self._threats.extend(new_threats)

        # 4. Generate Market Pulse
        pulse = await self.generate_market_pulse()

        return AnalysisResponse(
            request_id=request_id,
            status="completed",
            signals_found=new_signals,
            opportunities_found=new_opps,
            threats_found=new_threats,
            pulse=pulse
        )

    async def generate_market_pulse(self) -> MarketPulse:
        """
        Aggregates active signals, opportunities, and threats into a Market Pulse summary.
        """
        # Determine sentiment dynamically based on opportunities vs threats ratio
        opp_count = len(self._opportunities)
        threat_count = len(self._threats)
        
        if opp_count == 0 and threat_count == 0:
            sentiment = "Neutral"
        elif opp_count > threat_count * 1.5:
            sentiment = "Bullish"
        elif threat_count > opp_count * 1.5:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral-to-Bullish" if opp_count >= threat_count else "Neutral-to-Bearish"

        # Sort opportunities by value_score and threats by risk_score
        sorted_opps = sorted(self._opportunities, key=lambda x: x.value_score, reverse=True)[:5]
        sorted_threats = sorted(self._threats, key=lambda x: x.risk_score, reverse=True)[:5]

        return MarketPulse(
            timestamp=datetime.now(timezone.utc),
            market_sentiment=sentiment,
            active_signals_count=len(self._signals),
            top_opportunities=sorted_opps,
            top_threats=sorted_threats,
            metadata={
                "total_evidence_count": len(self._evidences),
                "tracked_opportunities": len(self._opportunities),
                "tracked_threats": len(self._threats)
            }
        )

    async def get_opportunities(self) -> List[Opportunity]:
        """
        Returns all detected opportunities.
        """
        return self._opportunities


# Module-level singleton instance provider for FastAPI Dependency Injection
_service_instance = None

def get_analysis_service() -> AnalysisService:
    global _service_instance
    if _service_instance is None:
        _service_instance = AnalysisService(
            ddgs_collector=DDGSCollector(),
            news_collector=NewsCollector(),
            competitor_collector=CompetitorCollector(),
            signal_detector=SignalDetector(),
            opportunity_evaluator=OpportunityEvaluator()
        )
    return _service_instance
