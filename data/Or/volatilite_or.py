import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

df = pd.read_csv("processed/or_propre.csv", index_col="date", parse_dates=True)

# --- FEATURES (uniquement le passé) ---
df["rendement_1j"] = df["Close"].pct_change()
df["abs_rendement_1j"] = df["rendement_1j"].abs()
df["vol_5j"] = df["rendement_1j"].rolling(5).std()
df["vol_20j"] = df["rendement_1j"].rolling(20).std()
df["vol_60j"] = df["rendement_1j"].rolling(60).std()
df["amplitude_1j"] = (df["High"] - df["Low"]) / df["Close"]

# --- CIBLE : la volatilité des 5 prochains jours ---
df["cible"] = df["rendement_1j"].rolling(5).std().shift(-5)

df = df.iloc[:-5].dropna()

features = ["abs_rendement_1j", "vol_5j", "vol_20j", "vol_60j", "amplitude_1j"]
X, y = df[features], df["cible"]

# --- Découpage dans l'ordre du temps ---
train = df.index < "2024-01-01"
idx_train = X[train].index[:-5]          # on retire 5 lignes pour éviter la fuite
X_train, y_train = X.loc[idx_train], y.loc[idx_train]
X_test, y_test = X[~train], y[~train]

print("Train :", len(X_train), "lignes | Test :", len(X_test), "lignes")
print("Volatilité moyenne du test :", round(y_test.mean(), 5))

# --- Baselines (sans apprentissage) ---
print("\nBaseline 1 : on prédit la moyenne du train")
pred = [y_train.mean()] * len(y_test)
print("   MAE :", round(mean_absolute_error(y_test, pred), 5))

print("Baseline 2 : on prédit la volatilité des 20 derniers jours")
print("   MAE :", round(mean_absolute_error(y_test, X_test["vol_20j"]), 5),
      "  R2 :", round(r2_score(y_test, X_test["vol_20j"]), 3))

# --- Modèles entraînés ---
modeles = {
    "Régression linéaire": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42),
}
for nom, modele in modeles.items():
    modele.fit(X_train, y_train)
    pred = modele.predict(X_test)
    print(f"\n{nom}")
    print("   MAE :", round(mean_absolute_error(y_test, pred), 5),
          "  R2 :", round(r2_score(y_test, pred), 3))