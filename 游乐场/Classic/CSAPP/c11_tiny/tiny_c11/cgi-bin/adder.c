/*
 * adder.c - a minimal CGI program that adds two numbers together
 */
/* $begin adder */
#include "../csapp.h"

int main(void) {
    char *buf, *p;
    char arg1[MAXLINE], arg2[MAXLINE], content[MAXLINE], content_buf[MAXLINE];
    int n1=0, n2=0, is_head;

    is_head = atoi(getenv("IS_HEAD"));
    /* Extract the two arguments */
    if ((buf = getenv("QUERY_STRING")) != NULL) {
        p = strchr(buf, '&');
        *p = '\0';

        //11.10 创建HTML表单
        //从表单的GET方法获得数据的格式为 n1=5&n2=9
        //于是在原有基础上，新增判断字符串中是否有‘=’
        //来区分直接访问CGI程序还是从表单传递参数到CGI程序
        //如直接访问，则无偏移。如使用表单，则从‘=’后一字节偏移
        if(strchr(buf, '=')){
            strcpy(arg1, strchr(buf, '=')+1);
            strcpy(arg2, strchr(p+1, '=')+1);
        }else{
            strcpy(arg1, buf);
            strcpy(arg2, p+1);
        }

        n1 = atoi(arg1);
        n2 = atoi(arg2);
    }
    

    // sprintf实际只输出了最后一句"Thanks for visiting!\r\n"
    // 于是改用strcat字符串拼接
    /* Make the response body */
    sprintf(content, "Welcome to add.com: ");
    // sprintf(content, "%sTHE Internet addition portal.\r\n<p>", content);
    strcat(content, "THE Internet addition portal.\r\n<p>");
    // sprintf(content, "%sThe answer is: %d + %d = %d\r\n<p>", 
	//     content, n1, n2, n1 + n2);
    sprintf(content_buf, "The answer is: %d + %d = %d\r\n<p>", 
	    n1, n2, n1 + n2);
    strcat(content, content_buf);
    // sprintf(content, "%sThanks for visiting!\r\n", content);
    strcat(content, "Thanks for visiting!\r\n");  
    
    /* Generate the HTTP response */
    printf("Connection: close\r\n");
    printf("Content-length: %d\r\n", (int)strlen(content));
    printf("Content-type: text/html\r\n\r\n");
    //11.11支持HEAD方法 
    if(!is_head){
        printf("%s", content);
    }

    fflush(stdout);

    exit(0);
}
/* $end adder */
