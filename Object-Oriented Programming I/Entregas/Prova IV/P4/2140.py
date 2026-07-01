#crio uma funcao que realiza o troco para gilberto e a cada maior nota descontada do troco, ele incrementa 1 no contador
# se o resultado final for 0, ou seja o troco foi bem sucedido, e o contador for exatamente 2, entao o troco é possivel

def ctroco(t):
    notas = [100, 50, 20, 10, 5, 2]
    contador = 0
    for i in notas:
        while t>= i and t-i>=0:
            contador += 1
            t -= i
    if t == 0 and contador == 2:
        return "possible"
    else:
        return "impossible"
while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    troco = m-n #valor que tem que trocar
    print(ctroco(troco))