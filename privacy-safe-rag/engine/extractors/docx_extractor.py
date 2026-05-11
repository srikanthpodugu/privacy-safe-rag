import io
from docx import Document


def extract_docx_text(content):

    file_obj = io.BytesIO(content)

    doc = Document(file_obj)

    text = []

    for para in doc.paragraphs:

        if para.text:
            text.append(para.text)

    return "\n".join(text)
