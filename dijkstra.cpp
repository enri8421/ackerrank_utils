#include <bits/stdc++.h>

using namespace std;
typedef pair<int,int> pair_t;


void sp(int n, int s, const vector<vector<pair_t>> &G, vector<int>& dist){
    vector<int> vis(n);
    priority_queue<pair_t, vector<pair_t>, greater<pair_t>> nodes;
    dist[s] = 0;
    nodes.push({0, s});
    
    while(!nodes.empty()){
        pair_t n_min = nodes.top(); nodes.pop();
        int u = n_min.second;
        if (vis[u]) continue;
        vis[u] = 1;
        for (pair_t e_out: G[u]){
            int v = e_out.first;
            int w = e_out.second;
            if ((dist[v] > dist[u] + w) or (dist[v] < 0)){
                dist[v] = dist[u] + w;
                nodes.push({dist[v], v});
            }
        }
    }
}
int n = 0;
int s = 0;
vector<vector<pair_t>> G;

vector<int> dist(n, -1);
sp(n, s, G, dist);
