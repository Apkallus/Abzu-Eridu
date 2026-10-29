https://docs.pwntools.com/en/latest/tubes.html

# `pwnlib.tubes` — 与世界对话！

pwnlib 不是大卡车！它是一系列管道！

这是用于与套接字、进程、SSH 连接等通信的库。我们的目标是能够对远程 TCP 服务器、本地 TTY 程序以及通过 SSH 运行的程序使用同一套 API。

其组织方式是：大部分功能都在 [pwnlib.tubes.tube] 中实现。其余类只应实现使该类正常工作所必需的功能，以及可能仅与该特定类型 tube 相关的代码。

## 管道的类型

- `[pwnlib.tubes.buffer]` — tubes 的 buffer 实现
  - `[Buffer]`
    - `[Buffer.__contains__()]`
    - `[Buffer.__init__()]`
    - `[Buffer.__len__()]`
    - `[Buffer.add()]`
    - `[Buffer.get()]`
    - `[Buffer.get_fill_size()]`
    - `[Buffer.index()]`
    - `[Buffer.unget()]`
    - `[Buffer.__weakref__]`
- `[pwnlib.tubes.process]` — 进程
  - `[process]`
    - `[process.__getattr__()]`
    - `[process.__init__()]`
    - `[process.__on_enoexec()]`
    - `[process.__preexec_fn()]`
    - `[process.__pty_make_controlling_tty()]`
    - `[process._validate()]`
    - `[process.address_mapping()]`
    - `[process.can_recv_raw()]`
    - `[process.close()]`
    - `[process.communicate()]`
    - `[process.connected_raw()]`
    - `[process.elf_mapping()]`
    - `[process.fileno()]`
    - `[process.get_mapping()]`
    - `[process.heap_mapping()]`
    - `[process.kill()]`
    - `[process.leak()]`
    - `[process.lib_size()]`
    - `[process.libc_mapping()]`
    - `[process.libs()]`
    - `[process.maps()]`
    - `[process.musl_mapping()]`
    - `[process.poll()]`
    - `[process.readmem()]`
    - `[process.recv_raw()]`
    - `[process.send_raw()]`
    - `[process.settimeout_raw()]`
    - `[process.shutdown_raw()]`
    - `[process.stack_mapping()]`
    - `[process.terminate()]`
    - `[process.vdso_mapping()]`
    - `[process.vvar_mapping()]`
    - `[process.writemem()]`
    - `[process._setuid]`
    - `[process._stop_noticed]`
    - `[process.alarm]`
    - `[process.argv]`
    - `[process.aslr]`
    - `[process.corefile]`
    - `[process.cwd]`
    - `[process.elf]`
    - `[process.env]`
    - `[process.executable]`
    - `[process.libc]`
    - `[process.proc]`
    - `[process.program]`
    - `[process.pty]`
    - `[process.raw]`
    - `[process.stderr]`
    - `[process.stdin]`
    - `[process.stdout]`
- `[pwnlib.tubes.serialtube]` — 串口
  - `[serialtube]`
    - `[serialtube.__init__()]`
    - `[serialtube.can_recv_raw()]`
    - `[serialtube.close()]`
    - `[serialtube.connected_raw()]`
    - `[serialtube.fileno()]`
    - `[serialtube.recv_raw()]`
    - `[serialtube.send_raw()]`
    - `[serialtube.settimeout_raw()]`
    - `[serialtube.shutdown_raw()]`
- `[pwnlib.tubes.sock]` — 套接字
  - `[sock]`
  - `[remote]`
    - `[remote.fromsocket()]`
    - `[remote.__init__()]`
  - `[listen]`
    - `[listen.__init__()]`
    - `[listen.close()]`
    - `[listen.spawn_process()]`
    - `[listen.wait_for_connection()]`
    - `[listen.canonname]`
    - `[listen.family]`
    - `[listen.lhost]`
    - `[listen.lport]`
    - `[listen.protocol]`
    - `[listen.sockaddr]`
    - `[listen.type]`
  - `[server]`
    - `[server.__init__()]`
    - `[server.close()]`
    - `[server.next_connection()]`
    - `[server.canonname]`
    - `[server.family]`
    - `[server.lhost]`
    - `[server.lport]`
    - `[server.protocol]`
    - `[server.sockaddr]`
    - `[server.type]`
