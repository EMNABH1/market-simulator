from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Simulateur de Salle de Marché")

# Autorise le frontend à appeler cette API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DOSSIER = Path(__file__).resolve().parents[2] / "data" / "processed"
FICHIERS = {"GC=F": "or_propre.csv"}


def charger(symbole: str) -> pd.DataFrame:
    if symbole not in FICHIERS:
        raise HTTPException(status_code=404, detail="Symbole inconnu")
    return pd.read_csv(DOSSIER / FICHIERS[symbole], index_col="date", parse_dates=True)


@app.get("/api/prix/{symbole}")
def prix(symbole: str, jours: int = 90):
    df = charger(symbole).tail(jours)
    return [
        {
            "time": d.strftime("%Y-%m-%d"),
            "open": float(r["Open"]),
            "high": float(r["High"]),
            "low": float(r["Low"]),
            "close": float(r["Close"]),
        }
        for d, r in df.iterrows()
    ]


@app.get("/api/resume/{symbole}")
def resume(symbole: str):
    df = charger(symbole)
    dernier = float(df["Close"].iloc[-1])
    precedent = float(df["Close"].iloc[-2])
    return {
        "symbole": symbole,
        "dernier": dernier,
        "variation": dernier - precedent,
        "variation_pct": (dernier - precedent) / precedent * 100,
        "date": df.index[-1].strftime("%Y-%m-%d"),
    }


@app.get("/api/stats/{symbole}")
def stats(symbole: str):
    df = charger(symbole)
    close = df["Close"]
    rendements = close.pct_change()
    return {
        "dernier": float(close.iloc[-1]),
        "haut_1an": float(df["High"].tail(252).max()),
        "bas_1an": float(df["Low"].tail(252).min()),
        "var_1m_pct": float((close.iloc[-1] / close.iloc[-22] - 1) * 100),
        "var_1an_pct": float((close.iloc[-1] / close.iloc[-253] - 1) * 100),
        "vol_20j_pct": float(rendements.tail(20).std() * 100),
        "premiere_date": df.index[0].strftime("%Y-%m-%d"),
        "derniere_date": df.index[-1].strftime("%Y-%m-%d"),
        "nb_jours": int(len(df)),
    }