

from A1_1 import Grafo, Vertice
from min_heap import MinHeap
from auxiliar import Auxiliar

def dijstrika(grafo : Grafo, s : Vertice):
    # Inicialização dos vértices feita no construtor
    # Dv ← ∞ ∀v ∈ V
    # Av ← null ∀v ∈ V
    # Cv ← false ∀v ∈ V

    # Ds ← 0
    s.distancia = 0

    # Cria minHeap
    minHeap = MinHeap(maxsize=grafo.qtdVertices())

    minHeap.insert(s)
    minHeap.Print()

    # for i ← 1 to |V| do
    for i in range(grafo.qtdVertices()):
        # u ← Extract-Min(Q)
        u = minHeap.remove()

        # foreach v ∈ N(u) do
        for v in grafo.vizinhos(u.rotulo):
            # if Dv > Du + w(u, v) then
            if grafo.vertices[v].distancia > u.distancia + grafo.peso(u.rotulo, v):
                # Dv ← Du + w(u, v)
                grafo.vertices[v].distancia = u.distancia + grafo.peso(u.rotulo, v)

                # Av ← u
                grafo.vertices[v].anterior = u

                # if Cv = false then
                if not grafo.vertices[v].acessado:
                    # Insert(Q, v)
                    minHeap.insert(grafo.vertices[v])
                    # minHeap.Print()
                    # input()
    
    # return D, A
    # Cada elemento de grafo.vertices esta com o seu antecessor e a distancia ate a raiz

def exibir(grafo : Grafo, s : Vertice):
    """
    1: 2,3,4,1; d=7
    2: 2; d=0
    3: 2,3; d=4
    4: 2,3,4; d=6
    5: 2,3,5; d=8

    Cada linha representa o caminho realizado de s para o vertice da respectiva
linha. Em cada linha, antes dos simbolo “:” deveria estar o vertice destino. A direita de “:”, encontra-se o caminho
percorrido de s ate o vertice destino. Mais a direita encontram-se os simbolos “d=” seguidos da distancia necessaria
para percorrer o caminho.
    """

    for v in grafo.vertices.values():
        caminho = []
        u = v
        while u != s:
            caminho.append(u.rotulo)
            u = u.anterior
        caminho.append(s.rotulo)
        caminho.reverse()
        print(f'{v.rotulo}: {",".join(caminho)}; d={v.distancia}')

if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, ponderado = True)
    dijstrika(aux.grafo, aux.grafo.vertices[sys.argv[2]])
    exibir(aux.grafo, aux.grafo.vertices[sys.argv[2]])