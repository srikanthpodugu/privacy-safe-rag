from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from engine.policies.policy import DOMAIN_POLICIES
from engine.tokenizer import DeterministicTokenizer


class PIIScrubber:

    def __init__(self):

        self.analyzer = AnalyzerEngine()
        self.tokenizer = DeterministicTokenizer()

        self._register_custom_recognizers()

    # ==========================================================
    # CUSTOM RECOGNIZERS
    # ==========================================================
    def _register_custom_recognizers(self):

        recognizers = []

        # PHONE
        phone = Pattern(
            name="phone",
            regex=r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            score=0.95
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="PHONE_NUMBER",
                patterns=[phone]
            )
        )

        # ACCOUNT
        account = Pattern(
            name="account",
            regex=r"\b(?:ACC|ACCT)[- ]?\d{6,16}\b",
            score=0.90
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="ACCOUNT_NUMBER",
                patterns=[account]
            )
        )

        # SSN
        ssn = Pattern(
            name="ssn",
            regex=r"\b\d{3}-\d{2}-\d{4}\b",
            score=0.95
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="US_SSN",
                patterns=[ssn]
            )
        )

        # CREDIT CARD
        cc = Pattern(
            name="cc",
            regex=r"\b(?:\d[ -]*?){13,16}\b",
            score=0.90
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="CREDIT_CARD",
                patterns=[cc]
            )
        )

        # MRN
        mrn = Pattern(
            name="mrn",
            regex=r"\b(?:MRN|MR#)[- ]?\d{4,12}\b",
            score=0.90
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="MEDICAL_RECORD_NUMBER",
                patterns=[mrn]
            )
        )

        # DOB
        dob = Pattern(
            name="dob",
            regex=r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b",
            score=0.85
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="DATE_OF_BIRTH",
                patterns=[dob]
            )
        )

        # IP ADDRESS
        ip = Pattern(
            name="ip",
            regex=r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b",
            score=0.85
        )
        recognizers.append(
            PatternRecognizer(
                supported_entity="IP_ADDRESS",
                patterns=[ip]
            )
        )

        for r in recognizers:
            self.analyzer.registry.add_recognizer(r)

    # ==========================================================
    # MAIN SCRUB FUNCTION (TOKENIZATION ENABLED)
    # ==========================================================
    def scrub(self, text: str, domain: str):

        policy = DOMAIN_POLICIES.get(domain, DOMAIN_POLICIES["general"])
        allowed_entities = set(policy["scrub"])

        results = self.analyzer.analyze(
            text=text,
            language="en",
            score_threshold=0.5
        )

        # IMPORTANT: reverse order to preserve indexes
        results = sorted(results, key=lambda x: x.start, reverse=True)

        for r in results:

            if r.entity_type not in allowed_entities:
                continue

            original_value = text[r.start:r.end]

            token = self.tokenizer.generate_token(
                entity_type=r.entity_type,
                original_value=original_value
            )

            text = text[:r.start] + token + text[r.end:]

        return text