#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int N, M, Q;
vector<vector<int>> H;

int main() {
    fastIO();

    while (cin >> N >> M) {
        if (N == 0 && M == 0) break;

        H.assign(N, vector<int>(M));

        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < M; ++j) {
                cin >> H[i][j];
            }
        }

        cin >> Q;

        for (int q = 0; q < Q; ++q) {
            int L, U;
            cin >> L >> U;

            int max_len = 0;

            for (int i = 0; i < N; ++i) {
                // Find the first column where H[i][j] >= L
                int idx = lower_bound(all(H[i]), L) - H[i].begin();

                for (int j = idx; j < M; ++j) {
                    int len = min(N - i, M - j);
                    if (len <= max_len) break;

                    for (int k = max_len; k < len; ++k) {
                        int ni = i + k;
                        int nj = j + k;
                        if (H[ni][nj] <= U) {
                            max_len = k + 1;
                        } else {
                            break;
                        }
                    }
                }
            }

            cout << max_len << "\n";
        }

        cout << "-\n";
    }

    return 0;
}