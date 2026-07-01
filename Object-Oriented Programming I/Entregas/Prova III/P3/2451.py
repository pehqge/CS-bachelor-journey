# nessa, comeco adicionando os valores do pacman na lista chamada pacman
# depois, vou interando em cada linha do pacman. Se a linha for par, ele anda da esquerda para a direita. E impar, ao contrario
# se ele encontra um 'o' no caminho, ele adiciona 1 no contador de frutas atuais
# se encontrar um 'A', ele adiciona a lista de totais de frutas o numero do contador e reseta o contador
# no final, ele procura o maximo da lista para saber qual eh o maximo de frutas possiveis

n = int(input())
pacman = []
totais = []
contador = 0
for i in range(n):
  pacman.append(list(input().strip()))
for i in range(n):
  if i%2 == 0 or i == 0:
    for j in range(n):
      if pacman[i][j] == 'o':
        contador+=1
      elif pacman[i][j] == 'A':
        totais.append(contador)
        contador = 0
  else:
    for j in range(n-1, -1, -1):
      if pacman[i][j] == 'o':
        contador+=1
      elif pacman[i][j] == 'A':
        totais.append(contador)
        contador = 0
totais.append(contador)
print(max(totais))