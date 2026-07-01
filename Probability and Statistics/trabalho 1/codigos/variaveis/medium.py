import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["Medium"])
df["MediumClean"] = df["Medium"].fillna("Sem Medium").str.strip()

top15 = df["MediumClean"].value_counts().nlargest(15).index.tolist()
counts_top15 = (
    df[df["MediumClean"].isin(top15)]["MediumClean"]
      .value_counts()
      .loc[top15]
)

fig, ax = plt.subplots(figsize=(10,6))
counts_top15.plot.barh(
    ax=ax,
    color="lightgreen"
)


ax.invert_yaxis()
ax.set_axisbelow(True)
ax.xaxis.grid(True, color="lightgray", linestyle="-", linewidth=0.3)

ax.set_title("Os 15 Meios/Materiais Mais Comuns")
ax.set_xlabel("Quantidade de Peças")
ax.set_ylabel("Meio/Material")
plt.tight_layout()
plt.show()
