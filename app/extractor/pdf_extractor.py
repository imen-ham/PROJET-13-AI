import pdfplumber
import PyPDF2
from pathlib import Path

class PDFExtractor:
    def extract_text(self, file_path: str) -> dict:
        """Extrait le texte d'un PDF avec métadonnées."""
        result = {
            "text": "",
            "pages": [],
            "metadata": {},
            "method": "pdfplumber"
        }
        try:
            with pdfplumber.open(file_path) as pdf:
                result["metadata"] = pdf.metadata or {}
                full_text = []
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text() or ""
                    tables = page.extract_tables() or []
                    result["pages"].append({
                        "page_num": i + 1,
                        "text": page_text,
                        "tables": tables
                    })
                    full_text.append(page_text)
                result["text"] = "\n\n".join(full_text)
                if result["text"].strip():
                    return result
        except Exception as e:
            result["error_pdfplumber"] = str(e)

        # Fallback PyPDF2
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                texts = []
                for page in reader.pages:
                    texts.append(page.extract_text() or "")
                result["text"] = "\n".join(texts)
                result["method"] = "PyPDF2"
        except Exception as e:
            result["error_pypdf2"] = str(e)

        return result

    def extract_from_bytes(self, file_bytes: bytes, filename: str) -> dict:
        """Extrait depuis des bytes (upload Streamlit)."""
        import tempfile, os
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name
        try:
            return self.extract_text(tmp_path)
        finally:
            os.unlink(tmp_path)