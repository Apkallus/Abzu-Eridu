#include "csapp.h"

// struct hostent *gethostbyname(const char *hostname);

// struct hostent{
//     char *h_name;  //official name
//     char **h_aliases;  //alias list
//     int  h_addrtype;  //host address type
//     int  h_length;  //address lenght
//     char **h_addr_list;  //address list
// };

static sem_t gts_mutex;
char **gtb_ts_copy_array(char **origin_p, int flag);

//结构复杂，malloc分配内存 
struct hostent *gethostbyname_ts(const char *hostname){
    printf("===into gethostbyname_ts===\n");
    struct hostent *res_ptr, *origin_ptr;
    int t_size;
    sem_init(&gts_mutex, 0, 1);
    P(&gts_mutex);
    //分配结构并调用原函数
    res_ptr = (struct hostent *)malloc(sizeof(struct hostent));
    origin_ptr = gethostbyname(hostname);

    //复制int元素
    res_ptr->h_addrtype = origin_ptr->h_addrtype;
    res_ptr->h_length = origin_ptr->h_length;

    //复制h_name字符串
    t_size = strlen(origin_ptr->h_name) + 1;
    res_ptr->h_name = (char *)malloc(t_size);
    strcpy(res_ptr->h_name, origin_ptr->h_name);

    //复制指针数组
    res_ptr->h_aliases = gtb_ts_copy_array(origin_ptr->h_aliases, 0);
    res_ptr->h_addr_list = gtb_ts_copy_array(origin_ptr->h_addr_list, 1);

    V(&gts_mutex);
    return res_ptr;
}

char **gtb_ts_copy_array(char **origin_p, int flag){
    printf("===into gtb_ts_copy_array===\n");
    // char *p, **res_p;
    // ###错误！！ 二级指针未初始化直接赋值，导致之后的数组地址写入随机位置
    char *p, **res_p= (char **)malloc(sizeof(char *));;
    int i, k;
    //得到指针数组元素数量
    for(i = 0, p = origin_p[0]; p; i++, p=origin_p[i]){

        if(flag)
            printf("i h_addr_list : %s\n",inet_ntoa(*((struct in_addr *)origin_p[i])));
        else
            printf("i h_aliases : %s\n",origin_p[i]);
    }
    printf("i = %d\n", i);
    //分配指针数组
    *res_p = (char *)malloc((i + 1)*sizeof(char *));
    res_p[i] = NULL;
    //分配并复制数组内的指针所指向的字符串
    for(k = 0, p = origin_p[0]; p; k++, p=origin_p[k]){
        res_p[k] = (char *)malloc(strlen(p) + 1);
        strcpy(res_p[k], p);

        if(flag)
            printf("k h_addr_list : %s\n",inet_ntoa(*((struct in_addr *)res_p[k])));
        else
            printf("k h_aliases : %s\n",res_p[k]);
    }

    int j;
    for(j=0, p=res_p[0]; p ; j++, p=res_p[j]){
        if(flag)
            printf("j h_addr_list : %s\n",inet_ntoa(*((struct in_addr *)res_p[j])));
        else
            printf("j h_aliases : %s\n",res_p[j]);        
    }

    return res_p;
}

int main(int argc, char *argv[])
{
    struct hostent *h;
    printf("===into main===\n");
    if ((h=gethostbyname_ts("www.bing.com")) == NULL) { /* 取得地址信息 */
                printf("gethostbyname");
                exit(1);
        }
    printf("Host name alias : %s\n", h->h_name);
    
    int i;
    char **loop_ptr;

    for(loop_ptr = h->h_addr_list, i = 0; loop_ptr[i]; i++)
        printf("main h_addr_list : %s<<\n",inet_ntoa(*((struct in_addr *)loop_ptr[i])));

    for(loop_ptr = h->h_aliases, i = 0; loop_ptr[i]; i++)
        printf("main h_aliases : %s<<\n",loop_ptr[i]);
        
    return 0;
}