#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int main() {
    fastIO();

    int cases;
    cin >> cases;
    for (int c = 1; c <= cases; c++) {
        int N, E, T;
        cin >> N >> E >> T;
        int M;
        cin >> M;

        vector<vector<pair<int, int>>> adj(N + 1);
        for (int i = 0; i < M; i++) {
            int a, b, time;
            cin >> a >> b >> time;
            adj[b].push_back({a, time});
        }

        vector<int> dist(N + 1, INT_MAX);
        dist[E] = 0;
        priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
        pq.push({0, E});

        while (!pq.empty()) {
            pair<int, int> current = pq.top();
            pq.pop();

            int cd = current.first;
            int u = current.second;

            if (cd > dist[u]) continue;

            for (const pair<int, int>& edge : adj[u]) {
                int v = edge.first;
                int w = edge.second;

                if (dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                    pq.push({dist[v], v});
                }
            }
        }

        int ans = 0;
        for (int i = 1; i <= N; i++) {
            if (dist[i] <= T) ans++;
        }

        cout << ans << "\n";
        if (c < cases) cout << "\n";
    }

    return 0;
}