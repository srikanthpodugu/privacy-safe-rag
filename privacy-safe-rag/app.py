from engine.ingestor import PrivacyIngestor

print("Initializing Universal Privacy-Safe AI Gateway...")
engine = PrivacyIngestor()

test_scenarios = {

    "Finance":
    """
    Transfer $5000 to account ACC998812
    for Srikanth Podugu.
    SSN: 123-45-6789
    Credit Card: 4111-1111-1111-1111
    """,

    "HR":
    """
    Candidate John Smith lives at
    123 Apple St.
    Email: john@gmail.com
    Phone: 555-0101
    DOB: 01/01/1990
    """,

    "Healthcare":
    """
    Patient Jane Doe
    MRN-88291
    visited Austin Medical Center.
    Contact: jane@hospital.org
    """
}

print("\n================ PRIVACY TEST ================\n")

for domain, text in test_scenarios.items():

    print(f"DOMAIN: {domain}")
    print("\nORIGINAL:")
    print(text)

    scrubbed = engine.extract_and_scrub_text(text)

    print("\nSCRUBBED:")
    print(scrubbed)

    print("\n" + "=" * 50 + "\n")

print("Privacy Layer Operational.")