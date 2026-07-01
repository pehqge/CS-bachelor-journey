#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

const int MAX_TIME = 1000000;

struct Interval {
    int start, end;
};

bool compareIntervals(const Interval &a, const Interval &b) {
    return a.start < b.start;
}

int main() {
    fastIO();

    int n, m;

    while (cin >> n >> m, n || m) {
        bool conflict = false;
        vector<Interval> intervals;

        
        for (int i = 0; i < n; ++i) {
            int start, end;
            cin >> start >> end;

            intervals.push_back({start, end});
        }

        
        for (int i = 0; i < m; ++i) {
            int start, end, interval;
            cin >> start >> end >> interval;

            int current_start = start;
            int current_end = end;

            while (current_start < MAX_TIME) {
                intervals.push_back({current_start, current_end});

                current_start += interval;
                current_end += interval;

                if (current_start >= current_end) break; 
            }
        }

        
        sort(all(intervals), compareIntervals);

        
        for (size_t i = 1; i < intervals.size(); ++i) {
            if (intervals[i].start < intervals[i - 1].end) {
                conflict = true;
                break;
            }
        }

        if (conflict) {
            cout << "CONFLICT\n";
        } else {
            cout << "NO CONFLICT\n";
        }
    }

    return 0;
}