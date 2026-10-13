import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("or_brut.csv", index_col="date", parse_dates=True)

print("--- Volume médian par année ---")
print(df["Volume"].groupby(df.index.year).median())

print("\n--- Jours à volume zéro, par année ---")
zeros = df[df["Volume"] == 0]
print(zeros.groupby(zeros.index.year).size())

df["rendement"] = df["Close"].pct_change() * 100
print("\n--- 5 plus fortes hausses (%) ---")
print(df["rendement"].nlargest(5))
print("\n--- 5 plus fortes baisses (%) ---")
print(df["rendement"].nsmallest(5))

df["Close"].plot(title="Or : prix de clôture")
plt.show()