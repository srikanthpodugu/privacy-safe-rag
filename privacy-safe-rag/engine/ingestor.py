import re
import pypdf

from presidio_analyzer import (
    AnalyzerEngine,
    PatternRecognizer,
    Pattern
)

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


class PrivacyIngestor:

    def __init__(self):

        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

        self._register_custom_recognizers()

    # ==========================================================
    # CUSTOM RECOGNIZERS
    # ==========================================================
    def _register_custom_recognizers(self):

        recognizers = []

        # ------------------------------------------------------
        # BANK ACCOUNT
        # ------------------------------------------------------
        account_pattern = Pattern(
            name="bank_account_pattern",
            regex=r"\b(?:ACC|ACCT)?[- ]?\d{8,16}\b",
            score=0.85
        )

        account_recognizer = PatternRecognizer(
            supported_entity="ACCOUNT_NUMBER",
            patterns=[account_pattern]
        )

        recognizers.append(account_recognizer)

        # ------------------------------------------------------
        # SSN
        # ------------------------------------------------------
        ssn_pattern = Pattern(
            name="ssn_pattern",
            regex=r"\b\d{3}-\d{2}-\d{4}\b",
            score=0.95
        )

        ssn_recognizer = PatternRecognizer(
            supported_entity="US_SSN",
            patterns=[ssn_pattern]
        )

        recognizers.append(ssn_recognizer)

        # ------------------------------------------------------
        # CREDIT CARD
        # ------------------------------------------------------
        cc_pattern = Pattern(
            name="credit_card_pattern",
            regex=r"\b(?:\d[ -]*?){13,16}\b",
            score=0.9
        )

        cc_recognizer = PatternRecognizer(
            supported_entity="CREDIT_CARD",
            patterns=[cc_pattern]
        )

        recognizers.append(cc_recognizer)

        # ------------------------------------------------------
        # MEDICAL RECORD NUMBER
        # ------------------------------------------------------
        mrn_pattern = Pattern(
            name="mrn_pattern",
            regex=r"\b(?:MRN|MR#)[- ]?\d{4,12}\b",
            score=0.9
        )

        mrn_recognizer = PatternRecognizer(
            supported_entity="MEDICAL_RECORD_NUMBER",
            patterns=[mrn_pattern]
        )

        recognizers.append(mrn_recognizer)

        # ------------------------------------------------------
        # DOB
        # ------------------------------------------------------
        dob_pattern = Pattern(
            name="dob_pattern",
            regex=r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b",
            score=0.85
        )

        dob_recognizer = PatternRecognizer(
            supported_entity="DATE_OF_BIRTH",
            patterns=[dob_pattern]
        )

        recognizers.append(dob_recognizer)

        # ------------------------------------------------------
        # IP ADDRESS
        # ------------------------------------------------------
        ip_pattern = Pattern(
            name="ip_pattern",
            regex=r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
            score=0.8
        )

        ip_recognizer = PatternRecognizer(
            supported_entity="IP_ADDRESS",
            patterns=[ip_pattern]
        )

        recognizers.append(ip_recognizer)

        # Register all recognizers
        for recognizer in recognizers:
            self.analyzer.registry.add_recognizer(recognizer)

    # ==========================================================
    # MAIN SCRUB FUNCTION
    # ==========================================================
    def extract_and_scrub_text(self, raw_text):

        # --------------------------------------------
        # Detect entities
        # --------------------------------------------
        results = self.analyzer.analyze(
            text=raw_text,
            language="en",
            score_threshold=0.5
        )

        # --------------------------------------------
        # Remove false positives
        # --------------------------------------------
        cleaned_results = []

        blocked_words = {
            "account",
            "name",
            "phone",
            "number",
            "email",
            "customer",
            "patient"
        }

        for result in results:

            detected_text = raw_text[result.start:result.end].lower()

            if detected_text in blocked_words:
                continue

            cleaned_results.append(result)

        # --------------------------------------------
        # Custom replacement operators
        # --------------------------------------------
        operators = {
            "PERSON": OperatorConfig(
                "replace",
                {"new_value": "<PERSON>"}
            ),
            "EMAIL_ADDRESS": OperatorConfig(
                "replace",
                {"new_value": "<EMAIL>"}
            ),
            "PHONE_NUMBER": OperatorConfig(
                "replace",
                {"new_value": "<PHONE>"}
            ),
            "LOCATION": OperatorConfig(
                "replace",
                {"new_value": "<LOCATION>"}
            ),
            "ACCOUNT_NUMBER": OperatorConfig(
                "replace",
                {"new_value": "<ACCOUNT_NUMBER>"}
            ),
            "US_SSN": OperatorConfig(
                "replace",
                {"new_value": "<SSN>"}
            ),
            "CREDIT_CARD": OperatorConfig(
                "replace",
                {"new_value": "<CREDIT_CARD>"}
            ),
            "MEDICAL_RECORD_NUMBER": OperatorConfig(
                "replace",
                {"new_value": "<MRN>"}
            ),
            "DATE_OF_BIRTH": OperatorConfig(
                "replace",
                {"new_value": "<DOB>"}
            ),
            "IP_ADDRESS": OperatorConfig(
                "replace",
                {"new_value": "<IP_ADDRESS>"}
            )
        }

        # --------------------------------------------
        # Anonymize
        # --------------------------------------------
        anonymized_result = self.anonymizer.anonymize(
            text=raw_text,
            analyzer_results=cleaned_results,
            operators=operators
        )

        return anonymized_result.text

    # ==========================================================
    # PDF SUPPORT
    # ==========================================================
    def extract_text_from_pdf(self, pdf_path):

        extracted_text = []

        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)

            for page in reader.pages:
                text = page.extract_text()

                if text:
                    extracted_text.append(text)

        return "\n".join(extracted_text)