#  Specifications Techniques — FormExtract

## 1. Présentation du projet

FormExtract est une application de traitement automatique de formulaires.
Elle permet d'extraire, valider et exporter des données structurées
depuis des documents PDF, texte ou image.

---

## 2. Architecture globale
```
┌─────────────────────────────────────────────────┐
│                  FRONTEND                        │
│              Streamlit (Python)                  │
│  Upload │ Schéma │ Résultats │ Export            │
└────────────────────┬────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│                  BACKEND                         │
│                                                  │
│  ┌─────────────┐  ┌─────────────┐               │
│  │ PDF         │  │ Image       │               │
│  │ Extractor   │  │ Extractor   │               │
│  │ pdfplumber  │  │ Tesseract   │               │
│  │ PyPDF2      │  │ OCR         │               │
│  └──────┬──────┘  └──────┬──────┘               │
│         └────────┬────────┘                      │
│                  │                               │
│  ┌───────────────▼──────────────┐                │
│  │        AI Extractor          │                │
│  │   Groq LLaMA3-70b            │                │
│  │   Anthropic Claude           │                │
│  │   Mock (regex)               │                │
│  └───────────────┬──────────────┘                │
│                  │                               │
│  ┌───────────────▼──────────────┐                │
│  │       Data Validator         │                │
│  │  Validation types & formats  │                │
│  │  Score de confiance          │                │
│  └───────────────┬──────────────┘                │
└──────────────────┼──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│                  EXPORT                          │
│         JSON complet │ JSON simple │ CSV         │
└─────────────────────────────────────────────────┘
```

---

## 3. Stack technique

| Composant | Technologie | Version |
|---|---|---|
| Interface | Streamlit | 1.35.0 |
| Extraction PDF | pdfplumber | 0.11.0 |
| Extraction PDF fallback | PyPDF2 | 3.0.1 |
| OCR Image | Tesseract | - |
| OCR Python | pytesseract | 0.3.10 |
| Traitement image | Pillow | 10.4.0 |
| IA principale | Groq LLaMA3-70b | - |
| IA alternative | Anthropic Claude | - |
| Validation schéma | jsonschema | 4.22.0 |
| Export données | pandas | 2.2.2 |
| Config | python-dotenv | 1.0.1 |
| Tests | pytest | - |

---

## 4. Structure du projet
```
PROJET-13-AI/
├── main.py                      # Application Streamlit principale
├── requirements.txt             # Dépendances Python
├── .env                         # Variables d'environnement (non pushé)
├── .env.example                 # Modèle de configuration
├── .gitignore                   # Fichiers exclus de Git
├── JOURNAL.md                   # Journal de développement
├── README.md                    # Documentation publique
├── SPEC.md                      # Specifications techniques (ce fichier)
├── cli.py                       # Interface ligne de commande
├── app/
│   ├── config.py                # Configuration centralisée
│   ├── database.py              # Historique SQLite
│   ├── extractor/
│   │   ├── pdf_extractor.py     # Extraction PDF
│   │   ├── image_extractor.py   # OCR image
│   │   ├── ai_extractor.py      # Extraction IA
│   │   └── schema_manager.py    # Gestion schémas JSON
│   ├── validator/
│   │   └── data_validator.py    # Validation + score confiance
│   └── ui/
│       └── components.py        # Composants UI réutilisables
│
├── schemas/                     # Schémas JSON personnalisés
└── tests/
    ├── test_validator.py        # Tests validation
    ├── test_extractor.py        # Tests extraction
    └── test_schema.py           # Tests schémas
```
    
│   
```

---

## 5. Flux de données
```
1. UPLOAD
   Utilisateur uploade un fichier (PDF / TXT / PNG / JPG)
        ↓
2. EXTRACTION BRUTE
   PDF  → pdfplumber → texte + tableaux + métadonnées
          (fallback PyPDF2 si échec)
   TXT  → lecture directe UTF-8
   IMG  → prétraitement (gris + contraste + netteté)
          → Tesseract OCR → texte + score confiance
        ↓
3. EXTRACTION IA
   Texte brut + Schéma JSON → Prompt → Groq LLaMA3
   Réponse → parsing JSON → champs extraits + scores
        ↓
4. VALIDATION
   Chaque champ → vérification type + format + contraintes
   Attribution statut : high / medium / low / invalid / missing
        ↓
5. CORRECTION MANUELLE
   Utilisateur révise les champs douteux dans l'interface
        ↓
6. EXPORT
   JSON complet (avec métadonnées)
   JSON simplifié (data only)
   CSV (tableau)
```

---

## 6. Format de sortie JSON
```json
{
  "metadata": {
    "overall_confidence": 0.88,
    "total_fields": 8,
    "extracted_count": 7,
    "valid_count": 6
  },
  "data": {
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean@email.com",
    "telephone": "06 12 34 56 78"
  },
  "details": {
    "nom": {
      "value": "Dupont",
      "confidence": 0.95,
      "status": "high_confidence",
      "is_valid": true,
      "manually_corrected": false
    }
  }
}
```

---

## 7. Score de confiance

| Score | Statut | Couleur | Action |
|---|---|---|---|
| 0.9 → 1.0 | high_confidence | Vert | Aucune |
| 0.7 → 0.9 | medium_confidence |  Jaune | Vérifier |
| 0.0 → 0.7 | low_confidence |  Rouge | Corriger |
| - | invalid | Rouge vif | Format incorrect |
| - | missing | Gris | Champ absent |

Seuil de révision : **0.7** — en dessous, le champ est signalé pour intervention humaine.

---

## 8. Schémas JSON supportés

### Formulaire générique
nom, prénom, date_naissance, email, téléphone, adresse, ville, code_postal

### Facture
numero_facture, date_facture, nom_client, montant_ht, tva, montant_ttc, iban

### Formulaire médical
nom_patient, date_naissance, numero_secu, medecin, date_consultation, diagnostic, traitement, allergies

### Schéma personnalisé
L'utilisateur peut définir ses propres champs via l'éditeur JSON intégré.

---

## 9. Sécurité

- Clés API stockées dans `.env` — jamais pushées sur GitHub
- `.env` listé dans `.gitignore`
- Champs password masqués dans l'interface
- `.env.example` fourni comme modèle sans vraies clés

---

## 10. Scope négatif

-  Pas de base de données
-  Pas de traitement de manuscrits illisibles
-  Pas de reconnaissance de tableaux multi-niveaux
-  Pas d'intégration temps réel avec systèmes externes
-  Pas de génération de valeurs manquantes (null si absent)
-  Pas d'authentification utilisateur
## 11. Historique des extractions (SQLite)

- Stockage automatique de chaque extraction
- Table : id, date, fichier, schema, total_champs, detectes, valides, fiabilite, donnees
- Statistiques visuelles : fiabilité par extraction, détectés vs valides
- Recherche par fichier ou schéma
- Export CSV de l'historique
- Suppression individuelle ou totale
## 12. CLI — Interface ligne de commande

L'application est accessible via deux interfaces :

**Interface web** (Streamlit) :
```bash
streamlit run main.py
```

**Interface CLI** :
```bash
python cli.py --file FACTURE.txt --schema Facture
```

### Arguments CLI
- `--file` → chemin du fichier à analyser (PDF ou TXT)
- `--schema` → schéma JSON à utiliser
- `--output` → fichier de sortie (défaut: result.json)
- `--format` → format de sortie json ou csv

### Avantages CLI
- Automatisation dans des scripts
- Intégration dans des pipelines
- Utilisation sans navigateur