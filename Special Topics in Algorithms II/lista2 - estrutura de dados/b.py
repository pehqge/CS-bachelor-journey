lista = []

def median(lista):
    lista.sort()
    n = len(lista)
    if n % 2 == 0:
        return (lista[n//2 - 1] + lista[n//2]) / 2
    else:
        return lista[n//2]

while True:
    try:
        x = int(input())
        lista.append(x)
        print(int(median(lista)))
    except EOFError:
        break