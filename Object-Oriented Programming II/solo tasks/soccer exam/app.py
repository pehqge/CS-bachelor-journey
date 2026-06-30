from campeonato import Campeonato

campeonato = Campeonato("PROVA FINAL POO2")

# Crie 8 equipes
for i in range(8):
    campeonato.adicionar_equipe(f"Equipe {i+1}", f"Treinador {i+1}")

# Crie 2 grupos
for i in range(2):
    campeonato.criar_grupo(f"Grupo {i+1}")

# Atribua 4 equipes distintas a cada grupo
for i in range(4):
    campeonato.atribuir_equipe(f"Equipe {i+1}", "Grupo 1")
    campeonato.atribuir_equipe(f"Equipe {i+5}", "Grupo 2")


# Adicione 4 jogos e seus resultados para cada grupo
""" Professor, eu não entendi muito bem essa pergunta e também não entendo como funciona classificação de futebol. 
Então, eu assumi que a fase de grupos são os jogos dentro do grupo e que a pontuação da partida vai para cada equipe ganhadora."""

campeonato.criar_partida("Equipe 1", 2, "Equipe 2", 6) # vitoria equipe 2
campeonato.criar_partida("Equipe 3", 1, "Equipe 4", 1) # empate equipe 3 e 4
campeonato.criar_partida("Equipe 5", 8, "Equipe 6", 5) # vitoria equipe 5
campeonato.criar_partida("Equipe 7", 7, "Equipe 8", 6) # vitoria equipe 7


# Mostre as seleções participantes do campeonato
for i in range(2):
    campeonato.mostrar_equipes_grupo(f"Grupo {i+1}")
print()

# Mostre a classificação por grupo
for i in range(2):
    campeonato.mostrar_classificacao_grupo(f"Grupo {i+1}")
    print()
