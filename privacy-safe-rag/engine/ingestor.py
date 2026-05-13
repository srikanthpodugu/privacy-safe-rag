from collections import defaultdict

from engine.domain_classifier import SemanticDomainClassifier
from engine.context.context_detector import ContextualSensitivityDetector

from engine.extractors.pdf_extractor import extract_pdf_text
from engine.extractors.docx_extractor import extract_docx_text

from engine.scrubbers.pii_scrubber import PIIScrubber
from engine.fusion.pii_fusion_engine import PIIFusionEngine

from engine.governance.policy_engine import GovernanceEngine
from engine.audit.audit_logger import AuditLogger

from presidio_analyzer import AnalyzerEngine


class PrivacyIngestor:

    def __init__(self):

        self.domain_classifier = SemanticDomainClassifier()
        self.context_detector = ContextualSensitivityDetector()

        self.analyzer = AnalyzerEngine()

        self.fusion_engine = PIIFusionEngine()

        self.scrubber = PIIScrubber(
            analyzer=self.analyzer,
            fusion_engine=self.fusion_engine
        )

        self.governance_engine = GovernanceEngine()
        self.audit_logger = AuditLogger()

    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================
    def process_file(self, content, filename):

        filename = filename.lower()

        # 1. EXTRACT TEXT
        if filename.endswith(".pdf"):
            text = extract_pdf_text(content)

        elif filename.endswith(".docx"):
            text = extract_docx_text(content)

        else:
            try:
                text = content.decode("utf-8", errors="ignore")
            except:
                text = str(content)

        # 2. DOMAIN
        domain = self.domain_classifier.classify(text)

        # 3. CONTEXT
        contextual_findings = self.context_detector.detect(text)

        # 4. SCRUBBING (NOW USING FUSION ENGINE)
        scrub_result = self.scrubber.scrub(text=text, domain=domain)

        scrubbed_text = scrub_result["scrubbed_text"]
        entities = scrub_result["entities"]

        # 5. ENTITY BREAKDOWN
        pii_entities = defaultdict(int)
        for e in entities:
            pii_entities[e["entity_type"]] += 1

        pii_entities = dict(pii_entities)

        # 6. RISK ENGINE (existing)
        risk_score = len(entities) * 10 + len(contextual_findings) * 15

        if domain == "healthcare":
            risk_score *= 1.5

        if domain == "finance":
            risk_score *= 1.3

        risk_level = (
            "CRITICAL" if risk_score > 100 else
            "HIGH" if risk_score > 60 else
            "MEDIUM" if risk_score > 30 else
            "LOW"
        )

        risk_output = {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level
        }

        # 7. GOVERNANCE
        governance = self.governance_engine.evaluate(
            risk_level=risk_level,
            domain=domain
        )

        # 8. AUDIT
        self.audit_logger.log_event(
            filename=filename,
            domain=domain,
            risk_score=risk_score,
            risk_level=risk_level,
            governance_action=governance["action"],
            entity_breakdown=pii_entities
        )

        # 9. RESPONSE
        return {
            "filename": filename,
            "contextual_findings": contextual_findings,
            "domain": domain,
            "status": "processed",
            "entity_breakdown": pii_entities,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "governance": governance,
            "output": scrubbed_text
        }