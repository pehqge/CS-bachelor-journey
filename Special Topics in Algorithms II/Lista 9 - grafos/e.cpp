#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

bool winnable(int n, vector<int>& energy, vector<vector<int>>& adj) {
    vector<int> dist(n + 1, INT_MIN);
    dist[1] = 100;

    for (int i = 0; i < n - 1; ++i) {
        for (int u = 1; u <= n; ++u) {
            if (dist[u] > 0) {
                for (int v : adj[u]) {
                    if (dist[u] + energy[v] > dist[v]) {
                        dist[v] = dist[u] + energy[v];
                    }
                }
            }
        }
    }

    queue<int> q;
    vector<bool> reachable(n + 1, false);
    for (int u = 1; u <= n; ++u) {
        if (dist[u] > 0) {
            for (int v : adj[u]) {
                if (dist[u] + energy[v] > dist[v]) {
                    q.push(u);
                    reachable[u] = true;
                }
            }
        }
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : adj[u]) {
            if (!reachable[v]) {
                reachable[v] = true;
                q.push(v);
            }
        }
    }

    return dist[n] > 0 || reachable[n];
}

int main() {
    fastIO();

    while (true) {
        int n;
        cin >> n;
        if (n == -1) break;

        vector<int> energy(n + 1);
        vector<vector<int>> adj(n + 1);

        for (int i = 1; i <= n; ++i) {
            int m;
            cin >> energy[i] >> m;
            adj[i].resize(m);
            for (int j = 0; j < m; ++j) {
                cin >> adj[i][j];
            }
        }

        cout << (winnable(n, energy, adj) ? "winnable" : "hopeless") << "\n";
    }

    return 0;
}