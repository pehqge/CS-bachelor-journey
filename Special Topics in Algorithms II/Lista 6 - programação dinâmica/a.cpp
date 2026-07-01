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
    
    int N;
    cin >> N;
    
    vector<int> h(N);
    for (int i = 0; i < N; ++i) {
        cin >> h[i];
    }
    
    vector<int> dp(N, INT_MAX);
    dp[0] = 0; 
    
    for (int i = 1; i < N; ++i) {
        dp[i] = dp[i-1] + abs(h[i] - h[i-1]);
        
        if (i > 1) {
            dp[i] = min(dp[i], dp[i-2] + abs(h[i] - h[i-2]));
        }
    }
    
    cout << dp[N-1] << "\n";
    
    return 0;
}