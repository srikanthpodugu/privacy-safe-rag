import io
import pypdf


def extract_pdf_text(content):

    file_obj = io.BytesIO(content)

    reader = pypdf.PdfReader(file_obj)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)
