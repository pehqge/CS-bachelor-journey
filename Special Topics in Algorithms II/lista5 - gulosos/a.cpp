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

    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;

        vector<ll> coins(n);
        for (int i = 0; i < n; ++i) {
            cin >> coins[i];
        }

        int count = 1; 
        ll sum = coins[0];

        for (int i = 1; i < n - 1; ++i) {
            if (sum + coins[i] < coins[i + 1]) {
                sum += coins[i];
                count++;
            }
        }

        if (n > 1) {
            count++;
        }

        cout << count << "\n";
    }

    return 0;
}