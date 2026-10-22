# 标准库

## 互联网协议和支持

---



### http.server --- HTTP 服务器

https://docs.python.org/zh-cn/3.14/library/http.server.html

#### 命令行接口

```sh
python -m http.server [OPTIONS] [port]
```

选项
- `port`
    服务器默认监听 8000 端口

- `-p, --protocol <version>`
    指定服务器所采用的 HTTP 版本。 在默认情况下，服务器会采用 HTTP/1.0
