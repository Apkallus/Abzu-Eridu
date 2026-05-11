#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>
#include<sys/mman.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>

/*
    修改后无法保存到磁盘文件，
    尝试再次映射得到的内容为已修改后的，
    已使用O_RDWR打开文件
    PROT_WRITE，MAP_SHARED设置写模式与共享模式

    猜测：虽然修改了文件在虚拟内存中的映射，
        再次映射或使用其他程序映射都得到修改后的内容
        但修改后的内容无法同步到磁盘文件
    ## 将文件从虚拟机与windows的共享文件夹复制到虚拟机区域后运行成功
*/
int main(int argc, char *argv[]){

    char *cp;
    struct stat stat_buf;
    
    int fd=open("hello.txt",O_RDWR);
    fstat(fd,&stat_buf);
    size_t length=stat_buf.st_size;  

    cp=(char *)mmap(NULL,length,PROT_WRITE,MAP_SHARED,fd,0);
    cp[0]='J';
    msync(cp,length,MS_SYNC);

    munmap(cp,length);
    close(fd);

    return 0;
}