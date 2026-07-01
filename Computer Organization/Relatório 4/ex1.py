def raiz_quadrada(x, n):
    # Estimativa inicial
    estimativa = 1.0

    # Loop para calcular n valores de estimativa
    for _ in range(n):
        # Calcula a nova estimativa usando o método de Newton
        estimativa = (( x / estimativa)+estimativa) / 2.0

    return estimativa

def main():
    # Solicita o número e a quantidade de iterações ao usuário
    x = float(input("Digite o número para calcular a raiz quadrada: "))
    n = int(input("Digite o número de iterações desejadas: "))

    # Calcula a estimativa da raiz quadrada usando o método de Newton
    estimativa_final = raiz_quadrada(x, n)

    # Exibe o resultado
    print(f"A estimativa da raiz quadrada de {x} após {n} iterações é: {estimativa_final}")

if __name__ == "__main__":
    main()
