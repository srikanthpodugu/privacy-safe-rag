# engine/policy.py

HEALTHCARE_POLICY = {
    "scrub": {
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
        "US_SSN",
        "DATE_OF_BIRTH",
        "MEDICAL_RECORD_NUMBER",
        "ACCOUNT_NUMBER",
        "IP_ADDRESS",
        "LOCATION"
    }
}

FINANCE_POLICY = {
    "scrub": {
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
        "US_SSN",
        "CREDIT_CARD",
        "ACCOUNT_NUMBER",
        "IP_ADDRESS",
        "LOCATION"
    }
}

HR_POLICY = {
    "scrub": {
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
        "US_SSN",
        "DATE_OF_BIRTH",
        "LOCATION",
        "IP_ADDRESS"
    }
}

DEFAULT_POLICY = {
    "scrub": {
        "PERSON",
        "EMAIL_ADDRESS",
        "PHONE_NUMBER"
    }
}

DOMAIN_POLICIES = {
    "healthcare": HEALTHCARE_POLICY,
    "finance": FINANCE_POLICY,
    "hr": HR_POLICY,
    "general": DEFAULT_POLICY
}