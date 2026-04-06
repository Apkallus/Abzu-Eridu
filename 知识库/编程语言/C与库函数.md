

- `__attribute__((packed))`  
    禁止结构体自动填充（padding）
- `__attribute__ ((constructor))` 
    在 `main()` 之前自动执行这个函数。
- `setvbuf(stdin, NULL, _IONBF, 0);`  
    `setvbuf(stdout, NULL, _IONBF, 1);`  
    `stdin` 与 `stdout` 不使用缓冲，立即读写
    
- `int __snprintf_chk(char * str, size_t maxlen, int flag, size_t strlen, const char * format)`

## 库函数

### setuid(geteuid())

```c
#include <unistd.h>

int setuid(uid_t uid);
```
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

### execve - 执行程序

```c
#include <unistd.h>

int execve(const char *path, char *const _Nullable argv[],
        char *const _Nullable envp[]);
```

execve() 函数执行由 path 指定的程序。这会导致调用进程当前正在运行的程序被新程序替换，新程序具有新的栈、堆以及（已初始化和未初始化）数据段。

### mmap, munmap - 将文件或设备映射或取消映射到内存中

```c
#include <sys/mman.h>

void *mmap(size_t length;
            void addr[length], size_t length, int prot, int flags,
            int fd, off_t offset);
int munmap(size_t length;
            void addr[length], size_t length);
```

`mmap()` 在调用进程的虚拟地址空间中创建一个新的映射。新映射的起始地址由 `addr` 指定。参数 `length` 指定映射的长度（必须大于 0）。

文件映射（与匿名映射相对，参见下面的 `MAP_ANONYMOUS`）的内容，是使用从文件描述符 `fd` 所引用的文件（或其他对象）中、从偏移量 `offset` 开始的 `length` 字节进行初始化的。`offset` 必须是 `sysconf(_SC_PAGE_SIZE)` 返回的页面大小的整数倍。
- 非匿名映射的 `fd` 设置内核设备以触发内核模块操作

在 `mmap()` 调用返回之后，文件描述符 `fd` 可以立即关闭，而不会使映射失效。

参数 `prot` 描述了映射所需的内存保护属性（且不得与文件的打开模式冲突）。其值可以是 `PROT_NONE`，或者以下一个或多个标志的按位或：
- `PROT_READ` 0x1
    可读
- `PROT_WRITE` 0x2
    可写
- `PROT_EXEC`
    可执行

`flags` 参数决定了对映射的更新是否对映射同一区域的其他进程可见，以及更新是否传递到底层文件。此行为通过在 `flags` 中**恰好包含**以下值之一来确定：
- `MAP_PRIVATE` 0x2
    匿名映射其内容全 0，匿名映射忽略 fd
- `MAP_ANON` 0x20
    写时复制的私有映射
- `MAP_POPULATE`
    为映射预填充（预缺页）页表。对于文件映射，这会对文件进行预读操作。这将有助于减少后续因缺页而导致的阻塞。如果映射无法被填充（例如，当使用 `MAP_HUGETLB` 时受到映射巨页数量的限制），`mmap()` 调用不会失败。Linux 2.6.23 版本添加了对 `MAP_POPULATE` 与私有映射结合使用的支持。

- `MAP_SHARED` 0x1
    共享此映射。对映射的更新对映射同一区域的其他进程可见，并且（对于文件 backed 映射而言）会传递到底层文件。

- `MAP_FIXED` 0x10
    不要将 `addr` 解释为提示：将映射精确放置在该地址。`addr` 必须适当对齐：对于大多数架构，页大小的倍数即可满足；然而，某些架构可能会施加额外的限制。如果 `addr` 和 `length` 指定的内存区域与任何现有映射的页面重叠，则现有映射的重叠部分将被丢弃。如果无法使用指定的地址，`mmap()` 将失败。

    追求可移植性的软件应谨慎使用 `MAP_FIXED` 标志，牢记进程内存映射的确切布局在不同 Linux 版本、C 库版本和操作系统发行版之间可能会有显著变化。请仔细阅读**注意**部分中对该标志的讨论！

- `MAP_FIXED_NOREPLACE`
    该标志在地址强制方面提供与 `MAP_FIXED` 类似的行为，但不同之处在于 `MAP_FIXED_NOREPLACE` 永远不会覆盖已有的映射范围。如果请求的范围与现有映射冲突，则此调用失败并返回错误 `EEXIST`。因此，该标志可用作一种（相对于其他线程）原子地尝试映射地址范围的方式：一个线程将成功，所有其他线程将报告失败。

    请注意，不识别 `MAP_FIXED_NOREPLACE` 标志的旧内核通常（在检测到与现有映射冲突时）会回退到“非 `MAP_FIXED`”类型的行为：它们将返回一个与请求地址不同的地址。因此，向后兼容的软件应将返回的地址与请求的地址进行比较。

```asm
mmap((void*)0x1337000, 0x100000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_FIXED, challenge_fd, 0);
    ; rax syscall 9
    ; rdi addr, 
    ; rsi length, 
    ; rdx prot, 
    ; r10 flags,
    ; r8 fd, 
    ; r9 offset

    mov rdi, 0x1337000
    mov rsi, 0x1000
    mov rdx, 3
    mov r10, 0x11
    mov r8, 3
    mov r9, 0
    mov rax, 9
    syscall
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

`def_action`
- kill 0 
- allow 0x7fff0000

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

`action`：
- `SCMP_ACT_ALLOW` 0x7fff0000
- `SCMP_ACT_KILL` 0

### seccomp_load

```c
#include <seccomp.h>

typedef void * scmp_filter_ctx;

int seccomp_load(scmp_filter_ctx ctx);
```

将提供的 seccomp 过滤器加载到内核中；如果函数成功，新的 seccomp 过滤器将在函数返回时生效。如果在进行加载 seccomp 过滤器之前调用了 seccomp_precompute(3)，并且过滤器没有发生任何更改，则 seccomp_load()可以被认为是异步信号安全的。

### dirname 

`dirname [选项] 文件名...`

从文件路径字符串中提取目录部分






### setns - 将线程与一个命名空间重新关联

```c
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>

int setns(int fd, int nstype);
```

setns() 系统调用允许调用线程切换到不同的命名空间。`fd` 参数是以下之一：
- 指向 /proc/pid/ns/ 目录中某个魔法链接的文件描述符（或指向该链接的绑定挂载）；
    - 注意打开文件句柄的读写权限，或许仅可读，或许仅可写
- 一个 PID 文件描述符（参见 pidfd_open(2)）。

如果调用者知道（或不在乎）fd 所引用的命名空间类型，则指定 `nstype` 为 0 即可。如果调用者不知道 fd 所引用的命名空间类型，并希望确保该命名空间是特定类型，则指定非零值的 nstype 会很有用。（调用者可能不知道 fd 所引用的命名空间类型，如果文件描述符是由其他进程打开的，并通过例如 UNIX 域套接字传递给调用者。）

### chmod

```c
#include <sys/stat.h>

