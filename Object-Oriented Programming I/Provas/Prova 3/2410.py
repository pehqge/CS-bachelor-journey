# aqui eu só criei uma lista e fui adicionando cada valor nela e no final fiz um set para remover todos os repetidos. Então só imprimi o tamanho desse set.
n = int(input())
lista = []
for i in range(n):
    lista.append(int(input()))
print(len(set(lista)))
    