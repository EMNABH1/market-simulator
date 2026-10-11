import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("processed/or_propre.csv", index_col="date", parse_dates=True)

df["rendement_1j"] = df["Close"].pct_change()
df["abs_rendement_1j"] = df["rendement_1j"].abs()
df["vol_5j"] = df["rendement_1j"].rolling(5).std()
df["vol_20j"] = df["rendement_1j"].rolling(20).std()
df["vol_60j"] = df["rendement_1j"].rolling(60).std()
df["amplitude_1j"] = (df["High"] - df["Low"]) / df["Close"]
df["cible"] = df["rendement_1j"].rolling(5).std().shift(-5)
df = df.iloc[:-5].dropna()

features = ["abs_rendement_1j", "vol_5j", "vol_20j", "vol_60j", "amplitude_1j"]
X, y = df[features], df["cible"]

tscv = TimeSeriesSplit(n_splits=5, gap=5)
for i, (tr, te) in enumerate(tscv.split(X), start=1):
    modele = LinearRegression().fit(X.iloc[tr], y.iloc[tr])
    mae_modele = mean_absolute_error(y.iloc[te], modele.predict(X.iloc[te]))
    mae_base = mean_absolute_error(y.iloc[te], X.iloc[te]["vol_20j"])
    gain = (1 - mae_modele / mae_base) * 100
    print(f"Découpage {i} : test {X.index[te[0]].date()} -> {X.index[te[-1]].date()}")
    print(f"   MAE baseline : {mae_base:.5f}   MAE modèle : {mae_modele:.5f}   gain : {gain:+.1f} %")