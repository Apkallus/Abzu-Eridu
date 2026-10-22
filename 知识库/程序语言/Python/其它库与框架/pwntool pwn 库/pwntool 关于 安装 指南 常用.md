# pwntools

<https://docs.pwntools.com/>

## 待归档

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



设置timeout并满足时，将抛出异常。使用 `try ... except ...`

tube 对象函数：
- `send()`  
    发送原始字节（对应接收程序的 `read`）
    - `shutdown('send')`  
        发送 EOF 关闭 `send`

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

## 关于 pwntools

无论你是用它编写漏洞利用，还是把它作为另一个软件项目的一部分，使用方式都会有所不同。

历史上，pwntools 被用作一种编写漏洞利用的 DSL。在之前版本的 pwntools 中，只需执行 `from pwn import *` 就会带来各种便利的副作用。

在为 2.0 重新设计 pwntools 时，我们注意到两个相反的目标：

- 我们希望拥有“正常”的 Python 模块结构，让其他人能快速熟悉 pwntools。
- 我们希望有更多副作用，尤其是将终端置于 raw 模式。

为了实现这一点，我们决定设置两个不同的模块。[`pwnlib`] 将是我们干净漂亮的 Python 模块，而 [`pwn`] 将在 CTF 期间使用。

### [`pwn`] — 为 CTF 优化的工具箱

如前所述，我们还希望默认获得大量这些副作用。这就是此模块的目的。它执行以下操作：

