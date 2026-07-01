import pandas as pd
import numpy as np

df = pd.read_csv("trabalho1/tabela_met.csv", usecols=["area", "volume", "Object Begin Date"])

df["sqrt_area"] = np.sqrt(df["area"].astype(float))
df["cube_root_volume"] = np.cbrt(df["volume"].astype(float))

variables = ["area", "sqrt_area", "volume", "cube_root_volume", "Object Begin Date"]
df_stats = pd.DataFrame({
    "min":              df[variables].min(),
    "max":              df[variables].max(),
    "25th_percentile":  df[variables].quantile(0.25),
    "mean":             df[variables].mean(),
    "median":           df[variables].median(),
    "75th_percentile":  df[variables].quantile(0.75),
    "std_dev":          df[variables].std(),
    "variance":         df[variables].var(),
})

print("Resumo Estatístico (originais e transformados):\n")
print(df_stats.to_string(float_format="%.2f"))
