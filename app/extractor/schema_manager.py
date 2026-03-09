import json
from pathlib import Path

DEFAULT_SCHEMAS = {
    "Formulaire générique": {
        "title": "Formulaire générique",
        "type": "object",
        "properties": {
            "nom": {"type": "string", "description": "Nom de famille"},
            "prenom": {"type": "string", "description": "Prénom"},
            "date_naissance": {"type": "string", "format": "date", "description": "Date de naissance"},
            "email": {"type": "string", "format": "email", "description": "Adresse email"},
            "telephone": {"type": "string", "description": "Numéro de téléphone"},
            "adresse": {"type": "string", "description": "Adresse postale"},
            "ville": {"type": "string", "description": "Ville"},
            "code_postal": {"type": "string", "description": "Code postal"},
        },
        "required": ["nom", "prenom"]
    },
    "Facture": {
        "title": "Facture",
        "type": "object",
        "properties": {
            "numero_facture": {"type": "string", "description": "Numéro de facture"},
            "date_facture": {"type": "string", "format": "date"},
            "nom_client": {"type": "string"},
            "montant_ht": {"type": "number", "description": "Montant HT"},
            "tva": {"type": "number", "description": "TVA (%)"},
            "montant_ttc": {"type": "number", "description": "Montant TTC"},
            "iban": {"type": "string", "description": "IBAN du fournisseur"},
        },
        "required": ["numero_facture", "montant_ttc"]
    },
    "Formulaire médical": {
        "title": "Formulaire médical",
        "type": "object",
        "properties": {
            "nom_patient": {"type": "string"},
            "date_naissance": {"type": "string", "format": "date"},
            "numero_secu": {"type": "string", "description": "Numéro de sécurité sociale"},
            "medecin": {"type": "string"},
            "date_consultation": {"type": "string", "format": "date"},
            "diagnostic": {"type": "string"},
            "traitement": {"type": "string"},
            "allergies": {"type": "string"},
        },
        "required": ["nom_patient"]
    }
}

class SchemaManager:
    def get_default_schemas(self) -> dict:
        return DEFAULT_SCHEMAS

    def load_from_json(self, json_str: str) -> dict:
        return json.loads(json_str)

    def validate_schema(self, schema: dict) -> tuple[bool, str]:
        if "properties" not in schema:
            return False, "Le schéma doit contenir une clé 'properties'"
        if not isinstance(schema["properties"], dict):
            return False, "'properties' doit être un objet"
        return True, "Schéma valide"

    def schema_to_display(self, schema: dict) -> list[dict]:
        """Convertit le schéma en liste pour affichage."""
        result = []
        required = schema.get("required", [])
        for name, definition in schema.get("properties", {}).items():
            result.append({
                "Champ": name,
                "Type": definition.get("type", "string"),
                "Description": definition.get("description", ""),
                "Obligatoire": "✅" if name in required else "❌",
                "Format": definition.get("format", "")
            })
        return result