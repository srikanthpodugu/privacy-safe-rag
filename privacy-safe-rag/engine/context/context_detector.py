from sentence_transformers import SentenceTransformer
import numpy as np


class ContextualSensitivityDetector:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # ======================================================
        # SENSITIVE CONTEXT PROTOTYPES
        # ======================================================
        self.context_profiles = {

            "healthcare_sensitive": [

                "patient diagnosis and treatment",

                "medical condition and prescriptions",

                "clinical healthcare records",

                "hospital treatment notes"
            ],

            "finance_sensitive": [

                "financial fraud investigation",

                "banking payment records",

                "credit risk assessment",

                "financial account exposure"
            ],

            "hr_sensitive": [

                "employee termination details",

                "salary and compensation discussion",

                "performance review discussion",

                "confidential HR investigation"
            ]
        }

        # Precompute embeddings
        self.profile_embeddings = {

            k: np.mean(
                self.model.encode(v),
                axis=0
            )

            for k, v in self.context_profiles.items()
        }

    # ==========================================================
    # DETECT CONTEXTUAL SENSITIVITY
    # ==========================================================
    def detect(self, text):

        text_embedding = self.model.encode(text)

        findings = []

        for label, embedding in \
            self.profile_embeddings.items():

            score = self._cosine_similarity(
                text_embedding,
                embedding
            )

            if score > 0.45:

                findings.append({

                    "context_type": label,

                    "confidence": round(float(score), 3)
                })

        return findings

    # ==========================================================
    # COSINE SIMILARITY
    # ==========================================================
    def _cosine_similarity(self, a, b):

        a = np.array(a)

        b = np.array(b)

        return np.dot(a, b) / (
            np.linalg.norm(a) *
            np.linalg.norm(b)
        )
