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

    string s;
    while (cin >> s, s != ".") {
        int n = s.size();
        vector<int> lps(n, 0);
        
        for (int i = 1, comprimento = 0; i < n; ) {
            if (s[i] == s[comprimento]) {
                lps[i++] = ++comprimento;
            } else if (comprimento > 0) {
                comprimento = lps[comprimento - 1];
            } else {
                lps[i++] = 0;
            }
        }
        
        int comprimentoPrefixo = lps[n - 1];
        int menorPeriodo = n - comprimentoPrefixo;
        int resultado = (n % menorPeriodo == 0) ? n / menorPeriodo : 1;
        
        cout << resultado << "\n";
    }

    return 0;
}