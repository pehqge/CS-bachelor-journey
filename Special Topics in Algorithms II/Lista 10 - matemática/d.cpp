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

    const int MOD = 131071;
    string line;
    while (cin >> line) {
        ll number = 0;
        for (char ch : line) {
            if (ch == '#') {
                cout << (number % MOD == 0 ? "YES" : "NO") << "\n";
                number = 0;
            } else {
                number = (number * 2 + (ch - '0')) % MOD;
            }
        }
    }

    return 0;
}