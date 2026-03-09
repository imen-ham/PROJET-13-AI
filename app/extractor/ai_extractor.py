import json
import re
from app.config import Config

class AIExtractor:
    def __init__(self):
        self.provider = Config.AI_PROVIDER
        self._init_client()

    def _init_client(self):
        self.client = None
        if self.provider == "groq" and Config.GROQ_API_KEY:
            from groq import Groq
            self.client = Groq(api_key=Config.GROQ_API_KEY)
        elif self.provider == "anthropic" and Config.ANTHROPIC_API_KEY:
            import anthropic
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def extract(self, text: str, schema: dict) -> dict:
        """Extrait les données selon le schéma JSON fourni."""
        if self.provider == "mock" or not self.client:
            return self._mock_extraction(text, schema)
        elif self.provider == "groq":
            return self._extract_groq(text, schema)
        elif self.provider == "anthropic":
            return self._extract_anthropic(text, schema)

    def _build_prompt(self, text: str, schema: dict) -> str:
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        return f"""Tu es un expert en extraction de données de formulaires.

Voici le document à analyser :
---
{text[:6000]}
---

Voici le schéma JSON des champs à extraire :
{schema_str}

INSTRUCTIONS:
1. Extrais UNIQUEMENT les champs définis dans le schéma
2. Pour chaque champ, fournis une valeur extraite ET un score de confiance (0.0 à 1.0)
3. Si un champ est absent du document, utilise null
4. Réponds UNIQUEMENT avec un JSON valide, sans texte avant ou après

Format de réponse OBLIGATOIRE:
{{
  "extracted_fields": {{
    "nom_champ": {{
      "value": "valeur extraite ou null",
      "confidence": 0.95,
      "raw_text": "texte brut trouvé dans le document"
    }}
  }},
  "overall_confidence": 0.88,
  "notes": "observations générales"
}}"""

    def _extract_groq(self, text: str, schema: dict) -> dict:
        prompt = self._build_prompt(text, schema)
        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            return self._parse_json_response(content)
        except Exception as e:
            return {"error": str(e), "extracted_fields": {}}

    def _extract_anthropic(self, text: str, schema: dict) -> dict:
        prompt = self._build_prompt(text, schema)
        try:
            response = self.client.messages.create(
                model=Config.ANTHROPIC_MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.content[0].text
            return self._parse_json_response(content)
        except Exception as e:
            return {"error": str(e), "extracted_fields": {}}

    def _parse_json_response(self, content: str) -> dict:
        """Parse robuste de la réponse JSON."""
        # Nettoie les backticks
        content = re.sub(r"```json\s*|\s*```", "", content).strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Tente d'extraire le JSON avec regex
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
        return {"error": "Parsing JSON échoué", "extracted_fields": {}, "raw": content}

    def _mock_extraction(self, text: str, schema: dict) -> dict:
        """Mode démo sans API - simule une extraction."""
        fields = schema.get("properties", {})
        extracted = {}
        text_lower = text.lower()

        for field_name, field_def in fields.items():
            field_type = field_def.get("type", "string")
            # Cherche des patterns basiques
            value = self._basic_extract(field_name, text, field_type)
            extracted[field_name] = {
                "value": value,
                "confidence": 0.75 if value else 0.0,
                "raw_text": value or "",
                "source": "mock_regex"
            }

        return {
            "extracted_fields": extracted,
            "overall_confidence": 0.70,
            "notes": "Mode démonstration (sans API). Connectez une API pour une extraction précise.",
            "provider": "mock"
        }

    def _basic_extract(self, field_name: str, text: str, field_type: str):
        """Extraction basique par regex pour le mode mock."""
        import re
        patterns = {
            "nom": r"(?:nom|name)\s*[:\-]?\s*([A-ZÀ-Ü][a-zà-ü]+(?:\s+[A-ZÀ-Ü][a-zà-ü]+)*)",
            "prenom": r"(?:prénom|prenom|first.name)\s*[:\-]?\s*([A-ZÀ-Ü][a-zà-ü]+)",
            "email": r"[\w\.-]+@[\w\.-]+\.\w+",
            "telephone": r"(?:\+?\d[\d\s\-\.]{8,14}\d)",
            "date": r"\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}",
            "adresse": r"(?:adresse|address)\s*[:\-]?\s*(.+?)(?:\n|$)",
            "ville": r"(?:ville|city)\s*[:\-]?\s*([A-ZÀ-Ü][a-zà-ü\s]+)",
            "code_postal": r"\b\d{5}\b",
            "montant": r"(?:\d+[\s\u00a0]?\d*[,\.]\d{2}|\d+)\s*(?:€|EUR|eur)?",
        }
        for key, pattern in patterns.items():
            if key in field_name.lower():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1) if match.lastindex else match.group()
        return None