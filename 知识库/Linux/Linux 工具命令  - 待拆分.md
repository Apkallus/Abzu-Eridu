

## 使用帮助 & 环境基础

### 帮助系统

### 包管理工具

#### Cargo ———— Rust 的包管理器

##### cargo-install —— 下载并安装 Rust 库

https://doc.rust-lang.org/cargo/commands/cargo-install.html

```sh
cargo install [options] crate[@version]…
cargo install [options] --path path
cargo install [options] --git url [crate…]
cargo install [options] --list
```


#### pip3 - python3 包管理器

- `--cache-dir 目录` 
	设置缓存目录
- `--no-cache-dir` 
	禁用缓存

#### pip

https://pip.pypa.io/en/stable/cli/pip

General Options

- `--trusted-host <hostname>`
	将此主机或 `host:port` 对标记为**受信任**，即使它没有有效证书或未启用 HTTPS。
	（环境变量：`PIP_TRUSTED_HOST`）

##### pip_install

Options

- `-r, --requirement <file>`
	从给定的 requirements 文件中安装。文件或 URL 可以是 pip 的 requirements.txt 格式或 pylock.toml 格式（pylock.toml 支持为实验性）。此选项可多次使用。
	（环境变量：`PIP_REQUIREMENT`）

- `-i, --index-url <url>`
	设置包目录 URL

#### rpm

`rpm` 是一个强大的软件包管理器，可用于构建、安装、查询、验证、更新和卸载单个软件包。一个软件包由一个文件归档和用于安装和卸载归档文件的元数据组成。元数据包括辅助脚本、文件属性以及关于软件包的描述信息。软件包有两种类型：二进制软件包，用于封装要安装的软件；以及源代码软件包，包含生成二进制软件包所需的源代码和构建方法（配方）。

- 操作

	查询和验证软件包

	*   `-U, --upgrade`  
		将软件包安装或升级到更新的版本。在新软件包安装完成后，旧的和/或已被废弃的软件包将被移除。

- 事务选项

	这些事务选项适用于 `--install`、`--upgrade`、`--reinstall` 和 `--erase` 操作。

	*   `-h, --hash`  
		在软件包归档解包时打印 50 个井号（`#`）作为进度标记。与 `-v|--verbose` 结合使用可获得更美观的显示效果。


- 验证选项

	软件包和文件的选择选项与软件包查询的选项相同（包括将 `rpm-manifest(5)` 文件作为参数）。其他仅适用于验证模式的选项有：

	*   `--nodeps`  
		不验证软件包的依赖关系。

	*   `--nodigest`  
		读取时不验证软件包或头部的摘要（digest）。

	*   `--nofiles`  
		不验证软件包文件的任何属性。

	*   `--noscripts`  
		不执行 `%verifyscript` 脚本片段（如果有的话）。

	*   `--nosignature`  
		读取时不验证软件包或头部的签名。

	*   `--nolinkto`、`--nofiledigest`（原 `--nomd5`）、`--nosize`、`--nomtime`、`--nomode`、`--nordev`  
		不验证相应的文件属性。

	*   `--nouser`、`--nogroup`  
		不验证文件的用户/组归属。请注意，仅查阅本地的 `passwd(5)` 和 `group(5)` 数据库。

	*   `--nocaps`  
		不验证文件的能力（capabilities）。

示例：
- `rpm -vhU --nodigest --nofiledigest 应用`
	- 安装最新版并查看进度
	- 不验证头部摘要/字段摘要（应对 `does not verify: no digest`）

#### software-properties-common

- `add-apt-repository ppa:deadsnakes/ppa`
	添加旧版软件仓库

#### dpkg —— Debian 软件包管理器
       

`dpkg [选项...] 命令`

描述
	dpkg 是一个中等层级的工具，用于安装、构建、移除和管理 Debian 软件包。作为命令行界面（CLI），dpkg 的主要且更用户友好的前端是 apt(8)；作为终端用户界面（TUI），则是 aptitude(8)。dpkg 本身完全通过命令行参数控制，这些参数包含恰好一个命令以及零个或多个选项。命令参数告诉 dpkg 要做什么，选项则以某种方式控制命令的行为。

	dpkg 也可以用作 dpkg-deb(1) 和 dpkg-query(1) 的前端。支持的命令列表可在后面的“命令”部分找到。当遇到任何此类命令时，dpkg 只是用给定的参数运行 dpkg-deb 或 dpkg-query，但目前不会向它们传递任何特定选项；若要使用此类选项，需要直接调用后端程序。

命令
- `-i, --install package-file...`
	安装包
	
#### Alien - 跨平台包转换工具

#### rbenv - ruby 版本管理器

- 安装自定义版本
	`rbenv install 2.7.6`

#### yarn

https://classic.yarnpkg.com/en/docs/usage

Adding a dependency

```sh
yarn add [package]
yarn add [package]@[version]
yarn add [package]@[tag]
```



### 工具组合

#### BusyBox——嵌入式 Linux 的瑞士军刀

```
busybox <applet> [arguments...]  # or
<applet> [arguments...]            # if symlinked
```

BusyBox 将许多常用 UNIX 工具的微型版本组合成一个单一的小型可执行文件。它为 GNU coreutils、util-linux 等工具提供了极简的替代品。BusyBox 中的工具通常比其功能齐全的 GNU 同类工具拥有更少的选项；然而，所包含的选项提供了预期的功能，并且行为非常类似于 GNU 版本。

### 系统信息

#### uname —— 打印架构信息

```sh
uname [OPTION]...
```

参数
- `-a, --all`
	打印所有信息

### 环境

#### env

```sh
env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]
```
在环境中将每个 NAME 设置为 VALUE，并运行 COMMAND。
单独使用等同于 `-i`。
通过运行不带任何选项或参数（即输入数据）的 env 命令，可以看到当前用户的所有当前环境变量及其值，包括 PATH 变量中的所有目录

- `-i, --ignore-environment`
	以空环境开始
	- `env -i PATH=/usr/bin:/bin`
		在“干净环境”下，确保只从系统目录找到工具链组件

#### set

- 无参数时查看环境变量

#### printenv —— 打印环境变量

```sh
printenv [OPTION] [VARIABLE]...
```

查看特定或全部环境变量

#### which

```sh
which [options] [--] programname [...]   
```

`which` 命令模拟 shell 在搜索命令时的行为：按顺序查看 `$PATH` 中的每个目录，并打印找到的第一个与您传入参数同名的文件。

which 接受一个或多个参数。对于它的每个参数，它会向标准输出打印出当这个参数在 shell 提示符下输入时将会被执行的可执行文件的完整路径。它通过在环境变量 PATH 列出的目录中搜索可执行文件或脚本

#### PIPE & PTY

- PIPE 
	给子进程创建一根匿名管道，把子进程的某个标准流（stdin/stdout/stderr）接到进程里。

	stdout=PIPE：子进程写到 stdout 的内容。
	stdin=PIPE：写给 p.send(b"...") 的字节，会作为子进程的 stdin 输入。
	管道的特点：不是终端，没有行编辑/termios 能力；很多交互程序（尤其用 termios、curses）会因为 stdin 不是 TTY 而报错。

- PTY
	给子进程分配一个 伪终端（pseudo-terminal）。

	它看起来像真实终端设备（/dev/pts/N），所以：

	isatty() 为真
	termios.tcgetattr() / tcsetattr() 可用
	可以关闭回显、关闭规范模式（ICANON）等

#### setarch 

修改进程的“personality”标志来改变程序看到的系统架构（如让 64 位程序认为自己在 32 位环境中运行）或设置特定的内存布局标志。

- `setarch $(arch) /bin/sh -p`
	- `$(arch)` 获取当前系统架构

### 库

#### getent - 从名称服务切换库获取条目

`getent database [key ...]`

- `getent group sudo`
	查询指定组的信息 
	`grep '^sudo:' /etc/group`

## 文件系统 & 路径

### 浏览 & 基础操作


#### tree - 以树状形式列出目录内容

```sh
tree [-adfghilnopqrstuvxACDFNS] [-L level [-R]] [-H baseHREF] [-T title] [-o filename] [--nolinks] [-P pattern] [-I pattern] [--inodes] [--device] [--noreport] [--dirsfirst] [--version] [--help] [--filelimit #] [directory ...] 
```

#### namei

``` namei [options] pathname...```

递归列出目录中文件信息


#### basename 从文件名中剥离目录和后缀

打印移除任何前导目录组件的 NAME。如果指定，也移除尾随的 SUFFIX。

#### du - 估计文件空间使用情况

递归地总结每个文件（目录）的磁盘使用情况。

- `-c`, `--total`
    整合为总大小
	
- `-h, --human-readable`
	以人类可读的格式打印大小（例如，1K 234M 2G）

#### dmesg - 打印或控制内核环形缓冲区

`dmesg [-c] [-r] [-n level] [-s bufsize]`

dmesg 用于检查或控制内核环形缓冲区。


虽然现代 dmesg 版本通常移除了 `-F` 或 `-f`（从文件读取）选项，但在一些非常古老的系统或题目中，如果 dmesg 支持读取任意文件，可以直接用它来读取文件内容

#### findmnt - 查看文件系统

```
findmnt [options]

findmnt [options] device|mountpoint

findmnt [options] [--source] device [--target path|--mountpoint
mountpoint]
```

findmnt 将列出所有挂载的文件系统或搜索特定的文件系统。findmnt 命令可以在 /etc/fstab、/etc/mtab 或 /proc/self/mountinfo 中进行搜索。如果未给出设备或挂载点，将显示所有文件系统。

- `-o, --output 列表`
	定义输出列。参考 --help 输出以获取当前支持的列列表。如果未指定 --list 或 --raw 选项，TARGET 列包含树格式化。

	如果指定列表，默认列列表可以扩展（例如，findmnt -o +PROPAGATION）。
- `-T, --target path`
	定义挂载目标。如果路径不是挂载点文件或目录，则findmnt会以相反的顺序检查路径元素以获取挂载点（此功能仅在搜索内核文件时支持，不适用于--fstab）。当不希望检查路径元素且路径是严格指定的挂载点时，建议使用--mountpoint选项。

示例：打印 `/home/hacker/mc` 文件的挂载选项，此处为 `nosuid`，内核将忽略 suid 位
```sh
findmnt -T ./mc -o TARGET,SOURCE,FSTYPE,OPTIONS
TARGET       SOURCE FSTYPE   OPTIONS
/home/hacker none   virtiofs rw,nosuid,relatime
```

#### basename - 从文件名中去除目录和后缀

`basename NAME [SUFFIX]`

打印名称，并移除所有前导目录组件。如果指定，同时移除尾随后缀。

### 逆向工程/二进制

#### checksec

查看安全属性“声明”
- PIE：
	- 含义：位置无关可执行文件。开启 PIE 后，程序每次加载到内存时，其基地址（包括代码段、数据段等）都是随机的。
	- 影响：这实现了程序的地址空间布局随机化（ASLR）。攻击者无法提前预测任何函数或数据的固定地址，必须首先通过信息泄露来获取一个真实的地址，然后才能计算其他地址。
