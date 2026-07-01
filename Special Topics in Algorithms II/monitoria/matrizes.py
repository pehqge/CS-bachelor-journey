matriz = [[1, 2, 3], 
          [4, 5, 6], 
          [3, 8, 9]]


# pegando a posicao
for i in range(len(matriz)): # pega a quantidade de linhas na matriz
    for j in range(len(matriz[0])): # pega a quantidade de colunas na matriz
        if matriz[i][j] == 3:
            print(f"Encontrou 3 na posição [{i}][{j}]")
        
        
        
# criando uma matriz 

# jeito 1
matriz = []

for i in range(5):
    linha = []
    for j in range(5):
        linha.append(0)
    matriz.append(linha)

# jeito 2
matriz = [[0 for i in range(5)] for j in range(5)]


# adicionar elementos
matriz[5][4] = 3


# pegando o item em si
for linha in matriz:
    for item in linha:
        continue