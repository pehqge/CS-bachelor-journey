#include <bits/stdc++.h>

using namespace std;

int main() {
    int m, n;
    while (cin >> m >> n) {
        int maxw = (m > 1800) ? m + 200 : m;
        vector<int> dp(maxw + 1, -1);
        dp[0] = 0;

        for (int i = 0; i < n; ++i) {
            int price, favour;
            cin >> price >> favour;
            for (int j = maxw; j >= price; --j) {
                if (dp[j - price] != -1) {
                    dp[j] = max(dp[j], dp[j - price] + favour);
                }
            }
        }

        int best = 0;
        for (int total_expense = 0; total_expense <= maxw; ++total_expense) {
            if (dp[total_expense] != -1) {
                int net_expense = (total_expense > 2000) ? total_expense - 200 : total_expense;
                if (net_expense <= m) {
                    best = max(best, dp[total_expense]);
                }
            }
        }

        cout << best << '\n';
    }
    return 0;
}