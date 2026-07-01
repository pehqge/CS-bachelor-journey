import sys
from auxiliar import Auxiliar, Grafo, Vertice

def cfc(grafo: Grafo):
    # Input : Grafo dirigido g=(V,E)
    C, T, A, F = DFS(grafo)

    grafoT = transpor_grafo(grafo)

    Ct, Tt, At, Ft = DFS_adaptado(grafoT, F)

    # print(f' At refornado por DFS_adaptado: {At}')

    floresta = separa_arvores(At)

    return floresta

def DFS(grafo: Grafo):
    # Input : Grafo dirigido g=(V,E)
    # configuração dos vértices feita no construtor da classe
    C, T, A, F = [], {}, {}, {}
    tempo = 0
    for u in grafo.vertices.values():
        if not u.acessado:
            tempo = DFS_visit(grafo, u, C, T, A ,F, tempo)

    return C, T, A, F

def transpor_grafo(grafo: Grafo):
    grafoT = Grafo()

    # cria vértices no grafo transposto
    for rotulo, vertice in grafo.vertices.items():
        grafoT.cria_vertice(rotulo)

    # inverte as arestas
    for (u,v), peso in grafo.arestas.items():
        grafoT.cria_aresta(v, u, peso)
    # print(f'grafoT: {grafoT.arestas}, vertices: {grafoT.vertices}')
    return grafoT

    
def DFS_adaptado(grafo: Grafo, F: list[int]):
    tempo = 0

    # cria uma lista dos vértices em ordem decrescente de tempo de término
    vertices_ordenados = sorted(grafo.vertices.values(), key=lambda v: v.tempo_fim, reverse=True)

    C = [False] * grafo.qtdVertices()
    T, A, F =  {}, {}, {}

    for u in vertices_ordenados:
        if not u.acessado:
            tempo = DFS_visit(grafo, u, C, T, A, F, tempo)

    return C, T, A, F

def DFS_visit(grafo: Grafo, v: Vertice, C, T, A, F: dict, tempo):
    v.acessado = True
    tempo += 1
    v.tempo_inicio = tempo
    C.append(v.acessado)

    # Armazenar o tempo de início
    T[v.rotulo] = tempo

    for vizinho_rotulo in v.vizinhos:
        u = grafo.vertices[vizinho_rotulo]
        if not u.acessado:
            u.anterior = v
            A[u.rotulo] = v.rotulo  # Armazenar o predecessor
            tempo = DFS_visit(grafo, u, C, T, A, F, tempo)

    tempo += 1
    v.tempo_fim = tempo
    F[v.rotulo] = tempo  # Armazenar o tempo de término

    return tempo


def separa_arvores(At):
    componentes = []
    visitados = set()

    for k in At.keys():
        if k not in visitados:
            aux = []
            aux.append(k)
            visitados.add(k)
            aux.extend(print_recursiva(k, At, visitados))
            componentes.append(aux)

    for componente in componentes:
        print(', '.join(componente))

def print_recursiva(k, At, visitados):
    lista = []
    for i, v in At.items():
        if k == v:
            if i not in visitados:
                lista.append(i)
                visitados.add(i)
                lista.extend(print_recursiva(i, At, visitados))
    return lista

def main():
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, ponderado=False)
    floresta = cfc(aux.grafo)
    # print_(floresta)  # Imprime as árvores da floresta

if __name__ == '__main__':
    main()