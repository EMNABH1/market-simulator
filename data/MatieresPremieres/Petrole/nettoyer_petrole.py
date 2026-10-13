from pathlib import Path

import pandas as pd

DOSSIER = Path(__file__).resolve().parent
df = pd.read_csv(DOSSIER / "petrole_brut.csv", index_col="date", parse_dates=True)

df = df.sort_index()
df = df[~df.index.duplicated(keep="first")]

# Jours sans vraie séance : prix totalement figé ET volume zéro
fige = (df["Open"] == df["High"]) & (df["High"] == df["Low"]) & (df["Low"] == df["Close"])
print("Lignes supprimées (prix figé + volume 0) :", int((fige & (df["Volume"] == 0)).sum()))
df = df[~(fige & (df["Volume"] == 0))]

# Le volume n'est comparable qu'à partir de 2020
df["volume_fiable"] = df.index.year >= 2020
df["prix_non_positif"] = (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1)

dossier_traite = DOSSIER.parent / "processed"
dossier_traite.mkdir(exist_ok=True)
df.to_csv(dossier_traite / "petrole_propre.csv")
print(len(df), "lignes dans petrole_propre.csv")
print("Lignes avec un prix non positif :", int(df["prix_non_positif"].sum()))