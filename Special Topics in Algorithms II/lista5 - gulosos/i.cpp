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

    vector<int> balao(n);
    int alt_maxima = 0;

    for (int i = 0; i < n; ++i) {
        cin >> balao[i];
        alt_maxima = max(alt_maxima, balao[i]);
    }

    vector<int> flecha(alt_maxima + 2, 0);
    int tiros = 0;

    for (int i = 0; i < n; ++i) {
        int H = balao[i];
        if (flecha[H] > 0) {
            flecha[H]--;
        } else {
            tiros++;
        }
        
        if (H > 1) {
            flecha[H - 1]++;
        }
    }

    cout << tiros << endl;



    return 0;
}