#include "/home/anupam/test1/ClashRCRound2/Sandboxing/include/sandbox.h"
#include <iostream>
#include <string.h>
using namespace std;

int main() {install_filters();
	// your code goes here
	int t;
	cin>>t;
	string arr[t];
	for(int i=0;i<t;i++)
	{
	    int n,k,x,y;
	    cin>>n>>k>>x>>y;
	    int count=x;
	    
	    for(int j=0;j<n;j++)
	    {
	        count=(x+k)%n;
	        if(count==y)
	        {   arr[i]="YES";
	            break;
	        }
	        x=count;
	    }
        if(arr[i]!="YES")
        {
            arr[i]="NO";
        }
	    
	}
for(int k=0;k<t;k++)
{
    cout<<arr[k]<<"\n";
}
	return 0;
}