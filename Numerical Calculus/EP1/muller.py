# AUTORES: João Vitor Curcio Sutter e Pedro Henrique Gimenez


from typing import Callable


def muller(f: Callable, x0: int | float, x1: int | float, x2: int | float) -> float:
    print("Iniciando algoritmo de Muller...")
    tolerancia = 0.01
    max_iteracoes = 1000

    x = x2
    it = 2

    while (abs(f(x)) > tolerancia and it < max_iteracoes):
        q0 = (f(x0) - f(x2)) / (x0 - x2)
        q1 = (f(x1) - f(x2)) / (x1 - x2)

        a = (q0 - q1) / (x0 - x1)
        b = q0 * (x2 - x1)/(x0 - x1) + q1 * (x0 - x2) / (x0 - x1)
        c = f(x2)

        delta = (b ** 2 - 4 * a * c) ** (1 / 2)
        sinal = b / abs(b)
        x = x2 - (2 * c) / (b + sinal * delta)

        x0 = x1
        x1 = x2
        x2 = x

        it += 1

    print("O algoritmo foi executado com sucesso!")
    print("Valor aproximado da raíz: " + str(x) + "\n")


def f(x):
    # x^4 - 3x^3 + x^2 + x + 1

    return x ** 4 - 3 * (x ** 3) + x ** 2 + x + 1

# Raíz real 1
muller(f, 1.2, 1.3, 1.5)

# Raíz real 2
muller(f, 2.2, 2.1, 2.4)

# Raíz complexa
muller(f, -0.5, 0, 0.5)
