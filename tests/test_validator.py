import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.validator.data_validator import DataValidator

validator = DataValidator()

# ─── Tests Email ─────────────────────────────────────────────────────────────
def test_email_valide():
    result = validator._validate_field(
        "email", "jean.dupont@gmail.com",
        {"type": "string", "format": "email"}, []
    )
    assert result["is_valid"] == True

def test_email_invalide():
    result = validator._validate_field(
        "email", "jean@",
        {"type": "string", "format": "email"}, []
    )
    assert result["is_valid"] == False

def test_email_sans_domaine():
    result = validator._validate_field(
        "email", "jean.dupont",
        {"type": "string", "format": "email"}, []
    )
    assert result["is_valid"] == False

# ─── Tests Date ──────────────────────────────────────────────────────────────
def test_date_format_fr():
    result = validator._validate_field(
        "date_naissance", "15/03/1990",
        {"type": "string", "format": "date"}, []
    )
    assert result["is_valid"] == True

def test_date_format_iso():
    result = validator._validate_field(
        "date_naissance", "1990-03-15",
        {"type": "string", "format": "date"}, []
    )
    assert result["is_valid"] == True

def test_date_invalide():
    result = validator._validate_field(
        "date_naissance", "abc-xyz",
        {"type": "string", "format": "date"}, []
    )
    assert result["is_valid"] == False

# ─── Tests Nombre ────────────────────────────────────────────────────────────
def test_nombre_valide():
    result = validator._validate_field(
        "montant", "1500.50",
        {"type": "number"}, []
    )
    assert result["is_valid"] == True

def test_nombre_invalide():
    result = validator._validate_field(
        "montant", "abc",
        {"type": "number"}, []
    )
    assert result["is_valid"] == False

def test_nombre_virgule():
    result = validator._validate_field(
        "montant", "1500,50",
        {"type": "number"}, []
    )
    assert result["is_valid"] == True

# ─── Tests Champs obligatoires ───────────────────────────────────────────────
def test_champ_obligatoire_present():
    result = validator._validate_field(
        "nom", "Dupont",
        {"type": "string"}, ["nom"]
    )
    assert result["is_valid"] == True

def test_champ_obligatoire_manquant():
    result = validator._validate_field(
        "nom", None,
        {"type": "string"}, ["nom"]
    )
    assert result["is_valid"] == False

def test_champ_optionnel_absent():
    result = validator._validate_field(
        "commentaire", None,
        {"type": "string"}, []
    )
    assert result["is_valid"] == True

# ─── Tests Statut ────────────────────────────────────────────────────────────
def test_statut_high_confidence():
    assert validator._get_status(0.95, True, "Dupont") == "high_confidence"

def test_statut_medium_confidence():
    assert validator._get_status(0.80, True, "Dupont") == "medium_confidence"

def test_statut_low_confidence():
    assert validator._get_status(0.50, True, "Dupont") == "low_confidence"

def test_statut_missing():
    assert validator._get_status(0.0, True, None) == "missing"

def test_statut_invalid():
    assert validator._get_status(0.9, False, "abc") == "invalid"