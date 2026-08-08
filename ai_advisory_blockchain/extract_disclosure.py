# Disclosure Extraction - Paytm Money
# MOCK_LLM=1 mode (default, graded baseline)

import os
import re
from disclosure_snippets import DISCLOSURE_SNIPPETS

MOCK_LLM = os.environ.get("MOCK_LLM", "1") == "1"

def extract_signals(snippet: str) -> dict:
    text = snippet.lower()
    
    # Risk flags detection
    risk_flags = []
    if "litigation" in text:
        risk_flags.append("litigation_risk")
    if "regulatory" in text or "regulator" in text:
        risk_flags.append("regulatory_risk")
    if "42 percent" in text or "customer" in text and "revenue" in text:
        risk_flags.append("customer_concentration_risk")
    
    # Hedging detection
    hedging_phrases = ["assuming", "cautiously", "visibility", "limited", "uncertainty"]
    hedging_detected = any(phrase in text for phrase in hedging_phrases)
    
    # Sentiment classification
    if any(word in text for word in ["confident", "approved", "expanded"]):
        sentiment = "confident"
    elif hedging_detected:
        sentiment = "cautious"
    else:
        sentiment = "neutral"
    
    return {
        "risk_flags": risk_flags,
        "hedging_detected": hedging_detected,
        "sentiment": sentiment
    }

if __name__ == "__main__":
    print("=" * 60)
    print("DISCLOSURE SIGNAL EXTRACTION (MOCK MODE)")
    print("=" * 60)
    
    for snippet in DISCLOSURE_SNIPPETS:
        doc_id = snippet[:6]
        result = extract_signals(snippet)
        print(f"\n{doc_id}")
        print(f"  Risk Flags: {result['risk_flags']}")
        print(f"  Hedging: {result['hedging_detected']}")
        print(f"  Sentiment: {result['sentiment']}")
