https://www.man7.org/linux/man-pages/man1/intro.1.html

## 文件/编码

### genisoimage - 创建具有可选 Rock Ridge 属性的 ISO9660/Joliet/HFS 文件系统

https://linux.die.net/man/1/genisoimage

```sh
genisoimage [options] [-o filename] pathspec [pathspec ...] 
```

- `-o` `filename`  
    指定 ISO9660 文件系统映像的输出文件。这可以是磁盘文件、磁带驱动器，也可以直接对应光盘写入器的设备名。如果未指定，则使用 stdout

- `-sort` `sort_file`  
    对介质上的文件位置进行排序。
	> 错误信息泄露文件内容

```sh
# 读取拥有权限的文件
genisoimage -o - 拥有权限的文件

# 错误信息泄露
genisoimage -sort /flag
```

### od - 以八进制和其他格式转储文件

https://www.man7.org/linux/man-pages/man1/od.1.html

```sh
od [option]... [file]...
od [-abcdfilosx]... [file] [[+]offset[.][b]]
od [option]... --traditional [file] [[+]offset[.][b] [[+]label[.][b]]]
```

将文件 `FILE` 的内容以默认的八进制字节格式写入标准输出。如果提供多个 `FILE` 参数，则按指定顺序连接它们作为输入。

- `-A radix`, `--address-radix=radix`  
    文件偏移量的输出格式；RADIX 是 `[doxn]` 中的一种，用于十进制、八进制、十六进制或无。
    - `n`  
        无偏移量

- `-t type`  `--format=type`  
	选择文件数据的输出格式。type 是一个由以下类型标识符字符之一组成的字符串。

    除了类型“a”和“c”之外，您可以通过在类型指示符字符后面加一个十进制整数来指定在解释给定数据类型中的每个数字时使用的字节数。

传统规范格式：
- `-a`  
    与 `-t a` 相同，选择命名字符，忽略高阶字符比特

- `-c`  
	与 `-t c` 相同，选择 ASCII 字符或反斜杠转义


`TYPE` 由以下一种或多种规格组成：
- `a`  
    ascii

- `x[SIZE]`  
    16进制

示例
```console
$ echo -n 'abcdef' | od -An -tx1
   61 62 63 64 65 66

$ echo -n 'abcdef' | od -An -tx2
   6261 6463 6665

# 无偏移量，输出 ascii
$ echo -n 'abcdef' | od -An -ta
   a   b   c   d   e   f
```

### bzip2, bunzip2 bzcat bzip2recover - 压缩或扩展文件

https://linux.die.net/man/1/bzip2

```sh
bzip2 [ -cdfkqstvzVL123456789 ] [ filenames ... ]
bunzip2 [ -fkvsVL ] [ filenames ... ]
bzcat [ -s ] [ filenames ... ]
bzip2recover filename
```

- `-d --decompress`  
	强制解压缩

- `-z --compress`
	强制压缩

- `-c --stdout`  
	压缩或解压到标准输出。

```sh
bzip2 -c /flag | bzip2 -d
```

### zip - 打包和压缩（归档）文件


https://linux.die.net/man/1/zip
```sh
zip [-aABcdDeEfFghjklLmoqrRSTuvVwXyz!@$] [--longoption ...] [-b path] [-n suffixes] [-t date] [-tt date] [zipfile [file ...]] [-xi list] 
```

```sh
# 读取文件
zip my_flag.zip /flag && unzip -c my_flag.zip 

# 交互 shell
# 测试命令后添加注释符号 `#` 以分离后缀，或任意分隔符
zip foo.zip foo.zip -T -TT "/bin/sh #"
```

#### 使用

**命令格式。** 基本命令格式为

```sh
zip options archive inpath inpath ...
```

其中 `archive` 是新的或现有的 `zip` 归档，`inpath` 是目录或文件路径，可选地包含通配符。当给定现有 `zip` 归档的名称时，`zip` 将替换 `zip` 归档中同名的条目（匹配归档中存储的相对名称）或为新名称添加条目。例如，如果 `foo.zip` 存在并包含 `foo/file1` 和 `foo/file2`，而目录 `foo` 包含文件 `foo/file1` 和 `foo/file3`，那么：

```sh
zip -r foo.zip foo
```

或更简洁地

```sh
zip -r foo foo
```

**`-@` 文件列表。** 如果文件列表指定为 `-@` [MacOS 上不可用]，`zip` 从标准输入而不是命令行获取输入文件列表。例如，

```sh
zip -@ foo
```

将标准输入中每行列出的文件存储到 `foo.zip` 中。

在 Unix 下，此选项与 `find` (1) 命令结合使用可以产生强大效果。例如，要归档当前目录及其子目录中的所有 C 源文件：

```sh
find . -name "*.[ch]" -print | zip source -@
```

（注意模式必须加引号，以防止 shell 展开它）。

**流式输入和输出。** `zip` 还接受单个短横线（`-`）作为 zip 文件名，在这种情况下，它将 zip 文件写入标准输出，允许将输出管道传输到另一个程序。例如：

```sh
zip -r - . | dd of=/dev/nrst0 obs=16k
```

会将 zip 输出直接写入具有指定块大小的磁带，以备份当前目录。

`zip` 还接受单个短横线（`-`）作为要压缩文件的名称，在这种情况下，它将从标准输入读取文件，允许 zip 从另一个程序获取输入。例如：

```sh
tar cf - . | zip backup -
```

#### 参数

- `-r`, `--recurse-paths`  
    递归遍历目录结构；例如：

    ```sh
    zip -r foo.zip foo
    ```

- `-X, --no-extra`  
	不要保存额外的文件属性

- `-TT cmd`, `--unzip-command cmd`  
    使用命令 `cmd` 而不是 `unzip -tqq` 来测试归档（当使用 `-T` 选项时）。在 Unix 上，要使用当前目录中的 unzip 副本而不是标准系统 unzip，可以使用：

    ```sh
    zip archive file1 file2 -T -TT "./unzip -tqq"
    ```

    在 `cmd` 中，`{}` 被替换为临时归档的名称，否则归档名称附加到命令末尾。检查返回代码是否成功（Unix 上为 0）。

### unzip - 解压 zip 归档文件

https://linux.die.net/man/1/unzip

```sh
unzip [-Z] [-cflptTuvz[abjnoqsCDKLMUVWX$/:^]] file[.zip] [file(s) ...] [-x xfile(s) ...] [-d exdir]
```

`unzip` 将列出、测试或提取 ZIP 归档中的文件

- `-l`  
    列出归档文件（短格式）。打印指定文件的名称、未压缩文件大小和修改日期时间，以及所有指定文件的总计。

- `-v`  
    列出归档文件（详细格式）或显示诊断版本信息。

- `-p`  
    将文件提取到管道（stdout）。除了文件数据外，不向 stdout 发送任何内容，并且文件始终以二进制格式提取，与存储时完全一样（无转换）。

- `-c`  
    将文件提取到 stdout/屏幕（“CRT”）。此选项类似于 `-p` 选项，但提取时会打印每个文件的名称，允许 `-a` 选项，并在适当时自动执行 ASCII-EBCDIC 转换。此选项未列在 `unzip` 使用屏幕中。


### funzip - 用于在管道中从 ZIP 压缩包中提取文件的过滤器

https://linux.die.net/man/1/funzip

```sh
funzip [-password] [input[.zip|.gz]] 
```

示例

```sh
zip - /flag | funzip
```

### cpio - 复制文件到和从归档

在 copy-out 模式中，`cpio` 将文件复制到归档中。它从标准输入读取文件名列表（每行一个），并将归档写入标准输出。

在 copy-in 模式中，`cpio` 从归档中复制文件或列出归档内容。它从标准输入读取归档。

在 copy-pass 模式中，`cpio` 将文件从一个目录树复制到另一个目录树，结合 copy-out 和 copy-in 步骤而不实际使用归档。它从标准输入读取要复制的文件列表；要复制到的目录作为非选项参数给出。

- `-o`, `--create`  
    以 copy-out 模式运行。参见“Copy-out 模式”。

- `-i`, `--extract`  
    以 copy-in 模式运行。参见“Copy-in 模式”。

- `-p`, `--pass-through`  
    以 copy-pass 模式运行。参见“Copy-pass 模式”。

- `-F`, `--file=archive`  
    要使用的归档文件名，而不是标准输入或输出。要使用另一台机器上的磁带驱动器作为归档，请使用以 `HOSTNAME:` 开头的文件名。主机名前面可以加上用户名和 `@`，以便以该用户身份访问远程磁带驱动器（如果你有相应权限，通常是该用户的 `~/.rhosts` 文件中的条目）。

- `-r`, `--rename`  
    交互式重命名文件。

- `-R [user][:.][group]`, `--owner [user][:.][group]`  
    在 copy-out 和 copy-pass 模式下，将所有创建文件的所有权设置为指定用户和/或组。用户、组或两者必须存在。如果省略组但给出了 `:` 或 `.` 分隔符，则使用给定用户的登录组。只有超级用户可以更改文件的所有权。

- `--to-stdout`  
    将文件提取到标准输出。此选项可用于 copy-in 模式。

- `--rsh-command=COMMAND`  
    通知 `cpio` 应使用 `COMMAND` 与远程设备通信。

示例：

```sh
# 标准输入输出流，读取文件内容
ls /flag | cpio -o | cpio -i --to-stdout

# 异常信息读取文件内容
ls /flag | cpio -o

# 复制文件，并修改属主/组
ls /flag | cpio -p -R nobody.nogroup ~
```

```sh
# 命令执行的完整权限 shell
# 尝试远程连接时，预期 rsh 格式 `rsh [OPTION...] [USER@]HOST [COMMAND [ARG...]]`
# 当传递有效的 HOST 名称 `localhost` 时，替换后的 rsh 命令将为：
# `/bin/sh localhost` 此处主机名作为参数1传递，最终同名文件将被作为 shell 脚本执行
echo '/bin/sh </dev/tty >/dev/tty 2>/dev/tty' > localhost &&
cpio -o --rsh-command '/bin/sh' -F localhost:
```

### ar - 创建、修改和从归档中提取

https://man7.org/linux/man-pages/man1/ar.1.html

```sh
ar [-X32_64] [-]p[mod] [--plugin name] [--target bfdname]
[--output dirname] [--record-libdeps libdeps] [--thin] [relpos]
[count] archive [member...]
```

```sh
# 快速归档，若不存在则创建
ar qc my_flag.a /flag
# 打印归档文件内容到标准输出
ar p my_flag.a
```

`p` 操作码字母指定要执行的操作；它可以是以下任意一个，但只能指定其中一个：

- `p`  
    将归档的指定成员*打印*到标准输出文件。如果指定 `v` 修饰符，则在将其内容复制到标准输出之前显示成员名称。

    如果未指定 `member` 参数，则打印归档中的所有文件。

- `x`  
    从归档中*提取*成员（名为 `member`）。你可以与此操作一起使用 `v` 修饰符，以请求 `ar` 在提取每个名称时列出它。

    如果未指定 `member`，则提取归档中的所有文件。

    无法从薄归档中提取文件，并且从使用 `P` 创建的归档中提取文件存在限制：路径不能是绝对路径，不能包含 `..`，并且路径中的任何子目录都必须存在。如果希望避免这些限制，则使用 `--output` 选项指定输出目录。

- `q`  
    *快速追加*；历史上，将文件 `member...` 添加到 `archive` 末尾，而不检查替换。

- `r`  
    将文件 `member...` 插入 `archive`（*替换*）。此操作与 `q` 的不同之处在于，如果任何先前存在的成员名称与要添加的名称匹配，则删除这些成员。

许多修饰符（`mod`）可以紧跟在 `p` 操作码字母之后，以指定操作行为的变体：

- `c`  
    *创建*归档。当请求更新时，如果指定的 `archive` 不存在，它总是会被创建。但除非你通过使用此修饰符事先指定期望创建它，否则会发出警告。

### tar —— 归档

https://www.man7.org/linux/man-pages/man1/tar.1.html

```sh
# Traditional usage
    tar {A|c|d|r|t|u|x}[GnSkUWOmpsMBiajJzZhPlRvwo] [ARG...]

# UNIX-style usage
    tar -A [OPTIONS] -f ARCHIVE ARCHIVE...

    tar -c [-f ARCHIVE] [OPTIONS] [FILE...]

    tar -d [-f ARCHIVE] [OPTIONS] [FILE...]

    tar -r [-f ARCHIVE] [OPTIONS] [FILE...]

    tar -t [-f ARCHIVE] [OPTIONS] [MEMBER...]

    tar -u [-f ARCHIVE] [OPTIONS] [FILE...]

    tar -x [-f ARCHIVE] [OPTIONS] [MEMBER...]
```



示例
```sh
# 创建归档文件，无压缩
tar cf archive.tar inputfile.txt
tar -c -f archive.tar inputfile.txt

# 创建归档文件，并使用 gzip 压缩。此时扩展名应匹配压缩工具
tar cfz archive.tar.gzip inputfile.txt
tar -c -f archive.tar.gzip -z inputfile.txt
```

```sh
# tar 不支持 `/` 符号，设置 -C 以切换目录执行
tar -c -f my_flag.tar -C / flag &&
# 提取归档文件到标准输出
tar -x -O -f my_flag.tar 

# 标准输入输出流
tar -c -f - -C / flag | tar -x -O -f -

# 标准输出 + 命令执行
tar -c -f - -C / flag | tar -x --to-command 'cat'
```

```sh
# 交互 shell 的各种方式

# 调用程序
echo '/bin/sh </dev/tty >/dev/tty 2>/dev/tty' > foo && tar -c -f - foo | tar -x --to-command '/bin/sh'

# 命令过滤
tar -x -f /dev/null -I '/bin/sh -c "/bin/sh </dev/tty >/dev/tty 2>/dev/tty"'

tar -x -f /dev/null -I '/bin/sh -c "/bin/sh 0<&2 1>&2"'

# 远程连接
echo '/bin/sh </dev/tty >/dev/tty 2>/dev/tty' > localhost
tar -x --rsh-command '/bin/sh' -f localhost:caffee

# 检查点
tar -x -f /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

#### 操作模式

- `-c`, `--create`  
    创建新归档。参数提供要归档的文件名称。除非给出 `--no-recursion` 选项，否则目录会被递归归档。

- `-t`, `--list`  
    列出归档内容。参数是可选的。给出时，它们指定要列出的成员名称。

