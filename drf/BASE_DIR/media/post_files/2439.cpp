#include <iostream>
using namespace std;

int main(){
    int n;
    cin >> n;

    for(int a = n; a > 0; a--){
        for(int i = a-1; i > 0; i--){
            cout << " ";
        }
        for(int j = 1; j <= n-a+1; j++){
            cout <<"*";
        }
        cout << "\n";
    }

    return 0;
    
}
/* 
" " "*"
4   1
3   2
2   3
1   4
0   5 */