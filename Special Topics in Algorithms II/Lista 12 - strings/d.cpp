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

    int n;
    cin >> n;

    while (n--) {
        int k, w;
        cin >> k >> w;

        vector<string> palavras(w);
        for (int i = 0; i < w; ++i) {
            cin >> palavras[i];
        }

        int total = k; 
        for (int i = 1; i < w; ++i) {
            string anterior = palavras[i - 1];
            string atual = palavras[i];
            int overlap = 0;

            for (int j = 1; j <= k; ++j) {
                if (anterior.substr(k - j) == atual.substr(0, j)) {
                    overlap = j;
                }
            }

            total += k - overlap;
        }

        cout << total << "\n";
    }

    return 0;
}