from collections import defaultdict


class RiskAggregationEngine:

    def __init__(self):

        # Base weights (tunable later)
        self.weights = {
            "pii_entity": 2.0,
            "contextual_signal": 3.0,
            "domain_multiplier": {
                "healthcare": 1.5,
                "finance": 1.4,
                "hr": 1.2,
                "general": 1.0
            }
        }

    # ==========================================================
    # MAIN SCORING FUNCTION
    # ==========================================================
    def compute_risk(
        self,
        pii_entities: dict,
        contextual_findings: list,
        domain: str,
        scrubbed_text: str
    ):

        # --------------------------
        # 1. PII SCORE
        # --------------------------
        pii_score = 0

        for entity, count in pii_entities.items():
            pii_score += count * self.weights["pii_entity"]

        # --------------------------
        # 2. CONTEXT SCORE
        # --------------------------
        context_score = 0

        for c in contextual_findings:
            context_score += c.get("confidence", 0) * self.weights["contextual_signal"]

        # --------------------------
        # 3. ENTITY DENSITY SCORE
        # --------------------------
        words = len(scrubbed_text.split())
        entity_count = sum(pii_entities.values())

        density_score = (entity_count / words) * 100 if words > 0 else 0

        # --------------------------
        # 4. DOMAIN MULTIPLIER
        # --------------------------
        multiplier = self.weights["domain_multiplier"].get(domain, 1.0)

        # --------------------------
        # FINAL SCORE
        # --------------------------
        raw_score = (
            pii_score +
            context_score +
            density_score
        )

        final_score = raw_score * multiplier

        # --------------------------
        # RISK LEVEL
        # --------------------------
        if final_score >= 150:
            level = "CRITICAL"
        elif final_score >= 80:
            level = "HIGH"
        elif final_score >= 30:
            level = "MEDIUM"
        else:
            level = "LOW"

        # --------------------------
        # GOVERNANCE DECISION
        # --------------------------
        if level == "CRITICAL":
            action = "HIPAA_RESTRICTED"
        elif level == "HIGH":
            action = "HUMAN_REVIEW"
        elif level == "MEDIUM":
            action = "TOKENIZE_AND_ALLOW"
        else:
            action = "ALLOW"

        return {
            "risk_score": round(final_score, 2),
            "risk_level": level,
            "governance": {
                "allow_external_llm": level in ["LOW"],
                "allow_local_llm": level in ["LOW", "MEDIUM"],
                "requires_human_approval": level in ["HIGH", "CRITICAL"],
                "action": action
            }
        }