- Canary：
	- 含义：栈保护（金丝雀）已启用。在函数调用时，会在栈上的返回地址前插入一个随机值（canary），函数返回前会检查该值是否被改变。
	- 影响：如果发生栈溢出并覆盖了返回地址，必然会破坏这个 canary 值，导致程序检测到异常并立即终止。这直接阻止了普通的栈溢出攻击。在 CTF 中，你需要通过信息泄露来获取 canary 的值，或者在溢出时精确地绕过它。
- NX / Stack Executable：
	- 含义：数据执行保护。它通过 CPU 的 NX 位将内存中的数据区（如栈、堆）标记为不可执行。
	- 影响：即使你通过漏洞将恶意代码（shellcode）注入到栈或堆上，CPU 也无法在那里执行指令。这使得传统的“注入并跳转”攻击失效，攻击者必须转向 Ret2libc 或 ROP 等利用已有代码片段的技术。
- RELRO：Full 
	- 含义：重定位表只读。它主要保护程序的 GOT（全局偏移表），防止攻击者通过缓冲区溢出等手段篡改 GOT 表中的函数地址。
	- 影响：Full RELRO 使得 GOT 表在程序启动后完全不可写，这基本封杀了 GOT 表劫持（GOT overwrite）的攻击手法。在 CTF 中，这通常意味着你需要寻找其他利用路径，比如 ROP（Return-Oriented Programming）。
- stripped：
	是否剥离符号表（函数名、变量名等调试信息）

查看 cpu 是否支持此特性：`grep -m1 -oE 'shstk|ibt' /proc/cpuinfo`。  
编译时设置了静态特性，然而运行时内核/硬件不一定支持，支持 CET 的 CPU 消费级硬件出现在 2020 后，服务器级出现在 2021 年后。
- `shstk`
	含义：影子栈（Shadow Stack）。这是 Intel CET（Control-Flow Enforcement Technology）技术的一部分。它会为程序维护一个专门的、受保护的“影子栈”，用于存放返回地址的副本。
	影响：当函数返回时，CPU 会同时从普通栈和影子栈中弹出返回地址并进行比对。如果攻击者修改了普通栈上的返回地址，两个地址会不一致，CPU 会触发异常。这极大地增加了 ROP 攻击的难度。
- `ibt`
	- 含义：间接分支追踪（Indirect Branch Tracking）。同样是 CET 的一部分，它要求所有的间接跳转（如 jmp rax、call rdx）必须跳转到一个以特殊指令（如 ENDBR64）开头的位置。
	- 影响：这可以有效防御 JOP（Jump-Oriented Programming）和 COP（Call-Oriented Programming）等攻击，因为攻击者无法随意跳转到代码段的中间位置，只能跳转到合法的函数入口或指定的跳转板。

#### readelf

readelf 显示一个或多个 ELF 格式目标文件的信息。选项控制要显示的特定信息。

- `-a`  
	`--all`  
	等同于指定 --file-header、--program-headers、--sections、--symbols、--relocs、--dynamic、--notes 和 --version-info。

- `-l`
	查看头部表

- `-h, --file-header`
	显示文件开头处ELF头信息的内容。
- `-S`  
	`--sections`   
	`--section-headers`  
	显示文件节标题中包含的信息（如果有的话）。
	- `readelf -S /challenge/server | egrep '\.bss|\.data'`
- `-s`  
	`--symbols`  
	`--syms`
	显示文件符号表段的条目，如果它有的话。
- `-W`
	`--wide`
	不要将输出行拆分以适应 80 列。默认情况下，readelf 会拆分 64 位 ELF 文件的节标题和段列表行，以便它们适应 80 列。此选项会导致 readelf 将每个节标题或每个段单独打印在一行上，这在宽度超过 80 列的终端上更易读。
	- 注意：若不添加此选项可能导致过滤失败
- `-x <number or name>`  
	`--hex-dump=<number or name>`  
	以十六进制字节的形式显示指定段的內容。一个数字通过段表中的索引来标识特定的段；任何其他字符串则标识对象文件中所有具有该名称的段。

示例：
- 查找符号名为 `d` 的表地址
	```sh
	readelf /challenge/substitution-sorcery -sW | grep ' d$'
    40: 0000000000002140   128 OBJECT  LOCAL  DEFAULT   18 d
	```
	- 128 字节对象，第18段

#### nm - 列出来自目标文件中的符号

- `-a, --debug-syms`
	显示所有符号，包括仅供调试器使用的符号；通常这些符号不会被列出。
- `-D, --dynamic`
	显示动态符号而不是普通符号。这仅对动态对象有意义，例如某些类型的共享库。

#### patchelf - 修改 ELF 文件

`patchelf OPTION FILE ...`

PatchELF 是一个用于修改现有 ELF 可执行文件和库的简单工具。它可以更改可执行文件的动态加载器（"ELF 解释器"），以及更改可执行文件和库的 RPATH。

#### objcopy - 复制和转换目标文件

GNU objcopy 工具将一个目标文件的内容复制到另一个文件中。创建临时文件来执行其转换，并在完成后删除它们。

例：
- `objcopy --dump-section .text=shellcode-raw shellcode-elf`
	从 `shellcode-elf` 复制指令字段到 `shellcode-raw`

#### strip - 从对象文件中丢弃符号

strip 从对象文件 objfile 中丢弃所有符号。对象文件列表可以包含归档文件。至少必须给出一个对象文件。
strip 修改其参数中指定的文件，而不是以不同的名称写入修改后的副本。

#### objdump - 显示来自对象文件的信息

objdump 显示一个或多个目标文件的信息。选项用于控制显示特定的信息。

指令：
- `-d`
	`--disassemble`
	显示来自objfile的机器指令的汇编助记符。此选项仅反汇编预期包含指令的部分。
- `-M options`
	`--disassembler-options=options`  
	向反汇编器传递目标特定信息。仅在部分目标上受支持。如果需要指定多个反汇编器选项，则可以使用多个`-M` 选项，或者将它们组合成一个逗号分隔的列表。
	
	- `-M intel`  
		使用 intel 语法格式
- `-R`
	`--dynamic-reloc`
	打印文件的动态重定位条目。这仅对动态对象有意义，例如某些类型的共享库。至于`-r`，如果与`-d`或`-D`一起使用，重定位信息将穿插在反汇编中。
	- `objdump -R /challenge/server | egrep ' read@| write@'`

#### ROPgadget - 批量搜 gadget

<https://github.com/JonathanSalwan/ROPgadget>

默认只枚举以 ret/jmp/call 等“gadget 终结指令”收尾的短序列

查找内核工具时成功执行

注：
- ROPgadget 无法识别 `syscall; ret`

- `--binary`
	指定 ELF 文件
	`ROPgadget --binary /challenge/server | grep -n "leave ; ret"`

- `--only <key>`
	只显示特定的指令


#### rp++

rop查找工具

- `-f` 指定文件
- `-r num` 限制指令长度，
- `--unique` 去重的独特指令

例：
- `rp++ --unique -r2 -f /challenge/server`

#### ropper

rop查找工具

查找内核工具时爆掉

- `--file 文件名` 指定文件
- `--nocolor` 禁用终端颜色码
- `--all` 关闭去重复
- `--chain <generator>`   
	Generates a ropchain `[generator parameter=value[parameter=value]]`
	- available rop chain generators:
		- `execve` (execve[=<cmd>], default /bin/sh) [Linux x86, x86_64]
		- `mprotect`  (mprotect address=0xdeadbeef size=0x10000) [Linux x86, x86_64]
		- `virtualprotect` (virtualprotect address=0xdeadbeef) [Windows x86]

例：
- `ropper --file /challenge/server --nocolor`

#### ldd - 打印共享库依赖关系

`ldd [OPTION]... FILE...`

使用 `ldd` 查看文件的共享库依赖，使用得到的共享库路径，共享库文件将打印出版本信息

#### ndisasm - 80x86 二进制文件反汇编器

`ndisasm [ -o origin ] [ -s sync-point [...]] [ -a | -i ] [ -b bits ] [ -u ] [ -e hdrlen ] [ -k offset,length [...]] infile`

- `-b bits`
	指定 16 位、32 位或 64 位模式。默认为 16 位模式。

#### valgrind - 一套用于调试和分析程序的工具

`valgrind [valgrind-options] [your-program] [your-program-options]`

Valgrind 是一个用于调试和分析 Linux 可执行文件的灵活程序。它由一个核心组成，该核心在软件中提供了一个合成 CPU，以及一系列调试和分析工具。其架构是模块化的，因此可以轻松创建新工具，而不会干扰现有结构。


#### pahole - 显示和操作数据结构布局。

`pahole [options] files`

pahole 显示调试信息格式中编码的数据结构布局，支持 DWARF 和 CTF 格式。

这有助于优化重要数据结构的大小，确定数据结构起始偏移处的字段，调查 ABI 变化，以及更广泛地理解需要处理的新代码库。文件必须包含相关的调试信息。

这些信息可以存储在文件本身中，在 ELF 段中，或在另一个文件中。一种获取这些信息的方法是在编译时向编译器指定 -g 选项。这样，信息将被存储在 ELF 段中。

对于 DWARF 调试信息格式，这会添加 .debug_info ELF 段。对于 CTF，它位于一个 ELF 段 .SUNW_ctf 中。

大多数 Linux 发行版中可用的 debuginfo 软件包也受 pahole 支持，其中调试信息存储在单独的文件中。默认情况下，pahole 显示指定文件中所有命名结构的布局。

- 偏移为 10 进制

- `-C, --class_name=CLASS_NAMES`
	显示仅这些类。这可以是类名或文件URL（例如：file://class_list.txt）的逗号分隔列表。

例：
- `pahole -C task_struct /opt/linux/vmlinux`

#### rabin2 - 二进制文件查看

```sh
Usage: rabin2 [-AcdeEghHiIjlLMqrRsSUvVxzZ] [-@ at] [-a arch] [-b bits] [-B addr]
[-C F:C:D] [-f str] [-m addr] [-n str] [-N m:M] [-P[-P] pdb]
[-o str] [-O str] [-k query] [-D lang symname] | file
```

- `-z` 
	strings (from data section)

### 文件/目录管理

#### chroot - 使用特殊根目录运行命令或交互式 shell

`chroot [OPTION] NEWROOT [COMMAND [ARG]...]`

运行命令，并将根目录设置为 NEWROOT。





#### unlink - 调用unlink函数以删除指定的文件

```sh
unlink FILE
unlink OPTION
```

调用unlink函数以删除指定的FILE。

### 查找

#### bzip2, bunzip2 bzcat bzip2recover - 压缩或扩展文件

