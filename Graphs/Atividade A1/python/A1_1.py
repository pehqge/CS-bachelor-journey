# Davi Ludvig Longen Machado
# 23100473

import sys


class Grafo:
    def __init__(self) -> None:
        self.vertices = {}
        self.arestas = {}

    def cria_vertice(self, rotulo : str) -> None:
        self.vertices[rotulo] = Vertice(rotulo)

    def cria_aresta(self, u : str, v : str, peso : float) -> None:

        # Checa se os vértices existem, caso contrário, cria-os
        if u not in self.vertices:
            self.cria_vertice(u)
        if v not in self.vertices:
            self.cria_vertice(v)
    
        # Adiciona a aresta entre os vértices (torna-os vizinhos)
            # Adição de vizinho aumenta o grau do vértice
        self.vertices[u].adiciona_vizinho(v)
        self.vertices[v].adiciona_vizinho(u)

        # Adiciona o peso da aresta
            # Adiciona o peso nos dois sentidos, pois o grafo é não-direcionado e facilita acesso
        self.arestas[(u, v)] = peso
        self.arestas[(v, u)] = peso

    # Funções da questão A1_1
    def qtdVertices(self) -> int:
        return len(self.vertices)
    
    def qtdArestas(self) -> int:
        return len(self.arestas)

    def grau(self, v : str) -> int:
        return self.vertices[v].grau
    
    def rotulo(self, v : str) -> str:
        return self.vertices[v].rotulo
    
    def vizinhos(self, v : str) -> list:
        return self.vertices[v].vizinhos
    
    def haAresta(self, u : str, v : str) -> bool:
        return v in self.vertices[u].vizinhos
    
    def peso(self, u : str, v : str) -> float:
        if self.haAresta(u, v):
            return self.arestas[(u, v)]
        return float('inf')
    

    

class Vertice:
    def __init__(self, rotulo : str) -> None:
        self.rotulo = rotulo
        self.vizinhos = []
        self.grau = 0

        # Atributos para busca
        self.acessado = False
        self.distancia = float('inf')
        self.anterior = None

    def adiciona_vizinho(self, vizinho) -> None:
        self.vizinhos.append(vizinho)
        self.incrementa_grau()
    
    def incrementa_grau(self) -> None:
        self.grau += 1

    def __lt__(self, other):
        # Se o outro for um vértice, compara a distância
        if isinstance(other, Vertice):
            return self.distancia < other.distancia
        # Se for um número, compara a distância com o número
        return self.distancia < other
