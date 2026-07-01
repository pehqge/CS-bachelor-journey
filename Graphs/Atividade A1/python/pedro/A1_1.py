class Grafo:
    def __init__(self, arquivo : str) -> None:
        self.vertices = {}
        self.arestas = {}
        self.ler_arquivo(arquivo)
        
    def adiciona_vertice(self, id : int, rotulo : str) -> None:
        self.vertices[id] = Vertice(id, rotulo)
        
    def adiciona_aresta(self, u : int, v : int, peso : float) -> None:
        self.arestas[(u, v)] = peso
        
        self.vertices[u].adiciona_vizinho(v, peso)
        self.vertices[v].adiciona_vizinho(u, peso)
        
    def get_aresta(self, u : int, v : int):
        if (u, v) in self.arestas.keys():
            return (u, v)
        elif (v, u) in self.arestas.keys():
            return (v, u)
        return None  
        
    def qtdVertices(self) -> int:
        return len(self.vertices)
    
    def qtdArestas(self) -> int:
        return len(self.arestas)//2
    
    def grau(self, v : int):
        return self.vertices[v].grau
    
    def rotulo(self, v : int):
        return self.vertices[v].rotulo
    
    def vizinhos(self, v : int):
        return self.vertices[v].vizinhos
    
    def haAresta(self, u : int, v : int):
        return (u, v) in self.arestas.keys() or (v, u) in self.arestas.keys()
    
    def peso(self, u : int, v : int):
        return self.arestas[self.get_aresta(u, v)]
    
    def ler_arquivo(self, arquivo : str) -> None:
        # le o arquivo .net
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
            
            vertices = int(linhas[0].split(' ')[1])
            for i in range(1, vertices + 1):
                linha = linhas[i].split(' ')
                id = int(linha[0])
                rotulo = (" ".join(linha[1:])).strip()
                
                self.adiciona_vertice(id, rotulo)
                
            for i in range(vertices + 2, len(linhas)):
                linha = linhas[i].split(' ')
                u = int(linha[0])
                v = int(linha[1])
                peso = float(linha[2])
                
                self.adiciona_aresta(u, v, peso)
                
    def print_grafo(self):
        print("Vertices:")
        for v in self.vertices:
            print(f"ID: {self.vertices[v].id} - Rotulo: {self.vertices[v].rotulo}")
        print("\nArestas:")
        for a in self.arestas:
            print(f"Vertices: {a} - Peso: {self.arestas[a]}")
        

class Vertice:
    def __init__(self, id : int, rotulo : str) -> None:
        self.id = id
        self.rotulo = rotulo
        self.vizinhos = {}
        self.grau = 0
        
    def adiciona_vizinho(self, v : int, peso : float) -> None:
        self.vizinhos[v] = peso
        self.grau += 1

