#include <stdio.h>
#include <stdlib.h>
#include "csapp.h"

int mysystem(char *command){

    pid_t pid;
    char *strsh[4]={"/bin/sh", "-c", command, NULL};
    //参数表中使用 -c 将之后的字符串作为命令解析
    //那么无需拆分command，而是将其作为之后的参数字符串
    //参数表结尾为NULL空指针

    if((pid = fork()) == 0){
        if(execve(strsh[0], strsh, environ)){
            printf("execve sh failed");
            exit(0);
        }
    }
    
    int status;
    if(waitpid(pid, &status, 0) < 0){
        printf("waitpid error");
        exit(0);
    }
    
    int res;
    if(WIFEXITED(status)){
        res=WEXITSTATUS(status);
    }else{
        res=WIFSIGNALED(status);
    }
    return res;
}

int main(void){
    int res;
    // res = mysystem("ls -al");
    res = mysystem("ps");
    return 0;
}