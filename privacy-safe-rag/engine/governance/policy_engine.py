class GovernanceEngine:

    def __init__(self):

        # ======================================================
        # GOVERNANCE POLICIES
        # ======================================================
        self.policies = {

            "LOW": {

                "allow_external_llm": True,

                "allow_local_llm": True,

                "requires_human_approval": False,

                "action": "ALLOW"
            },

            "MEDIUM": {

                "allow_external_llm": True,

                "allow_local_llm": True,

                "requires_human_approval": False,

                "action": "TOKENIZE_AND_ALLOW"
            },

            "HIGH": {

                "allow_external_llm": False,

                "allow_local_llm": True,

                "requires_human_approval": True,

                "action": "LOCAL_LLM_ONLY"
            },

            "CRITICAL": {

                "allow_external_llm": False,

                "allow_local_llm": True,

                "requires_human_approval": True,

                "action": "BLOCK_EXTERNAL"
            }
        }

    # ==========================================================
    # APPLY POLICY
    # ==========================================================
    def evaluate(self, risk_level, domain):

        decision = self.policies.get(risk_level)

        # ======================================================
        # DOMAIN OVERRIDES
        # ======================================================
        if domain == "healthcare":

            decision["allow_external_llm"] = False

            if risk_level in ["HIGH", "CRITICAL"]:

                decision["action"] = "HIPAA_RESTRICTED"

        return decision
