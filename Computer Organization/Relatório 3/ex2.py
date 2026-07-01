def soma_recursiva(vet, n):
    if n == 0:
        return 0
    else:
        return vet[n - 1] + soma_recursiva(vet, n - 1)

vetor = input("Digite um vetor de entrada: ").split()
vetor = [int(elemento) for elemento in vetor]
N = len(vetor)

resultado = soma_recursiva(vetor, N)
print("Soma:", resultado)
