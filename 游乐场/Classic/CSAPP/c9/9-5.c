#include<stdio.h>
#include<unistd.h>
#include<sys/mman.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
int main(int argc, char *argv[]){

    char *cp,*chp;
    struct stat stat_buf;
    // #未进行参数检查
    stat(argv[1],&stat_buf);
    //stat获得文件状态结构，并得到文件大小
    size_t length=stat_buf.st_size;
    int fd=open(argv[1],O_RDONLY,0);
    //open使用文件路径，得到文件描述符
    cp=(char *)mmap(NULL,length,PROT_READ,MAP_PRIVATE,fd,0);
    //mmap使用之前得到的文件大小与文件描述符，在虚拟内存区域复制文件内容
    write(STDOUT_FILENO,cp,length);
    //write从虚拟内存区域输出length长度的内容到标准输出
    munmap(cp,length);
    close(fd);
    //删除虚拟内存区域
    return 0;
}