# minha ideia aqui foi ficar adicionando a uma variavel a soma de todos os inputs que ele ia me dando e depois printei a divisao do total por 60 para me dar as sacas e o resto dessa divisao para me dar os litros
while True:
    try:
        matriz = []
        total = 0
        m, n = map(int, input().split())
        for i in range(m):
            total += sum(list(map(int, input().split())))
        sacas = total//60
        litros = total%60
        print(f"{sacas} saca(s) e {litros} litro(s)")
    except EOFError:
        break