# carregando bibliotecas que vamos usar
library(ggplot2)
library(dplyr)
library(tidyr)
library(stringr)

# carregando o arquivo csv
df <- read.csv("trabalho1/tabela_met.csv", stringsAsFactors = FALSE, check.names = FALSE)

# renomeando as colunas para facilitar o uso no R
names(df)[names(df) == "Is Highlight"] <- "IsHighlight"
names(df)[names(df) == "Classification"] <- "Classificacao"

# convertendo IsHighlight para lógico
df$IsHighlight <- as.logical(df$IsHighlight)

# filtrando obras destacadas
obras_destacadas <- df %>%
  filter(IsHighlight == TRUE)

# filtrando pinturas e esculturas
pinturas <- obras_destacadas %>%
  filter(str_detect(tolower(Classificacao), "painting")) %>%
  filter(!is.na(area)) %>%
  # removendo outliers extremos para melhor visualização
  filter(area < quantile(area, 0.99, na.rm = TRUE))

esculturas <- obras_destacadas %>%
  filter(str_detect(tolower(Classificacao), "sculpture")) %>%
  filter(!is.na(volume)) %>%
  # removendo outliers extremos para melhor visualização
  filter(volume < quantile(volume, 0.99, na.rm = TRUE))

# calculando quartis para pinturas
q1_pintura <- quantile(pinturas$area, 0.25)
q2_pintura <- quantile(pinturas$area, 0.50) # mediana
q3_pintura <- quantile(pinturas$area, 0.75)

# calculando quartis para esculturas
q1_escultura <- quantile(esculturas$volume, 0.25)
q2_escultura <- quantile(esculturas$volume, 0.50) # mediana
q3_escultura <- quantile(esculturas$volume, 0.75)

# filtrando para mostrar apenas obras abaixo do q3
pinturas_abaixo_q3 <- pinturas %>% filter(area <= q3_pintura)
esculturas_abaixo_q3 <- esculturas %>% filter(volume <= q3_escultura)

# criando pasta para salvar imagens
dir.create("trabalho1/imagens", showWarnings = FALSE, recursive = TRUE)

# definindo cores e tema comum
cor_pintura <- "#3A539B"  # azul escuro
cor_escultura <- "#674172"  # roxo
tema_comum <- theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold"),
    plot.subtitle = element_text(hjust = 0.5, size = 12),
    axis.title = element_text(size = 12, face = "bold"),
    axis.text = element_text(size = 10),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_line(color = "#E8E8E8", size = 0.3),
    panel.grid.major.y = element_line(color = "#E8E8E8", size = 0.3),
    legend.position = "none"
  )

# preparando dataframes para anotações de quartis
quartis_pintura <- data.frame(
  quartil = c("Q1", "Q2", "Q3"),
  valor = c(q1_pintura, q2_pintura, q3_pintura),
  cor = c("blue", "red", "green")
)

quartis_escultura <- data.frame(
  quartil = c("Q1", "Q2", "Q3"),
  valor = c(q1_escultura, q2_escultura, q3_escultura),
  cor = c("blue", "red", "green")
)

# gráfico de densidade para pinturas (área) abaixo do Q3
densidade_pinturas <- ggplot(pinturas_abaixo_q3, aes(x = area)) +
  # histograma semi-transparente por baixo
  geom_histogram(aes(y = after_stat(density)), fill = cor_pintura, alpha = 0.3, bins = 30) +
  # linha de densidade suavizada
  geom_density(color = cor_pintura, linewidth = 1, fill = cor_pintura, alpha = 0.2) +
  # adicionando linhas verticais dos quartis
  geom_vline(data = quartis_pintura, aes(xintercept = valor, color = quartil), 
             linetype = "dashed", linewidth = 0.8) +
  # anotações dos quartis
  geom_text(data = quartis_pintura,
            aes(x = valor, y = 0, label = paste0(quartil, ": ", round(valor, 1)), color = quartil),
            hjust = -0.1, vjust = -1, size = 4) +
  # definindo cores para os quartis
  scale_color_manual(values = c("Q1" = "blue", "Q2" = "red", "Q3" = "green")) +
  # ajustando eixos e títulos
  scale_x_continuous(labels = scales::comma) +
  labs(
    title = "Distribuição da Área das Pinturas Destacadas (abaixo do Q3)",
    subtitle = "Quartis das obras classificadas como pinturas com status de destaque",
    x = "Área (cm²)",
    y = "Densidade"
  ) +
  tema_comum

# gráfico de densidade para esculturas (volume) abaixo do Q3
densidade_esculturas <- ggplot(esculturas_abaixo_q3, aes(x = volume)) +
  # histograma semi-transparente por baixo
  geom_histogram(aes(y = after_stat(density)), fill = cor_escultura, alpha = 0.3, bins = 30) +
  # linha de densidade suavizada
  geom_density(color = cor_escultura, linewidth = 1, fill = cor_escultura, alpha = 0.2) +
  # adicionando linhas verticais dos quartis
  geom_vline(data = quartis_escultura, aes(xintercept = valor, color = quartil), 
             linetype = "dashed", linewidth = 0.8) +
  # anotações dos quartis
  geom_text(data = quartis_escultura,
            aes(x = valor, y = 0, label = paste0(quartil, ": ", round(valor, 1)), color = quartil),
            hjust = -0.1, vjust = -1, size = 4) +
  # definindo cores para os quartis
  scale_color_manual(values = c("Q1" = "blue", "Q2" = "red", "Q3" = "green")) +
  # ajustando eixos e títulos
  scale_x_continuous(labels = scales::comma) +
  labs(
    title = "Distribuição do Volume das Esculturas Destacadas (abaixo do Q3)",
    subtitle = "Quartis das obras classificadas como esculturas com status de destaque",
    x = "Volume (cm³)",
    y = "Densidade"
  ) +
  tema_comum

# exibindo os gráficos
print(densidade_pinturas)
print(densidade_esculturas)

# salvando os gráficos
ggsave(
  filename = "trabalho1/imagens/densidade_pinturas_highlight_q3.png",
  plot = densidade_pinturas,
  width = 30,
  height = 20,
  dpi = 300,
  units = "cm",
  bg = "white"
)

ggsave(
  filename = "trabalho1/imagens/densidade_esculturas_highlight_q3.png",
  plot = densidade_esculturas,
  width = 30,
  height = 20,
  dpi = 300,
  units = "cm",
  bg = "white"
) 