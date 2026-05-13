class ConfidenceCalibrator:

    def __init__(self):

        # ==========================================
        # ENTITY THRESHOLDS
        # ==========================================
        self.thresholds = {

            "PERSON": 0.45,
            "PHONE_NUMBER": 0.55,
            "EMAIL_ADDRESS": 0.55,
            "IP_ADDRESS": 0.55,
            "DATE_TIME": 0.75,
            "LOCATION": 0.45,
            "ACCOUNT_NUMBER": 0.55,
            "CREDIT_CARD": 0.65,
            "MEDICAL_RECORD_NUMBER": 0.55,
            "US_SSN": 0.75
        }

        # reject tiny spans
        self.min_length = {

            "PERSON": 4,
            "DATE_TIME": 6,
            "PHONE_NUMBER": 8,
            "EMAIL_ADDRESS": 5
        }

        # dangerous false-positive words
        self.blocked_values = {

            "annually",
            "department",
            "linkedin",
            "resume",
            "salary",
            "internal",
            "report",
            "invoice"
        }

    # ==========================================================
    # MAIN FILTER
    # ==========================================================
    def validate(self, entity, original_text):

        entity_type = entity["entity_type"]

        confidence = entity.get("confidence", 0.5)

        start = entity["start"]
        end = entity["end"]

        value = original_text[start:end].strip()

        # ======================================================
        # CONFIDENCE CHECK
        # ======================================================
        threshold = self.thresholds.get(entity_type, 0.6)

        if confidence < threshold:
            return False

        # ======================================================
        # MIN LENGTH CHECK
        # ======================================================
        min_len = self.min_length.get(entity_type, 2)

        if len(value) < min_len:
            return False

        # ======================================================
        # BLOCKED FALSE POSITIVES
        # ======================================================
        if value.lower() in self.blocked_values:
            return False

        # ======================================================
        # BAD DATE DETECTIONS
        # ======================================================
        if entity_type == "DATE_TIME":

            if value.isalpha():
                return False

            # muat contain digit
            if not any(char.isdigit() for char in value):
                return False     

        return True
