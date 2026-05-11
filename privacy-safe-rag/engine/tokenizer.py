import hashlib
import json
import os


class DeterministicTokenizer:

    def __init__(self):

        # Secret key used for deterministic hashing
        self.secret_key = "privacy-safe-rag-secret"

        # Vault storage
        self.vault_path = "vault.json"

        # Load existing vault
        self.vault = self._load_vault()

    # ==========================================================
    # LOAD VAULT
    # ==========================================================
    def _load_vault(self):

        if os.path.exists(self.vault_path):

            with open(self.vault_path, "r") as f:
                return json.load(f)

        return {}

    # ==========================================================
    # SAVE VAULT
    # ==========================================================
    def _save_vault(self):

        with open(self.vault_path, "w") as f:
            json.dump(self.vault, f, indent=2)

    # ==========================================================
    # GENERATE DETERMINISTIC TOKEN
    # ==========================================================
    def generate_token(self, entity_type: str, original_value: str):

        # Normalize value
        normalized = original_value.strip().lower()

        # Deterministic hash
        hash_value = hashlib.sha256(
            f"{self.secret_key}:{normalized}".encode()
        ).hexdigest()[:8]

        token = f"{entity_type}_{hash_value}"

        # Store mapping in vault
        if token not in self.vault:
            self.vault[token] = original_value
            self._save_vault()

        return token

    # ==========================================================
    # RE-IDENTIFICATION
    # ==========================================================
    def reidentify(self, token: str):

        return self.vault.get(token, None)
