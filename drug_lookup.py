"""
Utility for the UI layer.
Given a brand name OR chemical name entered by the user,
returns the canonical chemical name and drug info.

Usage:
    from drug_lookup import lookup
    result = lookup("prozac")
    # {"chemical": "fluoxetine", "class": "SSRI", "brands": ["prozac", "sarafem"]}
"""

from config import BRAND_TO_CHEMICAL, DRUG_DATABASE


def lookup(user_input: str) -> dict | None:
    """
    Returns drug info dict for a given brand or chemical name.
    Returns None if not found.
    """
    key = user_input.strip().lower()
    chemical = BRAND_TO_CHEMICAL.get(key)
    if not chemical:
        return None
    info = DRUG_DATABASE[chemical]
    return {
        "chemical":  chemical,
        "class":     info["class"],
        "brands":    info["brands"],
    }


def lookup_or_suggest(user_input: str) -> dict:
    """
    Like lookup(), but if not found returns close matches
    using simple substring matching.
    """
    result = lookup(user_input)
    if result:
        return {"found": True, "data": result}

    # Fuzzy fallback — find anything containing the input
    key = user_input.strip().lower()
    suggestions = []
    for chemical, info in DRUG_DATABASE.items():
        if key in chemical:
            suggestions.append(chemical)
        for brand in info["brands"]:
            if key in brand:
                suggestions.append(chemical)

    return {"found": False, "suggestions": list(set(suggestions))}


if __name__ == "__main__":
    # Quick test
    tests = ["prozac", "Zoloft", "LEXAPRO", "adderall", "unknowndrug"]
    for t in tests:
        print(f"{t:15} -> {lookup_or_suggest(t)}")