import numpy as np
import random

def sad_V1(lista1, lista2):
    return np.sum(np.abs(np.array(lista1) - np.array(lista2)))

def sad_V3(lista1, lista2):
    resultado = 0
    for i in range(len(lista1)):
        resultado += sad_V1(lista1[i], lista2[i])
    return resultado

def gera_estimulo(arquivo):
    # criacao de listas com 4 numeros aleatorios de 8 bits
    MemA = [random.sample(range(0, 255), 4) for _ in range(16)]
    MemB = [random.sample(range(0, 255), 4) for _ in range(16)]
    
    # realiza os calculos
    sad = sad_V3(MemA, MemB)
    
    # converte a lista original para binario
    MemA_bin = [[format(x, '08b') for x in y] for y in MemA]
    MemB_bin = [[format(x, '08b') for x in y] for y in MemB]
    
    for i in range(len(MemA_bin)):
        arquivo.write(''.join(MemA_bin[i]) + ' ' + ''.join(MemB_bin[i]) + ' ')
    arquivo.write(format(sad, '014b') + '\n')

# escreve em resultado.txt 50 vezes
with open('estimulos.dat', 'w') as f:
    for _ in range(50):
        gera_estimulo(f)