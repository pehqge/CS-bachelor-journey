import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from newton import newton


class Graph:
    """Classe para plotagem de gráficos"""

    def __init__(self, precision, n):
        self.precision = precision
        self.n = n

    def plot_first_graph(self, sistema, colors, labels, plot_range):
        """Gráfico 1: para onde convergiu"""

        x_axis = np.linspace(start=plot_range[0], stop=plot_range[1], num=self.n)
        y_axis = x_axis

        to_plot = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                x, y = newton(x_axis[j], y_axis[i], sistema.jacobian, sistema.f1, sistema.f2, max_iter=20)

                for solution_index, solution in enumerate(sistema.solutions):
                    # Define a cor do ponto de acordo com a solução para a qual ele converge

                    if np.linalg.norm(np.array([x, y]) - np.array(solution)) <= self.precision:
                        to_plot[self.n - i - 1][j] = solution_index + 1
                        break

        boundaries = np.arange(len(colors) + 1) - 0.5
        norm = BoundaryNorm(boundaries=boundaries, ncolors=(len(colors) + 1))
        cmap = ListedColormap(colors)
        plt.imshow(to_plot, cmap=cmap, norm=norm, extent=(plot_range[0], plot_range[1], plot_range[0], plot_range[1]))

        colorbar = plt.colorbar(ticks=range(len(colors)))
        colorbar.ax.set_yticklabels(labels)

        solution_points = np.array(sistema.solutions)
        plt.scatter(
            solution_points[:, 0],
            solution_points[:, 1],
            color="grey",
            edgecolors="black",
            s=50,
            zorder=5,
            label="Soluções exatas",
        )

        plt.title("Regiões de convergência")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()

    def paint_solution(self, sistema, x_j, y_i, max_iter):
        """Algoritmo auxiliar para pintar o gráfico 2."""

        num_of_iterations = 1

        while num_of_iterations <= max_iter:
            x, y = newton(
                x_j, y_i, sistema.jacobian, sistema.f1, sistema.f2, max_iter=num_of_iterations
            )

            for solution in sistema.solutions:
                # Define a cor do ponto de acordo com o número de iterações necessárias para convergir

                if np.linalg.norm(np.array([x, y]) - np.array(solution)) <= self.precision:
                    return num_of_iterations

            num_of_iterations += 1

        return 0

    def plot_second_graph(self, sistema, plot_range):
        """Gráfico 2: como convergiu"""

        x_axis = np.linspace(start=plot_range[0], stop=plot_range[1], num=self.n)
        y_axis = x_axis.copy()

        to_plot = np.zeros((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                to_plot[self.n - i - 1][j] = self.paint_solution(
                    sistema, x_axis[j], y_axis[i], max_iter=20
                )

        cmap = plt.get_cmap("viridis")
        cmap.set_under("black")  # Set the color for zero values

        plt.imshow(to_plot, cmap=cmap, extent=(plot_range[0], plot_range[1], plot_range[0], plot_range[1]), vmin=0.1)
        plt.colorbar(ticks=range(1, len(sistema.solutions) + 1), label="Número de iterações")

        solution_points = np.array(sistema.solutions)
        plt.scatter(
            solution_points[:, 0],
            solution_points[:, 1],
            color="grey",
            edgecolors="black",
            s=50,
            zorder=5,
            label="Soluções exatas",
        )

        plt.title("Regiões de convergência")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.show()
