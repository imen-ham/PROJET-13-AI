import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "formextract.db"

def init_db():
    """Initialise la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extractions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            fichier TEXT NOT NULL,
            schema_nom TEXT NOT NULL,
            total_champs INTEGER,
            detectes INTEGER,
            valides INTEGER,
            fiabilite REAL,
            donnees JSON,
            details JSON
        )
    """)
    conn.commit()
    conn.close()

def save_extraction(fichier, schema_nom, validated_data, export_data):
    """Sauvegarde une extraction dans la BDD."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO extractions 
        (date, fichier, schema_nom, total_champs, detectes, valides, fiabilite, donnees, details)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%d/%m/%Y %H:%M"),
        fichier,
        schema_nom,
        validated_data.get("total_fields", 0),
        validated_data.get("extracted_count", 0),
        validated_data.get("valid_count", 0),
        validated_data.get("overall_confidence", 0),
        json.dumps(export_data, ensure_ascii=False),
        json.dumps(validated_data.get("validated_fields", {}), ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

def get_all_extractions():
    """Récupère toutes les extractions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, date, fichier, schema_nom, total_champs, detectes, valides, fiabilite, donnees
        FROM extractions
        ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_extraction_by_id(extraction_id):
    """Récupère une extraction par son ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM extractions WHERE id = ?", (extraction_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_extraction(extraction_id):
    """Supprime une extraction."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM extractions WHERE id = ?", (extraction_id,))
    conn.commit()
    conn.close()

def clear_all():
    """Vide tout l'historique."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM extractions")
    conn.commit()
    conn.close()