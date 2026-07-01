from auxiliar import GrafoBipartido, Vertice, Auxiliar
import sys

def hopcroft_karp(grafo: GrafoBipartido):
    dist = {}
    m = 0
    
    while bfs(grafo, dist):
        for x in grafo.X:
            if x.mate == None and dfs(grafo, x, dist):
                m += 1
                
    emparelhamento = []
    for x in grafo.X:
        if x.mate is not None:
            emparelhamento.append(f"{x.rotulo}-{x.mate.rotulo}")
                
    return m, emparelhamento
    
def bfs(grafo: GrafoBipartido, dist: dict):
    q = []
    
    for x in grafo.X:
        if x.mate == None:
            dist[x] = 0
            q.append(x)
        else:
            dist[x] = float('inf')
            
    dist[None] = float('inf')
        
    while q:
        x = q.pop(0)
        
        if dist[x] < dist[None]:
            for y in x.vizinhos:
                y = grafo.get_vertice(y)
                
                if dist.get(y.mate, float('inf')) == float('inf'):
                    dist[y.mate] = dist[x] + 1
                    q.append(y.mate)
    
    return dist[None] != float('inf')


def dfs(grafo: GrafoBipartido, x: Vertice, dist: dict):
    if x != None:
        for y in x.vizinhos:
            y = grafo.get_vertice(y)
            
            if dist[y.mate] == (dist[x] + 1) and dfs(grafo, y.mate, dist):
                y.mate = x
                x.mate = y
                return True
            
        dist[x] = float('inf')
        return False
    return True

if __name__ == '__main__':
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, type="bipartido")
    
    m, emparelhamento = hopcroft_karp(aux.grafo)
    print(m)
    print(", ".join(emparelhamento))