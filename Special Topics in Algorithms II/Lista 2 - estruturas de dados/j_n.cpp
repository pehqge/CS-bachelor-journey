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

    int K; 
    cin >> K;

    for (int case_num = 1; case_num <= K; ++case_num) {
        int N; 
        cin >> N;

        vector<set<int>> friends_stamps(N + 1); 
        map<int, vector<int>> stamp_owners;     

        
        for (int i = 1; i <= N; ++i) {
            int M; 
            cin >> M;

            set<int> stamps_set;
            for (int j = 0; j < M; ++j) {
                int stamp;
                cin >> stamp;
                stamps_set.insert(stamp);
            }

            friends_stamps[i] = stamps_set;

            for (int stamp : stamps_set) {
                stamp_owners[stamp].push_back(i);
            }
        }

        vector<int> unique_counts(N + 1, 0); 
        int total_unique = 0;                

        
        for (const auto& entry : stamp_owners) {
            if (entry.second.size() == 1) {
                int owner = entry.second[0];
                unique_counts[owner]++;
                total_unique++;
            }
        }

        
        cout << "Case " << case_num << ":";
        cout << fixed << setprecision(6);

        for (int i = 1; i <= N; ++i) {
            double percentage = 0.0;
            if (total_unique > 0) {
                percentage = (unique_counts[i] * 100.0) / total_unique;
            }
            cout << " " << percentage << "%";
        }
        cout << "\n";
    }

    return 0;
}