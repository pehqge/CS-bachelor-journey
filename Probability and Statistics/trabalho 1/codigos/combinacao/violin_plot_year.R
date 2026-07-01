# carregando bibliotecas que vamos usar
library(ggplot2)
library(dplyr)
library(tidyr)

# carregando o arquivo csv
df <- read.csv("trabalho1/tabela_met.csv", stringsAsFactors = FALSE, check.names = FALSE)

# renomeando as colunas para facilitar o uso no R
names(df)[names(df) == "Is Highlight"] <- "IsHighlight"
names(df)[names(df) == "Object Begin Date"] <- "ObjectBeginDate"

# mudando o tipo das colunas para facilitar o uso
df$ObjectBeginDate <- as.numeric(df$ObjectBeginDate) # numero
df$IsHighlight <- as.logical(df$IsHighlight)       # verdadeiro ou falso

# ----

# criando um dataframe para o grupo de destaques
destaques_plot_data <- data.frame(
  Ano = df$ObjectBeginDate[df$IsHighlight == TRUE],
  Grupo = "Artes em Destaque"
)

# criando um dataframe para o grupo de todas as artes
todas_plot_data <- data.frame(
  Ano = df$ObjectBeginDate,
  Grupo = "Todas as Artes"
)

# juntando os dois dataframes em um só para usar no grafico
plot_df <- rbind(destaques_plot_data, todas_plot_data)

# nomeando os grupos
plot_df$Grupo <- factor(plot_df$Grupo, levels = c("Artes em Destaque", "Todas as Artes"))

# ----

# calculando as estatisticas para as anotações
stats_summary <- plot_df %>%
  group_by(Grupo) %>%
  summarise(
    q1 = quantile(Ano, 0.25, na.rm = TRUE),
    mediana = median(Ano, na.rm = TRUE),
    q3 = quantile(Ano, 0.75, na.rm = TRUE),
    .groups = 'drop' 
  )

# dataframe responsavel por colocar as anotações no grafico
annotations_df <- stats_summary %>%
  pivot_longer(
    cols = c(q1, mediana, q3),
    names_to = "stat_type",
    values_to = "y_pos"
  ) %>%
  mutate(
    label_prefix = case_when(
      stat_type == "q1" ~ "Q1:",
      stat_type == "mediana" ~ "Mediana:",
      stat_type == "q3" ~ "Q3:",
      TRUE ~ stat_type
    ),
    label = paste(label_prefix, round(y_pos)),
    text_color = case_when(
      stat_type == "q1" ~ "blue",
      stat_type == "mediana" ~ "red",
      stat_type == "q3" ~ "#439F43FF",
      TRUE ~ "black"
    )
  )

# ----

violin_plot_ano_destaque <- ggplot(plot_df, aes(x = Grupo, y = Ano, fill = Grupo)) + # criando o grafico
  geom_violin(width = 0.6, alpha = 0.8, show.legend = FALSE) + # violino
  geom_boxplot(width = 0.1, outlier.shape = NA, alpha = 0.9, show.legend = FALSE) + # caixa dentro do violino
  scale_fill_manual(values = c("Artes em Destaque" = "#90ee90", "Todas as Artes" = "#ffb3b3")) + # cores
  geom_text(
    data = annotations_df,
    aes(x = Grupo, y = y_pos, label = label, color = text_color),
    nudge_x = 0.32,
    size = 8,
    hjust = 0
  ) +
  scale_color_identity() +
  labs(
    title = "Ano de Confecção por Destaque",
    x = NULL,
    y = "Ano de Confecção"
  ) +
  
  # ajusta as legendas do eixo y
  scale_y_continuous(breaks = scales::pretty_breaks(n = 15)) +
  theme_bw() + 
  # coisas do tema
  theme(
    panel.grid.major.y = element_line(color = "grey", linetype = "dashed"), 
    panel.grid.minor.y = element_blank(), 
    panel.grid.major.x = element_blank(),
    plot.title = element_text(hjust = 0.5, size = 30, face = "bold"), 
    axis.title.x = element_text(size = 20, face = "bold"),
    axis.title.y = element_text(size = 24, face = "bold"),
    axis.text.x = element_text(size = 24),
    axis.text.y = element_text(size = 20)
  )

# ----

# exibe o grafico
print(violin_plot_ano_destaque)

# salva o grafico como arquivo
ggsave(
  filename = "trabalho1/imagens/violin_plot_ano_destaque.png",
  plot = violin_plot_ano_destaque,
  width = 50,
  height = 50,
  dpi = 300,
  units = "cm"
) 

