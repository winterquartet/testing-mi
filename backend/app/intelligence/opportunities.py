import hashlib
from datetime import datetime, timezone
from typing import List, Tuple
from app.models.signal import Signal
from app.models.opportunity import Opportunity
from app.models.threat import Threat

class OpportunityEvaluator:
    """
    Opportunity Evaluator.
    Responsible for analyzing market Signals to extract strategic Opportunities and identify Threats.
    """

    async def evaluate_opportunities(self, signals: List[Signal]) -> Tuple[List[Opportunity], List[Threat]]:
        """
        Evaluate a list of Signals and synthesize potential Opportunities and Threats.
        Returns a tuple: (opportunities, threats).
        """
        # In a complete implementation, this would map signals to market gaps, capabilities, and risks.
        # We provide a clean, schema-compliant and query-reflective logic.
        opportunities: List[Opportunity] = []
        threats: List[Threat] = []

        if not signals:
            return opportunities, threats

        for sig in signals:
            # Determine if signal indicates a threat (e.g., strong competitor action) or an opportunity (e.g., market demand)
            is_competitor_action = sig.category in ["changelog_update", "pricing_change", "competitor_move"]
            
            hash_input = (sig.id + sig.title).encode("utf-8")
            hash_id = hashlib.sha256(hash_input).hexdigest()[:10]

            if is_competitor_action:
                # Competitor actions pose threats to existing customer base, but could also suggest replication opportunities
                risk_score = round(min(10.0, sig.strength * 10), 1)
                threats.append(
                    Threat(
                        id=f"th_{hash_id}",
                        title=f"Market Share Risk: {sig.title}",
                        description=f"Potential impact on market positioning. Competitor is taking active steps: {sig.description}",
                        risk_score=risk_score,
                        signals=[sig],
                        timestamp=datetime.now(timezone.utc),
                        metadata={"derived_from_signal": sig.id}
                    )
                )
                
                # Also represent as a counter-opportunity
                value_score = round(min(10.0, sig.strength * 8.5), 1)
                opportunities.append(
                    Opportunity(
                        id=f"opp_{hash_id}_counter",
                        title=f"Counter Strategy: Build competitive feature for {sig.title}",
                        description=f"Opportunity to retain customers by matching or exceeding competitor's offering in: {sig.description}",
                        value_score=value_score,
                        signals=[sig],
                        timestamp=datetime.now(timezone.utc),
                        metadata={"derived_from_signal": sig.id, "type": "counter_move"}
                    )
                )
            else:
                # General market/news updates usually present product enhancement opportunities
                value_score = round(min(10.0, sig.strength * 9.0), 1)
                opportunities.append(
                    Opportunity(
                        id=f"opp_{hash_id}",
                        title=f"Leverage Trend: {sig.title}",
                        description=f"Strategic opportunity identified to build/integrate capabilities related to: {sig.description}",
                        value_score=value_score,
                        signals=[sig],
                        timestamp=datetime.now(timezone.utc),
                        metadata={"derived_from_signal": sig.id}
                    )
                )

        return opportunities, threats
