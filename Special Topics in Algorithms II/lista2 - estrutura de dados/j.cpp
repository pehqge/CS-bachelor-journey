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

    int n; 
    cin >> n;

    for (int i = 0; i < n; i++) {
        int k; 
        cin >> k;

        vector<int> friends(51, 0);    
        vector<int> stamps(10001, 0); 
        int unique_stamps = 0;         

        for (int j = 1; j <= k; j++) {
            int m; 
            cin >> m;

            set<int> stamp_set; 
            for (int l = 0; l < m; l++) {
                int x;
                cin >> x;
                stamp_set.insert(x);
            }

            for (auto x : stamp_set) {
                if (stamps[x] == 0) {
                    stamps[x] = j; 
                    friends[j]++;
                    unique_stamps++;
                } else if (stamps[x] > 0 && stamps[x] != j) {
                   
                    friends[stamps[x]]--; 
                    stamps[x] = -1;       
                    unique_stamps--;
                }
            }
        }

        cout << "Case " << i + 1 << ":";
        if (unique_stamps > 0) {
            for (int j = 1; j <= k; j++) {
                double percentage = (double)friends[j] * 100.0 / unique_stamps;
                printf(" %.6f%%", percentage);
            }
        } else {
            for (int j = 1; j <= k; j++) {
                printf(" 0.000000%%");
            }
        }
        cout << "\n";
    }

    return 0;
}