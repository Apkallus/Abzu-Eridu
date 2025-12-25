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
- ```-d, --data <data>```
    (HTTP MQTT) Sends the specified data in a POST request to the HTTP server
- ```-I, --head```
	Fetch the headers only.
- ```-k, --insecure```
	(TLS SFTP SCP) 默认情况下，curl 建立的每个安全连接在传输之前都会验证其安全性。这个选项使 curl 跳过验证步骤，在不检查的情况下继续进行。
- ```-L, --location```
	(HTTP) 如果服务器报告请求的页面已移动到不同位置（通过 Location: 标头和 3XX 响应代码指示），此选项会使 curl 重新向新位置发起请求。如果与 --show-headers 或 --head 一起使用，则会显示所有请求页面的标头。
- ```-O，--remote-name``` 
	下载的文件名使用原文件名
- ```-s, --silent``` 
	静默下载
- ```-S, --show-error``` 
	失败时显示错误信息
- ```-x, --proxy [protocol://]host[:port]``` 
	Use the specified proxy.
- ```-X, --request <method>``` 
	Change the method to use when starting the transfer.

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

#### nc

```nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
	  [-m minttl] [-O length] [-P proxy_username] [-p source_port]
	  [-q seconds] [-s sourceaddr] [-T keyword] [-V rtable] [-W recvlimit]
	  [-w timeout] [-X proxy_protocol] [-x proxy_address[:port]]
	  [destination] [port]
```

#### echo


参数
- `-n` 不输出尾随的换行符
- `-e` 启用反斜杠转义的解释


#### namei

``` namei [options] pathname...```

递归列出目录中文件信息

#### dig

域名信息收集器（domain information groper）

参数
- `+short` 简洁信息

#### whois

查询对象的 whois 数据库