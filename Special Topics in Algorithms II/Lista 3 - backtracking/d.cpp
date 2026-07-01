#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int N, A, B, C;
vector<tuple<int, int, int>> solutions;

int main() {
    fastIO();

    cin >> N;

    while (N--) {
        cin >> A >> B >> C;

        bool found = false;
        int min_x = INT_MAX, min_y = INT_MAX, min_z = INT_MAX;

        for (int x = -100; x <= 100 && !found; ++x) {
            for (int y = -100; y <= 100 && !found; ++y) {
                if (x == y) continue;
                for (int z = -100; z <= 100; ++z) {
                    if (x == z || y == z) continue;
                    if (x + y + z != A) continue;
                    if (x * y * z != B) continue;
                    if (x * x + y * y + z * z != C) continue;
                    vector<int> nums = {x, y, z};
                    sort(all(nums));
                    int tx = nums[0], ty = nums[1], tz = nums[2];
                    if (tx < min_x || (tx == min_x && ty < min_y)) {
                        min_x = tx;
                        min_y = ty;
                        min_z = tz;
                    }
                    found = true;
                }
            }
        }

        if (found) {
            cout << min_x << " " << min_y << " " << min_z << "\n";
        } else {
            cout << "No solution.\n";
        }
    }

    return 0;
}