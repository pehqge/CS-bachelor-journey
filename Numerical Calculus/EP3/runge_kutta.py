"""Arquivo com a solução do EP3"""

import numpy as np
import matplotlib.pyplot as plt

def dSdt(S, I, beta):
    return -beta * S * I

def dIdt(S, I, beta, gamma):
    return beta * S * I - gamma * I

def dRdt(I, gamma):
    return gamma * I

def rk4(S0, I0, R0, t0, tf, h, beta, gamma):
    """Método de Runge-Kutta de 4ª ordem para resolver o sistema de EDOs do modelo SIR."""

    t = np.arange(t0, tf + h, h)
    n = len(t)
    S, I, R = np.zeros(n), np.zeros(n), np.zeros(n)
    S[0], I[0], R[0] = S0, I0, R0


    for i in range(1, n):
        k1s = dSdt(S[i - 1], I[i - 1], beta)
        k1i = dIdt(S[i - 1], I[i - 1], beta, gamma)
        k1r = dRdt(I[i - 1], gamma)

        k2s = dSdt(S[i - 1] + (k1s * h) / 2,
                   I[i - 1] + (k1i * h) / 2,
                   beta)
        k2i = dIdt(S[i - 1] + (k1s * h) / 2,
                   I[i - 1] + (k1i * h) / 2,
                   beta, gamma)
        k2r = dRdt(I[i - 1] + (k1i * h) / 2,
                   gamma)

        k3s = dSdt(S[i - 1] + (k2s * h) / 2,
                   I[i - 1] + (k2i * h) / 2,
                   beta)
        k3i = dIdt(S[i - 1] + (k2s * h) / 2,
                   I[i - 1] + (k2i * h) / 2,
                   beta, gamma)
        k3r = dRdt(I[i - 1] + (k2i * h) / 2,
                   gamma)

        k4s = dSdt(S[i - 1] + k3s * h,
                   I[i - 1] + k3i * h,
                   beta)
        k4i = dIdt(S[i - 1] + k3s * h,
                   I[i - 1] + k3i * h,
                   beta, gamma)
        k4r = dRdt(I[i - 1] + k3i* h,
                   gamma)

        S[i] = S[i - 1] + h * (k1s + (2 * k2s) + (2 * k3s) + k4s) / 6
        I[i] = I[i - 1] + h * (k1i + (2 * k2i) + (2 * k3i) + k4i) / 6
        R[i] = R[i - 1] + h * (k1r + (2 * k2r) + (2 * k3r) + k4r) / 6

    return t, S, I, R

# Parâmetros do modelo SIR. 24 foi dividido por 24 para converter de horas para dias
beta = 10 / (40 * 8 * (24 / 24))
gamma = 3 / (15 * (24 / 24))

# Simulação 1: Parâmetros originais
t, S1, I1, R1 = rk4(S0=49, I0=1, R0=0, t0=0, tf=25, h=0.1, beta=beta, gamma=gamma)

# Simulação 2: Beta reduzido pela metade
beta_reduced = beta / 2

t, S2, I2, R2 = rk4(S0=49, I0=1, R0=0, t0=0, tf=25, h=0.1, beta=beta_reduced, gamma=gamma)

# Plotagem dos resultados
plt.figure(figsize=(12, 5))

plt.subplot(121)
plt.plot(t, S1, 'b', label='Suscetíveis')
plt.plot(t, I1, 'r', label='Infectados')
plt.plot(t, R1, 'g', label='Removidos')
plt.title('Simulação 1: Parâmetros originais')
plt.xlabel('Tempo (dias)')
plt.ylabel('População')
plt.legend()

plt.subplot(122)
plt.plot(t, S2, 'b', label='Suscetíveis')
plt.plot(t, I2, 'r', label='Infectados')
plt.plot(t, R2, 'g', label='Removidos')
plt.title('Simulação 2: Beta reduzido')
plt.xlabel('Tempo (dias)')
plt.ylabel('População')
plt.legend()

plt.tight_layout()
plt.show()
