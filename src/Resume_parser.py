import io

def extract_text_from_pdf(file_obj):
    text = ""
    raw = file_obj.read() if hasattr(file_obj, "read") else file_obj
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        if text.strip():
            return text
    except Exception as e:
        print(f"pdfplumber error: {e}")
    try:
        import fitz
        doc = fitz.open(stream=raw, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        print(f"fitz error: {e}")
    return text
