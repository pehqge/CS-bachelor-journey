import sys
from itertools import combinations

class Grafo:
    def __init__(self) -> None:
        self.vertices = {}
        self.arestas = {}

    def cria_vertice(self, rotulo: str) -> None:
        self.vertices[rotulo] = Vertice(rotulo)

    def qtdVertices(self) -> int:
        return len(self.vertices)
    
    def qtdArestas(self) -> int:
        return len(self.arestas)

    def grau(self, v: str) -> int:
        return self.vertices[v].grau
    
    def rotulo(self, v: str) -> str:
        return self.vertices[v].rotulo
    
    def vizinhos(self, v: str) -> list:
        return self.vertices[v].vizinhos
    
    def haAresta(self, u: str, v: str) -> bool:
        return v in self.vertices[u].vizinhos
    
    def peso(self, u: str, v: str) -> float:
        return self.arestas.get((u, v), float('inf'))
    
    def limpar_atributos(self):
        for v in self.vertices.values():
            v.acessado = False
            v.distancia = float('inf')
            v.anterior = None
            v.tempo = float('inf')
            v.ordem = float('inf')
    
    def get_vertice(self, rotulo):
        return self.vertices.get(rotulo, None)


class GrafoDirigido(Grafo):
    def cria_aresta(self, u: str, v: str, peso: float) -> None:
        if u not in self.vertices:
            self.cria_vertice(u)
        if v not in self.vertices:
            self.cria_vertice(v)
    
        self.vertices[u].adiciona_vizinho(v)
        self.arestas[(u, v)] = peso

    def inverter_arestas(self):
        arestas_invertidas = {}
        for (u, v), peso in self.arestas.items():
            arestas_invertidas[(v, u)] = peso
            self.vertices[u].remove_vizinho(v)
            self.vertices[v].adiciona_vizinho(u)
        self.arestas = arestas_invertidas

class GrafoNaoDirigido(Grafo):
    def cria_aresta(self, u: str, v: str, peso: float) -> None:
        if u not in self.vertices:
            self.cria_vertice(u)
        if v not in self.vertices:
            self.cria_vertice(v)
    
        self.vertices[u].adiciona_vizinho(v)
        self.vertices[v].adiciona_vizinho(u)
        self.arestas[(u, v)] = peso
        self.arestas[(v, u)] = peso
        
    def subgrafo(self, vertices):
        subgrafo = GrafoNaoDirigido()
        for v in vertices:
            v = self.get_vertice(v)
            subgrafo.cria_vertice(v.rotulo)
            for u in v.vizinhos:
                if u in vertices:
                    subgrafo.cria_aresta(v.rotulo, u, self.peso(v.rotulo, u))
        return subgrafo
    
    def conjuntos_independentes(grafo):
        n = len(grafo.vertices)
        vertices = list(grafo.vertices)
        S = [set(vertices[i] for i in range(n) if (mask & (1 << i))) for mask in range(1 << n)]
        S.sort(key=len, reverse=True) 
        R = []

        for X in S:
            c = True
            for v in X:
                for u in X:
                    if u != v and u in grafo.vizinhos(v):
                        c = False
                        break
                if not c:
                    break

            if c:
                R.append(X)
                S = [Y for Y in S if not Y.issubset(X)]

        return R
        
class GrafoBipartido(GrafoNaoDirigido):
    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        
        self.X = set()
        self.Y = set()
    
    def cria_vertice(self, rotulo: str, total: int) -> None:
        vertice = Vertice(rotulo)
        self.vertices[rotulo] = vertice
        
        if self.count < total // 2:
            self.X.add(vertice)
        else:
            self.Y.add(vertice)
            
        self.count += 1
                        
class Vertice:
    def __init__(self, rotulo: str) -> None:
        self.rotulo = rotulo
        self.vizinhos = []
        self.grau = 0

        self.acessado = False
        self.distancia = float('inf')
        self.mate = None
        self.anterior = None
        self.tempo = float('inf')
        self.ordem = float('inf')

        self.titulo = None
        self.cd = None

    def adiciona_vizinho(self, vizinho) -> None:
        self.vizinhos.append(vizinho)
        self.incrementa_grau()

    def remove_vizinho(self, vizinho) -> None:
        self.vizinhos.remove(vizinho)
        self.decrementa_grau()

    def decrementa_grau(self) -> None:
        self.grau -= 1
    
    def incrementa_grau(self) -> None:
        self.grau += 1

    def __lt__(self, other):
        if isinstance(other, Vertice):
            return self.distancia < other.distancia
        return self.distancia < other


class Auxiliar:
    def __init__(self, arquivo: str, type: str) -> None:
        self.arquivo = arquivo

        if type == "bipartido":
            self.grafo = GrafoBipartido()
        elif type == "dirigido":
            self.grafo = GrafoDirigido()
        elif type == "naodirigido":
            self.grafo = GrafoNaoDirigido()
        else:
            raise ValueError("Tipo de grafo inválido")

        self.ler(type)

    def ler(self, type) -> None:
        with open(self.arquivo, 'r') as net:
            linhas = net.readlines()

            linha_tmp = linhas[0].strip().split(' ')[1]
            num_vertices = int(linha_tmp)

            linhas_vertices = linhas[1:num_vertices + 1]
            linhas_arcos = [linha for linha in linhas[1 + num_vertices + 1:] if linha != "\n"]

            for linha in linhas_vertices:
                rotulo = linha.strip().split(' ')[0]
                
                if type == "bipartido":
                    self.grafo.cria_vertice(rotulo, len(linhas_vertices))
                else:
                    self.grafo.cria_vertice(rotulo)
                    
                tituloStr = (' '.join(linha.strip().split(' ')[1:])).strip('"')
                self.grafo.vertices[rotulo].titulo = tituloStr

            for linha in linhas_arcos:
                u, v, peso = linha.strip().split(' ')
                self.grafo.cria_aresta(u, v, float(peso))
            

if __name__ == '__main__':
    arquivo = sys.argv[1]
    bipartido = True if sys.argv[2] == "bipartido" else False
    aux = Auxiliar(arquivo, type = "bipartido" if bipartido else "naodirigido")