## 获得shellcode

写汇编代码 - 编译为可执行文件 - 提取指令字段
- 命令行组合：
    ```sh
    # 无链接库、静态
    gcc -nostdlib -static -o shellcode-elf shellcode.s 

    # 复制指令字段
    objcopy --dump-section .text=shellcode-raw shellcode-elf
    ```

- python与pwntools
    ```py
    from pwn import *
    context.arch = "amd64"
    sc_bytes = asm("""
        mov rdi, 0x1337
        mov rax, 60
        syscall
    """)
    # 打印反汇编内容
    print(disasm(sc_bytes))
    ```

    或需先运行 `tmux`
    ```py
    from pwn import *
    context.arch = "amd64"
    # 设置终端
    context.terminal = ["tmux", "splitw", "-h"]
    # 打印出收发字节的 debug 信息
    context.log_level = "debug"
    # 使用gdb调试汇编
    p = gdb.debug_assembly("""
        mov rdi, 0x1337
        mov rax, 60
        syscall
    """)
    # 停止，或使用 p.interactive()
    pause()
    ```

    或需先运行 `tmux`
    ```py
    from pwn import *
    context.arch = "amd64"
    # 设置终端
    context.terminal = ["tmux", "splitw", "-h"]
    # 使用gdb调试程序，使用 gdb 的自定义脚本时需关闭 gef 插件，否则仅显示 gef 默认界面
    p = gdb.debug("/challenge/run", """
        display/3i $rip
        display/3i $rsp
        display/4gx $rsp
        display/6gx $rbp-0x30
        display/4gx $rbp
        b * main
    """, setuid=False, aslr=False)
    # 停止
    p.interactive()
    ```

- 无空字节: 使用位移、低段寄存器移动、异或等方式消除空格字节
    

## 调试shellcode

- 在代码中添加对于gdb调试的 int3 汇编硬编码调试断点
- 添加汇编标签后设置调试断点
- strace
- 内存映射
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
    `cat shellcode-raw | ./tester`


## 常见错误
- 大小字段
    ```log
    single byte:
    mov [rax], bl
    2-byte word:
    mov [rax], bx
    4-byte dword:
    mov [rax], ebx
    8-byte qword:
    mov [rax], rbx

    single byte:
    mov BYTE PTR [rax], 5
    2-byte word:
    mov WORD PTR [rax], 5
    4-byte dword:
    mov DWORD PTR [rax], 5
    8-byte qword:
    mov QWORD PTR [rax], 5
    ```

- 函数的输入终止字符  
    ```log
    Byte (Hex Value)            Problematic Methods
    Null byte \0 (0x00)         strcpy
    Newline \n (0x0a)           scanf gets getline fgets
    Carriage return \r (0x0d)   scanf
    Space (0x20)                scanf
    Tab \t (0x09)               scanf
    DEL (0x7f)                  protocol-specific (telnet, VT100, etc)
    ```
    即，对应的注入点函数需在载荷中避免对应字符

## 复刻文件

- 对原 c 文件进行复制并修改 c 源代码后编译得到复刻程序，使用 gdb 进入复刻程序获得栈地址。虽然无法完全使用gdb对原程序进行调试，但可进入main开头获得rsp地址，以计算与本地复刻程序的差值，使用此差值即可实现地址覆盖 ———— 栈地址校准

    `gcc -g -O0 -no-pie -fno-stack-protector  -z execstack -o integration-web-overflow integration-web-overflow.c`
    - 使用与程序匹配的调试级编译，并匹配地址随机、栈保护、栈执行设置  

- 原可执行文件复刻后再进行库打桩，可能直接得到相同的栈地址。
    - 查看库打桩小节



## tips

- 若可执行shellcode，且当前位置可写，那么可尝试动态修改指令
- 读取金丝雀时，由于其第一字节为 `\x00` 于是载荷+1
- 基于分页中的低3个半字节不变，对地址进行部分覆盖爆破
    - 若地址随机可选择固定值爆破
    - 若地址固定（关闭随机或服务器这样仅初始随机而后续固定）应当使用遍历爆破

- 保护特性状态：
    - `checksec` 
        查看二进制文件的编译特性“声明”
    - `(gdb) info auxv` 
        运行时的环境与能力“提示位”
    - `grep -m1 -oE 'shstk|ibt' /proc/cpuinfo` 
        查看cpu是否支持特性

- 故障排除：
    - 各字段值设置是否准确
    - 实际长度是否超过最大预期长度，从而导致边界超出，使得后续字段偏移

ROP：
- 若使用 call 工具链，无需将 rip 压栈
- 若使用 jmp 工具链，需在跳转前将 rip 压栈

GOT：
- 设置内容：
    - 覆盖的目标 GOT，被之后命令执行
    - 覆盖后的跳转落脚点，劫持后的命令块
- 调整覆盖GOT与落脚点，以确保至少执行核心落脚点命令而不是在此之前自我调用的无限递归

## SROP

rt_sigreturn （系统调用号 15）内核会把当前用户栈当作“信号栈帧（ucontext/sigcontext）”去解析，然后一次性恢复一堆寄存器
- rax = 15
- 拥有 syscall
- RSP 指向受控内存地址

使用 pwntool 的 SigreturnFrame() 信号帧结构快速创建信号帧

落脚点设置：
- 若可一次性读取大量载荷，仅设置帧的 rip 到第1个 syscall，持续执行帧载荷
- 若空间高度受限，设置帧的 rip 到第2个 syscall，添加跳转到开头片段以实现 读取 >> 执行 的循环 
    - 第一个帧载荷设置 mmap 以创造伪栈空间，并设置 rsp 指针到伪栈向后一些的偏移（使用push将写入到分配空间外）
        

    - 在末尾添加跳转到开头片段，
        ```py
        # 开头片段
        read_loop:
            # read 调用
            xor edi, edi
            push rsp
            pop rsi
            xor eax, eax
            cdq
            mov dl, 0xf8
            syscall    

            # rt_sigreturn 调用    
            push 0xf
            pop rax
            syscall

            # 跳转到 read 开头循环读取与调用 
            jmp read_loop
        ```
- 读取信号帧载荷到栈
- 从栈中弹出信号帧设置寄存器
- 跳转到开头继续读取下一个帧载荷，持续循环
- 技巧：
    - 每轮 读取-执行 后，空间可覆盖，于是 rsp 可设置同一位置
    - 在 mmap 分配的空间中，可选择不会被帧载荷覆盖的另一段地址保存字符串或文件内容
    - 若拥有 mmap 空间的 x 权限，可在 read 载荷后设置 rip 执行 shellcode

## setcontext 
