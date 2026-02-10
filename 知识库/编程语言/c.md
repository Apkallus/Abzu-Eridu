- `__attribute__((packed))`  
    禁止结构体自动填充（padding）
- `__attribute__ ((constructor))` 
    在 `main()` 之前自动执行这个函数。
- `setvbuf(stdin, NULL, _IONBF, 0);`  
    `setvbuf(stdout, NULL, _IONBF, 1);`  
    `stdin` 与 `stdout` 不使用缓冲，立即读写
    
- `int __snprintf_chk(char * str, size_t maxlen, int flag, size_t strlen, const char * format)`

### setuid(geteuid())

对于 suid 程序
    real uid = hacker
    effective uid = root

从内核角度看，用 effective uid 做权限检查  

但 libc / shell 会检查：real uid != effective uid 或 rgid != egid 判断认为这是一个 setuid 程序，于是进入 “secure execution” 模式：
- 会清理或忽略很多环境变量（包括想控制的 PATH）
- system() 里 /bin/sh 可能会用一个“安全 PATH”，不信任用户提供的 PATH

函数：
- `geteuid()` 
    读取 effective uid
- `setuid()`  
    设置 real uid

于是 `setuid(geteuid())` 将提权


### mmap

调试shellcode：
```c
void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset);

page = mmap(0x1337000,      // 期望映射到的虚拟地址。
            0x1000,         // 映射的大小 4KB
            PROT_READ | PROT_WRITE | PROT_EXEC, // 页的权限是：可读 / 可写 / 可执行
            MAP_PRIVATE | MAP_ANON, // 匿名映射其内容全 0 | 写时复制的私有映射
            0, 0            // 对匿名映射来说这两个参数会被忽略，随便写成 0。
            );
// 调用成功后，page 就指向一块 4KB 的、RWX 的内存区域。

// 从标准输入读取最多 4096 字节数据，直接写入刚刚分配的那块 RWX 内存。
read(0, page, 0x1000);

// void(*)() 是 “指向 void f(void) 形式函数的指针” 的类型。
// 即，强制类型转换为函数指针后调用那块 RWX 内存
((void(*)())page)();
```

### personality()

读取/设置当前进程的 personality 标志位（一个 bitmask）。

`personality(0xffffffff)`（也常写 `personality(-1)`）是一个约定用法：表示“只读取当前 personality，不修改”。

如果调用成功，current 通常是个不大的数；只有调用失败才会返回 -1。

### dlsym(RTLD_NEXT, x) 

`#include <dlfcn.h>`

dlsym 是动态链接库（DL）操作的函数，用于在运行时（Runtime）从一个已加载的共享库（如 .so 文件）中查找指定符号（函数或变量）的内存地址。

原型：void *dlsym(void *handle, const char *symbol);

返回值：成功时返回指向符号 symbol 的指针（函数指针），失败则返回 NULL。

RTLD_NEXT 句柄：查找“下一个”定义
- RTLD_NEXT 是一个特殊的伪句柄（Pseudo-handle），它指示 dlsym 从当前库之后加载的库中，按照默认的库搜索顺序查找指定的符号。

`dlsym(RTLD_NEXT, "bind")` 在库打桩中，于当前的自定义构造库后（原库）查找函数，从而得到原始函数以包装。


### accept(server_fd, addr, addrlen)

在 Linux 上常用 accept(server_fd, NULL, NULL)：
只要 addr 和 addrlen 同时设为 NULL，内核不会去解引用指针，也就不会因为 EFAULT 崩掉。