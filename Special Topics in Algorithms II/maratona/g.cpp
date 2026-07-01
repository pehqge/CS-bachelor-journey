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

    vector<pair<int, int>> cows(n); 

    
    for (int i = 0; i < n; ++i) {
        int g, d;
        cin >> g >> d;
        cows[i] = {g, d};
    }

    sort(cows.begin(), cows.end(), [](const pair<int, int>& a, const pair<int, int>& b) {
        return a.first > b.first; 
    });

   
    int d_max = 0;
    for (const auto& cow : cows) {
        if (cow.second > d_max) {
            d_max = cow.second;
        }
    }

    vector<bool> tempos(d_max + 1, false);

    int milk = 0;

    for (const auto& cow : cows) {
        int g = cow.first;   
        int d = cow.second; 

        for (int t = d; t >= 1; --t) {
            if (!tempos[t]) {
                tempos[t] = true; 
                milk += g;        
                break;           
            }
        }
    }

    cout << milk << "\n";

    return 0;
}