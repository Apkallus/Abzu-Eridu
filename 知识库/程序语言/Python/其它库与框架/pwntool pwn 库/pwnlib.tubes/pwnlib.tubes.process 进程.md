https://docs.pwntools.com/en/latest/tubes/processes.html

# `pwnlib.tubes.process` — 进程

## `class pwnlib.tubes.process.process()`

```py
class pwnlib.tubes.process.process(argv=None, shell=False, executable=None, cwd=None, env=None, ignore_environ=None, stdin=-1, stdout=<pwnlib.tubes.process.PTY_ object>, stderr=-2, close_fds=True, preexec_fn=<function process.<lambda>>, preexec_args=(), raw=True, aslr=None, setuid=None, where='local', display=None, alarm=None, creationflags=0, *args, **kwargs)
```

基类：[tube]

生成一个新进程，并用 [tube] 对其进行包装，以便通信。

参数：

- `argv`（`list`）  
    要传递给所生成进程的参数列表。

- `shell`（`bool`）  
    设置为 `True` 时，将 `argv` 解释为字符串并传给 shell 解释，而不是作为 `argv`。

- `executable`（`str`）  
    要执行的二进制文件路径。如果为 `None`，则使用 `argv[0]`。不能与 `shell` 一起使用。

- `cwd`（`str`）  
    工作目录。默认使用当前工作目录。

- `env`（`dict`）  
    要添加到环境中的环境变量。

- `ignore_environ`（`bool`）  
    忽略 Python 的环境。默认情况下，当且仅当未指定 `env` 时使用 Python 的环境。

- `stdin`（`int`）  
    用于 `stdin` 的文件对象或文件描述符编号。默认使用管道。也可以通过将其设置为 `PTY` 来改用 pty。这会使程序以交互方式运行（例如，`python` 会显示 `>>>` 提示符）。如果应用程序直接读取 `/dev/tty`，请使用 pty。

- `stdout`（`int`）  
    用于 `stdout` 的文件对象或文件描述符编号。默认使用 pty，以禁用 libc 例程对 stdout 的任何缓冲。也可以设置为 `PIPE` 以使用普通管道。

- `stderr`（`int`）  
    用于 `stderr` 的文件对象或文件描述符编号。默认使用 `STDOUT`。也可以设置为 `PIPE` 以使用单独的管道，不过 [pwnlib.tubes.tube.tube] 包装器将无法读取这些数据。

- `close_fds`（`bool`）  
    关闭除 `stdin`、`stdout`、`stderr` 之外的所有已打开文件描述符。默认使用 `True`。

- `preexec_fn`（`callable`）  
    在调用 `execve` 之前立即调用的可调用对象。

- `preexec_args`（`iterable`）  
    传递给 `preexec_fn` 的参数。

- `raw`（`bool`）  
    将创建的 pty 设置为 raw 模式（即禁用回显和控制字符）。默认是 `True`。如果没有创建 pty，则此项无效。

- `aslr`（`bool`）  
    如果设置为 `False`，则通过 `personality`（`setarch -R`）和 `setrlimit`（`ulimit -s unlimited`）禁用 ASLR。

    这会禁用目标进程的 ASLR。但是，如果执行了 `setuid` 二进制文件，`setarch` 的更改会丢失。

    默认值继承自 `context.aslr`。有关其他选项和信息，请参见下面的 `setuid`。

- `setuid`（`bool`）  
    用于控制目标二进制的 `setuid` 状态以及相应采取的操作。

    默认情况下，此值为 `None`，因此不会做出任何假设。

    如果为 `True`，则将目标二进制视为 `setuid`。当 `aslr=False` 时，这会修改用于禁用进程 ASLR 的机制。这在本地调试时很有用，尤其是当漏洞利用对象是 `setuid` 二进制文件时。

    如果为 `False`，则阻止 `setuid` 位对目标二进制生效。这仅在 Linux 内核 v3.5 或更高版本上受支持。

- `where`（`str`）  
    进程运行的位置，用于日志记录。

- `display`（`list`）  
    要显示的参数列表，而不是主可执行文件名。

- `alarm`（`int`）  
    为进程设置 SIGALRM 警报超时。

- `creationflags`（`int`）  
    仅限 Windows。要传递给 `CreateProcess` 的标志。

**示例**

