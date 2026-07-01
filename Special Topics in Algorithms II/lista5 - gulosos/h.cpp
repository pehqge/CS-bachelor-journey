#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Rock {
    char type;
    int position;
};

int main() {
    fastIO();

    int T;
    cin >> T;
    for (int caseNum = 1; caseNum <= T; ++caseNum) {
        int N, D;
        cin >> N >> D;

        vector<Rock> rocks(N);
        for (int i = 0; i < N; ++i) {
            string s;
            cin >> s;
            rocks[i].type = s[0];
            rocks[i].position = stoi(s.substr(2));
        }

        vector<int> forward_positions;
        forward_positions.push_back(0);
        for (const auto& rock : rocks) {
            forward_positions.push_back(rock.position);
        }
        forward_positions.push_back(D);

        int max_forward_leap = 0;
        for (size_t i = 0; i < forward_positions.size() - 1; ++i) {
            int leap = forward_positions[i + 1] - forward_positions[i];
            max_forward_leap = max(max_forward_leap, leap);
        }

        vector<int> backward_positions;
        backward_positions.push_back(D);
        for (int i = N - 1; i >= 0; --i) {
            if (rocks[i].type == 'B') {
                backward_positions.push_back(rocks[i].position);
            }
        }
        backward_positions.push_back(0);

        int max_backward_leap = 0;
        for (size_t i = 0; i < backward_positions.size() - 1; ++i) {
            int leap = backward_positions[i] - backward_positions[i + 1];
            max_backward_leap = max(max_backward_leap, leap);
        }

        int minimized_max_leap = max(max_forward_leap, max_backward_leap);

        cout << "Case " << caseNum << ": " << minimized_max_leap << "\n";
    }

    return 0;
}