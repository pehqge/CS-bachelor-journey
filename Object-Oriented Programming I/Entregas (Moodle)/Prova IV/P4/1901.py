# nessa, criei uma matriz e fui adicionando os valores para ficar como a matriz de binox.
# depois, fui interando para cada posicao que binox visitou e adicionando o tipo da borboleta numa nova matriz "visitados"
# por ultimo, imprimo a quantidade de elementos unicos da matriz "visitados"

n = int(input())
matriz = []
visitados = []
for i in range(n):
    linha = list(map(int, input().split()))
    matriz.append(linha)
for i in range(n*2):
    a, b = map(int, input().split())
    visitados.append(matriz[a-1][b-1])
print(len(set(visitados)))