```
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
	压缩或解压缩到标准输出。

#### zip - 打包和压缩（归档）文件

`zip [-aABcdDeEfFghjklLmoqrRSTuvVwXyz!@$] [--longoption ...] [-b path] [-n suffixes] [-t date] [-tt date] [zipfile [file ...]] [-xi list]`

`zip 目标文件.zip 源文件`

- `zip - 源文件`
	使用单个短横线("-")作为 zip 文件名时，将 zip 文件写入标准输出。
	此时丢失原始的属主/属组。

- `-X, --no-extra` 
	不要保存额外的文件属性（OS/2 上的扩展属性、Unix 上的 uid/gid 和文件时间）。
	使用-X 选项时，zip 会删除所有旧字段，并且只包含 Unicode 和 Zip64 额外字段（目前这两个额外字段不能禁用）。

#### unzip - 解压 zip 归档文件

- `-l` 显示归档文件
- `-v` 显示归档文件详细信息



#### 7z

用法：7z <命令> [<开关>...] <归档文件> [<文件名>...]
       [<@列表文件...>]

<命令>
  a : 向归档文件中添加文件
  b : 基准测试
  d : 从归档文件中删除文件
  e : 从归档文件中提取文件（不使用目录名）
  h : 计算文件的哈希值
  i : 显示支持的格式信息
  l : 列出归档文件内容
  rn : 重命名归档文件中的文件
  t : 测试归档文件的完整性
  u : 更新归档文件中的文件
  x : 提取文件并保留完整路径

#### ar - 创建、修改和从存档中提取文件

`ar [--plugin name] [-X32_64] [-]p[mod [relpos] [count]] archive [member...]`

`ar rc 目标归档文件.a 源文件1 源文件2`

- `r`
	将文件 member...插入存档（带替换）。
- `c`
	创建归档。如果您请求更新，指定的归档如果不存在则总是会被创建。但除非您使用这个修饰符预先说明您期望创建它，否则会发出警告。
- `p`
	将归档中指定的成员打印到标准输出文件。如果指定了 v 修饰符，则在将成员内容复制到标准输出之前显示成员名称。
	如果你没有指定成员参数，归档中的所有文件都会被打印。


#### cpio - 复制文件到和从归档

在复制模式下，cpio 将文件复制到归档中。它从标准输入读取文件名列表，每行一个文件名，并将归档写入标准输出。

在复制传递模式下，cpio 将文件从一个目录树复制到另一个目录树，而无需实际使用存档。它从标准输入读取要复制的文件列表；目标目录作为非选项参数提供。

- `-o, --create`
	以复制出模式运行
- `-i, --extract`
	在复制输入模式下运行
- `-v, --verbose`
	列出处理的文件
- `-R [user][:.][group], --owner [user][:.][group]`
	在复制输出和复制传递模式下，将所有创建的文件的所有权设置为指定的用户和/或组。必须提供用户、组或两者。如果省略组但提供了':'或'.'分隔符，则使用给定用户登录组。只有超级用户可以更改文件的所有权。

示例：
- `ls | cpio -ov > directory.cpio`
	创建归档文件
- `cpio -iv -R hacker.hacker < directory.cpio`
	获取文件目录.cpio 中存档的文件，并设置属为hacker

#### genisoimage - 创建具有可选 Rock Ridge 属性的 ISO9660/Joliet/HFS 文件系统

`genisoimage [options] [-o filename] pathspec [pathspec ...]`

- `-o filename`
	指定 ISO9660 文件系统映像的输出文件。
- `-sort`
	对媒体上的文件位置进行排序。（错误信息泄露文件内容）

#### upx - 打包器

- `-压缩级别数字` 压缩级别

## 文本 / 文件内容处理

### 文本编辑器



#### emacs

开源文本编辑器

核心在于内置的 Emacs Lisp (Elisp) 编程语言。用户可以通过编写 Elisp 脚本或安装插件，实现几乎任何功能，包括编程、编译、调试、邮件收发、新闻阅读、文件管理、版本控制甚至浏览网页

#### nano - Nano 的另一个编辑器，一个增强版的免费 Pico 克隆版

`nano [OPTIONS] [[+LINE,COLUMN] FILE]...`

小巧的编辑器

### 查看 & 选择

#### readlink 读取符号链接指向的目标

示例：
- `readlink /proc/self/ns/net`  
	读取当前进程(/proc/self/)的 network namespace 的“命名空间句柄”符号链接。
	(Network namespace 是 Linux 的一种隔离机制：每个 netns 拥有自己独立的网络栈视图)

#### split - 将文件分割成多个片段

`split [OPTION]... [INPUT [PREFIX]]`

将 INPUT 固定大小的片段输出到 PREFIXaa、PREFIXab、...；默认大小是 1000 行，默认 PREFIX 是'x'。如果没有 INPUT，或者当 INPUT 是-时，读取标准输入。

- `-l, --lines=NUMBER`
	每个输出文件包含 NUMBER 行
	
- `--filter`：
	对每个分割后的文件块执行指定的命令。

### 过滤 & 匹配

####  rsync - a fast, versatile, remote (and local) file-copying tool

`rsync -av --exclude='*bzImage*' --exclude='*vmlinux*' /challenge/ "$MY_COPY_DIR"`

#### ed red

`ed [-GVhs] [-p string] [file]`
`red [-GVhs] [-p string] [file]`

ed 是一款行编辑器。它用于创建、显示、修改和以其他方式操作文本文件。red 是受限版的 ed：它只能编辑当前目录中的文件，并且不能执行 shell 命令。

命令：
- `,`
	缓冲区中的第一行到最后一行。这相当于地址范围 `1,$`。
- `(.,.)p`
	打印指定的行。如果从终端调用，ed 会在每页结束时暂停，直到输入换行符。当前地址会被设置为最后打印的行。
- `q`
	退出 ed。

示例：

```sh
ed /flag
,p
q
```


#### tac - 反向连接并打印文件

```sh
tac [OPTION]... [FILE]...
```

将每个 FILE 写入标准输出，最后一行在前。如果没有 FILE，或 FILE 为 -，则读取标准输入。

> 文件末尾需空行：无空行则最后两个元素拼接

长选项的强制参数对短选项也是强制的。

- **`-b`**, **`--before`**
  将分隔符附加在前面而不是后面
- **`-r`**, **`--regex`**
  将分隔符解释为正则表达式
- **`-s`**, **`--separator`**=*STRING*
  使用 STRING 作为分隔符而不是换行符
- **`--help`**
  显示此帮助并退出
- **`--version`**
  输出版本信息并退出

#### jq - 命令行 JSON 处理器

https://github.com/jqlang/jq


## 进程 & 终端控制

### 进程


#### pgrep && pkill

```sh
pgrep [-flvx] [-d delimiter] [-n|-o] [-P ppid,...] [-g pgrp,...]
[-s sid,...] [-u euid,...] [-U uid,...] [-G gid,...]
[-t term,...] [pattern]
```

```sh
pkill [-signal] [-fvx] [-n|-o] [-P ppid,...] [-g pgrp,...]
[-s sid,...] [-u euid,...] [-U uid,...] [-G gid,...]
[-t term,...] [pattern]
```

`pgrep` 会检查当前正在运行的进程，并将符合选择条件的进程 ID 列出到标准输出。

`pgrep -u root sshd`
只会列出名为 sshd 且由 root 拥有的进程。

`pkill` 会将指定的信号（默认为 SIGTERM）发送给每个进程，而不是在标准输出中列出它们。

参数：
- `-f`：通常情况下，模式仅与进程名匹配。当设置-f 时，将使用完整的命令行（包含路径）。
- `-x`：仅匹配名称（如果指定了 -f，则为命令行）完全匹配模式的进程。
	- `-fx`: 按完整命令行匹配（所有内容，包含参数）

#### parallel - 并行运行程序

```
parallel [options] [command] -- [argument ...]
parallel [options] -- [command ...]
```

parallel 运行指定的命令，并将其中指定的每个参数逐一传递给它。对每个参数都重复这一过程。任务可以并行运行。默认情况下，每个 CPU 运行一个任务。

如果 -- 前面没有指定命令，那么它后面的命令将并行运行。

选项：
- `-j maxjobs`  
	用于限制同时运行的任务数量。

参数：
- `--delay secs`
	控制任务启动间隔

#### nice - 以修改的调度优先级运行程序

`nice [OPTION] [COMMAND [ARG]...]`

使用调整后的优先级运行 COMMAND，这会影响进程调度。如果没有 COMMAND，则打印当前的优先级。优先级范围从-20（最有利于调度）到 19（最不利于调度）。

- `-n, --adjustment=N`
	将整数 N 加到优先级（默认值为 10）

- `nice cat /flag`

#### ionice - 获取/设置程序的 I/O 调度类和优先级

```
ionice [[-c class] [-n classdata] [-t]] -p PID [PID]...
ionice [-c class] [-n classdata] [-t] COMMAND [ARG]...
```

该程序用于设置或获取程序的 I/O 调度类别和优先级。如果未提供任何参数或仅给出 -p，ionice 将查询该进程当前的 I/O 调度类别和优先级。

Idle:
以空闲 I/O 优先级运行的程序只有在其他程序在定义的宽限期中没有请求磁盘 I/O 时才会获得磁盘时间。

Best effort:
这是任何未请求特定 I/O 优先级的进程的有效调度类。此类接受 0-7 的优先级参数，数字越小优先级越高。具有相同最佳努力优先级的程序以轮转方式提供服务。

Real time:
RT 调度类会首先获得对磁盘的访问权，无论系统内正在发生什么。因此，RT 类需要谨慎使用，因为它可能会使其他进程饥饿。与尽力而为类一样，定义了 8 个优先级级别，表示给定进程在每个调度窗口中会获得多大的时间片。这种调度类不允许普通（即非 root）用户使用。

- `-c class`
	调度类。0 表示无，1 表示实时，2 表示尽力而为，3 表示空闲。

- `-n classdata`
	调度类数据。如果该类接受参数，则定义类数据。对于实时和尽力而为，0-7 是有效数据。

- `-p pid`
	输入进程 PID 来查看或更改已运行的进程。如果未提供此参数，ionice 将使用给定参数运行列出的程序。

#### timeout - 带有时间限制运行命令

`timeout [OPTION] NUMBER[SUFFIX] COMMAND [ARG]...`

- `timeout 1 /bin/sh -p`

#### stdbuf - 运行 COMMAND，对其标准流进行修改的缓冲操作

`stdbuf OPTION... COMMAND`

参数：
- `-i, --input=MODE`
	调整标准输入流缓冲
- `-o, --output=MODE`
	调整标准输出流缓冲
- `-e, --error=MODE`
	调整标准错误流缓冲

如果 MODE 是'L'，相应的流将被行缓冲。此选项与标准输入无效。
如果 MODE 是'0'，相应的流将无缓冲。

示例：
- `stdbuf -i0 -o0 -e0 /bin/sh -p`

#### watch - 定期执行程序，全屏显示输出

`watch [-dhvt] [-n <seconds>] [--differences[=cumulative]] [--help] [--interval=<seconds>] [--no-title] [--version] <command>`

watch 会反复执行命令，显示其输出（第一个全屏）。这允许你观察程序输出随时间的变化。默认情况下，程序每 2 秒运行一次；使用 -n 或 --interval 指定不同的间隔。

-d 或 --differences 标志将突出显示连续更新之间的差异。--cumulative 选项使高亮显示"粘性"，显示所有曾经更改过的位置的实时显示。-t 或 --no-title 选项关闭显示顶部显示间隔、命令和当前时间的标题，以及其后的空行。

注意命令是通过"sh -c"传递的，这意味着你可能需要使用额外的引号才能达到预期效果。


- `-x, --exec`
	将命令直接传递给 exec 而非 sh -c
	- `watch -x cat /flag`

- `-n, --interval seconds `
	指定更新间隔。小于 0.1 和大于 2678400（31 天）的值会被转换为相应的边界值。在任何语言环境下，句点（`.`）和逗号（`,`）均可使用。可以通过 `WATCH_INTERVAL` 环境变量持久地设置非默认间隔（遵循相同的规则和格式）。


### 终端快捷键 & 作业控制（概念）

#### 终端快捷键与命令

`Ctrl-C`（即按住 `Ctrl` 键的同时按下 `C`）会向正在等待终端输入的应用发送"*中断*"信号，通常这将促使应用程序正常退出。

`Ctrl-Z` 将进程*挂起*至后台。

`Ctrl-R` 搜索历史命令，实时匹配当前输入
- `回车` 选定并执行
- `→` 右方向键选定并边界 

`fg` 命令——这是一个*内置命令*，它会获取被挂起的进程，将其恢复并放回你终端的*前台*。
`bg` 命令在*后台*恢复进程。

在命令末尾追加 `&` 符号可直接启动即进入*后台*运行！



#### tab 键补全

如果你在 shell 中按 tab 键，它会尝试推断你将要输入的内容并自动补全。  
默认情况下，`bash` 会在出现多个匹配选项时自动扩展到第一个分歧点（在此例中为 `fl`）。  
当你*第二次*按下 tab 键时，它会列出这些匹配选项。  

补全选项根据位置，即上下文不同，对应不同文件:
- 命令位置：补的是“可执行命令”（过滤掉普通文件）。
- 参数位置：补的是“文件名/路径”（不过滤普通文件）。

#### crontab - 创建、编辑和管理定时自动任务（cron 作业）

https://www.geeksforgeeks.org/linux-unix/crontab-in-linux-with-examples/

Crontab 配置
- Linux 系统上的每个用户都可以维护自己的 crontab 文件，用于存放计划任务。
- Crontab 文件用于定义哪些命令或脚本应该运行以及运行的时间。

所有 crontab 都遵循相同的语法：

```log
分钟 小时 日 月 星期 命令
分钟 (0 – 59)
小时 (0 – 23)
日 (1 – 31)
月 (1 – 12)
星期 (0 – 7) (星期日是 0 或 7，星期一是 1...)
```

格式
- `*` 表示所有可能的单位
	- `*/5` 每5时间单位1次

参数
- `-l` 列出
- `-e` 编辑

### shell

#### sh

```sh
sh [-abCefhimnuvx] [-o option]... [+abCefhimnuvx] [+o option]...
	[command_file [argument...]]

