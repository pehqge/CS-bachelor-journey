import pandas as pd
from scipy.stats import ttest_ind

# ======================================================
# Preparacao dos Dados

# ------------------------------------------------------
# 1. Extracao

data = pd.read_csv("../data/met_data.csv")
data_pinturas = data[data["Is_Sculpture"] == False]  # dados das pinturas


# ------------------------------------------------------
# 2. Criacao de Amostra Aleatria (1000 pinturas)

amostra = data_pinturas.sample(n = 1000, random_state=123)  # random_state eh usado pra gerar a mesma amostra
# o tamanho da amostra e random_state podem ser modificados como desejado

# ------------------------------------------------------
# 3. Filtro de Colunas Relevantes e Remocao de NanNs

amostra = amostra[["Is_Highlight", "area/volume"]].dropna()

# ------------------------------------------------------
# 4. Separacao de Obras Destacadas e Nao Destacadas

destacadas = amostra[amostra["Is_Highlight"] == True]["area/volume"]
nao_destacadas = amostra[amostra["Is_Highlight"] == False]["area/volume"]

# ======================================================
# Exploracao das Hipoteses
'''
H0: A média da área das pinturas destacadas é igual à das não destacadas.
H1: As médias são diferentes.
'''

print("Hipótese 1 — Teste de comparação de médias (área das pinturas)\n")

# ------------------------------------------------------
# 1. Calculo das Medias

media_destacadas = destacadas.mean()
media_nao_destacadas = nao_destacadas.mean()

# ------------------------------------------------------
# 2. Teste t de Student (Para Amostras Independentes)

t, p_valor = ttest_ind(destacadas, nao_destacadas)

print(f"Média das áreas (destacadas): {media_destacadas:.2f}")
print(f"Média das áreas (não destacadas): {media_nao_destacadas:.2f}\n")
print(f"t = {t:.4f}")
print(f"p-valor = {p_valor:.4f}\n")

# ------------------------------------------------------
# 3. Validacao da Hipotese

a = 0.05
if p_valor < a:
    print("Rejeitamos H0: Há diferença significativa entre as médias.")
else:
    print("Não rejeitamos H0: Não há diferença significativa entre as médias.")
