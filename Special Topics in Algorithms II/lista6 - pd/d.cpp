#include <bits/stdc++.h>

using namespace std;

long long dp[51][51][2];

int n, k, m;

long long solve(int pos, int tam_restante, int color) {
    if (pos == k) {
        return tam_restante == 0 ? 1 : 0;
    }
    if (dp[pos][tam_restante][color] != -1)
        return dp[pos][tam_restante][color];
    long long ans = 0;
    for (int wi = 1; wi <= m && wi <= tam_restante; ++wi) {
        ans += solve(pos + 1, tam_restante - wi, 1 - color);
    }
    dp[pos][tam_restante][color] = ans;
    return ans;
}

int main() {
    while (cin >> n >> k >> m) {
        memset(dp, -1, sizeof(dp));
        cout << solve(0, n, 0) << endl;
    }
    return 0;
}