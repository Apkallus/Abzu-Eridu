bool palindrome( char *s ){
	int counti=0,flag=1;
	while(s[counti]!='\0'){
		counti++;
	}
	counti--;
	for(int start=0,end=counti;start<end;start++,end--){
		if(s[start]!=s[end]){
			flag=0;
			break;
		}
	}
	return flag;
}