```pycon
>>> p = process('python')
>>> p.sendline(b"print('Hello world')")
>>> p.sendline(b"print('Wow, such data')")
>>> b'' == p.recv(timeout=0.01)
True
>>> p.shutdown('send')
>>> p.proc.stdin.closed
True
>>> p.connected('send')
False
>>> p.recvline(drop=True)
b'Hello world'
>>> p.recvuntil(b',')
b'Wow,'
>>> p.recvregex(b'.*data')
b' such data'
>>> p.recv()[-1:] == b'\n'
True
>>> p.recv()
Traceback (most recent call last):
...
EOFError
```

```pycon
>>> p = process('cat')
>>> d = open('/dev/urandom', 'rb').read(4096)
>>> p.recv(timeout=0.1)
b''
>>> p.write(d)
>>> p.recvrepeat(0.1) == d
True
>>> p.recv(timeout=0.1)
b''
>>> p.shutdown('send')
>>> p.wait_for_close()
>>> p.poll()
0

>>> p = process('cat /dev/zero | head -c8', shell=True, stderr=open('/dev/null', 'w+b'))
>>> p.recv()
b'\x00\x00\x00\x00\x00\x00\x00\x00'

>>> p = process(['python','-c','import os; print(os.read(2,1024).decode())'],
...             preexec_fn = lambda: os.dup2(0,2))
>>> p.sendline(b'hello')
>>> p.recvline()
b'hello\n'

>>> stack_smashing = ['python','-c','open("/dev/tty","wb").write(b"stack smashing detected")']
>>> process(stack_smashing).recvall()
b'stack smashing detected'

>>> process(stack_smashing, stdout=PIPE).recvall()
b''

>>> getpass = ['python','-c','import getpass; print(getpass.getpass("XXX"))']
>>> p = process(getpass, stdin=PTY)
>>> p.recv()
b'XXX'
>>> p.sendline(b'hunter2')
>>> p.recvall()
b'\nhunter2\n'

>>> process('echo hello 1>&2', shell=True).recvall()
b'hello\n'

>>> process('echo hello 1>&2', shell=True, stderr=PIPE).recvall()
b''

>>> a = process(['cat', '/proc/self/maps']).recvall()
>>> b = process(['cat', '/proc/self/maps'], aslr=False).recvall()
>>> with context.local(aslr=False):
...    c = process(['cat', '/proc/self/maps']).recvall()
>>> a == b
False
>>> b == c
True

>>> process(['sh','-c','ulimit -s'], aslr=0).recvline()
b'unlimited\n'

>>> io = process(['sh','-c','sleep 10; exit 7'], alarm=2)
>>> io.poll(block=True) == -signal.SIGALRM
True

>>> binary = ELF.from_assembly('nop', arch='mips')
>>> p = process(binary.path)
>>> binary_dir, binary_name = os.path.split(binary.path)
>>> p = process('./{}'.format(binary_name), cwd=binary_dir)
>>> p = process(binary.path, cwd=binary_dir)
>>> p = process('./{}'.format(binary_name), cwd=os.path.relpath(binary_dir))
>>> p = process(binary.path, cwd=os.path.relpath(binary_dir))

>>> def write(s):
...   import os
...   os.write(1, s)
>>> print(process('false', preexec_fn=write, preexec_args=(b"Hello World!", )).recvline().strip().decode())
Hello World!
```

### `__getattr__()`

```py
__getattr__(attr)
```

允许对底层进程对象进行透传访问，例如 `pid` 和 `stdin` 等字段。

### `__init__()`

```py
__init__(argv=None, shell=False, executable=None, cwd=None, env=None, ignore_environ=None, stdin=-1, stdout=<pwnlib.tubes.process.PTY_ object>, stderr=-2, close_fds=True, preexec_fn=<function process.<lambda>>, preexec_args=(), raw=True, aslr=None, setuid=None, where='local', display=None, alarm=None, creationflags=0, *args, **kwargs)
```

### `__on_enoexec()`

```py
__on_enoexec(exception)
```

收到了“exec format”错误（ENOEXEC）。

这意味着用户尝试执行例如在非 ARM 系统上的 ARM 二进制文件，并且没有为 QEMU 安装 binfmt 辅助程序。

### `__preexec_fn()`

在调用 `execve()` 之前，在子进程中执行的例程。

处理设置控制 TTY 以及调用用户提供的 `preexec_fn`。

