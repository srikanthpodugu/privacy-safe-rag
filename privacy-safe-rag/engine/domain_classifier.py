from sentence_transformers import SentenceTransformer
import numpy as np


class SemanticDomainClassifier:

    def __init__(self):

        # Lightweight, strong general model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Domain prototypes (NO KEYWORDS used for matching)
        self.domain_profiles = {
            "hr": [
                "resume of a software engineer with work experience",
                "job application and employment history document",
                "curriculum vitae describing skills and projects",
                "hiring candidate profile with education and experience"
            ],
            "finance": [
                "banking transaction and payment invoice document",
                "credit card statement and financial report",
                "loan application and billing statement",
                "financial audit and accounting records"
            ],
            "healthcare": [
                "patient medical record and diagnosis report",
                "hospital clinical notes and prescriptions",
                "medical history with treatment and MRN",
                "healthcare lab results and doctor notes"
            ],
            "general": [
                "general informational document text",
                "random text not belonging to a specific domain"
            ]
        }

        # Precompute domain embeddings
        self.domain_embeddings = {
            domain: np.mean(self.model.encode(samples), axis=0)
            for domain, samples in self.domain_profiles.items()
        }

    def classify(self, text: str) -> str:

        text_embedding = self.model.encode(text)

        best_domain = "general"
        best_score = -1

        for domain, domain_embedding in self.domain_embeddings.items():

            score = self._cosine_similarity(text_embedding, domain_embedding)

            if score > best_score:
                best_score = score
                best_domain = domain

        return best_domain

    def _cosine_similarity(self, a, b):

        a = np.array(a)
        b = np.array(b)

        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))