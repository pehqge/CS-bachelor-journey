
from A1_1 import Grafo
import auxiliar

def buscaEmLargura(grafo : Grafo, s : str):
    # Padrão de entrada:
    # 0: 8
    # 1: 3,4,5
    # 2: 1,2,6,7

    # Acessa o vértice de origem
    try:
        s = grafo.vertices[s]
        s.acessado = True
        s.distancia = 0
    except KeyError:
        return KeyError(f'O vértice {s} não existe no grafo')
    
    # Fila de vértices a serem visitados
    fila = []
    fila.append(s)

    # Dicionario de niveis
    niveis = {}

    while fila:
        # Acessando vértice u
        u = fila.pop(0)
        vizinhos = grafo.vizinhos(u.rotulo)

        # Acessa distância de u
            # Se não existe nível, cria
        if u.distancia not in niveis:
            niveis[u.distancia] = []

        # Adiciona u ao nível correspondente
        niveis[u.distancia].append(u.rotulo)

        for v in vizinhos:
            if not grafo.vertices[v].acessado:
                # Conhecendo v
                grafo.vertices[v].acessado = True
                grafo.vertices[v].distancia = u.distancia + 1
                grafo.vertices[v].anterior = u
                fila.append(grafo.vertices[v])

    # Saida no formato solicitado
    for nivel in sorted(niveis.keys()):
        print(f"{nivel}: {', '.join(niveis[nivel])}")

if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1]
    aux = auxiliar.Auxiliar(arquivo, ponderado = False)
    buscaEmLargura(aux.grafo, sys.argv[2])