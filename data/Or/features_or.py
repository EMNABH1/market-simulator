import pandas as pd

df = pd.read_csv("processed/or_propre.csv", index_col="date", parse_dates=True)

# --- FEATURES : uniquement des infos connues au jour J (le passé) ---
df["rendement_1j"] = df["Close"].pct_change()
df["rendement_5j"] = df["Close"].pct_change(5)
df["sma_5"] = df["Close"].rolling(5).mean() / df["Close"] - 1
df["sma_20"] = df["Close"].rolling(20).mean() / df["Close"] - 1
df["volatilite_20j"] = df["rendement_1j"].rolling(20).std()

# RSI sur 14 jours
delta = df["Close"].diff()
gain = delta.clip(lower=0).rolling(14).mean()
perte = (-delta.clip(upper=0)).rolling(14).mean()
df["rsi_14"] = 100 - 100 / (1 + gain / perte)

# --- CIBLE : le prix dans 5 jours est-il plus haut qu'aujourd'hui ? ---
df["cible"] = (df["Close"].shift(-5) > df["Close"]).astype(int)

# Les 5 dernières lignes n'ont pas de futur connu : on les retire
df = df.iloc[:-5]
df = df.dropna()

colonnes = ["rendement_1j", "rendement_5j", "sma_5", "sma_20",
            "volatilite_20j", "rsi_14", "cible"]
df[colonnes].to_csv("processed/or_features.csv")

print(len(df), "lignes")
print("\nRépartition de la cible (1 = hausse à 5 jours) :")
print(df["cible"].value_counts(normalize=True).round(3))
print(df[colonnes].tail())