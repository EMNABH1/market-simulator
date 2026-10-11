import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score

df = pd.read_csv("processed/or_features.csv", index_col="date", parse_dates=True)
X = df.drop(columns="cible")
y = df["cible"]

# Découpage dans l'ordre du temps (jamais aléatoire)
train = df.index < "2024-01-01"
test = df.index >= "2024-01-01"

# On retire 5 lignes à la fin du train : leur cible regarde dans la période de test
idx_train = X[train].index[:-5]
X_train, y_train = X.loc[idx_train], y.loc[idx_train]
X_test, y_test = X[test], y[test]

print("Train :", len(X_train), "lignes, jusqu'à", X_train.index.max().date())
print("Test  :", len(X_test), "lignes, depuis", X_test.index.min().date())
print("Part de hausses dans le test :", round(y_test.mean(), 3))

modeles = {
    "Baseline (toujours la classe la plus fréquente)": DummyClassifier(strategy="most_frequent"),
    "Régression logistique": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=5, random_state=42),
}

print()
for nom, modele in modeles.items():
    modele.fit(X_train, y_train)
    pred = modele.predict(X_test)
    print(f"{nom}")
    print(f"   accuracy : {accuracy_score(y_test, pred):.3f}   F1 : {f1_score(y_test, pred):.3f}")