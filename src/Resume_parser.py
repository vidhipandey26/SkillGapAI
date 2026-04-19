"""
resume_parser.py
Extracts raw text from uploaded PDF resumes using pdfplumber.
Falls back to PyMuPDF if pdfplumber fails on a page.
"""
import io

def extract_text_from_pdf(file_obj) -> str:
    """
    Accept a Streamlit UploadedFile or any file-like object.
    Returns extracted plain text string.
    """
    text = ""
    raw_bytes = file_obj.read() if hasattr(file_obj, "read") else file_obj

    # ── Primary: pdfplumber ──────────────────────────────────────────────────
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
        print(f"[pdfplumber] failed: {e}")

    # ── Fallback: PyMuPDF (fitz) ─────────────────────────────────────────────
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=raw_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        print(f"[PyMuPDF] failed: {e}")

    return text