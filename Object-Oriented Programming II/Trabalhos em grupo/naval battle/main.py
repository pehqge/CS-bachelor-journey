from barco import Barcos

#inicializa os barcos do computador  
computador= Barcos()
computador.gerador_ai()

# inicializa os barcos do jogador
jogador=Barcos()
for i in range(1, 9):
  jogador.escolha_jogador(i)
  
# jogo principal rodando
while True:
  print(computador.meus_barcos)
  jogador.jogador_ataque(computador.meus_barcos) #turno do jogador
  if jogador.contador==8:
    exit()
    
  computador.maquina_ataque(jogador.meus_barcos) #turno da maquina
  if computador.contador==8:
    exit()