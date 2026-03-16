import pytesseract
from PIL import Image
import io

class ImageExtractor:
    def __init__(self):
        # Windows: décommente et adapte le chemin
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def extract_text(self, file_bytes: bytes, lang: str = "fra+eng") -> dict:
        """OCR sur image avec score de confiance."""
        result = {"text": "", "confidence": 0.0, "method": "tesseract"}
        try:
            image = Image.open(io.BytesIO(file_bytes))
            # Prétraitement
            image = self._preprocess(image)

            # Extraction avec données de confiance
            data = pytesseract.image_to_data(
                image, lang=lang, output_type=pytesseract.Output.DICT
            )
            words = [w for w, c in zip(data["text"], data["conf"])
                     if w.strip() and int(c) > 0]
            confs = [int(c) for c in data["conf"] if int(c) > 0]

            result["text"] = pytesseract.image_to_string(image, lang=lang)
            result["confidence"] = round(sum(confs) / len(confs) / 100, 2) if confs else 0.0
            result["word_count"] = len(words)
        except Exception as e:
            result["error"] = str(e)
            result["text"] = ""
        return result

    def _preprocess(self, image: Image.Image) -> Image.Image:
        """Améliore la qualité pour l'OCR."""
        if image.mode != "L":
            image = image.convert("L")
        # Augmenter contraste
        from PIL import ImageEnhance, ImageFilter
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = image.filter(ImageFilter.SHARPEN)
        return image