from presidio_analyzer import PatternRecognizer, Pattern


def register_custom_recognizers(analyzer):

    recognizers = []

    patterns = [
        (
            "PHONE_NUMBER",
            r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
            0.95,
            "phone"
        ),
        (
            "ACCOUNT_NUMBER",
            r"\b(?:ACC|ACCT)[- ]?\d{6,16}\b",
            0.9,
            "account"
        ),
        (
            "US_SSN",
            r"\b\d{3}-\d{2}-\d{4}\b",
            0.95,
            "ssn"
        ),
        (
            "CREDIT_CARD",
            r"\b(?:\d[ -]*?){13,16}\b",
            0.9,
            "cc"
        ),
        (
            "MEDICAL_RECORD_NUMBER",
            r"\b(?:MRN|MR#)[- ]?\d{4,12}\b",
            0.9,
            "mrn"
        ),
        (
            "DATE_OF_BIRTH",
            r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b",
            0.85,
            "dob"
        ),
        (
            "IP_ADDRESS",
            r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b",
            0.85,
            "ip"
        )
    ]

    for entity, regex, score, name in patterns:

        pattern = Pattern(
            name=name,
            regex=regex,
            score=score
        )

        recognizer = PatternRecognizer(
            supported_entity=entity,
            patterns=[pattern]
        )

        analyzer.registry.add_recognizer(recognizer)
