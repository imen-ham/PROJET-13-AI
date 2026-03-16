import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractor.schema_manager import SchemaManager
from app.extractor.ai_extractor import AIExtractor

schema_manager = SchemaManager()

# ─── Tests SchemaManager ─────────────────────────────────────────────────────
def test_schemas_disponibles():
    schemas = schema_manager.get_default_schemas()
    assert "Formulaire générique" in schemas
    assert "Facture" in schemas
    assert "Formulaire médical" in schemas

def test_schema_generique_contient_champs():
    schema = schema_manager.get_default_schemas()["Formulaire générique"]
    assert "nom" in schema["properties"]
    assert "prenom" in schema["properties"]
    assert "email" in schema["properties"]

def test_schema_facture_contient_champs():
    schema = schema_manager.get_default_schemas()["Facture"]
    assert "numero_facture" in schema["properties"]
    assert "montant_ttc" in schema["properties"]

def test_validation_schema_valide():
    schema = {
        "type": "object",
        "properties": {
            "nom": {"type": "string"}
        }
    }
    ok, msg = schema_manager.validate_schema(schema)
    assert ok == True

def test_validation_schema_invalide():
    schema = {"type": "object"}
    ok, msg = schema_manager.validate_schema(schema)
    assert ok == False

def test_schema_to_display():
    schema = schema_manager.get_default_schemas()["Formulaire générique"]
    display = schema_manager.schema_to_display(schema)
    assert isinstance(display, list)
    assert len(display) > 0
    assert "Champ" in display[0]

def test_load_from_json():
    import json
    schema = {"type": "object", "properties": {"nom": {"type": "string"}}}
    result = schema_manager.load_from_json(json.dumps(schema))
    assert result["type"] == "object"

# ─── Tests AIExtractor Mock ───────────────────────────────────────────────────
def test_mock_extraction_email():
    extractor = AIExtractor()
    text = "Email: jean.dupont@gmail.com"
    schema = {
        "properties": {
            "email": {"type": "string", "format": "email"}
        }
    }
    result = extractor._mock_extraction(text, schema)
    assert "extracted_fields" in result
    assert "email" in result["extracted_fields"]

def test_mock_extraction_champ_absent():
    extractor = AIExtractor()
    text = "Aucune information utile ici"
    schema = {
        "properties": {
            "email": {"type": "string", "format": "email"}
        }
    }
    result = extractor._mock_extraction(text, schema)
    assert result["extracted_fields"]["email"]["confidence"] == 0.0

def test_parse_json_valide():
    extractor = AIExtractor()
    content = '{"extracted_fields": {}, "overall_confidence": 0.8}'
    result = extractor._parse_json_response(content)
    assert result["overall_confidence"] == 0.8

def test_parse_json_avec_backticks():
    extractor = AIExtractor()
    content = '```json\n{"extracted_fields": {}, "overall_confidence": 0.5}\n```'
    result = extractor._parse_json_response(content)
    assert result["overall_confidence"] == 0.5