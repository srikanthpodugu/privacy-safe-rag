# Universal Privacy-Safe AI Gateway
A production-grade "Privacy-First" wrapper for LLM applications. 
This system acts as a secure firewall, redacting sensitive PII from any document before it reaches an AI model.

## The Core Problem
Most AI systems send raw documents directly to cloud LLMs, risking the exposure of Sensitive Personal Information (PII/PHI). This project implements a **Local Governance Layer** that redacts sensitive data *before* it ever leaves your secure environment.

## Use Cases
- **Finance:** Masking Account Numbers and Transaction details.
- **Legal:** Redacting Client names and specific case dates in contracts.
- **HR/Recruitment:** Anonymizing Resumes to prevent hiring bias and protect PII.
- **Healthcare:** Ensuring HIPAA-lite compliance by scrubbing Patient identifiers.

## 🛠️ The Tech Stack (The "Brain" of the Project)
- **Microsoft Presidio:** This is our primary Data Governance engine which uses pattern matching and ML to identify Names, SSNs, and Phone Numbers.
- **spaCy (en_core_web_lg):** This allows our system to understand English context and grammar.
- **PyPDF:** This is for extracting text from complex  PDFs.
- **Local-First Processing:** Designed to run PII redaction locally (via Ollama or local NLP models) to ensure 100% data residency.

## 🔒 Privacy Workflow
1. **Extraction:** PyPDF reads the raw document.
2. **Analysis:** Presidio + spaCy scan for entities (PERSON, PHONE, EMAIL).
3. **Anonymization:** Real names are replaced with safe placeholders 
4. **Processing:** The "scrubbed" text is then safely used for AI summaries or questions.

## Note: Streamlit
Streamlit is just a demo layer and all the scrubbing happens before LLM call. This UI is for visualization only.

## 🧩 What Makes My Project Different

Unlike traditional PII scrubbing systems, my project introduces:

🔹 1. Semantic Domain Awareness

Instead of keyword-based detection, the system understands meaning using embeddings:

HR resumes
Finance documents
Healthcare records

This ensures context-aware privacy rules, not brittle keyword logic.

🔹 2. Deterministic Tokenization (Core Differentiator)

Sensitive data is not just removed — it is replaced with:

John Matthews → <PERSON_1029>
john@email.com → <EMAIL_5521>

This enables:

Re-identification when needed (via vault)
Consistent masking across systems
Safe analytics on anonymized datasets

🔹 3. Policy-Driven Scrubbing

Each domain has its own privacy policy:

Healthcare → stricter PHI rules
Finance → account + transaction focus
HR → resume + identity masking
General → minimal scrubbing

## 🧪 Current Capabilities (MVP Status)

✔ PDF / DOCX / TXT ingestion
✔ Semantic domain detection (no keywords)
✔ PII detection using Presidio
✔ Deterministic tokenization
✔ Domain-based privacy policies
✔ FastAPI backend

## 1. 🧪 Current Scope vs Future Scope (VERY IMPORTANT)

📌 Current Scope (MVP)
Single-node processing
Rule + embedding based classification
Presidio-based PII detection
Deterministic tokenization

🚧 Future Scope (Roadmap)
Token vault (re-identification service)
Multi-language PII detection
LLM-based contextual entity detection
Risk scoring + compliance layer (GDPR/HIPAA/PCI)
Distributed ingestion pipeline (Kafka / queue-based)
