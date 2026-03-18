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

## 沙箱

### seccomp_init & seccomp_reset 

```c
#include <seccomp.h>

typedef void * scmp_filter_ctx;

scmp_filter_ctx seccomp_init(uint32_t def_action);
int seccomp_reset(scmp_filter_ctx ctx, uint32_t def_action);
```

seccomp_init() 和 seccomp_reset() 函数（重新）初始化内部 seccomp 过滤器状态，准备其使用，并根据 def_action 参数设置默认操作。必须在使用任何其他 libseccomp 函数之前调用 seccomp_init() 函数，因为如果过滤器上下文未正确初始化，其余的库 API 将会失败。seccomp_reset() 函数在重新初始化之前会释放现有的过滤器上下文状态，并且只能在 seccomp_init() 调用成功后调用。如果 seccomp_reset() 带着空过滤器被调用，它会重置库的全局任务状态，包括任何通过 seccomp_notify_fd(3) 获取的通知文件描述符。通常情况下这不需要，但在 fork() 或 clone() 调用后继续使用库时可能需要，以确保 API 级别和用户通知状态被正确重置。

### seccomp_syscall_resolve_num_arch

```c
#include <seccomp.h>

int seccomp_syscall_resolve_name(const char *name);
int seccomp_syscall_resolve_name_arch(uint32_t arch_token,
                                        const char *name);
int seccomp_syscall_resolve_name_rewrite(uint32_t arch_token,
                                        const char *name);
char *seccomp_syscall_resolve_num_arch(uint32_t arch_token, int num);
```

seccomp_syscall_resolve_name()、seccomp_syscall_resolve_name_arch()和 seccomp_syscall_resolve_name_rewrite()函数将常用的系统调用名称解析为内核和 libseccomp API 使用的系统调用编号，其中 seccomp_syscall_resolve_name_rewrite()会为修改系统调用的架构重写系统调用编号。系统调用重写通常发生在多路复用系统调用的情况下，例如 x86 上的 socketcall(2)或 ipc(2)。seccomp_syscall_resolve_num_arch()函数将内核使用的系统调用编号解析为常用的系统调用名称。

### seccomp_rule_add

```c
int seccomp_rule_add(scmp_filter_ctx ctx, uint32_t action,
                            int syscall, unsigned int arg_cnt, ...);
int seccomp_rule_add_exact(scmp_filter_ctx ctx, uint32_t action,
                            int syscall, unsigned int arg_cnt, ...);

int seccomp_rule_add_array(scmp_filter_ctx ctx,
                            uint32_t action, int syscall,
                            unsigned int arg_cnt,
                            const struct scmp_arg_cmp *arg_array);
int seccomp_rule_add_exact_array(scmp_filter_ctx ctx,
                            uint32_t action, int syscall,
                            unsigned int arg_cnt,
                            const struct scmp_arg_cmp *arg_array);

```
seccomp_rule_add()、seccomp_rule_add_array()、seccomp_rule_add_exact()和 seccomp_rule_add_exact_array()函数都向当前的 seccomp 过滤器添加一个新的过滤规则。seccomp_rule_add()和 seccomp_rule_add_array()函数会尽力按照指定方式添加规则，但由于架构特性（例如 x86 上的多路复用系统调用内部重写，如 socket 和 ipc 函数），可能会对规则进行轻微的修改。seccomp_rule_add_exact()和 seccomp_rule_add_exact_array()函数会尝试精确地按照指定方式添加规则，因此在不同架构上可能会表现出不同的行为。虽然它们不保证精确的过滤器规则集，但 seccomp_rule_add()和 seccomp_rule_add_array()会保证无论在何种架构上都能保持相同的行为。

常用编号：
- `SCMP_ACT_ALLOW` 0x7fff0000

### seccomp_load

```c
#include <seccomp.h>

typedef void * scmp_filter_ctx;

int seccomp_load(scmp_filter_ctx ctx);
```

将提供的 seccomp 过滤器加载到内核中；如果函数成功，新的 seccomp 过滤器将在函数返回时生效。如果在进行加载 seccomp 过滤器之前调用了 seccomp_precompute(3)，并且过滤器没有发生任何更改，则 seccomp_load()可以被认为是异步信号安全的。

#### dirname 

`dirname [选项] 文件名...`

从文件路径字符串中提取目录部分

## 原型

- `size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream)`  
    写入指针，每块大小，块数，读取文件流



## 备忘

- `scanf`  遇到 `\n`（空白字符）停止读取，读取字符串时自动在末尾添加 `\x00`

- `atoi` 字符串转整型