#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int N, numerador, denominador;
bool primeiro = true;

char nums[11];

int main() {
    fastIO();

    while (cin >> N && N != 0) {
        if (!primeiro) {
            cout << "\n";
        }
        primeiro = false;

        bool encontrou = false;

        for (denominador = 1234; denominador <= 98765; denominador++) {
            numerador = N * denominador;

            if (numerador > 98765)
                break;

            sprintf(nums, "%05d%05d", numerador, denominador);

            int contador[10] = {0};
            bool valido = true;

            for (int i = 0; i < 10; i++) {
                contador[nums[i] - '0']++;
            }

            for (int i = 0; i < 10; i++) {
                if (contador[i] != 1) {
                    valido = false;
                    break;
                }
            }

            if (valido) {
                cout << setw(5) << setfill('0') << numerador << " / " << setw(5) << setfill('0') << denominador << " = " << N << "\n";
                encontrou = true;
            }
        }

        if (!encontrou) {
            cout << "There are no solutions for " << N << ".\n";
        }
    }

    return 0;
}