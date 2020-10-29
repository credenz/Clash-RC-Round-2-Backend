#include "/home/koushal/PycharmProjects/Clash/Clash-RC-Round-2-Backend/Sandboxing/include/sandbox.h"
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

using namespace std;
using namespace __gnu_pbds;

typedef tree<int, null_type, less_equal<int>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;

const int MAX_N = 1e5 + 5;
const int MAX_L = 20; // ~ Log N
const long long MOD = 1e9 + 7;
const long long INF = 1e9 + 7;

typedef int ll;
typedef vector<ll> vi;
typedef pair<ll,ll> par;
typedef vector<par> parv;
typedef vector<vi> vvi;
// Author : Koushal Bhat
#define forr(i,p,n) for( ll i=p; i<n; i++)
#define forn(i,p,n) for(ll i=p; i<=n; i++)
#define rev(i,n,p) for(ll i=n; i>=p; i--)
#define PI 3.14159265358979323846
#define LSOne(S) (S & (-S))
#define isBitSet(S, i) ((S >> i) & 1)



void solve() {
    ll n=0;
    cin>>n;
    string s;
    cin>>s;
    ll count1=0,count2=0;
    vector<ll>one;
    vector<ll>two;
    forr(i,0,n){
        if(i%2==0)
        {
            if(s[i]=='1')
            one.push_back(i);
        }
        else
        {
            if(s[i]=='0')
            one.push_back(i);
        }
        
    }
    forr(i,0,n){
        if(i%2==0)
        {
            if(s[i]=='0')
            two.push_back(i);
        }
        else
        {
            if(s[i]=='1')
            two.push_back(i);
        }
        
    }
    //forr(i,0,one.size())cout<<one[i]<<" ";cout<<'\n';
    //forr(i,0,two.size())cout<<two[i]<<" ";cout<<'\n';

    if(one.size())count1=1;
    if(two.size())count2=1;
    forr(i,1,one.size()){
        if(one[i]==one[i-1]+1)
        continue;
        else
        {
            count1++;
        }
        

    }
    forr(i,1,two.size()){
        if(two[i]==two[i-1]+1)
        continue;
        else
        {
            count2++;
        }

    }
    //cout<<count1<<" "<<count2<<'\n';
    cout<<min(count1,count2)<<'\n';
    
}

int main() {install_filters();
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    ll tc; cin >> tc;
    forn(t,1,tc) {
        //cout << "Case #" << t  << ": ";
        solve();
    }
}