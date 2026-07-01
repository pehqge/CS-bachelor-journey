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

    vector<int> entrada(8);
    string linha;
    int caso = 1;

    while (getline(cin, linha)) {
        if (linha.empty())
            continue;

        stringstream ss(linha);
        for (int i = 0; i < 8; ++i) {
            ss >> entrada[i];
        }

        vector<int> permutacao = {1,2,3,4,5,6,7,8};
        int min_movimentos = INT_MAX;

        do {
            int movimentos = 0;
            for (int i = 0; i < 8; ++i) {
                if (permutacao[i] != entrada[i]) {
                    movimentos++;
                }
            }

            bool valido = true;
            for (int i = 0; i < 8 && valido; ++i) {
                for (int j = i + 1; j < 8 && valido; ++j) {
                    if (abs(permutacao[i] - permutacao[j]) == abs(i - j)) {
                        valido = false;
                    }
                }
            }

            if (valido) {
                min_movimentos = min(min_movimentos, movimentos);
            }

        } while (next_permutation(all(permutacao)));

        cout << "Case " << caso << ": " << min_movimentos << "\n";
        caso++;
    }

    return 0;
}