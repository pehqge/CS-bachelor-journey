import numpy as np
import scipy.stats as stats

# ------ Problema 1 - (ultimo exercicio da aula de regressao) ------

# *-* a) As variáveis Idade em semanas e Altura são correlacionadas? *-*
# Calcule o coeficiente de correlação Linear de Pearson e 
# verifique se ele difere significativamente de zero (5% de significância)


# calculando o coeficiente de correlação linear de Pearson (r)
# r = (n*sum(xi*yi) - sum(xi)*sum(yi)) / sqrt((n*sum(xi^2) - sum(xi)^2) * (n*sum(yi^2) - sum(yi)^2))

# variaveis de r
xi = [1, 2, 3, 4, 5, 6, 7] # semanas
yi = [5, 13, 16, 23, 33, 38, 40] # alturas em cm do feijao
xi2 = [x**2 for x in xi]
yi2 = [y**2 for y in yi]
xiyi = [xi[i]*yi[i] for i in range(len(xi))]

# achando ax+ b


# somatorios
sum_xi = sum(xi)
sum_yi = sum(yi)
sum_xi2 = sum(xi2)
sum_yi2 = sum(yi2)
sum_xiyi = sum(xiyi)

r = (len(xi)*sum_xiyi - sum_xi*sum_yi) / (np.sqrt((len(xi)*sum_xi2 - sum_xi**2)) * np.sqrt(len(xi)*sum_yi2 - sum_yi**2))
print(f"coeficiente de correlação linear de Pearson: {r}")

# 1: Teste de hipotese
# H0: r = 0
# H1: r != 0

# 2: Teste T
t = r * np.sqrt(len(xi)-2) / np.sqrt(1-r**2)
print(f"\nt: {t}")
t_tab = stats.t.ppf(0.975, len(xi)-2) # pega o valor crítico de t para 5% de significância
print(f"t tabelado: {t_tab}\n")

# 3: Regra de decisao

if t > t_tab or t < -t_tab:
    print("Rejeitamos H0 e concluimos que r é significativo")
else:
    print("Não rejeitamos H0 e concluimos que r não é significativo")
    
# 4: Conclusao
# como p_valor < 0.05, rejeitamos H0 e concluimos que r é significativo

# *-* b) Obtenha a reta de mínimos quadrados que descreve o comportamento do altura em função da idade *-*

b = (len(xi)*sum_xiyi - sum_xi*sum_yi) / (len(xi)*sum_xi2 - sum_xi**2)
a = (sum_yi - b*sum_xi) / len(xi)

print(f"\nequação da reta: y = {a} + {b}x")


# *-* c) Calcule a altura esperada para uma idade de 8 semanas *-*

x_8 = 8
y_8 = a + b*x_8
print(f"\naltura esperada para uma idade de 8 semanas: {y_8}")

