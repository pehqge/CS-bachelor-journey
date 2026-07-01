# aqui eu comecei montando uma matriz cheia de 3 de tamanho nxn. Em seguida coloquei 1's na diagonal principal e depois coloquei 2's na diagonal secundaria.

while True:
    try:
        n = int(input())
        matriz = [[3 for i in range(n)] for j in range(n)]
        for i in range(n):
            matriz[i][i] = 1
            matriz[i][n-1-i] = 2

        for i in matriz:
            print("".join(map(str, i)))
            
    except EOFError:
        break
