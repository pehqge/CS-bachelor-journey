#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int contarOcorrencias(const string& sub, const string& texto) {
    int count = 0, pos = 0;
    while ((pos = texto.find(sub, pos)) != string::npos) {
        count++;
        pos++;
    }
    return count;
}

int main() {
    fastIO();

    string s, l;
    while (cin >> s >> l, s != "0") {
        int type1 = contarOcorrencias(s, l);

        set<string> modificacoesTipo2;
        for (int i = 0; i < s.size(); ++i) {
            string modificado = s.substr(0, i) + s.substr(i + 1);
            modificacoesTipo2.insert(modificado);
        }

        set<string> modificacoesTipo3;
        for (int i = 0; i <= s.size(); ++i) {
            for (char c : {'A', 'G', 'C', 'T'}) {
                string modificado = s.substr(0, i) + c + s.substr(i);
                modificacoesTipo3.insert(modificado);
            }
        }

        int type2 = 0;
        for (const string& mod : modificacoesTipo2) {
            type2 += contarOcorrencias(mod, l);
        }

        int type3 = 0;
        for (const string& mod : modificacoesTipo3) {
            type3 += contarOcorrencias(mod, l);
        }

        cout << type1 << " " << type2 << " " << type3 << "\n";
    }

    return 0;
}