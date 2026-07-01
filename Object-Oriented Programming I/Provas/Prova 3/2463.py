# Nessa, começo iniciando dois valores para a busca do maior: o maximo e o a, os dois possuem o valor da primeira casa a ser checada.
# depois faco um loop para ir passando de casa por casa a ser checada, em que o a eh o max da casa checada e o a anterior + a casa checada. (isso serve para manter o valor de a, caso a proxima casa tenha diminuido ele)
# depois, o maximo vai manter o valor entre o maximo ja achado anteriormente e a casa atual que estamos.
# no final, ele imprime o maximo

n = int(input())
lista = list(map(int, input().split()))
a = lista[0]
maximo = lista[0]
for i in range(1, n):
    a = max(lista[i], a + lista[i])
    maximo = max(maximo, a)
print(maximo)