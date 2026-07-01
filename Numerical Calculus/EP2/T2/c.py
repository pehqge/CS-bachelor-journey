import numpy as np
import matplotlib.pyplot as plt

# Dados da tabela
r = np.array([2.70, 2.00, 1.61, 1.20, 1.02])
theta = np.deg2rad(np.array([48, 67, 83, 108, 126]))  # Convertendo ângulos para radianos

# Função que define a lei de Kepler
def g(theta, a):
    return a[0] / (1 - a[1] * np.cos(theta))

# Função que calcula o resíduo
def residual(a):
    return r - g(theta, a)

# Função que calcula a matriz Jacobiana
def jacobian(a):
    n = len(theta)
    
    J = np.zeros((n, 2))
    J[:, 0] = 1 / (1 - a[1] * np.cos(theta))  # Derivada em relação a a0
    J[:, 1] = a[0] * np.cos(theta) / (1 - a[1] * np.cos(theta)) ** 2  # Derivada em relação a a1
    return J

# Implementação do método de Gauss-Newton
def gauss_newton(a0, tol=1e-6, itmax=100):
    a = a0
    erro = 1
    it = 0
    while erro > tol and it < itmax:
        # Calcula o resíduo e a matriz Jacobiana
        r = residual(a)
        J = jacobian(a)

        # Calcula a atualização dos parâmetros
        JTJ = J.T @ J
        JTr = J.T @ r
        s = np.linalg.solve(JTJ, JTr)

        # Atualiza os parâmetros e o erro
        a = a + s
        erro = np.max(np.abs(s))
        it += 1

    return a, it

# Chute inicial
a0 = np.array([2, 1])

# Aplica o método de Gauss-Newton
a, it = gauss_newton(a0)

# Imprime os resultados
print("Parâmetros otimizados:", a)
print("Número de iterações:", it)

# Calcula o resíduo final
r_final = residual(a)

# Imprime o resíduo final
print("Resíduo final:", r_final)

# Plota os dados originais e a curva ajustada
plt.plot(theta, r, 'o', label='Dados originais')
theta_fit = np.linspace(theta.min(), theta.max(), 100)
plt.plot(theta_fit, g(theta_fit, a), '-', label='Curva ajustada (Gauss-Newton)')
plt.xlabel('theta (rad)')
plt.ylabel('r')
plt.legend()
plt.show()