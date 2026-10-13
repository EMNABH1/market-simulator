# Simulateur de Salle de Marché

Plateforme de simulation de trading avec IA, AI Stress Testing, XAI et module actuariat.
Projet Informatique Finance, ESPRIT, année universitaire 2026-2027.

## État actuel

Deux marchés sont disponibles avec des données réelles : les matières premières (or, pétrole, argent et cuivre) et les cryptomonnaies (Bitcoin, Ethereum, Solana et Dogecoin). Le site propose la sélection du marché, les cotations, le trading simulé et le portefeuille. Les modules risque, backtesting, IA et stress testing restent à intégrer.

## Stack

- Frontend : Next.js, TypeScript, Tailwind CSS, Lightweight Charts
- Backend : FastAPI (Python), pandas
- Données : Yahoo Finance (yfinance), scikit-learn pour les modèles

## Structure du dépôt

```
backend/            API FastAPI (app/main.py)
data/MatieresPremieres/Or/       scripts et modèles pour l'or
data/MatieresPremieres/Petrole/  scripts pétrole
data/MatieresPremieres/Argent/   scripts argent
data/MatieresPremieres/Cuivre/   scripts cuivre
data/Crypto/                     scripts pour quatre cryptomonnaies
data/**/processed/               CSV nettoyés (générés par les scripts, absents de GitHub)
frontend/           site Next.js
  src/components/   tableaux de bord, marchés, trading et portefeuille
```

## Lancer le projet

Prérequis : Python 3.11 ou plus et Node.js LTS. Les CSV ne sont pas sur GitHub ; téléchargez et nettoyez les données avant de démarrer l'API. Les commandes ci-dessous sont pour PowerShell, depuis la racine du dépôt.

### 1. Données

```
python -m venv data\venv
.\data\venv\Scripts\Activate.ps1
python -m pip install -r data\MatieresPremieres\Or\requirements.txt

Push-Location data\MatieresPremieres\Or
python telecharger_or.py
python nettoyer_or.py
Pop-Location

Push-Location data\MatieresPremieres\Petrole
python telecharger_petrole.py
python nettoyer_petrole.py
Pop-Location

Push-Location data\MatieresPremieres\Argent
python telecharger_argent.py
python nettoyer_argent.py
Pop-Location

Push-Location data\MatieresPremieres\Cuivre
python telecharger_cuivre.py
python nettoyer_cuivre.py
Pop-Location

Push-Location data\Crypto
python telecharger_crypto.py
python nettoyer_crypto.py
Pop-Location
```

Les scripts crypto récupèrent Bitcoin, Ethereum, Solana et Dogecoin. Les CSV nettoyés sont écrits sous `data\MatieresPremieres` et `data\Crypto` ; l'API les lit directement.

### 2. API (dans un second terminal)

```
Set-Location backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

L'API est disponible sur http://127.0.0.1:8000. Par exemple, http://127.0.0.1:8000/api/resume/GC=F affiche le dernier cours de l'or.

### 3. Site (dans un troisième terminal)

```
Set-Location frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000, puis créer un compte ou se connecter pour accéder au tableau de bord.

## Modèles de l'or (optionnel)

```
Set-Location data\MatieresPremieres\Or
python features_or.py
python entrainer_or.py
python volatilite_or.py
python evaluer_vol.py
python expliquer_vol.py
```

Résultat principal : la direction de l'or à 5 jours n'est pas prévisible avec les seuls indicateurs de prix (AUC moyenne d'environ 0,51), alors que la volatilité à 5 jours l'est modestement (gain moyen d'environ 7 % sur une règle simple).

## Workflow Git

- `main` : version intégrée, protégée. Une branche par fonctionnalité, créée depuis `main`.
- Intégration par Pull Request vers `main`, relue par un autre membre, après test (données, API, site).

## Source des données

Prix de l'or : Yahoo Finance, contrat à terme COMEX (GC=F), journalier depuis 2012. C'est un future, pas le prix spot : de petits sauts sont possibles au changement de contrat. Le volume n'est comparable qu'à partir de 2020. Les matières premières et cryptomonnaies sont également téléchargées depuis Yahoo Finance ; les scripts conservent l'historique disponible pour chaque symbole.