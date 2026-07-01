#include <bits/stdc++.h>
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

    for (int tc = 1; tc <= T; ++tc) {
        vector<string> deck(52);
        vector<bool> done(52, false);
        
        for (int i = 0; i < 52; i++) {
            cin >> deck[i];
        }

        int Y = 0;
        int pos = 26;

        for (int i = 0; i < 3; ++i) {
            int X;
            
            if (deck[pos][0] >= '2' && deck[pos][0] <= '9') {
                X = deck[pos][0] - '0';
            } else {
                X = 10;
            }

            Y += X;
            
            done[pos] = true;
            --pos;

            for (int j = 0; j < 10 - X; ++j) {
                done[pos] = true;
                --pos;
            }
        }

        cout << "Case " << tc << ": ";

        for (int i = 0, j = 0;; ++i) {
            if (!done[i]) ++j;
            
            if (j == Y) {
                cout << deck[i] << endl;
                break;
            }
        }
    }
    
    return 0;
}