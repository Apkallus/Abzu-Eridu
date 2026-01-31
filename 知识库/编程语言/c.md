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