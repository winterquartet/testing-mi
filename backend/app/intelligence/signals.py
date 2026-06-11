import hashlib
from datetime import datetime, timezone
from typing import List
from app.models.evidence import Evidence
from app.models.signal import Signal

class SignalDetector:
    """
    Signal Detector.
    Responsible for clustering and synthesizing raw Evidence into meaningful market Signals.
    """

    async def detect_signals(self, evidences: List[Evidence]) -> List[Signal]:
        """
        Processes a list of raw Evidence items and groups/synthesizes them into Signals.
        """
        # In full production, this would employ advanced text classification, deduplication, 
        # or NLP clustering. As per requirements, we implement a robust clean structure 
        # that aggregates evidence by general categorization inferred from source / metadata.
        if not evidences:
            return []

        # Simple semantic clustering logic: group by general domain/source
        signals = []
        
        # We group evidence based on source/content keywords to form distinct signals
        groups = {}
        for ev in evidences:
            category = ev.metadata.get("category") or ev.metadata.get("event_type") or "general"
            if category not in groups:
                groups[category] = []
            groups[category].append(ev)

        for category, ev_list in groups.items():
            # Calculate overall strength as average confidence weighted by number of evidences
            avg_confidence = sum(e.confidence for e in ev_list) / len(ev_list)
            strength = min(1.0, avg_confidence * (1.0 + 0.1 * (len(ev_list) - 1)))
            
            # Formulate title and description
            title = f"Synthesized Signal: {category.replace('_', ' ').title()} Activity"
            description = (
                f"Aggregated signal of type '{category}' detected from {len(ev_list)} "
                f"supporting evidence sources. Focus content: " + " | ".join(e.content[:60] for e in ev_list)
            )
            
            hash_content = (title + description).encode("utf-8")
            sig_id = f"sig_{hashlib.sha256(hash_content).hexdigest()[:10]}"

            signals.append(
                Signal(
                    id=sig_id,
                    title=title,
                    description=description,
                    category=category,
                    strength=round(strength, 2),
                    evidences=ev_list,
                    timestamp=datetime.now(timezone.utc),
                    metadata={"source_count": len(ev_list)}
                )
            )

        return signals
