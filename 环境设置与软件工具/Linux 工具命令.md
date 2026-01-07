## 功能



### docker

`docker run -d -p 127.0.0.1:3000:3000 getting-started`
[文档](https://docs.docker.com/get-started/workshop/02_our_app/)

- `docker run`
	运行容器，并指定镜像的名称
- `-p HOST:CONTAINER`
	用于在主机和容器之间创建端口映射，其中 HOST 是主机上的地址， CONTAINER 是容器上的端口

- `-ps`
	显示正在运行的容器。要查看所有容器，使用 --all （或 -a ）标志
- `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]` 
	运行中的容器中执行新命令，[文档](https://docs.docker.com/reference/cli/docker/container/exec/)
	- `-i, --interactive`
		即使未附加也保持 STDIN 打开
	- `-t, --tty`		
		分配伪终端
	- `-u, --user`
		Username or UID，使用 `-u root` 或 `-u 0`以root权限进入
	
	例，`docker exec -u root -it 容器名或ID /bin/bash`


### man

man 是系统的手册分页程序。

手册页操作：
您可以使用方向键（以及 PgUp/PgDn 键）滚动手册页，并使用 `/` 进行搜索。
搜索后，可按 `n` 键跳至下一个结果，按 `N` 键跳至上一个结果。
除了 `/`，您还可以使用 `?` 进行反向搜索！

参数：
- `-k, --apropos [关键词]`  
	大约等同于 apropos。搜索关键词对应的手册概述并显示所有匹配结果。

### 文件与内容，字符串处理

#### head

```head [参数] [文件]```

默认查看文件前十行

参数
- ```n行数``` 显示的行数

#### echo


参数
- `-n` 不输出尾随的换行符
- `-e` 启用反斜杠转义的解释

#### tr

`tr [OPTION]... STRING1 [STRING2]`

- `[:lower:]`
    all lower case letters

- `[:upper:]`
   all upper case letters

例：
- 字符串大写转小写
	`tr [:upper:] [:lower:]`

#### grep

[手册](https://www.man7.org/linux/man-pages/man1/grep.1.html)

```sh
grep [OPTION]... PATTERNS [FILE]...
grep [OPTION]... -e PATTERNS ... [FILE]...
grep [OPTION]... -f PATTERN_FILE ... [FILE]...
```

`grep` 在每个`FILE`中搜索模式。  
在第一个形式中（如果没有 -e 或 -f 选项），第一个操作数模式是由换行符分隔的一个或多个模式，grep 会打印出与模式匹配的每一行。

参数
- `-r, --recursive`  
	递归搜索目录
- `-E, --extended-regexp` 
	将模式解释为扩展正则表达式。
- `-P, --perl-regexp`
	将模式解释为 perl 正则表达式。
	- `(?<=foo)`
		匹配 foo 但不包含在结果中
- `-o, --only-matching`
	仅打印匹配（非空）的行部分，每个这样的部分单独输出在一行上。

#### diff

```sh
diff [OPTION]... FILES
```

逐行比较文件。

输出示例：
- `2a3` 在第一个文件的第2行后追加第二个文件的第3行
- `5c5` 第一个文件的第5行被替换为第二个文件的第5行

#### ls

`ls [OPTION]... [FILE]...`

列出参数所指定目录中的文件，若未提供参数则默认列出当前目录内容。

参数：
- `-a, --all`  
	不忽略以 . 开头的条目。
- `-l`  
	使用长列表格式
- `-R, --recursive`  
	递归列出子目录

#### touch

`touch [OPTION]... FILE...`

更新每个文件的访问和修改时间为当前时间。
如果不存在，一个不存在的文件参数会被创建为空文件，除非提供 -c 或 -h 选项。

#### mv

```sh
mv [OPTION]... [-T] SOURCE DEST
mv [OPTION]... SOURCE... DIRECTORY
mv [OPTION]... -t DIRECTORY SOURCE...
```

将 SOURCE 重命名为 DEST，或将 SOURCE(s) 移动到 DIRECTORY。

#### cp

```sh
cp [OPTION]... [-T] SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
cp [OPTION]... -t DIRECTORY SOURCE...
```

将 SOURCE 复制到 DEST，或将 SOURCE(s) 复制到 DIRECTORY。

#### namei

``` namei [options] pathname...```

递归列出目录中文件信息

#### mkdir

```sh
mkdir [OPTION]... DIRECTORY...
```

创建目录（如果它们尚不存在）。

#### find

`find [path...] [expression]`

如果未指定搜索条件，`find` 将匹配所有文件。  
如果未指定搜索位置，`find` 将使用当前工作目录（`.`）。  

参数：
- `-name pattern`  
	基础文件名匹配 pattern
- `type [类型]`  
	d 目录  
	f 普通文件  
	l 符号链接  
	p 命名管道  
	s 套接字  

#### ln

```sh
ln [选项]... [-T] 目标 链接名
ln [选项]... 目标
ln [选项]... 目标... 目录
ln [选项]... -t 目录 目标...
```

在第一种格式中，创建具有指定链接名且指向指定目标的链接。在第二种格式中，在当前目录创建指向目标位置的链接。在第三、四种格式中，在指定目录中创建指向指定目标的链接。默认创建硬链接，当使用 --symbolic 时创建符号链接。

参数：
- `-s, --symbolic`  
	创建符号链接而非硬链接

#### 文件名通配符

- `*` 多字符通配符，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `?` 单字符通配符，，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `[]` 单字符限定匹配，匹配括号内指定的可能字符子集的通配符。
- `[!]`、`[^]` 排除符，如果方括号内的第一个字符是 `!` 或（在较新版本的 bash 中）`^`，该通配符模式将进行反向匹配，即该方括号实例会匹配*不*在所列出的字符范围内的字符。  
	当 `!` 字符不是 `[]` 通配符的首字符时，它在 bash 中具有不同的特殊含义！`^` 没有这个问题，但在较旧的 shell 中可能不兼容。

## 工具

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

#### Ncat

[手册](https://nmap.org/book/ncat-man.html)
参数：
- `-l, --listen`  
	绑定并监听传入连接

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



#### dig

域名信息收集器（domain information groper）

参数
- `+short` 简洁信息

#### whois

查询对象的 whois 数据库



#### openssl

- `s_client`
	通用 SSL/TLS 客户端

##### openssl enc

`openssl enc|cipher [-cipher] [-help] [-list] [-ciphers] [-in filename] [-out filename] [-pass arg] [-e] [-d] [-a] [-base64] [-A] [-k password] [-kfile filename] [-K key] [-iv IV] [-S salt] [-salt] [-nosalt] [-z] [-md digest] [-iter count] [-pbkdf2] [-saltlen size] [-p] [-P] [-bufsize number] [-nopad] [-v] [-debug] [-none] [-skeymgmt skeymgmt] [-skeyopt opt:value] [-skeyuri uri] [-storepass arg] [-rand files] [-writerand file] [-provider name] [-provider-path path] [-provparam [name:]key=value] [-propquery propq]`

[文档](https://docs.openssl.org/master/man1/openssl-enc/)

- `-a` 或 `-base64`
	编码解码时处理换行符
- `-A`
	不处理换行符
- `-d`
	解密数据
- `-kfile filename`
	从指定文件读取密码
- `-加密算法-密钥长度-工作模式`
	- 例：`-aes-256-cbc`
		aes算法 256位密钥 密码块链接模式（cbc）

##### openssl x509

- `-noout`
	禁止其他输出

- `-pubkey`
	以PEM格式打印证书公钥

##### openssl rsa

`openssl rsa [-help] [-inform DER|PEM|P12|ENGINE] [-outform DER|PEM] [-in filename|uri] [-passin arg] [-out filename] [-passout arg] [-aes128] [-aes192] [-aes256] [-aria128] [-aria192] [-aria256] [-camellia128] [-camellia192] [-camellia256] [-des] [-des3] [-idea] [-text] [-noout] [-modulus] [-traditional] [-check] [-pubin] [-pubout] [-RSAPublicKey_in] [-RSAPublicKey_out] [-pvk-strong] [-pvk-weak] [-pvk-none] [-engine id] [-provider name] [-provider-path path] [-propquery propq]`

- `-in filename|uri` 
	指定了从何处读取密钥，如果未指定此选项，则使用标准输入。如果密钥是加密的，将提示输入密码短语。
- `-noout` 
- `-modulus`
	打印出密钥的模值。

##### openssl dgst

`openssl dgst|digest [-digest] [-list] [-help] [-c] [-d] [-debug] [-hex] [-binary] [-xoflen length] [-r] [-out filename] [-sign filename|uri] [-keyform DER|PEM|P12|ENGINE] [-passin arg] [-verify filename] [-prverify filename] [-signature filename] [-sigopt nm:v] [-hmac key] [-mac alg] [-macopt nm:v] [-fips-fingerprint] [-engine id] [-engine_impl id] [-rand files] [-writerand file] [-provider name] [-provider-path path] [-propquery propq] [file ...]`

- `-digest`
	指定要使用的支持的分 digest 的名称。见 `-list` 选项
- `-sign filename|uri`
	使用提供的私钥对摘要进行数字签名。
- `-out filename`
	输出文件名，或默认标准输出。
- `file ...`
	要处理的文件或文件列表。如果没有指定文件，则使用标准输入。



#### hashcat

[文档](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat)


#### ssh-keygen

[文档](https://www.ssh.com/academy/ssh/keygen)

参数：
- `-f <filename>`
	选择存储密钥的文件
- `-N "新"` 	
	为密钥提供一个新的密码短语
- `-i "输入"` 	
	访问现有密钥文件

示例：
- `ssh-keygen -f key -N ''`	
	生成一个 以 `key` 为名称的 ssh 密钥，私钥 `key`，公钥 `key.pub`。密码为 `''`
	

#### 其他

- `2>/dev/null`
	丢弃错误信息

- `mkdir [OPTION]... DIRECTORY...`
	创建目录

- 如果你在 shell 中按 tab 键，它会尝试推断你将要输入的内容并自动补全。  
	默认情况下，`bash` 会在出现多个匹配选项时自动扩展到第一个分歧点（在此例中为 `fl`）。  
	当你*第二次*按下 tab 键时，它会列出这些匹配选项。  
	
	补全选项根据位置，即上下文不同，对应不同文件:
	- 命令位置：补的是“可执行命令”（过滤掉普通文件）。
	- 参数位置：补的是“文件名/路径”（不过滤普通文件）。


## 参考

https://man.archlinux.org/man

https://linux.die.net/man

https://pwn.college/