import sqlite3
import hashlib
import uuid


class TokenVault:

    def __init__(self, db_path="vault.db"):

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self._create_table()

    # -----------------------------
    # Create table
    # -----------------------------
    def _create_table(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS token_map (
                id TEXT PRIMARY KEY,
                token TEXT,
                value TEXT,
                entity_type TEXT,
                hash TEXT
            )
        """)

        self.conn.commit()

    # -----------------------------
    # Generate stable hash
    # -----------------------------
    def _hash(self, value: str, entity_type: str):

        raw = f"{value.lower()}::{entity_type}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # -----------------------------
    # Get or create token
    # -----------------------------
    def get_token(self, value: str, entity_type: str):

        value_hash = self._hash(value, entity_type)

        self.cursor.execute(
            "SELECT token FROM token_map WHERE hash=?",
            (value_hash,)
        )

        row = self.cursor.fetchone()

        if row:
            return row[0]

        # generate deterministic token
        token = f"{entity_type.upper()}_{str(uuid.uuid4())[:8]}"

        self.cursor.execute("""
            INSERT INTO token_map (id, token, value, entity_type, hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            token,
            value,
            entity_type,
            value_hash
        ))

        self.conn.commit()

        return token

    # -----------------------------
    # Reverse lookup (re-identification)
    # -----------------------------
    def resolve_token(self, token: str):

        self.cursor.execute(
            "SELECT value FROM token_map WHERE token=?",
            (token,)
        )

        row = self.cursor.fetchone()

        return row[0] if row else None
