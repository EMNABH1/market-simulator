from pathlib import Path

import pandas as pd
import yfinance as yf

DOSSIER = Path(__file__).resolve().parent

ACTIFS = {
    "bitcoin": ("BTC-USD", "2014-09-17"),
    "ethereum": ("ETH-USD", "2017-11-09"),
    "solana": ("SOL-USD", "2020-04-10"),
    "dogecoin": ("DOGE-USD", "2017-11-09"),
}

for nom, (ticker, debut) in ACTIFS.items():
    df = yf.download(ticker, start=debut, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.index.name = "date"
    df.to_csv(DOSSIER / f"{nom}_brut.csv")
    print(nom, ":", len(df), "lignes sauvegardées")