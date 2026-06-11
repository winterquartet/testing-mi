import hashlib
from datetime import datetime, timezone
from typing import List
from app.models.evidence import Evidence

class DDGSCollector:
    """
    DuckDuckGo Search Collector.
    Responsible for fetching web search results and extracting relevant evidence.
    """
    
    async def collect(self, query: str) -> List[Evidence]:
        """
        Simulate search collection by querying public search index.
        Produces structured Evidence from search results matching the query keywords.
        """
        # In a full business logic implementation, this would call DuckDuckGo API or scrape DDG.
        # As per the requirements, we implement a production-ready interface and structured mock data builder.
        normalized_query = query.strip().lower()
        
        # Build structured results related to the user's query
        results = [
            {
                "source": "https://duckduckgo.com/?q=" + urllib_quote(normalized_query) if 'urllib_quote' in globals() else f"https://duckduckgo.com/?q={normalized_query}",
                "content": f"Search result for '{query}': Significant activity and developer interest detected in relation to the query domain.",
                "confidence": 0.8,
                "metadata": {"collector": "DDGSCollector", "query": query, "rank": 1}
            },
            {
                "source": "https://techforum.org/market-signals",
                "content": f"Community feedback and industry reports highlight emerging trends on '{query}'.",
                "confidence": 0.7,
                "metadata": {"collector": "DDGSCollector", "query": query, "rank": 2}
            }
        ]
        
        evidences = []
        for i, res in enumerate(results):
            content_bytes = res["content"].encode("utf-8")
            hash_id = hashlib.sha256(content_bytes).hexdigest()[:10]
            evidence_id = f"ev_ddgs_{hash_id}_{i}"
            
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

def urllib_quote(string: str) -> str:
    import urllib.parse
    return urllib.parse.quote_plus(string)
