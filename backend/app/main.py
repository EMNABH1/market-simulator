from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from . import formation, moteur


@asynccontextmanager
async def lifespan(_app: FastAPI):
    moteur.init_db()
    yield


app = FastAPI(title="Simulateur de Salle de Marché", lifespan=lifespan)

# Autorise le frontend à appeler cette API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FICHIERS = moteur.FICHIERS
NOMS = {
    "GC=F": "Or",
    "CL=F": "Pétrole WTI",
    "SI=F": "Argent",
    "HG=F": "Cuivre (HG=F) · USD/lb",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum",
    "SOL-USD": "Solana",
    "DOGE-USD": "Dogecoin",
}
bearer = HTTPBearer(auto_error=False)


class Identifiants(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=1024)


class DemandeAvancement(BaseModel):
    jours: Literal[1, 7, 30]


class DemandeOrdre(BaseModel):
    symbole: str
    sens: Literal["ACHAT", "VENTE"]
    quantite: float = Field(gt=0)


class ReponsesQuiz(BaseModel):
    reponses: list[int] = Field(min_length=10, max_length=10)


def utilisateur_connecte(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentification requise")
    user_id = moteur.utilisateur_du_jeton(credentials.credentials)
    utilisateur = moteur.obtenir_utilisateur(user_id) if user_id is not None else None
    if utilisateur is None:
        raise HTTPException(status_code=401, detail="Jeton invalide")
    return utilisateur


def _acces_cours(cours_id: str, user_id: int):
    cours_info = formation.COURS_PAR_ID.get(cours_id)
    if cours_info is None:
        raise HTTPException(status_code=404, detail="Cours inconnu")
    niveau, cours = cours_info
    cours_progression, niveau_progression = moteur.progression_formation(user_id)
    index_niveau = next(
        index for index, item in enumerate(formation.NIVEAUX) if item["id"] == niveau["id"]
    )
    if any(
        not niveau_progression.get(formation.NIVEAUX[index]["id"], {}).get("reussi")
        for index in range(index_niveau)
    ):
        raise HTTPException(status_code=403, detail="Réussissez le quiz du niveau précédent pour continuer")
    index_cours = next(index for index, item in enumerate(niveau["cours"]) if item["id"] == cours_id)
    if any(
        not cours_progression.get(niveau["cours"][index]["id"], {}).get("reussi")
        for index in range(index_cours)
    ):
        raise HTTPException(status_code=403, detail="Réussissez le quiz du cours précédent pour continuer")
    return niveau, cours, cours_progression, niveau_progression


def _acces_quiz_niveau(niveau_id: str, user_id: int):
    niveau = formation.NIVEAUX_PAR_ID.get(niveau_id)
    if niveau is None:
        raise HTTPException(status_code=404, detail="Niveau inconnu")
    _, niveau_progression = moteur.progression_formation(user_id)
    index_niveau = next(
        index for index, item in enumerate(formation.NIVEAUX) if item["id"] == niveau_id
    )
    if any(
        not niveau_progression.get(formation.NIVEAUX[index]["id"], {}).get("reussi")
        for index in range(index_niveau)
    ):
        raise HTTPException(status_code=403, detail="Réussissez le quiz du niveau précédent pour continuer")
    cours_progression, _ = moteur.progression_formation(user_id)
    if any(not cours_progression.get(cours["id"], {}).get("reussi") for cours in niveau["cours"]):
        raise HTTPException(status_code=403, detail="Terminez tous les cours du niveau avant son quiz")
    return niveau


@app.get("/api/formation")
def etat_formation(utilisateur: dict = Depends(utilisateur_connecte)):
    cours_progression, niveau_progression = moteur.progression_formation(utilisateur["id"])
    niveau_actif = next(
        (
            niveau for niveau in formation.NIVEAUX
            if not niveau_progression.get(niveau["id"], {}).get("reussi")
        ),
        None,
    )
    resultats_niveaux = []
    for index_niveau, niveau in enumerate(formation.NIVEAUX):
        niveau_debloque = all(
            niveau_progression.get(previous["id"], {}).get("reussi")
            for previous in formation.NIVEAUX[:index_niveau]
        )
        cours_resultats = []
        for index, cours in enumerate(niveau["cours"]):
            etat = cours_progression.get(cours["id"], {})
            prerequis_reussis = all(
                cours_progression.get(niveau["cours"][previous]["id"], {}).get("reussi")
                for previous in range(index)
            )
            disponible = niveau_debloque and prerequis_reussis
            cours_resultats.append(
                {
                    "id": cours["id"],
                    "titre": cours["titre"],
                    "resume": cours["resume"],
                    "etudie": bool(etat.get("etudie")),
                    "score": etat.get("meilleur_score"),
                    "reussi": bool(etat.get("reussi")),
                    "disponible": disponible,
                }
            )
        niveau_etat = niveau_progression.get(niveau["id"], {})
        quiz_disponible = (
            niveau_debloque
            and all(cours_progression.get(cours["id"], {}).get("reussi") for cours in niveau["cours"])
            and not bool(niveau_etat.get("reussi"))
        )
        resultats_niveaux.append(
            {
                "id": niveau["id"],
                "nom": niveau["nom"],
                "description": niveau["description"],
                "cours": cours_resultats,
                "quiz_disponible": quiz_disponible,
                "quiz_score": niveau_etat.get("meilleur_score"),
                "quiz_reussi": bool(niveau_etat.get("reussi")),
            }
        )
    cours_actuel = None
    if niveau_actif is not None:
        cours_actuel = next(
            (
                cours["id"] for cours in niveau_actif["cours"]
                if not cours_progression.get(cours["id"], {}).get("reussi")
            ),
            None,
        )
    return {
        "seuil_reussite": formation.SEUIL_REUSSITE,
        "note_maximale": 10,
        "niveau_actif": niveau_actif["id"] if niveau_actif else None,
        "cours_actuel": cours_actuel,
        "niveaux": resultats_niveaux,
    }


@app.get("/api/formation/cours/{cours_id}")
def lire_cours(cours_id: str, utilisateur: dict = Depends(utilisateur_connecte)):
    niveau, cours, cours_progression, _ = _acces_cours(cours_id, utilisateur["id"])
    etat = cours_progression.get(cours_id, {})
    return {
        "id": cours["id"],
        "titre": cours["titre"],
        "niveau": niveau["nom"],
        "resume": cours["resume"],
        "objectifs": cours["objectifs"],
        "sections": cours["sections"],
        "reflexe": cours["reflexe"],
        "etudie": bool(etat.get("etudie")),
        "score": etat.get("meilleur_score"),
        "reussi": bool(etat.get("reussi")),
        "quiz": formation.questions_publiques(cours["quiz"]) if etat.get("etudie") else [],
    }


@app.post("/api/formation/cours/{cours_id}/etudier")
def etudier_cours(cours_id: str, utilisateur: dict = Depends(utilisateur_connecte)):
    _acces_cours(cours_id, utilisateur["id"])
    moteur.marquer_cours_etudie(utilisateur["id"], cours_id)
    return {"cours_id": cours_id, "etudie": True}


@app.post("/api/formation/cours/{cours_id}/quiz")
def quiz_cours(
    cours_id: str,
    demande: ReponsesQuiz,
    utilisateur: dict = Depends(utilisateur_connecte),
):
    _, cours, cours_progression, _ = _acces_cours(cours_id, utilisateur["id"])
    if not cours_progression.get(cours_id, {}).get("etudie"):
        raise HTTPException(status_code=403, detail="Marquez le cours comme étudié avant de passer son quiz")
    score = formation.noter(cours["quiz"], demande.reponses)
    if score is None:
        raise HTTPException(status_code=422, detail="Les réponses du quiz sont invalides")
    reussi = moteur.enregistrer_score_cours(
        utilisateur["id"], cours_id, score, formation.SEUIL_REUSSITE
    )
    return {
        "cours_id": cours_id,
        "score": score,
        "note_maximale": 10,
        "seuil_reussite": formation.SEUIL_REUSSITE,
        "reussi": reussi,
        "correction": formation.corriger(cours["quiz"], demande.reponses),
    }


@app.get("/api/formation/niveaux/{niveau_id}/quiz")
def lire_quiz_niveau(niveau_id: str, utilisateur: dict = Depends(utilisateur_connecte)):
    niveau = _acces_quiz_niveau(niveau_id, utilisateur["id"])
    _, progression_niveaux = moteur.progression_formation(utilisateur["id"])
    if progression_niveaux.get(niveau_id, {}).get("reussi"):
        raise HTTPException(status_code=409, detail="Ce niveau est déjà validé")
    return {
        "niveau_id": niveau_id,
        "nom": niveau["nom"],
        "quiz": formation.questions_publiques(niveau["quiz"]),
    }


@app.post("/api/formation/niveaux/{niveau_id}/quiz")
def quiz_niveau(
    niveau_id: str,
    demande: ReponsesQuiz,
    utilisateur: dict = Depends(utilisateur_connecte),
):
    niveau = _acces_quiz_niveau(niveau_id, utilisateur["id"])
    score = formation.noter(niveau["quiz"], demande.reponses)
    if score is None:
        raise HTTPException(status_code=422, detail="Les réponses du quiz sont invalides")
    reussi = moteur.enregistrer_score_niveau(
        utilisateur["id"], niveau_id, score, formation.SEUIL_REUSSITE
    )
    return {
        "niveau_id": niveau_id,
        "score": score,
        "note_maximale": 10,
        "seuil_reussite": formation.SEUIL_REUSSITE,
        "reussi": reussi,
        "correction": formation.corriger(niveau["quiz"], demande.reponses),
    }


def charger(symbole: str) -> pd.DataFrame:
    if symbole not in FICHIERS:
        raise HTTPException(status_code=404, detail="Symbole inconnu")
    chemin = moteur.chemin_actif(symbole)
    if chemin is None or not chemin.is_file():
        raise HTTPException(status_code=404, detail="Données de l'actif indisponibles")
    return pd.read_csv(chemin, index_col="date", parse_dates=True)


@app.get("/api/actifs")
def actifs():
    return [{"symbole": symbole, "nom": NOMS[symbole]} for symbole in FICHIERS]


@app.get("/api/marches")
def marches(_utilisateur: dict = Depends(utilisateur_connecte)):
    disponibles = moteur.charger_actifs()
    return [
        {
            "id": id_marche,
            "nom": m["nom"],
            "description": m["description"],
            "disponible": any(s in disponibles for s in m["actifs"]),
            "actifs": [{"symbole": s, "nom": NOMS[s]} for s in m["actifs"]],
        }
        for id_marche, m in moteur.MARCHES.items()
    ]


@app.post("/api/marches/{id_marche}/choisir")
def choisir_marche(id_marche: str, utilisateur: dict = Depends(utilisateur_connecte)):
    """Si la date simulée précède le début des données du marché, on l'avance (jamais en arrière)."""
    if id_marche not in moteur.MARCHES:
        raise HTTPException(status_code=404, detail="Marché inconnu")
    actifs_marche = moteur.charger_actifs(marche=id_marche)
    if not actifs_marche:
        raise HTTPException(status_code=503, detail="Aucune donnée disponible pour ce marché")
    depart = pd.Timestamp(moteur.date_debut(actifs_marche))
    date_actuelle = pd.Timestamp(utilisateur["sim_date"])
    if date_actuelle < depart:
        moteur.definir_date(utilisateur["id"], depart.date())
        date_actuelle = depart
    return {"marche": id_marche, "sim_date": date_actuelle.strftime("%Y-%m-%d")}


@app.get("/api/prix/{symbole}")
def prix(symbole: str, jours: int = 90, jusqua: date | None = None):
    df = charger(symbole)
    if jusqua is not None:
        df = df.loc[:jusqua.isoformat()]
    df = df.tail(jours)
    return [
        {
            "time": d.strftime("%Y-%m-%d"),
            "open": float(r["Open"]),
            "high": float(r["High"]),
            "low": float(r["Low"]),
            "close": float(r["Close"]),
            "volume": int(r["Volume"]) if pd.notna(r["Volume"]) else 0,
        }
        for d, r in df.iterrows()
    ]


@app.get("/api/resume/{symbole}")
def resume(symbole: str, jusqua: date | None = None):
    df = charger(symbole)
    if jusqua is not None:
        df = df.loc[:jusqua.isoformat()]
    if df.empty:
        raise HTTPException(status_code=404, detail="Aucune donnée à cette date")
    dernier = float(df["Close"].iloc[-1])
    precedent = float(df["Close"].iloc[-2]) if len(df) > 1 else dernier
    return {
        "symbole": symbole,
        "dernier": dernier,
        "variation": dernier - precedent,
        "variation_pct": (dernier - precedent) / precedent * 100,
        "date": df.index[-1].strftime("%Y-%m-%d"),
    }


@app.get("/api/stats/{symbole}")
def stats(symbole: str, jusqua: date | None = None):
    df = charger(symbole)
    if jusqua is not None:
        df = df.loc[:jusqua.isoformat()]
    if df.empty:
        raise HTTPException(status_code=404, detail="Aucune donnée à cette date")
    close = df["Close"]
    rendements = close.pct_change()
    var_1m = float((close.iloc[-1] / close.iloc[-22] - 1) * 100) if len(close) >= 22 else None
    var_1an = float((close.iloc[-1] / close.iloc[-253] - 1) * 100) if len(close) >= 253 else None
    rendements_valides = rendements.dropna().tail(20)
    volatilite = float(rendements_valides.std() * 100) if len(rendements_valides) >= 2 else None
    return {
        "dernier": float(close.iloc[-1]),
        "haut_1an": float(df["High"].tail(252).max()),
        "bas_1an": float(df["Low"].tail(252).min()),
        "var_1m_pct": var_1m,
        "var_1an_pct": var_1an,
        "vol_20j_pct": volatilite,
        "premiere_date": df.index[0].strftime("%Y-%m-%d"),
        "derniere_date": df.index[-1].strftime("%Y-%m-%d"),
        "nb_jours": int(len(df)),
    }


@app.post("/api/auth/inscription", status_code=201)
def inscription(identifiants: Identifiants):
    actifs_charges = moteur.charger_actifs()
    if not actifs_charges:
        raise HTTPException(status_code=503, detail="Aucune donnée d'actif disponible")
    ok, message = moteur.creer_compte(
        identifiants.username,
        identifiants.password,
        moteur.date_debut(actifs_charges),
    )
    if not ok:
        raise HTTPException(status_code=409, detail=message)
    return {"message": message}


@app.post("/api/auth/connexion")
def connexion(identifiants: Identifiants):
    user_id = moteur.authentifier(identifiants.username, identifiants.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    return {"access_token": moteur.creer_jeton(user_id), "token_type": "bearer"}


@app.get("/api/moi")
def moi(utilisateur: dict = Depends(utilisateur_connecte)):
    return utilisateur


@app.post("/api/simulation/avancer")
def avancer(
    demande: DemandeAvancement,
    utilisateur: dict = Depends(utilisateur_connecte),
):
    actifs_charges = moteur.charger_actifs()
    if not actifs_charges:
        raise HTTPException(status_code=503, detail="Aucune donnée d'actif disponible")
    date_actuelle = pd.Timestamp(utilisateur["sim_date"])
    nouvelle_date = date_actuelle + pd.Timedelta(days=demande.jours)
    limite = pd.Timestamp(moteur.date_fin(actifs_charges))
    if nouvelle_date > limite:
        raise HTTPException(status_code=400, detail="La période demandée dépasse la fin des données disponibles")
    moteur.definir_date(utilisateur["id"], nouvelle_date.date())
    return {"sim_date": nouvelle_date.strftime("%Y-%m-%d"), "jours": demande.jours}


@app.post("/api/ordres", status_code=201)
def creer_ordre(
    demande: DemandeOrdre,
    utilisateur: dict = Depends(utilisateur_connecte),
):
    if demande.symbole not in FICHIERS:
        raise HTTPException(status_code=404, detail="Symbole inconnu")
    actifs_charges = moteur.charger_actifs()
    serie = actifs_charges.get(demande.symbole)
    if serie is None:
        raise HTTPException(status_code=404, detail="Données de l'actif indisponibles")
    date_sim = pd.Timestamp(utilisateur["sim_date"])
    prix = moteur.prix_a_date(serie, date_sim)
    ok, message = moteur.passer_ordre(
        utilisateur["id"],
        demande.symbole,
        demande.sens,
        demande.quantite,
        prix,
        date_sim,
    )
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {
        "message": message,
        "symbole": demande.symbole,
        "sens": demande.sens,
        "quantite": demande.quantite,
        "prix": prix,
        "sim_date": date_sim.strftime("%Y-%m-%d"),
    }


@app.get("/api/ordres")
def ordres(utilisateur: dict = Depends(utilisateur_connecte)):
    return moteur.lire_ordres(utilisateur["id"]).to_dict(orient="records")


@app.get("/api/portefeuille")
def portefeuille(utilisateur: dict = Depends(utilisateur_connecte)):
    actifs_charges = moteur.charger_actifs()
    table_ordres = moteur.lire_ordres(utilisateur["id"])
    positions = moteur.positions(table_ordres)
    lignes = moteur.tableau_positions(positions, actifs_charges, utilisateur["sim_date"])
    positions_json = lignes.to_dict(orient="records")
    valeur_positions = float(lignes["Valeur"].sum())
    return {
        "sim_date": utilisateur["sim_date"],
        "liquidites": utilisateur["cash"],
        "positions": positions_json,
        "valeur_positions": valeur_positions,
        "valeur_totale": round(utilisateur["cash"] + valeur_positions, 2),
    }