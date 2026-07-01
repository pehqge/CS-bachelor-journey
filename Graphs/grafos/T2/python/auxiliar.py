import sys


class Grafo:
    def __init__(self) -> None:
        self.rotulos = {}
        self.vertices = {}
        self.arestas = {}

    def cria_vertice(self, rotulo: str) -> None:
        if rotulo not in self.vertices:
            self.vertices[rotulo] = Vertice(rotulo)

    def cria_aresta(self, u: str, v: str, peso: float = 1.0) -> None:
        if u not in self.vertices:
            self.cria_vertice(u)
        if v not in self.vertices:
            self.cria_vertice(v)

        # Garante ordenação para aresta não-direcionada e evita duplicação
        if (u, v) not in self.arestas and (v, u) not in self.arestas:
            self.vertices[u].adiciona_vizinho(v)
            self.vertices[v].adiciona_vizinho(u)
            self.arestas[(u, v)] = self.arestas[(v, u)] = peso

    def qtdVertices(self) -> int:
        return len(self.vertices)

    def qtdArestas(self) -> int:
        return len(self.arestas) // 2

    def grau(self, v: str) -> int:
        return self.vertices[v].grau

    def rotulo(self, v: str) -> str:
        return self.vertices[v].rotulo

    def vizinhos(self, v: str) -> list:
        return list(self.vertices[v].vizinhos)

    def haAresta(self, u: str, v: str) -> bool:
        return v in self.vertices[u].vizinhos

    def peso(self, u: str, v: str) -> float:
        return self.arestas.get((u, v), float('inf'))


class Vertice:
    def __init__(self, rotulo: str) -> None:
        self.rotulo = rotulo
        self.vizinhos = set()
        self.grau = 0
        self.acessado = False #Cv
        self.distancia = float('inf')
        self.anterior = None # Av
        self.tempo_inicio = float('inf') #Tv
        self.tempo_fim = float('inf') # Fv

    def adiciona_vizinho(self, vizinho) -> None:
        if vizinho not in self.vizinhos:
            self.vizinhos.add(vizinho)
            self.incrementa_grau()

    def incrementa_grau(self) -> None:
        self.grau += 1

    def __lt__(self, other):
        return isinstance(other, Vertice) and self.distancia < other.distancia


class Auxiliar:
    def __init__(self, arquivo: str, ponderado: bool = False) -> None:
        self.arquivo = arquivo
        self.ponderado = ponderado
        self.grafo = Grafo()
        self.ler()

    def ler(self) -> None:
        try:
            with open(self.arquivo, 'r') as net:
                linhas = net.readlines()
                num_vertices = int(linhas[0].strip().split(' ')[1])
                linhas_rotulos = linhas[1:num_vertices + 1]
                linhas_arestas = [linha for linha in linhas[num_vertices + 2:] if linha.strip()]

                for linha in linhas_rotulos:
                    rotulo = linha.strip().split(' ')[0]
                    self.grafo.cria_vertice(rotulo)

                for linha in linhas_arestas:
                    u, v, *peso = linha.strip().split()
                    peso = float(peso[0]) if self.ponderado and peso else 1.0
                    self.grafo.cria_aresta(u, v, peso)
        except FileNotFoundError:
            print(f"Erro: Arquivo '{self.arquivo}' não encontrado.")
        except ValueError as e:
            print(f"Erro de valor ao ler o arquivo: {e}")

