from contextlib import asynccontextmanager
from datetime import date
from typing import Literal

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from . import moteur


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
    quantite: int = Field(gt=0)


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
    return {"message": message, "symbole": demande.symbole, "sens": demande.sens,
            "quantite": demande.quantite, "prix": prix, "sim_date": date_sim.strftime("%Y-%m-%d")}


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