- `-x`, `--extract`, `--get`  
    从归档中提取文件。参数是可选的。给出时，它们指定要提取的归档成员名称。

#### 选项

##### 输出流选择

- `-O`, `--to-stdout`  
    将文件提取到标准输出。

- `--to-command=COMMAND`  
    将提取的文件管道传输到 `COMMAND`。参数是外部程序的路径名，可选地带有命令行参数。程序将被调用，正在提取的文件内容通过其标准输入提供。

##### 扩展文件属性

- `--no-acls`  
    禁用 POSIX ACL 支持。

##### 设备选择和切换

- `-f`, `--file=ARCHIVE`  
    使用归档文件或设备 `ARCHIVE`。如果未给出此选项，`tar` 将首先检查环境变量 `TAPE`。如果设置了，其值将用作归档名称。否则，`tar` 将假定编译时的默认值。可以使用 `--show-defaults` 选项或在 `tar --help` 输出末尾检查默认值。

    包含冒号的归档名称指定远程机器上的文件或设备。冒号前的部分被视为机器名或 IP 地址，冒号后的部分被视为文件或设备路径名，例如：

    `--file=remotehost:/dev/sr0`

    可选用户名可以加在主机名前，两者之间用 `@` 符号分隔。

    默认情况下，远程主机通过 `rsh`(1) 命令访问。如今通常使用 `ssh`(1) 代替。可以通过给出以下命令行选项来实现：

    `--rsh-command=/usr/bin/ssh`

    远程机器应安装 `rmt`(8) 命令。如果其路径名与 `tar` 的默认值不匹配，可以使用 `--rmt-command` 选项告知 `tar` 正确的路径名。

- `--rsh-command=COMMAND`  
    访问远程归档时使用 `COMMAND` 代替 `rsh`。参见上面的 `-f` 选项描述。

##### 压缩选项

- `-a`, `--auto-compress`  
    使用归档后缀确定压缩程序。

- `--no-auto-compress`  
    不使用归档后缀确定压缩程序。

- `-I`, `--use-compress-program=COMMAND`  
    通过 `COMMAND` 过滤数据。它必须接受 `-d` 选项以进行解压。参数可以包含命令行选项。

- `-j`, `--bzip2`  
    通过 `bzip2`(1) 过滤归档。

- `-z`, `--gzip`, `--gunzip`, `--ungzip`  
    通过 `gzip`(1) 过滤归档。

##### 本地文件选择

- `-C`, `--directory=DIR`  
    在执行任何操作之前切换到 `DIR`。此选项对位置敏感，即它影响其后的所有命令行参数，因此其后出现的任何相对文件名将被视为相对于 `DIR`。但是，它不影响其后*命令行选项*的参数，例如 `-f`、`-T` 或 `-N`。

##### 信息输出

- `--checkpoint[=N]`  
    每第 `N` 条记录显示进度消息（默认 10）。

- `--checkpoint-action=ACTION`  
    在每个检查点运行 `ACTION`。

    - `exec` 动作执行给定的外部命令。例如：

        ```console
        $ tar -c --checkpoint=1000 --checkpoint-action=exec=/sbin/cpoint
        ```

#### gzip, gunzip, zcat - 压缩或扩展文件

https://linux.die.net/man/1/gzip

```sh
gzip [ -acdfhlLnNrtvV19 ] [-S suffix] [ name ... ]
gunzip [ -acfhlLnNrtvV ] [-S suffix] [ name ... ]
zcat [ -fhLV ] [ name ... ] 
```

zcat 与 gunzip -c 完全相同。（在某些系统上，zcat 可能被安装为 gzcat 以保留对 compress 的原始链接。）zcat 会解压缩命令行上的文件列表或其标准输入，并将未压缩的数据写入标准输出。zcat 会解压缩具有正确魔数标记的文件，无论它们是否有 .gz 后缀。

- `-d --decompress --uncompress`  
	解压缩

- `-c --stdout --to-stdout`  
	将输出写入标准输出；保持原始文件不变。如果有多个输入文件，输出将由一系列独立压缩的成员组成。为获得更好的压缩效果，在压缩前应将所有输入文件连接起来。

```sh
gzip -c /flag | gzip -d
```

## 远程控制

### rsh - 远程 shell 客户端

```sh
rsh [OPTION...] [USER@]HOST [COMMAND [ARG...]]
```

### ssh

https://www.openssh.org/manual.html

#### ssh - OpenSSH 远程登录客户端

https://www.man7.org/linux/man-pages/man1/ssh.1.html
- https://man.openbsd.org/ssh

```sh
ssh 	[-46AaCfGgKkMNnqsTtVvXxYyZ] [-B bind_interface] [-b bind_address] [-c cipher_spec] [-D [bind_address:]port] [-E log_file] [-e escape_char] [-F configfile] [-I pkcs11] [-i identity_file] [-J destination] [-L address] [-l login_name] [-m mac_spec] [-O ctl_cmd] [-o option] [-P tag] [-p port] [-R address] [-S ctl_path] [-W host:port] [-w local_tun[:remote_tun]] destination [command [argument ...]]

ssh 	[-Q query_option]
```

`ssh`（SSH客户端）是一种用于登录远程机器并执行远程命令的程序。

参数
- `-i identity_file`
    指定用于公钥认证的身份文件（私钥）路径。若本地不存在私钥文件，也可指定公钥文件，以使用 `ssh-agent(1)` 中已加载的对应私钥。默认值为 `~/.ssh/id_rsa`、`~/.ssh/id_ecdsa`、`~/.ssh/id_ecdsa_sk`、`~/.ssh/id_ed25519` 和 `~/.ssh/id_ed25519_sk`。身份文件亦可在配置文件中按主机单独指定。支持使用多个 `-i` 选项（或在配置文件中指定多个身份）。若未通过 `CertificateFile` 指令显式指定证书，`ssh` 还将尝试从身份文件名追加 `-cert.pub` 后所得的文件名中加载证书信息。


示例：
```sh
# 使用名为 `key` 的私钥认证，用户名@主机名
ssh -i key hacker@dojo.pwn.college
``` 

#### ssh-keygen - 认证密钥生成、管理和转换

https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html

参数：
- `-f <filename>`
	指定密钥文件
- `-N new_passphrase` 	
	设置新密码（到密钥）
- `-i "输入"` 	
	使用现有私钥文件连接
- `-D pkcs11`
	从 PKCS#11 共享库 pkcs11 中下载其提供的公钥。与 -s 选项一起使用时，该选项表示某个 CA 的密钥位于一个 PKCS#11 令牌中。（需使用相对或绝对路径）

	- `dlopen()`加载指定共享库后会找一个固定导出符号：`C_GetFunctionList`，于是设置的共享库中应当包含此结构（导入头部或设置最小对应结构）


示例：
```sh
# 生成一个名为 `key` 的 ssh 密钥，私钥 `key`，公钥 `key.pub`。设置密码为 `''`
ssh-keygen -f key -N ''

# 使用名为 `key` 的私钥登录
ssh -i key 用户名@主机名
```	

## 打印文本

### echo - 显示一行文本

https://www.man7.org/linux/man-pages/man1/echo.1.html

```sh
echo [SHORT-OPTION]... [STRING]...
echo LONG-OPTION
```

将 STRING(s)（一个或多个字符串）回显到标准输出。

参数
- `-n`  
	不输出末尾的换行符。
- `-e`  
	启用对反斜杠转义序列的解析。

### yes —— 重复输出字符串，直到被终止

https://www.man7.org/linux/man-pages/man1/yes.1.html

```sh
yes [STRING]...
yes OPTION
```

反复输出所有指定的 STRING(s)或 `'y'`。

## 延迟

### sleep - 延迟指定时间

https://man7.org/linux/man-pages/man1/sleep.1.html

```bash
sleep NUMBER[SUFFIX]...
sleep OPTION
```

暂停 `NUMBER` 秒，其中 `NUMBER` 是整数或浮点数。`SUFFIX` 可以是 `'s'`、`'m'`、`'h'` 或 `'d'`，分别表示秒、分钟、小时、天。如果有多个参数，则暂停它们值之和的时间。

## 数值运算

### seq - 打印数字序列

https://man7.org/linux/man-pages/man1/seq.1.html

```bash
seq [OPTION]... LAST
seq [OPTION]... FIRST LAST
seq [OPTION]... FIRST INCREMENT LAST
```

从 FIRST 到 LAST 按 INCREMENT 步长打印数字。

- `-f, --format=FORMAT`
  使用 printf 风格的浮点 FORMAT
- `-s, --separator=STRING`
  使用 STRING 分隔数字（默认：`\n`）
- `-w, --equal-width`
  通过填充前导零来等宽

如果省略 FIRST 或 INCREMENT，则默认为 1。也就是说，即使 LAST 小于 FIRST，省略的 INCREMENT 也默认为 1。当当前数字与 INCREMENT 之和大于 LAST 时，数字序列结束。FIRST、INCREMENT 和 LAST 被解释为浮点值。如果 FIRST 小于 LAST，INCREMENT 通常为正；如果 FIRST 大于 LAST，INCREMENT 通常为负。INCREMENT 不得为 0；FIRST、INCREMENT 和 LAST 均不得为 `NaN`。FORMAT 必须适合打印一个 `double` 类型的参数；如果 FIRST、INCREMENT 和 LAST 都是最大精度为 PREC 的定点十进制数，则默认为 `%.PRECf`，否则默认为 `%g`。

```bash
# 从1开始，间隔5，直到100
for i in $(seq 1 5 100); do
    echo $i
done
```

## 编码解码

### hexdump  

https://www.man7.org/linux/man-pages/man1/hexdump.1.html

```sh
hexdump [options] file ...

hd [options] file ...
```

`hexdump` 实用程序是一个过滤器，用于以用户指定的格式显示指定文件；如果未指定文件，则显示标准输入。

- `-c`, `--one-byte-char`  
    单字节字符显示。以十六进制显示输入偏移量，随后每行显示十六个以空格分隔、三列、空格填充的输入数据字符。

- `-f`, `--format-file` `file`  
    指定一个文件，其中包含一个或多个以换行分隔的格式字符串。空行以及第一个非空白字符为井号（`#`）的行会被忽略。

- `-v`, `--no-squeezing`  
    `-v` 选项使 `hexdump` 显示所有输入数据。不使用 `-v` 时，任意数量的、与紧邻前一组输出行相同（输入偏移量除外）的输出行组，都会替换为仅包含一个星号的一行。

- `-e`, `--format` `format_string`  
    指定用于显示数据的格式字符串。

#### 格式

格式字符串包含任意数量的格式单元，格式单元之间由空白分隔。一个格式单元最多包含三项：迭代次数、字节数和格式。

### xxd

https://linux.die.net/man/1/xxd

```sh
xxd -h[elp]
xxd [options] [infile [outfile]]
xxd -r[evert] [options] [infile [outfile]]
```

`xxd` 为给定文件或标准输入创建十六进制转储。它还可以将十六进制转储转换回原始二进制形式。

如果未给出 `infile`，则读取标准输入。如果 `infile` 指定为 `-` 字符，则从标准输入获取输入。如果未给出 `outfile`（或在其位置使用 `-` 字符），则结果发送到标准输出。

- `-p`, `-ps`, `-postscript`, `-plain`  
    以 PostScript 连续十六进制转储样式输出。也称为纯十六进制转储样式。

- `-r`, `-revert`  
    反向操作：将十六进制转储转换（或修补）为二进制。如果不写入标准输出，`xxd` 会写入其输出文件而不截断它。使用 `-r -p` 组合可读取不含行号信息且没有特定列布局的纯十六进制转储。允许在任何位置出现额外空白和换行。

```console
# 字符串转十六进制字符串
$ echo -n 'pwn' | xxd -p
70776e

# 十六进制字符串还原到字符串
$ echo 70776e | xxd -r -p
pwn
$ echo 70 77 6e | xxd -r -p
pwn
```

### base32

https://www.man7.org/linux/man-pages/man1/base32.1.html

```sh
base32 [OPTION]... [FILE]
```
- `-d, --decode`
	解码数据。

- `-w, --wrap=COLS`
	设置换行字符数量，默认76。设置0禁用换行

### base64

https://www.man7.org/linux/man-pages/man1/base64.1.html

```sh
base64 [OPTION]... [FILE]
```

- `-d, --decode`
	解码数据。

- `-w, --wrap=COLS`
	设置换行字符数量，默认76。设置0禁用换行

## 架构

### setarch 在新程序环境中更改报告的架构和/或设置个性标志

https://man7.org/linux/man-pages/man8/setarch.8.html

```sh
setarch [arch] [options] [program [argument...]]
arch [options] [program [argument...]]
```

```sh
setarch --addr-no-randomize /bin/sh -p
```

- `--list`  
    列出 `setarch` 已知的体系结构。`setarch` 是否能够实际设置每种体系结构取决于正在运行的内核。

- `--show[=personality]`  
    显示当前活动的 personality 和标志。如果提供了 `personality` 参数，则显示该 personality 而不是当前的。`personality` 是一个十六进制数字，其可能值在 `sys/personality.h` 中描述。

- `-p`, `--pid=pid`  
    与 `--show` 一起使用时，显示指定进程的 personality 和标志。

- `-v`, `--verbose`  
    详细模式。

- `-3`, `--3gb`  
    指定的 `program` 应使用最多 3GB 的地址空间。在 x86 上受支持。打开 `ADDR_LIMIT_3GB`。

- `-B`, `--32bit`  
    将地址空间限制为 32 位以模拟硬件。在 ARM 和 Alpha 上受支持。打开 `ADDR_LIMIT_32BIT`。

- `-L`, `--addr-compat-layout`  
    提供传统的虚拟地址空间布局。当 `program` 二进制文件没有 `PT_GNU_STACK` ELF 头时使用。打开 `ADDR_COMPAT_LAYOUT`。

- `-R`, `--addr-no-randomize`  
    禁用虚拟地址空间的随机化。打开 `ADDR_NO_RANDOMIZE`。

- `-X`, `--read-implies-exec`  
    如果设置了此项，则 `mmap(2)` 的 `PROT_READ` 也将添加 `PROT_EXEC` 位——如传统 x86 二进制文件所预期。请注意，ELF 加载器在遇到传统二进制文件时会自动设置此位。打开 `READ_IMPLIES_EXEC`。

