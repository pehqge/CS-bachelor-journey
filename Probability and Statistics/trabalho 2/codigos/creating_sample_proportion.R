# Certifique-se de que o pacote dplyr está carregado
library(dplyr)

# --- Gerar uma Amostra Aleatória ---
# Definindo o tamanho da amostra
sample_size <- 1000 # Exemplo: amostrar 1000 obras

# replace = FALSE` significa que cada linha é selecionada no máximo uma vez (amostragem sem reposição).
set.seed(123) # Um número qualquer, usado para reprodutibilidade
met_sample <- met_data %>%
  sample_n(size = sample_size, replace = FALSE)