- `[pwnlib.tubes.ssh]` — SSH
  - `[ssh]`
    - `[ssh._pathlib]`
    - `[ssh.__call__()]`
    - `[ssh.__getattr__()]`
    - `[ssh.__getitem__()]`
    - `[ssh.__init__()]`
    - `[ssh.__repr__()]`
    - `[ssh._init_remote_platform_info()]`
    - `[ssh._libs_remote()]`
    - `[ssh.checksec()]`
    - `[ssh.close()]`
    - `[ssh.connect_remote()]`
    - `[ssh.connected()]`
    - `[ssh.download()]`
    - `[ssh.download_data()]`
    - `[ssh.download_dir()]`
    - `[ssh.download_file()]`
    - `[ssh.get()]`
    - `[ssh.getenv()]`
    - `[ssh.interactive()]`
    - `[ssh.libs()]`
    - `[ssh.listen()]`
    - `[ssh.listen_remote()]`
    - `[ssh.process()]`
    - `[ssh.put()]`
    - `[ssh.read()]`
    - `[ssh.remote()]`
    - `[ssh.run()]`
    - `[ssh.run_to_end()]`
    - `[ssh.set_working_directory()]`
    - `[ssh.shell()]`
    - `[ssh.system()]`
    - `[ssh.unlink()]`
    - `[ssh.upload()]`
    - `[ssh.upload_data()]`
    - `[ssh.upload_dir()]`
    - `[ssh.upload_file()]`
    - `[ssh.which()]`
    - `[ssh.write()]`
    - `[ssh.arch]`
    - `[ssh.aslr]`
    - `[ssh.aslr_ulimit]`
    - `[ssh.bits]`
    - `[ssh.cache]`
    - `[ssh.client]`
    - `[ssh.distro]`
    - `[ssh.host]`
    - `[ssh.ibt]`
    - `[ssh.key]`
    - `[ssh.keyfile]`
    - `[ssh.os]`
    - `[ssh.password]`
    - `[ssh.pid]`
    - `[ssh.port]`
    - `[ssh.raw]`
    - `[ssh.sftp]`
    - `[ssh.user]`
    - `[ssh.user_shstk]`
    - `[ssh.version]`
  - `[ssh_channel]`
    - `[ssh_channel.interactive()]`
    - `[ssh_channel.kill()]`
    - `[ssh_channel.poll()]`
  - `[ssh_process]`
    - `[ssh_process.getenv()]`
    - `[ssh_process.libs()]`
    - `[ssh_process.argv]`
    - `[ssh_process.cwd]`
    - `[ssh_process.elf]`
    - `[ssh_process.executable]`
    - `[ssh_process.libc]`
    - `[ssh_process.pid]`
  - `[ssh_connecter]`
  - `[ssh_listener]`

## `pwnlib.tubes.tube` — 通用功能

## `class pwnlib.tubes.tube.tube`

包含套接字、TTY 和 SSH 连接所共有的所有 tube 函数。

### `__enter__()`

允许使用 `with` 控制作用域并关闭会话。

**示例**

```pycon
>>> t = tube()
>>> def p(x): print(x)
>>> t.close = lambda: p("Closed!")
>>> with t: pass
Closed!
```

### `__exit__()`

```py
__exit__(type, value, traceback)
```

处理 `with` 语句的关闭操作。

参见 [`__enter__()`]。

### `__init__()`

```py
__init__(timeout=pwnlib.timeout.Timeout.default, level=None, *a, **kw)
```

### `__lshift__()`

```py
__lshift__(other)
```

连接多个 tube 的简写。

更多信息参见 [`connect_input()`]。

**示例**

以下写法等价：

```py
tube_a >> tube_b
tube_a.connect_input(tube_b)
```

这在串联多个 tube 时很有用：

```py
tube_a >> tube_b >> tube_a
tube_a.connect_input(tube_b)
tube_b.connect_input(tube_a)
```

### `__ne__()`

```py
__ne__(other)
```

将 tube 相互连接的简写。

以下写法等价：

```py
a >> b >> a
a <> b
```

更多信息参见 [`connect_input()`]。

### `__rshift__()`

```py
__rshift__(other)
```

`<<` 运算符的反向操作。参见 [`__lshift__()`]。

更多信息参见 [`connect_input()`]。

### `_fillbuffer()`

```py
_fillbuffer(timeout=default)
```

通过恰好调用一次 `recv_raw()`，从管道填充内部缓冲区。

返回：

- 接收到的数据字节，如果未接收到数据则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda *a: b'abc'
>>> len(t.buffer)
0
>>> t._fillbuffer()
b'abc'
>>> len(t.buffer)
3
```

### `_normalize_keepends_drop()`

```py
_normalize_keepends_drop(keepends, drop, drop_default)
```

```pycon
>>> t = tube()
>>> t._normalize_keepends_drop(None, None, True)
True
>>> t._normalize_keepends_drop(None, None, False)
False
>>> t._normalize_keepends_drop(None, True, True)
True
>>> t._normalize_keepends_drop(None, True, False)
True
>>> t._normalize_keepends_drop(True, None, True)
False
>>> t._normalize_keepends_drop(True, None, False)
False
>>> t._normalize_keepends_drop(None, False, True)
False
>>> t._normalize_keepends_drop(None, False, False)
False
>>> t._normalize_keepends_drop(False, None, True)
True
>>> t._normalize_keepends_drop(False, None, False)
True
>>> t._normalize_keepends_drop(False, True, False)
Traceback (most recent call last):
    ...