sh -c [-abCefhimnuvx] [-o option]... [+abCefhimnuvx] [+o option]...
	command_string [command_name [argument...]]

sh -s [-abCefhimnuvx] [-o option]... [+abCefhimnuvx] [+o option]...
	[argument...]
```

选项
- `-c`
	- 从 `command_string` 操作数读取命令。将特殊参数 `0`（参见第 2.5.2 节“特殊参数”）的值设置为 `command_name` 操作数的值，并将位置参数（`$1`、`$2` 等）依次设置为其余参数操作数的值。不从标准输入读取任何命令。


示例
```sh
sudo sh -c "多条命令"
```

#### bash

```sh
bash [options] [command_string | file]
```

- `-c`

	- 如果指定了 `-c` 选项，则从第一个非选项参数 `command_string` 中读取命令。如果 `command_string` 之后还有参数，则第一个参数会被赋值给 `$0`，其余参数则会被依次赋值给位置参数。对 `$0` 的赋值会设置 shell 的名称，该名称将用于警告和错误消息。

示例
```sh
sudo bash -c "多条命令"
```

### 终端多路复用

#### Screen

```sh
screen [ -options ] [ cmd [ args ] ]
screen -r [[pid.]tty[.host]]
screen -r sessionowner/[[pid.]tty[.host]]
```
Screen 是一个全屏窗口管理器，可以在多个进程（通常是交互式 shell）之间切换物理终端。  
当 screen 被调用时，它会创建一个包含 shell（或指定的命令）的单个窗口，然后退出以便你可以像平常一样使用该程序。

当您完成命令行操作后，输入 `exit` 或按下 `Ctrl-D` 即可退出 screen 会话。
随后 screen 将终止并返回到您的*原始* shell。

在其默认配置中，`Ctrl-A` 是激活所有 `screen` 快捷键的按键：
- `Ctrl-A c` - 创建一个新窗口
- `Ctrl-A n` - 切换到下一个窗口
- `Ctrl-A p` - 切换到上一个窗口
- `Ctrl-A 0` 到 `Ctrl-A 9` - 直接跳转到窗口 0-9
- `Ctrl-A "` - 调出所有窗口的选择菜单

通过按下 `Ctrl-A`，然后按 `d`（代表**d**etach）即可实现分离。
请记住：按住 Ctrl 键并按下 A，然后松开这两个键再按下 d 键。

若要**重新连接**，您可以使用 `screen` 的 `-r` 参数：



参数：
- `-ls` and `-list`  
	打印出包含 pid.tty.host 字符串的列表，这些字符串用于标识你的 screen 会话。
	- 'detached'的会话可以用'screen -r'恢复。
	- 'attached'的会话正在运行并且有一个控制终端。
	- 'multi' 会话在多用户模式下运行。
- `-r [pid.tty.host]`  
	`-r sessionowner/[pid.tty.host]`  
	恢复一个已分离的screen会话。除了与-d/-D组合的其他选项外，不得指定其他选项，但可能需要`[pid.]tty.host`的前缀来区分多个已分离的screen会话。第二种形式用于连接到另一个用户在多用户模式下运行的screen会话。这表示screen应该在另一个用户的目录中查找会话。这需要setuid-root。

## 权限 & 用户管理
 
### 访问控制 getfacl setfacl getcap setcap capsh getpcaps
 
- ACL  
    ls -l 末尾出现 +：表示该文件/目录存在 ACL（或其他扩展权限信息）。
    - 对象：  
        **文件/目录**访问（r/w/x、遍历、默认继承）
    - 模型：
        DAC（自主访问控制）扩展
    - 细节：
        ACL 有个 `mask` 会“限制”除 owner 以外的命名用户/组与所属组权限
    - 命令：
        - `getfacl <file>` 查看 ACL 明细
            - `-R, --recursive`：
                递归查看目录下所有条目
            - `-p, --absolute-names`：
                输出绝对路径（递归时更好用）
            - `-c, --omit-header`：
                省略头部注释（脚本处理方便）

            - 常见典型行：
                - `user::rwx`：文件 owner 的权限
                - `user:alice:rw-`：命名用户 alice 的权限（ACL 的价值所在）
                - `group::r-x / group:dev:rw-`：文件所属组 / 命名组
                - `mask::r-x`：mask（掩码），会“卡住”除 owner 之外的用户/组权限上限
                - `other::---`：其他人权限
                - `default:user:alice:...`：目录的默认 ACL（新建子文件/目录时继承）

                常见意外：给了 user:alice:rw-，但实际生效是 rw- ∧ mask，所以看起来“没生效”。
        - `setfacl`
            - `-m, --modify ACLSPEC`：添加/修改条目
                ACLSPEC 常见写法：
                - `u:alice:rw`（命名用户）
                - `g:dev:rx`（命名组）
                - `m::r`（设置 mask）
            - `--set ACL`：用给定 ACL 整体覆盖
            - `-x, --remove ACLSPEC`：删除指定条目
            - `-b, --remove-all`：删除所有访问 ACL（回到纯 rwx）
            - `-R`：递归（对目录树批量设置时）
- Capabilities
    Capabilities 分两类：文件 capabilities（filecap）和进程 capabilities（进程运行时携带）。
    - 对象：  
        **进程**特权操作（绑定低端口、改网络配置、加载内核模块等）
    - 模型：
        root 特权拆分后的内核权限模型
    - 命令：
        - `getcap <binary>` 
            查看可执行**文件** capabilities
            - `-r, --recursive DIR` 
                递归查目录

            - 输出：
                `/path/prog cap_net_bind_service=ep` 
                含义：该文件执行时可获得 `cap_net_bind_service`，集合标志是 `e/p/i`。
                - `e` = Effective：执行后立即生效
                - `p` = Permitted：允许集合（上限）
                - `i` = Inheritable：可继承集合（和后续 exec/ambient 等联动）

        - `setcap` 
            设置/移除文件 capabilities
            - `setcap 'cap_xxx=+ep' FILE`：
                给文件加 capability
            - `setcap -r FILE`：
                移除该文件所有 capability
        - `capsh`
            - `capsh --print`：
                打印当前进程 capability 状态（含 bounding set 等）
        - `getpcaps PID`：
            查看某个**进程**的 capabilities

### 身份信息

#### w —— 显示当前登录用户及其操作

```sh
w [option ...] [user]
```

#### last —— 登录历史记录

#### id

```sh
id [选项]... [用户名]
```

打印指定用户名的用户和组信息，或者（当省略用户名时）为当前用户打印。

#### groups

查看当前用户组

### 权限位

#### chmod

```sh
chmod [OPTION]... MODE[,MODE]... FILE...
chmod [OPTION]... OCTAL-MODE FILE...
chmod [OPTION]... --reference=RFILE FILE...
```

`chmod`根据mode修改每个给定文件的文件模式位，mode可以是表示要进行的更改的符号表示，也可以是表示新模式位的位模式的八进制数。
符号模式的格式为`[ugoa...][[+-=][perms...]...]`，其中perms是集合`rwxXst`中的零个或多个字母，或者是集合`ugo`中的一个字母。可以给出多个符号模式，用逗号分隔。
字母组合`ugoa`控制将更改哪个用户的文件访问权限：文件的所有者（`u`）、文件组中的其他用户（`g`）、文件组外的其他用户（`o`）或所有用户（`a`）。如果没有给出这些，效果就像给出了`a`一样，但umask中设置的位不会受到影响。

suid 对脚本通常无效，但对 ELF 二进制有效
`S` 权限位表示设置了 suid 但未设置 x

运算符：
- `+` 将选定的文件模式位添加到每个文件的现有文件模式位
- `-` 将它们移除
- `=` 将它们覆盖添加
	- `=-`  在覆盖运算符右侧使用 `-` 清除权限

通常，您需要是文件的所有者才能更改其权限。

注，使用使用 `,` 将多个模式链接到 `chmod` 命令，以同时修改多个模式。

### 文件所有者 / 组

#### chgrp

```sh
chgrp [OPTION]... GROUP FILE...
chgrp [OPTION]... --reference=RFILE FILE...
```

将每个文件的组改为 GROUP。使用--reference 选项时，将每个文件的组改为 RFILE 的组。

除非您是文件的所有者*并且*是新组的成员，否则这通常需要 `root` 访问权限

#### chown

```sh
chown [选项]... [所有者][:[组]] 文件...
chown [选项]... --reference=RFILE 文件...
```

chown (**ch**ange **own**er，更改所有者) 更改每个给定文件的用户和/或组所有权:

- 如果只给出一个所有者（用户名或数字用户 ID），则该用户将成为每个给定文件的所有者，并且文件组不会改变。
- 如果所有者后面跟着一个冒号和一个组名（或数字组 ID），并且它们之间没有空格，则文件的组所有权也会改变。
- 如果用户名后面跟着一个冒号但没有组名，则该用户将成为文件的所有者，并且文件的组将更改为该用户的登录组。
- 如果给出了冒号和组，但省略了所有者，则只更改文件的组；在这种情况下，`chown` 执行与 `chgrp` 相同的功能。
- 如果只给出一个冒号，或者整个操作符为空，则既不改变所有者也不改变组。

通常，`chown` 只能由 `root` 用户调用。

tips
- chown 自动清空 suid

### 身份切换 & 认证

#### passwd

`passwd [-k] [-l] [-u [-f]] [-d] [-e] [-n mindays] [-x maxdays] [-w warndays] [-i inactivedays] [-S] [--stdin] [username]`

passwd 用于更新用户的身份验证令牌。

passwd 命令启用了 SUID（保存用户 ID）。当执行 passwd 命令时，当前生效的有效用户 ID（EUID）会被复制到保存用户 ID（即 root）。因此，通过这种技术，普通用户账户可以更新其密码在 /etc/shadow 文件中。

具有 root 权限才能更改其他所有用户的密码

#### chage

`chage [options] [LOGIN]`

修改密码更改之间的天数以及上次密码更改的日期。系统使用这些信息来确定用户何时需要更改密码。

#### gpasswd

#### newgrp 

`newgrp target_group`
输入组密码，验证通过后会启动一个新的子 Shell。在这个新 Shell 中，你的“有效组 ID”会切换到目标组。

#### sg

`sg target_group 'id'`
输入组密码，在当前 Shell 的“有效组 ID”会切换到目标组，用于执行单条命令。

### 权限与安全模型

```sh
-rw-r--r-- 1 hacker hacker    0 May 22 13:42 college_file
drwxr-xr-x 2 hacker hacker 4096 May 22 13:42 pwn_directory
```

第一个字符是文件类型。
接下来的九个字符是文件或目录的实际访问权限，分为三组：
1. 前三个字符表示所有者的权限
2. 中间三个字符表示所属组的权限
3. 最后三个字符表示所有其他访问（例如其他用户和其他组）对文件的权限

有两列显示拥有文件的*用户*（本例中为用户 `hacker`）和拥有文件的*组*（本例中同样为组 `hacker`）。

`t` 位即*粘滞位*。
粘滞位意味着该目录仅允许文件所有者重命名或删除目录中的文件，
- 疑问：❓ 粘滞目录下的符号链接跟随，当符号链接拥有者与进程 euid 或目录拥有者不同则无法跟随

内核在检查权限时，只会使用“最具体”那一组位。
具体规则（从高到低优先级）：

1. 如果你是这个文件的所有者 → 只看 `u`（user） 那三位
2. 否则，如果你属于这个文件的组 → 只看 `g`（group） 那三位
3. 否则 → 只看 `o`（other） 那三位

Linux 文件/目录权限的一个微妙特性：对目录拥有写入权限的任何人都可以*移动*和*删除*其中的文件。
即，拥有目录写入权限，但不拥有目录下文件权限时，仍可对目录下文件进行移动与删除。然后写入同名文件进行伪造。

典型用户主目录中的许多文件*默认即为全局可读*，尽管这些文件常被用于存储敏感信息。
除非显式修改权限，否则 `.bashrc` 就是全局可读的！

SUID:

```sh
-rwsr-xr-x 1 root root 232416 Dec 1 11:45 /usr/bin/sudo
```

原本是可执行位`x`的位置出现的 `s` 表示该程序是*带有 SUID* 可执行的。
这意味着，无论哪个用户运行该程序（只要他们有执行权限），该程序都将以其所有者用户（在本例中为 `root` 用户）的身份执行。
作为文件的所有者，您可以使用 chmod 设置文件的 SUID 位


## 网络 & 安全工具

### 状态信息 & 配置

#### service —— 运行初始化脚本

```sh
service --status-all
```

`service --status-all` runs all init scripts, in alphabetical order, with the `status` command. 

#### ip - 显示/操作路由、设备、策略路由和隧道

```
ip [ OPTIONS ] OBJECT { COMMAND | help }
OBJECT := { link | addr | addrlabel | route | rule | neigh | tunnel | maddr | mroute | monitor }
OPTIONS := { -V[ersion] | -s[tatistics] | -r[esolve] | -f[amily] { inet | inet6 | ipx | dnet | link } | -o[neline] }
```
ip addr add 10.0.0.2/24 dev eth0
配置：
- `ip addr add A.B.C.D/24 dev 网络接口名`  
	对网络接口(如 eth)设置 ip 地址与网段

#### iptables - IPv4 数据包过滤和 NAT 的管理工具

https://git.netfilter.org/

http://wiki.netfilter.org/wiki-nftables/index.php?title=Netfilter_hooks

https://iptables.org/documentation/HOWTO/netfilter-hacking-HOWTO-3.html

iptables 用于设置、维护和检查 Linux 内核中 IP 数据包过滤规则的表。
可以定义多个不同的表。每个表包含若干内置链，也可能包含用户定义的链。

目标：
防火墙规则指定了数据包的标准和一个目标。如果数据包不匹配，则检查链中的下一条规则；如果匹配，则由目标值指定的下一条规则将被执行，该目标值可以是用户定义链的名称，或者是 ACCEPT、DROP、QUEUE 或 RETURN 等特殊值之一：

- `ACCEPT` 表示允许数据包通过。
- `DROP` 表示丢弃数据包。
- `QUEUE` 表示将数据包传递给用户空间。
- `RETURN` 表示停止遍历此链并在前一个（调用）链中的下一个规则处继续。

表：
目前有三个独立的表

- `-t, --table table`  
	这个选项指定了命令应该操作的包匹配表。

	- filter:  
		这是默认表（如果未传递 -t 选项）。它包含内置链 INPUT（用于发往本地套接字的包）、FORWARD（用于通过该设备路由的包）和 OUTPUT（用于本地生成的包）。
	- nat:  
		当遇到创建新连接的数据包时，会查询此表。它包含三个内置链：PREROUTING（在数据包刚到达时立即修改）、OUTPUT（在本地生成的数据包路由之前修改）和 POSTROUTING（在数据包即将外出时修改）。
	- mangle:  
		此表用于专门的数据包修改。在内核 2.4.17 之前，它有两个内置链：PREROUTING（在数据包路由之前修改传入的数据包）和 OUTPUT（在本地生成的数据包路由之前修改）。自内核 2.4.18 起，还支持另外三个内置链：INPUT（用于进入设备本身的数据包）、FORWARD（用于修改通过设备路由的数据包）和 POSTROUTING（在数据包即将外出时修改）。
	- raw:  
		此表主要用于配置与 NOTRACK 目标结合使用的连接跟踪豁免。


命令：
- `-A, --append chain rule-specification`  
	将一个或多个规则附加到选定链的末尾。

- `-I, --insert chain [rulenum] rule-specification`
	将一条或多条规则插入到选定链中作为给定的规则编号。因此，如果规则编号为 1，则规则或规则将插入到链头。如果没有指定规则编号，这也是默认行为。

- `-D, --delete chain rule-specification`  
	`-D, --delete chain rulenum`  
	从选定链中删除一条或多条规则。该命令有两种版本：规则可以指定为链中的编号（从 1 开始为第一条规则）或匹配规则。

- `-L, --list [chain]`
	列出选定链中的所有规则。如果没有选定链，将列出所有链。
- `-Z, --zero [chain [rulenum]]`
	清零所有链中的数据包和字节计数器，或仅清零指定链的计数器，或仅清零链中指定规则的计数器。也可以同时指定 `-L, --list`（列表）选项，以便在计数器被清零之前立即查看它们（参见上文）。

参数：
- `-p, --protocol [!] protocol`  
	规则或要检查的数据包的协议。  
	指定的协议可以是 tcp、udp、icmp 或 all，也可以是一个数值，代表这些协议中的一种或另一种。  
	在协议前使用 "!" 参数可以反转测试结果。

- `-s, --source [!] address[/mask]`
	源地址指定。  
	地址可以是网络名称、主机名（请注意，使用远程查询（如 DNS）解析任何名称是一个非常糟糕的想法）、网络 IP 地址（带/掩码）或普通 IP 地址。掩码可以是网络掩码或普通数字，指定网络掩码左侧的 1 的个数。因此，掩码 24 相当于 255.255.255.0。在地址指定前使用"!"参数会反转地址的意义。标志--src 是这个选项的别名。	

- `-d, --destination [!] address[/mask]`
	目标指定。有关语法细节，请参阅 -s（源）标志的描述。标志 --dst 是此选项的别名。

- `-j, --jump target`  
	这指定了规则的目标；即，如果数据包匹配该规则要做什么。

匹配扩展：
iptables 可以使用扩展包匹配模块。这些模块有两种加载方式：隐式加载，当指定`-p` 或`--protocol` 时；或者使用`-m` 或`--match` 选项，后跟匹配模块的名称。

- `--source-port [!] port[:port]`  
	源端口或端口范围指定。  
	这可以是一个服务名称或端口号。也可以使用 port:port 格式指定一个包含范围。如果省略第一个端口，则默认为 "0"；如果省略最后一个端口，则默认为 "65535"。如果第二个端口大于第一个端口，它们将被交换。标志 `--sport` 是这个选项的便捷别名。

- `--destination-port [!] port[:port]`  
	目标端口或端口范围指定。标志 `--dport` 是此选项的方便别名。



目标扩展:
- `REDIRECT`  
	这个目标仅在 nat 表中有效，在 PREROUTING 和 OUTPUT 链中，以及仅从这些链调用的用户定义链中。它通过将目标 IP 更改为入站接口的主地址来将数据包重定向到机器本身（本地生成的数据包映射到 127.0.0.1 地址）。

	- `--to-ports port[-port]` 
		这指定了要使用的目标端口或端口范围：如果没有这个选项，目标端口将不会被修改。只有当规则同时指定 -p tcp 或 -p udp 时才有效。

- `REJECT`  
	这用于向匹配的数据包发送错误数据包：否则它等同于 DROP，因此它是一个终止目标，结束规则遍历。这个目标仅在 INPUT、FORWARD 和 OUTPUT 链中有效，以及仅从这些链调用的用户定义链中有效。
	

其他参数
- -F 清空所有链
- -i 接口名
- -L 列出所有设置


**其他选项**

可以指定以下附加选项：

- `-v, --verbose`
	详细输出。此选项使 `list` 命令显示接口名称、规则选项（如果有）以及 TOS 掩码。数据包和字节计数器也会列出，并分别使用后缀 'K'、'M' 或 'G' 表示 1000、1,000,000 和 1,000,000,000 的倍数（但请参阅 `-x` 选项以更改此行为）。对于追加、插入、删除和替换操作，此选项会打印有关所操作规则或规则的详细信息。`-v` 可以多次指定，以可能输出更详细的调试信息：指定两次时，`iptables-legacy` 会转储 libiptc 中的表信息和条目，而 `iptables-nft` 会以 netlink（VM 代码）表示形式转储规则；指定三次时，`iptables-nft` 还会转储发送给内核的任何 netlink 消息。