int chmod(const char *path, mode_t mode);
int fchmod(int fd, mode_t mode);
```

suid 为 4xxx

```asm
; rax syscall 90
; rdi 路径字符串，此处为 a
; rsi 权限模式，此处为 other read 4

xor edi, edi
push 97
push rsp
pop rdi

xor esi, esi
push 4
pop rsi

xor eax, eax
mov al, 90
syscall
```
### open, openat, creat - 打开并可能创建文件

```c
#include <fcntl.h>

int open(const char *path, int flags, ...
            /* mode_t mode */ );

int creat(const char *path, mode_t mode);

int openat(int dirfd, const char *path, int flags, ...
            /* mode_t mode */ );
```

open 也可打开目录为 fd
openat dirfd的-100表示当前工作目录

- `O_APPEND`
    文件以追加模式打开。在每次 `write(2)` 之前，文件偏移量会被定位到文件末尾，就像调用了 `lseek(2)` 一样。文件偏移量的修改和写操作作为一个单一的原子步骤执行。

    如果在 NFS 文件系统上多个进程同时向一个文件追加数据，`O_APPEND` 可能会导致文件损坏。这是因为 NFS 不支持追加到文件，所以客户端内核必须模拟它，而模拟过程无法避免竞争条件。
    

open 汇编示例：
- 64
    ```asm
    ; 无 0x00 版
    ; rax 系统调用号 2
    ; rdi 路径，此处为 /flag
    ; rsi 模式，此处为 O_RDONLY 0

    mov edi, 0x67616c66
    shl rdi, 8
    mov dil, 0x2f
    push rdi
    mov rdi, rsp

    xor rsi, rsi
    xor rax, rax
    mov al, 2
    syscall
    ```
- 32
    ```asm
    ; rax 32位系统调用号 5
    ; rbx 路径字符串，此处为 flag
    ; rcx 打开模式，此处为只读 0

    mov eax, 5
    push 0x67616c66
    push rsp
    pop rbx  
    mov ecx, 0
    int 0x80
    ```

openat 汇编示例：
- 64
    ```asm
    ; rax 系统调用号 257
    ; rdi 目录 fd，此处为 3
    ; rsi 文件路径字符串，此处为 flag
    ; rdx 模式，此处为 0

    mov rax, 257    
    mov rdi, 3                  
    push 0x67616c66
    push rsp
    pop rsi         
    xor edx, edx        
    syscall
    ```
- 32
    ```asm
    ; rax 32位系统调用号 295
    ; rbx 目录 fd，此处为 4
    ; rcx 文件路径字符串指针，此处为 0x1337100
    ; rdx 模式，此处为 0

    mov rax, 295    
    mov rbx, 4           
    mov rcx, 0x1337100 
    xor edx, edx        
    int 0x80
    ```

### exit_group - 终止调用进程所属线程组中的所有线程

```c
#include <sys/syscall.h>       /* Definition of SYS_* constants */
#include <unistd.h>

[[noreturn]] void syscall(SYS_exit_group, int status);
```

注意：glibc 并未提供 `exit_group()` 的包装函数，因此必须使用 `syscall(2)`。

**描述**

该系统调用将终止调用进程所属线程组中的所有线程。

**返回值**

该系统调用不会返回。

```asm
    mov rdi, 77
    mov rax, 231
    syscall
```

### write - 写入文件描述符

```c
#include <unistd.h>

ssize_t write(int fd, const void buf[count], size_t count);
```

write() 将最多 count 个字节从以 buf 开头的缓冲区写入由文件描述符 fd 指向的文件。

```asm
; rax 系统调用号 1
; rdi outfd，此处为标准输出 1
; rsi buf，此处为之前系统调用保存到栈的指针
; rdx 字符数量，此处为 0x10

push rax
push rsp
pop rsi
mov rax, 1
mov edi, 1
mov rdx, 0x10
syscall
```

### sendfile - 在文件描述符之间传输数据

```c
#include <sys/sendfile.h>

ssize_t sendfile(int out_fd, int in_fd, off_t *_Nullable offset,
                size_t count);
```

sendfile() 在一个文件描述符和另一个文件描述符之间复制数据。由于这种复制是在内核中完成的，因此 sendfile() 比 read(2)和 write(2)的组合更高效，后者需要将数据在用户空间和内核空间之间传输。
- `in_fd` 应该是一个以读模式打开的文件描述符，`out_fd` 应该是一个以写模式打开的描述符。
- 如果 `offset` 不为 NULL，则它指向一个变量，该变量包含 sendfile()将从 in_fd 读取数据的文件偏移量。当 sendfile()返回时，该变量将被设置为读取的最后一个字节之后的字节的偏移量。如果 offset 不为 NULL，则 sendfile()不会修改 in_fd 的文件偏移量；否则，文件偏移量将调整为反映从 in_fd 读取的字节数。
- 如果 offset 为 NULL，则数据将从 in_fd 的文件偏移量处开始读取，并且调用将更新文件偏移量。
- `count` 是要在文件描述符之间复制的字节数。
- `in_fd` 参数必须对应一个支持 mmap(2)类操作（即不能是套接字）的文件。但自 Linux 5.12 起，如果 out_fd 是一个管道，sendfile()会降级为 splice(2)，并适用其限制。


64位：
```asm
;无 0x00 版
; rax 系统调用号 40
; rdi 写 fd，此处为标准输出 1
; rsi 读 fd，此处为之前调用返回值 rax 传递的 fd
; rdx 偏移量，此处为 0
; r10 复制字节数

xor rdi, rdi
inc rdi
mov rsi, rax
xor rdx, rdx

xor r10, r10
inc r10
shl r10, 10

xor rax, rax
mov al, 40
syscall
```

32位：
```asm
; rax 32位系统调用号 239
; rbx 写 fd，此处为标准输出 1
; rcx 读 fd，此处为之前调用返回值 rax 传递的 fd
; rdx 偏移量，此处为 0
; rsi 复制字节数

mov rbx, 1
mov rcx, rax
xor rdx, rdx
mov rsi, 0x60
mov rax, 239
int 0x80
```

### setresuid、setresgid - 设置真实、有效和已保存的用户或组 ID

```c
#define _GNU_SOURCE /* See feature_test_macros(7) */
#include <unistd.h>

int setresuid(uid_t ruid, uid_t euid, uid_t suid);
int setresgid(gid_t rgid, gid_t egid, gid_t sgid);
```

setresuid() 函数设置调用进程的实际用户 ID、有效用户 ID 和已保存的 set-user-ID。

### link, linkat - 为文件创建新名称

```c
#include <unistd.h>

int link(const char *oldpath, const char *newpath);

#include <fcntl.h>           /* Definition of AT_* constants */
#include <unistd.h>

int linkat(int olddirfd, const char *oldpath,
            int newdirfd, const char *newpath, int flags);