- 从顶层 [`pwnlib`] 以及许多子模块中的函数导入所有内容。这意味着如果你执行 `import pwn` 或 `from pwn import *`，你将可以访问编写漏洞利用所需的一切。
- 调用 [`pwnlib.term.init()`] 将终端置于 raw 模式，并实现使其看起来不像 raw 模式的功能。
- 将 `pwnlib.context.log_level` 设置为 `"info"`。
- 尝试解析 [`sys.argv`](https://docs.python.org/3/library/sys.html#sys.argv) 中的一些值，并且每成功解析一个值就将其移除。

### [`pwnlib`] — 普通 Python 库

此模块是我们“干净”的 Python 代码。原则上，我们认为导入 [`pwnlib`] 或其任何子模块都不应产生任何显著副作用（例如缓存除外）。

大多数情况下，你也只会获得你导入的部分。例如，仅通过执行 `import pwnlib.util`，你不会获得 [`pwnlib.util.packing`] 的访问权限。

尽管有一些例外（例如 [`pwnlib.shellcraft`]），它们不太符合简单干净的目标，但仍然可以在没有隐式副作用的情况下导入。


## 安装

Pwntools 在 64 位 Ubuntu LTS 发行版（22.04 和 24.04）上获得最佳支持。大多数功能应能在任何类 POSIX 发行版（Debian、Arch、FreeBSD、OSX 等）上工作。

### 先决条件

为了充分利用 `pwntools`，你应安装以下系统库。

- [Binutils]  
  - [Ubuntu]
  - [Mac OS X]
  - [Windows]
  - [Alternate OSes]

- [Python Development Headers]  
  - [Ubuntu]
  - [Mac OS X]

注意：在 Mac OS X 上，你需要安装 `cmake`（`brew install cmake`）和 `pkg-config`（`brew install pkg-config`）。

```sh
brew install pwntools
```

### 发布版本

pwntools 作为 Python3 的 `pip` 包提供。v5.0.0 版本支持 Python3.10 或更高版本。如果你使用更早版本的 Python，请使用 v4。

#### Python3

安装 Pwntools 所需的 Python 版本会在尽力而为的基础上尽可能保持低版本。不过，新功能面向 Python3.10 及更高版本。

```console
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade pwntools
```

#### Python2（已弃用）

Pwntools v5.0.0 已移除对 Python2 的支持。最后一个支持 Python2 的版本是 v4.15.0。

注意：Pwntools 维护者**强烈建议**在所有未来的 Pwntools 脚本和项目中使用 Python3。

此外，由于 `pip` 放弃了对 Python2 的支持，必须安装特定版本的 `pip`。

```console
$ sudo apt-get update
$ sudo apt-get install python python-pip python-dev git libssl-dev libffi-dev build-essential
$ python2 -m pip install --upgrade pip==20.3.4
$ python2 -m pip install --upgrade pwntools
```

### 命令行工具

使用 `sudo` 安装时，上述命令会将 Pwntools 的命令行工具安装到类似 `/usr/bin` 的位置。

不过，如果你以非特权用户运行，可能会看到类似下面的警告消息：

```text
WARNING: The scripts asm, checksec, common, constgrep, cyclic, debug, disablenx, disasm,
elfdiff, elfpatch, errno, hex, main, phd, pwn, pwnstrip, scramble, shellcraft, template,
unhex, update and version are installed in '/home/user/.local/bin' which is not on PATH.
```

按照列出的说明操作，并将 `~/.local/bin` 添加到 `$PATH` 环境变量中。

### 开发

如果你在本地开发 Pwntools，你大概会想做类似这样的事情：

```console
$ git clone https://github.com/Gallopsled/pwntools
$ pip install --upgrade --editable ./pwntools
```

## 入门

为了让你初步体验 pwntools，我们先看几个示例。

编写漏洞利用时，pwntools 通常遵循“厨房水槽”式（大杂烩）方法。

```py
>>> from pwn import *
```

这会将大量功能导入全局命名空间。现在你可以用单个函数进行汇编、反汇编、打包、解包以及许多其他操作。

所有被导入内容的完整列表可在 [`from pwn import *`] 中找到。

### 教程

Pwntools 的一系列在线教程位于 [https://github.com/Gallopsled/pwntools-tutorial#readme](https://github.com/Gallopsled/pwntools-tutorial#readme)。

### 建立连接

你需要与挑战二进制程序通信才能 pwn 它，对吧？pwntools 通过其 [`pwnlib.tubes`] 模块让这件事简单得不可思议。

它提供了一个标准接口，用于与进程、套接字、串口以及各种对象通信，并附带一些用于常见任务的精巧辅助工具。例如，通过 [`pwnlib.tubes.remote`] 进行远程连接。

```py
>>> conn = remote('ftp.ubuntu.com',21)
>>> conn.recvline()
b'220 ...'
>>> conn.send(b'USER anonymous\r\n')
>>> conn.recvuntil(b' ', drop=True)
b'331'
>>> conn.recvline()
b'Please specify the password.\r\n'
>>> conn.close()
```

启动监听器也很容易：

```py
>>> l = listen()
>>> r = remote('localhost', l.lport)
>>> c = l.wait_for_connection()
>>> r.send(b'hello')
>>> c.recv()
b'hello'
```

借助 [`pwnlib.tubes.process`]，与进程交互很容易。

```py
>>> sh = process('/bin/sh')
>>> sh.sendline(b'sleep 3; echo hello world;')
>>> sh.recvline(timeout=1)
b''
>>> sh.recvline(timeout=5)
b'hello world\n'
>>> sh.close()
```

你不仅能以编程方式与进程交互，还能真正**交互**。

```py
>>> sh.interactive()
$ whoami
user
```

甚至还有 SSH 模块，用于当你需要通过 SSH 登录到某台机器以执行本地/setuid 漏洞利用时，使用 [`pwnlib.tubes.ssh`]。你可以快速生成进程并获取输出，或生成一个进程并像 `process` tube 一样与其交互。

```py
>>> shell = ssh('bandit0', 'bandit.labs.overthewire.org', password='bandit0', port=2220)
>>> shell['whoami']
b'bandit0'
>>> shell.download_file('/etc/motd')
>>> sh = shell.run('sh')
>>> sh.sendline(b'sleep 3; echo hello world;')
>>> sh.recvline(timeout=1)
b''
>>> sh.recvline(timeout=5)
b'hello world\n'
>>> shell.close()
```

### 打包整数

编写漏洞利用时的一项常见任务，是在 Python 所看到的整数与其字节序列表示之间进行转换。通常人们会求助于内置的 `struct` 模块。

pwntools 通过 [`pwnlib.util.packing`] 让这更容易。不必再记住解包代码，也不必在代码中到处塞辅助例程。

```py
>>> import struct
>>> p32(0xdeadbeef) == struct.pack('I', 0xdeadbeef)
True
>>> leet = unhex('37130000')
>>> u32(b'abcd') == struct.unpack('I', b'abcd')[0]
True
```

打包/解包操作已针对许多常见位宽定义。

```py
>>> u8(b'A') == 0x41
True
```

### 设置目标架构和操作系统

目标架构通常可以作为参数传给需要它的例程。

```py
>>> asm('nop')
b'\x90'
>>> asm('nop', arch='arm')
b'\x00\xf0 \xe3'
```

不过，也可以在全局 `context` 中一次性设置。操作系统、字长和字节序也可以在这里设置。

```py
>>> context.arch      = 'i386'
>>> context.os        = 'linux'
>>> context.endian    = 'little'
>>> context.word_size = 32
```

此外，你可以使用简写一次性设置所有值。

```py
>>> asm('nop')
b'\x90'
>>> context(arch='arm', os='linux', endian='big', word_size=32)
>>> asm('nop')
b'\xe3 \xf0\x00'
```

### 设置日志详细程度

你可以通过 `context` 控制标准 pwntools 日志的详细程度。

例如，设置

```py
>>> context.log_level = 'debug'
```

将导致 `tube` 发送和接收的所有数据都打印到屏幕上。

### 汇编与反汇编

你再也不需要运行从互联网上找到的某个已经汇编好的 shellcode 堆了！[`pwnlib.asm`] 模块充满了很棒的东西。

```py
>>> enhex(asm('mov eax, 0'))
'b800000000'
```

但如果你确实这么做了，也很容易弄明白！

```py
>>> print(disasm(unhex('6a0258cd80ebf9')))
   0:   6a 02                   push   0x2
   2:   58                      pop    eax
   3:   cd 80                   int    0x80
   5:   eb f9                   jmp    0x0
```

不过，大多数时候你甚至不需要编写自己的 shellcode！pwntools 附带 [`pwnlib.shellcraft`] 模块，其中装满了有用的、节省时间的 shellcode。

假设我们想要 `setreuid(getuid(), getuid())`，然后将文件描述符 4 `dup` 到 `stdin`、`stdout` 和 `stderr`，然后弹出一个 shell！

```py
>>> enhex(asm(shellcraft.setreuid() + shellcraft.dupsh(4)))
'6a3158cd80...'
```

### 杂项工具

多亏了 [`pwnlib.util.fiddling`]，你再也不用写 hexdump 了。

多亏了 `pwnlib.cyclic`，可以找到缓冲区中导致崩溃的偏移。

```py
>>> cyclic(20)
b'aaaabaaacaaadaaaeaaa'
>>> # 假设崩溃时 EIP = 0x62616166（b'faab'，即 pack(0x62616166)）
>>> cyclic_find(b'faab')
120
```

### ELF 操作

不要再硬编码了！使用 [`pwnlib.elf`] 在运行时查找它们。

```py
>>> e = ELF('/bin/cat')
>>> print(hex(e.address))
0x400000
>>> print(hex(e.symbols['write']))
0x401680
>>> print(hex(e.got['write']))
0x60b070
>>> print(hex(e.plt['write']))
0x401680
```

你甚至可以修补并保存文件。

```py
>>> e = ELF('/bin/cat')
>>> e.read(e.address, 4)
b'\x7fELF'
>>> e.asm(e.address, 'ret')
>>> e.save('/tmp/quiet-cat')
>>> disasm(open('/tmp/quiet-cat','rb').read(1))
'   0:   c3                      ret'
```

## `from pwn import *`

你会看到 pwntools 最常见的用法是：

```py
>>> from pwn import *
```

这会将海量内容导入全局命名空间，让你的生活更轻松。

下面是大多数被导入对象和例程的快速清单，大致按重要性和使用频率排序。

- `pwnlib.context`
  
  - [pwnlib.context.context]
  - 负责大多数 pwntools 便利设置
  - 排查漏洞利用问题时，设置 `context.log_level = 'debug'`
  - 作用域感知，因此你可以通过 [ContextType.local()] 为代码的某个子部分禁用日志

- `remote`、`listen`、`ssh`、`process`
  
  - [pwnlib.tubes]
  - 围绕 CTF 挑战常见功能的超级便利包装器
  - 连接到任何地方、任何对象，并按你期望的方式工作
  - 用于常见任务的辅助工具，例如 `recvline`、`recvuntil`、`clean` 等
  - 通过 `.interactive()` 直接与应用交互

- `p32` 和 `u32`
  
  - [pwnlib.util.packing]
  - 有用的函数，让你再也不必记住 `struct.pack` 中的 `'>'` 表示有符号还是无符号，也不必在末尾加上难看的 `[0]` 索引
  - 以合理的方式设置 `signed` 和 `endian`（这些也可以一次性在 `context` 上设置，之后无需再管）
  - 最常见的大小已预定义（`u8`、`u64` 等），而 [pwnlib.util.packing.pack()] 允许你定义自己的大小

- `log`
  
  - [pwnlib.log]
  - 让你的输出更漂亮！

- `cyclic` 和 `cyclic_func`
  
  - [pwnlib.util.cyclic]
  - 用于生成字符串的实用工具，使你仅凭 N（通常为 4）个字节就能找到任意给定子串的偏移。这对直接的缓冲区溢出非常有用。不必再盯着 `0x41414141`，你可以知道 `0x61616171` 意味着你在缓冲区偏移 64 处控制了 EIP。

- `asm` 和 `disasm`
  
  - [pwnlib.asm]
  - 快速将汇编转换为字节，或反之，无需折腾
  - 支持你安装了 binutils 的任何架构
  - 超过 20 种不同架构在 [ppa:pwntools/binutils](https://launchpad.net/~pwntools/+archive/ubuntu/binutils) 提供了预构建二进制文件

- `shellcraft`
  
  - [pwnlib.shellcraft]
  - 开箱即用的 shellcode 库
  - `asm(shellcraft.sh())` 会给你一个 shell
  - 用于 shellcode 片段复用的模板库

- `ELF`
  
  - [pwnlib.elf]
  - ELF 二进制操作工具，包括符号查找、虚拟内存到文件偏移的辅助工具，以及修改二进制文件并保存回磁盘的能力

- `DynELF`
  
  - [pwnlib.dynelf]
  - 仅给定任意已加载模块的指针，以及一个能在任意地址泄露数据的函数，就能动态解析函数

- `ROP`
  
  - `pwnlib.rop`
  - 使用 DSL 描述你想做什么来自动生成 ROP 链，而不是使用原始地址

- `gdb.debug` 和 `gdb.attach`
  
  - [pwnlib.gdb]
  - 在 GDB 下启动二进制文件，并弹出一个新终端与之交互。自动设置断点，让漏洞利用的迭代快得多。
  - 或者，根据 PID、[pwnlib.tubes] 对象，甚至仅根据连接到它的套接字，附加到正在运行的进程

- `args`
  
  - 包含全大写命令行参数的字典，便于快速访问
  - 通过 `python foo.py REMOTE=1` 运行，且 `args['REMOTE'] == '1'`。
  - 还可以控制日志详细程度和终端花哨程度
    
    - `NOTERM`
    - `SILENT`
    - `DEBUG`

- `randoms`、`rol`、`ror`、`xor`、`bits`
  
  - [pwnlib.util.fiddling]
  - 有用的实用工具，用于从给定字母表生成随机数据，或简化通常需要用 `0xffffffff` 掩码，或难看地多次调用 `ord` 和 `chr` 的数学运算

- `net`
  
  - [pwnlib.util.net]
  - 用于查询网络接口的例程

- `proc`
  
  - [pwnlib.util.proc]
  - 用于查询进程的例程

- `pause`
  
  - 它是新的 `getch`

- `safeeval`
  
  - [pwnlib.util.safeeval]
  - 用于安全求值 Python 代码且不产生恶劣副作用的函数。

这些都不言自明，但放在全局命名空间中很有用。

- `hexdump`
- `read` 和 `write`
- `enhex` 和 `unhex`
- `more`
- `group`
- `align` 和 `align_down`
- `urlencode` 和 `urldecode`
- `which`
- `wget`

此外，以下所有模块都会为你自动导入。反正你本来也会这么做。

- `os`
- `sys`
- `time`
- `requests`
- `re`
- `random`