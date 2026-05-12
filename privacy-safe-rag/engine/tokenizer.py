from engine.vault.token_vault import TokenVault


class DeterministicTokenizer:

    def __init__(self):

        self.vault = TokenVault()

    # ==========================================================
    # GENERATE DETERMINISTIC TOKEN
    # ==========================================================
    def generate_token(
        self,
        entity_type,
        original_value
    ):

        return self.vault.get_token(
            value=original_value,
            entity_type=entity_type
        )