# Simulateur de Salle de Marché

Plateforme de simulation de trading avec IA, AI Stress Testing, XAI et module actuariat.
Projet Informatique Finance, ESPRIT, année universitaire 2026-2027.

## État actuel

Seule la matière **or (GC=F)** est branchée sur de vraies données : statistiques, graphique en bougies, moyenne mobile. Les autres modules (trading, portefeuille, IA, stress testing) restent à intégrer.

## Stack

- Frontend : Next.js, TypeScript, Tailwind CSS, Lightweight Charts
- Backend : FastAPI (Python), pandas
- Données : Yahoo Finance (yfinance), scikit-learn pour les modèles

## Structure du dépôt

```
backend/            API FastAPI (app/main.py)
data/Or/            scripts de collecte, nettoyage, features et modèles pour l'or
data/processed/     CSV nettoyés (générés par les scripts, absents de GitHub)
frontend/           site Next.js
  src/components/   EnteteActif, PriceChart (génériques) et Or/ (blocs de l'or)
```

## Lancer le projet (données de l'or)

Les CSV ne sont pas sur GitHub : il faut d'abord les générer. Prérequis : Python 3.11 ou plus, Node.js LTS.

### 1. Données (depuis `data/Or`)

```
cd data/Or
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python telecharger_or.py
python nettoyer_or.py
```

`telecharger_or.py` crée `or_brut.csv`, puis `nettoyer_or.py` crée `data/processed/or_propre.csv`, que l'API lit.

### 2. API (depuis `backend`, dans un second terminal)

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Test : http://127.0.0.1:8000/api/resume/GC=F doit afficher le dernier prix de l'or.

### 3. Site (depuis `frontend`, dans un troisième terminal)

```
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000.

## Modèles de l'or (optionnel, depuis `data/Or`)

```
python features_or.py
python entrainer_or.py
python volatilite_or.py
python evaluer_vol.py
python expliquer_vol.py
```

Résultat principal : la direction de l'or à 5 jours n'est pas prévisible avec les seuls indicateurs de prix (AUC moyenne d'environ 0,51), alors que la volatilité à 5 jours l'est modestement (gain moyen d'environ 7 % sur une règle simple).

## Workflow Git

- `main` : version stable. `develop` : intégration. Une branche par fonctionnalité.
- Nom de branche et commits avec la clé Jira, par exemple `feature/SCRUM-5-donnees-or`.
- Intégration par Pull Request vers `develop`, relue par un autre membre.
- Ne jamais committer de fichier `.env`, de clé API ou de CSV.

## Source des données

Prix de l'or : Yahoo Finance, contrat à terme COMEX (GC=F), journalier depuis 2012. C'est un future, pas le prix spot : de petits sauts sont possibles au changement de contrat. Le volume n'est comparable qu'à partir de 2020.