### `__pty_make_controlling_tty()`

```py
__pty_make_controlling_tty(tty_fd)
```

使伪终端成为控制 tty。这应该比 `pty.fork()` 函数更具可移植性。具体来说，这应该能在 Solaris 上工作。

### `_validate()`

```py
_validate(cwd, executable, argv, env)
```

对可执行文件路径、`argv` 和 `envp` 执行扩展验证。

主要是为了让 Python 满意，同时也为了防止常见陷阱。

### `address_mapping() → mapping`

```py
address_mapping(address) → mapping
```

返回指定地址处的映射。

示例：

```pycon
>>> p = process(['cat'])
>>> p.sendline(b'meow')
>>> p.recvline()
b'meow\n'
>>> libc = p.libc_mapping().address
>>> heap = p.heap_mapping().address
>>> elf = p.elf_mapping().address
>>> p.address_mapping(libc).path
'.../libc...'
>>> p.address_mapping(heap + 0x123).path
'[heap]'
>>> p.address_mapping(elf + 0x1234).path
'.../cat'
>>> p.address_mapping(elf - 0x1234) == None
True
```

### `can_recv_raw() → bool`

```py
can_recv_raw(timeout) → bool
```

不应直接调用。如果在超时时间内有可用数据，则返回 True，但会忽略对象上的缓冲区。

### `close()`

关闭 tube。

### `communicate() → str`

```py
communicate(stdin=None) → str
```

在进程上调用 `subprocess.Popen.communicate()` 方法。

### `connected_raw()`

```py
connected_raw(direction)
```

```py
connected(direction = 'any') -> bool
```

不应直接调用。当且仅当 tube 在给定方向上已连接时返回 True。

### `elf_mapping() → mapping`, `elf_mapping() → [mapping]`

```py
elf_mapping(single=True) → mapping
elf_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

返回以 [process.elf()] 路径和 `single` 为参数的 [process.get_mapping()]。

示例：

```pycon
>>> p = process(['cat'])
>>> p.sendline(b'meow')
>>> p.recvline()
b'meow\n'
>>> mapping = p.elf_mapping()
>>> mapping.path
'...cat...'
>>> mapping.perms.execute
False
>>> mapping.perms.write
False
>>> hex(mapping.address)
'0x55a2abba0000'
>>> mappings = p.elf_mapping(single=False)
>>> len(mappings) > 1
True
>>> hex(mappings[1].address)
'0x55a2abba2000'
>>> mappings[0].end == mappings[1].start
True
>>> mappings[1].perms.execute
True
```

### `fileno() → int`

返回用于读取的文件编号。

### `get_mapping() → mapping`, `get_mapping() → [mapping]`

```py
get_mapping(path_value, single=True) → mapping
get_mapping(path_value, False) → [mapping]
```

参数：

- `path_value`（`str`）  
    所请求映射的精确路径，有效值还包括 `[stack]`、`[heap]` 等。

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

根据 `path_value` 返回进程内存中找到的映射。

示例：

```pycon
>>> p = process(['cat'])
>>> mapping = p.get_mapping('[stack]')
>>> mapping.path == '[stack]'
True
>>> mapping.perms.execute
False
>>>
>>> mapping = p.get_mapping('does not exist')
>>> print(mapping)
None
>>>
>>> mappings = p.get_mapping(which('cat'), single=False)
>>> len(mappings) > 1
True
```

### `heap_mapping() → mapping`, `heap_mapping() → [mapping]`

```py
heap_mapping(single=True) → mapping
heap_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

返回以 `'[heap]'` 和 `single` 为参数的 [process.get_mapping()]。

示例：

```pycon
>>> p = process(['cat'])
>>> p.sendline(b'meow')
>>> p.recvline()
b'meow\n'
>>> mapping = p.heap_mapping()
>>> mapping.path
'[heap]'
>>> mapping.perms.execute
False
>>> mapping.perms.write
True
>>> hex(mapping.address)
'0x557650fae000'
>>> mappings = p.heap_mapping(single=False)
>>> len(mappings)
1
```

### `kill()`

杀死进程。

### `leak()`

```py
leak(address, count=1)
```

泄露进程内指定地址处的内存。

参数：

- `address`（`int`）  
    要泄露内存的地址。

- `count`（`int`）  
    在该地址处要泄露的字节数。

