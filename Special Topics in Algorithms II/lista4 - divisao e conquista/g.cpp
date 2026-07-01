#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

ll consumo_para_valor(ll valor) {
    if (valor <= 200) {
        return valor / 2;
    } else if (valor <= 29900) {
        return (valor - 200) / 3 + 100;
    } else if (valor <= 4979900) {
        return (valor - 29900) / 5 + 10000;
    } else {
        return (valor - 4979900) / 7 + 1000000;
    }
}

ll valor_para_consumo(ll consumo) {
    if (consumo <= 100) {
        return consumo * 2;
    } else if (consumo <= 10000) {
        return 200 + (consumo - 100) * 3;
    } else if (consumo <= 1000000) {
        return 200 + 29700 + (consumo - 10000) * 5;
    } else {
        return 200 + 29700 + 4950000 + (consumo - 1000000) * 7;
    }
}

int main() {
    fastIO();

    ll A, B;
    while (cin >> A >> B && (A || B)) {
        ll consumo_total = consumo_para_valor(A);

        ll low = 0, high = consumo_total / 2;
        ll resposta = 0;

        while (low <= high) {
            ll mid = (low + high) / 2;
            ll c1 = mid;
            ll c2 = consumo_total - c1;

            ll valor_c1 = valor_para_consumo(c1);
            ll valor_c2 = valor_para_consumo(c2);

            ll diferenca = valor_c2 - valor_c1;

            if (diferenca == B) {
                resposta = valor_c1;
                break;
            } else if (diferenca < B) {
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        cout << resposta << "\n";
    }

    return 0;
}