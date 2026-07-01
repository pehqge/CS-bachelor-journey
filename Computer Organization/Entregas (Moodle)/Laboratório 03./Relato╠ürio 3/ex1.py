def multiplicacao(a,b):
    mult = 0
    for i in range(b):
        mult +=a
    return mult

a = int(input("Defina um valor para a: "))
b = int(input("Defina um valor para b: "))
resultado = multiplicacao(a,b)
print(resultado)