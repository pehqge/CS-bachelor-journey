from cmath import inf
from auxiliar import*
import os

class cfc:
    def __init__(self, grafo: Grafo):
        self.grafo = grafo
        self.tempo_final = {}
        self.visitados = {}
        self.componentes = []

    def run(self):
        self.DFS()  # Primeira DFS para calcular tempos finais
        grafo_transposto = self.transposicao()  # Transpõe o grafo
        self.DFS_transposto(grafo_transposto)  # Segunda DFS no grafo transposto para as CFCs
        self.print_saida()

    def DFS(self):
        self.tempo_final = {}
        self.visitados = {v: False for v in self.grafo.vertices.keys()}
        tempo = [0]  # Para manter o tempo como referência mutável

        for v in self.grafo.vertices.keys():
            if not self.visitados[v]:
                self.DFS_visit(v, tempo)

    def DFS_visit(self, v, tempo):
        self.visitados[v] = True
        tempo[0] += 1  # Incrementa o tempo inicial

        for vizinho in self.grafo.vizinhos(v):
            if not self.visitados[vizinho]:
                self.DFS_visit(vizinho, tempo)

        tempo[0] += 1  # Incrementa o tempo final
        self.tempo_final[v] = tempo[0]

    def transposicao(self):
        grafo_transposto = Grafo()
        for vertice in self.grafo.vertices:
            grafo_transposto.cria_vertice(vertice)

        for (u, v) in self.grafo.arestas:
            grafo_transposto.cria_aresta(v, u)  # Inverte direção da aresta

        return grafo_transposto

    def DFS_transposto(self, grafo_transposto):
        # Ordena vértices pela ordem decrescente do tempo final
        vertices_ordenados = sorted(self.tempo_final, key=self.tempo_final.get, reverse=True)

        self.visitados = {v: False for v in self.grafo.vertices.keys()}  # Reseta a lista de visitados

        for v in vertices_ordenados:
            if not self.visitados[v]:  # Se não foi visitado, é o início de uma nova CFC
                componente = []
                self.DFS_visit_transposto(grafo_transposto, v, componente)
                self.componentes.append(componente)  # Adiciona a nova componente

    def DFS_visit_transposto(self, grafo, v, componente):
        self.visitados[v] = True
        componente.append(v)  # Adiciona o vértice à componente

        for vizinho in grafo.vizinhos(v):
            if not self.visitados[vizinho]:
                self.DFS_visit_transposto(grafo, vizinho, componente)

    def print_saida(self):
        for componente in self.componentes:
            componente.sort(reverse=True)  # Ordena cada componente de forma decrescente
            print(', '.join(componente))


# main principal
def main():
    arquivo = os.path.join(os.path.dirname(__file__), '../testes/cfc.net')
    aux = Auxiliar(arquivo, ponderado=False)
    grafo = aux.grafo

    componente_fortemente_conexa = cfc(grafo)
    componente_fortemente_conexa.run()

main()
# python3 auxiliar.py "../pequenas/email.net"