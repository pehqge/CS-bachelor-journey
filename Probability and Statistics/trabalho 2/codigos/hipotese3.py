import pandas as pd                  
from scipy.stats import pointbiserialr 
import numpy as np                    
import matplotlib.pyplot as plt

# ------------------------------------------------------
# 1. PREPARAÇÃO DOS DADOS

data = pd.read_csv("../data/met_data.csv")

amostra = data.sample(
    n=1000,                           
    random_state=123
)

# POPULAÇÃO:
# Mantém só as colunas de interesse e remove linhas com NaN
populacao = data[["Object_Begin_Date", "Is_Highlight"]].dropna()
# Converte o booleano em inteiro 1/0
populacao["Highlight_Num"] = populacao["Is_Highlight"].astype(int)

# AMOSTRA:
# Seleciona apenas as colunas de interesse, e remove linhas com valores não disponíveis
amostra = amostra[["Object_Begin_Date", "Is_Highlight"]].dropna()
# Transforma o booleano True/False de 'Is_Highlight' em inteiro 1/0
amostra["Highlight_Num"] = amostra["Is_Highlight"].astype(int)

# ------------------------------------------------------
# 2. FORMULAÇÃO DAS HIPÓTESES

# H0: rho_pb = 0 (nenhuma correlação entre Object_Begin_Date e Highlight_Num)
# H1: rho_pb ≠ 0 (existe correlação)

# ------------------------------------------------------
# 3. CÁLCULO DO COEFICIENTE POINT-BISERIAL

# POPULAÇÃO
rho_pb_populacao, p_valor_populacao = pointbiserialr(
    populacao["Highlight_Num"],
    populacao["Object_Begin_Date"]
)

# AMOSTRA
# Chama pointbiserialr com as duas colunas de interesse da amostra, e retorna o valor do coeficiente de correlação em rho_pb (rho point-biserial), e retorna p-valor, que indica a significância estatística. O p-valor diz o quão improvável seria obter no caso de nenhuma correlação (H0 correta)
rho_pb_amostra, p_valor_amostra = pointbiserialr(
    amostra["Highlight_Num"], 
    amostra["Object_Begin_Date"]
)


print("\nPoint-Biserial Correlation (Object_Begin_Date and Is_Highlight):\n")

# POPULAÇÃO
print("População:")
print(f"rho_pb_populacao = {rho_pb_populacao:.4f}") 
print(f"p-valor_populacao = {p_valor_populacao:.4f}\n") 

# AMOSTRA
print("Amostra:")
print(f"rho_pb_amostra = {rho_pb_amostra:.4f}") 
print(f"p-valor_amostra = {p_valor_amostra:.4f}\n")  

# ------------------------------------------------------
# 4. INTERPRETAÇÃO

# Define o nível de significância (5%)
alpha = 0.05                     

print("\nINTERPRETAÇÃO DOS RESULTADOS:\n")

# POPULAÇÃO
print("População:")
if p_valor_populacao < alpha:
    sentido = "positiva" if rho_pb_populacao > 0 else "negativa"
    print(f"Rejeitamos H0, pois há correlação {sentido} significativa.")
else:
    print("Não rejeitamos H0: nenhuma correlação significativa.")

# AMOSTRA
print("\nAmostra:")
if p_valor_amostra < alpha: 
    sentido = "positiva" if rho_pb_amostra > 0 else "negativa"
    print(f"Rejeitamos H0, pois há correlação {sentido} significativa.")
else:
    print("Não rejeitamos H0: nenhuma correlação significativa.")

# ------------------------------------------------------
# 5. VISUALIZAÇÃO

# POPULACAO
plt.figure(figsize=(10,6))
y = populacao["Highlight_Num"] + (np.random.rand(len(populacao)) - 0.5) * 0.1
plt.scatter(populacao["Object_Begin_Date"], y, alpha=0.4)
plt.yticks([0,1], ["Não-Highlight","Highlight"])
plt.xlabel("Ano de Início da Obra")
plt.title("Object_Begin_Date e Is_Highlight")
plt.tight_layout()           
plt.show()        

# AMOSTRA
plt.figure(figsize=(10,6))
y = amostra["Highlight_Num"] + (np.random.rand(len(amostra)) - 0.5) * 0.1
plt.scatter(amostra["Object_Begin_Date"], y, alpha=0.4)
plt.yticks([0,1], ["Não-Highlight","Highlight"])
plt.xlabel("Ano de Início da Obra")
plt.title("Object_Begin_Date e Is_Highlight")
plt.tight_layout()           
plt.show()                   