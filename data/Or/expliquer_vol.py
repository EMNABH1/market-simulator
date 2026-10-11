import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

df = pd.read_csv("processed/or_propre.csv", index_col="date", parse_dates=True)

df["rendement_1j"] = df["Close"].pct_change()
df["abs_rendement_1j"] = df["rendement_1j"].abs()
df["vol_5j"] = df["rendement_1j"].rolling(5).std()
df["vol_20j"] = df["rendement_1j"].rolling(20).std()
df["vol_60j"] = df["rendement_1j"].rolling(60).std()
df["amplitude_1j"] = (df["High"] - df["Low"]) / df["Close"]
df["cible"] = df["rendement_1j"].rolling(5).std().shift(-5)

features = ["abs_rendement_1j", "vol_5j", "vol_20j", "vol_60j", "amplitude_1j"]

# Dernière ligne connue : sert à l'explication locale (sa cible n'existe pas encore)
derniere = df[features].dropna().iloc[[-1]]

data = df.iloc[:-5].dropna()
X, y = data[features], data["cible"]
train = data.index < "2024-01-01"
idx_train = X[train].index[:-5]
X_train, y_train = X.loc[idx_train], y.loc[idx_train]
X_test, y_test = X[~train], y[~train]

# On met les variables à la même échelle pour pouvoir comparer leurs poids
scaler = StandardScaler().fit(X_train)
modele = LinearRegression().fit(scaler.transform(X_train), y_train)

# --- 1. EXPLICATION GLOBALE ---
print("=== 1. Poids de chaque variable (variables standardisées) ===")
for nom, coef in sorted(zip(features, modele.coef_), key=lambda t: -abs(t[1])):
    sens = "hausse" if coef > 0 else "baisse"
    print(f"   {nom:18s} {coef:+.5f}  (pousse la volatilité prévue à la {sens})")

print("\n=== 2. Importance par permutation (sur le test) ===")
res = permutation_importance(
    modele, scaler.transform(X_test), y_test,
    scoring="neg_mean_absolute_error", n_repeats=20, random_state=42,
)
for nom, imp in sorted(zip(features, res.importances_mean), key=lambda t: -t[1]):
    print(f"   {nom:18s} erreur +{imp:.5f} si on brouille cette variable")

# --- 2. EXPLICATION LOCALE (dernière date connue) ---
z = scaler.transform(derniere)[0]
contrib = modele.coef_ * z
prevision = modele.intercept_ + contrib.sum()

print(f"\n=== 3. Pourquoi cette prévision ? (date : {derniere.index[0].date()}) ===")
print(f"   Niveau de départ (moyenne) : {modele.intercept_:.5f}")
for nom, c, val in sorted(zip(features, contrib, derniere.iloc[0]), key=lambda t: -abs(t[1])):
    print(f"   {nom:18s} valeur {val:.5f}  ->  contribution {c:+.5f}")
print(f"   Volatilité prévue (5 prochains jours) : {prevision:.5f}")