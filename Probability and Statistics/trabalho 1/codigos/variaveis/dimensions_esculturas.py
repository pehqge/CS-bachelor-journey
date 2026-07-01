import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["volume"])
vol = df["volume"].dropna().astype(float)

max_vol   = 150000    
bin_width = 5000

vol = vol[vol <= max_vol]

bins = np.arange(0, max_vol + bin_width, bin_width)

fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(
    vol,
    bins=bins,
    rwidth=0.8
)

ax.set_axisbelow(True)
ax.yaxis.grid(True, color='lightgray', linestyle='-', linewidth=0.3)

ax.set_title("Distribuição de Volume (cm³) das Esculturas (até {:,})".format(max_vol))
ax.set_xlabel("Volume (cm³)")
ax.set_ylabel("Contagem de Peças")
ax.set_xlim(0, max_vol)
ax.set_xticks(bins)
plt.xticks(rotation=60)

plt.tight_layout()
plt.show()
