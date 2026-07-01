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

    while (true) {

        if (cin.eof()) break;

        int n;
        cin >> n;

        int tracks;
        cin >> tracks;

        vector<int> lenghts;

        for (int i = 0; i < tracks; i++)
        {
            int song;
            cin >> song;
            lenghts.push_back(song);
        }
        
        int limitBmask = (1 << tracks);

        int best = 0;
        int bestmask = 0;

        for (int bmask = 0; bmask < limitBmask; bmask++)
        {
            int sum = 0;
            for (int i = 0; i < tracks; i++)
            {
                if (bmask & (1 << i))
                {
                    sum += lenghts[i];
                }
            }

            if (sum <= n && sum >= best && bmask >= bestmask)
            {
                best = sum;
                bestmask = bmask;
            }
            
        }

        for (int i = 0; i < tracks; i++)
        {
            if (bestmask & (1 << i))
            {
                cout << lenghts[i] << " ";
            }
        }
        cout << "sum:" << best << "\n";

    }

    return 0;
}