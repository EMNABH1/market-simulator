import pandas as pd

df = pd.read_csv("or_brut.csv", index_col="date", parse_dates=True)

print("--- Premières lignes ---")
print(df.head())
print("\n--- Dernières lignes ---")
print(df.tail())
print("\n--- Statistiques ---")
print(df.describe())
print("\nValeurs manquantes :")
print(df.isnull().sum())
print("\nDates en double :", df.index.duplicated().sum())
print("Volumes à zéro :", (df["Volume"] == 0).sum())
print("Dates non triées :", not df.index.is_monotonic_increasing)