- `-n, --numeric` 
	数字输出。IP 地址和端口号将以数字格式打印。默认情况下，程序会尝试将其显示为主机名、网络名或服务名（在适用时）。
- `--line-numbers`
	在列出规则时，在每条规则的开头添加行号，行号对应该规则在链中的位置。

示例：
- `iptables -L [表名/链名] -n -v --line-numbers`
	列出所有（或特定）设置，显示详细的数字输出，包含行号

#### ss - 另一个用于调查套接字的工具

- `-n，--numeric`
	以数字形式显示服务
- `-l，--listening`
	仅显示监听套接字(默认被忽略)
- `-p，--processes`
	显示使用套接字的进程

- `-t, --tcp`
	显示 TCP 套接字
- `-u, --udp`
	显示 UDP 套接字

#### ethtool

- `-i --driver 设备名称`
	查询指定网络设备的关联驱动信息。（例如，查看虚拟机网卡类型）

#### nft

### 基础下载/请求


#### wget - 非交互式网络下载器

`wget [option]... [URL]...`

参数
- `--no-verbose` 关闭详细输出
- `-i file, --input-file=file`
	从本地或外部文件中读取 URL。如果将-指定为文件，则 URL 将从标准输入中读取。（使用./-从名为-的文件中逐字读取。）
	字母自动转为小写。
- `-O file, --output-document=file`
	文档不会被写入到相应的文件中，而是所有文档将被连接在一起并写入到 `file` 中。如果将-用作 `file`，文档将被打印到标准输出，禁用链接转换。（使用./-将文档实际打印到名为-的文件中。）

	使用`-O` 的意图并非仅仅是“使用 `URL` 中的文件名而不是 `file`”；它更类似于 shell 重定向：`wget -O file http://foo` 的意图是像 `wget -O - http://foo > file` 一样工作；file 将被立即截断，所有下载的内容都将写入其中。

- `-r`
	递归下载

- `-l inf`
	无限深度

- `-nH`
	不创建以主机名命名的文件夹

- `-c`
	断点续传

- `ftp://用户名:密码@主机`
	使用 ftp 协议下载

### 网络监听

#### wireshark

```
wireshark [ -a <捕获自动停止条件> ] ... [ -b <捕获环形缓冲区选项> ] ... [ -B <捕获缓冲区大小（仅限 Win32）] [ -c <捕获数据包数量> ] [ -C <配置配置文件> ] [ -D ] [ --display=<要使用的 X 显示> ] [ -f <捕获过滤器> ] [ -g <数据包编号> ] [ -h ] [ -H ] [ -i <捕获接口>|- ] [ -k ] [ -K <密钥表> ] [ -l ] [ -L ] [ -m <字体> ] [ -n ] [ -N <名称解析标志> ] [ -o <偏好/最近设置> ] ... [ -p ] [ -P <路径设置>] [ -Q ] [ -r <输入文件> ] [ -R <读取（显示）过滤器> ] [ -S ] [ -s <捕获快照长度> ] [ -t ad|a|r|d|dd|e ] [ -v ] [ -w <输出文件> ] [ -y <捕获链路类型> ] [ -X <扩展选项> ] [ -z <统计信息> ] [ <输入文件> ]
```

GUI：
`follow - TCP Stream `查看 
    把同一条 TCP 连接里的所有 payload，按顺序重组并展示出来

#### tshark - 抓取和分析网络流量

TShark 是一款网络协议分析器。它可以从活动网络中抓取数据包，或从先前保存的抓取文件中读取数据包，将数据包的解码形式打印到标准输出，或写入文件。TShark 的原生抓取文件格式是 libpcap 格式，这也是 tcpdump 和其他各种工具使用的格式。

TShark 能够检测、读取和写入 Wireshark 支持的相同捕获文件。

参数：
- `-r <infile>`  
	从 infile 中读取数据包，可以是任何支持的捕获文件格式（包括压缩文件）。这里不能使用命名管道或 stdin！

#### tcpdump 抓包工具

- `-n`：不做名字解析
- `-i 接口`：指定抓包接口（如，eth0）
- `-vv`：更详细输出
- `-A`: 以ASCII格式显示内容
- `-X`: 以十六进制和ASCII格式显示
- `-e` 打印链路级头部

示例：
- `tcpdump -ni eth0 -vv 'arp or icmp or (udp and host 10.0.0.2)'`
- `sudo tcpdump -i ens32 -n -e "tcp port 23"`

### 网络扫描 & 连接

#### socat - 多用途中继 (SOcket CAT)

https://linux.die.net/man/1/socat

`CWsocat [options] <address> <address>`

Socat 是一个基于命令行的工具，用于建立两个双向字节流并在它们之间传输数据。由于这些流可以由多种不同类型的数据接收端和发送端（参见地址类型）构建，并且可以应用许多地址选项到这些流上，因此 socat 可以用于多种不同的目的。

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


#### ping, ping6 - 向网络主机发送 ICMP ECHO_REQUEST

参数：
- `-c count`  
	在发送 count 个 ECHO_REQUEST 数据包后停止。使用截止时间选项时，ping 会等待 count 个 ECHO_REPLY 数据包，直到超时过期。
- `-W timeout`  
	等待响应的时间，以秒为单位。
- `-b`
    广播地址

#### hping3

- `-S --syn`
	Set SYN tcp flag.
- `-p --destport [+][+]dest port`
	Set destination port, default is 0
	`+`  用来递增端口号
- `-c --count count`
	Stop after sending (and receiving) count response packets. 
- `-t --ttl time to live`
	Using this option you can set TTL (time to live) of outgoing packets

示例
- `sudo hping3 -S -p 32769 --ttl 5 -c 1 目标IP`
	测试端口伪造来源：在很近的地方收到的 ISP 伪造的响应
	
#### mtr - 路由延迟测试

- `-r, --report` 
	报告模式：10次测试后打印报告并终止

- `-w`
	宽打印，包含完整主机名

- `-F 输入文件`
	文件列表，空行分隔

#### ncat

