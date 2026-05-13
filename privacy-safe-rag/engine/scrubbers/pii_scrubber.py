from engine.vault.tokenizer import DeterministicTokenizer


class PIIScrubber:

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.tokenizer = DeterministicTokenizer()

    # ==========================================================
    # SCRUB FUNCTION
    # ==========================================================
    def scrub(self, text: str, domain: str):

        results = self.analyzer.analyze(
            text=text,
            language="en",
            score_threshold=0.5
        )

        # IMPORTANT: reverse sorting prevents index shift issues
        results = sorted(results, key=lambda x: x.start, reverse=True)

        scrubbed_text = text
        entity_counts = {}

        # ======================================================
        # TOKENIZATION LOOP
        # ======================================================
        for r in results:

            original_value = text[r.start:r.end]

            token = self.tokenizer.generate_token(
                entity_type=r.entity_type,
                original_value=original_value
            )

            scrubbed_text = (
                scrubbed_text[:r.start]
                + token
                + scrubbed_text[r.end:]
            )

            entity_counts[r.entity_type] = entity_counts.get(r.entity_type, 0) + 1

        return {
            "scrubbed_text": scrubbed_text,
            "entity_breakdown": entity_counts
        }