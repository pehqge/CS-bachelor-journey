import pandas as pd
import numpy as np
import sys
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from pathlib import Path

csv = sys.argv[1] if len(sys.argv) > 1 else "trabalho 2/data/met_data.csv"
if not Path(csv).is_file():
    sys.exit(f"Arquivo não encontrado: {csv}")

# 1. carregar e padronizar nomes
df = pd.read_csv(csv)
df.columns = (df.columns.str.strip()
                        .str.lower()
                        .str.replace(r"[^\w]+", "_", regex=True))

# 2. filtrar esculturas válidas
esc = (df.query("is_sculpture == True")
         .dropna(subset=["object_begin_date", "area_volume"])
         .copy())

# 3. log10 do volume
esc["log_vol"] = np.log10(esc.area_volume.replace(0, np.nan))
esc = esc.dropna(subset=["log_vol"])      # garante mesmas linhas no gráfico e modelo

# 4. regressão
model = smf.ols("log_vol ~ object_begin_date", data=esc).fit()
print("\n────────  Esculturas – Regressão log(volume) ~ ano  ────────")
print(model.summary())

# 5. plota o gráfico
plt.figure(figsize=(9,5))
plt.scatter(esc.object_begin_date, esc.log_vol, s=8, alpha=.3)
x = np.linspace(esc.object_begin_date.min(), esc.object_begin_date.max(), 200)
y = model.params.Intercept + model.params.object_begin_date * x
plt.plot(x, y, c="red", lw=2)
plt.xlabel("Ano da obra")
plt.ylabel("log10(volume cm³)")
plt.title("Esculturas do MET – Tamanho ao longo do tempo")
plt.grid(alpha=.25)
plt.tight_layout()
plt.show()