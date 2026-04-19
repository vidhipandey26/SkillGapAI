import io

def extract_text_from_pdf(file_obj) -> str:
    text = ""
    raw_bytes = file_obj.read() if hasattr(file_obj, "read") else file_obj

    # Primary: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    # Fallback: PyMuPDF
    try:
        import fitz
        doc = fitz.open(stream=raw_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text("text") + "\n"
        doc.close()
        if text.strip():
            return text
    except Exception as e:
        print(f"PyMuPDF failed: {e}")

    # Last resort: decode with error ignoring
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
        return text
    except Exception as e:
        print(f"Decode failed: {e}")

    return ""
