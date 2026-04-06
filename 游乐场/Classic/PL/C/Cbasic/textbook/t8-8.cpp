void Shift( char s[] ){
	char temp[4]={s[0],s[1],s[2],'\0'};
	strcpy(s,&s[3]);
	strcat(s,temp); 
}
