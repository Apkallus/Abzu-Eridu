# `pwnlib.tubes.sock` — 套接字

https://docs.pwntools.com/en/latest/tubes/sockets.html

## `class pwnlib.tubes.sock.sock`

基类：`tube`。

用于 `tubes.remote` 和 `tubes.listen` 类的基类型。

## `class pwnlib.tubes.remote.remote()`

```py
class pwnlib.tubes.remote.remote(host, port, fam='any', typ='tcp', sock=None, ssl=False, ssl_context=None, ssl_args=None, sni=True, *args, **kwargs)
```

基类：`sock`。

创建到远程主机的 TCP 或 UDP 连接。同时支持 IPv4 和 IPv6。

返回的对象支持 `pwnlib.tubes.sock` 和 `pwnlib.tubes.tube` 的所有方法。

**参数：**
- **host**（`str`）— 要连接的主机。
- **port**（`int`）— 要连接的端口。
- **fam** — 字符串 `"any"`、`"ipv4"` 或 `"ipv6"`，或传给 `socket.getaddrinfo()` 的整数。
- **typ** — 字符串 `"tcp"` 或 `"udp"`，或传给 `socket.getaddrinfo()` 的整数。
- **timeout** — 正数、`None` 或字符串 `"default"`。
- **sock**（`socket.socket`）— 要继承的套接字，而不是建立连接。
- **ssl**（`bool`）— 使用 SSL 包装套接字。
- **ssl_context**（`ssl.SSLContext`）— 指定用于包装套接字的 `SSLContext`。
- **ssl_args**（`dict`）— 以字典形式传入 `ssl.wrap_socket()` 的命名参数。
- **sni**（`str`、`bool`）— 设置 `ssl_args` 中的 `'server_hostname'`。设为 `True` 时根据 `host` 参数设置；设为 `False` 时不提供值。默认是 `True`。

**示例**

```pycon
>>> r = remote('google.com', 443, ssl=True)
>>> r.send(b'GET /\r\n\r\n')
>>> r.recvn(4)
b'HTTP'
```

如果无法建立连接，将引发异常。

```text
>>> r = remote('127.0.0.1', 1)
Traceback (most recent call last):
...
PwnlibException: Could not connect to 127.0.0.1 on port 1
```

也可以使用 `remote.fromsocket()` 包装现有套接字。

```pycon
>>> import socket
>>> s = socket.socket()
>>> s.connect(('google.com', 80))
>>> s.send(b'GET /' + b'\r\n'*2)
9
>>> r = remote.fromsocket(s)
>>> r.recvn(4)
b'HTTP'
>>> s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
>>> s.connect(('2606:4700:4700::1111', 80))
>>> s.send(b'GET ' + b'\r\n'*2)
8
>>> r = remote.fromsocket(s)
>>> r.recvn(4)
b'HTTP'
```

### `classmethod fromsocket()`

```py
classmethod fromsocket(socket)
```

辅助方法，使用 tube API 包装标准 Python `socket.socket`。

**参数：**
- **socket** — `socket.socket` 实例。

**返回：**
- `pwnlib.tubes.remote.remote` 实例。

### `__init__()`

```py
__init__(host, port, fam='any', typ='tcp', sock=None, ssl=False, ssl_context=None, ssl_args=None, sni=True, *args, **kwargs)
```

## `class pwnlib.tubes.listen.listen()`

```py
class pwnlib.tubes.listen.listen(port=0, bindaddr='::', fam='any', typ='tcp', *args, **kwargs)
```

基类：`sock`。

创建用于接收数据的 TCP 或 UDP 套接字。同时支持 IPv4 和 IPv6。使用监听套接字前需要调用 `wait_for_connection()`。

返回的对象支持 `pwnlib.tubes.sock` 和 `pwnlib.tubes.tube` 的所有方法。

**参数：**
- **port**（`int`）— 要连接的端口。默认由操作系统自动选择。
- **bindaddr**（`str`）— 要绑定到的地址。默认为 `0.0.0.0` / `::`。
- **fam** — 字符串 `"any"`、`"ipv4"` 或 `"ipv6"`，或传给 `socket.getaddrinfo()` 的整数。
- **typ** — 字符串 `"tcp"` 或 `"udp"`，或传给 `socket.getaddrinfo()` 的整数。

**示例**

