import pdfplumber


def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from uploaded PDF resume
    """
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text