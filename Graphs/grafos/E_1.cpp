#include <bits/stdc++.h>

using namespace std;

// Classe para um grafo não-dirigido e ponderado.

class Node {
public:
    int id;
    string rotulo;
    Node(int id, string rotulo) {
        this->id = id;
        this->rotulo = rotulo;
    }
};

class Edge {
public:
    Node* src;
    Node* dest;
    int peso;
    Edge(Node* src, Node* dest, int peso) {
        this->src = src;
        this->dest = dest;
        this->peso = peso;
    }
};

class Graph {
public:
    vector<Node*> nodes;
    vector<vector<Edge*>> adjList;

    // Construtor
    Graph(string file_name) {
        ler(file_name);
    }

    // Destrutor
    ~Graph() {
        for (auto node : nodes) {
            delete node;
        }
        for (auto& edgeList : adjList) {
            for (auto edge : edgeList) {
                delete edge;
            }
        }
    }

    // Adiciona um nó ao grafo
    void addNode(int id, string rotulo) {
        Node* newNode = new Node(id, rotulo);
        nodes[id] = newNode;
    }

    // Adiciona uma aresta ao grafo
    void addEdge(int srcId, int destId, int peso) {
        Node* src = nodes[srcId];
        Node* dest = nodes[destId];
        Edge* edge = new Edge(src, dest, peso);
        adjList[srcId].push_back(edge);

        // Por ser nao direcionado, adiciona uma aresta reversa
        Edge* reverseEdge = new Edge(dest, src, peso);
        adjList[destId].push_back(reverseEdge);
    }

    int qtdVertices() {
        return nodes.size();
    }

    int qtdArestas() {
        int qtd = 0;
        for (int i = 0; i < adjList.size(); i++) {
            qtd += adjList[i].size();
        }
        return qtd / 2; // Since each edge is counted twice
    }

    int grau(int id) {
        return adjList[id].size();
    }

    string rotulo(int id) {
        return nodes[id]->rotulo;
    }

    vector<int> vizinhos(int id) {
        vector<int> vizs;
        for (auto edge : adjList[id]) {
            vizs.push_back(edge->dest->id);
        }
        return vizs;
    }

    bool haAresta(int srcId, int destId) {
        for (auto edge : adjList[srcId]) {
            if (edge->dest->id == destId) {
                return true;
            }
        }
        return false;
    }

    int peso(int srcId, int destId) {
        for (auto edge : adjList[srcId]) {
            if (edge->dest->id == destId) {
                return edge->peso;
            }
        }
        return INT_MAX;
    }

    void ler(string file_name) {
        ifstream file(file_name);
        if (!file.is_open()) {
            cout << "Erro ao abrir o arquivo " << file_name << endl;
            return;
        }

        string line;
        // Lê a quantidade de vértices
        getline(file, line);
        int n = stoi(line.substr(10)); // Pega o número de vértices a partir da linha "*vertices n"

        // **Resize nodes and adjList**
        nodes.resize(n);
        adjList.resize(n);

        // Lê cada vértice
        for (int i = 0; i < n; i++)
        {
            getline(file, line);
            int index = stoi(line.substr(0, line.find(' ')));
            string rotulo = line.substr(line.find(' ') + 1);
            addNode(index - 1, rotulo);
        }

        // Lê as arestas
        while (getline(file, line))
        {
            if (line.find("*edges") != string::npos)
                continue;

            int u = stoi(line.substr(0, line.find(' '))) - 1;
            line = line.substr(line.find(' ') + 1);
            int v = stoi(line.substr(0, line.find(' '))) - 1;
            int peso = stoi(line.substr(line.find(' ') + 1));
            addEdge(u, v, peso);
        }

        file.close();
    }
};

// main para testar todos os metodos da classe e imprimir grafo

int main() {
    Graph g("grafo.txt");

    cout << "Quantidade de vértices: " << g.qtdVertices() << endl;
    cout << "Quantidade de arestas: " << g.qtdArestas() << endl;

    for (int i = 0; i < g.qtdVertices(); i++) {
        cout << "Grau do vértice " << i+1 << ": " << g.grau(i) << endl;
    }

    for (int i = 0; i < g.qtdVertices(); i++) {
        cout << "Vizinhos do vértice " << i+1 << ": ";
        for (auto viz : g.vizinhos(i)) {
            cout << viz+1 << " ";
        }
        cout << endl;
    }

    for (int i = 0; i < g.qtdVertices(); i++) {
        cout << "Rótulo do vértice " << i+1 << ": " << g.rotulo(i) << endl;
    }

    for (int i = 0; i < g.qtdVertices(); i++) {
        for (int j = 0; j < g.qtdVertices(); j++) {
            if (g.haAresta(i, j)) {
                cout << "Peso da aresta (" << i+1 << ", " << j+1 << "): " << g.peso(i, j) << endl;
            }
        }
    }

    return 0;
}