pwnlib.exception.PwnlibException: 'drop' and 'keepends' arguments cannot be used together.
```

### `_read()`

```py
_read(*a, **kw)
```

[`_recv()`] 的别名。

### `_recv() → bytes`

```py
_recv(numb=4096, timeout=default) → bytes
```

从内部缓冲区或操作系统（如果缓冲区为空）接收一个数据块。

### `can_read()`

```py
can_read(*a, **kw)
```

[`can_recv()`] 的别名。

### `can_read_raw()`

```py
can_read_raw(*a, **kw)
```

`can_recv_raw()` 的别名。

### `can_recv() → bool`

```py
can_recv(timeout=0) → bool
```

如果在 `timeout` 秒内有可用数据，则返回 `True`。

**示例**

```pycon
>>> import time
>>> t = tube()
>>> t.can_recv_raw = lambda *a: False
>>> t.can_recv()
False
>>> _=t.unrecv(b'data')
>>> t.can_recv()
True
>>> _=t.recv()
>>> t.can_recv()
False
```

### `clean()`

```py
clean(timeout=0.05)
```

通过以较低超时反复调用 [`pwnlib.tubes.tube.tube.recv()`] 直到失败，移除 tube 中所有缓冲数据。

如果 `timeout` 为零，则只清除缓存数据。

注意：如果 timeout 设置为零，则不会实际轮询底层网络；只会清除内部缓冲区。

返回：

- 接收到的所有数据。

**示例**

```pycon
>>> t = tube()
>>> t.unrecv(b'clean me up')
>>> t.clean(0)
b'clean me up'
>>> len(t.buffer)
0
```

### `clean_and_log()`

```py
clean_and_log(timeout=0.05)
```

行为与 [`pwnlib.tubes.tube.tube.clean()`] 完全相同，但会通过 `pwnlib.self.info()` 记录接收到的数据。

返回：

- 接收到的所有数据。

**示例**

```pycon
>>> def recv(n, data=[b'', b'hooray_data']):
...     while data: return data.pop()
>>> t = tube()
>>> t.recv_raw      = recv
>>> t.connected_raw = lambda d: True
>>> t.fileno        = lambda: 1234
>>> with context.local(log_level='info'):
...     data = t.clean_and_log()
[...] Received 0xb bytes:
    b'hooray_data'
>>> data
b'hooray_data'
>>> context.clear()
```

### `close()`

关闭 tube。

### `connect_both()`

```py
connect_both(other)
```

将此 tube 对象的两端与另一个 tube 对象连接。

### `connect_input()`

```py
connect_input(other)
```

将此 tube 的输入连接到另一个 tube 对象的输出。

**示例**

```pycon
>>> def p(x): print(x.decode())
>>> def recvone(n, data=[b'data']):
...     while data: return data.pop()
...     raise EOFError
>>> a = tube()
>>> b = tube()
>>> a.recv_raw = recvone
>>> b.send_raw = p
>>> a.connected_raw = lambda d: True
>>> b.connected_raw = lambda d: True
>>> a.shutdown      = lambda d: True
>>> b.shutdown      = lambda d: True
>>> import time
>>> _=(b.connect_input(a), time.sleep(0.1))
data
```

### `connect_output()`

```py
connect_output(other)
```

将此 tube 的输出连接到另一个 tube 对象的输入。

**示例**

```pycon
>>> def p(x): print(repr(x))
>>> def recvone(n, data=[b'data']):
...     while data: return data.pop()
...     raise EOFError
>>> a = tube()
>>> b = tube()
>>> a.recv_raw = recvone
>>> b.send_raw = p
>>> a.connected_raw = lambda d: True
>>> b.connected_raw = lambda d: True
>>> a.shutdown      = lambda d: True
>>> b.shutdown      = lambda d: True
>>> _=(a.connect_output(b), time.sleep(0.1))
b'data'
```

### `connected() → bool`

```py
connected(direction='any') → bool
```

如果 tube 在指定方向上已连接，则返回 `True`。

参数：

- `direction`（`str`）  
    可以是字符串 `'any'`、`'in'`、`'read'`、`'recv'`、`'out'`、`'write'`、`'send'`。

Doctest：

```pycon
>>> def p(x): print(x)
>>> t = tube()
>>> t.connected_raw = p
>>> _=list(map(t.connected, ('any', 'in', 'read', 'recv', 'out', 'write', 'send')))
any
recv
recv
recv
send
send
send
>>> t.connected('bad_value')
Traceback (most recent call last):
...
KeyError: "direction must be in ['any', 'in', 'out', 'read', 'recv', 'send', 'write']"
```

### `fileno() → int`

返回用于读取的文件编号。

### `interactive()`

```py
interactive(prompt=pwnlib.term.text.bold_red('$') + ' ')
```

同时读写 tube。原则上，这只是将 tube 连接到标准输入和标准输出；但实际上这更可用，因为我们使用 `pwnlib.term` 打印浮动提示符。

因此，它只在 `pwnlib.term.term_mode` 中工作。

### `read()`

```py
read(*a, **kw)
```

[`recv()`] 的别名。

### `readS()`

```py
readS(*a, **kw)
```

[`recvS()`] 的别名。

### `read_raw()`

```py
read_raw(*a, **kw)
```

`recv_raw()` 的别名。

### `readall()`

```py
readall(*a, **kw)
```

[`recvall()`] 的别名。

### `readallS()`

```py
readallS(*a, **kw)
```

[`recvallS()`] 的别名。

### `readallb()`

```py
readallb(*a, **kw)
```

[`recvallb()`] 的别名。

### `readb()`

```py
readb(*a, **kw)
```

[`recvb()`] 的别名。

### `readline()`

```py
readline(*a, **kw)
```

[`recvline()`] 的别名。

### `readlineS()`

```py
readlineS(*a, **kw)
```

[`recvlineS()`] 的别名。

### `readline_contains()`

```py
readline_contains(*a, **kw)
```

[`recvline_contains()`] 的别名。

### `readline_containsS()`

```py
readline_containsS(*a, **kw)
```

[`recvline_containsS()`] 的别名。

### `readline_containsb()`

```py
readline_containsb(*a, **kw)
```

[`recvline_containsb()`] 的别名。

### `readline_endswith()`

```py
readline_endswith(*a, **kw)
```

[`recvline_endswith()`] 的别名。

### `readline_endswithS()`

```py
readline_endswithS(*a, **kw)
```

[`recvline_endswithS()`] 的别名。

### `readline_endswithb()`

```py
readline_endswithb(*a, **kw)
```

[`recvline_endswithb()`] 的别名。

### `readline_pred()`

```py
readline_pred(*a, **kw)
```

[`recvline_pred()`] 的别名。

### `readline_regex()`

```py
readline_regex(*a, **kw)
```

[`recvline_regex()`] 的别名。

### `readline_regexS()`

```py
readline_regexS(*a, **kw)
```

[`recvline_regexS()`] 的别名。

### `readline_regexb()`

```py
readline_regexb(*a, **kw)
```

[`recvline_regexb()`] 的别名。

### `readline_startswith()`

```py
readline_startswith(*a, **kw)
```

[`recvline_startswith()`] 的别名。

### `readline_startswithS()`

```py
readline_startswithS(*a, **kw)
```

[`recvline_startswithS()`] 的别名。

### `readline_startswithb()`

```py
readline_startswithb(*a, **kw)
```

[`recvline_startswithb()`] 的别名。

### `readlineb()`

```py
readlineb(*a, **kw)
```

[`recvlineb()`] 的别名。

### `readlines()`

```py
readlines(*a, **kw)
```

[`recvlines()`] 的别名。

### `readlinesS()`

```py
readlinesS(*a, **kw)
```

[`recvlinesS()`] 的别名。

### `readlinesb()`

```py
readlinesb(*a, **kw)
```

[`recvlinesb()`] 的别名。

### `readn()`

```py
readn(*a, **kw)
```

[`recvn()`] 的别名。

### `readnS()`

```py
readnS(*a, **kw)
```

[`recvnS()`] 的别名。

### `readnb()`

```py
readnb(*a, **kw)
```

[`recvnb()`] 的别名。

### `readpred()`

```py
readpred(*a, **kw)
```

[`recvpred()`] 的别名。

### `readpredS()`

```py
readpredS(*a, **kw)
```

[`recvpredS()`] 的别名。

### `readpredb()`

```py
readpredb(*a, **kw)
```

[`recvpredb()`] 的别名。

### `readregex()`

```py
readregex(*a, **kw)
```

[`recvregex()`] 的别名。

### `readregexS()`

```py
readregexS(*a, **kw)
```

[`recvregexS()`] 的别名。

### `readregexb()`

```py
readregexb(*a, **kw)
```

[`recvregexb()`] 的别名。

### `readrepeat()`

```py
readrepeat(*a, **kw)
```

[`recvrepeat()`] 的别名。

### `readrepeatS()`

```py
readrepeatS(*a, **kw)
```

[`recvrepeatS()`] 的别名。

### `readrepeatb()`

```py
readrepeatb(*a, **kw)
```

[`recvrepeatb()`] 的别名。

### `readuntil()`

```py
readuntil(*a, **kw)
```

[`recvuntil()`] 的别名。

### `readuntilS()`

```py
readuntilS(*a, **kw)
```

[`recvuntilS()`] 的别名。

### `readuntilb()`

```py
readuntilb(*a, **kw)
```

[`recvuntilb()`] 的别名。

### `recv() → bytes`

```py
recv(numb=4096, timeout=default) → bytes
```

从 tube 接收最多 `numb` 字节数据，并在有任何数量数据可用时立即返回。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

引发：

- `exceptions.EOFError` – 连接已关闭。

返回：

- 一个 bytes 对象，包含从套接字接收到的字节；如果在等待时发生超时，则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> # Fake a data source
>>> t.recv_raw = lambda n: b'Hello, world'
>>> t.recv() == b'Hello, world'
True
>>> t.unrecv(b'Woohoo')
>>> t.recv() == b'Woohoo'
True
>>> with context.local(log_level='debug'):
...    _ = t.recv()
[...] Received 0xc bytes:
    b'Hello, world'
```

