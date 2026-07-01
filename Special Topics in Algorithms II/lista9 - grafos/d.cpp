#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

bool temCicloNeg(int n, vector<tuple<int, int, int>>& edges) {
    vector<int> dist(n, INT_MAX);
    dist[0] = 0;

    for (int i = 0; i < n - 1; ++i) {
        for (auto& [u, v, t] : edges) {
            if (dist[u] != INT_MAX && dist[u] + t < dist[v]) {
                dist[v] = dist[u] + t;
            }
        }
    }

    for (auto& [u, v, t] : edges) {
        if (dist[u] != INT_MAX && dist[u] + t < dist[v]) {
            return true;
        }
    }

    return false;
}

int main() {
    fastIO();

    int c;
    cin >> c;

    while (c--) {
        int n, m;
        cin >> n >> m;

        vector<tuple<int, int, int>> edges;

        for (int i = 0; i < m; ++i) {
            int x, y, t;
            cin >> x >> y >> t;
            edges.emplace_back(x, y, t);
        }

        cout << (temCicloNeg(n, edges) ? "possible" : "not possible") << "\n";
    }

    return 0;
}