- `-Z`, `--mmap-page-zero`  
    SVr4 错误模拟，将 `mmap(2)` 的零页设置为只读。当 `program` 依赖此行为且源代码不可用于修复时使用。打开 `MMAP_PAGE_ZERO`。

### dmesg - 打印或控制内核环形缓冲区

`dmesg [ -c ] [ -n level ] [ -s bufsize ]`

dmesg 用于检查或控制内核环形缓冲区。

- `-W, --follow-new`
	等待并打印新信息

例：
- 查看内核保护状态

	```sh
	dmesg | grep -Ei 'NX|execute disable|SMEP|SMAP|KPTI'
	[    0.000000] NX (Execute Disable) protection: active
	```

### insmod - 一个简单的程序，用于将模块插入 Linux 内核

`insmod [OPTIONS] [filename] [module options]`

insmod 是一个简单的程序，用于将模块插入内核。
大多数用户会选择使用 modprobe(8) 来代替，因为它更聪明，并且能够处理模块依赖。

只有最通用的错误消息会被报告：由于尝试链接模块的工作现在是在内核内部完成的，因此 dmesg(1) 通常会提供更多关于错误的信息。

### lsmod - 显示 Linux 内核中模块的状态

`lsmod [OPTIONS]`

lsmod 是一个简单的程序，它可以很好地格式化 /proc/modules 的内容，显示当前加载的内核模块。


### rmmod - 一个简单的程序，用于从 Linux 内核中移除模块

`rmmod [OPTIONS] [list of modulenames]`

rmmod 是一个简单的程序，用于从内核中移除一个模块或多个模块（当提供模块卸载支持时）。大多数用户会选择使用带 -r 选项的 modprobe(8)，因为它还会移除未使用的依赖模块。

当提供模块列表时，程序将逐个处理它们。如果某个模块未找到，rmmod 会立即退出并返回错误代码。如果模块移除失败，程序将记录一个错误，并继续处理下一个模块。这种行为不受 --force 选项控制。

### htop - 查看实时的进程、cpu、内存状态

## 进程

### strace — 跟踪系统调用和信号

https://www.man7.org/linux/man-pages/man1/strace.1.html

```sh
strace [-ACdffhikkqqrtttTvVwxxyyYzZ] [-a column] [-b execve]
       [-e expr]... [-I n] [-o file] [-O overhead] [-p pid]...
       [-P path]... [-s strsize] [-S sortby] [-U columns]
       [-X format] [--seccomp-bpf]
       [--stack-trace-frame-limit=limit] [--syscall-limit=limit]
       [--secontext[=format]] [--tips[=format]] { -p pid | [-DDD]
       [-E var[=val]]... [-u username] command [args] }

strace -c [-dfwzZ] [-b execve] [-e expr]... [-I n] [-O overhead]
       [-p pid]... [-P path]... [-S sortby] [-U columns]
       [--seccomp-bpf] [--syscall-limit=limit] [--tips[=format]] {
       -p pid | [-DDD] [-E var[=val]]... [-u username] command
       [args] }

strace --tips[=format]
```

在最简单的用法中，`strace` 运行指定的 `command` 直到其退出。它会拦截并记录进程发起的系统调用，以及进程接收到的信号。每个系统调用的名称、参数和返回值会打印到标准错误，或打印到由 `-o` 选项指定的文件。

```sh
# 输出摘要
strace -c testa.py

# 跟踪 write，输出摘要
strace -e write -c testa.py
```

#### 选项

##### 常规

- `-e expr`  
    通过指定限定表达式来修改要跟踪的事件或跟踪方式。表达式格式为：

    ```sh
    [qualifier=][!]value[,value]...
    ```

    其中 `qualifier` 是 `trace`（或 `t`）、`trace-fds`（或 `trace-fd`、`fd`、`fds`）、`abbrev`（或 `a`）、`verbose`（或 `v`）、`raw`（或 `x`）、`signal`（或 `signals`、`s`）、`read`（或 `reads`、`r`）、`write`（或 `writes`、`w`）、`fault`、`inject`、`status`、`quiet`（或 `silent`、`silence`、`q`）、`secontext`、`decode-fds`（或 `decode-fd`）、`decode-pids`（或 `decode-pid`）或 `kvm` 之一，`value` 是依赖于限定符的符号或数字。默认限定符是 `trace`。使用感叹号会否定值集合。例如，`-e open` 等价于 `-e trace=open`，意思是只跟踪 `open` 系统调用。相反，`-e trace=!open` 表示跟踪除 `open` 之外的每个系统调用。此外，特殊值 `all` 和 `none` 可分别用于跟踪每个事件或不跟踪任何事件。

    注意，某些 shell 即使在带引号的参数中也会使用感叹号进行历史扩展。在这种情况下，必须用反斜杠转义感叹号。


### 统计

- 
    ```
    -c
    --summary-only
    ```
    统计每个系统调用的时间、调用次数和错误数，并在程序退出时报告摘要，同时抑制常规输出。这会显示系统时间（在内核中花费的 CPU 时间），它与墙上时钟时间无关。如果 `-c` 与 `-f` 一起使用，则只保留所有被跟踪进程的聚合总计。

### watch - 定期执行程序，全屏显示输出

https://man7.org/linux/man-pages/man1/watch.1.html

```sh
watch [option ...] command
```

`watch` 重复运行 `command`，显示其输出和错误（第一屏内容）。这允许你观察程序输出随时间的变化。默认情况下，`command` 每 2 秒运行一次，`watch` 将一直运行直到被中断。标题栏会显示 `command` 的启动时间、运行时间以及退出码。

```sh
# 特权 shell 1：exec 外侧 sh -p 传递特权，内侧 sh -p 继承特权 shell
watch -x /bin/sh -p -c 'reset; /bin/sh -p 1>&0 2>&0'

# 特权 shell 2：设置当前 id 为 root，并启动特权 shell
watch -x /bin/sh -p -c 'reset; setpriv --clear-groups --regid 0 --reuid 0 /bin/sh 1>&0 2>&0'
watch -x setpriv --clear-groups --regid 0 --reuid 0 /bin/sh -c 'reset; /bin/sh 1>&0 2>&0'
watch -x chroot --userspec=root:root / /bin/sh -c 'reset; /bin/sh 1>&0 2>&0'

# 特权 shell 3：使用不降权的 shell
watch -x zsh -c 'reset; zsh 1>&0 2>&0'

# 无特权 shell：外侧 sh -c 丢失特权
watch 'reset; /bin/sh 1>&0 2>&0'
```

- `-c`, `--color`  
    解释 ANSI 颜色和样式序列。

- `-C`, `--no-color`  
    不解释 ANSI 颜色和样式序列。

- `-x`, `--exec`  
    将 `command` 传递给 `exec(3)` 调用而不是 `sh -c`。程序将启动得更快。Shell 功能（环境设置、变量和路径名展开等）将不可用。

### stdbuf - 运行 `COMMAND`，并修改其标准流的缓冲操作。

```sh
stdbuf OPTION... COMMAND
```
运行 `COMMAND`，并修改其标准流的缓冲操作。

```sh
stdbuf -i0 -o0 -e0 /bin/sh -p
```

- `-i, --input=MODE`  
    调整标准输入流缓冲

- `-o, --output=MODE`  
    调整标准输出流缓冲

- `-e, --error=MODE`  
    调整标准错误流缓冲

如果 `MODE` 为 `L`，则相应流将采用行缓冲。此选项对标准输入无效。

如果 `MODE` 为 `0`，则相应流将不缓冲。

### timeout - 运行带时间限制的命令

https://man7.org/linux/man-pages/man1/timeout.1.html

```sh
timeout [OPTION]... DURATION COMMAND [ARG]...
```

启动 `COMMAND`，如果它在 `DURATION` 之后仍在运行，则将其杀死。

```sh
# 交互 shell
timeout 0 /bin/sh -p
```

### nice - 以修改后的调度优先级运行程序

```sh
nice [OPTION] [COMMAND [ARG]...]
```

以调整后的 niceness 运行 `COMMAND`，这会影响进程调度。没有 `COMMAND` 时，打印当前 niceness。niceness 值范围为 `-20`（对进程最有利）到 `19`（对进程最不利）。

```sh
# 交互 shell
nice /bin/sh -p
```

- `-n, --adjustment=N`  
    将整数 `N` 加到 niceness 上（默认 `10`）

### ps - 报告当前进程的快照

https://www.man7.org/linux/man-pages/man1/ps.1.html

```sh
ps [选项]
```

`ps` 显示关于部分活动进程的信息

- `-o` 选项启用自定义 `stat` 列
	- `T`  表示进程因 `Ctrl-Z` 操作而被挂起
	- `S` 表示其正在等待输入时处于睡眠状态
	- `R` 表示该进程正在活跃运行
	- `+` 号代表其处于前台

**“标准”语法：** 在这种语法中，你可以使用 `-e` 列出“每个”进程，使用 `-f` 获得“完整格式”输出，包括参数。这些可以合并为单个参数 `-ef`。

**“BSD”语法：** 在这种语法中，你可以使用 `a` 列出所有用户的进程，使用 `x` 列出不在终端中运行的进程，使用 `u` 获得“用户可读”的输出。这些可以合并为单个参数 `aux`。

`ps -ef` 和 `ps aux` 都会将命令列表截断到终端的宽度。如果你无法读取进程的完整路径，可能需要放大终端（或将输出重定向到某处以避免这种截断行为）。或者，你可以传入 `w` 选项*两次*（例如 `ps -efww` 或 `ps auxww`）来禁用截断。

示例
```sh
# 读取进程信息并禁用截断
ps auxww
```

### kill —— 向指定的进程或进程组发送指定的信号

https://www.man7.org/linux/man-pages/man1/kill.1.html

```sh
kill  [-signal|-s signal|-p]  [-q value] [-a] [--timeout
milliseconds signal] [--] PID[:_inode_]...

kill  [-signal|-s signal] PID[:_inode_]...

kill -l [number|0xsigmask] | -L

kill -d PID[:_inode_]
```

如果未指定信号，则发送 `TERM` 信号。该信号的默认动作是终止进程。进程可为 `TERM` 信号安装处理程序，以便在有序终止之前执行清理步骤。

`KILL` 信号（编号 9），无法被捕获，因此不会给目标进程在终止前执行任何清理的机会。

- `-s, --signal signal`  
    要发送的信号。参数值为名称或编号。

- `-l, --list [number|0xsigmask]`  
    打印信号名称列表，将给定的信号编号转换为名称，或将给定的信号掩码转换为名称。信号信息在 `/usr/include/linux/signal.h`

```sh
# 发送强制终止信号
kill -s 9 目标进程
```

## 用户

### unshare - 在新命名空间中运行程序

https://www.man7.org/linux/man-pages/man1/unshare.1.html

```sh
unshare [options] [program [arguments]]
```

`unshare` 命令创建新的命名空间（如下文所述命令行选项所指定），然后执行指定的 `program`。如果未给出 `program`，则运行 `${SHELL}`。如果未设置 `SHELL`，则使用用户 `passwd(5)` 条目中的 shell。如果那里也未定义 shell，则使用 `/bin/sh` 作为后备。

```sh
# 待测试，在命名空间内设置 id 为 root 的 交互式 shell
unshare -Urm /bin/sh
```

- `-m`, `--mount[=file]`  
    创建新的 mount 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。注意 `file` 必须位于传播类型不是 `shared` 的挂载上（否则会产生错误）。当不确定当前设置时，使用命令 `findmnt -o+PROPAGATION`。另请参见下面的示例。

- `-U`, `--user[=file]`  
    创建新的 user 命名空间。如果指定了 `file`，则通过在 `file` 处创建 bind mount 使命名空间持久化。

- `-r`, `--map-root-user`  
    仅在当前有效用户和组 ID 已映射到新创建的 user 命名空间中的超级用户 UID 和 GID 之后运行程序。这使得即使以非特权方式运行，也可以方便地获得管理新创建命名空间各个方面所需的能力（例如在网络命名空间中配置接口或在 mount 命名空间中挂载文件系统）。作为便利功能，它不支持更复杂的用例，例如映射多个 UID 和 GID 范围。此选项隐含 `--setgroups=deny` 和 `--user`。此选项等效于 `--map-user=0 --map-group=0`。


### chroot - 以特殊的根目录运行命令或交互式 shell ⚔️

```sh
chroot [OPTION]... NEWROOT [COMMAND [ARG]...]
```

以根目录设置为 `NEWROOT` 运行 `COMMAND`。
> 判断 euid，可设置 ruid

```sh
# 修改真实用户与组 id 到 root，启动特权 shell
chroot --userspec=root:root / /bin/sh
```

- `--groups=G_LIST`  
    以 `g1,g2,..,gN` 指定补充组

- `--userspec=USER:GROUP`  
    指定要使用的用户和组（ID 或名称）

- `--skip-chdir`  
    不将工作目录更改为 `/`

### runuser - 以替代用户和组 ID 运行命令

```sh
runuser [options] -u user [[--] command [argument...]]

runuser [options] [-] [user [argument...]]
```

`runuser` 可用于以替代用户和组 ID 运行命令。如果未给出 `-u` 选项，`runuser` 回退到与 `su` 兼容的语义并执行 shell。`runuser` 与 `su` 命令的区别在于 `runuser` 不询问密码（因为它只能由 root 用户执行），并且使用不同的 PAM 配置。`runuser` 命令不必以 set-user-ID 权限安装。

不带参数调用时，`runuser` 默认以 `root` 身份运行交互式 shell。

> 判断 ruid

### sudo —— 以其他用户的身份执行命令

