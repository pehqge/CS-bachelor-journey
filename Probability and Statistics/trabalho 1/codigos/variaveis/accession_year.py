import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["AccessionYear"])
years = df["AccessionYear"].dropna().astype(int)

min_year, max_year = years.min(), years.max()
start = (min_year // 5) * 5
end   = ((max_year // 5) + 1) * 5
bins  = list(range(start, end + 1, 5))

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    years,
    bins=bins,
    rwidth=0.8
)

ax.set_axisbelow(True)
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.3)

ax.set_title("Número de Peças Adquiridas por Intervalo de 5 Anos")
ax.set_xlabel("Ano (bins de 5 anos)")
ax.set_ylabel("Quantidade de Peças")
ax.set_xticks(bins)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()