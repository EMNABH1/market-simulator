import yfinance as yf

df = yf.download("GC=F", start="2012-01-01", auto_adjust=False, progress=False)
df.columns = df.columns.get_level_values(0)
df = df[["Open", "High", "Low", "Close", "Volume"]]
df.index.name = "date"
df.to_csv("or_brut.csv")
print(len(df), "lignes sauvegardées")