示例：

```pycon
>>> e = ELF(which('bash-static'))
>>> p = process(e.path)

为了确保不会与进程初始化发生竞态条件...

>>> p.sendline(b'echo hello')
>>> p.recvuntil(b'hello')
b'hello'

现在我们可以泄露一些数据了！

>>> p.leak(e.address, 4)
b'\x7fELF'
```

### `lib_size() → int`

```py
lib_size(path_value) → int
```

参数：

- `path_value`（`str`）  
    共享库的精确路径。

- `process`（由...加载）

返回共享库在进程内存中的大小。如果未找到该库，则返回零。

示例：

```pycon
>>> p = process(['cat'])
>>> p.send(b'meow')
>>> p.recvuntil(b'meow')
b'meow'
>>> libc_size = p.lib_size(p.libc.path)
>>> hex(libc_size)
'0x1d5000'
>>> libc_mappings = p.libc_mapping(single=False)
>>> libc_size == (libc_mappings[-1].end - libc_mappings[0].start)
True
```

### `libc_mapping() → mapping`, `libc_mapping() → [mapping]`

```py
libc_mapping(single=True) → mapping
libc_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

根据 `single` 返回进程内存中找到的第一个 libc 映射，或所有 libc 映射。

示例：

```pycon
>>> p = process(['cat'])
>>> p.sendline(b'meow')
>>> p.recvline()
b'meow\n'
>>> mapping = p.libc_mapping()
>>> mapping.path
'...libc...'
>>> mapping.perms.execute
False
>>> mapping.perms.write
False
>>> hex(mapping.address)
'0x7fbde7fd7000'
>>>
>>> mappings = p.libc_mapping(single=False)
>>> len(mappings) > 1
True
>>> hex(mappings[1].address)
'0x7fbde7ffd000'
>>> mappings[0].end == mappings[1].start
True
>>> mappings[1].perms.execute
True
```

### `libs() → dict`

返回一个字典，将进程加载的每个共享库路径映射到其在进程地址空间中的加载地址。

### `maps() → [mapping]`

返回进程映射列表。

`mapping` 对象具有以下字段：`addr`、`address`（`addr` 的别名）、`start`（`addr` 的别名）、`end`、`size`、`perms`、`path`、`rss`、`pss`、`shared_clean`、`shared_dirty`、`private_clean`、`private_dirty`、`referenced`、`anonymous`、`swap`。

`perms` 是权限对象，具有以下字段：`read`、`write`、`execute`、`private`、`shared`、`string`。

示例：

```pycon
>>> p = process(['cat'])
>>> p.sendline(b"meow")
>>> p.recvline()
b'meow\n'
>>> proc_maps = open("/proc/" + str(p.pid) + "/maps", "r").readlines()
>>> pwn_maps = p.maps()
>>> len(proc_maps) == len(pwn_maps)
True
>>> checker_arr = []
>>> for proc, pwn in zip(proc_maps, pwn_maps):
...     proc = proc.split(' ')
...     p_addrs = proc[0].split('-')
...     checker_arr.append(int(p_addrs[0], 16) == pwn.addr == pwn.address == pwn.start)
...     checker_arr.append(int(p_addrs[1], 16) == pwn.end)
...     checker_arr.append(pwn.size == pwn.end - pwn.start)
...     checker_arr.append(pwn.perms.string == proc[1])
...     proc_path = proc[-1].strip()
...     checker_arr.append(pwn.path == proc_path or (pwn.path == '[anon]' and proc_path == ''))
...
>>> checker_arr == [True] * len(proc_maps) * 5
True
```

有关此内容的实用信息可在 <https://man7.org/linux/man-pages/man5/proc.5.html> 中找到，特别是 `/proc/pid/maps` 部分。

`memory_maps()` 返回 `pmmap_ext` 对象列表。定义（来自 `psutil/_pslinux.py`）为：

```py
pmmap_grouped = namedtuple(
    'pmmap_grouped',
    ['path', 'rss', 'size', 'pss', 'shared_clean', 'shared_dirty',
    'private_clean', 'private_dirty', 'referenced', 'anonymous', 'swap'])
pmmap_ext = namedtuple(
    'pmmap_ext', 'addr perms ' + ' '.join(pmmap_grouped._fields))
