#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

double dist(pair<int, int>& a, pair<int, int>& b) {
    return sqrt(pow(a.first - b.first, 2) + pow(a.second - b.second, 2));
}

int main() {
    fastIO();

    int n, test_case = 1;

    while (cin >> n && n != 0) {
        vector<pair<int, int>> stones(n);

        for (int i = 0; i < n; ++i) {
            cin >> stones[i].first >> stones[i].second;
        }

        vector<vector<double>> graph(n, vector<double>(n, 1e9));

        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                graph[i][j] = dist(stones[i], stones[j]);
            }
        }

        for (int k = 0; k < n; ++k) {
            for (int i = 0; i < n; ++i) {
                for (int j = 0; j < n; ++j) {
                    graph[i][j] = min(graph[i][j], max(graph[i][k], graph[k][j]));
                }
            }
        }

        cout << "Scenario #" << test_case++ << "\n";
        cout << fixed << setprecision(3) << "Frog Distance = " << graph[0][1] << "\n\n";
    }

    return 0;
}