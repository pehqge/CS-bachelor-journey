#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

vector<int> arrSuf(const string &s) {
    int n = s.size();
    vector<int> sufixo(n), rank(n), temp_rank(n), cnt(max(n, 256), 0);

    for (int i = 0; i < n; ++i) sufixo[i] = i, rank[i] = s[i];
    for (int k = 1; k < n; k <<= 1) {
        auto cmp = [&](int i, int j) {
            if (rank[i] != rank[j]) return rank[i] < rank[j];
            int ri = (i + k < n) ? rank[i + k] : -1;
            int rj = (j + k < n) ? rank[j + k] : -1;
            return ri < rj;
        };
        sort(all(sufixo), cmp);

        temp_rank[sufixo[0]] = 0;
        for (int i = 1; i < n; ++i) {
            temp_rank[sufixo[i]] = temp_rank[sufixo[i - 1]] + cmp(sufixo[i - 1], sufixo[i]);
        }
        rank = temp_rank;
    }
    return sufixo;
}

int main() {
    fastIO();

    string s;
    while (getline(cin, s)) {
        if (s.empty()) break;

        int n;
        cin >> n;
        vector<int> consultas(n);
        for (int i = 0; i < n; ++i) cin >> consultas[i];
        cin.ignore();

        vector<int> sufixo = arrSuf(s);
        for (int i = 0; i < n; ++i) {
            cout << sufixo[consultas[i]];
            if (i < n - 1) cout << " ";
        }
        cout << "\n";
    }

    return 0;
}