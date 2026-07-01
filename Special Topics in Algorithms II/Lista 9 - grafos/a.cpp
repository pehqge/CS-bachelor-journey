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

    int M;
    while (cin >> M && M != 0) {
        string O, D;
        cin >> O >> D;

        struct W {
            string l1, l2, p;
            int l1_id, l2_id, len;
        };

        vector<W> words(M);
        unordered_map<string,int> lang_map;
        int lang_count = 0;

        auto get_lang_id=[&](const string &L){
            if(lang_map.find(L)==lang_map.end()) lang_map[L]=lang_count++;
            return lang_map[L];
        };

        for (int i = 0; i < M; i++) {
            cin >> words[i].l1 >> words[i].l2 >> words[i].p;
            words[i].l1_id = get_lang_id(words[i].l1);
            words[i].l2_id = get_lang_id(words[i].l2);
            words[i].len = (int)words[i].p.size();
        }

        int O_id = get_lang_id(O);
        int D_id = get_lang_id(D);

        vector<vector<int>> lang_words(lang_count);
        for (int i = 0; i < M; i++) {
            lang_words[words[i].l1_id].push_back(i);
            lang_words[words[i].l2_id].push_back(i);
        }

        vector<vector<int>> adj(M);
        for (int lid = 0; lid < lang_count; lid++) {
            auto &lst = lang_words[lid];
            for (int i = 0; i < (int)lst.size(); i++) {
                for (int j = i+1; j < (int)lst.size(); j++) {
                    int w1 = lst[i], w2 = lst[j];
                    adj[w1].push_back(w2);
                    adj[w2].push_back(w1);
                }
            }
        }

        const int NO_CHAR = 26;
        vector<vector<ll>> dist(M, vector<ll>(27,LLONG_MAX));
        struct Node {
            ll cost;int w,c;
            bool operator>(const Node&o) const {return cost>o.cost;}
        };

        priority_queue<Node,vector<Node>,greater<Node>>pq;

        for (int i = 0; i < M; i++) {
            bool has_O = (words[i].l1_id == O_id || words[i].l2_id == O_id);
            if (has_O) {
                dist[i][NO_CHAR]=words[i].len;
                pq.push({(ll)words[i].len,i,NO_CHAR});
            }
        }

        ll ans=-1;
        while(!pq.empty()){
            auto [cd,cw,cc]=pq.top();pq.pop();
            if(cd>dist[cw][cc]) continue;
            bool has_D=(words[cw].l1_id==D_id||words[cw].l2_id==D_id);
            if(has_D){ans=cd;break;}
            int w_char=words[cw].p[0]-'a';
            for (auto nw: adj[cw]) {
                if (w_char==(words[nw].p[0]-'a')) continue;
                int ncc= w_char;
                ll nd=cd+words[nw].len;
                if(nd<dist[nw][ncc]){
                    dist[nw][ncc]=nd;
                    pq.push({nd,nw,ncc});
                }
            }
        }

        if(ans==-1) cout<<"impossivel\n";else cout<<ans<<"\n";
    }

    return 0;
}