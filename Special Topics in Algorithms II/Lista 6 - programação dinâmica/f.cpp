#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

static ll dp[501][501];

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

ll aij(int i, int j, int n) {
    if (i >= j) {
        ll max1 = 0;

        if (i < n) {
            for (int k = i + 1; k <= n; k++) {
                max1 = max(max1, dp[k][1] + dp[k][j]);
            }
        }

        ll max2 = 0;
        if (j > 0) {
            for (int k = 1; k < j; k++) {
                max2 = max(max2, dp[i][k] + dp[n][k]);
            }
        }

        dp[i][j] = max1 + max2;
        return dp[i][j];

    } else {
        ll max_val = 0;
        for (int k = i; k < j; k++) {
            max_val = max(max_val, dp[i][k] + dp[k + 1][j]);
        }

        dp[i][j] = max_val;
        return dp[i][j];
    }
}

int main() {
    fastIO();
    int n, a1;

    while (cin >> n >> a1) {
        memset(dp, 0, sizeof(dp)); 
        
        dp[n][1] = a1;  
        
      
        for (int i = n; i >= 1; i--) {
            for (int j = 1; j <= n; j++) {
                if (i == n && j == 1) continue; 

                if (i >= j) {
                    ll max1 = 0, max2 = 0;

                    for (int k = i + 1; k <= n; k++) {
                        max1 = max(max1, dp[k][1] + dp[k][j]);
                    }

                    for (int k = 1; k < j; k++) {
                        max2 = max(max2, dp[i][k] + dp[n][k]);
                    }

                    dp[i][j] = max1 + max2;
                } else {
                    for (int k = i; k < j; k++) {
                        dp[i][j] = max(dp[i][j], dp[i][k] + dp[k + 1][j]);
                    }
                }
            }
        }

        cout << dp[1][n] << "\n"; 
    }

    return 0;
}