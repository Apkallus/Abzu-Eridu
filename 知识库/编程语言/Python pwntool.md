### pwntools

<https://docs.pwntools.com/>

创建 tube 对象：
- 进程：`p = process(["/challenge/run"], stderr=STDOUT)`
    - `stdout=DEVNULL` 来自 `from subprocess import DEVNULL`
    - `stderr=文件对象` 分离标准错误写到文件中，pwntools 默认把 stderr 合并到 stdout
    - `close_fds=False` 默认关闭父进程的 fd 而无法继承到子进程，关闭后可传递 fd
        - 同时设置 `os.set_inheritable(fd, True)` 以开启 python 的 fd 继承
            ``` py
            log_fd = os.open("log.log", os.O_RDWR)
            os.set_inheritable(os.dup(log_fd), True)
            p = process(..., close_fds=False)
            ```
- 网络：`p = remote("127.0.0.1", 1337)`



设置timeout并满足时，将抛出异常。使用 `try ... except ...`

tube 对象函数：
- `send()`  
    发送原始字节（对应接收程序的 `read`）
    - `shutdown('send')`  
        发送 EOF 关闭 `send`

- `sendline()`
    发送一行数据，末尾添加换行符 `\n`（对应接收程序的 `scanf`）
- `sendlineafter(delim, data, timeout=default)→ str`  
    在获得 `delim` 提示后，发送 `data` 数据

- `send_signal(signal.SIGKILL)`
    发送信号，可搭配 `signal` 模块的常量

- `recv(numb=4096, timeout=default)→ bytes`：
    从管道中接收最多 numb 字节的数据，并在任何数量的数据可用时立即返回。  
    如果请求在超时秒数之前没有得到满足，所有数据将被缓冲，并返回一个空字符串（''）。

- `recvn(n)`：
    确保读满 n 字节（不够会等）
- `recvline(drop=False, timeout=default, keepends=True)→ bytes`  
    从管道中接收一行数据。  
    “一行”是指以 `newline` 中设置的字节序列终止的任意字节序列，默认值为 `b'\n'` 。
    - `keepends` 数据是否包括末尾的换行符
- `recvall(timeout=Timeout.forever)`
    尽量把对端输出读到 EOF（进程结束/管道关闭）为止，即如果希望后续继续发送数据可能导致EOF报错
- `recvuntil(delims, drop=False, timeout=default)→ bytes`
    接收数据直到遇到其中一个分隔符，分隔符将被消耗。
    如果在超时秒数内未满足请求，则所有数据将被缓冲，并返回一个空字符串 `''`。
    可与`recvline`组合，在收到提示数据后再读取。
- `recvrepeat(timeout=default)→ bytes`
    接收数据，直到超时或文件结束符（EOF）被达到。

- `p.close()`
    关闭当前线程
- `p.wait_for_close()`
    等待直到进程结束
- `p.poll()`    
    返回进程的退出状态，如果进程仍在运行则返回 None。(搭配 `p.wait_for_close()`)
- `can_recv()`
    测是否可读，可用于网络连接
- `p.clean(timeout=0.05)`
    把已有输出都读掉
- `cyclic(N)`
    循环字符串（如，baacaadaa），相对重复字符串还可显示对应位置：
    - `cyclic_find("caa")`
        定位特定循环模式的偏移
    - 流程：
        - `cyclic` 构建一个足够大而可覆盖返回地址的循环载荷
        - 发送此载荷，并在 `gdb` 查看崩溃时的 `rsp` 循环值
        - 复制此 `rsp` 循环值并使用 `cyclic_find` 得到从输入 buf 到返回地址的长度

- `p64(N)` `p8()`
    将int包装为小端序的64位bytes
- `u64()`
    将64位bytes以小端序解包为int

- `p.interactive()`  
    进入交互模式，python程序到此中断，而不是执行后退出，从而可进入/继续在 gdb 中。且持续从 socket/process 读取已到达的数据并打印到屏幕，同时把键盘输入转发给程序。
- `p.pid`
    得到当前进程的 pid，协同 gdb attach

示例：
```py
# 初始模板
from pwn import *
import signal

# 恢复 py 脚本中 SIGPIPE 的默认行为，从而可被 head 截断
# 若尝试 try except 异常，从而持续运行，则需注释掉
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

# 设置架构
context.arch = "amd64"

# 设置 tmux 调试
context.terminal = ["tmux", "splitw", "-h"]

# 日志的详细输出使用 debug，仅错误使用 error
context.log_level = "debug"

# 文件路径
file_path_str = "/challenge/toddlerone-level-11-1"

# 网络客户端
def get_net_client_process():
    p = remote("127.0.0.1", 1337)
    return p

# debug 模式与普通模式
def get_debug_or_process(debug=False):
    if debug:
        p = gdb.debug(file_path_str, """
            display/6i $rip
            display/4gx $rsp
            display/6gx $rbp-0x30
            display/6gx $rbp
            b* $_base()+0x3310
            continue
        """, setuid=False, aslr=True)
    else:
        ## 将 stderr 导出到文件
        # err_log = open('/home/hacker/err.log', 'wb')
        # p = process([file_path_str], stderr=err_log)
        p = process([file_path_str])
        
    return p

p = get_debug_or_process('')
p.recvuntil(b'Please input: ')
```

