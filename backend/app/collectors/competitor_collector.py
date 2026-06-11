import hashlib
from datetime import datetime, timezone
from typing import List
from app.models.evidence import Evidence

class CompetitorCollector:
    """
    Competitor Collector.
    Responsible for scanning competitor landing pages, changelogs, and pricing structures.
    """

    async def collect(self, competitor_query: str) -> List[Evidence]:
        """
        Collect updates, changelogs, or pricing changes related to the target competitor or query.
        Returns structured Evidence.
        """
        # In full production, this would crawl/scrape competitor websites, Github updates, or changelogs.
        # We provide a clean, schema-compliant mock return.
        results = [
            {
                "source": f"https://{competitor_query.replace(' ', '').lower()}.com/changelog",
                "content": f"Competitor update detected: Substantial changes to the pricing tiers and core feature set observed for '{competitor_query}'.",
                "confidence": 0.95,
                "metadata": {"collector": "CompetitorCollector", "target": competitor_query, "event_type": "changelog_update"}
            },
            {
                "source": f"https://{competitor_query.replace(' ', '').lower()}.com/pricing",
                "content": f"Competitor pricing adjustment: Introduction of pay-as-you-go credit-based billing for services relating to '{competitor_query}'.",
                "confidence": 0.9,
                "metadata": {"collector": "CompetitorCollector", "target": competitor_query, "event_type": "pricing_change"}
            }
        ]

        evidences = []
        for i, res in enumerate(results):
            content_bytes = res["content"].encode("utf-8")
            hash_id = hashlib.sha256(content_bytes).hexdigest()[:10]
            evidence_id = f"ev_comp_{hash_id}_{i}"

            evidences.append(
                Evidence(
                    id=evidence_id,
                    source=res["source"],
                    content=res["content"],
                    confidence=res["confidence"],
                    timestamp=datetime.now(timezone.utc),
                    metadata=res["metadata"]
                )
            )

        return evidences
