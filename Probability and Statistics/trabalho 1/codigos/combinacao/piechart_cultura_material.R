# carregando bibliotecas que vamos usar
library(ggplot2)
library(dplyr)
library(tidyr)
library(forcats) # para fct_reorder

# carregando o arquivo csv
df <- read.csv("trabalho1/tabela_met.csv", stringsAsFactors = FALSE, check.names = FALSE)

# renomeando as colunas
names(df)[names(df) == "Culture"] <- "Cultura"
names(df)[names(df) == "Medium"] <- "Meio"

# encontrando as 5 culturas mais frequentes
top5_culturas <- df %>%
  filter(Cultura != "" & !is.na(Cultura)) %>%
  count(Cultura, sort = TRUE) %>%
  slice_head(n = 5) %>%
  pull(Cultura)

# processando dados para os pie charts
df_piechart_data <- df %>%
  filter(Cultura %in% top5_culturas & Meio != "" & !is.na(Meio)) %>%
  count(Cultura, Meio) %>%
  group_by(Cultura) %>%
  mutate(
    rank = dense_rank(desc(n)), # rank para pegar os top 5 meios
    Meio_grupo = ifelse(rank <= 5, Meio, "Outros"),
    Meio_grupo = factor(Meio_grupo) # convertendo para fator
  ) %>%
  group_by(Cultura, Meio_grupo) %>%
  summarise(contagem = sum(n), .groups = 'drop') %>%
  group_by(Cultura) %>%
  mutate(
    porcentagem = round(contagem / sum(contagem) * 100, 1),
    Meio_grupo = fct_reorder(Meio_grupo, porcentagem, .desc = TRUE)
  ) %>%
  # ordenando os dados para que as fatias do piechart também sigam a ordem da legenda
  arrange(Cultura, desc(porcentagem))

# criando diretorio para salvar as imagens
dir.create("trabalho1/imagens/piecharts_culturas", showWarnings = FALSE, recursive = TRUE)

# definindo cores
cores_piechart <- c("#377EB8", "#4DAF4A", "#E41A1C", "#984EA3", "#FF7F00", "#A65628", "#F781BF", "#F1C232") # Adicionada mais uma cor caso 'Outros' seja frequente

# gerando um piechart para cada cultura
for (cult_idx in seq_along(top5_culturas)) {
  cultura_atual <- top5_culturas[cult_idx]
  
  dados_cultura_atual <- df_piechart_data %>%
    filter(Cultura == cultura_atual)
  
  # criando o piechart
  grafico <- ggplot(dados_cultura_atual, 
                    aes(x = "", y = porcentagem, fill = Meio_grupo)) +
    geom_bar(stat = "identity", width = 1, color = "white", linewidth = 0.6) +
    coord_polar("y", start = 0) +
    geom_text(
      aes(label = ifelse(porcentagem > 3, paste0(porcentagem, "%"), "")),
      position = position_stack(vjust = 0.5),
      color = "white",
      fontface = "bold",
      size = 4.5
    ) +
    scale_fill_manual(values = cores_piechart) +
    labs(
      title = paste("Cultura:", cultura_atual),
      subtitle = "Distribuição dos materiais",
      fill = "Material"
    ) +
    theme_bw(
      base_size = 14 # tamanho base da fonte para o tema
    ) +
    theme(
      plot.title = element_text(hjust = 0.5, size = 18, face = "bold"),
      plot.subtitle = element_text(hjust = 0.5, size = 14, margin = margin(b = 15)),
      legend.position = "bottom",
      legend.title = element_text(size = 12, face = "bold"),
      legend.text = element_text(size = 10),
      legend.key.size = unit(0.7, "cm"),
      panel.grid = element_blank(),
      axis.text = element_blank(),
      axis.ticks = element_blank(),
      axis.title = element_blank(),
      panel.border = element_blank(), 
      plot.background = element_rect(fill = "white", colour = "white"),
      plot.margin = margin(1, 1, 1, 1, "cm") # adicionando margem ao redor do grafico
    )
  
  # nome do arquivo para salvar
  nome_arquivo <- paste0("trabalho1/imagens/piecharts_culturas/piechart_", 
                         gsub("[^a-zA-Z0-9_]", "_", tolower(cultura_atual)), ".png")
  
  # salvando a visualizacao individual
  ggsave(
    filename = nome_arquivo,
    plot = grafico,
    width = 30,
    height = 20,
    dpi = 300,
    units = "cm",
    bg = "white"
  )
  
} 