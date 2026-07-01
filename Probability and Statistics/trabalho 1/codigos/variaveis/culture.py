import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["Culture"])
df["CultureBase"] = df["Culture"].str.split(pat=",", n=1).str[0].str.strip()
df["CultureBaseFilled"] = df["CultureBase"].fillna("nan (Sem Cultura Associada)")

freq = df["CultureBaseFilled"].value_counts()
top15 = freq.drop("nan (Sem Cultura Associada)", errors="ignore") \
            .nlargest(15).index.tolist()

ordered_categories = ["nan (Sem Cultura Associada)"] + top15
counts = freq.loc[ordered_categories]

fig, ax = plt.subplots(figsize=(10, 6))
counts.plot.barh(ax=ax, color="skyblue")

ax.invert_yaxis()

ax.set_axisbelow(True)

ax.xaxis.grid(True, color="lightgray", linestyle="-", linewidth=0.3)

ax.set_title("Top 15 Culturas + Sem Cultura Associada")
ax.set_xlabel("Contagem de Peças")
ax.set_ylabel("Categoria de Cultura")
plt.tight_layout()
plt.show()
