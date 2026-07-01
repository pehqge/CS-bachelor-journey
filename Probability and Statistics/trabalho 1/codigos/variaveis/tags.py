import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["Tags"])

df = df.dropna(subset=["Tags"])
df = df.assign(Tag=df["Tags"].str.split(r"\|")).explode("Tag")
df["Tag"] = df["Tag"].str.strip() 

top15 = df["Tag"].value_counts().nlargest(15).index.tolist()

counts = df[df["Tag"].isin(top15)]["Tag"].value_counts().loc[top15]

fig, ax = plt.subplots(figsize=(10, 6))
counts.plot.barh(
    ax=ax,
    color="skyblue",
)
ax.invert_yaxis()        
ax.set_axisbelow(True)
ax.xaxis.grid(True, color="lightgray", linestyle="-", linewidth=0.3)

ax.set_title("Top 15 Tags")
ax.set_xlabel("Contagem de Peças")
ax.set_ylabel("Tag")
plt.tight_layout()
plt.show()
