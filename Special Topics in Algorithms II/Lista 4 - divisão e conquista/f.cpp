#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

bool alcanca(const vector<int>& pulos, int k) {
    for (int h : pulos) {
        if (h > k) {
            return false;
        } else if (h == k) {
            k--;
        }
    }
    return true;
}

int main() {
    fastIO();

    int T;
    cin >> T;

    for (int caso = 1; caso <= T; ++caso) {
        int n;
        cin >> n;

        vector<int> bambus(n);
        for (int i = 0; i < n; ++i) {
            cin >> bambus[i];
        }

        vector<int> pulos(n);
        int altura = 0;
        int max_pulo = 0;
        for (int i = 0; i < n; ++i) {
            pulos[i] = bambus[i] - altura;
            max_pulo = max(max_pulo, pulos[i]);
            altura = bambus[i];
        }

        int esq = max_pulo;
        int dir = max_pulo + n;

        while (esq < dir) {
            int mid = esq + (dir - esq) / 2;
            if (alcanca(pulos, mid)) {
                dir = mid;
            } else {
                esq = mid + 1;
            }
        }

        cout << "Case " << caso << ": " << esq << endl;
    }
    

    return 0;
}