```pycon
>>> l = listen(1234)
>>> r = remote('localhost', l.lport)
>>> _ = l.wait_for_connection()
>>> l.sendline(b'Hello')
>>> r.recvline()
b'Hello\n'
>>> l.close()
>>> r.close()
```

```pycon
>>> # 默认情况下可与 ipv4 配合使用
>>> l = listen(1234)
>>> l.spawn_process('/bin/sh')
>>> r = remote('127.0.0.1', l.lport)
>>> r.sendline(b'echo Goodbye')
>>> r.recvline()
b'Goodbye\n'
```

```pycon
>>> # 它默认也可与 ipv6 配合使用！
>>> l = listen()
>>> r = remote('::1', l.lport)
>>> _ = l.wait_for_connection()
>>> r.sendline(b'Bye-bye')
>>> l.recvline()
b'Bye-bye\n'
```

### `__init__()`

```py
__init__(port=0, bindaddr='::', fam='any', typ='tcp', *args, **kwargs)
```

### `close()`

关闭该 `tube`。

### `spawn_process()`

```py
spawn_process(*args, **kwargs)
```

启动一个新进程，并将此 `tube` 作为其标准输入、标准输出和标准错误。

接受与 `subprocess.Popen` 相同的参数。

### `wait_for_connection()`

阻塞直到建立连接。

### `canonname = None`

监听接口的规范名称。

### `family = None`

套接字族。

### `lhost = None`

本地主机。

### `lport = 0`

本地端口。

### `protocol = None`

套接字协议。

### `sockaddr = None`

正在监听的 `sockaddr` 结构。

### `type = None`

套接字类型（例如 `socket.SOCK_STREAM`）。

## `class pwnlib.tubes.server.server()`

```py
class pwnlib.tubes.server.server(port=0, bindaddr='::', fam='any', typ='tcp', callback=None, blocking=False, *args, **kwargs)
```

基类：`sock`。

创建用于监听连接的 TCP 或 UDP 服务器。同时支持 IPv4 和 IPv6。

有两种使用方式：调用 `next_connection()` 为每个传入连接获取一个 `tube`，或提供一个回调，对每个传入连接以对应 `tube` 调用该回调。提供回调时，接受线程可以在回调运行期间阻塞，也可以在新线程中启动回调。仅在未提供回调时，`next_connection()` 方法才有效。

**参数：**
- **port**（`int`）— 要连接的端口。默认由操作系统自动选择。
- **bindaddr**（`str`）— 要绑定到的地址。默认为 `0.0.0.0` / `::`。
- **fam** — 字符串 `"any"`、`"ipv4"` 或 `"ipv6"`，或传给 `socket.getaddrinfo()` 的整数。
- **typ** — 字符串 `"tcp"` 或 `"udp"`，或传给 `socket.getaddrinfo()` 的整数。
- **callback** — 在传入连接上启动的函数。它应仅接受一个 `pwnlib.tubes.remote` 参数。
- **blocking**（`bool`）— 是否在回调运行期间阻塞接受线程。为 `False` 时，回调在另一个线程中执行。仅在提供回调时相关。默认为 `False`。

**示例**

```pycon
>>> s = server(8888)
>>> client_conn = remote('localhost', s.lport)
>>> server_conn = s.next_connection()
>>> client_conn.sendline(b'Hello')
>>> server_conn.recvline()
b'Hello\n'
>>> client_conn.close()
>>> s.close()
```

```pycon
>>> def cb(r):
...     client_input = r.readline()
...     r.send(client_input[::-1])
...
>>> t = server(8888, callback=cb)
>>> client_conn = remote('localhost', t.lport)
>>> client_conn.sendline(b'callback')
>>> client_conn.recv()
b'\nkcabllac'
>>> client_conn.close()
>>> t.close()
```

### `__init__()`

```py
__init__(port=0, bindaddr='::', fam='any', typ='tcp', callback=None, blocking=False, *args, **kwargs)
```

### `close() → None`

关闭监听套接字并等待接受线程结束。

### `next_connection() → tubes.remote`

如果未提供回调，返回服务器的下一个连接。

### `canonname = None`

监听接口的规范名称。

### `family = None`

套接字族。

### `lhost = None`

本地主机。

### `lport = 0`

本地端口。

### `protocol = None`

套接字协议。

### `sockaddr = None`

正在监听的 `sockaddr` 结构。

### `type = None`

套接字类型（例如 `socket.SOCK_STREAM`）。