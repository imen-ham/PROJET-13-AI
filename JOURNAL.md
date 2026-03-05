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