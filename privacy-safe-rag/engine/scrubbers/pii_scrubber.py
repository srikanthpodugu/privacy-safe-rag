from engine.vault.tokenizer import DeterministicTokenizer
from engine.calibration.confidence_calibrator import ConfidenceCalibrator


class PIIScrubber:

    def __init__(self, analyzer=None, fusion_engine=None):

        self.analyzer = analyzer
        self.fusion_engine = fusion_engine

        self.tokenizer = DeterministicTokenizer()

        self.calibrator = ConfidenceCalibrator()

        self.allowed_entities = {

            "PERSON",
            "PHONE_NUMBER",
            "EMAIL_ADDRESS",
            "IP_ADDRESS",
            "DATE_TIME",
            "US_SSN",
            "CREDIT_CARD",
            "LOCATION",
            "ACCOUNT_NUMBER",
            "MEDICAL_RECORD_NUMBER"
        }

    # ==========================================================
    # MAIN SCRUB FUNCTION
    # ==========================================================
    def scrub(self, text: str, domain: str = None):

        # ======================================================
        # PRESIDIO DETECTION
        # ======================================================
        presidio_results = self.analyzer.analyze(
            text=text,
            language="en",
            score_threshold=0.5
        )

        presidio_results = [

            r for r in presidio_results

            if r.entity_type in self.allowed_entities
        ]

        # ======================================================
        # REGEX FALLBACK
        # ======================================================
        import re

        regex_results = []

        phone_pattern = r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

        for match in re.finditer(phone_pattern, text):

            regex_results.append({

                "entity_type": "PHONE_NUMBER",
                "start": match.start(),
                "end": match.end()
            })

        # ======================================================
        # FUTURE LLM RESULTS
        # ======================================================
        llm_results = []

        # ======================================================
        # FUSION ENGINE
        # ======================================================
        final_entities = self.fusion_engine.merge([

            {
                "source": "presidio",
                "results": presidio_results
            },

            {
                "source": "regex",
                "results": regex_results
            },

            {
                "source": "llm",
                "results": llm_results
            }
        ])

        # ======================================================
        # CONFIDENCE CALIBRATION
        # ======================================================
        validated_entities = []

        for entity in final_entities:

            is_valid = self.calibrator.validate(

                entity=entity,
                original_text=text
            )

            if is_valid:
                validated_entities.append(entity)

        # ======================================================
        # TOKENIZATION
        # ======================================================
        scrubbed_text = text

        validated_entities = sorted(

            validated_entities,

            key=lambda x: x["start"],

            reverse=True
        )

        for entity in validated_entities:

            original_value = text[
                entity["start"]:entity["end"]
            ]

            token = self.tokenizer.generate_token(

                entity_type=entity["entity_type"],
                original_value=original_value
            )

            scrubbed_text = (

                scrubbed_text[:entity["start"]] +

                token +

                scrubbed_text[entity["end"]:]
            )

        # ======================================================
        # RETURN
        # ======================================================
        return {

            "scrubbed_text": scrubbed_text,

            "entities": validated_entities
        }