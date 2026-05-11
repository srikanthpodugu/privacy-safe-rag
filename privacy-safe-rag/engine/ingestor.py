import pypdf
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PrivacyIngestor:
    def __init__(self):
        # The AI brain which identifies sensitive info
        self.analyzer = AnalyzerEngine()
        # The tool which masks  (e.g., John Doe -> <PERSON>)
        self.anonymizer = AnonymizerEngine()

    def extract_and_scrub(self, pdf_path):
        """Reads a healthcare PDF and redacts PII locally."""
        text = ""
        with open(pdf_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        
        # We are targetting Names, Phone Numbers, and Emails
        results = self.analyzer.analyze(text=text, language='en', 
                                        entities=["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS"])
        
        # Scrubbing the sensitive data before it ever hits the LLM
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        return anonymized_result.text

