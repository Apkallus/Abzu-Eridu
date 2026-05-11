void StringCount( char s[] ){
	int letter = 0, blank = 0, digit = 0, other = 0;
	int i;
	char ch;
	for(i=0;(ch=s[i]!='\0');i++){
		ch=s[i];
		if(ch>='a'&&ch<='z'||ch>='A'&&ch<='Z'){
			letter++;
		}else if(ch>='0'&&ch<='9'){
			digit++;
		}else if(ch==' '||ch=='\n'){
			blank++;
		}else{
			other++;
		}
	}
	printf("letter = %d, blank = %d, digit = %d, other = %d",letter,blank,digit,other);
}