```

link() 创建一个指向现有文件的新链接（也称为硬链接）。

linkat() linkat() 系统调用与 link() 完全相同，除了此处描述的差异。
- 如果 oldpath 中的路径名是相对的，那么它将相对于由文件描述符 olddirfd 引用的目录进行解释（而不是像 link()那样相对于调用进程的当前工作目录）。
- 如果 oldpath 是相对的且 olddirfd 是特殊值 AT_FDCWD，那么 oldpath 将相对于调用进程的当前工作目录进行解释（类似于 link()）。
- 如果 oldpath 是绝对的，那么 olddirfd 将被忽略。
- newpath 的解释方式与 oldpath 相同，只是相对路径名将相对于由文件描述符 newdirfd 引用的目录进行解释。

linkat 汇编示例：
```asm
; rax 系统调用号 265
; rdi 旧目录 fd，此处为 3
; rsi 旧文件路径，此处为 flag
; rdx 新目录 fd，此处为当前工作目录 -100
; r10 新文件路径，此处为 gg
; r8 模式，此处为 0

mov rax, 265         
mov rdi, 3 
xor esi, esi
push 0x67616c66
push rsp
pop rsi      
mov rdx, -100    
push 0x6767
push rsp
pop r10  
xor r8d, r8d 
syscall
```

### chdir, fchdir - 改变工作目录

```c
#include <unistd.h>

int chdir(const char *path);
int fchdir(int fd);
```

chdir() 函数将调用进程的当前工作目录更改为 path 参数指定的目录。
fchdir() 与 chdir() 相同；唯一区别在于目录是通过打开的文件描述符给出的。

chdir 汇编示例：
```asm
; rax 系统调用号 80
; rdi 目录路径字符串，此处为 ../../

mov rax, 80
mov rdi, 0x2F2E2E2F2E2E
push rdi
push rsp
pop rdi 
syscall
```

fchdir 汇编示例：
```asm
; rax 系统调用号 81
; rdi 目录 fd，此处为 3

mov rax, 81         
mov rdi, 3 
syscall
```
### mkdir, mkdirat - 创建目录

```c
#include <sys/stat.h>

int mkdir(const char *path, mode_t mode);

#include <fcntl.h>           /* Definition of AT_* constants */
#include <sys/stat.h>

int mkdirat(int dirfd, const char *path, mode_t mode);
```

mkdir()尝试创建一个名为 path 的目录。

mkdirat() mkdirat()系统调用与 mkdir()完全相同，除了这里描述的区别。
- 如果 path 是相对路径，则它相对于由文件描述符 dirfd 引用的目录进行解释（而不是像 mkdir()对相对路径那样相对于调用进程的当前工作目录）。
- 如果路径是相对的，并且 dirfd 是特殊值 AT_FDCWD，那么路径相对于调用进程的当前工作目录被解释（类似于 mkdir()）。
- 如果路径是绝对的，那么 dirfd 会被忽略。

mkdir 汇编示例：
```asm
; rax 系统调用号 83
; rdi 路径字符串，此处为 gg
; rsi 权限模式，此处为8进制 0777

mov rax, 83         
push 0x6767
push rsp
pop rdi 
mov rsi, 0777  
syscall
```

### chroot - 更改根目录

```c
#include <unistd.h>

int chroot(const char *path);
```

```asm
; rax 系统调用号 161
; rdi 路径，此处为 gg

mov rax, 161         
push 0x6767
push rsp
pop rdi   
syscall
```

### umask - 设置文件模式创建掩码

```c
#include <sys/stat.h>

mode_t umask(mode_t mask);
```

umask() 将调用进程的文件模式创建掩码（umask）设置为掩码 & 0777（即，仅使用掩码的文件权限位），并返回掩码的先前值。

umask 由 open(2)、mkdir(2) 和其他创建文件的系统调用使用，以修改新创建文件或目录的权限。具体来说，umask 中的权限会从 open(2) 和 mkdir(2) 的 mode 参数中关闭。

```asm
; rax 系统调用号 95
; rdi mask，此处清空到 0

mov eax, 95
xor edi, edi
syscall
```

### exit

```c
#include <stdlib.h>  

[[noreturn]] void exit(int status);
```

64位：
```asm
; 无 0x00 版
; rax 系统调用号 60
; rdi 退出码

xor rdi, rdi
xor rax, rax
mov al, 60
syscall
```

32位：
```asm
; rax 32位系统调用号 1
; rbx 退出码

mov eax, 1
xor ebx, ebx
int 0x80   
```

### read - 从文件描述符中读取

```c
#include <unistd.h>

ssize_t read(int fd, void buf[count], size_t count);
```

read() 尝试从文件描述符 fd 中读取最多 count 个字节到从 buf 开始的缓冲区中。

64位：
```asm
; rax 系统调用号 0
; rdi fd
; rsi buf
; rdx count

xor eax, eax
mov rdi, 3
mov rsi, 0x1337100
mov rdx, 0x40
syscall
```

### nanosleep - 高精度休眠

```c
int nanosleep(const struct timespec *duration,
                struct timespec *_Nullable rem);

struct timespec {
    time_t tv_sec;   // 8字节结构，秒 (seconds)
    long   tv_nsec;  // 纳秒 (nanoseconds)
};
```

nanosleep() 暂停调用线程的执行，直到至少经过 *duration 指定的时间，或者收到一个触发调用线程中的处理器调用的信号，或者进程终止。

如果调用被信号处理器中断，nanosleep() 返回 -1，将 errno 设置为 EINTR，并将剩余时间写入由 rem 指向的结构，除非 rem 为 NULL。然后可以使用 *rem 的值再次调用 nanosleep() 以完成指定的暂停（但请参阅注意事项）。

```asm
; rax 系统调用号 35
; rdi duration结构指针，此处为 0x1337090
; rsi rem，此处设置 NULL 0

mov eax, 35
mov rdi, 0x1337090
xor esi, esi
syscall
```

### socketpair

```c
#include <sys/socket.h>

int socketpair(int domain, int type, int protocol, int sv[2]);
```

socketpair () 调用会创建一个未命名的连接套接字对。
在指定的域中，以指定的类型，并使用可选的协议。
创建的文件描述符分别存储在 `sv[0]` 和 `sv[1]` 中

### printf, fprintf, sprintf, snprintf, vprintf, vfprintf, vsprintf, vsnprintf - 格式化输出转换

```c
#include <stdio.h>

