#include <bits/stdc++.h>
using namespace std;

bool rps(const string &play1, const string &play2) {
    if ((play1 == "rock" && play2 == "scissors") ||
        (play1 == "scissors" && play2 == "paper") ||
        (play1 == "paper" && play2 == "rock")) {
        return true;
    }
    return false;
}

int main() {
    bool first_case = true;  
    while (true) {
        int n, k;
        
        scanf("%d", &n);
        if (n == 0) {
            break;
        }

        if (!first_case) { 
            printf("\n");
        }
        first_case = false;  
        
        scanf("%d", &k);
        vector<int> wins(n + 1, 0);
        vector<int> losses(n + 1, 0);
        
        int total_games = k * n * (n - 1) / 2; 

        int player1, player2;
        char play1[10], play2[10];

        for (int i = 0; i < total_games; i++) {
            scanf("%d %s %d %s", &player1, play1, &player2, play2);

            if (rps(string(play1), string(play2))) {
                wins[player1]++;
                losses[player2]++;
            } else if (strcmp(play1, play2) != 0) {
                wins[player2]++;
                losses[player1]++;
            }
        }

        for (int i = 1; i <= n; i++) {
            if (wins[i] + losses[i] == 0) {
                printf("-\n");
            } else {
                printf("%.3f\n", (double)wins[i] / (wins[i] + losses[i]));
            }
        }
    }
    return 0;
}