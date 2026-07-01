# carregando bibliotecas que vamos usar
library(ggplot2)
library(dplyr)
library(tidyr)
library(stringr)
library(forcats)

# carregando o arquivo csv
df <- read.csv("trabalho1/tabela_met.csv", stringsAsFactors = FALSE, check.names = FALSE)

# renomeando as colunas
names(df)[names(df) == "Tags"] <- "Tags"
names(df)[names(df) == "Is Highlight"] <- "IsHighlight"

# convertendo IsHighlight para lógico
df$IsHighlight <- as.logical(df$IsHighlight)

# separando as tags (apenas para obras em destaque)
tags_destaque <- df %>%
  filter(!is.na(Tags) & Tags != "" & IsHighlight == TRUE) %>%
  select(Tags) %>%
  # separando as tags pelo delimitador "|"
  mutate(Tags = strsplit(Tags, "\\|")) %>%
  # expandindo a lista de tags para ter uma linha por tag
  unnest(Tags) %>%
  # limpando espaços extras
  mutate(Tags = trimws(Tags))

# contando as tags em destaque mais frequentes
top_tags_destaque <- tags_destaque %>%
  count(Tags, sort = TRUE) %>%
  slice_head(n = 10)

# preparando os dados para o gráfico de pareto
dados_pareto <- top_tags_destaque %>%
  # adicionando a categoria "Outros" para as tags menos frequentes
  bind_rows(
    tags_destaque %>%
      anti_join(top_tags_destaque, by = "Tags") %>%
      count(name = "n") %>%
      mutate(Tags = "Outros")
  ) %>%
  # ordenando do maior para o menor, com "Outros" no final
  arrange(desc(n)) %>%
  mutate(
    # Criando fator para manter a ordem no gráfico
    Tags = factor(Tags, levels = c(pull(top_tags_destaque, Tags), "Outros")),
    # Calculando a porcentagem
    porcentagem = n / sum(n) * 100,
    # Calculando a porcentagem acumulada
    porcentagem_acumulada = cumsum(porcentagem),
    # Adicionando rótulos para o gráfico
    rotulo_valor = n,
    rotulo_porcentagem = paste0(round(porcentagem), "%")
  )

# definindo cores
cor_barras <- "#5D8AA8"
cor_linha_pareto <- "#7B3F00"

# criando o gráfico de pareto
grafico_pareto <- ggplot() +
  # adicionando as barras
  geom_bar(
    data = dados_pareto,
    aes(x = Tags, y = n, fill = "Contagem"),
    stat = "identity",
    width = 0.7
  ) +
  # adicionando a linha de porcentagem acumulada
  geom_line(
    data = dados_pareto,
    aes(x = Tags, y = porcentagem_acumulada * max(n) / 100, group = 1, color = "% Acumulada"),
    size = 0.8
  ) +
  # adicionando pontos à linha de porcentagem acumulada
  geom_point(
    data = dados_pareto,
    aes(x = Tags, y = porcentagem_acumulada * max(n) / 100, group = 1, color = "% Acumulada"),
    size = 2.5,
    shape = 21,
    fill = "white",
    stroke = 0.8
  ) +
  # adicionando rótulos de porcentagem acumulada
  geom_text(
    data = dados_pareto,
    aes(x = Tags, y = porcentagem_acumulada * max(n) / 100, 
        label = paste0(round(porcentagem_acumulada), "%")),
    vjust = -0.8,
    color = cor_linha_pareto,
    fontface = "bold",
    size = 3.2
  ) +
  # adicionando rótulos de contagem em cada barra
  geom_text(
    data = dados_pareto,
    aes(x = Tags, y = n / 2, label = rotulo_valor),
    color = "white",
    fontface = "bold",
    size = 3.2
  ) +
  # configurando os eixos
  scale_y_continuous(
    name = "Contagem",
    sec.axis = sec_axis(~ . * 100 / max(dados_pareto$n), name = "% Acumulada")
  ) +
  # definindo cores
  scale_fill_manual(values = c("Contagem" = cor_barras)) +
  scale_color_manual(values = c("% Acumulada" = cor_linha_pareto)) +
  # personalizando o tema
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(hjust = 0.5, size = 16, face = "bold", margin = margin(b = 10)),
    plot.subtitle = element_text(hjust = 0.5, size = 12, margin = margin(b = 20)),
    axis.title.x = element_blank(),
    axis.title.y = element_text(size = 12, face = "bold"),
    axis.text.x = element_text(angle = 45, hjust = 1, size = 10),
    axis.text.y = element_text(size = 10),
    legend.title = element_blank(),
    legend.position = "top",
    legend.margin = margin(b = 10),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "#E8E8E8", size = 0.3),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA),
    plot.margin = margin(t = 20, r = 20, b = 20, l = 20)
  ) +
  # adicionando título e subtítulo
  labs(
    title = "Top 10 tags em obras destacadas",
    subtitle = "Distribuição das tags mais frequentes em obras com destaque"
  )

# exibindo o gráfico
print(grafico_pareto)

# criando diretório para salvar a imagem se não existir
dir.create("trabalho1/imagens", showWarnings = FALSE, recursive = TRUE)

# salvando o gráfico
ggsave(
  filename = "trabalho1/imagens/pareto_tags_highlight.png",
  plot = grafico_pareto,
  width = 30,
  height = 20,
  dpi = 300,
  units = "cm",
  bg = "white"
) 