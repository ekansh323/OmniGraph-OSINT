"""Named Entity Recognition (NER) service using spaCy (en_core_web_sm).

Extracts entities (Persons, Organizations, Locations, Monetary amounts, etc.)
and normalizes labels for the OSINT knowledge graph.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

_nlp = None

def _load_model():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy en_core_web_sm model")
        except Exception as e:
            logger.warning(f"Could not load spaCy en_core_web_sm ({e}), falling back to blank model or heuristics")
            try:
                import spacy
                _nlp = spacy.blank("en")
            except Exception:
                _nlp = None
    return _nlp


def normalize_entity_type(label: str) -> str:
    """Map standard spaCy NER labels to OSINT entity types."""
    mapping = {
        "PERSON": "Person",
        "PER": "Person",
        "ORG": "Organization",
        "GPE": "Location",
        "LOC": "Location",
        "FAC": "Location",
        "MONEY": "FinancialAccount",
        "NORP": "Group",
        "PRODUCT": "Asset",
        "EVENT": "Event",
        "DATE": "Date",
    }
    return mapping.get(label.upper(), label.title())


def extract_entities(text: str) -> List[Dict[str, Any]]:
    """Extract named entities from raw text.

    Returns a list of dictionaries:
        [{"name": "...", "type": "...", "label": "...", "confidence": 0.90, "start": int, "end": int}]
    """
    if not text or not text.strip():
        return []

    nlp = _load_model()
    if nlp is None:
        return []

    doc = nlp(text)
    entities = []
    seen = set()

    for ent in doc.ents:
        clean_name = ent.text.strip().replace("\n", " ")
        if not clean_name or len(clean_name) < 2:
            continue

        normalized_type = normalize_entity_type(ent.label_)
        key = (clean_name.lower(), normalized_type)
        if key in seen:
            continue
        seen.add(key)

        # Baseline confidence score for spaCy pipeline match
        confidence = 0.90 if ent.label_ in ("PERSON", "ORG", "GPE", "MONEY") else 0.75

        entities.append({
            "name": clean_name,
            "type": normalized_type,
            "label": ent.label_,
            "confidence": confidence,
            "start": ent.start_char,
            "end": ent.end_char,
        })

    return entities
