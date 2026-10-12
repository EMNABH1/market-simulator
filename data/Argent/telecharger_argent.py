from pathlib import Path

import pandas as pd
import yfinance as yf

DOSSIER = Path(__file__).resolve().parent

df = yf.download("SI=F", start="2005-01-01", auto_adjust=False, progress=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
df = df[["Open", "High", "Low", "Close", "Volume"]]
df.index.name = "date"
df.to_csv(DOSSIER / "argent_brut.csv")
print(len(df), "lignes sauvegardées")