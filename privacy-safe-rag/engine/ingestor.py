from engine.domain_classifier import SemanticDomainClassifier

from engine.extractors.pdf_extractor import extract_pdf_text
from engine.extractors.docx_extractor import extract_docx_text

from engine.scrubbers.pii_scrubber import PIIScrubber


class PrivacyIngestor:

    def __init__(self):

        self.domain_classifier = SemanticDomainClassifier()
        self.scrubber = PIIScrubber()

    # ==========================================================
    # MAIN PIPELINE
    # ==========================================================
    def process_file(self, content, filename):

        filename = filename.lower()

        # ----------------------------
        # Extract text
        # ----------------------------
        if filename.endswith(".pdf"):
            text = extract_pdf_text(content)

        elif filename.endswith(".docx"):
            text = extract_docx_text(content)

        else:
            try:
                text = content.decode("utf-8", errors="ignore")
            except:
                text = str(content)

        # ----------------------------
        # Semantic domain detection
        # ----------------------------
        domain = self.domain_classifier.classify(text)

        # ----------------------------
        # PII scrubbing + tokenization
        # ----------------------------
        scrubbed_text = self.scrubber.scrub(
            text=text,
            domain=domain
        )

        # ----------------------------
        # Response
        # ----------------------------
        return {
            "filename": filename,
            "domain": domain,
            "status": "processed",
            "output": scrubbed_text
        }