int printf(const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
int sprintf(char *str, const char *format, ...);
int snprintf(char *str, size_t size, const char *format, ...);

#include <stdarg.h>

int vprintf(const char *format, va_list ap);
int vfprintf(FILE *stream, const char *format, va_list ap);
int vsprintf(char *str, const char *format, va_list ap);
int vsnprintf(char *str, size_t size, const char *format, va_list ap);
```

printf () 函数族会按照下述格式生成输出。
- printf ( ) 函数和 vprintf () 将输出写入标准输出流 stdout ； 
- fprintf () 和 vfprintf () 将输出写入指定的输出 stream ； 
- sprintf ()、 snprintf ()、 vsprintf () 和 vsnprintf () 向字符串 str 写入数据。

函数 snprintf () 和 vsnprintf () 最多向 str 写入 size 字节（包括终止空字节 ('\0')）。

这八个函数根据格式字符串的控制写入输出，该格式字符串指定如何将后续参数（或通过 stdarg (3) 的可变长度参数功能访问的参数）转换为输出。

C99 和 POSIX.1-2001 规定，如果调用 sprintf ()、 snprintf ()、 vsprintf () 或 vsnprintf() 会导致在重叠对象之间进行复制（例如，如果目标字符串数组和提供的输入参数之一引用同一个缓冲区），则结果未定义 。请参阅注释。

### pivot_root - 更改根文件系统

```c
int pivot_root(const char *new_root, const char *put_old);
```

pivot_root () 将调用进程的根文件系统移动到 put_old 目录，并将 new_root 设置为调用进程的新根文件系统。

new_root 不一定是挂载点。在这种情况下， /proc/mounts 将显示包含 new_root 的文件系统的挂载点。 作为根（ / ）。
- 当设置目录路径不是挂载点时，将挂载承载此目录路径的挂载点，而不是目录路径本身。设置目标目录路径自我挂载以确保挂载到预期位置

### unshare - 分离进程执行上下文的各个部分

```c
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>

int unshare(int flags);
```

`unshare ()` 函数允许进程解除与其他进程共享的执行上下文部分。当使用 `fork (2)` 或 `vfork (2)` 创建新进程时，执行上下文的一部分（例如挂载命名空间）会被隐式共享；而其他部分（例如虚拟内存）则可以通过显式请求在使用 `clone (2)` 创建进程时进行共享。

unshare () 的主要用途是允许进程控制其共享的执行上下文，而无需创建新进程。

flags 参数是一个位掩码，用于指定执行上下文的哪些部分不应共享。该参数通过将以下零个或多个常量进行按位或运算来指定：
- `CLONE_NEWNS`
    此标志与 clone (2) CLONE_NEWNS 标志的效果相同。取消共享挂载命名空间，以便调用进程拥有其命名空间的私有副本，该副本不与其他任何进程共享。指定此标志会自动同时启用 CLONE_FS。CLONE_NEWNS 的用法 需要 CAP_SYS_ADMIN 权限。

### mount - 挂载文件系统

```c
#include <sys/mount.h>

int mount(const char *source, const char *target,
          const char *filesystemtype, unsigned long mountflags,
          const void *data);
```

mount () 将源 （通常是设备名称，但也可能是目录名称或虚拟名称）指定的文件系统附加到目标指定的目录。

挂载标志 mountflags：
- `MS_BIND` 0x1000
    执行绑定挂载，使文件系统中的某个文件或目录子树在另一位置可见。 绑定挂载可以跨越文件系统边界，甚至跨越 chroot (2) 隔离区。filesystemtype 和 data 参数会被忽略。在 Linux 2.6.26 之前， mountflags 参数也会被忽略（绑定挂载的挂载选项与底层挂载点相同）。
- `MS_REC`
    与 MS_BIND 结合使用以创建递归绑定挂载，并与传播类型标志结合使用以递归地更改子树中所有挂载的传播类型。
- `MS_PRIVATE` 
    使其挂载为私有。挂载和卸载事件**不会传播**到这个挂载点内外。
- `MS_REMOUNT` 0x20
    重新挂载
- `MS_RDONLY`
    以只读方式挂载文件系统。

```asm
; mount(NULL, "/data", NULL, MS_REMOUNT|MS_BIND, NULL) 
; rax 系统调用号 165
; rdi source 字符串指针，此处为 NULL 0
; rsi target 字符串指针，此处为栈中的 /data
; rdx filesystemtype，此处为 NULL 0
; r10 mountflags，此处为 0x1000 | 0x20
; r8 data，此处为 NULL 0

mov eax, 165
xor edi, edi
mov rsi, 0x617461642f
push rsi
push rsp
pop rsi
xor rdx, rdx
mov r10, 0x1020
xor r8, r8
syscall
```

### umount、umount2 - 卸载文件系统

```c
#include <sys/mount.h>

int umount(const char *target);
int umount2(const char *target, int flags);
```

umount() 和 umount2() 删除在目标上挂载的（最顶层）文件系统的连接。

Linux 2.1.116 版本添加了 umount2() 系统调用，它和 umount() 类似，可以卸载目标，但允许使用额外的标志来控制操作的行为：

- `MNT_DETACH`
    执行惰性卸载：使挂载不可用于新的访问，立即将文件系统及其所有下层挂载的文件系统与彼此以及与挂载表断开连接，并在挂载不再繁忙时实际执行卸载。

### chown、fchown、lchown、fchownat - 更改文件的所有权

```c
#include <unistd.h>

int chown(const char *path, uid_t owner, gid_t group);
int fchown(int fd, uid_t owner, gid_t group);
int lchown(const char *path, uid_t owner, gid_t group);

#include <fcntl.h>           /* Definition of AT_* constants */
#include <unistd.h>

int fchownat(int dirfd, const char *path,
            uid_t owner, gid_t group, int flags);
```

chown汇编：
```asm
; rax syscall 92
; rdi path，此处为 /data/mc
; rsi owner，此处为 root 的 0
; rdx group，此处为 root 的 0

mov rax, 92
xor rdi, rdi
push rdi
mov rdi, 0x636d2f617461642f
push rdi
push rsp
pop rdi
xor rsi, rsi
xor rdx, rdx
syscall
```

### ioctl - 控制设备

```c
#include <sys/ioctl.h>

int ioctl(int fd, unsigned long op, ...);  /* glibc, BSD */
int ioctl(int fd, int op, ...);            /* musl, other UNIX */
```

ioctl() 系统调用操作特殊文件的底层设备参数。特别是，许多字符特殊文件（例如终端）的操作特性可以通过 ioctl() 操作进行控制。参数 fd 必须是一个打开的文件描述符。

第二个参数是一个与设备相关的操作码。第三个参数是一个无类型的内存指针。传统上它是 char *argp（来自 void * 在 C 语言中有效之前的时代），并在本次讨论中这样命名。

ioctl() 操作编码了参数是输入参数还是输出参数，以及参数 argp 的大小（以字节为单位）。用于指定 ioctl() 操作的宏和定义位于文件 `<sys/ioctl.h>` 中。参见注释。

```asm
; syscall 编号 16
; rdi, fd 3
; rsi, op 0x539
; rdx, 0

    mov rdi, 3
    mov rsi, 0x539
    mov rdx, 0
    mov rax, 16
    syscall
```

### memset - 用常量字节填充内存区域


```c
#include <string.h>

void *memset(size_t n;
            void s[n], int c, size_t n);
```

`memset()` 函数将从 `s` 指向的内存区域的前 `n` 个字节填充为常量字节 `c`。


### sem_getvalue - 获取信号量的当前值

```c
#include <semaphore.h>

int sem_getvalue(sem_t *restrict sem, int *restrict sval);
```

`sem_getvalue()` 将 `sem` 指向的信号量的当前值存入 `sval` 指向的整型变量中。

如果存在一个或多个进程或线程阻塞在 `sem_wait(3)` 上等待锁定该信号量，POSIX.1 允许 `sval` 返回两种可能的值：要么返回 0；要么返回一个负数，其绝对值表示当前阻塞在 `sem_wait(3)` 上的进程和线程数量。Linux 采用前一种行为（返回 0）。

### strnstr - 在长度受限的字符串中查找第一个子串

```c
/**
 * @s1: 要被搜索的字符串
 * @s2: 要搜索的子串
 * @len: 要搜索的最大字符数
 */
char *strnstr(const char *s1, const char *s2, size_t len)
{
	size_t l2;

	l2 = strlen(s2);
	if (!l2)
		return (char *)s1;
	while (len >= l2) {
		len--;
		if (!memcmp(s1, s2, l2))
			return (char *)s1;
		s1++;
	}
	return NULL;
}
```

```asm
; rdi 获取之前函数得到的地址
; rsi "pwn.college{"
; rdx 4096

    mov rdi, rax
    lea rsi, [rip + goal]
    mov rdx, 4096
    mov rax, 0xffffffff81a9f540
    call rax

goal:
    .asciz "pwn.college{"
```

### shm_open, shm_unlink - 创建/打开或删除POSIX共享内存对象

```c
#include <sys/mman.h>
#include <sys/stat.h> /* For mode constants */
#include <fcntl.h> /* For O_* constants */

int shm_open(const char *name, int oflag, mode_t mode);

int shm_unlink(const char *name);
```

shm_open() 创建并打开一个新的 POSIX 共享内存对象，或者打开一个已存在的 POSIX 共享内存对象。POSIX 共享内存对象实际上是一个句柄，不同进程可以使用 mmap(2) 访问同一区域的共享内存。shm_unlink() 函数执行相反的操作，删除先前由 shm_open() 创建的对象。

shm_open() 的操作类似于 open(2)。name 指定要创建或打开的共享内存对象的名称。为了可移植性，共享内存对象应该由形如 /somename 的名称标识；即，一个以空字符终止的字符串，最多包含 NAME_MAX（即 255）个字符，由一个初始斜杠后跟一个或多个非斜杠字符组成。

### truncate, ftruncate - 将文件截断到指定长度

```c
#include <unistd.h>

int truncate(const char *path, off_t length);
int ftruncate(int fd, off_t length);
```

`truncate()` 和 `ftruncate()` 函数会将指定路径 `path` 或文件描述符 `fd` 所指向的常规文件截断或扩展至精确的 `length` 字节长度。

如果文件原先大于该长度，超出部分的数据将丢失。如果文件原先小于该长度，文件将被扩展，扩展部分读取时返回空字节（`'\0'`）。

文件偏移量不受影响。

如果文件大小发生变化，文件的 `st_ctime` 和 `st_mtime` 字段（分别对应最后状态更改时间和最后修改时间，参见 `inode(7)`）将被更新，并且设置用户 ID 位和设置组 ID 位可能会被清除。

对于 `ftruncate()`，文件必须以写入方式打开；对于 `truncate()`，文件必须可写。

### sched_getcpu - 确定调用线程正在运行的CPU

```c
#include <sched.h>

int sched_getcpu(void);
```

`sched_getcpu()` 返回调用线程当前正在执行的 CPU 编号。

成功时，`sched_getcpu()` 返回一个非负的 CPU 编号。出错时，返回 -1，并设置 `errno` 以指示错误类型。

### sched_setaffinity, sched_getaffinity - 设置和获取线程的CPU亲和性掩码

```c
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>

int sched_setaffinity(pid_t pid, size_t cpusetsize,
                        const cpu_set_t *mask);
int sched_getaffinity(pid_t pid, size_t cpusetsize,
                        cpu_set_t *mask);
```

线程的 CPU 亲和性掩码决定了该线程允许在哪些 CPU 上运行。在多处理器系统上，设置 CPU 亲和性掩码可用于获得性能提升。例如，通过将一个 CPU 专用于某个特定线程（即，将该线程的亲和性掩码设置为指定单个 CPU，并将所有其他线程的亲和性掩码设置为排除该 CPU），可以确保该线程获得最大执行速度。将线程限制在单个 CPU 上运行，还可以避免线程在一个 CPU 上停止执行后在另一个 CPU 上重新执行时因缓存失效而带来的性能开销。

CPU 亲和性掩码通过 `cpu_set_t` 结构体表示，即由 `mask` 指向的“CPU 集”。用于操作 CPU 集的一组宏在 `CPU_SET(3)` 中进行了描述。

`sched_setaffinity()` 将线程 ID 为 `pid` 的线程的 CPU 亲和性掩码设置为 `mask` 所指定的值。如果 `pid` 为零，则使用调用线程。参数 `cpusetsize` 是 `mask` 所指向数据的长度（以字节为单位）。通常该参数应指定为 `sizeof(cpu_set_t)`。

如果 `pid` 指定的线程当前未在 `mask` 所指定的任一 CPU 上运行，则该线程会被迁移到 `mask` 所指定的某个 CPU 上。

`sched_getaffinity()` 将线程 ID 为 `pid` 的线程的亲和性掩码写入 `mask` 所指向的 `cpu_set_t` 结构体中。`cpusetsize` 参数指定 `mask` 的大小（以字节为单位）。如果 `pid` 为零，则返回调用线程的掩码。

### CPU_ZERO, CPU_SET - 用于操作CPU集的宏

```c
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>

void CPU_ZERO(cpu_set_t *set);

void CPU_SET(int cpu, cpu_set_t *set);
```

**描述**

`cpu_set_t` 数据结构表示一组 CPU。CPU 集用于 `sched_setaffinity(2)` 及类似的接口。

`cpu_set_t` 数据类型实现为位掩码。然而，该数据结构应被视为不透明类型：所有对 CPU 集的操作都应通过本手册页中描述的宏来完成。

提供以下宏来操作 CPU 集 `set`：

*   `CPU_ZERO()` 清空 `set`，使其不包含任何 CPU。
*   `CPU_SET()` 将 CPU `cpu` 添加到 `set` 中。

当指定 `cpu` 参数时，它不应产生副作用，因为上述宏可能会多次对该参数求值。

系统上的第一个 CPU 对应 `cpu` 值为 0，下一个 CPU 对应 `cpu` 值为 1，依此类推。不应假设特定的 CPU 可用，也不应假设 CPU 集合是连续的，因为 CPU 可能被动态下线或因其他原因不存在。常量 `CPU_SETSIZE`（当前为 1024）指定了比 `cpu_set_t` 中可存储的最大 CPU 编号大 1 的值。

- `CPU_SET` 寻找 cpu 编号的组，再于组中寻找对应的位，并置位





### ptrace - 程序追踪

```c
#include <sys/ptrace.h>

long ptrace(enum __ptrace_request op, pid_t pid,
            void *addr, void *data);
```

**ptrace()** 系统调用提供了一种机制，允许一个进程（追踪器）观察和控制另一个进程（被追踪者）的执行，并检查和修改被追踪者的内存与寄存器。它主要用于实现断点调试和系统调用跟踪。

被追踪者首先需要被附加到追踪器上。附加及后续命令均按线程进行：在一个多线程进程中，每个线程都可以单独附加到一个（可能不同的）追踪器上，也可以保持未附加状态从而不被调试。因此，“被追踪者”始终指代“（单个）线程”，而非“一个（可能是多线程的）进程”。Ptrace 命令总是通过如下形式的调用来发送给特定的被追踪者：

```c
ptrace(PTRACE_foo, pid, ...)
```

其中 `pid` 是对应 Linux 线程的线程 ID。

（请注意，在本手册页中，“多线程进程”指由使用 `clone(2)` 的 `CLONE_THREAD` 标志创建的线程所组成的线程组。）

一个进程可以通过调用 `fork(2)` 并让产生的子进程执行 `PTRACE_TRACEME`，随后（通常）再执行 `execve(2)` 来发起追踪。或者，一个进程也可以使用 `PTRACE_ATTACH` 或 `PTRACE_SEIZE` 开始追踪另一个进程。

在被追踪期间，被追踪者每次收到信号时都会停止，即使该信号被忽略也是如此。（`SIGKILL` 是例外，它仍会发挥其通常的作用。）追踪器在其下一次调用 `waitpid(2)`（或相关的“wait”系列系统调用）时会收到通知；该调用会返回一个状态值，其中包含指示被追踪者停止原因的信息。当被追踪者停止时，追踪器可以使用各种 ptrace 操作来检查和修改被追踪者。随后，追踪器会让被追踪者继续运行，并可以选择忽略已送达的信号（甚至改为投递另一个信号）。

- `PTRACE_TRACEME ` 
    表示此进程将要被其父进程追踪。如果父进程并不期望追踪该进程，那么该进程不应执行此操作。（`pid`、`addr` 和 `data` 参数被忽略。）

    `PTRACE_TRACEME` 操作仅由被追踪者使用；其余操作仅由追踪者使用。在以下操作中，`pid` 指定要操作的被追踪者的线程 ID。除 `PTRACE_ATTACH`、`PTRACE_SEIZE`、`PTRACE_INTERRUPT` 和 `PTRACE_KILL` 之外的其他操作，要求被追踪者必须处于停止状态。

- `PTRACE_GETREGS, PTRACE_GETFPREGS`
    分别将被追踪者的通用寄存器或浮点寄存器复制到追踪者指定的 `data` 地址处。

### sem_wait - 信号量加锁

```c
#include <semaphore.h>

int sem_wait(sem_t *sem);
int sem_trywait(sem_t *sem);
int sem_timedwait(sem_t *restrict sem,
                    const struct timespec *restrict abs_timeout);
```

`sem_wait()` 用于递减（锁定）`sem` 指向的信号量。如果信号量的值大于 0，则递减操作立即执行，函数随即返回。如果信号量当前值为 0，则调用将阻塞，直到满足以下条件之一：可以执行递减操作（即信号量的值增至大于 0），或者信号处理程序中断了该调用。

### sem_post - 信号量解锁

```c
#include <semaphore.h>

int sem_post(sem_t *sem);
```

`sem_post()` 用于递增（解锁）`sem` 指向的信号量。如果信号量的值因此变为大于 0，则另一个在 `sem_wait(3)` 调用中阻塞的进程或线程将被唤醒，并继续执行锁定该信号量的操作。


### sleep - 睡眠秒

```c
#include <unistd.h>

unsigned int sleep(unsigned int seconds);
```

`sleep()` 会使调用线程睡眠，直到指定的实时秒数已经过去，或者直到有未被忽略的信号到达。


### usleep - 暂停执行微秒

```c
#include <unistd.h>

int usleep(useconds_t usec);
```

`usleep()` 函数会使调用线程的执行暂停（至少）`usec` 微秒。该睡眠时间可能会因任何系统活动、处理该调用所花费的时间或系统定时器的粒度而略微延长。

### stdint.h

`uint64_t/uint32_t`

### sched_yield - 线程让出 CPU

```c
#include <sched.h>

int sched_yield(void);
```

`sched_yield()` 使调用线程主动让出 CPU。该线程会被移至其静态优先级队列的末尾，然后由另一个新线程开始运行。

### memcpy - 复制内存区域

```c
#include <string.h>

void *memcpy(void dest[restrict .n], const void src[restrict .n], size_t n);
```

**描述**  
`memcpy()` 函数从内存区域 `src` 复制 `n` 个字节到内存区域 `dest`。这两个内存区域不能重叠。如果内存区域存在重叠，请使用 `memmove(3)`。

**返回值**  
`memcpy()` 函数返回指向 `dest` 的指针。

### memmove - 复制内存区域

```c
#include <string.h>

void *memmove(void dest[.n], const void src[.n], size_t n);
```

**描述**  
`memmove()` 函数从内存区域 `src` 复制 `n` 个字节到内存区域 `dest`。这两个内存区域可以重叠：复制操作的过程就好像先将 `src` 中的字节复制到一个临时数组中（该数组与 `src` 和 `dest` 均不重叠），然后再将字节从临时数组复制到 `dest`。

**返回值**  
`memmove()` 函数返回指向 `dest` 的指针。

### signal - 设置信号处理函数

```c
#include <signal.h>

void (*signal(int sig, void (*func)(int)))(int);
```

`sig`:
- `SIGSEGV`	(Signal Segmentation Violation) 
    非法访问存储器，如访问不存在的内存单元

`func`
- 自定义函数指针
- `SIG_DFL`	默认的信号处理程序
- `SIG_IGN`	忽视信号
 
### setjmp, sigsetjmp, longjmp, siglongjmp - 执行非局部跳转

```c
#include <setjmp.h>

int setjmp(jmp_buf env);
int sigsetjmp(sigjmp_buf env, int savesigs);

[[noreturn]] void longjmp(jmp_buf env, int val);
[[noreturn]] void siglongjmp(sigjmp_buf env, int val);
```

这些函数用于执行“非局部跳转”：
将执行流从一个函数转移到另一个函数中预设的位置。
- `setjmp()` 函数动态地建立控制流后续将要转移的目标
- `longjmp()` 执行实际的执行流转移

`setjmp()` 函数将调用环境的各类信息（通常是栈指针、指令指针，可能还包括其他寄存器的值以及信号掩码）保存到缓冲区 `env` 中，以供后续 `longjmp()` 使用。在直接调用时，`setjmp()` 返回 0。

`longjmp()` 函数利用保存在 `env` 中的信息，将控制流返回到之前调用 `setjmp()` 的位置，并将栈“回退”到 `setjmp()` 调用时的状态。此外，根据具体实现，某些其他寄存器的值以及进程信号掩码也可能被恢复到 `setjmp()` 调用时的状态。

在成功的 `longjmp()` 调用之后，程序的执行仿佛 `setjmp()` 进行了第二次返回。这种“伪返回”可以通过其返回值与真正的 `setjmp()` 调用区分开：因为“伪返回”返回的是 `val` 参数中提供的值。如果程序员错误地将 `val` 设为 0，那么“伪返回”将实际返回 1。

**sigsetjmp() 和 siglongjmp()**  
`sigsetjmp()` 和 `siglongjmp()` 同样执行非局部跳转，但提供了对进程信号掩码的可预测处理。

当且仅当提供给 `sigsetjmp()` 的 `savesigs` 参数为非零值时，进程当前的信号掩码会被保存到 `env` 中，并且如果后续使用该 `env` 执行 `siglongjmp()`，信号掩码将被恢复。

**返回值**  
`setjmp()` 和 `sigsetjmp()` 在直接调用时返回 0；在 `longjmp()` 或 `siglongjmp()` 之后发生的“伪返回”中，它们返回 `val` 中指定的非零值。

`longjmp()` 或 `siglongjmp()` 函数不会返回。

```c
sigjmp_buf env;

void sigsegv_handler(int sig) {
    siglongjmp(env, 1);
}

void main(){

    signal(SIGSEGV, sigsegv_handler);   

    if (sigsetjmp(env, 1) == 0) {
        // 首次执行，返回 0
    } else {
        // longjmp 控制流返回
    }
}
```

### fork - 创建子进程

```c
#include <unistd.h>

pid_t fork(void);
```

**描述**
fork() 通过复制调用进程来创建一个新进程。新进程被称为子进程，调用进程被称为父进程。

子进程和父进程运行在独立的内存空间中。在 fork() 时刻，两个内存空间具有完全相同的内容。其中一个进程执行的内存写入、文件映射 (mmap(2)) 和解除映射 (munmap(2)) 不会影响另一个进程。

子进程是父进程的精确副本，但以下几点除外：

• 子进程拥有自己唯一的进程 ID，并且该 PID 不与任何现有进程组 (setpgid(2)) 或会话相匹配。

• 子进程的父进程 ID 与父进程的进程 ID 相同。

• 子进程不继承父进程的内存锁 (mlock(2), mlockall(2))。

• 子进程的进程资源利用率 (getrusage(2)) 和 CPU 时间计数器 (times(2)) 被重置为零。

• 子进程的待处理信号集最初为空 (sigpending(2))。

• 子进程不从父进程继承信号量调整值 (semop(2))。

• 子进程不从父进程继承与进程相关的记录锁 (fcntl(2))。（另一方面，它确实从父进程继承了 fcntl(2) 打开文件描述锁和 flock(2) 锁。）

• 子进程不从父进程继承定时器 (setitimer(2), alarm(2), timer_create(2))。

• 子进程不从父进程继承未完成的异步 I/O 操作 (aio_read(3), aio_write(3))，也不继承任何异步 I/O 上下文（参见 io_setup(2)）。

上述列表中的进程属性均由 POSIX.1 规定。父进程和子进程在以下 Linux 特有的进程属性上也存在差异：

• 子进程不继承父进程的目录变更通知 (dnotify)（参见 fcntl(2) 中 F_NOTIFY 的描述）。

• prctl(2) PR_SET_PDEATHSIG 设置被重置，使得子进程在其父进程终止时不会收到信号。

• 默认的定时器宽容值（timer slack）设置为父进程当前的定时器宽容值。参见 prctl(2) 中 PR_SET_TIMERSLACK 的描述。

• 已使用 madvise(2) MADV_DONTFORK 标志标记的内存映射在 fork() 时不会被继承。

• 在 fork() 之后，已使用 madvise(2) MADV_WIPEONFORK 标志标记的地址范围内的内存在子进程中被清零。（对于子进程中这些地址范围，MADV_WIPEONFORK 设置仍然保留。）

• 子进程的终止信号始终是 SIGCHLD（参见 clone(2)）。

• 由 ioperm(2) 设置的端口访问权限位不会被子进程继承；子进程必须使用 ioperm(2) 开启它所需的任何位。

请注意以下几点：

• 子进程创建时只有一个线程——即调用 fork() 的那个线程。父进程的整个虚拟地址空间在子进程中被复制，包括互斥锁、条件变量和其他 pthreads 对象的状态；使用 pthread_atfork(3) 可能有助于处理由此可能引发的问题。

• 在多线程程序中调用 fork() 之后，子进程在调用 execve(2) 之前只能安全地调用异步信号安全函数（参见 signal-safety(7)）。

• 子进程继承父进程的打开文件描述符集合的副本。子进程中的每个文件描述符指向与父进程中相应文件描述符相同的打开文件描述（参见 open(2)）。这意味着两个文件描述符共享打开文件状态标志、文件偏移量和信号驱动 I/O 属性（参见 fcntl(2) 中 F_SETOWN 和 F_SETSIG 的描述）。

• 子进程继承父进程的打开消息队列描述符集合的副本（参见 mq_overview(7)）。子进程中的每个文件描述符指向与父进程中相应文件描述符相同的打开消息队列描述。这意味着两个文件描述符共享相同的标志 (mq_flags)。

• 子进程继承父进程的打开目录流集合的副本（参见 opendir(3)）。POSIX.1 规定父进程和子进程中相应的目录流可以共享目录流定位；在 Linux/glibc 上，它们不共享。

**返回值**
成功时，在父进程中返回子进程的 PID，在子进程中返回 0。失败时，在父进程中返回 -1，不创建子进程，并设置 errno 以指示错误。

```asm
; syscall 57
; fork 返回值为 0 则对应子进程

    mov rax, 57
    syscall

    test rax, rax
    je child

parent:

child:

```

###  clone, __clone2, clone3 - 创建子进程

```c
#define _GNU_SOURCE
#include <sched.h>

int clone(typeof(int (void *_Nullable)) *fn,
            void *stack,
            int flags,
            void *_Nullable arg, ...
            /* pid_t *_Nullable parent_tid,
            void *_Nullable tls,
            pid_t *_Nullable child_tid */ );
```

**描述**

这些系统调用以类似于 fork(2) 的方式创建一个新的（“子”）进程。

与 fork(2) 相比，这些系统调用能够更精确地控制调用进程与子进程之间共享哪些执行上下文。例如，使用这些系统调用，调用者可以控制两个进程是否共享虚拟地址空间、文件描述符表以及信号处理函数表。这些系统调用还允许将新创建的子进程放入独立的命名空间（namespaces(7)）中。

请注意，在本手册页中，“调用进程”通常对应“父进程”。但请参阅下面关于 `CLONE_PARENT` 和 `CLONE_THREAD` 的描述。

本页描述以下接口：

*   glibc 的 `clone()` 包装函数及其所基于的底层系统调用。正文主要描述包装函数；原始系统调用的差异在本页末尾说明。
*   较新的 `clone3()` 系统调用。

在本页剩余部分中，当说明适用于所有这些接口的细节时，使用术语“clone 调用”。

**`clone()` 包装函数**

当使用 `clone()` 包装函数创建子进程时，子进程通过调用参数 `fn` 指向的函数开始执行。（这与 fork(2) 不同，fork(2) 中子进程从 fork(2) 调用点继续执行。）参数 `arg` 作为函数 `fn` 的参数传递。

当 `fn(arg)` 函数返回时，子进程终止。`fn` 返回的整数即为子进程的退出状态。子进程也可以通过调用 exit(2) 显式终止，或在收到致命信号后终止。

参数 `stack` 指定子进程所使用的栈的位置。由于子进程与调用进程可能共享内存，子进程无法在与调用进程相同的栈上执行。因此，调用进程必须为子进程的栈设置内存空间，并将指向该空间的指针传递给 `clone()`。在运行 Linux 的所有处理器（HP PA 处理器除外）上，栈都是向下增长的，因此 `stack` 通常指向为子进程栈所设置的内存空间的最高地址。请注意，`clone()` 并没有提供一种让调用者向内核告知栈区域大小的方式。


**版本说明**

glibc 的 `clone()` 包装函数在调用 `clone()` 系统调用之前，会对 `stack` 所指向的内存进行一些修改（这些修改是为了正确地为子进程设置栈）。因此，在使用 `clone()` 递归创建子进程的情况下，不要将父进程栈所使用的缓冲区用作子进程的栈。

在 i386 架构上，不应通过 vsyscall 调用 `clone()`，而应直接通过 `int $0x80` 调用。

**C 库/内核差异**

原始的 `clone()` 系统调用更接近于 `fork(2)`，因为子进程从调用点继续执行。因此，`clone()` 包装函数的 `fn` 和 `arg` 参数被省略了。

与 glibc 包装函数不同，原始的 `clone()` 系统调用允许将 `stack` 参数设置为 NULL（`clone3()` 同样允许 `cl_args.stack` 为 NULL）。在这种情况下，子进程使用父进程栈的副本（写时复制语义确保当任一进程修改栈时，子进程会获得栈页的独立副本）。此时，为了正确运行，不应指定 `CLONE_VM` 选项。（如果因为使用 `CLONE_VM` 标志而共享了父进程的内存，则不会发生写时复制，很可能导致混乱。）

原始系统调用中的参数顺序也有所不同，并且不同架构之间的参数也存在差异，具体如下所述。

在 x86-64 及其他一些架构（包括 sh、tile 和 alpha）上，原始系统调用接口为：

```c
long clone(unsigned long flags, void *stack,
                    int *parent_tid, int *child_tid,
                    unsigned long tls);
```

```asm
; syscall 编码 56
; 设置最简参数
; rdi, flags SIGCHLD
; rsi, stack 需为有效地址，不共享时设置 0

    mov rdi, 0x11
    mov rsi, 0 
    mov rdx, 0
    mov r10, 0
    mov r8, 0
    mov rax, 56
    syscall

    test rax, rax
    je child

parent:


child:


```

## 汇编头文件

### emmintrin.h

```c
_mm_clflush (void const *__A)
{
  __builtin_ia32_clflush (__A);
}

_mm_lfence (void)
{
  __builtin_ia32_lfence ();
}

_mm_mfence (void)
{
  __builtin_ia32_mfence ();
}
```

- `_mm_clflush`
    刷新缓存行，写回并清除
    - 当前挑战为 64 字节
    - `clflush` 对不存在的页面触发段错误

- `_mm_lfence`
    内存顺序加载
    - 似乎额外拥有同步之前指令的功能

- `_mm_mfence`
    内存顺序加载与存储

```asm
lfence
mfence 

;; clflush 寄存器保存地址
clflush [reg]
```

### xmmintrin.h

```c
_mm_sfence (void)
{
  __builtin_ia32_sfence ();
}
```

- `_mm_mfence`
    内存顺序存储

### ia32intrin.h & x86gprintrin.h

`error "Never use <ia32intrin.h> directly; include <x86gprintrin.h> instead."`

```c
__rdtsc (void)
{
  return __builtin_ia32_rdtsc ();
}
```

- `__rdtsc`
    cpu 计时

```asm
; 低rax， 高rdx
; 通常仅需 rax

rdtsc
shl rdx, 32
or rax, rdx
```

## GCC 内置

### __builtin_prefetch

https://gcc.gnu.org/onlinedocs/gcc-3.3.6/gcc/Other-Builtins.html

内置函数：`void __builtin_prefetch (const void *addr, ...)`  

该函数用于在数据被访问之前将其移入缓存，从而最大程度地减少缓存未命中的延迟。可以在代码中插入对 `__builtin_prefetch` 的调用，只要你知道内存中哪些地址的数据很可能即将被访问。如果目标平台支持，则会生成数据预取指令。如果在访问之前足够早地执行预取，那么当访问发生时，数据就已经在缓存中了。

`addr` 的值是要预取的内存地址。
有两个可选参数 `rw` 和 `locality`：
- `rw` 的值是一个编译时常量，为 1 或 0；
    - 1 表示预取是为写入该内存地址做准备
    - 0（默认值）表示预取是为读取做准备。
- `locality` 的值必须是介于 0 到 3 之间的编译时常量整数。
    - 值为 0 表示数据没有时间局部性，因此在访问之后无需将其保留在缓存中。
    - 值为 3 （默认值）表示数据具有高度的时间局部性，应尽可能保留在所有级别的缓存中。
    - 值为 1 和 2 分别表示时间局部性较低或中等。

```c
for (i = 0; i < n; i++)
  {
    a[i] = a[i] + b[i];
    __builtin_prefetch (&a[i+j], 1, 1);
    __builtin_prefetch (&b[i+j], 0, 1);
    /* ... */
  }
```

如果 `addr` 无效，数据预取不会产生错误，但地址表达式本身必须有效。例如，预取 `p->next` 时，如果 `p->next` 不是有效地址，不会触发错误；但如果 `p` 本身不是有效地址，则在求值时就会触发错误。

如果目标平台不支持数据预取，则会对地址表达式进行求值（如果它包含副作用），但不会生成其他代码，GCC 也不会发出警告。

```asm
; __builtin_prefetch 寄存器保存地址
; prefetcht. 与 prefetchnta 不区分 rw

prefetcht0 [rdi]    ; locality 3
prefetcht1 [rdi]    ; locality 2
prefetcht2 [rdi]    ; locality 1
prefetchnta [rdi]   ; locality 0 (non-temporal)
```

## 备忘

- `scanf`  遇到 `\n`（空白字符）停止读取，读取字符串时自动在末尾添加 `\x00`

- `atoi` 字符串转整型

- `%p` 输出的地址可能被混淆/截断
- `%px` 输出原始十六进制地址

- `volatile` 变量类型前缀，确保访问内存且不被优化掉

- 内联汇编
    ```c
    asm volatile(
    "lea rbx, [%0]\n"
    :
    : "r"(addr)
    : "rbx"
    );
    ```
    - `%0` 参数索引，访问之后的参数
    - `: "r"(addr)` 参数列表，参数0放入 `r` 通用寄存器中
    - `: "rbx"` 破坏列表，声明 rbx 已被破坏

- 结构定义时末尾添加分号
- 结构字段初始化：`struct stname varname = {1, 2, 3, 4, 5};`
