#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[], char *envp[]){


    printf("Command-Line arguments:\n");
    for(int i=0; argv[i]!=NULL; i++){
        printf("argv[%2d]: %s\n", i, argv[i]);
    }


    printf("Environment arguments:\n");
    for(int i=0; envp[i]!=NULL; i++){
        printf("envp[%2d]: %s\n", i, envp[i]);
    }
    return 0;
}