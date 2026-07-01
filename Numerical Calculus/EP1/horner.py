# AUTORES: João Vitor Curcio Sutter e Pedro Henrique Gimenez


def horner(grau: int, coeficientes: list, x0: int | float) -> None:
    print("Iniciando algoritmo de Horner...")

    num_coeficientes = grau + 1
    y = coeficientes[num_coeficientes - 1]
    z = coeficientes[num_coeficientes - 1]

    print("\n" + "----- VALORES DE Y E Z -------")
    for coef_atual in range(num_coeficientes - 2, 0, -1):
        print("-" * 30)
        print("y = " + str(y))
        print("z = " + str(z))

        y = x0 * y + coeficientes[coef_atual]
        z = x0 * z + y

    y = x0 * y + coeficientes[0]

    print("-" * 30)
    print("Valor final de y = " + str(y))
    print("Valor final de z = " + str(z))
    print("Valor obtido para x1: " + str(x0 - y / z) + "\n")


# x^4 - 3x^3 + x^2 + x + 1
# Grau: 4
# a0 a a4: [1, 1, 1, -3, 1]

# Aproximação da raíz 1, x0 = 1.5
horner(4, [1, 1, 1, -3, 1], 1.5)

# Aproximação da raíz 2, x0 = 2.2
horner(4, [1, 1, 1, -3, 1], 2.2)
