# essa questão basicamente busca o mmc das 3 luas
# para fazer o mmc fui pelo principio de fazer 2 primeiro para depois fazer o mmc do resultado dos 2 e do ultimo
# para fazer mmc, é preciso saber qual é o maior valor entre a e b. Depois ver se esse valor divide os dois ao mesmo tempo, se caso não, adiciono o valor do original do maior no i.
# e o i quando dividir os 2 ao mesmo tempo, ele para.
# depois imprimo o valor do mmc dos 3

def mmc(a, b, c):
    def mmc2(x, y):
        maior = max(x, y)
        i = maior
        while True:
            if i % x == 0 and i % y == 0:
                return i
            i += maior
    mmcab = mmc2(a, b)
    return mmc2(mmcab, c)
while True:
    try:
        m = int(input())
        l1, l2, l3 = map(int, input().split())
        total = mmc(l1, l2, l3)
        print(total-m)
    except EOFError:
        break