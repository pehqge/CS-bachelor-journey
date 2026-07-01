def rafael(x, y): #funcao de rafael
    return (3*x)**2+y**2
def beto(x, y): #funcao do beto
    return 2*(x**2)+(5*y)**2
def carlos(x, y): #funcao do carlos
    return -100*x+y**3

# Depois, eu pego o maximo do resultado das 3 funcoes. E por ultimo, comparo o resultado com cada resultado para ver de quem é o numero. E imprimo a resposta
for i in range(int(input())):
    a, b = map(int, input().split())
    maior = max(rafael(a, b), beto(a, b), carlos(a, b))
    if maior == rafael(a, b):
        print("Rafael ganhou")
    elif maior == beto(a, b):
        print("Beto ganhou")
    else:
        print("Carlos ganhou")