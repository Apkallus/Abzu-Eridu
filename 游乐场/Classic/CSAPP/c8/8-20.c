#include <stdio.h>
#include "csapp.h"

int main(int argc, char *argv[], char *envp[]){

    if(execve("/bin/ls", argv, environ) < 0){
        printf("execve failed");
        exit(0);
    }
}