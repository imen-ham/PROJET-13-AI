#  Journal de Développement — Projet 13 : FormExtract AI

## Partie 1 — Initialisation du projet
**Date :** 05/03/2026  
 

### Ce qui a été fait
- Création de la structure complète du projet
- Configuration de l'environnement virtuel Python 3.11
- Installation des dépendances (requirements.txt)
- Configuration initiale (.env, config.py)

### Difficultés rencontrées
- Incompatibilité Python 3.14 avec Pillow → résolu en installant Python 3.11
- Erreur proxies avec groq==0.9.0 → résolu en upgrading vers groq==0.11.0

### Choix techniques
- Python 3.11 pour compatibilité maximale
- Structure modulaire app/extractor, app/validator, app/ui
- Mode mock pour tester sans clé API

### Prochaine étape
- Implémenter les modules d'extraction PDF, TXT et image
---

## Partie 2 — Extraction de documents
**Date :** 07/03/2026  


### Ce qui a été fait
- Implémentation PDFExtractor avec pdfplumber + PyPDF2 en fallback
- Implémentation ImageExtractor avec OCR Tesseract
- Gestion des formats supportés : PDF, TXT, PNG, JPG
- Prétraitement des images pour améliorer la qualité OCR

### Difficultés rencontrées
- Certains PDFs non lisibles par pdfplumber → fallback PyPDF2
- Qualité OCR variable selon les images → ajout prétraitement contraste/sharpen

### Choix techniques
- Double librairie PDF pour robustesse maximale
- Prétraitement image automatique avant OCR
- Extraction des métadonnées PDF en plus du texte

### Prochaine étape
- Intégration de l'IA pour extraction contextuelle des champs

## Partie 3 — Intégration IA
**Date :** 09/03/2026  


### Ce qui a été fait
- Implémentation AIExtractor avec support Groq, Anthropic et Mock
- Création SchemaManager avec 3 schémas prédéfinis (générique, facture, médical)
- Prompt engineering pour extraction structurée en JSON
- Parsing robuste des réponses JSON de l'IA
- Sécurisation des clés API dans l'interface

### Difficultés rencontrées
- Parsing JSON instable → ajout nettoyage regex
- Incompatibilité groq==0.9.0 → résolu avec groq==0.11.0 + httpx==0.27.0
- Clé API visible dans l'interface → masquage avec placeholder

### Choix techniques
- Groq LLaMA3-70b : gratuit, rapide et précis
- Mode mock pour démo sans clé API
- JSON Schema comme contrat d'extraction

### Prochaine étape
- Implémenter la validation des données et scores de confiance
---

## Partie 4 — Validation des données
**Date :** 11/03/2026  

### Ce qui a été fait
- Implémentation DataValidator avec validation par type et format
- Validation email, date, nombre et pattern regex
- Score de confiance par champ (0.0 à 1.0)
- Détection automatique des champs obligatoires manquants
- Statuts : high_confidence, medium_confidence, low_confidence, invalid, missing

### Difficultés rencontrées
- Formats de dates multiples à gérer (DD/MM/YYYY, YYYY-MM-DD, DD.MM.YYYY...)
- Définir des seuils de confiance pertinents et compréhensibles

### Choix techniques
- Seuil de confiance à 0.7 pour déclencher une révision manuelle
- Support de 5 formats de dates différents
- Enrichissement des données avec métadonnées de validation

### Prochaine étape
- Développer l'interface Streamlit complète avec les composants UI
---

## Partie 5 — Interface Streamlit
**Date :** 15/03/2026  


### Ce qui a été fait
- Développement interface Streamlit complète avec thème clair pastel
- 4 onglets : Upload & Analyse, Schéma, Résultats & Correction, Export
- Sidebar avec statut du système et guide rapide
- Composants UI réutilisables (badges confiance, metric cards, header)
- Correction du chemin Tesseract OCR pour Windows
- Tests avec fichiers TXT et factures

### Difficultés rencontrées
- Tesseract non installé sur certains PC → ajout chemin explicite
- Modèle Groq llama3-70b-8192 déprécié → migration vers llama-3.3-70b-versatile
- Thème CSS personnalisé pour look professionnel et neutre

### Choix techniques
- Thème pastel bleu clair pour interface professionnelle
- Session state Streamlit pour persister les données entre onglets

### Prochaine étape
- Finalisation : README, SPEC, tests unitaires
---

## Partie 6 — Finalisation du projet
**Date :** 15/03/2026 
### Ce qui a été fait
- Rédaction du README complet avec guide d'installation
- Rédaction des specifications techniques (SPEC.md)
- Implémentation de 34 tests unitaires (pytest)
- Tests validation email, date, nombre, champs obligatoires
- Tests extraction schémas et parsing JSON
- Vérification complète du projet end-to-end

### Difficultés rencontrées
- Adaptation des tests au mode mock sans clé API
- Organisation des tests par module pour plus de clarté

### Choix techniques
- pytest comme framework de test standard Python
- 3 fichiers de tests séparés par module
- SPEC.md pour documenter l'architecture technique complète

### Bilan du projet
- 6 parties développées sur 10 jours
- Application complète et fonctionnelle
- 34 tests unitaires passés avec succès
- Interface professionnelle et intuitive
---

## Partie 7 — Historique des extractions (SQLite)
**Date :** 17/03/2026    

### Ce qui a été fait
- Ajout base de données SQLite pour stocker l'historique
- Nouveau module app/database.py
- Onglet Historique avec métriques globales
- Tableau de toutes les extractions passées
- Possibilité de voir les détails, supprimer ou vider l'historique

### Choix techniques
- SQLite : léger, sans configuration, intégré à Python
- Stockage JSON des données extraites dans la BDD
---

## Partie 8 — Statistiques visuelles et recherche
**Date :** 17/03/2026  
### Ce qui a été fait
- Ajout de 2 graphiques dans l'onglet Historique
- Graphique fiabilité par extraction (%)
- Graphique champs détectés vs valides
- Barre de recherche dans l'historique (par fichier ou schéma)
- Export CSV de l'historique filtré

### Choix techniques
- st.bar_chart() de Streamlit pour les graphiques
- Filtrage pandas sur le DataFrame de l'historique
---

## Partie 9 — CLI (Command Line Interface)
**Date :** 17/03/2026  
 
### Ce qui a été fait
- Création de cli.py pour extraction en ligne de commande
- Support fichiers TXT et PDF
- Affichage résultats dans le terminal
- Export JSON et CSV depuis la CLI
- Arguments : --file, --schema, --output, --format

### Utilisation
python cli.py --file FACTURE.txt --schema Facture
