# nessa, eu comeco inicializando os valores das colunas inicias e depois vou pedindo para ele somar ao total os valores da linha i e as colunas desejadas da lista
# depois, eu adiciono 2 valores: o antes do primeiro e o depois do ultimo nas colunas
# e depois ele confere se é soma ou media e realiza a operacao desejada

matriz = []
colunas = [5, 6]
valor = input()
total = 0
for i in range(12):
  minimatriz = []
  for i in range(12):
    minimatriz.append(float(input()))
  matriz.append(minimatriz)
for i in range(7, 12):
  for j in colunas:
    total += matriz[i][j]
  colunas.insert(0, colunas[0]-1)
  colunas.append(colunas[-1]+1)
if valor == 'S':
  print(f"{total:.1f}")
else:
  print(f"{total/30:.1f}")