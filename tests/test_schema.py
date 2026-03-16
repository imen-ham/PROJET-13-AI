import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app.extractor.schema_manager import SchemaManager

schema_manager = SchemaManager()

def test_tous_schemas_ont_properties():
    schemas = schema_manager.get_default_schemas()
    for name, schema in schemas.items():
        assert "properties" in schema, f"Schéma '{name}' manque 'properties'"

def test_tous_schemas_ont_required():
    schemas = schema_manager.get_default_schemas()
    for name, schema in schemas.items():
        assert "required" in schema, f"Schéma '{name}' manque 'required'"

def test_champs_requis_existent_dans_properties():
    schemas = schema_manager.get_default_schemas()
    for name, schema in schemas.items():
        for req in schema.get("required", []):
            assert req in schema["properties"], \
                f"Champ requis '{req}' absent des properties dans '{name}'"

def test_schema_medicale_champs():
    schema = schema_manager.get_default_schemas()["Formulaire médical"]
    assert "nom_patient" in schema["properties"]
    assert "medecin" in schema["properties"]
    assert "diagnostic" in schema["properties"]

def test_ajout_champ_custom():
    schema = {
        "type": "object",
        "properties": {
            "nom": {"type": "string"}
        },
        "required": []
    }
    schema["properties"]["telephone"] = {"type": "string"}
    schema["required"].append("telephone")
    assert "telephone" in schema["properties"]
    assert "telephone" in schema["required"]

def test_serialisation_json():
    schema = schema_manager.get_default_schemas()["Formulaire générique"]
    json_str = json.dumps(schema, ensure_ascii=False)
    parsed = json.loads(json_str)
    assert parsed["properties"] == schema["properties"]