[手册](https://nmap.org/book/ncat-man.html)
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

#### nc - 任意 TCP 和 UDP 连接/监听

```
nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
	  [-m minttl] [-O length] [-P proxy_username] [-p source_port]
	  [-q seconds] [-s sourceaddr] [-T keyword] [-V rtable] [-W recvlimit]
	  [-w timeout] [-X proxy_protocol] [-x proxy_address[:port]]
	  [destination] [port]
```

nc（或 netcat）工具可用于各种涉及 TCP 或 UDP 的任务。它可以打开 TCP 连接、发送 UDP 数据包、监听任意 TCP 和 UDP 端口、进行端口扫描，并处理 IPv4 和 IPv6。与 telnet(1) 不同，nc 脚本编写得很好，并将错误消息输出到标准错误而不是像 telnet(1) 那样发送到标准输出。

参数：
- `-v`  
	标志来开启详细输出
- `-u` 
	使用 UDP 而不是默认的 TCP 选项。如监听udp数据包
- `-l`  
	监听传入连接而不是向远程主机发起连接。
- `-w timeout`  
	如果连接和标准输入在超过 timeout 秒后处于空闲状态，则连接将被静默关闭。
- `-N`   
	在输入结束后通过 shutdown(2) 系统调用关闭网络套接字。
	

示例：
- `nc -l 1234`  
	监听 1234 端口上的连接
- `nc 127.0.0.1 1234`  
	连接到 ip 127.0.0.1 端口 1234

#### host

```host [-aCdilrTvVw] [-c class] [-N ndots] [-t type] [-W time] [-R number] [-m flag] [-p port] hostname [server]```

参数
- `-t <type>` 指定查询类型，如 `ns`为名字服务器
    - `host -t PTR <反向IP>.in-addr.arpa` 反向查询
        将IP地址转换为反向格式（如 192.168.1.100 → 100.1.168.192.in-addr.arpa）
- `-l <域名> [权威 DNS 服务器地址]` 使用 AXFR（区域传输）协议，列出一个域的所有主机记录
- `<server>` 指定本次查询的 DNS 服务器

#### traceroute - 路由跟踪

- `-m 跳数`
	设置最大 hop 跳数

### 加密 & 哈希

#### base64

`base64 [OPTION]... [FILE]`

- `-d, --decode`
	Decode data.

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

例
- 使用 sha1 哈希签名
	```sh
	echo -n 'str' | openssl dgst -sha1 -hmac '密钥'
	```


#### openvpn – 安全的 IP 隧道守护进程。

**概要**  
`openvpn [ 选项 ... ]`

**简介**  
OpenVPN 是由 James Yonan 开发的开源 VPN 守护进程。由于 OpenVPN 试图成为一个提供极大灵活性的通用 VPN 工具，因此本手册页中包含了大量选项。如果你是 OpenVPN 新手，你可能想跳至后面的示例部分，在那里你将看到如何在命令行上构建简单的 VPN，甚至无需配置文件。

另请注意，OpenVPN 网站上提供了更多文档和示例：http://openvpn.net/

如果你想查看本手册的简短版本，请参阅 `openvpn` 的使用信息，该信息可通过不带任何参数运行 `openvpn` 获得。

**描述**  
OpenVPN 是一个健壮且高度灵活的 VPN 守护进程。它支持 SSL/TLS 安全、以太网桥接、通过代理或 NAT 进行的 TCP 或 UDP 隧道传输、动态 IP 地址和 DHCP 支持、可扩展至成百上千个用户，并可移植到大多数主要的操作系统平台。

OpenVPN 与 OpenSSL 库紧密绑定，其大部分加密能力均源自该库。

OpenVPN 支持使用预共享密钥（静态密钥模式）进行传统加密，或使用客户端和服务器证书进行公钥安全（SSL/TLS 模式）加密。它也支持非加密的 TCP/UDP 隧道。

OpenVPN 被设计为与大多数平台上存在的 TUN/TAP 虚拟网络接口协同工作。

总的来说，OpenVPN 旨在提供 IPSec 的许多关键功能，但又具有相对轻量级的特性。

## 容器、虚拟化、沙盒

### unshare - 在父命名空间中运行程序，使某些命名空间分离

`unshare [options] program [arguments]`

从父进程中分离指定的命名空间，然后执行指定的程序。

- `-p, --pid[=file]`
	创建新的 PID 命名空间。如果指定了 file，则通过在 file 位置创建绑定挂载来使命名空间持久化。（如果未同时指定--fork 选项，持久化 PID 命名空间的创建将失败。）
- `-u, --uts[=file]`
	创建新的 UTS 命名空间。如果指定了 file，则通过在 file 位置创建绑定挂载来使命名空间持久化。
- `-m, --mount[=file]`
	创建新的挂载命名空间。如果指定了文件，则通过在文件上创建绑定挂载来使命名空间保持持久。注意，文件必须位于传播类型不是共享的挂载上（否则将出错）。不确定当前设置时，可以使用命令 findmnt -o+PROPAGATION。
- `-f, --fork`
	将指定的程序作为 unshare 的子进程而不是直接运行它。这在创建新的 PID 命名空间时很有用。注意，当 unshare 等待子进程时，它会忽略 SIGINT 和 SIGTERM，并且不会将任何信号转发给子进程。需要向子进程发送信号。
- `--mount-proc[=mountpoint]`
	在运行程序之前，将 proc 文件系统挂载到 mountpoint（默认是 /proc）。这在创建新的 PID 命名空间时很有用。它还意味着创建一个新的挂载命名空间，因为 /proc 挂载会否则扰乱系统上的现有程序。新的 proc 文件系统明确挂载为私有（使用 MS_PRIVATE|MS_REC）。

### nsenter - 在不同的命名空间中运行程序

`nsenter [options] [program [arguments]]`

nsenter 命令在命令行选项中指定的命名空间中执行程序。如果未给出程序，则运行 "${SHELL}"（默认：/bin/sh）。

- `-m, --mount[=file]`
	进入挂载命名空间。如果没有指定文件，则进入目标进程的挂载命名空间。如果指定了文件，则进入文件指定的挂载命名空间。

### qemu-img


- `convert [-c] [-p] [-f fmt] [-t cache] [-O output_fmt] [-o options] [-S sparse_size] filename [filename2 [...]] output_filename`
	将磁盘镜像 `filename` 转换为目标格式 `output_fmt` 的磁盘镜像 `output_filename`。  

例
- `qemu-img convert x.vdi -O vmdk x.vmdk`

### vagrant

- box
    - `vagrant box list` 查看 box 列表
    - `vagrant box add --name 虚拟机名称 box文件路径` 添加 box 到虚拟机
    - `vagrant box remove box名称` 移除特定 box
- 虚拟机
    - `vagrant up` 启动所有虚拟机
        - `vagrant up 虚拟机名称` 启动特定虚拟机
    - `vagrant reload 虚拟机名称` 重新加载虚拟机
    - `vagrant destroy 虚拟机名称` 销毁虚拟机
	- 管理
		- `vagrant winrm -c "命令字符串" 虚拟机` 在虚拟机中执行命令
		- `vagrant winrm-config 虚拟机` 显示虚拟机配置

- 插件
    - `vagrant plugin install 插件名称` 安装插件

- `vagrant status` 查看状态
- `vagrant port 虚拟机名称` 查看虚拟机端口

配置文件示例：
- [AD-lab](https://github.com/alebov/AD-lab/blob/main/Vagrantfile) 
- [metasploitable3](https://github.com/rapid7/metasploitable3/blob/master/Vagrantfile) 

## /bin/bash

- `bash -p` 启用特权模式
	直接执行 `/bin/bash` 时，`bash` 会自动丢弃特权。但如果传递 `-p` 参数，可以维持权限。

	处于此模式时，shell 不读取 $ENV 和 $BASH_ENV 文件，环境中的 shell 函数不会被继承，且若环境中存在，SHELLOPTS、BASHOPTS、CDPATH 和 GLOBIGNORE 这些变量会被忽略。若 shell 启动时其有效用户 ID（或组 ID）与真实用户 ID（或组 ID）不相等，且未提供 -p 选项，则会采取上述措施并将有效用户 ID 重设为真实用户 ID。若启动时提供了 -p 选项，则不会重设有效用户 ID。关闭此选项会把有效用户 ID 和组 ID 设置为真实的用户 ID 和组 ID。


## 程序调试

### 跟踪系统调用

#### strace

<https://linux.die.net/man/1/strace>

```sh
strace [ -dDffhiqrtttTvVxx ] [ -acolumn ] [ -eexpr ] ... [ -ofile ] [ -ppid ] ... [ -sstrsize ] [ -uusername ] [ -Evar=val ] ... [ -Evar ] ... [ command [ arg ... ] ]

strace -c [ -D ] [ -eexpr ] ... [ -Ooverhead ] [ -Ssortby ] [ command [ arg ... ] ]
```

运行指定的命令直到它退出。它会拦截并记录进程调用的**系统调用**以及进程接收到的信号。每个系统调用的名称、参数和返回值会打印到标准错误或通过 `-o` 选项指定的文件中。

#### ltrace

```sh
ltrace [-CdfhiLrStttV] [-a column] [-e expr] [-l filename] [-n nr] [-o filename] [-p pid] ... [-s strsize] [-u username] [-X extern] [-x extern] ... [--align=column] [--debug] [--demangle] [--help] [--indent=nr] [--library=filename] [--output=filename] [--version] [command [arg ...]]
```
运行指定的命令直到退出。它会拦截并记录执行过程中调用的**动态库调用**以及接收到的信号。它还可以拦截并打印程序执行的系统调用。

### 编译

#### as

- `-a[cdghlmns]`
	以多种方式开启调试列表功能（信息泄露）
	- `as -a -o foo.o /flag`

汇编字段：
- `.incbin "path"`：把某个文件的原始字节直接塞进当前 section（不会当成汇编解析）
- `.include "path"`：按文本包含进来，会继续按汇编语法解析（容易报错/泄露）

```
.section .rodata
    .incbin "/flag"
    .byte 0
```
- 切到 `.rodata` 只读数据段，读取文件为字节并在末尾添加 `\00` 后使用 `strings` 提取字符串

#### gcc

```sh
gcc -o prog code.
```

预处理（对 .c），调用 `as` 汇编，再调用 `ld` 链接。
`-o <输出文件>`，紧跟在 `-o` 后面的就是目标文件名。
其他不以 `-` 开头的参数就是输入/源文件。

若汇编代码中存在 `_start` 入口，使用 `gcc -o` 时默认添加的对象文件或库中也存在 `_start`，将报错 `multiple definition of '_start'`


- `-E`: `.i`（文本） 预处理
	- 展开宏（#define）
	- 处理条件编译（#if/#ifdef）
	- 处理文件包含（#include）
		- `#include "/flag"`
- `-S`: `.s` （汇编文本） 预处理 + 编译
- `-c`: `.o` （ELF 目标文件，二进制）
-  链接: 可执行文件/`.so` （ELF，二进制）
- `-nostdlib` 
	不要在链接时使用标准系统启动文件或库。传递给链接器的将是没有启动文件，只有你指定的库。
- `-static` 
	在支持动态链接的系统上，这会阻止与共享库链接。在其他系统上，此选项无效。
- `-print-file-name=include` 
	查看 `include` 路径

参数：
- `-g -O0` 调试级编译
- `-no-pie` 无地址随机
- `-fno-stack-protector`  无栈保护
- `-z execstack` 栈执行

- `-shared`：指示编译器生成共享库。
- `-fPIC`：生成位置无关代码，这是共享库的硬性要求。
- `-ldl`：链接 libdl 库，如果你的代码使用了 dlsym，则必须添加此选项。

- `-v`
	在标准错误输出中打印运行编译阶段所执行的命令。同时打印编译器驱动程序的版本号、预处理器的版本号以及编译器的版本号。
- `-###`
	与 -v 类似，但命令不会被执行，并且所有命令参数都被引号括起来。这对于 shell 脚本捕获驱动程序生成的命令行非常有用。
- `-masm=dialect`
	使用指定的风格输出汇编指令。同时影响基本 `asm` 和扩展 `asm` 所使用的风格。支持的选项（按风格顺序）为 `att` 或 `intel`。默认值为 `att`。Darwin 平台不支持 `intel`。
- `-funwind-tables`  
	与 `-fexceptions` 类似，区别在于该选项仅生成所需的静态数据，但不会以任何其他方式影响生成的代码。通常无需手动启用此选项；需要此处理机制的语言处理器会代为启用。

- `-fasynchronous-unwind-tables`  
	如果目标机支持，则以 DWARF 格式生成展开表（unwind table）。该表在每条指令边界处都是精确的，因此可用于异步事件（如调试器或垃圾回收器）的栈展开。
- `-fno-ident`  
	忽略 `#ident` 指令。

- `-fno-inline`  
	不将任何函数内联展开，但标记有 `always_inline` 属性的函数除外。这是未开启优化时的默认行为。

	可以通过为单个函数标记 `noinline` 属性来使其免于内联。

例：
- `gcc -nostdlib -static -o shellcode-elf shellcode.s `
	无链接库、静态
- `grep -R "_mm_clflush" "$(gcc -print-file-name=include)"`
	查找函数/宏对应头文件
- `gcc -masm=intel -O2 -fno-stack-protector -fno-asynchronous-unwind-tables -fno-unwind-tables -fno-pie -fno-ident -fno-inline -S -o microarch_prefetch.s microarch_prefetch.c`
	对 c 进行汇编后修改为 shellcode
	- 系统调用被设置为普通调用，需手动修改

#### make - GNU make 工具用于维护程序组

`make [ -f makefile ] [ options ] ... [ targets ] ...`

读取 Makefile 并根据其中定义的规则（rules）来执行命令

Makefile格式：
```makefile
目标(target): [依赖(prerequisites)]
[TAB]命令(recipe)
```
在 Makefile 中，通常使用换行加 Tab 键来分隔目标和命令，但通过 ; 可以在同一行内完成定义。

- `-E string, --eval string`
	在命令行中直接写入一段 Makefile 规则
	- `make --eval='x:; /bin/sh -p'`

### 调试器

#### gdb - 调试机器码进程

https://pwn.college/computing-101/debugging-refresher/

```sh
[-help] [-nx] [-q] [-batch] [-cd=dir] [-f] [-b bps] [-tty=dev] [-s symfile] [-e prog] [-se prog] [-c core] [-x cmds] [-d dir] [prog[core|procID]]
```

GDB 可以做四种主要的事情（以及其他支持这些事情的事情）来帮助你捕捉正在发生的错误：
- 启动你的程序，指定任何可能影响其行为的东西。
- 使你的程序在指定条件下停止。
- 当你的程序停止时，检查发生了什么。
- 修改你的程序，以便你可以通过纠正一个错误的效果来实验，并继续学习另一个错误。

对于 python 这样的解释型语言，gdb 调试的是解释器：
`gdb --args /usr/bin/python3 -I ./python程序`

当程序设置suid位时默认启用地址空间随机化功能。

参数：
- `-x 脚本` 从脚本处读取gdb命令，用于复杂调试
- `--args` 启动带参数的命令
- `-quiet`
	`-q`
	不要打印介绍和版权信息。这些信息在批处理模式下也被抑制。
- `--pid=进程ID`
	将GDB附加到一个已经运行的程序，该程序的进程ID为pid

**子命令**
```sh
(gdb) help stepi
```
输入子命令之后按下回车即可重复此命令，而无需重复输入。

1. `gdb 命令地址`：启动gdb来调试命令
2. `run`（`r`）：从头运行程序，到断点或结束暂停
	- `run 参数1 参数2`：向程序提供参数
- `start`：在main()函数的第一行停止执行来开始调试程序。
	- `start 参数1 参数2`：向程序提供参数
- `break *函数名`（`b`）：在函数入口设置断点
	- `break *函数名 + 50` 在函数入口的偏移量处设置断点
- `hbreak` 硬件断点，在地址固定时确保设置断点而不会出现 `break` 的未加载错误 
- `tbreak` 创建临时断点
- `watch/rwatch/awatch` 对内存的写/读/全停
- `del break 1`：删除断点1
- `catch syscall 系统调用名` 在“系统调用”发生时自动中断（设置一种特殊的断点）。
	- `catch syscall read` 每次程序执行 read 系统调用，gdb 都会停下来。
- `continue`：继续执行直至遇到断点
- `info register`或缩写`info reg`：查看所有寄存器信息
	- `info break` 查看断点信息
	- `info registers cr4` 查看控制寄存器
		- `SMEP` 内核态不能执行用户态页
		- `SMAP` 内核态默认不能随意读写用户态页
- `layout regs`: 启用 gdb 的 TUI 模式，显示所有寄存器内容及附近指令
- `print $rax`（`p`）：查看特定寄存器信息
	- `p/[x] $rsp`拥有多种格式，需查表
	- `p/a *(long *) $rsp`将寄存器rsp的值作为长指针并解引用再按地址格式打印
- `x/5i $rip` 查看寄存器rip地址处的5条汇编指令
	- `x/[x] $rip`拥有多种格式，需查表
	注，x之后即为地址，无需转换并解引用，可直接使用地址。
- `disassemble 函数名`（`disass`）：查看函数的汇编代码
- `stepi <n>` （`si <n>`）单步执行一条指令，可选`n`指令步数
- `nexti <n>` （ `ni <n>`）单步执行一条指令，但会跳过函数调用，可选`n`指令步数
- ``display/<n><u><f>`  每次程序停止时自动显示表达式的值  
	- `display/8i $rip` 会持续显示后续 8 条指令
	- `display/4gx $rsp` 会持续显示栈上前 4 个值
		- 使用负数显示之前的值
	- `display/x $rdi` 持续显示寄存器 rdi 的16进制值
	- `undisplay 1` 或 `delete display 1` 删除自动显示项目
	- `disable display 1` 与 `enable display 1` 禁用与启用显示项目
- `finish` 执行完成当前函数
- `$变量`使用变量，包括寄存器变量与保存的打印值变量
- `set $变量 = $rdi`创建并设置自定义变量
	- 也可以修改目标程序的状态。例如：
		- `set $rdi = 0` 可将 $rdi 清零
		- `set *((uint64_t *) $rsp) = 0x1234` 可将栈顶第一个值设为 0x1234  
		- `set *((uint16_t *) 0x31337000) = 0x1337` 可将地址 0x31337000 处的 2 字节设为 0x1337
		例如：`set {uint64_t}($rbp-0x8) = 0x...` 设置金丝雀
	- `set args 参数` 设置参数
	- `set environment` 设置环境（如，库打桩）
	- `set breakpoint pending on` 全局自动设置无法解析符号的断点（断点到库的`__libc_start_main` 后取参数rdi自动进入main）
- `q`退出
- `record` 录制功能
	- `rsi` 启用录制功能后可回退（然而回退时的寄存器状态可能不准确）
	- `record stop` 停止录制
- `bt` 查看函数调用关系
- `(gdb) attach 进程PID`
	将GDB附加到一个已经运行的程序，该程序的进程ID为pid

shell
- `shell 命令`
	运行 shell 命令

fork 子进程调试：
- `set follow-fork-mode child` fork 进入子进程
- `set detach-on-fork off` 不丢掉父进程，可在必要时切回去
- 或丢失 `display` 设置内容，但实际上成功停在断点

线程：
- `thread <编号>`
	切换线程

使用参数化命令 `x/<n><u><f> <address>` 来检查内存内容。此格式中：
- `<u>` 表示显示的单位大小
- `<f>` 表示显示的格式  
- `<n>` 表示要显示的元素数量

有效的单位大小包括：`b`（1 字节）、`h`（2 字节）、`w`（4 字节）和 `g`（8 字节）。有效的格式包括：`d`（十进制）、`x`（十六进制）、`s`（字符串）和 `i`（指令）。地址可以通过寄存器名、符号名或绝对地址指定。此外，在指定地址时还可以使用数学表达式。

例，从rsp保存的地址读取十六进制的八字节整数：
`p/x *(long *) $rsp`
等效于
`x/gx $rsp`

查看符号表信息：使用 `&符号` 得到符号地址
```sh
(gdb) p &d
$1 = (<data variable, no debug info> *) 0x5f0921165140 <d>
(gdb) x/128bx &d
0x5f0921165140 <d>:     0x08    0x26    0x7b    0x68    0x6e    0x43    0x76    0x31
```

查看结构信息：
```sh
p *(struct task_struct*)$rdi
p ((struct task_struct*)$rdi)->pid
p ((struct task_struct*)$rdi)->comm
```

汇编语法查看指令，可通过命令 `set disassembly-flavor intel` 设置。

`info`命令：
- `info proc mappings` 
	查看进程内存映射
- `info threads`
	查看线程信息
- `info files`
	查看当前加载的可执行文件及调试符号
- `info frame`
	查看当前栈帧信息
- `info auxv`
	运行时的环境与能力“提示位”

**脚本**

你可以将命令写入某个文件（例如 `x.gdb`），然后使用 `-x <脚本路径>` 参数启动 gdb。该文件将在 gdb 启动后执行所有命令。

或者，你可以使用 `-ex '<命令>'` 执行单个命令，并通过多个 `-ex` 参数传递多个命令。

最后，你可以将某些命令放入 `~/.gdbinit` 中，使其在任何 gdb 会话中自动执行（建议将 `set disassembly-flavor intel` 放入该文件）。

`commands` 给“最近设置的断点”绑定一段 gdb 自动执行的脚本。
`end`结束 `commands` 脚本块
```
commands
	代码块
	continue
end
```

**.gdbinit**
```
# 设置 gef 插件
source /opt/gef/gef.py
# 使用 intel 风格语法
set disassembly-flavor intel
# pwntool 关闭地址随机后的固定起始地址，使用静态分析工具得到的地址偏移即可设置断点
set $base = 0x0000555555554000

define hookpost-start
    display/3i $rip
    display/3gx $rsp
end
```

`set pagination off` 关闭分页
`set confirm off` 关闭确认

保存输出内容到日志文件：
`set print elements 0` 关闭显示的元素数目限制
`set logging file gdb_log_output.txt` 设置日志文件
`set logging on` 日志记录开始
`set logging off` 日志记录停止
退出gdb后得到此日志文件

导出内存范围的二进制内容到文件：
`dump binary memory out.bin 起始地址 结束地址`
- 使用 `info files` 获取 `.rodata`或`.data`等字段（根据起始地址查看所属字段） 的末尾作为结束地址
- 示例：`(gdb) dump binary memory out.bin (char*)&d (char*)&d + 128` 导出符号表内容

创建gdb脚本后的使用：
- 在gdb内 `source 脚本名.gdb`，也可将此命令放入 `.gdbinit`
	- `source /opt/pt-dump.py` 导入页表功能，使用 `pt` 查看页表
- 在命令行启动gdb `gdb 文件 -x 脚本名.gdb`


为了在 .gdbinit 里自动化，一种常见做法是用 hook，在“程序已经开始运行”之后再下 display，例如：

用 `hookpost-start` 或 `hookpost-run` 在你敲 `start` / `run` 之后自动执行一些命令；
在这个 hook 里再下 `display/3i $rip`（那时寄存器已经存在了）。

使用函数：
- `p (long long) lseek64(3, 0, 0)`
	将 fd 3 的偏移设置到开头

##### gdb 插件 gef

`source /opt/gef/gef.py`

似乎无法用于堆查看，或需使用 pwndbg

- `nb 名称 断点位置`  
	命名断点
- `$_base()`  
	返回当前模块（或指定地址所属内存段）的基地址。
	- 在处理 PIE 程序时，可直接用 `p $_base() + 0x1234` 这样的方式访问绝对地址
- `got`  
	查看当前进程的 GOT 状态。该命令会列出 GOT 中的函数及其当前地址（是否已解析）。
	- 可指定函数名进行过滤，例如 `got printf`
- `tele/deref [-h] [-r REFERENCE] [-l LENGTH] [address]`  
	从起始地址递归打印内存引用信息

- `xinfo 地址`
	显示地址详细信息

- `grep 字符串`
	搜索字符串
- `ptype 符号`  查看类型
	- `ptype/ox {}` 查看结构与偏移
- `p{}`
	以自定义结构体打印数据

##### gdb 插件 pwndbg

`source /opt/pwndbg/gdbinit.py`

- `telescope [-h] [-r] [-f] [-i] [address] [count]`
	显示一个范围的内存引用，忽略空值。可快速定位可能有趣的地址，而无需手动查看所有值

##### gdb 插件 pt-dump

额外查看内核地址

- `pt -has 地址`
	查看地址信息

##### gdb 插件 libslub

查看内核对象堆的 slab 分配状态/空闲链表/对象内容

- `sbcache -n kmalloc-cg-512 --show-lockless-freelist --object-only`
	显示空闲链表

- `sbobject -n kmalloc-cg-512`
	显示对象池元数据与当前使用状态

- `sbobject -n kmalloc-cg-512 -c8 地址`
	显示对象所处 slab 状态

- `sbobject -n kmalloc-cg-512 -c8 地址 -x`
	显示对象数据

## 文件

### proc - 进程与内核模块

- 进程 `/proc/<pid>/...`
	- `ls -l /proc/<pid>/fd` 打开的 fd 的链接
		- 若进程拥有 /proc 的访问权限，则可使用其他进程已存在的 fd
	- `ls -l /proc/<pid>/cwd` 当前工作目录
	- `cat /proc/<pid>/status` 状态
- 系统 `/proc/...`
	- `cat /proc/cpuinfo` CPU
	- `cat /proc/kallsyms` 内核函数地址
	- `cat /proc/version` 系统版本
	- `cat /proc/cmdline` 内核启动参数

### dev - 设备

- `/dev/tty` 读写数据到终端
- `/dev/kvm` KVM 使用处理器扩展（HVM）进行虚拟化，cpu 虚拟化加速技术

## 系统管理

### setarch 在新程序环境中更改报告的架构和/或设置个性标志

```sh
setarch [arch] [options] [program [argument...]]
arch [options] [program [argument...]]
```

参数：
- `-R, --addr-no-randomize`  
	禁用虚拟地址空间的随机化。启用 ADDR_NO_RANDOMIZE。

例如：
- `setarch x86_64 -R 文件路径`

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

### 时间日期


## 待归档

### xargs - 从标准输入构建和执行命令行

`xargs` 从标准输入读取条目，条目以空格（可用双引号、单引号或反斜杠进行保护）或换行符分隔，然后执行命令（默认为 `echo`）一次或多次，并将初始参数后跟从标准输入读取的条目作为参数传递。标准输入中的空行将被忽略。

## 参考

### 文档

https://www.gnu.org/software/bash/manual/

https://bash.cyberciti.biz/guide/Main_Page

[Linux Shell 中 I/O 重定向](https://web.archive.org/web/20220629044814/http://bencane.com:80/2012/04/16/unix-shell-the-art-of-io-redirection/)