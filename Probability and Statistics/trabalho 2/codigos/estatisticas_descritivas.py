import pandas as pd
import numpy as np
from scipy import stats

# ======================================================
# Funcoes

# ------------------------------------------------------
# Intervalo de confiança de uma média
def intervalo_confianca_media(amostra, nivel=0.95):
    media = amostra.mean()
    desvio = amostra.std()
    n = len(amostra)
    erro = stats.t.ppf((1 + nivel) / 2, df=n - 1) * (desvio / np.sqrt(n))
    return media - erro, media + erro

# ------------------------------------------------------
# Intervalo de confiança de uma proporção
def intervalo_confianca_proporcao(p, n, nivel=0.95):
    z = stats.norm.ppf((1 + nivel) / 2)
    erro = z * np.sqrt(p * (1 - p) / n)
    return p - erro, p + erro

# ======================================================
# Leitura dos Arquivos

data = pd.read_csv("met_data.csv")
data_tags = pd.read_csv("met_data_tags.csv")

data_pinturas = data[data["Is_Sculpture"] == False]  # dados das pinturas
data_esculturas = data[data["Is_Sculpture"] == True]  # dados das esculturas

# ======================================================
# Estatísticas Descritivas por Variável

# ------------------------------------------------------
# 1. Ano da Obra

anos = data["Object_Begin_Date"]

media_ano = anos.mean()
mediana_ano = anos.median()
desvio_ano = anos.std()
min_ano = anos.min()
max_ano = anos.max()
ic_ano = intervalo_confianca_media(anos)

print("Ano das obras:")
print(f"Média: {media_ano:.2f}")
print(f"Mediana: {mediana_ano}")
print(f"Desvio padrão: {desvio_ano:.2f}")
print(f"Mínimo: {min_ano}, Máximo: {max_ano}")
print(f"IC 95% da média: ({ic_ano[0]:.2f}, {ic_ano[1]:.2f})")

# ------------------------------------------------------
# 2. Área das Pinturas

areas = data_pinturas["area/volume"]

media_area = areas.mean()
mediana_area = areas.median()
desvio_area = areas.std()
min_area = areas.min()
max_area = areas.max()
ic_area = intervalo_confianca_media(areas)

print("\nÁrea das pinturas:")
print(f"Média: {media_area:.2f}")
print(f"Mediana: {mediana_area}")
print(f"Desvio padrão: {desvio_area:.2f}")
print(f"Mínimo: {min_area}, Máximo: {max_area}")
print(f"IC 95% da média: ({ic_area[0]:.2f}, {ic_area[1]:.2f})")

# ------------------------------------------------------
# 3. Volume das Esculturas

volumes = data_esculturas['area/volume']

media_volume = volumes.mean()
mediana_volume = volumes.median()
desvio_volume = volumes.std()
min_volume = volumes.min()
max_volume = volumes.max()
ic_volume = intervalo_confianca_media(volumes)

print("\nVolume das esculturas:")
print(f"Média: {media_volume:.2f}")
print(f"Mediana: {mediana_volume}")
print(f"Desvio padrão: {desvio_volume:.2f}")
print(f"Mínimo: {min_volume}, Máximo: {max_volume}")
print(f"IC 95% da média: ({ic_volume[0]:.2f}, {ic_volume[1]:.2f})")

# ------------------------------------------------------
# 4. Tags

frequencia_tags = data_tags["Tags"].value_counts()
print("\nTags mais frequentes:")
print(frequencia_tags.head(10).to_string())

# ------------------------------------------------------
# 5. Obras em Destaque

n_total = len(data)
n_destaques = data["Is_Highlight"].sum()
proporcao = n_destaques / n_total
ic_proporcao = intervalo_confianca_proporcao(proporcao, n_total)

print("\nProporção de obras em destaque:")
print(f"Total de obras: {n_total}")
print(f"Número de destaques: {n_destaques}")
print(f"Proporção: {proporcao:.4f} ({proporcao*100:.2f}%)")
print(f"IC 95% da proporção: ({ic_proporcao[0]*100:.2f}%, {ic_proporcao[1]*100:.2f}%)")
