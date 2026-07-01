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
        int n;
        cin >> n;
        if (n == 0) break;

        unordered_map<string, int> combinations; 
        int max_frequency = 0;                   
        for (int i = 0; i < n; i++) {
            vector<int> courses(5);
            for (int j = 0; j < 5; j++) {
                cin >> courses[j];
            }
            sort(all(courses)); 

           
            stringstream ss;
            for (int course : courses) {
                ss << course << " ";
            }
            string key = ss.str();

            
            combinations[key]++;
           
            if (combinations[key] > max_frequency) {
                max_frequency = combinations[key];
            }
        }

        int total_popular = 0;
        
        for (const auto& entry : combinations) {
            if (entry.second == max_frequency) {
                total_popular += entry.second;
            }
        }

        cout << total_popular << "\n";
    }

    return 0;
}