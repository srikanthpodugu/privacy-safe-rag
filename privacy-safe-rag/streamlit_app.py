import streamlit as st
from engine.ingestor import PrivacyIngestor
import pypdf

engine = PrivacyIngestor()

st.set_page_config(page_title="Privacy Safe AI Gateway", layout="wide")

st.title("🛡️ Universal Privacy-Safe AI Gateway")
st.subheader("Upload documents to detect and redact PII")

uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])

def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    if file.name.endswith(".pdf"):
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

if uploaded_file:

    raw_text = extract_text(uploaded_file)

    st.markdown("## 📄 Original Text")
    st.text_area("", raw_text, height=200)

    if st.button("🔒 Scrub PII"):

        scrubbed = engine.extract_and_scrub_text(raw_text)

        st.markdown("## 🧼 Scrubbed Output")
        st.text_area("", scrubbed, height=200)

        st.success("PII redaction complete")