# ---- INÍCIO: NOVO GRÁFICO APENAS 'TODAS AS ARTES' COM ZOOM ----

# criando um dataframe apenas para o grupo 'todas as artes'
# reutilizando 'todas_plot_data' já criado anteriormente no script
plot_df_todas <- todas_plot_data

# garantindo que 'grupo' seja um fator (embora aqui seja apenas um nível)
# isso ajuda o ggplot a tratar o eixo x corretamente
plot_df_todas$Grupo <- factor(plot_df_todas$Grupo)

# calculando as estatisticas para as anotações para 'todas as artes'
stats_summary_todas <- plot_df_todas %>%
  group_by(Grupo) %>% # 'Grupo' aqui será sempre 'Todas as Artes'
  summarise(
    q1 = quantile(Ano, 0.25, na.rm = TRUE),
    mediana = median(Ano, na.rm = TRUE),
    q3 = quantile(Ano, 0.75, na.rm = TRUE),
    .groups = 'drop' 
  )

# dataframe responsavel por colocar as anotações no grafico para 'todas as artes'
annotations_df_todas <- stats_summary_todas %>%
  pivot_longer(
    cols = c(q1, mediana, q3),
    names_to = "stat_type",
    values_to = "y_pos"
  ) %>%
  mutate(
    label_prefix = case_when(
      stat_type == "q1" ~ "Q1:",
      stat_type == "mediana" ~ "Mediana:",
      stat_type == "q3" ~ "Q3:",
      TRUE ~ stat_type # caso improvável de outros tipos de estatística
    ),
    label = paste(label_prefix, round(y_pos)),
    # definindo cores para as anotações de q1, mediana e q3
    text_color = case_when(
      stat_type == "q1" ~ "blue",
      stat_type == "mediana" ~ "red",
      stat_type == "q3" ~ "#439F43FF", # verde escuro
      TRUE ~ "black" # cor padrão para outros casos
    )
  )

# criando o gráfico de violino para 'todas as artes' com zoom
violin_plot_ano_todas_zoom <- ggplot(plot_df_todas, aes(x = Grupo, y = Ano)) + 
  geom_violin(fill = "#ffb3b3", width = 0.6, alpha = 0.8, show.legend = FALSE) + # usando a cor de 'todas as artes'
  geom_boxplot(width = 0.1, outlier.shape = NA, alpha = 0.9, show.legend = FALSE) + # caixa dentro do violino
  geom_text(
    data = annotations_df_todas,
    aes(x = Grupo, y = y_pos, label = label, color = text_color),
    nudge_x = 0.32, # ajustando a posição horizontal do texto
    size = 7,       # tamanho do texto das anotações
    hjust = 0       # alinhamento horizontal
  ) +
  scale_color_identity() + # aplicando as cores definidas em 'text_color'
  coord_cartesian(ylim = c(1000, 2021)) + # aplicando zoom no eixo y sem remover dados
  labs(
    title = "Gráfico de Violino: Ano de Confecção das Obras (1000-2021)",
    x = NULL, # removendo o rótulo do eixo x pois há apenas um grupo
    y = "Ano de Confecção"
  ) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 12)) + # ajustando os breaks para o novo intervalo do eixo y
  theme_bw() + 
  # aplicando tema similar ao gráfico original
  theme(
    panel.grid.major.y = element_line(color = "grey", linetype = "dashed"), 
    panel.grid.minor.y = element_blank(), 
    panel.grid.major.x = element_blank(), # sem grades verticais
    plot.title = element_text(hjust = 0.5, size = 20, face = "bold"), # ajustando título
    axis.title.x = element_text(size = 18, face = "bold"), # rótulo do eixo x
    axis.title.y = element_text(size = 20, face = "bold"), # rótulo do eixo y
    axis.text.x = element_text(size = 16), # texto do eixo x (nome do grupo)
    axis.text.y = element_text(size = 18)  # texto do eixo y (anos)
  )

# exibe o novo grafico (opcional, pode ser comentado)
# print(violin_plot_ano_todas_zoom)

# salva o novo grafico como arquivo
ggsave(
  filename = "trabalho1/imagens/violin_plot_ano_todas_zoom.png",
  plot = violin_plot_ano_todas_zoom,
  width = 25, # largura ajustada para um único grupo
  height = 20, # altura ajustada
  dpi = 300,
  units = "cm"
) 

# ---- FIM: NOVO GRÁFICO APENAS 'TODAS AS ARTES' COM ZOOM ---- 