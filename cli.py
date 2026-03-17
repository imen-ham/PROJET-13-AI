import argparse
import json
from app.extractor.pdf_extractor import PDFExtractor
from app.extractor.ai_extractor import AIExtractor
from app.extractor.schema_manager import SchemaManager
from app.validator.data_validator import DataValidator
from app.config import Config

def main():
    parser = argparse.ArgumentParser(
        description="FormExtract — Extraction de données depuis des formulaires"
    )
    parser.add_argument("--file", required=True, help="Chemin vers le fichier à analyser")
    parser.add_argument("--schema", default="Formulaire générique",
                        choices=["Formulaire générique", "Facture", "Formulaire médical"],
                        help="Schéma à utiliser")
    parser.add_argument("--output", default="result.json", help="Fichier de sortie JSON")
    parser.add_argument("--format", default="json", choices=["json", "csv"], help="Format de sortie")

    args = parser.parse_args()

    print(f"\n📋 FormExtract CLI")
    print(f"─────────────────────────────")
    print(f"📄 Fichier  : {args.file}")
    print(f"📋 Schéma   : {args.schema}")
    print(f"💾 Sortie   : {args.output}")
    print(f"─────────────────────────────\n")

    # Extraction du texte
    print("🔍 Lecture du document...")
    from pathlib import Path
    file_ext = Path(args.file).suffix.lower()

    if file_ext == ".pdf":
        extractor = PDFExtractor()
        with open(args.file, "rb") as f:
            result = extractor.extract_from_bytes(f.read(), args.file)
        raw_text = result.get("text", "")
    elif file_ext == ".txt":
        with open(args.file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    else:
        print(f"❌ Format non supporté : {file_ext}")
        return

    if not raw_text.strip():
        print("❌ Aucun contenu détecté")
        return

    print(f"✅ Contenu extrait ({len(raw_text)} caractères)")

    # Extraction IA
    print("🤖 Analyse en cours...")
    schema_manager = SchemaManager()
    schemas = schema_manager.get_default_schemas()
    schema = schemas[args.schema]

    ai_extractor = AIExtractor()
    result = ai_extractor.extract(raw_text, schema)

    # Validation
    print("✅ Validation des données...")
    validator = DataValidator()
    validated = validator.validate_and_enrich(result, schema)

    # Affichage résultats
    fields = validated.get("validated_fields", {})
    print(f"\n📊 Résultats :")
    print(f"─────────────────────────────")
    print(f"Total champs  : {validated['total_fields']}")
    print(f"Détectés      : {validated['extracted_count']}")
    print(f"Valides       : {validated['valid_count']}")
    print(f"Fiabilité     : {validated['overall_confidence']:.0%}")
    print(f"─────────────────────────────")

    for field_name, field_data in fields.items():
        status = "✅" if field_data.get("is_valid") else "❌"
        conf = field_data.get("confidence", 0)
        value = field_data.get("value", "—")
        print(f"{status} {field_name:<20} : {value} ({conf:.0%})")

    # Export
    export_data = {
        "metadata": {
            "fichier": args.file,
            "schema": args.schema,
            "overall_confidence": validated["overall_confidence"],
            "total_fields": validated["total_fields"],
            "extracted_count": validated["extracted_count"],
            "valid_count": validated["valid_count"],
        },
        "data": {k: v.get("value") for k, v in fields.items()}
    }

    if args.format == "json":
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Résultat sauvegardé dans : {args.output}")

    elif args.format == "csv":
        import csv
        csv_file = args.output.replace(".json", ".csv")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Champ", "Valeur", "Confiance", "Statut"])
            for k, v in fields.items():
                writer.writerow([
                    k,
                    v.get("value", ""),
                    f"{v.get('confidence', 0):.0%}",
                    v.get("status", "")
                ])
        print(f"\n💾 Résultat sauvegardé dans : {csv_file}")

    print("\n✅ Extraction terminée !\n")

if __name__ == "__main__":
    main()