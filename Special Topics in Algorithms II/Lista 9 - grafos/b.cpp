#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

struct Aresta {
    int u, v, l, id;
};

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

void floydWarshall(int n, vector<vector<int>>& dist) {
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            int ik = dist[i][k];
            if (ik == INT_MAX) continue;
            for (int j = 1; j <= n; j++) {
                int kj = dist[k][j];
                if (kj == INT_MAX) continue;
                int nd = ik + kj;
                if (nd < dist[i][j]) dist[i][j] = nd;
            }
        }
    }
}

int dijkstra(int n, int origem, int destino, const vector<vector<pair<int,int>>>& grafo, int excluiId, const vector<Aresta>& arestasPorId) {
    vector<int> d(n+1, INT_MAX);
    d[origem] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> fila;
    fila.push({0, origem});
    vector<bool> visit(n+1,false);

    while (!fila.empty()) {
        auto [cd, u] = fila.top();
        fila.pop();
        if (cd > d[u]) continue;
        if (u == destino) return d[u];
        if (visit[u]) continue;
        visit[u] = true;
        for (auto &ed : grafo[u]) {
            int eid = ed.second;
            if (eid == excluiId) continue;
            int v = arestasPorId[eid].u == u ? arestasPorId[eid].v : arestasPorId[eid].u;
            int nd = cd + arestasPorId[eid].l;
            if (nd < d[v]) {
                d[v] = nd;
                fila.push({nd,v});
            }
        }
    }

    return INT_MAX;
}

int main() {
    fastIO();

    int n, m;
    cin >> n >> m;
    vector<vector<int>> dist(n + 1, vector<int>(n + 1, INT_MAX));
    for (int i = 1; i <= n; i++) dist[i][i] = 0;

    vector<Aresta> arestas(m);
    for (int i = 0; i < m; i++) {
        cin >> arestas[i].u >> arestas[i].v >> arestas[i].l;
        arestas[i].id = i;
        int u = arestas[i].u, v = arestas[i].v, l = arestas[i].l;
        if (l < dist[u][v]) {
            dist[u][v] = l;
            dist[v][u] = l;
        }
    }

    floydWarshall(n, dist);

    vector<vector<pair<int,int>>> grafo(n+1);
    for (auto &ar : arestas) {
        grafo[ar.u].push_back({ar.v, ar.id});
        grafo[ar.v].push_back({ar.u, ar.id});
    }

    for (auto &ar : arestas) {
        int u = ar.u, v = ar.v, l = ar.l;
        if (dist[u][v] < l) {
            cout << dist[u][v] << "\n";
        } else if (dist[u][v] > l) {
            cout << (dist[u][v] == INT_MAX ? -1 : dist[u][v]) << "\n";
        } else {
            int d = dijkstra(n, u, v, grafo, ar.id, arestas);
            cout << (d == INT_MAX ? -1 : d) << "\n";
        }
    }

    return 0;
}