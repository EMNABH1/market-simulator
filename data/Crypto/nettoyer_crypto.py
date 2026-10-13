from pathlib import Path

import pandas as pd

DOSSIER = Path(__file__).resolve().parent
dossier_traite = DOSSIER / "processed"
dossier_traite.mkdir(exist_ok=True)

ACTIFS = ["bitcoin", "ethereum", "solana", "dogecoin"]

for nom in ACTIFS:
    print(f"--- {nom} ---")
    df = pd.read_csv(DOSSIER / f"{nom}_brut.csv", index_col="date", parse_dates=True)

    df = df.sort_index()
    df = df[~df.index.duplicated(keep="first")]

    sans_cloture = int(df["Close"].isna().sum())
    df = df.dropna(subset=["Close"])
    print("Lignes supprimées (Close manquant) :", sans_cloture)

    # Week-ends conservés : le marché crypto est ouvert 7j/7

    # Jours sans vraie activité : prix totalement figé ET volume zéro
    fige = (df["Open"] == df["High"]) & (df["High"] == df["Low"]) & (df["Low"] == df["Close"])
    sans_seance = fige & (df["Volume"] == 0)
    print("Lignes supprimées (prix figé + volume 0) :", int(sans_seance.sum()))
    df = df[~sans_seance]

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    sortie = dossier_traite / f"{nom}_propre.csv"
    df.to_csv(sortie)
    print(len(df), "lignes dans", sortie)