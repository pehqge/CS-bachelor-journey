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

    int N;
    while (cin >> N) {
        if (!cin || N == 0) break;

        vector<vector<ll>> c(N, vector<ll>(N));
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                cin >> c[i][j];
            }
        }

        bool invalid = false;
        for (int i = 0; i < N; ++i) {
            if (c[i][i] != 0) {
                cout << -1 << "\n";
                invalid = true;
                break;
            }
        }
        if (invalid) continue;

        vector<vector<ll>> dist = c;
        for (int k = 0; k < N; ++k) {
            for (int i = 0; i < N; ++i) {
                for (int j = 0; j < N; ++j) {
                    if (dist[i][k] + dist[k][j] < dist[i][j]) {
                        dist[i][j] = dist[i][k] + dist[k][j];
                    }
                }
            }
        }

        invalid = false;
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                if (dist[i][j] < c[i][j]) {
                    cout << -1 << "\n";
                    invalid = true;
                    break;
                }
            }
            if (invalid) break;
        }
        if (invalid) continue;

        int removable = 0;
        for (int i = 0; i < N; ++i) {
            for (int j = i + 1; j < N; ++j) {
                if (dist[i][j] == c[i][j]) {
                    bool remove = false;
                    for (int k = 0; k < N && !remove; ++k) {
                        if (k != i && k != j) {
                            if (dist[i][k] + dist[k][j] == c[i][j]) {
                                remove = true;
                            }
                        }
                    }
                    if (remove) removable += 2;
                }
            }
        }
        cout << removable / 2 << "\n";
    }

    return 0;
}
