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

    ll N;
    cin >> N;

    if (N < 1) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }


    if ((N & (N - 1)) != 0) {
        cout << "IMPOSSIBLE\n";
    } else {
       
        int k = 0;
        ll temp = N;
        while (temp > 1) {
            temp >>= 1;
            k++;
        }

        string S(k + 1, 'A');
        S[k] = 'B'; 
        cout << S << "\n";
    }

    return 0;
}