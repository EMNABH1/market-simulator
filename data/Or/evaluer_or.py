import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import roc_auc_score, balanced_accuracy_score

df = pd.read_csv("processed/or_features.csv", index_col="date", parse_dates=True)
X = df.drop(columns="cible")
y = df["cible"]

modele = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

# Validation dans l'ordre du temps : 5 découpages successifs, avec un écart de 5 jours
tscv = TimeSeriesSplit(n_splits=5, gap=5)
for i, (tr, te) in enumerate(tscv.split(X), start=1):
    modele.fit(X.iloc[tr], y.iloc[tr])
    proba = modele.predict_proba(X.iloc[te])[:, 1]
    pred = modele.predict(X.iloc[te])
    print(f"Découpage {i} : test {X.index[te[0]].date()} -> {X.index[te[-1]].date()}")
    print(f"   hausses dans le test : {y.iloc[te].mean():.3f}"
          f"   AUC : {roc_auc_score(y.iloc[te], proba):.3f}"
          f"   accuracy équilibrée : {balanced_accuracy_score(y.iloc[te], pred):.3f}")