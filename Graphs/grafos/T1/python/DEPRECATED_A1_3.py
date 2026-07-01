
from A1_1 import Grafo
import auxiliar

def dfs(grafo : Grafo, u : str, visitados : dict):
    visitados[u] = True
    for v in grafo.vizinhos(u):
        if not visitados.get(v):
            dfs(grafo, v, visitados)

def conexo(grafo : Grafo) -> bool:
    visitados = {}
    inicio = next((v for v in grafo.vertices), None)

    if not inicio:
        return False

    dfs(grafo, inicio, visitados)

    return len(visitados) == grafo.qtdVertices()

def existeCicloEuleriano(grafo : Grafo) -> bool:
    if not conexo(grafo):
        return False
    
    for v in grafo.vertices:
        if grafo.grau(v) % 2 != 0:
            return False
    
    return True

def encontrarCicloEuleriano(grafo : Grafo) -> list:
    if not existeCicloEuleriano(grafo):
        return []

    ciclo = []
    pilha = []
    pilha.append(grafo.vertices[0].rotulo)

    while pilha:
        u = pilha[-1]

        if grafo.grau(u) == 0:
            ciclo.append(pilha.pop())
        else:
            for v in grafo.vizinhos(u):
                if grafo.haAresta(u, v):
                    pilha.append(v)
                    grafo.removeAresta(u, v)
                    break
    
    return ciclo

if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1]
    aux = auxiliar.Auxiliar(arquivo, ponderado = False)
    ciclo = encontrarCicloEuleriano(aux.grafo)
    print(ciclo)