import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["Is Highlight"])

df["HighlightLabel"] = df["Is Highlight"].map({
    True: "É destaque",
    False: "Não é destaque",
    "True": "É destaque",
    "False": "Não é destaque"
}).fillna("Sem dado")

counts = df["HighlightLabel"].value_counts()

plt.figure(figsize=(8,8))
wedges, texts, autotexts = plt.pie(
    counts.values,
    labels=counts.index,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
plt.title("Proporção de Objetos em Destaque", )

min_idx = counts.values.argmin()
x_min, y_min = autotexts[min_idx].get_position()
autotexts[min_idx].set_position((x_min * 1.4, y_min * 1.4))

max_idx = counts.values.argmax()
autotexts[max_idx].set_color("white")
autotexts[min_idx].set_color("white")

plt.tight_layout()
plt.show()