### `recvS()`

```py
recvS(*a, **kw)
```

与 [`recv()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvall() → bytes`

```py
recvall(timeout=Timeout.forever) → bytes
```

接收数据直到 EOF，并关闭 tube。

### `recvallS()`

```py
recvallS(*a, **kw)
```

与 [`recvall()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvallb()`

```py
recvallb(*a, **kw)
```

与 [`recvall()`] 相同，但返回 `bytearray`。

### `recvb()`

```py
recvb(*a, **kw)
```

与 [`recv()`] 相同，但返回 `bytearray`。

### `recvline() → bytes`

```py
recvline(drop=False, timeout=default) → bytes
```

从 tube 接收单行。

“行”是由 [`newline`] 中设置的字节序列终止的任意字节序列，默认是 `b'\n'`。

如果在收到换行符之前连接关闭（`EOFError`），默认会返回已缓冲的数据，并记录一条警告。如果缓冲区为空，则引发 `EOFError`。可以通过设置 `pwnlib.context.ContextType.throw_eof_on_incomplete_line()` 改变此行为。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字节字符串（`b''`）。

参数：

- `drop`（`bool`）  
    丢弃行尾（`False`）。

- `timeout`（`int`）  
    超时时间。

引发：

- `EOFError` – 在请求可满足之前连接关闭，且缓冲区为空。

返回：

- 在收到第一个换行符 `'\n'` 之前通过 tube 接收到的所有字节。可选择保留结尾。如果在收到换行符之前连接关闭，则返回截至该点已接收的剩余数据。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'Foo\nBar\r\nBaz\n'
>>> t.recvline()
b'Foo\n'
>>> t.recvline()
b'Bar\r\n'
>>> t.recvline(False)
b'Baz'
>>> t.newline = b'\r\n'
>>> t.recvline(drop=True)
b'Foo\nBar'
>>> t = tube()
>>> def _recv_eof(n):
...     if not _recv_eof.throw:
...         _recv_eof.throw = True
...         return b'real line\ntrailing data'
...     raise EOFError
>>> _recv_eof.throw = False
>>> t.recv_raw = _recv_eof
>>> t.recvline()
b'real line\n'
>>> t.recvline()
b'trailing data'
>>> t.recvline()
Traceback (most recent call last):
    ...
EOFError
```

### `recvlineS()`

```py
recvlineS(*a, **kw)
```

与 [`recvline()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvline_contains() → bytes`

```py
recvline_contains(items, drop=True, timeout=default) → bytes
```

接收行，直到找到至少包含 `items` 中一项的行。

参数：

- `items`（`str`、`tuple`）  
    要搜索的字符串列表，或单个字符串。

- `drop`（`bool`）  
    丢弃行尾（`True`）。

- `timeout`（`int`）  
    超时时间，单位为秒。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b"Hello\nWorld\nXylophone\n"
>>> t.recvline_contains(b'r')
b'World'
>>> f = lambda n: b"cat dog bird\napple pear orange\nbicycle car train\n"
>>> t = tube()
>>> t.recv_raw = f
>>> t.recvline_contains(b'pear')
b'apple pear orange'
>>> t = tube()
>>> t.recv_raw = f
>>> t.recvline_contains((b'car', b'train'))
b'bicycle car train'
```

### `recvline_containsS()`

```py
recvline_containsS(*a, **kw)
```

与 [`recvline_contains()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvline_containsb()`

```py
recvline_containsb(*a, **kw)
```

与 [`recvline_contains()`] 相同，但返回 `bytearray`。

### `recvline_endswith() → bytes`

```py
recvline_endswith(delims, drop=True, timeout=default) → bytes
```

持续接收行，直到找到以 `delims` 中某一项结尾的行。返回最后接收到的行。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

更多细节参见 [`recvline_startswith()`]。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'Foo\nBar\nBaz\nKaboodle\n'
>>> t.recvline_endswith(b'r')
b'Bar'
>>> t.recvline_endswith((b'a',b'b',b'c',b'd',b'e'), drop=False)
b'Kaboodle\n'
>>> t.recvline_endswith(b'oodle')
b'Kaboodle'
```

### `recvline_endswithS()`

```py
recvline_endswithS(*a, **kw)
```

与 [`recvline_endswith()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvline_endswithb()`

```py
recvline_endswithb(*a, **kw)
```

与 [`recvline_endswith()`] 相同，但返回 `bytearray`。

### `recvline_pred() → bytes`

```py
recvline_pred(pred, drop=True, timeout=default) → bytes
```

接收数据，直到 `pred(line)` 返回真值。丢弃所有其他数据。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

参数：

- `pred`（`callable`）  
    要调用的函数。返回该函数返回 `True` 的行。

- `drop`（`bool`）  
    丢弃行尾（`True`）。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b"Foo\nBar\nBaz\n"
>>> t.recvline_pred(lambda line: line == b"Bar\n")
b'Bar'
>>> t.recvline_pred(lambda line: line == b"Bar\n", True)
b'Bar\n'
>>> t.recvline_pred(lambda line: line == b"Bar\n", drop=False)
b'Bar\n'
>>> t.recvline_pred(lambda line: line == b'Nope!', timeout=0.1)
b''
```

### `recvline_regex() → bytes`

```py
recvline_regex(regex, exact=False, drop=True, timeout=default) → bytes
```

[`recvline_pred()`] 的包装器，当正则表达式匹配某行时返回。

默认使用 `re.RegexObject.search()`；但如果 `exact` 设置为 `True`，则改用 `re.RegexObject.match()`。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

### `recvline_regexS()`

```py
recvline_regexS(*a, **kw)
```

与 [`recvline_regex()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvline_regexb()`

```py
recvline_regexb(*a, **kw)
```

与 [`recvline_regex()`] 相同，但返回 `bytearray`。

### `recvline_startswith() → bytes`

```py
recvline_startswith(delims, drop=True, timeout=default) → bytes
```

持续接收行，直到找到以 `delims` 中某一项开头的行。返回最后接收到的行。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

参数：

- `delims`（`str`、`tuple`）  
    要搜索的字符串列表，或单字符字符串。

- `drop`（`bool`）  
    丢弃行尾（`True`）。

- `timeout`（`int`）  
    超时时间，单位为秒。

返回：

- 接收到的第一行，其开头为 `delims` 中的某个分隔符。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b"Hello\nWorld\nXylophone\n"
>>> t.recvline_startswith((b'W',b'X',b'Y',b'Z'))
b'World'
>>> t.recvline_startswith((b'W',b'X',b'Y',b'Z'), drop=False)
b'Xylophone\n'
>>> t.recvline_startswith(b'Wo')
b'World'
```

### `recvline_startswithS()`

```py
recvline_startswithS(*a, **kw)
```

与 [`recvline_startswith()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvline_startswithb()`

```py
recvline_startswithb(*a, **kw)
```

与 [`recvline_startswith()`] 相同，但返回 `bytearray`。

### `recvlineb()`

```py
recvlineb(*a, **kw)
```

与 [`recvline()`] 相同，但返回 `bytearray`。

### `recvlines() → bytes 对象列表`

```py
recvlines(numlines, drop=True, timeout=default) → bytes 对象列表
```

接收最多 `numlines` 行。

“行”是由 [`newline`] 设置的字节序列终止的任意字节序列，默认是 `'\n'`。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

参数：

- `numlines`（`int`）  
    要接收的最大行数。

- `drop`（`bool`）  
    丢弃每行末尾的换行符（`True`）。

- `timeout`（`int`）  
    最大超时时间。

引发：

- `exceptions.EOFError` – 在请求可满足之前连接关闭。

返回：

- 一个字符串，包含从套接字接收到的字节；如果在等待时发生超时，则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'\n'
>>> t.recvlines(3)
[b'', b'', b'']
>>> t.recv_raw = lambda n: b'Foo\nBar\nBaz\n'
>>> t.recvlines(3)
[b'Foo', b'Bar', b'Baz']
>>> t.recvlines(3, True)
[b'Foo\n', b'Bar\n', b'Baz\n']
>>> t.recvlines(3, drop=False)
[b'Foo\n', b'Bar\n', b'Baz\n']
```

### `recvlinesS() → str 列表`

```py
recvlinesS(numlines, drop=True, timeout=default) → str 列表
```

此函数与 [`recvlines()`] 相同，但使用 `context.encoding()` 将接收到的字节解码为字符串。为了更好的性能，应尽可能使用 [`recvlines()`]。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'\n'
>>> t.recvlinesS(3)
['', '', '']
>>> t.recv_raw = lambda n: b'Foo\nBar\nBaz\n'
>>> t.recvlinesS(3)
['Foo', 'Bar', 'Baz']
```

### `recvlinesb() → bytearray 列表`

```py
recvlinesb(numlines, drop=True, timeout=default) → bytearray 列表
```

此函数与 [`recvlines()`] 相同，但返回 `bytearray`。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'\n'
>>> t.recvlinesb(3)
[bytearray(b''), bytearray(b''), bytearray(b'')]
>>> t.recv_raw = lambda n: b'Foo\nBar\nBaz\n'
>>> t.recvlinesb(3)
[bytearray(b'Foo'), bytearray(b'Bar'), bytearray(b'Baz')]
```

### `recvn() → bytes`

```py
recvn(numb, timeout=default) → bytes
```

精确接收 `n` 字节。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

引发：

- `exceptions.EOFError` – 在请求可满足之前连接关闭。

返回：

- 一个字符串，包含从套接字接收到的字节；如果在等待时发生超时，则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> data = b'hello world'
>>> t.recv_raw = lambda *a: data
>>> t.recvn(len(data)) == data
True
>>> t.recvn(len(data)+1) == data + data[:1]
True
>>> t.recv_raw = lambda *a: None
>>> # 剩余数据会被缓冲
>>> t.recv() == data[1:]
True
>>> t.recv_raw = lambda *a: time.sleep(0.01) or b'a'
>>> t.recvn(10, timeout=0.05)
b''
>>> t.recvn(10, timeout=0.06)
b'aaaaaa...'
```

### `recvnS()`

```py
recvnS(*a, **kw)
```

与 [`recvn()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvnb()`

```py
recvnb(*a, **kw)
```

与 [`recvn()`] 相同，但返回 `bytearray`。

### `recvpred() → bytes`

```py
recvpred(pred, timeout=default) → bytes
```

从 tube 一次接收一个字节，直到 `pred(all_bytes)` 求值为 `True`。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

参数：

- `pred`（`callable`）  
    要调用的函数，参数为当前累积的数据。

- `timeout`（`int`）  
    操作超时时间。

引发：

- `exceptions.EOFError` – 连接已关闭。

返回：

- 一个 bytes 对象，包含从套接字接收到的字节；如果在等待时发生超时，则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'abbbaccc'
>>> pred = lambda p: p.count(b'a') == 2
>>> t.recvpred(pred)
b'abbba'
>>> pred = lambda p: p.count(b'd') > 0
>>> t.recvpred(pred, timeout=0.05)
b''
```

### `recvpredS()`

```py
recvpredS(*a, **kw)
```

与 [`recvpred()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvpredb()`

```py
recvpredb(*a, **kw)
```

与 [`recvpred()`] 相同，但返回 `bytearray`。

### `recvregex() → bytes`

```py
recvregex(regex, exact=False, timeout=default, capture=False) → bytes
```

[`recvpred()`] 的包装器，当正则表达式匹配缓冲区中的字符串时返回。

返回在正则表达式匹配之前接收到的所有数据。如果 `capture` 设置为 `True`，则改为返回 `re.Match` 对象。

默认使用 `re.RegexObject.search()`；但如果 `exact` 设置为 `True`，则改用 `re.RegexObject.match()`。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'The lucky number is 1337 as always\nBla blubb blargh\n'
>>> m = t.recvregex(br'number is ([0-9]+) as always\n', capture=True)
>>> m.group(1)
b'1337'
>>> t.recvregex(br'Bla .* blargh\n')
b'Bla blubb blargh\n'
```

### `recvregexS()`

```py
recvregexS(*a, **kw)
```

与 [`recvregex()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvregexb()`

```py
recvregexb(*a, **kw)
```

与 [`recvregex()`] 相同，但返回 `bytearray`。

### `recvrepeat() → bytes`

```py
recvrepeat(timeout=default) → bytes
```

接收数据直到超时或 EOF。

**示例**

```pycon
>>> data = [
... b'd',
... b'', # 模拟超时
... b'c',
... b'b',
... b'a',
... ]
>>> def delayrecv(n, data=data):
...     return data.pop()
>>> t = tube()
>>> t.recv_raw = delayrecv
>>> t.recvrepeat(0.2)
b'abc'
>>> t.recv()
b'd'
```

### `recvrepeatS()`

```py
recvrepeatS(*a, **kw)
```

与 [`recvrepeat()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvrepeatb()`

```py
recvrepeatb(*a, **kw)
```

与 [`recvrepeat()`] 相同，但返回 `bytearray`。

### `recvuntil() → bytes`

```py
recvuntil(delims, drop=False, timeout=default) → bytes
```

接收数据直到遇到 `delims` 之一。

如果在 `timeout` 秒过去之前请求未满足，则所有数据都会被缓冲，并返回空字符串（`''`）。

参数：

- `delims`（`bytes`、`tuple`）  
    分隔字符的字节字符串，或分隔字节字符串列表。

- `drop`（`bool`）  
    丢弃结尾。如果为 `True`，则从返回值末尾移除。

引发：

- `exceptions.EOFError` – 在请求可满足之前连接关闭。

返回：

- 一个字符串，包含从套接字接收到的字节；如果在等待时发生超时，则为 `''`。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b"Hello World!"
>>> t.recvuntil(b' ')
b'Hello '
>>> _=t.clean(0)
>>> # 匹配 'Hello' 中的 'o'
>>> t.recvuntil((b' ',b'W',b'o',b'r'))
b'Hello'
>>> _=t.clean(0)
>>> # 显式匹配完整字符串
>>> t.recvuntil(b' Wor')
b'Hello Wor'
>>> _=t.clean(0)
>>> # 匹配完整字符串，并丢弃匹配内容
>>> t.recvuntil(b' Wor', drop=True)
b'Hello'
```

```pycon
>>> # 尝试使用正则特殊字符
>>> t = tube()
>>> t.recv_raw = lambda n: b"Hello|World"
>>> t.recvuntil(b'|', drop=True)
b'Hello'
```

### `recvuntilS()`

```py
recvuntilS(*a, **kw)
```

与 [`recvuntil()`] 相同，但返回 `str`，使用 `context.encoding` 解码结果。（注意，二进制版本要快得多。）

### `recvuntilb()`

```py
recvuntilb(*a, **kw)
```

与 [`recvuntil()`] 相同，但返回 `bytearray`。

### `send()`

```py
send(data)
```

发送数据。

如果启用了日志级别 `DEBUG`，还会打印出接收到的数据。

如果由于连接已关闭而无法再发送，则引发 `exceptions.EOFError`。

**示例**

```pycon
>>> def p(x): print(repr(x))
>>> t = tube()
>>> t.send_raw = p
>>> t.send(b'hello')
b'hello'
```

### `sendafter() → str`

```py
sendafter(delim, data, timeout=default) → str
```

`recvuntil(delim, timeout=timeout)` 与 `send(data)` 的组合。

### `sendline()`

```py
sendline(data)
```

`t.send(data + t.newline)` 的简写。

**示例**

```pycon
>>> def p(x): print(repr(x))
>>> t = tube()
>>> t.send_raw = p
>>> t.sendline(b'hello')
b'hello\n'
>>> t.newline = b'\r\n'
>>> t.sendline(b'hello')
b'hello\r\n'
```

### `sendlineafter() → str`

```py
sendlineafter(delim, data, timeout=default) → str
```

`recvuntil(delim, timeout=timeout)` 与 `sendline(data)` 的组合。

### `sendlinethen() → str`

```py
sendlinethen(delim, data, timeout=default) → str
```

`sendline(data)` 与 `recvuntil(delim, timeout=timeout)` 的组合。

### `sendthen() → str`

```py
sendthen(delim, data, timeout=default) → str
```

`send(data)` 与 `recvuntil(delim, timeout=timeout)` 的组合。

### `settimeout()`

```py
settimeout(timeout)
```

设置接收操作的超时。如果给定字符串 `"default"`，则使用 `context.timeout`。如果给定 `None`，则没有超时。

**示例**

```pycon
>>> t = tube()
>>> t.settimeout_raw = lambda t: None
>>> t.settimeout(3)
>>> t.timeout == 3
True
```

### `shutdown()`

```py
shutdown(direction='send')
```

根据 `direction` 关闭 tube 以停止进一步读取或写入。

参数：

- `direction`（`str`）  
    要关闭的方向；`"in"`、`"read"` 或 `"recv"` 关闭入方向，`"out"`、`"write"` 或 `"send"` 关闭出方向。

返回：

- `None`

**示例**

```pycon
>>> def p(x): print(x)
>>> t = tube()
>>> t.shutdown_raw = p
>>> _=list(map(t.shutdown, ('in', 'read', 'recv', 'out', 'write', 'send')))
recv
recv
recv
send
send
send
>>> t.shutdown('bad_value')
Traceback (most recent call last):
...
KeyError: "direction must be in ['in', 'out', 'read', 'recv', 'send', 'write']"
```

### `spawn_process()`

```py
spawn_process(*args, **kwargs)
```

生成一个新进程，并将此 tube 作为其 stdin、stdout 和 stderr。

接受与 `subprocess.Popen` 相同的参数。

### `stream()`

接收数据直到 tube 退出，并将其打印到 stdout。

类似于 [`interactive()`]，但不发送输入。

类似于 `print(tube.recvall())`，但数据在接收时打印，而不是在所有数据接收完后打印。

参数：

- `line_mode`（`bool`）  
    是逐行接收还是原始数据接收。

返回：

- 打印的所有数据。

### `timeout_change()`

不应直接调用。通知 tube 的 raw 层超时已更改。

继承自 `Timeout`。

### `unread()`

```py
unread(*a, **kw)
```

[`unrecv()`] 的别名。

### `unrecv()`

```py
unrecv(data)
```

将指定数据放回接收缓冲区的开头。

**示例**

```pycon
>>> t = tube()
>>> t.recv_raw = lambda n: b'hello'
>>> t.recv()
b'hello'
>>> t.recv()
b'hello'
>>> t.unrecv(b'world')
>>> t.recv()
b'world'
>>> t.recv()
b'hello'
```

### `upload_manually()`

```py
upload_manually(data, target_path='./payload', prompt=b'$', chunk_size=0x200, chmod_flags='u+x', compression='auto', end_marker='PWNTOOLS_DONE')
```

使用 base64 编码和压缩手动上传文件。当 tube 连接到 shell 时可以使用。

文件以 base64 编码块的形式追加到文件，然后解压：

```py
loop:
    echo <chunk> | base64 -d >> <target_path>.<compression>
<compression> -d -f <target_path>.<compression>
chmod <chmod_flags> <target_path>
```

假设目标系统上可用 `base64` 命令。当 `compression` 为 `auto` 时，会在 `gzip` 和 `xz` 中选择可用的最佳压缩工具，回退到未压缩上传。

参数：

- `data`（`bytes`）  
    要上传的数据。

- `target_path`（`str`）  
    要上传数据到的路径。

- `prompt`（`bytes`）  
    要等待的 shell 提示符。

- `chunk_size`（`int`）  
    每个要上传块的大小。

- `chmod_flags`（`str`）  
    与 chmod 一起使用的标志。`""` 表示忽略。

- `compression`（`str`）  
    要使用的压缩。`auto` 自动选择最佳压缩，或 `gzip` 或 `xz`。

- `end_marker`（`str`）  
    用于检测输出结束的标记。仅在未设置 prompt 时使用。

示例：

```pycon
>>> l = listen()
>>> l.spawn_process('/bin/sh')
>>> r = remote('127.0.0.1', l.lport)
>>> r.upload_manually(b'some\xca\xfedata\n', prompt=b'', chmod_flags='')
>>> r.sendline(b'cat ./payload')
>>> r.recvline()
b'some\xca\xfedata\n'

>>> r.upload_manually(cyclic(0x1000), target_path='./cyclic_pattern', prompt=b'', chunk_size=0x10, compression='gzip')
>>> r.sendline(b'sha256sum ./cyclic_pattern')
>>> r.recvlineS(keepends=False).startswith(sha256sumhex(cyclic(0x1000)))
True

>>> blob = ELF.from_assembly(shellcraft.echo('Hello world!\n') + shellcraft.exit(0))
>>> r.upload_manually(blob.data, prompt=b'')
>>> r.sendline(b'./payload')
>>> r.recvline()
b'Hello world!\n'
>>> r.close()
>>> l.close()
```

### `wait()`

```py
wait(timeout=pwnlib.timeout.Timeout.default)
```

等待直到 tube 关闭。

### `wait_for_close()`

```py
wait_for_close(timeout=pwnlib.timeout.Timeout.default)
```

等待直到 tube 关闭。

### `write()`

```py
write(*a, **kw)
```

[`send()`] 的别名。

### `write_raw()`

```py
write_raw(*a, **kw)
```

`send_raw()` 的别名。

### `writeafter()`

```py
writeafter(*a, **kw)
```

[`sendafter()`] 的别名。

### `writeline()`

```py
writeline(*a, **kw)
```

[`sendline()`] 的别名。

### `writelineafter()`

```py
writelineafter(*a, **kw)
```

[`sendlineafter()`] 的别名。

### `writelines()`

```py
writelines(*a, **kw)
```

`sendlines()` 的别名。

### `writelinethen()`

```py
writelinethen(*a, **kw)
```

[`sendlinethen()`] 的别名。

### `writethen()`

```py
writethen(*a, **kw)
```

[`sendthen()`] 的别名。

### `default: TimeoutDefault = pwnlib.timeout.Timeout.default`

表示不应更改超时的值。

### `forever: None = None`

表示不应发生超时的值。

### `property newline`

`sendline()` 等方法发送的字符，或用于 `recvline()` 的字符。

```pycon
>>> t = tube()
>>> t.newline = b'X'
>>> t.unrecv(b'A\nB\nCX')
>>> t.recvline()
b'A\nB\nCX'
```

```pycon
>>> t = tube()
>>> context.newline = b'\r\n'
>>> t.newline
b'\r\n'
```

```pycon
# 清理
>>> context.clear()
```