[官网文档](https://www.sudo.ws/)
[linux 手册](https://man7.org/linux/man-pages/man8/sudo.8.html)

```sh
sudo -h | -K | -k | -V
sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]
sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user] [-u user]
    [command [arg ...]]
sudo [-ABbEHnPS] [-C num] [-D directory] [-g group] [-h host] [-p prompt]
    [-R directory] [-T timeout] [-u user] [VAR=value] [-i | -s]
    [command [arg ...]]
sudoedit [-ABkNnS] [-C num] [-D directory] [-g group] [-h host] [-p prompt]
    [-R directory] [-T timeout] [-u user] file ...
```

`sudo` 允许被许可的用户以超级用户或安全策略指定的其他用户身份执行 `command`。调用用户的实际（*而非*有效）用户 ID 用于确定查询安全策略时使用的用户名。
> 判断 ruid

`sudo` 默认以 `root` 身份运行命令.  
`sudo` 通过检查策略来确定用户是否被授权以 `root` 身份运行命令。这些策略在 `/etc/sudoers` 文件中定义（似乎此文件本身即需要 root 权限读取）

示例
```sh
sudo bash -c "多条命令"
```
- sudo 后执行一条命令，若尝试执行复杂操作，最简单的是开启子进程 shell

参数
- `-u 用户名` 切换到用户后运行
- `-l, --list`

	- 如果未指定命令，则列出调用用户（或由 `-U` 选项指定的用户）在当前主机上的权限。若指定 `-ll`，且安全策略支持详细输出格式，则会采用更长的列表格式。

	- 如果指定了命令，且安全策略允许调用用户（或由 `-U` 选项指定的用户）在当前主机上执行该命令，则会显示该命令的完全限定路径及其所有参数。若指定 `-ll`（且安全策略支持），则会以详细格式显示匹配规则以及该命令。如果指定了命令但策略不允许，`sudo` 将以状态值 1 退出。

- `-s`, `--shell`  
    如果设置了 `SHELL` 环境变量，则运行它指定的 shell；否则运行调用用户密码数据库条目指定的 shell。如果指定了 `command`，则使用 `-c` 选项将其作为简单命令传递给 shell。`command` 和任何 `arg` 在将每个字符（包括空白）用反斜杠（`\`）转义后（字母数字、下划线、连字符和美元符号除外）用空格连接。如果未指定 `command`，则执行交互式 shell。大多数 shell 在指定 `command` 时与交互式会话相比行为不同；详情请查阅 shell 手册。

### setpriv - 以不同的 Linux 权限设置运行程序 ⚔️

```sh
setpriv [options] program [arguments]
```

设置或查询各种跨 `execve(2)` 继承的 Linux 权限设置。
> 判断 euid，可设置 ruid

```sh
# 修改真实用户与组 id 到 root，启动特权 shell
setpriv --clear-groups --regid 0 --reuid 0 /bin/sh
```

- `--rgid gid`, `--egid gid`, `--regid gid`  
    设置实际、有效或两者的 GID。`gid` 参数可以作为文本组名给出。

    为安全起见，如果设置任何主 `gid`，你必须指定 `--clear-groups`、`--groups`、`--keep-groups` 或 `--init-groups` 之一。

- `--ruid uid`, `--euid uid`, `--reuid uid`  
    设置实际、有效或两者的 UID。`uid` 参数可以作为文本登录名给出。

    设置 `uid` 或 `gid` 不会更改能力，尽管最后的 exec 调用可能会更改能力。这意味着，如果你是 root，你可能想执行类似以下操作：

    ```sh
    setpriv --reuid=1000 --regid=1000 --inh-caps=-all
    ```

### su - 以替代的用户和组 ID 执行命令

https://www.man7.org/linux/man-pages/man1/su.1.html

```sh
su [OPTION]... [-] [USER [ARG]...]
```

切换至目标 USER  
单独使用 `-` 表示 `-l`。
如果未给出 USER，则假设为 root。

`su` 是一个 `root` 身份的 setuid 二进制文件。在允许用户提权到 `root` 之前，它会检查用户是否知道 `root` 密码

参数
- `-c` 执行命令

## 文件目录操作

> 文件覆盖/移除时，检查目录权限，而非文件


### basename - 从文件名中去除目录和后缀

https://www.man7.org/linux/man-pages/man1/basename.1.html

```sh
basename NAME [SUFFIX]
basename OPTION... NAME...
```

打印 `NAME`，并移除任何前导目录组件。如果指定，还会移除末尾的 `SUFFIX`。

- `-a, --multiple`  
    支持多个参数，并将每个参数视为一个 `NAME`

- `-s, --suffix=SUFFIX`  
    移除末尾的 `SUFFIX`；隐含 `-a`

- `-z, --zero`  
    以 `NUL` 而不是换行结束每个输出行

```console
$ basename /usr/bin/sort
sort

$ basename include/stdio.h .h
stdio

$ basename -s .h include/stdio.h
stdio

$ basename -a any/str1 any/str2
str1
str2
```

### dirname - 从文件名中去除最后一个组件

https://www.man7.org/linux/man-pages/man1/dirname.1.html

```sh
dirname [OPTION] NAME...
```

输出每个 `NAME`，移除其最后一个非斜杠组件及末尾斜杠；如果 `NAME` 不含 `/`，则输出 `'.'`（表示当前目录）。

- `-z, --zero`  
    以 `NUL` 而不是换行结束每个输出行

```console
$ dirname /usr/bin/
/usr

$ dirname dir1/str dir2/str
dir1
dir2

$ dirname stdio.h
.
```

### file - 确定文件类型

https://www.man7.org/linux/man-pages/man1/file.1.html

```sh
file [-bcdEhiklLNnprsSvzZ0] [--apple] [--exclude-quiet]
[--extension] [--mime-encoding] [--mime-type] [-e testname]
[-F separator] [-f namefile] [-m magicfiles] [-P name=value]
file ... file -C [-m magicfiles] file [--help]
```

`file` 会尝试对每个参数进行分类。测试分为三组，按以下顺序执行：文件系统测试、魔数测试和语言测试。第一个成功的测试会导致文件类型被打印出来。

### find - 在目录层次结构中搜索文件

https://www.man7.org/linux/man-pages/man1/find.1.html

https://www.gnu.org/software/findutils/manual/html_node/index.html

```sh
find [path...] [expression]
```

如果未指定搜索条件，`find` 将匹配所有文件。  
如果未指定搜索位置，`find` 将使用当前工作目录（`.`）。  

参数：
- `-P`  
	永不跟随符号链接。这是默认行为。
- `-L`  
	跟随符号链接。
- `-H`  
	不要跟随符号链接，除非在处理命令行参数时。

表达式：
- `!` 
  非（注意转义）
- `-name pattern`   
	基础文件名匹配 pattern
- `-type [类型]`  
	- `d` 目录  
	- `f` 普通文件  
	- `l` 符号链接  
	- `p` 命名管道  
	- `s` 套接字  

- `-quit`  
	立即退出。
- `-readable`  
  匹配当前用户可读的文件。
- `-prune True`  
  如果文件是目录，则不要进入其中。

- `-print True`
  在标准输出上打印完整的文件名，后跟换行符。

GLOBAL OPTIONS
- `-ignore_readdir_race`
  通常情况下，`find` 在无法统计文件时会发出错误消息。如果你指定了此选项，并且在 `find` 从目录中读取文件名与尝试统计该文件之间的时间内，文件被删除，则不会显示任何错误消息。
- `-maxdepth levels`  
	最多向下遍历命令行参数指定的目录层数（一个非负整数）。-maxdepth 0 表示仅对命令行参数应用测试和操作。

运算符
- `expr1 expr2`
  and; 若表达式1为假，则不计算表达式2
- `expr1 -o expr2`   
  or; 如果 expr1 为真，则不计算 expr2。

操作：
- `-exec command`
	执行 command；如果返回 0 状态则返回 true。
	find 的所有后续参数被视为 command 的参数，直到遇到一个由 `;` 或 `+` 组成的参数为止。（在shell中需对分号进行转义或引号包裹为字面量）
	在 command 的参数中，字符串 `{}` 将被当前正在处理的文件名替换，而不仅仅是在单独的参数中

示例

```sh
# 在根目录下查找，忽略竞争条件文件
# 若不可读，则跳过文件与目录
# 否则对于文件名为 flag 且类型不为目录的文件：输出文件名，并调用 grep 打印目标字符串。若 grep 成功则退出（ grep 成功时返回0，对应 -exec 返回 true，于是继续 -quit）
find / -ignore_readdir_race \
  '!' -readable -prune \
  -o \
  -name flag '!' -type d -print -exec grep 'pwn' {} ';' -quit

# 交互 shell
find . -exec /bin/sh -p \;
```

### mkfifo - 创建先进先出的命名管道

https://www.man7.org/linux/man-pages/man1/mkfifo.1.html

```bash
mkfifo [选项]... 名称...
```

使用指定的名称创建持久化命名管道（FIFO）。  
阻塞，读取前需写入，并且写入后阻塞到被读取为止。  
想象容量为1的栈，入栈后需出栈。

### ln （硬链接/软链接）

https://www.man7.org/linux/man-pages/man1/ln.1.html

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

- `-f, --force`  
    删除已存在的目标文件

- `-n, --no-dereference`  
    如果 `LINK_NAME` 是指向目录的符号链接，则将其视为普通文件
例：
```sh
# 创建目标文件的符号链接
ln -s /target_file symbol_link

# 创建目录的符号链接，若已存在则作为文件覆盖，而不是解析符号链接
ln -sfn /target_dir symbol_link
```

### mv - 移动/重命名文件

https://www.man7.org/linux/man-pages/man1/mv.1.html

```sh
mv [OPTION]... [-T] SOURCE DEST
mv [OPTION]... SOURCE... DIRECTORY
mv [OPTION]... -t DIRECTORY SOURCE...
```

将 `SOURCE` 重命名为 `DEST`，或移动 `SOURCE(s)` 到 `DIRECTORY`。 

### rm - 删除文件或目录

https://www.man7.org/linux/man-pages/man1/rm.1.html

```sh
rm [OPTION]... FILE...
```

`rm` 会删除每个指定的文件。默认情况下，它不会删除目录。

选项：
- `-f, --force`
	忽略遇到的任何错误（不存在的文件和参数），永不提示
- `-r, -R, --recursive`  
	递归删除目录及其包含的所有文件
- `--no-preserve-root`
	无 `/` 根目录保护

```sh
# 删除目录及其中所有内容
rm -rf 示例目录
```

### mkdir —— 创建目录

https://www.man7.org/linux/man-pages/man1/mkdir.1.html

```sh
mkdir [OPTION]... DIRECTORY...
```

如果目录不存在，则创建该目录（或多个目录）。

参数：
- `-p, --parents`  
    如果存在错误，则不报错，按需创建父目录（创建重复父目录不报错），其文件权限不受任何 -m 选项影响

### touch - 创建文件，或修改文件时间戳

https://www.man7.org/linux/man-pages/man1/touch.1.html

```sh
touch [OPTION]... FILE...
```

将每个文件的访问时间和修改时间更新为当前时间。 

如果未指定 `-c` 或 `-h` 参数，不存在的 `FILE` 参数将被创建为空文件。 

当 `FILE` 参数字符串为 `-` 时，将被特殊处理，导致 `touch` 命令更改与标准输出关联的文件的时间戳。

### cp —— 复制文件、创建软硬链接、覆盖删除、选择保留属性

https://www.man7.org/linux/man-pages/man1/cp.1.html

```sh
cp [OPTION]... [-T] SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
cp [OPTION]... -t DIRECTORY SOURCE...
```

将 SOURCE 复制到 DEST，或将 SOURCE(s) 复制到 DIRECTORY。

参数：
- `-R, -r, --recursive`   
	递归复制目录内容
- `--remove-destination`
	强制替换，先删除已存在的目标文件，然后创建一个全新的文件。
- ` -f 或 --force`
	强制覆盖，如果目标文件存在且无法被打开（例如权限不足），尝试删除它后再复制。
	如果目标文件可以被打开，尝试直接覆盖其内容。
- `--no-preserve=ATTR`
	丢弃属性，在复制时不保留指定的源文件属性。
	常用的属性包括 mode（权限）、ownership（所有者）、timestamps（时间戳）和 all（所有）。
- `-a, --archive`
	完全保留，保留源文件的所有属性，包括所有者、组、权限、时间戳和链接。


### mkdir - 创建目录

```bash
mkdir [OPTION]... DIRECTORY...
```

如果目录尚不存在，则创建这些 `DIRECTORY`。

- `-m, --mode=MODE`
  设置文件模式（如同 `chmod`），而不是 `a=rwx - umask`
- `-p, --parents`
  如果已存在则不报错，按需创建父目录，其文件模式不受任何 `-m` 选项影响
- `-v, --verbose`
  为每个创建的目录打印一条消息
- `-Z`
  将每个创建的目录的 SELinux 安全上下文设置为默认类型
- `--context[=CTX]`
  类似 `-Z`，或者如果指定了 `CTX`，则将 SELinux 或 SMACK 安全上下文设置为 `CTX`

### ls - 列出目录内容

https://www.man7.org/linux/man-pages/man1/ls.1.html

```bash
ls [OPTION]... [FILE]...
```

列出关于 `FILE` 的信息（默认当前目录）。如果未指定 `-cftuvSUX` 或 `--sort`，则按字母顺序排序条目。

- `-a, --all` 🛠️
  不忽略以 `.` 开头的条目。

- `-A, --almost-all`
  不列出隐含的 `.` 和 `..`。

- `--author`
  与 `-l` 一起使用时，打印每个文件的作者。

- `-b, --escape`
  对非图形字符打印 C 风格转义。

- `--block-size=SIZE`
  与 `-l` 一起使用时，打印大小时按 `SIZE` 缩放；例如 `--block-size=M`；参见下面的 `SIZE` 格式。

- `-c`
  与 `-lt` 一起使用时：按 `ctime`（文件状态信息最后更改时间）排序并显示 `ctime`；与 `-l` 一起使用时：显示 `ctime` 并按名称排序；否则：按 `ctime` 排序，最新在前。

- `-C`
  按列列出条目。

- `--color[=WHEN]` 🛠️
  按 `WHEN` 为输出着色；更多信息见下文。
    > 有时终端 ls 无色彩，添加 `--color=auto`

- `-d, --directory`
  列出目录本身，而不是其内容。

- `-D, --dired`
  生成为 Emacs 的 `dired` 模式设计的输出。

- `-f`
  等同于 `-a -U`。

- `-F, --classify[=WHEN]`
  按 `WHEN` 向条目追加指示符（`*/=>@|` 之一）。

- `--file-type`
  类似 `-F`，但不追加 `*`。

- `--format=WORD`
  使用 `WORD` 格式：`across`、`horizontal`（`-x`）、`commas`（`-m`）、`long`（`-l`）、`single-column`（`-1`）、`verbose`（`-l`）、`vertical`（`-C`）。

- `--full-time`
  类似 `-l --time-style=full-iso`。

- `-g`
  类似 `-l`，但不列出所有者。

- `--group-directories-first`
  将目录分组排在文件之前。

- `-G, --no-group`
  在长列表中，不打印组名。

- `-h, --human-readable`
  与 `-l` 和 `-s` 一起使用时，以类似 `1K`、`234M`、`2G` 等格式打印大小。

- `--si`
  同样如此，但使用 1000 的幂而不是 1024。

- `-H, --dereference-command-line`
  跟随命令行中列出的符号链接。

- `--dereference-command-line-symlink-to-dir`
  跟随命令行中每个指向目录的符号链接。

- `--hide=PATTERN`
  不列出匹配 shell `PATTERN` 的隐含条目（会被 `-a` 或 `-A` 覆盖）。

- `--hyperlink[=WHEN]`
  按 `WHEN` 为文件名添加超链接。

- `--indicator-style=WORD`
  向条目名称追加样式为 `WORD` 的指示符：`none`（默认）、`slash`（`-p`）、`file-type`（`--file-type`）、`classify`（`-F`）。

- `-i, --inode`
  打印每个文件的索引号。

- `-I, --ignore=PATTERN`
  不列出匹配 shell `PATTERN` 的隐含条目。

- `-k, --kibibytes`
  文件系统使用量默认使用 1024 字节块；仅与 `-s` 和每个目录总计一起使用。

- `-l` 🛠️
  使用长列表格式。

- `-L, --dereference`
  当显示符号链接的文件信息时，显示该链接所引用文件的信息，而不是链接本身的信息。

- `-m`
  用逗号分隔的条目列表填满宽度。

- `-n, --numeric-uid-gid`
  类似 `-l`，但列出数字用户 ID 和组 ID。

- `-N, --literal`
  打印条目名称时不加引号。

- `-o`
  类似 `-l`，但不列出组信息。

- `-p, --indicator-style=slash`
  向目录追加 `/` 指示符。

- `-q, --hide-control-chars`
  用 `?` 代替非图形字符打印。

- `--show-control-chars`
  原样显示非图形字符；这是默认行为，除非程序是 `ls` 且输出是终端。

- `-Q, --quote-name`
  将条目名称括在双引号中。

- `--quoting-style=WORD`
  对条目名称使用引号样式 `WORD`：`literal`、`locale`、`shell`、`shell-always`、`shell-escape`、`shell-escape-always`、`c`、`escape`（覆盖 `QUOTING_STYLE` 环境变量）。

- `-r, --reverse`
  排序时反转顺序。

- `-R, --recursive` 🛠️
  递归列出子目录。
  > 但通常使用命令 `tree` 格式化递归显示

- `-s, --size`
  以块为单位打印每个文件的分配大小。

- `-S`
  按文件大小排序，最大在前。

- `--sort=WORD`
  将默认的 `name` 排序改为 `WORD`：`none`（`-U`）、`size`（`-S`）、`time`（`-t`）、`version`（`-v`）、`extension`（`-X`）、`name`、`width`。

- `--time=WORD`
  选择用于显示或排序的时间戳；访问时间（`-u`）：`atime`、`access`、`use`；元数据更改时间（`-c`）：`ctime`、`status`；修改时间（默认）：`mtime`、`modification`；创建时间：`birth`、`creation`；与 `-l` 一起使用时，`WORD` 决定显示哪个时间；与 `--sort=time` 一起使用时，按 `WORD` 排序（最新在前）。

- `--time-style=TIME_STYLE`
  与 `-l` 一起使用的时间/日期格式；参见下面的 `TIME_STYLE`。

- `-t`
  按时间排序，最新在前；参见 `--time`。

- `-T, --tabsize=COLS`
  假定制表符停靠点为每 `COLS` 列，而不是 8。

- `-u`
  与 `-lt` 一起使用时：按访问时间排序并显示访问时间；与 `-l` 一起使用时：显示访问时间并按名称排序；否则：按访问时间排序，最新在前。

- `-U`
  不排序目录条目。

- `-v`
  对文本中的（版本）数字进行自然排序。

- `-w, --width=COLS`
  将输出宽度设置为 `COLS`。`0` 表示不限制。

- `-x`
  按行列出条目，而不是按列。

- `-X`
  按条目扩展名字母顺序排序。

- `-Z, --context`
  打印每个文件的任何安全上下文。

- `--zero`
  以 `NUL` 而不是换行结束每个输出行。

- `-1`
  每行列出一个文件。

`SIZE` 参数是一个整数和可选单位（例如：`10K` 表示 `10*1024`）。单位有 `K,M,G,T,P,E,Z,Y,R,Q`（1024 的幂）或 `KB,MB,...`（1000 的幂）。也可以使用二进制前缀：`KiB=K`、`MiB=M`，等等。

`TIME_STYLE` 参数可以是 `full-iso`、`long-iso`、`iso`、`locale` 或 `+FORMAT`。`FORMAT` 的解释方式与 `[date(1)]` 中相同。如果 `FORMAT` 为 `FORMAT1<newline>FORMAT2`，则 `FORMAT1` 适用于非近期文件，`FORMAT2` 适用于近期文件。以 `posix-` 为前缀的 `TIME_STYLE` 仅在 POSIX locale 外生效。此外，`TIME_STYLE` 环境变量设置要使用的默认样式。

`WHEN` 参数默认为 `always`，也可以是 `auto` 或 `never`。

使用颜色区分文件类型在默认情况下以及使用 `--color=never` 时均被禁用。使用 `--color=auto` 时，仅当标准输出连接到终端时，`ls` 才发出颜色代码。`LS_COLORS` 环境变量可以更改设置。使用 `[dircolors(1)]` 命令进行设置。

**退出状态：**

- `0`
  如果正常。

- `1`
  如果存在轻微问题（例如无法访问子目录）。

- `2`
  如果存在严重问题（例如无法访问命令行参数）。

### du - 估计文件空间使用情况

https://www.man7.org/linux/man-pages/man1/du.1.html

```sh
du [OPTION]... [FILE]...
du [OPTION]... --files0-from=F
```

递归汇总一组文件的设备使用情况，包括目录。

- `-c`, `--total`  
    整合为总大小
	
- `-h, --human-readable`  
	以人类可读的格式打印大小（例如，1K 234M 2G）

- `-s, --summarize`
    仅显示每个参数的总数
    
## 系统

### systemctl - 控制 systemd 系统和服务管理器  

```sh
systemctl [OPTIONS...] COMMAND [UNIT...]
```

**描述**  
`systemctl` 可用于检查和控制 "systemd" 系统和服务管理器的状态。有关此工具所管理的基本概念和功能的介绍，请参阅 systemd(1)。

常用命令
```sh
# 启动服务
systemctl start 服务

# 启用并启动服务
systemctl enable --now 服务

# 查看服务状态
systemctl status 服务
```

## 文件浏览

### more - 在终端中显示文件内容

https://www.man7.org/linux/man-pages/man1/more.1.html

```sh
more [options] file ...
```

逐屏分页浏览文本的过滤器。这个版本特别原始。

```sh
# 交互 shell
more /etc/hosts
# 输入 shell 命令，`!/bin/sh`
```

- `!command or :!command`  
    在子shell中执行命令。

### less - 在终端中显示文件内容

https://www.man7.org/linux/man-pages/man1/less.1.html

```sh
less [-[+]aABcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX~] [-b size] [-D color]
      [-h lines] [-j line] [-k key-file] [-{o|O} log-file]
      [-p pattern ] [-P prompt] [-t tag] [-T tags-file]
      [-x tab[{,tab}...]] [-y lines] [-z lines] [-lines] [-"cc]
      [-# shift] [+less-command] [--] [file ...]
```

逐屏分页浏览文本的过滤器，但允许在文件中向前和向后移动。
此外，不需要在开始前读取整个输入文件，因此对于大型输入文件，它比文本编辑器（如）启动更快。

```sh
# 交互 shell
less /etc/hosts
# 输入 shell 命令，`!/bin/sh`
```

```sh
# 交互 shell
VISUAL='/bin/sh -s --' less /etc/hosts
VISUAL='/bin/sh </dev/tty >/dev/tty 2>/dev/tty #' less /etc/hosts
# 输入 shell 命令，`v`
```

```sh
# 交互 shell
LESSOPEN="/bin/sh -s 1>&0 2>&0 - %s" less /etc/hosts
LESSOPEN='/bin/sh </dev/tty >/dev/tty 2>/dev/tty # %s' less /etc/hosts
```

命令

- `v`  
    调用编辑器来编辑当前正在查看的文件。 编辑器将从环境变量 `VISUAL` 中获取

- `! shell-command`  
    调用一个 shell 来执行指定的 shell 命令。

- `# shell-command`  
    类似于 `!` 命令，只是该命令的展开方式与提示字符串相同。

输入预处理器

- `LESSOPEN="lessopen.sh %s"`  
    设置被执行的输入预处理器

## 终端

### tset、reset - 初始化或重置终端状态

https://man7.org/linux/man-pages/man1/reset.1.html

```sh
tset [-IQVcqrsw] [-] [-e ch] [-i ch] [-k ch] [-m mapping]
[terminal-type]
reset [-IQVcqrsw] [-] [-e ch] [-i ch] [-k ch] [-m mapping]
[terminal-type]
```

首先，`tset` 检索你终端的当前终端模式设置。

接下来，`tset` 确定你正在使用的终端类型。

当以 `reset` 调用时，`tset` 会在执行上述终端初始化之前，将终端模式设置为 “sane” 值

### Screen

https://www.man7.org/linux/man-pages/man1/screen.1.html

```sh
screen [ -options ] [ cmd [ args ] ]
screen -r [[pid.]tty[.host]]
screen -r sessionowner/[[pid.]tty[.host]]
```
Screen 是一个全屏窗口管理器，可以在多个进程（通常是交互式 shell）之间切换终端。  
当 screen 被调用时，它会创建一个包含 shell（或指定的命令）的单个窗口，然后退出以便你可以像平常一样使用该程序。

当你的命令行使用完毕后，输入 `exit` 或按 `Ctrl-D` 离开 `screen` 会话。然后 `screen` 将终止，并把你返回到*原始* shell。

按下 `Ctrl-A`，然后按 `d`（表示 detach）即可分离。这会让你返回普通终端，同时你的会话继续在后台运行。

要重新连接会话，使用 `screen -r`

在单个 `screen` 会话中，可拥有多个窗口，窗口通过不同的键盘快捷键处理

参数
- 
  ```
  -ls [match]
  -list [match]
  ```
  列出所有终端，打印 PID 与名称（可用来作为 `-r` 参数重新连接）

- 
  ```
  -r [pid.tty.host]
  -r sessionowner/[pid.tty.host]
  ```
  恢复一个已分离的screen会话

快捷键，在默认配置中，`screen` 使用 `Ctrl-A` 激活快捷键：

- `Ctrl-A d`
  分离

- `Ctrl-A c`  
  创建新窗口

- `Ctrl-A n`  
  下一个窗口

- `Ctrl-A p`  
  上一个窗口

- `Ctrl-A 0` 到 `Ctrl-A 9`  
  直接跳转到窗口 0-9

- `Ctrl-A "`  
  调出所有窗口的选择菜单


### tmux - 终端复用

https://www.man7.org/linux/man-pages/man1/tmux.1.html

```sh
tmux [-28lquvV] [-c shell-command] [-f file] [-L socket-name] [-S socket-path] [command [flags]]
```

tmux 是一个终端复用器：它允许创建、访问和控制多个终端，所有这些终端都可以从单个屏幕进行管理。tmux 可以从屏幕中分离出来，在后台继续运行，稍后可以重新附加到屏幕上。

命令：

- 
  ```
  tmux new-session [-s 会话名]
  tmux new [-s 会话名]
  ```
  创建新（命名）会话

- `tmux ls`  
  列出会话

- 
  ```
  tmux attach [-t 会话名]
  tmux a [-t 会话名]
  ```  
  重新连接到会话

快捷键，tmux 使用 `Ctrl-B` 激活快捷键
- `Ctrl-B d`  
  分离会话到后台，回到终端

- `Ctrl-B [`  
  进入复制模式，可使用键盘的上下页与箭头
	- `q` 退出复制模式

窗口快捷键
- `Ctrl-B c`  
  创建新窗口

- `Ctrl-B n`  
  下一个窗口

- `Ctrl-B p`  
  上一个窗口

- `Ctrl-B 0` 到 `Ctrl-B 9`  
  跳转到窗口 0-9

- `Ctrl-B w`  
  查看一个漂亮的窗口选择器

窗格快捷键（1个窗口内多个窗格）
- `Ctrl-B 方向键`  
  切换窗格 
  
- `Ctrl-B %`  
  左右分屏 

- `Ctrl-B "`  
  上下分屏 

- `Ctrl-B z`  
  暂时放大当前窗格、还原 

- `Ctrl-B Ctrl+方向键`  
  调整窗格大小

配置文件
- `~/.tmux.conf`  

## 文本编辑器

### emacs - 文本编辑器

https://linux.die.net/man/1/emacs

https://www.gnu.org/software/emacs/manual/html_node/emacs/index.html
- [选项索引](https://www.gnu.org/software/emacs/manual/html_node/emacs/Option-Index.html)


```sh
emacs [ command-line switches ] [ files ... ] 
```

核心在于内置的 Emacs Lisp (Elisp) 编程语言。用户可以通过编写 Elisp 脚本或安装插件，实现几乎任何功能，包括编程、编译、调试、邮件收发、新闻阅读、文件管理、版本控制甚至浏览网页

```sh
# 交互式输入命令
emacs --eval '(shell)'

# 交互式输入命令，提供完整的终端模拟
emacs --eval '(term "/bin/sh")'
```

> 见 [40 从 Emacs 运行 Shell 命令](https://www.gnu.org/software/emacs/manual/html_node/emacs/Shell.html)


#### Emacs 选项

以下选项具有普遍意义：

- `file`  
    编辑 `file`。

- `--file file`、`--find-file file`、`--visit file`  
    与直接将 `file` 作为参数指定相同。

- `-q`、`--no-init-file`  
    不加载初始化文件。

- `--no-site-file`  
    不加载站点范围的启动文件。

- `--no-splash`  
    启动时不显示启动画面。

- `-Q`、`--quick`  
    等同于 `-q --no-site-file --no-splash`。

- `--eval expr`、`--execute expr`  
    求值 Lisp 表达式 `expr`。

#### 在 X 下使用 Emacs

- `-nw`、`--no-window-system`  
    告诉 `Emacs` 不要使用其特殊的 X 接口。如果你从 `xterm(1)` 窗口调用 `Emacs` 时使用此开关，显示会在该窗口中完成。

### nano - 文本编辑器

https://www.nano-editor.org/dist/latest/nano.1.html

```sh
nano [options] [[+line[,column]] file]...

nano [options] [[+[crCR]{/|?}string] file]...
```

小巧的编辑器

```sh
# 交互 shell
nano -s '/bin/sh'
# 进入编辑器后输入任意之后被作为 sh 参数的内容 `/bin/sh`
# 最后使用拼写检查快捷键 `^T` 触发
```

```sh
nano
# `^R` 读取文件
# `^E` 执行命令
sh -s 1>&0 2>&0
```

- `-s "program [argument ...]"`, `--speller="program [argument ...]"`  
    使用此命令执行拼写检查和纠正，而不是使用调用 `hunspell(1)` 或 `spell(1)` 的内置纠正器。

- `-/`, `--modernbindings`  
    使用类似于大多数现代程序的键绑定：`^X` 剪切，`^C` 复制，`^V` 粘贴，`^Z` 撤销，`^Y` 重做，`^F` 向前搜索，`^G` 搜索下一个，`^S` 保存，`^O` 打开文件，`^Q` 退出，并且（当终端允许时）`^H` 显示帮助。此外，`^A` 设置标记，`^B` 向后搜索，`^D` 搜索上一个，`^R` 进行替换，`^P` 显示位置，`^T` 转到某行，`^W` 写出文件，`^E` 执行命令。注意此选项会覆盖选项 `-p`（`--preserve`）。


## 文件内容与字符串操作

### split - 将文件分割成多个片段

https://man7.org/linux/man-pages/man1/split.1.html

```sh
split [OPTION]... [FILE [PREFIX]]
```

将文件的输出写入 PREFIXaa、PREFIXab 等前缀；默认大小为 1000 行，默认前缀为 `'x'`。 

若无 `FILE` 或 `FILE` 为 `-`，则读取标准输入。 

- `-l, --lines=NUMBER`  
	为每个输出文件添加行数/记录数
	
- `--filter=COMMAND`  
	写入 shell 命令；文件名为 `$FILE`

```sh
# 读取文件
split --filter 'cat' /flag
# 交互式 shell
split --filter '/bin/sh -i 0<&2 1>&2' /flag
```

### tee - 从标准输入读取，并写入标准输出与文件

https://www.man7.org/linux/man-pages/man1/tee.1.html

```sh
tee [选项]... [文件]...
```

将标准输入复制到每个文件，并同时输出到标准输出。

参数：
- `-a, --append`  
	追加到给出的文件，而不是覆盖

示例
```sh
# `test` 将被 tee 写入文件的同时输出到 stdout 以打印
echo 'test' | tee file.txt

# 读取进程信息并禁用截断，保留表头，提取特定内容
ps auxww | tee >(head -n1) >(grep /challenge) > /dev/null
```

### grep

https://www.man7.org/linux/man-pages/man1/grep.1.html

```sh
grep [OPTION]... PATTERNS [FILE]...
grep [OPTION]... -e PATTERNS ... [FILE]...
grep [OPTION]... -f PATTERN_FILE ... [FILE]...
```

`grep` 在每个`FILE`中搜索模式。  
在第一个形式中（如果没有 -e 或 -f 选项），第一个操作数模式是由换行符分隔的一个或多个模式，grep 会打印出与模式匹配的每一行。

此外，还提供了两个变体程序 egrep 和 fgrep。egrep 等同于 grep -E。fgrep 等同于 grep -F。直接以 egrep 或 fgrep 的形式调用已被弃用，但提供这些选项是为了允许依赖它们的旧应用程序无需修改即可运行。

参数
- `-n`  
	显式匹配行的行号
- `-r, --recursive`  
	递归搜索目录
- `-R, --dereference-recursive`
    递归读取每个目录下的所有文件。跟随所有符号链接，与 -r 不同。
- `-E, --extended-regexp` 
	将模式解释为扩展正则表达式。
- `-P, --perl-regexp`
	将模式解释为 perl 正则表达式。
	- `(?<=foo)`
		匹配 foo 但不包含在结果中
- `-m NUM, --max-count=NUM`
	在读取 NUM 行匹配内容后停止读取文件。
- `-o, --only-matching`
	仅打印匹配（非空）的行部分，每个这样的部分单独输出在一行上。

匹配控制：
- `-v, --invert-match`  
	反转匹配的意义，选择不匹配的行。(-v 由 POSIX 指定。)
- `-i, --ignore-case`
    忽略模式和输入数据中的大小写差异，使仅在大小写上不同的字符能够匹配。

上下文行控制：
- `-A NUM, --after-context=NUM`
    在匹配行后打印 NUM 行的后续上下文。

- `-B NUM, --before-context=NUM`
    在匹配行前打印 NUM 行的前导上下文。

- `-C NUM, -NUM, --context=NUM`
    打印 NUM 行的输出上下文。

General Output Control:
- `-q, --quiet, --silent` 安静模式；不将任何内容写入标准输出。如果找到任何匹配项，即使检测到错误，也会立即以零状态退出。另请参阅 -s 或 --no-messages 选项。  
	可用来在脚本的条件表达式中根据返回值判断是否找到。

File and Directory Selection
`-a, --text`
    跨原始字节强制进行文本模式扫描

### diff

https://www.man7.org/linux/man-pages/man1/diff.1.html

```sh
diff [OPTION]... FILES
```

逐行比较文件。

输出示例：
- `2a3` 在文件1的第2行后，追加(append)文件2的第3行
- `5c7` 第文件1的第5行，被替换(change)为文件2的第7行

### cut

https://www.man7.org/linux/man-pages/man1/cut.1.html

```sh
cut OPTION... [FILE]...
```

从每个 FILE 中打印选定行的一部分到标准输出。

参数：
- `-d, --delimiter=分隔符`
	指定列字段分隔符
- `-f, --fields=LIST`
	指定列字段编号
- `-w, --whitespace-delimited[=trimmed]`
    使用空白字符序列作为字段分隔符
- `-z, --zero-terminated`
    换行符是 NUL，而不是换行符

```sh
# 使用空白作为列字段分隔符，提取列2。输出为换行分隔的每行对应的列
cut -w -f 2 文件 
```

### paste - 合并文件中的多行

https://www.man7.org/linux/man-pages/man1/paste.1.html

```sh
paste [OPTION]... [FILE]...
```

### sort - 排序文本文件的行

https://www.man7.org/linux/man-pages/man1/sort.1.html

```sh
sort [OPTION]... [FILE]...
sort [OPTION]... --files0-from=F
```

将所有 FILE(s) 的排序后连接结果写入标准输出。

默认情况下，`sort` 按字母顺序排列行。

参数
- `-r`：反向顺序（Z 到 A）
- `-n`：按数值排序（用于数字）
- `-u`：仅保留唯一行（删除重复项）
- `-R`：随机顺序

### rev - 反转文件或多个文件的行

https://www.man7.org/linux/man-pages/man1/rev.1.html

```sh
rev [option] [file...]
```

指定的文件复制到标准输出，反转每行中的字符顺序。如果没有指定文件，则读取标准输入。

### head

```sh
head [参数]... [文件]...
```

默认查看文件前十行

参数
- `-n, --lines=[-]NUM`  
	显示设置的行数
- `-c, --bytes=[-]NUM`  
  打印每个文件的前 `NUM` 个字节；以 `-` 开头时，打印每个文件除最后 `NUM` 个字节外的所有内容

```sh
# 显示前9行
head -n9
```

### tail - 输出文件的最后一部分

https://www.man7.org/linux/man-pages/man1/tail.1.html

```sh
tail [OPTION]... [FILE]...
```

将每个文件的最后 10 行打印到标准输出。如果有多个文件，每个文件前会加上一个标题，显示文件名。如果没有文件，或者文件是-，则读取标准输入。

参数
- `-n, --lines=K`
	输出最后 K 行，而不是最后 10 行

### uniq - 报告或省略重复的行

https://www.man7.org/linux/man-pages/man1/uniq.1.html

```sh
uniq [OPTION]... [INPUT [OUTPUT]]
```

### strings - 打印文件中可打印字符的字符串。

https://www.man7.org/linux/man-pages/man1/strings.1.html

```sh
strings [-afovV] [-min-len]
        [-n min-len] [--bytes=min-len]
        [-t radix] [--radix=radix]
        [-e encoding] [--encoding=encoding]
        [-U method] [--unicode=method]
        [-] [--all] [--print-file-name]
        [-T bfdname] [--target=bfdname]
        [-w] [--include-all-whitespace]
        [-s] [--output-separator sep_string]
        [--help] [--version] file...
```

strings 主要用于确定非文本文件的内容。

参数：
- `-t radix`
 `--radix=radix`
	在文件中每个字符串之前打印其偏移量。单个字符参数指定偏移量的基数:   
	o 表示八进制，x 表示十六进制，或 d 表示十进制。

### wc - 打印每个文件的行数、单词数和字节数

```sh
wc [OPTION]... [FILE]...
wc [OPTION]... --files0-from=F
```

为每个 FILE 打印换行符、单词和字节数，如果指定了多个 FILE，则还会打印总计行。如果没有 FILE，或者 FILE 是-，则读取标准输入。

- `-c, --bytes`
    print the byte counts

- `-m, --chars`
    print the character counts

- `-l, --lines`
    print the newline counts
        
- `--files0-from=F`
	从文件 F 中读取由 NUL 终止的名称指定的输入文件；如果 F 是 -，则从标准输入读取名称。（信息泄露）
	- `wc --files0-from=/flag`

```sh
# 使用换行符统计，快速得到命令行输出的文件/元素数量
ls -al | wc -l
```

### cat - 连接文件并打印到标准输出

https://man7.org/linux/man-pages/man1/cat.1.html

```sh
cat [OPTION]... [FILE]...
```

当没有 FILE，或 FILE 为 `-` 时，读取标准输入。
> 单纯读取标准输入时，效果为回显。若使用 `cat file1 - | nc`，确保不会在第一个文件发送后关闭 tcp 连接

- `-n, --number`
	对所有输出行进行编号

### tr —— 翻译或删除字符

https://www.man7.org/linux/man-pages/man1/tr.1.html

```bash
tr [OPTION]... STRING1 [STRING2]
```

从标准输入翻译、压缩和/或删除字符，并写入标准输出。`STRING1` 和 `STRING2` 指定控制操作的字符数组 `ARRAY1` 和 `ARRAY2`。

- `-c, -C, --complement`
    使用 `ARRAY1` 的补集

- `-d, --delete`
    删除 `ARRAY1` 中的字符，不进行翻译

- `-s, --squeeze-repeats`
    将最后指定的 `ARRAY` 中列出的重复字符的每个序列替换为该字符的单个出现

- `-t, --truncate-set1`
    首先将 `ARRAY1` 截断为 `ARRAY2` 的长度

`ARRAY` 被指定为字符串。大多数字符代表它们自身。解释序列为：

- `\NNN`
    八进制值为 NNN 的字符（1 到 3 个八进制数字）

- `\n`
    换行

- `\r`
    回车

- `\t`
    水平制表符

- ...

- `CHAR1-CHAR2`
    从 `CHAR1` 到 `CHAR2` 按升序排列的所有字符

- `[CHAR*]`
    在 `ARRAY2` 中，复制 `CHAR` 直到 `ARRAY1` 的长度

- `[CHAR*REPEAT]`
    `CHAR` 的 `REPEAT` 次复制，如果以 0 开头则为八进制 `REPEAT`

- `[:alnum:]`
    所有字母和数字

- `[:alpha:]`
    所有字母

- `[:digit:]`
    所有数字

- `[:lower:]`
    所有小写字母

- `[:print:]`
    所有可打印字符，包括空格

- `[:space:]`
    所有水平或垂直空白

- `[:upper:]`
    所有大写字母

- `[:xdigit:]`
    所有十六进制数字

- `[=CHAR=]`
    所有与 `CHAR` 等价的字符

- ...

如果未给出 `-d` 且 `STRING1` 和 `STRING2` 都出现，则进行翻译。`-t` 仅在翻译时有意义。`ARRAY2` 通过根据需要重复其最后一个字符来扩展到 `ARRAY1` 的长度。`ARRAY2` 的多余字符将被忽略。字符类按未指定的顺序展开；翻译时，`'[:lower:]'` 和 `'[:upper:]'` 可以成对使用以指定大小写转换。压缩在翻译或删除之后发生。像 `'[...]'` 这样的参数应加引号，以避免潜在的 shell 通配。


例：

```sh
# 删除换行
tr -d '\n'

# 修改换行为空格
tr '\n' ' '

# 翻转大小写
tr [:upper:][:lower:] [:lower:][:upper:]
tr A-Za-z a-zA-Z
```

### gawk - 模式扫描和处理语言

https://www.gnu.org/software/gawk/manual/gawk.html

https://www.man7.org/linux/man-pages/man1/gawk.1.html

```sh
gawk [ POSIX or GNU style options ] -f program-file [ -- ] file ...
gawk [ POSIX or GNU style options ] [ -- ] program-text file ...
```

`gawk` 是 GNU 项目对 AWK 编程语言的实现。它遵循 POSIX 1003.1 标准中的语言定义（查看 `awk(1p)`）。


```sh
# file 输出格式 `文件名: 文件类型`
# awk 使用 `:` 作为列分隔符，查找类型列中归为 text 的文件，并打印文件名列
file * | awk -F':' '$2 ~ /text/ {print $1}'   
```

参数

- 
    ```
    -F fs
    --field-separator fs
    ```
    使用 `fs` 作为输入字段分隔符（预定义变量 `FS` 的值）。

变量、记录和字段

- 字段  
    读取每条输入记录时，`gawk` 使用 `FS` 变量的值作为字段分隔符，将记录拆分为列字段。

    输入记录中的每个字段可以通过其位置引用：`$1`、`$2` 等。`$0` 是整条记录，包括前导和尾随空白。

    变量 `NF` 被设置为输入记录中的字段总数。

模式和动作，AWK 是一种面向行的语言。模式在前，动作在后。动作语句括在 `{` 和 `}` 中。

- 模式

    ```awk
    /regular expression/
    ```
- 动作

    动作语句括在花括号 `{` 和 `}` 中。动作语句由大多数语言中常见的赋值、条件和循环语句组成。可用的运算符、控制语句和输入/输出语句仿照 C 中的相应内容。

- 运算符

    - `(...)`  
        分组。

    - `$`  
        字段引用。

    - `~ !~`  
        正则表达式匹配、否定匹配。

### 🔍 sed - 用于过滤和转换文本的流编辑器

https://man7.org/linux/man-pages/man1/sed.1.html

https://www.gnu.org/software/sed/manual/html_node/index.html

```sh
sed [-V] [--version] [--help] [-n] [--quiet] [--silent]
	[-l N] [--line-length=N] [-u] [--unbuffered]
	[-E] [-r] [--regexp-extended]
	[-e script] [--expression=script]
	[-f script-file] [--file=script-file]
	[script-if-no-other-script]
	[file...]
```

`sed` 是一个流编辑器。流编辑器用于对输入流（文件或来自管道的输入）执行基本文本转换。虽然在某些方面类似于允许脚本化编辑的编辑器（如 `ed`），但 `sed` 只对输入进行一遍处理，因此效率更高。但 `sed` 在管道中过滤文本的能力使其与其他类型的编辑器特别不同。

- `-n`, `--quiet`, `--silent`
  抑制模式空间的自动打印（默认每轮自动打印）
- `--debug`
  注释程序执行
- `-e script`, `--expression=script`
  将脚本添加到要执行的命令中（即，添加多个处理）

如果未给出 `-e`、`--expression`、`-f` 或 `--file` 选项，则第一个非选项参数被视为要解释的 *`sed` 脚本*。所有剩余参数是输入文件的名称；如果未指定输入文件，则读取标准输入。

这只是 `sed` 命令的简要概要，供已经了解 `sed` 的人作为提醒；更完整的描述必须查阅其他文档（例如 texinfo 文档）。

零地址或单地址命令
- `r filename`
  追加从 `filename` 读取的文本。
- `R filename`
  追加从 `filename` 读取的一行。每次调用该命令都会从文件中读取一行。这是 GNU 扩展。

接受地址范围的命令
- `{`
  开始一个命令块（以 `}` 结束）。
- `p`
  打印当前模式空间。（即，立即打印当前空间的所有内容）
- `s/regexp/replacement/`
  尝试将 `regexp` 与模式空间匹配。如果成功，将匹配的部分替换为 `replacement`。`replacement` 可以包含特殊字符 `&` 来引用模式空间中匹配的部分，以及特殊转义 `\1` 到 `\9` 来引用 `regexp` 中对应的匹配子表达式。

#### 地址

`sed` 命令可以不带地址，此时命令会对所有输入行执行；带一个地址时，命令仅对匹配该地址的输入行执行；带两个地址时，命令会对从第一个地址开始到第二个地址结束的闭区间内的所有输入行执行。关于地址范围，有三点需要注意：语法是 `addr1,addr2`（即地址之间用逗号分隔）；`addr1` 匹配到的行总是会被接受，即使 `addr2` 选择的是更早的行；如果 `addr2` 是正则表达式，则不会对 `addr1` 匹配到的行进行测试。

在地址（或地址范围）之后、命令之前，可以插入 `!`，表示命令仅在地址（或地址范围）**不**匹配时执行。

支持以下地址类型：

- `number`
  仅匹配指定的行 `number`（除非在命令行中指定了 `-s` 选项，否则行号会跨文件累计递增）。

- `first~step`
  匹配从行 `first` 开始的每第 `step` 行。例如，`sed -n 1~2p` 会打印输入流中所有奇数行，而地址 `2~5` 会匹配从第二行开始的每第五行。`first` 可以为零；在这种情况下，`sed` 的行为就像它等于 `step` 一样。（这是一个扩展。）

- `$`
  匹配最后一行。

- `/regexp/`
  匹配与正则表达式 `regexp` 匹配的行。匹配在当前模式空间上执行，模式空间可以通过 `s///` 等命令修改。

- `\c regexp c`
  匹配与正则表达式 `regexp` 匹配的行。`c` 可以是任意字符。

#### 示例

```sh
# 空脚本，自动打印将逐行输出文件
sed '' file

# 抑制自动打印，使用打印当前模式空间脚本逐行打印
sed -n 'p' file

# 抑制自动打印，逐行打印文件地址范围 10-20行
sed -n '10, 20p' file
```

### fold - 将每个输入行换行以适合指定宽度

```sh
fold [OPTION]... [FILE]...
```

将每个 `FILE` 中的输入行换行，并写入标准输出。

没有 `FILE`，或 `FILE` 为 `-` 时，读取标准输入。

- `-b`、`--bytes`  
  按字节而非列计数

- `-c`、`--characters`  
  按字符而非列计数

- `-s`、`--spaces`  
  在空白后断行，或在长度大于 `WIDTH` 的单词中断行

- `-w`、`--width=WIDTH`  
  使用 `WIDTH` 列而不是 80 列

## 文本编辑器


## 手册

### man —— 系统参考手册的接口

https://www.man7.org/linux/man-pages/man1/man.1.html


```sh
man [man options] [[section] page ...] ...
man -k [apropos options] regexp ...
man -K [man options] [section] term ...
man -f [whatis options] page ...
man -l [man options] file ...
man -w|-W [man options] page ...
```

手册页存储在集中式数据库中，位于 `/usr/share/man` 目录

参数：
- `-k, --apropos [关键词]`  
	以正则表达式搜索关键词的简要描述和手册页名称，并打印所有匹配项。与 [`apropos`] 命令功能大致相同。

例：
```sh
# 查看 ascii 码进制映射
man ascii

# 搜索关键词
man -k 关键词
```
	
------

手册页操作：
用方向键和 PgUp/PgDn 在手册页中滚动。阅读完手册页后，按 `q` 退出。

用 `/` 搜索。搜索后，按 `n` 跳到下一个结果，按 `N` 跳到上一个结果。除了 `/`，使用 `?` 向后搜索

### apropos - 搜索手册页的名称和描述

https://man7.org/linux/man-pages/man1/apropos.1.html

```sh
apropos [-dalv?V] [-e|-w|-r] [-s list] [-m system[,...]] [-M path]
[-L locale] [-C file] keyword ...
```

例
```sh
# 搜索关键词
apropos 关键词
```

## 加密哈希

### cksum - 计算并验证文件校验和

https://www.man7.org/linux/man-pages/man1/cksum.1.html

```bash
cksum [OPTION]... [FILE]...
```

打印或验证校验和。默认使用 32 位 `CRC` 算法。

未指定 `FILE`，或 `FILE` 为 `-` 时，读取标准输入。

长选项的必需参数对短选项同样是必需的。

- `-a, --algorithm=TYPE`：选择要使用的摘要类型。参见下文 `DIGEST`
- `--base64`：输出 `base64` 编码的摘要，而非十六进制
- `-c, --check`：从各 `FILE` 中读取校验和并检查
- `-l, --length=BITS`：摘要长度（以位为单位）；对于 `blake2b`，不得超过最大大小且必须是 8 的倍数；对于 `sha2` 或 `sha3`，必须为 224、256、384 或 512
- `--raw`：输出原始二进制摘要，而非十六进制
- `--tag`：创建 BSD 风格校验和（默认）
- `--untagged`：创建反转风格校验和，不带摘要类型
- `-z, --zero`：以 `NUL` 而非换行结束每个输出行，并禁用文件名转义

**以下五个选项仅在验证校验和时有用：**

- `--ignore-missing`：不因文件缺失而失败或报告状态
- `--quiet`：不为每个成功验证的文件打印 `OK`
- `--status`：不输出任何内容，状态码表示成功
- `--strict`：对格式不正确的校验和行以非零状态退出
- `-w, --warn`：对格式不正确的校验和行发出警告

- `--debug`：指示所使用的实现
- `--help`：显示此帮助并退出
- `--version`：输出版本信息并退出

**`DIGEST` 决定摘要算法和默认输出格式：**

- `sysv`（等价于 `sum -s`）
- `bsd`（等价于 `sum -r`）
- `crc`（等价于 `cksum`）
- `crc32b`（仅可通过 `cksum` 使用）
- `md5`（等价于 `md5sum`）
- `sha1`（等价于 `sha1sum`）
- `sha2`（等价于 `sha{224,256,384,512}sum`）
- `sha3`（仅可通过 `cksum` 使用）
- `blake2b`（等价于 `b2sum`）
- `sm3`（仅可通过 `cksum` 使用）

检查时，输入应为该程序或等效独立程序的先前输出。

## 时间

### date - 打印或设置系统日期和时间

https://www.man7.org/linux/man-pages/man1/date.1.html

```sh
date [OPTION]... [+FORMAT]
date [OPTION]... MMDDhhmm[[CC]YY][.ss]
```

- `-f` 
	读取指定文件的每一行并尝试解析为日期。（信息泄露）

## 用户权限

#### passwd

`passwd [-k] [-l] [-u [-f]] [-d] [-e] [-n mindays] [-x maxdays] [-w warndays] [-i inactivedays] [-S] [--stdin] [username]`

passwd 用于更新用户的身份验证令牌。

passwd 命令启用了 SUID（保存用户 ID）。当执行 passwd 命令时，当前生效的有效用户 ID（EUID）会被复制到保存用户 ID（即 root）。因此，通过这种技术，普通用户账户可以更新其密码在 /etc/shadow 文件中。

具有 root 权限才能更改其他所有用户的密码

#### chage

`chage [options] [LOGIN]`

修改密码更改之间的天数以及上次密码更改的日期。系统使用这些信息来确定用户何时需要更改密码。

### gpasswd - 管理 /etc/group and /etc/gshadow

https://www.man7.org/linux/man-pages/man1/gpasswd.1.html

```sh
gpasswd [option] group
```

### newgrp - 登录到新组

```sh
newgrp [-] [group]
```

`newgrp` 命令用于在登录会话期间更改当前的组 ID。

```sh
newgrp root
```

#### sg

`sg target_group 'id'`
输入组密码，在当前 Shell 的“有效组 ID”会切换到目标组，用于执行单条命令。


## 文件 ACL

### getfacl 
### setfacl 

## json

### jq —— 修改或转换 JSON

https://manpages.ubuntu.com/manpages/tenacious/man1/jq.1.html

```sh
jq [options...] filter [files...]
```

```console
# 使用 `.key` 访问 value
$ jq .b <<< '{"a":"1","b":"2"}'
"2"
```

- `--slurp / -s`  
    修改过滤器为整个流，而非默认的 JSON 对象

- `--raw-input / -R`  
    传递字符串到过滤器，而非默认的 JSON 格式。
    如果与 `--slurp` 一起使用，则整个输入将作为一个长字符串传递给过滤器。

- `--raw-output / -r`  
    若过滤器的结果是字符串，则直接写入标准输出，不进行 JSON 字符串格式化

格式化与转义 `@foo`
- `@html`
- `@uri`
- `@base64`

```console
# 使用 jq 的普通字符串参数，对字符串进行 uri 编码
$ echo -n 'foo bar' | jq -sRr @uri
foo%20bar
```

## 网络

### socat - 多用途中继 (SOcket CAT)

http://www.dest-unreach.org/socat/doc/socat.html

https://www.man7.org/linux/man-pages/man1/socat.1.html

```sh
socat [options] <address> <address>
socat -V
socat -h[h[h]] | -?[?[?]]
filan
procan
```

`socat` 是一个基于命令行的实用程序，它建立两个双向字节流，并在它们之间传输数据。由于这些流可以由大量不同类型的数据接收器和数据源（参见地址类型）构造，并且可以对这些流应用许多地址选项，因此 `socat` 可用于许多不同目的。

```sh
# 服务器
socat \
TCP4-LISTEN:5556,fork \
EXEC:'"chroot --userspec=root:root / /bin/sh"',pty,stderr
```
- 接受连接 `TCP4-LISTEN` 并为每个连接 `fork` 新子进程
- 为了 `EXEC` 程序，子进程 `chroot` 到 `/`，设置真实 id 到 root，然后启动 `/bin/sh`  
    > 注意 `EXEC` 将空格作为参数分隔符，`chroot` 的空格使用 `"` 转义（从而作为本身，而不是 `EXEC` 的分隔符）
- `Socat` 和 `/bin/sh` 通过伪 tty（`pty`）通信
- `/bin/sh` 的 `stderr` 重定向到 `stdout`，因此其错误消息通过 `socat` 传输到连接的客户端

```sh
# 客户端
socat - TCP4:localhost:5556
```
- 在 STDIO `-` 与到主机 `localhost` 端口 `5556` 的 `TCP4` 连接之间传输数据

```sh
# 有效特权 shell
socat - exec:'"/bin/sh -p"',pty,ctty
```

### 地址规范

从 `socat` 1.5.0 及更高版本开始，词法分析尝试有意义地处理引号和括号，并允许转义特殊字符。如果找到字符 `{`、`[`、`'` 之一，则查找相应的结束字符 `}`、`]`、`'`；它们也可以嵌套。在这些结构内，`socat` 的特殊字符和字符串 `:`、`,`、`!!` 不会被特殊处理。所有这些字符和字符串都可以用 `\` 或在 `""` 内转义。

### 地址类型

#### `EXEC:<command-line>`

```
EXEC:<command-line>
```

派生一个子进程，使其与父进程建立通信，并使用 `execvp()` 调用指定程序。`<command-line>` 是简单命令，参数由单个空格分隔。如果程序名包含 `/`，最后一个 `/` 之后的部分作为 `ARGV[0]`。如果程序名是相对路径，则适用 `execvp()` 通过 `$PATH` 查找程序的语义。程序成功启动后，`socat` 将数据写入进程的 `stdin`，并从其 `stdout` 读取；默认使用由 `socketpair()` 生成的 UNIX 域套接字。（示例）  
选项组：`FD`、`SOCKET`、`EXEC`、`FORK`、`TERMIOS`  
有用选项：`path`、`fdin`、`fdout`、`chroot`、`su`、`su-d`、`nofork`、`socktype`、`pty`、`stderr`、`ctty`、`setsid`、`pipes`、`umask`、`login`、`sigint`、`sigquit`、`netns`  
另请参阅：`SYSTEM`、`SHELL`

---
参数
- `CWTCP-LISTEN:<port>`
	监听并接受 TCP 连接
	- Useful options: `crnl, fork, bind, range, tcpwrap, pf, max-children, backlog, mss, su, reuseaddr, retry, cool-write`

- `CWEXEC:<command-line>`

端口选项
- `CWreuseaddr`
    重用地址

子进程选项
- `CWfork`
	连接后创建子进程

示例
- `socat TCP-LISTEN:4000,reuseaddr,fork EXEC:'node /usr/app/bot.js'`
	监听 TCP 端口 4000，连接建立后创建子进程执行命令

- `socat - exec:'sh -p',pty,stderr,setsid,sigint,sane`
	- 地址1为 `-` 标准输入输出
	- 地址2为 `exec`
		逗号分隔选项:
		- pty 伪终端
		- stderr 标准错误重定向
		- setsid 在新会话中创建进程，获得作业控制权限
		- sigint 处理中断信号
		- sane 设置初始状态的组合选项



### `whois` - whois 目录服务客户端

```sh
whois [ { -h | --host } HOST ] [ { -p | --port } PORT ] [ -abBcdGHIKlLmMrRx ] [ -g SOURCE:FIRST-LAST ] [ -i ATTR[,ATTR]... ] [ -s SOURCE[,SOURCE]... ] [ -T TYPE[,TYPE]... ] [ --verbose ] [ --no-recursion ] OBJECT
whois -q KEYWORD
whois -t TYPE
whois -v TYPE
whois --help
whois --version
```

从数据库中搜索对象

选项
- `-h` `HOST`, `--host=HOST`  
  连接到 `HOST`。

```sh
# 从 ripe 数据库中查询 IP
whois -h whois.ripe.net 1.1.1.1
```

### ncat

[手册](https://nmap.org/book/ncat-man.html)

https://www.man7.org/linux/man-pages/man1/ncat.1.html

```sh
ncat [OPTIONS...] [hostname] [port]
```

参数：
- `-l, --listen`  
	绑定并监听传入连接
- `-e, --exec <command>`
	Executes the given command
- `-v` 
	信息详细程度，重复多次提高详细程度
- `--output 文件名`
	保存信息到文件

聆听模式示例

1. 创建文件
	```http
	HTTP/1.1 200 OK

	<html>
		<body>
			<h1> from ncat </h1>
		</body>
	</html>
	```

2. 使用 ncat 监听并返回文件设置的响应
	```sh
	ncat -l localhost 8080 < helloy.http
	```
	```powershell
	type helloy.http | ncat -l localhost 8080
	```

### nc - TCP/UDP 连接

https://manpages.ubuntu.com/manpages/stonking/man1/nc_openbsd.1.html

```sh
nc [-46bCDdFhklNnrStUuvZz]
   [-I length]
   [-i interval]
   [-M ttl]
   [-m minttl]
   [-O length]
   [-P proxy_username]
   [-p source_port]
   [-q seconds]
   [-s sourceaddr]
   [-T keyword]
   [-V rtable]
   [-W recvlimit]
   [-w timeout]
   [-X proxy_protocol]
   [-x proxy_address[:port]]
   [destination] [port]
```

`nc`（或 `netcat`）实用程序可用于几乎所有涉及 TCP、UDP 或 UNIX 域套接字的事情。它可以打开 TCP 连接、发送 UDP 数据包、监听任意 TCP 和 UDP 端口、进行端口扫描，并同时处理 IPv4 和 IPv6。
> 默认使用 TCP 连接

参数：

- `-u`  
    使用 UDP 而不是 TCP。

- `-w timeout`  
    无法建立或空闲的连接在 `timeout` 秒后超时。`-w` 标志对 `-l` 选项没有影响，即无论是否带有 `-w` 标志，`nc` 都将永远监听连接。默认没有超时。

- `-k`  
    当连接完成后，继续监听另一个连接。需要 `-l`。与 `-u` 选项一起使用时，服务器套接字不会连接，并且可以接收来自多个主机的 UDP 数据报。

- `-l`  
    监听传入连接，而不是向远程主机发起连接。要监听的 `destination` 和 `port` 可以指定为非可选参数，也可以分别使用 `-s` 和 `-p` 选项指定。此外，使用 `-w` 选项指定的任何超时都会被忽略。

- `-N`  
    在输入遇到 EOF 后对网络套接字执行 [shutdown(2)]。某些服务器需要这样做才能完成它们的工作。

- `-v`  
    生成更详细的输出。


示例

```sh
# 监听 1234 端口上的连接
nc -l 1234

# 连接到 ip 127.0.0.1 端口 1234
nc 127.0.0.1 1234
```

## 交互记录

### script - 制作终端会话的 typescript

```sh
script [options] [file] [-- command [argument...]]
```

`script` 会制作终端会话中所有内容的 typescript。终端数据以原始形式存储到日志文件，计时信息存储到另一个（可选的）结构化日志文件。

选项
- `-a`, `--append`  
  将输出追加到 `file` 或 `typescript`，保留先前内容。

- `-c`, `--command` `command`  
  运行 `command`，而不是交互式 shell。这使脚本可以轻松捕获那些在 stdout 不是 tty 时行为不同的程序的输出。除了使用 `-c` 选项，也可以在双短横线（`--`）之后指定 `command`。
  > 无伪终端的双重回显

- `-E`, `--echo` `when`  
  此选项控制会话伪终端从端的 `ECHO` 标志。支持的模式为 `always`、`never` 或 `auto`。 
  > 终端型，若输出则双重回显，若不输出则不被记录。需搭配显式记录参数
  
  - `auto` 默认值：伪终端从端启用 `ECHO`；如果当前标准输入是终端，则对其禁用 `ECHO` 以防止双重回显；如果当前标准输入不是终端（例如管道：`echo date | script`），则保持伪终端从端启用 `ECHO`，使标准输入数据在记录到会话日志的同时也显示在屏幕上。
  
  - `never` 模式会影响会话输出日志的内容，因为用户输入不会在输出中重复。

- `-B`, `--log-io` `file`  
  将输入和输出记录到同一个 `file`。注意，仅当同时指定 `--log-timing` 时此选项才有意义，否则无法从日志 `file` 中分离输出流和输入流。
  > 设置显式记录参数时，不应再设置原 `file` 参数

- `-T`, `--log-timing` `file`  
  将计时信息记录到 `file`。

- `-q`, `--quiet`  
  安静模式（不向标准输出写入开始和完成消息）。

```sh
# 命令型：作为目标程序包装器，记录交互
script -q /tmp/log -c "/target_program"

# 终端型：记录所有交互，关闭双重回显，显式设置记录参数
script -q --echo never --log-io /tmp/io
```

## 字体


### fc-cache — 构建字体信息缓存文件

```sh
fc-cache [ -cEfrsvVh ] [ --chroot root ] [ --error-on-no-fonts ] [ --force ] [ --really-force ] [ -y dir | --sysroot dir ] [ --system-only ] [ --verbose ] [ --version ] [ --help ] [ dir ... ]
```

`fc-cache` 扫描系统上的字体目录，并为使用 fontconfig 处理字体的应用程序构建字体信息缓存文件。

如果未给定目录参数，`fc-cache` 会使用当前字体配置中的每个目录。每个目录都会被扫描，以查找 FreeType 可读取的字体文件。随后会创建一个缓存，其中包含每个字体的属性及关联的文件名。此缓存用于在使用 fontconfig 库时加快应用程序启动速度。

请注意，`fc-cache` 必须针对每种架构执行一次，以生成为该架构定制的字体信息。


选项

- `-f --force`  
    强制重新生成看似最新的缓存文件，覆盖时间戳检查。

- `-r --really-force`  
    删除所有现有缓存文件并重新扫描。

- `-s --system-only`  
    仅扫描系统级目录，省略用户主目录中的位置。

- `-v --verbose`  
    忙碌时显示状态信息。

```sh
# 目录中新增字体后刷新，查看进度信息
fc-cache -fv
```

### fc-list — 列出可用字体

```sh
fc-list [ -vVh ] [ --verbose ] [ -f format | --format format ] [ -q | --quiet ] [ --version ] [ --help ]
[ pattern [ element ... ] ]
```

`fc-list` 列出系统中可供使用 fontconfig 的应用程序使用的字体和样式。如果指定了任何元素，则只打印这些元素。否则，除非请求详细输出，否则打印字体族和样式。

```sh
# 查看字体是否被正确应用，虽然 fc-list 拥有其匹配功能，但简单使用 grep
fc-list | grep 字体名
```

## 终端

### tput - 初始化终端、使用其能力或查询 terminfo 数据库

https://man7.org/linux/man-pages/man1/tput.1.html

```
tput [-v] [-T terminal-type] {cap-code [parameter ...]} ...
tput [-v] [-T terminal-type] [-x] clear
tput [-v] [-T terminal-type] init
tput [-v] [-T terminal-type] reset
tput [-v] [-T terminal-type] longname
tput [-v] -S
tput [-v] -V
```

`tput` 使用 `terminfo` 库和数据库，使终端特定的能力和信息可供 shell 使用，用于初始化或重置终端，或者报告当前（或指定）终端类型的描述。终端能力通过 `cap-code` 访问。

`terminfo(5)` 详细讨论了终端能力，并给出了标准化 `cap-code` 的完整列表。`user_caps(5)` 介绍了其他广泛使用但非标准的能力。


`tput` 作为 `ncurses`（new curses）项目的一部分

> python 的 curses 模块提供 curses 库的接口，匹配 ncurses 的 API

### `infocmp` - 比较或打印 `terminfo` 描述

https://man.archlinux.org/man/infocmp.1m

```sh
infocmp [-1cCdDeEFgGiIKlLnpqrtTuUVWx] [-A directory] [-B directory] [-Q encoding] [-R subset] [-s key] [-v level] [-w width] [terminal-type ...]
```

`infocmp` 从 `terminfo` 数据库中的已编译条目报告人类可读的终端类型描述，支持多种可选格式；它也可以比较这些条目，并通过引用其他条目的内容重写某个条目，以替换 `use` 表达式。一个 `terminfo` 条目由一个或多个终端类型标识符、终端类型的人类可读描述，以及描述其编程接口的终端能力列表组成。在所有情况下，程序都会先报告布尔值能力，再报告数值能力，最后报告字符串值能力。

```sh
# 查看终端能力信息
infocmp
```

## 环境

### env - 在修改后的环境中运行程序

```sh
env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]
```

在环境中将每个 `NAME` 设置为 `VALUE`，并运行 `COMMAND`。


```sh
# 在“干净环境”下，确保只从系统目录找到工具链组件
env -i PATH=/usr/bin:/bin`
```

```sh
# 交互 shell
env /bin/sh -p
```

- `-a, --argv0=ARG`  
    将 `ARG` 作为 `COMMAND` 的第零个参数传递

- `-i, --ignore-environment`  
    以空环境开始


单独的 `-` 意味着 `-i`。如果没有 `COMMAND`，则打印结果环境。

## 未分类

### chsh - 更改登录 shell

https://www.man7.org/linux/man-pages/man1/chsh.1.html

```sh
chsh [-s shell] [-l] [-h] [-V] [username|UID]
```

#### 描述

`chsh` 用于更改登录 shell。如果未在命令行中指定 shell，`chsh` 会提示输入一个 shell。

如果链接了 libuser，`chsh` 支持非本地条目（kerberos、LDAP 等）；否则，对于非本地条目，请使用 `ypchsh(1)`、`lchsh(1)` 或任何其他实现。

#### 选项

- `-s`, `--shell shell`  
  指定登录 shell。

- `-l`, `--list-shells`  
  打印 `/etc/shells` 中列出的 shell 列表并退出。

- `-h`, `--help`  
  显示帮助文本并退出。（短选项 `-h` 自版本 2.30 起使用；较早版本使用现已弃用的 `-u`。）

- `-V`, `--version`  
  显示版本并退出。（短选项 `-V` 自版本 2.39 起使用；较早版本使用现已弃用的 `-v`。）

#### 有效 shell

`chsh` 将接受系统上任何可执行文件的完整路径名。

对于非特权用户，默认行为是仅接受 `/etc/shells` 文件中列出的 shell，并对 root 用户发出警告。也可以在编译时配置为对所有用户仅发出警告。

#### 退出状态

如果操作成功，返回 0；如果操作失败或命令语法无效，返回 1。

### make - 用于维护程序组的 GNU make 工具

```sh
make [OPTION]... [TARGET]...
```

`make` 实用程序将自动确定大型程序中哪些部分需要重新编译，并发出重新编译它们的命令。

```makefile
# makefile 格式
immediate : immediate ; deferred
        deferred
```

```sh
# 交互 shell，若文件已存在，需添加无条件 make 参数

# makefile 文件格式，全权限 shell
make --eval '不存在的目标文件 : ; /bin/sh -p'

# make 函数型，普通 shell
make --eval='$(shell /bin/sh 1>&0 2>&0)'
```

- `-B`、`--always-make`  
    无条件地 make 所有目标。

- `-E` `string`、`--eval` `string`  
    在解析任何 makefile 之前，使用 `eval` 函数解释 `string`。

- `-C` `dir`、`--directory=dir`  
    在读取 makefile 或执行任何其他操作之前，切换到目录 `dir`。如果指定了多个 `-C` 选项，每个都相对于前一个解释：`-C / -C etc` 等价于 `-C /etc`。这通常用于 `make` 的递归调用。


#### 函数调用

函数调用类似于变量引用。它可以出现在变量引用可以出现的任何位置，并使用与变量引用相同的规则展开。函数调用如下所示：

```makefile
$(function arguments)
```

或者如下所示：

```makefile
${function arguments}
```

##### `shell` 函数

`shell` 函数与除 `wildcard` 函数之外的任何其他函数都不同（参见“`wildcard` 函数”），因为它与 `make` 之外的世界通信。

`shell` 函数为 `make` 提供了与大多数 shell 中反引号（`` ` ``）相同的功能：它执行*命令展开*。这意味着它接受一个 shell 命令作为参数，并展开为该命令的输出。`make` 对结果所做的唯一处理是将每个换行符（或回车/换行对）转换为单个空格。如果有尾随（回车和）换行符，则直接移除。

`shell` 函数的替代方法是 `!=` 赋值运算符；它提供类似行为，但有细微差别（参见“设置变量”）。`!=` 赋值运算符包含在较新的 POSIX 标准中。

以下是 `shell` 函数的一些使用示例：

```makefile
contents := $(shell cat foo)
```

将 `contents` 设置为文件 `foo` 的内容，每行之间用空格（而不是换行符）分隔。