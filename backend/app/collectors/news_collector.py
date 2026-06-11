import hashlib
from datetime import datetime, timezone
from typing import List
from app.models.evidence import Evidence

class NewsCollector:
    """
    News Collector.
    Responsible for fetching news articles, blogs, and press releases and extracting relevant evidence.
    """

    async def collect(self, query: str) -> List[Evidence]:
        """
        Collect news reports and press releases matching the specified search query.
        Returns structured Evidence.
        """
        # In full production, this integrates with news aggregator APIs (e.g., NewsAPI, GNews).
        # We supply a clean, robust schema-compliant mock return.
        results = [
            {
                "source": "https://industrynewsfeed.com/articles/market-update",
                "content": f"Press release regarding '{query}': Industry analysts report a 15% increase in adoption rates for related technologies.",
                "confidence": 0.85,
                "metadata": {"collector": "NewsCollector", "category": "press_release"}
            },
            {
                "source": "https://globaltechnews.net/breaking",
                "content": f"Global Tech News breaking article: Standardizations and regulatory frameworks are being established for '{query}'.",
                "confidence": 0.9,
                "metadata": {"collector": "NewsCollector", "category": "breaking_news"}
            }
        ]

        evidences = []
        for i, res in enumerate(results):
            content_bytes = res["content"].encode("utf-8")
            hash_id = hashlib.sha256(content_bytes).hexdigest()[:10]
            evidence_id = f"ev_news_{hash_id}_{i}"

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