```

以下是一个 `pmmap_ext` 条目的示例：

```log
pmmap_ext(addr='15555551c000-155555520000', perms='r--p', path='[vvar]', rss=0, size=16384, pss=0, shared_clean=0, shared_dirty=0, private_clean=0, private_dirty=0, referenced=0, anonymous=0, swap=0)
```

### `musl_mapping() → mapping`, `musl_mapping() → [mapping]`

```py
musl_mapping(single=True) → mapping
musl_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

根据 `single` 返回进程内存中找到的第一个 musl 映射，或所有 musl 映射。

### `poll() → int`

```py
poll(block=False) → int
```

参数：

- `block`（`bool`）  
    等待进程退出。

轮询进程的退出代码。如果进程尚未结束，则返回 None，否则返回退出代码。

### `readmem()`

```py
readmem(address, count=1)
```

泄露进程内指定地址处的内存。

参数：

- `address`（`int`）  
    要泄露内存的地址。

- `count`（`int`）  
    在该地址处要泄露的字节数。

示例：

```pycon
>>> e = ELF(which('bash-static'))
>>> p = process(e.path)

为了确保不会与进程初始化发生竞态条件...

>>> p.sendline(b'echo hello')
>>> p.recvuntil(b'hello')
b'hello'

现在我们可以泄露一些数据了！

>>> p.leak(e.address, 4)
b'\x7fELF'
```

### `recv_raw() → str`

```py
recv_raw(numb) → str
```

不应直接调用。接收数据时不使用对象上的缓冲区。

除非发生超时或连接关闭，否则应始终返回数据。在超时情况下应返回 None，在连接关闭情况下应引发 `exceptions.EOFError`。

### `send_raw()`

```py
send_raw(data)
```

不应直接调用。向 tube 发送数据。

如果由于 tube 已关闭而无法再发送，则应返回 `exceptions.EOFError`。

### `settimeout_raw()`

```py
settimeout_raw(timeout)
```

不应直接调用。设置 tube 的超时。

### `shutdown_raw()`

```py
shutdown_raw(direction)
```

不应直接调用。关闭 tube 以停止进一步读取或写入。

### `stack_mapping() → mapping`, `stack_mapping() → [mapping]`

```py
stack_mapping(single=True) → mapping
stack_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

返回以 `'[stack]'` 和 `single` 为参数的 [process.get_mapping()]。

示例：

```pycon
>>> p = process(['cat'])
>>> mapping = p.stack_mapping()
>>> mapping.path
'[stack]'
>>> mapping.perms.execute
False
>>> mapping.perms.write
True
>>> hex(mapping.address)
'0x7fffd99fe000'
>>> mappings = p.stack_mapping(single=False)
>>> len(mappings)
1
```

### `terminate()`

通过发送 SIGTERM 终止进程。

与发送 SIGKILL 的 [kill()] 相比，这是一种更优雅的停止进程的方式。进程在收到 SIGTERM 时有机会清理并优雅退出。

进程可以选择忽略此信号，因此真正的清理只在 [kill()]/[close()] 中完成。

注意：在 Windows 上没有 SIGTERM 信号，因此会改为调用 Win32 API 函数 `TerminateProcess()`，导致 [terminate()] 和 [kill()] 实际上相同。

示例：

```pycon
>>> p = process(['python', '-u', '-c', 'import signal;signal.signal(signal.SIGTERM, lambda signum,frame: (print("sigterm"),exit(0)));print("ready");import time;time.sleep(10)'])
>>> p.recvline_contains(b'ready')
b'ready'
>>> p.terminate()
>>> p.recvuntil(b'sigterm')
b'sigterm'
>>> p.close()
```

### `vdso_mapping() → mapping`, `vdso_mapping() → [mapping]`

```py
vdso_mapping(single=True) → mapping
vdso_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

返回以 `'[vdso]'` 和 `single` 为参数的 [process.get_mapping()]。

示例：

```pycon
>>> p = process(['cat'])
>>> mapping = p.vdso_mapping()
>>> mapping.path
'[vdso]'
>>> mapping.perms.execute
True
>>> mapping.perms.write
False
>>> hex(mapping.address)
'0x7ffcf13af000'
>>> mappings = p.vdso_mapping(single=False)
>>> len(mappings)
1
```

### `vvar_mapping() → mapping`, `vvar_mapping() → [mapping]`

```py
vvar_mapping(single=True) → mapping
vvar_mapping(False) → [mapping]
```

