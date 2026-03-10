import re
from datetime import datetime

class DataValidator:
    def validate_and_enrich(self, extracted: dict, schema: dict) -> dict:
        """Valide les données extraites et enrichit avec des métadonnées."""
        fields = extracted.get("extracted_fields", {})
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        validated = {}
        global_issues = []

        for field_name, field_data in fields.items():
            field_def = properties.get(field_name, {})
            value = field_data.get("value")
            confidence = field_data.get("confidence", 0.0)
            
            validation = self._validate_field(field_name, value, field_def, required)
            
            validated[field_name] = {
                **field_data,
                "is_valid": validation["is_valid"],
                "validation_message": validation["message"],
                "needs_review": confidence < 0.7 or not validation["is_valid"],
                "status": self._get_status(confidence, validation["is_valid"], value)
            }
            
            if not validation["is_valid"]:
                global_issues.append(f"{field_name}: {validation['message']}")

        # Champs requis manquants
        for req_field in required:
            if req_field not in fields or fields[req_field].get("value") is None:
                global_issues.append(f"Champ obligatoire manquant: {req_field}")
                if req_field not in validated:
                    validated[req_field] = {
                        "value": None,
                        "confidence": 0.0,
                        "is_valid": False,
                        "validation_message": "Champ obligatoire absent",
                        "needs_review": True,
                        "status": "missing"
                    }

        return {
            "validated_fields": validated,
            "overall_confidence": extracted.get("overall_confidence", 0.0),
            "global_issues": global_issues,
            "total_fields": len(properties),
            "extracted_count": sum(1 for f in validated.values() if f.get("value")),
            "valid_count": sum(1 for f in validated.values() if f.get("is_valid")),
            "review_count": sum(1 for f in validated.values() if f.get("needs_review")),
            "notes": extracted.get("notes", ""),
            "provider": extracted.get("provider", "unknown")
        }

    def _validate_field(self, name: str, value, definition: dict, required: list) -> dict:
        if value is None:
            if name in required:
                return {"is_valid": False, "message": "Champ obligatoire manquant"}
            return {"is_valid": True, "message": "Champ optionnel absent"}

        field_type = definition.get("type", "string")
        field_format = definition.get("format", "")

        if field_format == "email":
            if not re.match(r"[\w\.-]+@[\w\.-]+\.\w{2,}", str(value)):
                return {"is_valid": False, "message": "Format email invalide"}

        if field_format == "date":
            if not self._validate_date(str(value)):
                return {"is_valid": False, "message": "Format date invalide"}

        if field_type == "number":
            try:
                float(str(value).replace(",", ".").replace(" ", ""))
            except:
                return {"is_valid": False, "message": "Valeur numérique invalide"}

        if "pattern" in definition:
            if not re.match(definition["pattern"], str(value)):
                return {"is_valid": False, "message": f"Ne correspond pas au pattern attendu"}

        return {"is_valid": True, "message": "✓ Valide"}

    def _validate_date(self, date_str: str) -> bool:
        formats = ["%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%d.%m.%Y", "%m/%d/%Y"]
        for fmt in formats:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except:
                continue
        return False

    def _get_status(self, confidence: float, is_valid: bool, value) -> str:
        if value is None:
            return "missing"
        if not is_valid:
            return "invalid"
        if confidence >= 0.9:
            return "high_confidence"
        if confidence >= 0.7:
            return "medium_confidence"
        return "low_confidence"