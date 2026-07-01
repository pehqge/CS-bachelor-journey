import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["area"])
area = df["area"].dropna().astype(float)

area = area[area <= 70000]

bin_width = 2500
bins = np.arange(0, 70000 + bin_width, bin_width)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    area,
    bins=bins,
    rwidth=0.8
)

ax.set_axisbelow(True)
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.3)

ax.set_title("Distribuição de Área das Pinturas (até 70.000 cm²)")
ax.set_xlabel("Área (cm²)")
ax.set_ylabel("Contagem de Peças")

ax.set_xlim(0, 70000)
ax.set_xticks(bins)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
