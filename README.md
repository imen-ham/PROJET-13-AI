#  FormExtract AI — Projet 13

> Extracteur intelligent de données depuis des formulaires (PDF, TXT, Image)

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

##  Problématique

Dans un contexte professionnel, la saisie manuelle de données issues de formulaires
est chronophage et source d'erreurs. Ce projet automatise l'extraction, la validation
et l'export de ces données grâce à l'intelligence artificielle.

---

##  Fonctionnalités

-  **Upload** de formulaires PDF, TXT, PNG, JPG
-  **Extraction IA** via Groq (LLaMA3) ou Anthropic (Claude)
-  **Schémas JSON** personnalisables (formulaire, facture, médical...)
-  **Validation automatique** des données extraites
-  **Score de confiance** par champ extrait
-  **Correction manuelle** dans l'interface
-  **Export** JSON et CSV
-  **Mode démo** sans clé API
-  **Historique** des extractions avec SQLite
-  **Statistiques visuelles** (graphiques fiabilité, détectés vs valides)
-  **Recherche** dans l'historique par fichier ou schéma
-  **Export CSV** de l'historique
-  **CLI** — Extraction en ligne de commande sans interface graphique

---

##  Architecture
```
PROJET-13-AI/
├── app/
│   ├── extractor/
│   │   ├── pdf_extractor.py      # Extraction PDF
│   │   ├── image_extractor.py    # OCR Tesseract
│   │   ├── ai_extractor.py       # Extraction IA
│   │   └── schema_manager.py     # Gestion schémas
│   ├── validator/
│   │   └── data_validator.py     # Validation + confiance
│   ├── ui/
│   │   └── components.py         # Composants UI
│   └── config.py                 # Configuration
├── tests/
│   ├── test_validator.py         # Tests validation
│   ├── test_extractor.py         # Tests extraction
│   └── test_schema.py            # Tests schémas
├── schemas/                      # Schémas JSON
├── sample_forms/                 # Formulaires exemples
├── main.py                       # Application Streamlit
├── requirements.txt
├── .env.example
├── JOURNAL.md                    # Journal de développement
├── spec.md                       # Specifications techniques
├── cli.py                       # Interface ligne de commande
└── README.md

---

##  Installation

### 1. Cloner le projet
```bash
git clone https://github.com/imen-ham/PROJET-13-AI.git
cd PROJET-13-AI
```

### 2. Créer l'environnement virtuel
```bash
py -3.11 -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Édite .env avec ta clé API Groq
```

### 5. Lancer l'application
```bash
streamlit run main.py
```

---

##  Configuration API

| Provider | Gratuit | Lien |
|---|---|---|
| **Groq** |  Oui | https://console.groq.com |
| **Anthropic** |  Non | https://console.anthropic.com |
| **Mock** |  Oui | Aucune clé requise |

---

##  Schémas disponibles

| Schéma | Champs |
|---|---|
| Formulaire générique | nom, prénom, email, téléphone, adresse... |
| Facture | numéro, date, montant HT/TTC, IBAN... |
| Formulaire médical | patient, médecin, diagnostic, traitement... |

---

##  Technologies

- **Python 3.11**
- **Streamlit** — Interface utilisateur
- **pdfplumber / PyPDF2** — Extraction PDF
- **Tesseract OCR** — Extraction image
- **Groq API** — IA LLaMA3
- **JSON Schema** — Validation données

---
##  Utilisation CLI
```bash
# Extraction basique
python cli.py --file FACTURE.txt --schema Facture

# Avec export JSON
python cli.py --file formulaire.txt --schema "Formulaire générique" --output result.json

# Avec export CSV
python cli.py --file formulaire.pdf --schema Facture --output result.csv --format csv
```

### Arguments disponibles
| Argument | Description | Obligatoire |
|---|---|---|
| `--file` | Chemin vers le fichier |  |
| `--schema` | Schéma à utiliser |  (défaut: Formulaire générique) |
| `--output` | Fichier de sortie |  (défaut: result.json) |
| `--format` | Format de sortie (json/csv) |  (défaut: json) |
```

##  Journal de développement

Voir [JOURNAL.md](./JOURNAL.md) pour le détail de chaque partie.

---

##  Auteur

**imen-ham** — [GitHub](https://github.com/imen-ham)