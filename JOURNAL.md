# 📓 Journal de Développement — Projet 13 : FormExtract AI

## Partie 1 — Initialisation du projet
**Date :** 05/03/2026  
**Durée :** ~1h  

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