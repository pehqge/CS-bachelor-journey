import numpy as np

def minimos_quadrados(r_data, theta_data):
    if len(r_data) != len(theta_data):
        raise ValueError("r_data e theta_data devem ter o mesmo tamanho")
    
    # Criando matriz A
    A1 = len(theta_data)
    A2 = np.sum(np.cos(theta_data))
    A3 = A2
    A4 = np.sum(np.cos(theta_data)**2)
    
    A = np.array([[A1, A2], [A3, A4]])
    
    # Criando matriz B
    B1 = sum(1/i for i in r_data)
    B2 = np.sum(np.cos(theta_data)/r_data)
    
    B = np.array([B1, B2])
    
    # Resolvendo o sistema linear e encontrando b0 e b1
    b0, b1 = np.linalg.solve(A, B)
    
    # Encontrando a0 e a1
    a0 = 1/b0
    a1 = -a0 * b1
    
    return a0, a1, b0, b1
    
def main():
    # Temos que transformar r = a0 / (1 - a1 * cos(theta)) numa equação linear:

    # transformando na forma z = b0 + b1 * cos(theta) ficamos com:
    # 1/r = 1/a0 + a1/a0 * cos(theta)

    # z = 1/r
    # b0 = 1/a0
    # b1 = -a1/a0
    
    r = [2.7, 2, 1.61, 1.2, 1.02]
    theta = [48, 67, 83, 108, 126]
    
    a0, a1, b0, b1 = minimos_quadrados(r, np.radians(theta))
    
    print(f"A equação linear será z = {b0} + ({b1} * cos(theta))")
    print(f"Em que a0 = 1/b0 = {a0} e a1 = -a0 * b1 = {a1}")
    
if __name__ == "__main__":
    main()