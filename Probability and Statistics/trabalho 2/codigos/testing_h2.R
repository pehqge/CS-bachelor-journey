# Carrega o pacote dplyr para manipulação de dados
library(dplyr)

# Este script assume que 'met_sample' foi criado pelo bloco de código anterior.

# --- H2: Teste de Proporções ---
# H₀: A proporção de obras com tema religioso entre os destaques é igual à dos não destacados.
# H₁: A proporção de obras com tema religioso entre os destaques é diferente da dos não destacados.

# 1. Preparar os dados da AMOSTRA para o teste de proporções
# Contagem de obras religiosas e não religiosas para cada categoria de destaque NA AMOSTRA.
# Filtra linhas onde as colunas 'Is_Religious' ou 'Is_Highlight' são NA na amostra,
# pois elas são essenciais para o cálculo das proporções.
contingency_table_sample <- met_sample %>%
  filter(!is.na(Is_Religious) & !is.na(Is_Highlight)) %>%
  group_by(Is_Highlight) %>% # Agrupa os dados pela coluna 'Is_Highlight' (TRUE/FALSE)
  summarise(
    Religious_Count = sum(Is_Religious == TRUE),      # Conta o número de obras religiosas em cada grupo
    Non_Religious_Count = sum(Is_Religious == FALSE), # Conta o número de obras não religiosas em cada grupo
    Total_Count = n()                                 # Conta o total de obras em cada grupo
  )

# Extrair as contagens necessárias para a função prop.test()
# 'x' é um vetor com o número de "sucessos" (obras religiosas) para cada grupo (destacado/não destacado)
x_sample <- contingency_table_sample$Religious_Count
# 'n' é um vetor com o número total de observações para cada grupo
n_sample <- contingency_table_sample$Total_Count

# 2. Realizar o Teste de Proporções
# A função prop.test() é usada para comparar as proporções de dois ou mais grupos.
# x: vetor de contagens de sucessos.
# n: vetor de contagens totais (tamanho da amostra para cada grupo).
# alternative = "two.sided": indica um teste bicaudal (queremos saber se as proporções são diferentes,
#                             não se uma é especificamente maior ou menor que a outra).
# conf.level = 0.95: define o nível de confiança para o intervalo de confiança (95%).
proportion_test_result_sample <- prop.test(x = x_sample, n = n_sample, alternative = "two.sided", conf.level = 0.95)

# 3. Exibir os resultados
print("--- H2: Teste de Proporções (Tema Religioso vs. Destaque - Usando AMOSTRA) ---")
print("Tabela de Contingência (Contagens da Amostra):")
print(contingency_table_sample)
print("")
print("Resultado Completo do Teste de Proporções da Amostra:")
print(proportion_test_result_sample)

# 4. Interpretação do resultado
# Definir o nível de significância (alfa), geralmente 0.05.
alpha <- 0.05

print("")
print("--- Interpretação da Hipótese 2 (com Amostra) ---")
print(paste("Nível de Significância (alfa):", alpha))
print(paste("Valor-p calculado:", round(proportion_test_result_sample$p.value, 4)))

if (proportion_test_result_sample$p.value < alpha) {
  print("A decisão estatística é: Rejeitar a Hipótese Nula (H₀).")
  print("Conclusão: Há evidências estatísticas significativas (com base nesta amostra) para afirmar que a proporção de obras com tema religioso entre os destaques é DIFERENTE da proporção entre as obras não destacadas na população.")
} else {
  print("A decisão estatística é: Não rejeitar a Hipótese Nula (H₀).")
  print("Conclusão: Não há evidências estatísticas suficientes (com base nesta amostra) para afirmar que a proporção de obras com tema religioso difere significativamente entre os destaques e os não destacados na população.")
}

# Para entender as proporções em si:
prop_highlighted <- x_sample[contingency_table_sample$Is_Highlight == TRUE] / n_sample[contingency_table_sample$Is_Highlight == TRUE]
prop_non_highlighted <- x_sample[contingency_table_sample$Is_Highlight == FALSE] / n_sample[contingency_table_sample$Is_Highlight == FALSE]

print(paste("\nProporção de obras religiosas entre as destacadas (na amostra):", round(prop_highlighted, 4)))
print(paste("Proporção de obras religiosas entre as não destacadas (na amostra):", round(prop_non_highlighted, 4)))