参数：

- `single`（`bool=True`）  
    是仅返回第一个匹配的映射，还是返回所有匹配的映射。

返回以 `'[vvar]'` 和 `single` 为参数的 [process.get_mapping()]。

示例：

```pycon
>>> p = process(['cat'])
>>> mapping = p.vvar_mapping()
>>> mapping.path
'[vvar]'
>>> mapping.perms.execute
False
>>> mapping.perms.write
False
>>> hex(mapping.address)
'0x7ffee5f60000'
>>> mappings = p.vvar_mapping(single=False)
>>> len(mappings)
1
```

### `writemem()`

```py
writemem(address, data)
```

在进程内指定地址处写入内存。

参数：

- `address`（`int`）  
    要写入内存的地址。

- `data`（`bytes`）  
    要写入该地址的数据。

**示例**

让我们将数据写入 ELF 映射内存的开头。

```pycon
>>> context.clear(arch='i386')
>>> address = 0x100000
>>> data = cyclic(32)
>>> assembly = shellcraft.nop() * len(data)

等待一个字节输入，然后将数据写入 stdout

>>> assembly += shellcraft.write(1, address, 1)
>>> assembly += shellcraft.read(0, 'esp', 1)
>>> assembly += shellcraft.write(1, address, 32)
>>> assembly += shellcraft.exit()
>>> asm(assembly)[32:]
b'j\x01[\xb9\xff\xff\xef\xff\xf7\xd1\x89\xdaj\x04X\xcd\x801\xdb\x89\xe1j\x01Zj\x03X\xcd\x80j\x01[\xb9\xff\xff\xef\xff\xf7\xd1j Zj\x04X\xcd\x801\xdbj\x01X\xcd\x80'

汇编该二进制文件并进行测试

>>> elf = ELF.from_assembly(assembly, vma=address)
>>> io = elf.process()
>>> _ = io.recvuntil(b'\x90')
>>> _ = io.writemem(address, data)
>>> io.send(b'X')
>>> io.recvall()
b'aaaabaaacaaadaaaeaaafaaagaaahaaa'
```

### `_setuid`

是否允许 `setuid`。

### `_stop_noticed = 0`

我们是否已看到进程停止？如果是，则这是一个 Unix 时间戳。

### `alarm`

进程的 `alarm` 超时。

### `argv`

通过 `argv` 传递的参数。

### `aslr`

是否保留 ASLR 开启。

### `property corefile`

返回进程的 corefile。

如果进程仍存活，则尝试使用 GDB 创建 coredump。

如果进程已死亡：如果启用了 `context.disable_corefiles`，则返回 None；否则尝试定位内核创建的 coredump。

### `property cwd`

进程工作所在的目录。

示例：

```pycon
>>> p = process('sh')
>>> p.sendline(b'cd /tmp; echo AAA')
>>> _ = p.recvuntil(b'AAA')
>>> p.cwd == '/tmp'
True
>>> p.sendline(b'cd /proc; echo BBB;')
>>> _ = p.recvuntil(b'BBB')
>>> p.cwd
'/proc'
```

### `property elf`

返回启动该进程的可执行文件的 ELF 文件。

### `env`

通过 `envp` 传递的环境变量。

### `executable`

可执行文件的完整路径。

### `property libc`

返回当前进程 libc 的 ELF。如果可能，会自动调整到正确地址。

示例：

```pycon
>>> p = process("/bin/cat")
>>> p.send(b"meow")
>>> p.recvuntil(b"meow")
b'meow'
>>> libc = p.libc
>>> libc is not None
True
>>> libc
ELF('/lib64/libc-...so')
>>> p.close()
```

### `proc = None`

支持此进程的 `subprocess.Popen` 对象。

### `property program`

`executable` 的别名，用于向后兼容。

示例：

```pycon
>>> p = process('/bin/true')
>>> p.executable == '/bin/true'
True
>>> p.executable == p.program
True
```

### `pty`

哪个文件描述符是控制 TTY。

### `raw`

控制 TTY 是否设置为 raw 模式。

### `property stderr`

`self.proc.stderr` 的简写。

参见：[process.proc]

### `property stdin`

`self.proc.stdin` 的简写。

参见：[process.proc]

### `property stdout`

`self.proc.stdout` 的简写。

参见：[process.proc]