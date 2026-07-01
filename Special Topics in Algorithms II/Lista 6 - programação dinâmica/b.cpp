#include <bits/stdc++.h>

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int main() {
    fastIO();
    
    int t;
    cin >> t;

    for (int test = 1; test <= t; ++test) {
        int N;
        cin >> N;

        vector<int> heights(N), widths(N);

        for (int i = 0; i < N; ++i) {
            cin >> heights[i];
        }
        
        for (int i = 0; i < N; ++i) {
            cin >> widths[i];
        }

        vector<int> lis(N), lds(N);

        for (int i = 0; i < N; ++i) {
            lis[i] = widths[i];
            lds[i] = widths[i];
        }

        for (int i = 1; i < N; ++i) {
            for (int j = 0; j < i; ++j) {
                if (heights[i] > heights[j]) { 
                    lis[i] = max(lis[i], lis[j] + widths[i]);
                }
            }
        }

        
        for (int i = 1; i < N; ++i) {
            for (int j = 0; j < i; ++j) {
                if (heights[i] < heights[j]) { 
                    lds[i] = max(lds[i], lds[j] + widths[i]);
                }
            }
        }

        int maxLIS = *max_element(lis.begin(), lis.end());
        int maxLDS = *max_element(lds.begin(), lds.end());

        if (maxLIS >= maxLDS) {
            cout << "Case " << test << ". Increasing (" << maxLIS << "). Decreasing (" << maxLDS << ").\n";
        } else {
            cout << "Case " << test << ". Decreasing (" << maxLDS << "). Increasing (" << maxLIS << ").\n";
        }
    }

    return 0;
}