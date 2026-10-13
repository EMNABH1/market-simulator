from pathlib import Path

import pandas as pd

DOSSIER = Path(__file__).resolve().parent
df = pd.read_csv(DOSSIER / "cuivre_brut.csv", index_col="date", parse_dates=True)

df = df.sort_index()
df = df[~df.index.duplicated(keep="first")]

sans_cloture = int(df["Close"].isna().sum())
df = df.dropna(subset=["Close"])
print("Lignes supprimées (Close manquant) :", sans_cloture)

weekend = df.index.dayofweek >= 5
print("Lignes supprimées (week-end) :", int(weekend.sum()))
df = df[~weekend]

# Jours sans vraie séance : prix totalement figé ET volume zéro
fige = (df["Open"] == df["High"]) & (df["High"] == df["Low"]) & (df["Low"] == df["Close"])
sans_seance = fige & (df["Volume"] == 0)
print("Lignes supprimées (prix figé + volume 0) :", int(sans_seance.sum()))
df = df[~sans_seance]

df = df[["Open", "High", "Low", "Close", "Volume"]]
dossier_traite = DOSSIER / "processed"
dossier_traite.mkdir(exist_ok=True)
sortie = dossier_traite / "cuivre_propre.csv"
df.to_csv(sortie)
print(len(df), "lignes dans", sortie)