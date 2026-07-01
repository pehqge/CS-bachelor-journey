from auxiliar import GrafoDirigido, Vertice, Auxiliar
import sys

def edmonds_karp(grafo: GrafoDirigido, s: Vertice, t: Vertice):
    # reseta os vértices
    grafo.limpar_atributos()

    s.acessado = True
    Q = [s]

    while Q:
        u = Q.pop(0)
        
        for v in u.vizinhos:
            v = grafo.get_vertice(v)
            if not v.acessado and grafo.arestas.get((u.rotulo, v.rotulo), 0) > 0:
                v.acessado = True
                v.anterior = u
                if v == t:
                    p = [t.rotulo]
                    w = t
                    while w != s:
                        w = w.anterior
                        p.insert(0, w.rotulo)
                    return p
                Q.append(v)

    return None


def fluxo_maximo(grafo: GrafoDirigido, s: Vertice, t: Vertice):
    fluxo_maximo = 0

    while True:
        caminho_aumentante = edmonds_karp(grafo, s, t)
        if not caminho_aumentante:
            break

        fluxo_caminho = float('inf')
        for i in range(len(caminho_aumentante) - 1):
            u, v = caminho_aumentante[i], caminho_aumentante[i + 1]
            fluxo_caminho = min(fluxo_caminho, grafo.arestas[(u, v)])

        for i in range(len(caminho_aumentante) - 1):
            u, v = caminho_aumentante[i], caminho_aumentante[i + 1]
            grafo.arestas[(u, v)] -= fluxo_caminho
            grafo.arestas[(v, u)] = grafo.arestas.get((v, u), 0) + fluxo_caminho

        fluxo_maximo += fluxo_caminho

    return fluxo_maximo

if __name__ == '__main__':
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, type="dirigido")

    s_label = sys.argv[2]
    t_label = sys.argv[3]

    try:
        s = aux.grafo.get_vertice(s_label)
        t = aux.grafo.get_vertice(t_label)
    except AttributeError:
        print(f"Erro: Vértice {s_label} ou {t_label} não encontrado no grafo.")
        sys.exit(1)

    fluxo_max = fluxo_maximo(aux.grafo, s, t)
    print(int(fluxo_max))