### 功能

#### head

```head [参数] [文件]```

默认查看文件前十行

参数
- ```n行数``` 显示的行数

### 工具

#### curl

```curl [options / URLs]```

[手册](https://curl.se/docs/manpage.html)

参数
- ```-O，--remote-name``` 下载的文件名使用原文件名
- ```-s, --silent``` 静默下载
- ```-S, --show-error``` 失败时显示错误信息


#### wget

``` wget [option]... [URL]...```

参数
- ```--no-verbose``` 关闭详细输出

#### Nmap

```nmap [Scan Type(s)] [Options] {target specification}```

[文档](https://nmap.org/book/man.html)

参数
- ```-Pn``` 将所有主机视为在线，跳过主机发现
- ```-sS/sT/sA/sW/sM``` 分别对应TCP SYN/Connect()/ACK/Window/Maimon scans
- ```-p<port ranges>``` 指定扫描的端口，如```-p22```,```-p0-65535```
- ```-sV``` 探测开放端口以识别服务/版本信息

#### host

```host [-aCdilrTvVw] [-c class] [-N ndots] [-t type] [-W time] [-R number] [-m flag] [-p port] hostname [server]```

参数
- `-t <type>` 指定查询类型，如 `ns`为名字服务器
    - `host -t PTR <反向IP>.in-addr.arpa` 反向查询
        将IP地址转换为反向格式（如 192.168.1.100 → 100.1.168.192.in-addr.arpa）
- `-l <域名> [权威 DNS 服务器地址]` 使用 AXFR（区域传输）协议，列出一个域的所有主机记录
- `<server>` 指定本次查询的 DNS 服务器