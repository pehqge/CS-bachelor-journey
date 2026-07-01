#include <iostream>
#include <list>
#include <utility>  // para utilizar pair
#include <limits> // biblioteca que disponibiliza o maior valor inteiro (infinito positivo)
#include <fstream>
#include <vector>
using namespace std;

template<typename T>
class Grafo { // inicio da classe

    private:
        int V; // número de vértices
        vector<T> rotulos; // lista para os rótulos dos vértices
        list<pair<int, int>> *adjacencias; // ponteiro para um array contendo as listas de adjacências    
        int quantidade_arestas;
        

    public:
        Grafo(int V) { // construtor
            this->V = V; // atribui o número de vértices
            adjacencias = new list<pair<int, int>>[V]; // Cada vértice tem uma lista de pares (indice do vértice adjacente, peso da aresta)
            quantidade_arestas = 0; 
            rotulos.resize(V);
        } // end construtor

        ~Grafo() { //destrutor
            delete [] adjacencias;
        }

        int qtdVertices() { // retorna a quantidade de vértices
            return V;
        }

        int qtdArestas() { // retorna a quantidade de arestas
            return quantidade_arestas;
        }
        int grau(int v){ // retorna o grau do vértice (quantas arestas estão conectadas e ele)
            return adjacencias[v].size();
        }
        T rotulo(int v) const { // retorna o rótulo do vértice v
            if (v < 0 || v >= V) {
                throw out_of_range("Índice de vértice fora do intervalo");
            }
            return rotulos[v];
        }
        list<int> vizinhos(int v) { // retorna os vizinhos do vertice
            list<int> vizinhos;
            for (const auto &vertices : adjacencias[v]) {
                vizinhos.push_back(vertices.first);
            }
            return vizinhos;
        }

        bool haAresta(int u, int v) { // verifica se existe uma aresta entre os vertices
            for (auto &vertic : adjacencias[u]) {
                if (vertic.first == v) {
                    return true; // aresta de u para v
                }
            }
            for(auto &vertic: adjacencias[v]) {
                if (vertic.first == u) {
                    return true; // aresta v->u
                }
            }
            return false;
        }

        int peso(int u, int v) { // retorna o peso da aresta entre os vertices
            for (auto &vertice : adjacencias[u]) {
                if (vertice.first == v) {
                    return vertice.second; // peso de u->v
                }
            }

            for (auto &vertice : adjacencias[v]) {
                if (vertice.second == u) {
                    return vertice.first; // peso de v->u
                }
            }
            return numeric_limits<int>::max();
        }

        void ler(const string& arquivo) {
            ifstream file(arquivo);

            if (!file.is_open()) {
                cout << "Erro ao abrir o arquivo." << endl;
                return;
            }

            string line;
            // Lê a quantidade de vértices
            getline(file, line);
            int n = stoi(line.substr(10)); // Pega o número de vértices a partir da linha "*vertices n"

            // Lê os rótulos dos vértices
            for (int i = 0; i < n; i++) {
                getline(file, line);
                int index = stoi(line.substr(0, line.find(' ')));
                string label = line.substr(line.find(' ') + 1);
                rotulos[index - 1] = label;
            }

            // Lê as arestas
            while (getline(file, line)) {
                if (line.find("*edges") != string::npos)
                    continue;

                int u = stoi(line.substr(0, line.find(' '))) - 1;
                line = line.substr(line.find(' ') + 1);
                int v = stoi(line.substr(0, line.find(' '))) - 1;
                int peso = stoi(line.substr(line.find(' ') + 1));

                adjacencias[u].push_back(make_pair(v, peso));
                adjacencias[v].push_back(make_pair(u, peso)); // Como é grafo não-dirigido
                quantidade_arestas++;
            }

            file.close();
        }
        

}; // fim da classe



int main() {
    // Cria um grafo com 5 vértices
    Grafo<string> g(5);

    // Lê o grafo a partir de um arquivo
    g.ler("grafo.txt");

    // Imprime a quantidade de vértices
    cout << "Quantidade de vértices: " << g.qtdVertices() << endl;

    // Imprime a quantidade de arestas
    cout << "Quantidade de arestas: " << g.qtdArestas() << endl;

    // Imprime o grau de cada vértice
    for (int i = 0; i < g.qtdVertices(); i++) {
        cout << "Grau do vértice " << i + 1 << ": " << g.grau(i) << endl;
    }

    // Imprime o rótulo de cada vértice
    for (int i = 0; i < g.qtdVertices(); i++) {
        cout << "Rótulo do vértice " << i + 1 << ": " << g.rotulo(i) << endl;
    }

    // Verifica se há aresta entre dois vértices
    int u = 0, v = 1;
    if (g.haAresta(u, v)) {
        cout << "Há uma aresta entre os vértices " << u + 1 << " e " << v + 1 << endl;
    } else {
        cout << "Não há uma aresta entre os vértices " << u + 1 << " e " << v + 1 << endl;
    }

    // Imprime os vizinhos de um vértice
    int vertice = 2;
    list<int> vizinhos = g.vizinhos(vertice);
    cout << "Vizinhos do vértice " << vertice + 1 << ": ";
    for (int viz : vizinhos) {
        cout << viz + 1 << " "; // 1-indexado
    }
    cout << endl;

    // Imprime o peso de uma aresta
    int peso = g.peso(u, v);
    if (peso != numeric_limits<int>::max()) {
        cout << "Peso da aresta entre os vértices " << u + 1 << " e " << v + 1 << ": " << peso << endl;
    } else {
        cout << "Não há aresta entre os vértices " << u + 1 << " e " << v + 1 << endl;
    }

    return 0;
}
