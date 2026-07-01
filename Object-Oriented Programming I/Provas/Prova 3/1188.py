# nessa eu só confiro se as coordenadas dadas pelo problema estao no range de dentro do retangulo, ou seja se x1 <= x <= x2 e se y2 <= y <= y1, ja que ele me deu no problema que x1 eh o menor de todos e o y2 eh o menor de todos.
# e se o ponto esta dentro desse range, eu adiciono um no contador e depois imprimo quantos pontos estavam naquele caso de teste

teste = 0
while True:
    teste += 1
    x1, y1, x2, y2 = map(int, input().split())
    if x1 == 0 and y1 == 0 and x2 == 0 and y2 ==0:
        break
    n = int(input())
    contador = 0
    for i in range(n):
        x, y = input().split()
        x = int(x)
        y = int(y)
        if x >= x1 and x <= x2 and y >= y2 and y <= y1:
            contador += 1
    print(f"Teste {teste}")
    print(contador)