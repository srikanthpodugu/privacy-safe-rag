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
