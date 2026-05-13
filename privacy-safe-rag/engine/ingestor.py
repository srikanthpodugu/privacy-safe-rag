from collections import defaultdict

from engine.domain_classifier import SemanticDomainClassifier
from engine.context.context_detector import ContextualSensitivityDetector

from engine.extractors.pdf_extractor import extract_pdf_text
from engine.extractors.docx_extractor import extract_docx_text

from engine.scrubbers.pii_scrubber import PIIScrubber

from engine.risk.aggregation_engine import RiskAggregationEngine

from engine.governance.policy_engine import GovernanceEngine
from engine.audit.audit_logger import AuditLogger


class PrivacyIngestor:

    def __init__(self):

        self.domain_classifier = SemanticDomainClassifier()
        self.context_detector = ContextualSensitivityDetector()

        # IMPORTANT: analyzer is injected into scrubber
        self.scrubber = PIIScrubber(
            analyzer=self._get_analyzer()
        )

        self.risk_engine = RiskAggregationEngine()

        self.governance_engine = GovernanceEngine()
        self.audit_logger = AuditLogger()

    # ==========================================================
    # PRESIDIO ANALYZER ACCESS (centralized)
    # ==========================================================
    def _get_analyzer(self):
        from presidio_analyzer import AnalyzerEngine
        return AnalyzerEngine()

    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================
    def process_file(self, content, filename):

        filename = filename.lower()

        # --------------------------
        # 1. EXTRACT TEXT
        # --------------------------
        if filename.endswith(".pdf"):
            text = extract_pdf_text(content)

        elif filename.endswith(".docx"):
            text = extract_docx_text(content)

        else:
            text = content.decode("utf-8", errors="ignore")

        # --------------------------
        # 2. DOMAIN DETECTION
        # --------------------------
        domain = self.domain_classifier.classify(text)

        # --------------------------
        # 3. CONTEXT DETECTION
        # --------------------------
        contextual_findings = self.context_detector.detect(text)

        # --------------------------
        # 4. SCRUB + TOKENIZE (single pass)
        # --------------------------
        scrub_result = self.scrubber.scrub(
            text=text,
            domain=domain
        )

        scrubbed_text = scrub_result["scrubbed_text"]
        entity_breakdown = scrub_result["entity_breakdown"]

        # --------------------------
        # 5. RISK SCORING
        # --------------------------
        risk_result = self.risk_engine.compute_risk(
            pii_entities=entity_breakdown,
            contextual_findings=contextual_findings,
            domain=domain,
            scrubbed_text=scrubbed_text
        )

        # --------------------------
        # 6. GOVERNANCE
        # --------------------------
        governance = self.governance_engine.evaluate(
            risk_level=risk_result["risk_level"],
            domain=domain
        )

        # --------------------------
        # 7. AUDIT LOGGING
        # --------------------------
        self.audit_logger.log_event(
            filename=filename,
            domain=domain,
            risk_score=risk_result["risk_score"],
            risk_level=risk_result["risk_level"],
            governance_action=governance["action"],
            entity_breakdown=entity_breakdown
        )

        # --------------------------
        # 8. RESPONSE
        # --------------------------
        return {
            "filename": filename,
            "domain": domain,
            "status": "processed",

            "contextual_findings": contextual_findings,

            "entity_breakdown": entity_breakdown,

            "risk_score": risk_result["risk_score"],
            "risk_level": risk_result["risk_level"],

            "governance": governance,

            "output": scrubbed_text
        }