```py
# 从命令行传入多种格式的汇编代码，进行反汇编
from pwn import *
import sys

context.arch = "amd64"

argv_num = len(sys.argv)
print("input such: '4d 89 f0' or 4d89f0 or 4d 89 f0 or 0x4d 0x89 0xf0 or '\\x4d \\x89 \\xf0'")
print("list:", sys.argv)

if argv_num > 1:
    asm_bytes = bytes.fromhex(''.join(sys.argv[1:]).replace('0x', '').replace('\\x', ''))
else:
    asm_bytes = b'\x4d\x89\xf0'
    print('test bytes', asm_bytes)

disasm_bytes = disasm(asm_bytes)

print(disasm_bytes)
```

其他：
- `context.log_level = "debug"` 显示收发的字节，虽然此时不必将接收字节打印，但没有接收的部分不会被显示
- `from pwn import xor` 处理python原生不支持的bytes之间异或
- `pwnlib.context` — 设置运行时变量
    - `context.arch = 'amd64'`
        设置架构为 64 位 Intel
- `asm()` 将表示汇编的指令字符串转为实际汇编字节
    - `;` 语句分隔
    - `//` 注释
- `disasm()` 反汇编
- `gdb` 
    或需先运行 `tmux`
    - `gdb.debug(文件路径, gdb脚本, setuid=False, aslr=False)` 使用gdb调试程序
    - `gdb.debug_assembly()` 使用gdb调试汇编
    - `gdb.attach()` 
        ```py
        gdb.attach(p, gdbscript="""
        set disassembly-flavor intel
        display/3i $rip
        display/3i $rsp
        b *main+0
        c
        """)
        ```
- `SigreturnFrame()` 构建信号帧
    例：
    ```py
    frame = SigreturnFrame()
    frame.rax = 0
    frame.rip = 0x0000
    ```
- `unhex()` 将十六进制字符串转为原始字节
- `shellcraft.cat("/flag")`: 
    生成汇编代码（仅为汇编代码，仍需使用 `asm()` 转为机器指令字节）
- `ELF('/challenge/run')` 创建文件的 ELF 对象
    - `elf.got[目标函数]` 得到 got 全局偏移表字段 
    - `elf.plt['open']` 得到 plt 调用入口字段 
    - `elf.bss(0x30)` 得到数据段 bss 的地址，并预留 0x30 字节的偏移
    - `elf.symbols['main']` 得到符号 main 的地址
    - `elf.address` 可设置基地址，得到地址泄露计算并设置基地址，之后可直接使用其字段地址（此基地址 + rop 查找工具定位的目标偏移地址）
        - 泄露的绝对地址 - 此绝对地址对应的相对文件偏移 = elf 文件的绝对地址。  
            示例：
            - 使用泄露的 main 地址设置 elf 基地址       
                `elf.address = leak_main_addr - elf.symbols['main']` 
            - 使用泄露的 main 地址设置 elf 基地址   

                ```py
                # 使用 ldd 查看共享库文件路径
                lib_elf = ELF("/lib/x86_64-linux-gnu/libc.so.6")
                # 计算 libc 基址        
                lib_elf.address = leak_puts_addr - lib_elf.symbols['puts']            

                lib_chmod = lib_elf.symbols['chmod']
                ``` 
                - puts 函数设置 rdi 为地址即可泄露信息
                - environ 保存指向栈的环境变量字符串指针，泄露 lib 地址后即可得到栈地址
    
    - 根据字段值搜索对应地址 `elf.search(字段值)` 返回**生成器**

        ```py
        it = elf.search(b"puts\x00")   # 生成器
        addr = next(it)               # 取第一个匹配到的地址（int）
        ```
- 可能需开启地址随机以避免地址不对齐的崩溃
- `ROP([ELF1, ELF2...], badchars=b'\x09\x0a\x0b\x0c\x0d\x0e\x20')` 使用设置地址后的 ELF 对象构建 ROP 对象，排除设置的字符（在使用 printf/scanf 等字符串型输入输出时）
    - `rop.find_gadget(['pop rdi', 'ret']).address` 搜索工具并得到其地址
        - 使用其他 rop 查找工具确认位置存在后再使用 pwntool 的 ROP 对象获取地址而不是手动设置
        - 注意：部分存在的工具无法使用 ROP 定位
    - `rop.raw(data)` 将任意数据（整数、字符串、地址）直接追加到当前ROP链的末尾。
    - `rop.chain()` 将内部构建好的所有ROP数据（通过raw、call等方法添加的）拼接成一个完整的字节流（bytes）
    - `rop.dump()` 查看当前 rop 的栈布局
