# minha ideia aqui foi criar uma lista com todas as figurinhas e depois rodar a função set para tirar as figurinhas repetidas. Nisso imprimo a quantidade de figurinhas unicas e depois a diferença que é a quantidade de repetidas.
n = int(input())
figurinhas = []
for i in range(n):
    figurinhas.append(int(input()))
novas = set(figurinhas)
print(len(novas))
print(n-len(novas))