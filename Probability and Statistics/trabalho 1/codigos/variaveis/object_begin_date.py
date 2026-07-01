import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["Object Begin Date"])
years = df["Object Begin Date"].dropna().astype(int)

bin_width = 350
min_year, max_year = years.min(), years.max()
start = (min_year // bin_width) * bin_width
end   = ((max_year // bin_width) + 1) * bin_width
bins  = list(range(start, end + 1, bin_width))

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    years,
    bins=bins,
    rwidth=0.8
)

ax.set_axisbelow(True) 
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.3)

ax.set_title("Número de Peças Confeccionadas, em Intervalos de 350 Anos")
ax.set_xlabel("Ano de Confecção (intervalos de 350 anos)")
ax.set_ylabel("Quantidade de Peças")
ax.set_xticks(bins)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
