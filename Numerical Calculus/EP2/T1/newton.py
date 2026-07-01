import numpy as np


def newton(x, y, jacobian, f1, f2, max_iter):
    """
    Método de Newton.
    x: valor inicial para x.
    y: valor inicial para y.
    jacobian: função que retorna a matriz jacobiana.
    f1 e f2: funções que retornam os valores de f1(x, y) e f2(x, y).
    """

    for _ in range(max_iter):
        F = np.array([f1(x, y), f2(x, y)])
        J = jacobian(x, y)
        delta = np.linalg.solve(J, -F)

        x += delta[0]
        y += delta[1]

    return x, y
