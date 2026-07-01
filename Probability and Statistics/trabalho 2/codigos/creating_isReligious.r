# Certifique-se de que os pacotes dplyr e stringr estão carregados
# Verifica e instala 'dplyr' se necessário, depois o carrega.
if (!requireNamespace("dplyr", quietly = TRUE)) {
  install.packages("dplyr")
}
library(dplyr)

# Verifica e instala 'stringr' se necessário, depois o carrega.
if (!requireNamespace("stringr", quietly = TRUE)) {
  install.packages("stringr")
}
library(stringr)

# --- Defina a lista de tags religiosas (REFINADA) ---
# Esta lista é usada para identificar se uma obra de arte tem um tema religioso,
# focando em figuras, conceitos e eventos diretamente religiosos.
religious_tags_list <- c(
  "Adoration of the Magi", "Adoration of the Shepherds", "Agony in the Garden",
  "Akshobhya", "Angels", "Annunciation", "Anubis", "Apostles", "Archangel Gabriel",
  "Assumption of the Virgin", "Baptism of Christ", "Bearing the Cross", "Bes",
  "Bible", "Bishops", "Bodhisattvas", "Brahma", "Buddha", "Buddhism",
  "Cain", "Cathedrals", "Ceremonial Objects", "Ceremony", "Chalices",
  "Chapels", "Christ", "Churches", "Circumcision", "Coptic",
  "Coronation of the Virgin", "Cross", "Croziers", "Crucifixion",
  "Daoism", "David", "Deities", "Demeter", "Demons", "Descent from the Cross",
  "Devil", "Doves", "Dragons", "Durga", "Evangelists", "Eve",
  "Flight Into Egypt", "Ganesha", "God the Father", "Goddess", "Gods",
  "Greek Mythology", "Hathor", "Hell", "Hera", "Herakles", "Hercules",
  "Hermes", "Herod", "Hinduism", "Holy Family", "Isis", "Jesus", "Joseph",
  "Judas", "Juno", "Jupiter", "Krishna", "Lamentation", "Last Judgement",
  "Last Supper", "Leda", "Lotuses", "Madonna", "Madonna and Child",
  "Maenads", "Maitreya", "Manjushri", "Marriage of the Virgin", "Mars",
  "Martin Luther", "Mary Magdalene", "Mercury", "Miter", "Monks", "Moses",
  "Mosques", "Mythical Creatures", "Mythology", "Nativity", "Nike", "Noah",
  "Nuns", "Pagodas", "Parables", "Parvati", "Pelicans", "Pilate", "Popes",
  "Praying", "Priests", "Queen of Sheba", "Radha", "Reliquaries", "Resurrection",
  "Ritual Objects", "Rosaries", "Saint Andrew", "Saint Anne", "Saint Anthony",
  "Saint Barbara", "Saint Bartholomew", "Saint Catherine", "Saint Christopher",
  "Saint Francis", "Saint George", "Saint Helena", "Saint Jerome", "Saint John",
  "Saint John the Baptist", "Saint John the Evangelist", "Saint Joseph",
  "Saint Lawrence", "Saint Leonard", "Saint Lucy", "Saint Luke", "Saint Mark",
  "Saint Matthew", "Saint Michael", "Saint Nicholas", "Saint Paul", "Saint Peter",
  "Saint Sebastian", "Saint Ursula", "Saint Zenobius", "Saints", "Shakyamuni",
  "Shepherds", "Shintō", "Shiva", "Sibyl", "Solomon", "Stupas", "Temples",
  "Virgin Mary", "Vishnu", "Visitation", "Zeus"
)

# --- Adicionar a coluna 'Is_Religious' ao seu dataframe 'met_data_religions' ---
# Este código deve ser inserido após todas as outras mutações para o dataframe original
# 'met_data' (como processamento de dimensões, is_sculpture, area/volume),
# mas antes de expandir as tags para 'met_data_tags'.

# Certifique-se de que 'met_data' está carregado ou foi gerado pelos passos anteriores.
# Exemplo (se estiver rodando este código isoladamente para teste):
# met_data <- data.frame(
#   ID = 1:5,
#   Tags = c("Circus|Musicians|Musical Instruments|Men|Women", "Birds", "Madonna|Jesus", NA, "Buddha|Monks"),
#   Is_Highlight = c(TRUE, FALSE, TRUE, FALSE, TRUE) # Exemplo de coluna Is_Highlight
# )


met_data_religions <- met_data %>%
  # Verifica se alguma das tags religiosas está presente na string 'Tags' para cada linha.
  # Constrói um padrão regex unindo todas as tags religiosas com '|' (OR).
  # 'ignore.case = TRUE' pode ser adicionado se a capitalização da tag variar.
  mutate(
    Is_Religious = ifelse(
      is.na(Tags), # Se a coluna Tags for NA, então não é religiosa
      FALSE,       # Caso contrário, defina como FALSE
      str_detect(Tags, paste(religious_tags_list, collapse = "|")) # Verifica se há correspondência
    )
  )

# Agora, 'met_data_religions' conterá o dataframe com a nova coluna 'Is_Religious'.
# Você pode verificar os resultados (opcional):
# print(head(met_data_religions))

