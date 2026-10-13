import pandas as pd
from pathlib import Path

df = pd.read_csv("or_brut.csv", index_col="date", parse_dates=True)

df = df.sort_index()
df = df[~df.index.duplicated(keep="first")]

# Jours sans vraie séance : prix totalement figé ET volume zéro
fige = (df["Open"] == df["High"]) & (df["High"] == df["Low"]) & (df["Low"] == df["Close"])
print("Lignes supprimées (prix figé + volume 0) :", int((fige & (df["Volume"] == 0)).sum()))
df = df[~(fige & (df["Volume"] == 0))]

# Le volume n'est comparable qu'à partir de 2020
df["volume_fiable"] = df.index.year >= 2020

Path("processed").mkdir(exist_ok=True)
df.to_csv("processed/or_propre.csv")
print(len(df), "lignes dans or_propre.csv")