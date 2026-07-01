import numpy as np
from graph import Graph
from sistema import Sistema1, Sistema2

def main():
    """Plotamos os gráficos requisitados no enunciado."""

    # Criando os sistemas
    solution1 = [(1, 0), (-1, 0)]
    sistema1 = Sistema1(solution1)

    solution2 = [(1, 0), (-1 / 2, -np.sqrt(3) / 2), (-1 / 2, np.sqrt(3) / 2)]
    sistema2 = Sistema2(solution2)

    # Parâmetros
    precision = 10e-6
    n = 150

    # Objeto responsável pela exibição dos gráficos
    graph = Graph(precision, n)

    # plotando os gráficos dos sistemas
    graph.plot_first_graph(sistema1,
                           colors=["black", "cyan", "green"],
                           labels=["Não converge", "(1, 0)", "(-1, 0)"],
                           plot_range=[-1, 1])
    graph.plot_second_graph(sistema1, plot_range=[-1, 1])

    graph.plot_first_graph(sistema2,
                           colors=["black", "cyan", "green", "blue"],
                           labels=["Não converge", "(1, 0)", "(-1/2, -sqrt(3)/2)", "(-1/2, sqrt(3)/2)"],
                           plot_range=[-1.5, 1.5])
    graph.plot_second_graph(sistema2, plot_range=[-1.5, 1.5])


if __name__ == "__main__":
    main()
