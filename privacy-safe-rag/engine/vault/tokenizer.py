from engine.vault.token_vault import TokenVault


class DeterministicTokenizer:

    def __init__(self):
        self.vault = TokenVault()

    def generate_token(self, entity_type: str, original_value: str):
        return self.vault.get_token(
            value=original_value,
            entity_type=entity_type
        )