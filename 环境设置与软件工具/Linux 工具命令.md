
## 使用帮助 & 环境基础

### 帮助系统

#### man

man 是系统的手册分页程序。

手册页操作：
您可以使用方向键（以及 PgUp/PgDn 键）滚动手册页，并使用 `/` 进行搜索。
搜索后，可按 `n` 键跳至下一个结果，按 `N` 键跳至上一个结果。
除了 `/`，您还可以使用 `?` 进行反向搜索！

参数：
- `-k, --apropos [关键词]`  
	大约等同于 apropos。搜索关键词对应的手册概述并显示所有匹配结果。

#### --help

#### info

### 环境与 shell

#### env

```sh
env [选项]... [-] [NAME=VALUE]... [命令 [参数]...]
```
在环境中将每个 NAME 设置为 VALUE，并运行 COMMAND。
单独使用等同于 `-i`。
通过运行不带任何选项或参数（即输入数据）的 env 命令，可以看到当前用户的所有当前环境变量及其值，包括 PATH 变量中的所有目录

参数：
- `-i, --ignore-environment`  
	以空环境开始

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

#### Shell 启动文件

##### .bashrc

当你的 shell 启动时，它会在你的主目录中寻找 `.bashrc` 文件并将其作为*启动脚本*执行。

你可以通过设置环境变量、调整 shell 配置等方式，自定义 `/home/hacker/.bashrc` 以添加实用功能。

恶意软件常以 `.bashrc` 等启动脚本为目标，以实现持久化驻留！

设置变量，变量作用范围仅限当前bash及其子进程：
```sh
#!/bin/bash

cp /challenge/server myrun
if [ -n "$BashrcExist" ]; then
    return
fi

/challenge/server
export BashrcExist=1
```

设置标记文件，仅在非持久目录下作用于所有bash：
```sh
FLAG_FILE="/tmp/server_started"

cp /challenge/server myrun
if [ ! -f "$FLAG_FILE" ]; then
    /challenge/server
    touch "$FLAG_FILE"
fi
```

按完整命令行路径匹配，作用于所有bash：
```sh
#!/bin/bash

ProgramPath="/challenge/server"

cp $ProgramPath myrun
if ! pgrep -f "$ProgramPath" >/dev/null 2>&1; then 
    $ProgramPath
fi
```

若为 .c 源码文件则复制，若为二进制文件则使用base64编码，否则为python文件复制
```sh
#!/bin/bash

ProgramPath="/challenge/cimg"

if [ -f "${ProgramPath}.c" ]; then
    cp "${ProgramPath}.c" myrun
elif file $ProgramPath | grep -q 'ELF'; then
        base64 $ProgramPath > ~/myrun
else
        cp $ProgramPath myrun
fi
```

获取二进制文件路径，对其使用base64编码后保存到home目录
```sh
#!/bin/bash

# 显示挑战目录内容
echo ">>>"
ls -al /challenge/
echo ">>>"
file /challenge/*
echo ">>>"

MY_COPY_DIR=~/challenge-copy/

# 清空当前复制目录并新建
rm -rf "$MY_COPY_DIR"
mkdir -p "$MY_COPY_DIR"

# 复制挑战目录内容到复制目录
cp -r /challenge/* "$MY_COPY_DIR"

# 获取二进制文件路径与名称
BIN_FILE_PATH=$(file /challenge/* \
    | grep ELF \
    | sed 's/: \{1,\}.*$//')
BIN_FILE_NAME=$(echo $BIN_FILE_PATH | sed 's/\/.*\///')

# 对二进制文件进行base64编码后重命名
base64 "$BIN_FILE_PATH" > "$MY_COPY_DIR$BIN_FILE_NAME.base64"
```

##### .bash_profile

.bash_profile 是每个用户主目录中的一个隐藏文件，用于定义该用户特定的环境变量和启动程序。

##### `#!`

```bash
#!/bin/bash

echo "Hello Hackers!"
```

程序有多种类型，但如果程序文件以字符`#!`开头（通常称为"[Shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))"），Linux会将文件视为*解释型程序*，并将该行剩余内容视为*解释器*的路径。然后，内核会调用该解释器，并将程序文件的路径作为其唯一参数。

请注意，Shebang行必须位于文件的*第一行*——其前面不能有空行或空格！

常见Shebang：
- `#!/bin/bash` 用于bash脚本
- `#!/usr/bin/python3` 用于Python脚本
- `#!/bin/sh` 用于POSIX shell脚本——这是`bash`的一个功能较少但更兼容非Linux系统的原始前身！

### 库

#### getent - 从名称服务切换库获取条目

`getent database [key ...]`

- `getent group sudo`
	查询指定组的信息 
	`grep '^sudo:' /etc/group`

## 文件系统 & 路径

### 浏览 & 基础操作

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

#### cd （内建）

#### pwd （内建）

#### namei

``` namei [options] pathname...```

递归列出目录中文件信息

#### file - 确定文件类型

`file [-bchikLNnprsvz0] [--apple] [--mime-encoding] [--mime-type] [-e testname] [-F separator] [-f namefile] [-m magicfiles] file ...`

`file` 会尝试对每个参数进行分类。测试分为三组，按以下顺序执行：文件系统测试、魔数测试和语言测试。第一个成功的测试会导致文件类型被打印出来。

#### basename 从文件名中剥离目录和后缀

打印移除任何前导目录组件的 NAME。如果指定，也移除尾随的 SUFFIX。

#### du - 估计文件空间使用情况

递归地总结每个文件（目录）的磁盘使用情况。

#### dmesg - 打印或控制内核环形缓冲区

`dmesg [-c] [-r] [-n level] [-s bufsize]`

dmesg 用于检查或控制内核环形缓冲区。


虽然现代 dmesg 版本通常移除了 `-F` 或 `-f`（从文件读取）选项，但在一些非常古老的系统或题目中，如果 dmesg 支持读取任意文件，可以直接用它来读取文件内容

### 逆向工程/二进制

#### checksec

查看安全属性
- PIE：是否位置无关。No PIE ⇒ 代码段地址固定，ROP gadget 地址稳定。
- Canary：是否有栈金丝雀。无 canary ⇒ 覆盖返回地址更直接。
- NX / Stack Executable：能否在栈上执行 shellcode。
- RELRO：Full RELRO 会让 GOT 改写更难，但不影响 ret2plt/ret2csu 调用函数。
- IBT/SHSTK（CET）：可能影响某些间接跳转/返回，但你仍然可以尝试以“调用现有函数”为主的 ROP。

#### readelf 

readelf 显示一个或多个 ELF 格式目标文件的信息。选项控制要显示的特定信息。

- `-a`  
	`--all`  
	等同于指定 --file-header、--program-headers、--sections、--symbols、--relocs、--dynamic、--notes 和 --version-info。

- `-l`
	查看头部表

- `-S`  
	`--sections`   
	`--section-headers`  
	显示文件节标题中包含的信息（如果有的话）。
	- `readelf -S /challenge/server | egrep '\.bss|\.data'`

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

#### strip - 从对象文件中丢弃符号

strip 从对象文件 objfile 中丢弃所有符号。对象文件列表可以包含归档文件。至少必须给出一个对象文件。
strip 修改其参数中指定的文件，而不是以不同的名称写入修改后的副本。

#### strings - 打印文件中可打印字符的字符串。

strings 主要用于确定非文本文件的内容。

参数：
- `-t radix`
 `--radix=radix`
	在文件中每个字符串之前打印其偏移量。单个字符参数指定偏移量的基数:   
	o 表示八进制，x 表示十六进制，或 d 表示十进制。

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

默认只枚举以 ret/jmp/call 等“gadget 终结指令”收尾的短序列

- `--binary`：指定 ELF 文件
	`ROPgadget --binary /challenge/server | grep -n "leave ; ret"`

### 文件/目录管理

#### touch

`touch [OPTION]... FILE...`

更新每个文件的访问和修改时间为当前时间。
如果不存在，一个不存在的文件参数会被创建为空文件，除非提供 -c 或 -h 选项。

#### mkdir

```sh
mkdir [OPTION]... DIRECTORY...
```

创建目录（如果它们尚不存在）。

参数：
- `-p, --parents`  
	如果已存在，则不报错，按需创建父目录

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

参数：
- `-R, -r, --recursive`   
	递归复制目录内容
- ` --remove-destination`
	强制替换，先删除已存在的目标文件，然后创建一个全新的文件。
- ` -f 或 --force`
	强制覆盖，如果目标文件存在且无法被打开（例如权限不足），尝试删除它后再复制。
	如果目标文件可以被打开，尝试直接覆盖其内容。
- `--no-preserve=ATTR`
	丢弃属性，在复制时不保留指定的源文件属性。
	常用的属性包括 mode（权限）、ownership（所有者）、timestamps（时间戳）和 all（所有）。
- `-a, --archive`
	完全保留，保留源文件的所有属性，包括所有者、组、权限、时间戳和链接。
	
#### rm

```sh
rm [OPTION]... FILE...
```

rm 删除每个指定的文件。默认情况下，它不会删除目录。

选项：
- `-f, --force`
	忽略不存在的文件，从不提示
- `-r, -R, --recursive`  
	递归删除目录及其内容
- `--no-preserve-root`
	无`\`根目录保护

#### ln （硬链接/软链接）

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

### 查找

#### find - 在目录层次结构中搜索文件

`find [path...] [expression]`

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
- `-name pattern`  
	基础文件名匹配 pattern
- `-type [类型]`  
	d 目录  
	f 普通文件  
	l 符号链接  
	p 命名管道  
	s 套接字  
- `-maxdepth levels`
	最多向下遍历命令行参数指定的目录层数（一个非负整数）。-maxdepth 0 表示仅对命令行参数应用测试和操作。
- `-quit`
	立即退出。

操作：
- `-exec command`
	执行 command；如果返回 0 状态则返回 true。
	find 的所有后续参数被视为 command 的参数，直到遇到一个由 ';' 组成的参数为止。（在shell中需对分号进行转义或引号包裹为字面量）
	在 command 的参数中，字符串 '{}' 将被当前正在处理的文件名替换，而不仅仅是在单独的参数中
	- `find / -maxdepth 1 -name flag -exec cat {} \; -quit`
		在根目录的第一层（本层）寻找名称为flag的文件，并将其作为参数传递到执行的cat命令
	- `find / -exec /bin/sh -p \; -quit`
		随意找到任何文件后执行以权限传递模式 -p 运行的 sh
	
	
#### 文件名通配符

- `*` 多字符通配符，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `?` 单字符通配符，，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `[]` 单字符限定匹配，匹配括号内指定的可能字符子集的通配符。
- `[!]`、`[^]` 排除符，如果方括号内的第一个字符是 `!` 或（在较新版本的 bash 中）`^`，该通配符模式将进行反向匹配，即该方括号实例会匹配*不*在所列出的字符范围内的字符。  
	当 `!` 字符不是 `[]` 通配符的首字符时，它在 bash 中具有不同的特殊含义！`^` 没有这个问题，但在较旧的 shell 中可能不兼容。

### 归档

#### gzip, gunzip, zcat - 压缩或扩展文件

```
gzip [ -acdfhlLnNrtvV19 ] [-S suffix] [ name ... ]
gunzip [ -acfhlLnNrtvV ] [-S suffix] [ name ... ]
zcat [ -fhLV ] [ name ... ]
```

zcat 与 gunzip -c 完全相同。（在某些系统上，zcat 可能被安装为 gzcat 以保留对 compress 的原始链接。）zcat 会解压缩命令行上的文件列表或其标准输入，并将未压缩的数据写入标准输出。zcat 会解压缩具有正确魔数标记的文件，无论它们是否有 .gz 后缀。

- `-d --decompress --uncompress`
	解压缩
- `-c --stdout --to-stdout`
	将输出写入标准输出；保留原始文件不变

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

#### tar

`tar [OPTION...] [FILE]...`

通常均需使用 `-f` 指定文件名

- `-c, --create`
	创建一个新的归档文件
- `-f, --file=ARCHIVE`
	使用归档文件或设备 ARCHIVE
- `-x, --extract, --get`
	从存档中提取文件
- `-O, --to-stdout`
	将文件提取到标准输出

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

## 文本 / 文件内容处理

### 文本编辑器

#### vim - Vi 增强版，程序员文本编辑器

```
vim [options] [file ..]
vim [options] -
vim [options] -t tag
vim [options] -q [errorfile]
```

vim 是一个向上兼容 Vi 的文本编辑器。它可以用来编辑各种纯文本文件。它特别适用于编辑程序。

#### emacs

开源文本编辑器

核心在于内置的 Emacs Lisp (Elisp) 编程语言。用户可以通过编写 Elisp 脚本或安装插件，实现几乎任何功能，包括编程、编译、调试、邮件收发、新闻阅读、文件管理、版本控制甚至浏览网页

#### nano - Nano 的另一个编辑器，一个增强版的免费 Pico 克隆版

`nano [OPTIONS] [[+LINE,COLUMN] FILE]...`

小巧的编辑器

### 编码/格式转换

#### od - 以八进制和其他格式转储文件

```
od [OPTION]... [FILE]...
od [-abcdfilosx]... [FILE] [[+]OFFSET[.][b]]
od --traditional [OPTION]... [FILE] [[+]OFFSET[.][b] [+][LABEL][.][b]]
```

将 FILE 的不明确表示形式（默认为八进制字节）写入标准输出。如果提供多个 FILE 参数，则按列出的顺序将它们连接起来形成输入。如果没有 FILE，或 FILE 为-，则读取标准输入。

- `-t, --format=TYPE`
	选择输出格式或格式

传统规范格式：
- `-c`
	与 `-t c` 相同，选择 ASCII 字符或反斜杠转义

#### hd/hexdump  

`hexdump [-bcCdovx] [-e format_string] [-f format_file] [-n length] [-s skip]`

- `-f format_file`
	指定包含一个或多个由换行符分隔的格式字符串的文件。空行和以井号(#)作为第一个非空白字符的行将被忽略。

#### xxd - 制作十六进制转储或执行反向操作

```
xxd -h[elp]
xxd [options] [infile [outfile]]
xxd -r[evert] [options] [infile [outfile]]
```

#### base32

`base32 filename`：对文件内容进行 base32 编码。
`base32 -d filename`：对 base32 编码的文件进行解码。

#### base64 - base64 编码/解码数据并打印到标准输出

`base64 [OPTION]... [FILE]`

- `-d, --decode`
	解码数据。

### 查看 & 选择

#### head

```head [参数] [文件]```

默认查看文件前十行

参数
- ```n行数``` 或 ```n 行数```  
	显示设置的行数

#### tail - 输出文件的最后一部分

`tail [OPTION]... [FILE]...`

将每个文件的最后 10 行打印到标准输出。如果有多个文件，每个文件前会加上一个标题，显示文件名。如果没有文件，或者文件是-，则读取标准输入。

参数
- `-n, --lines=K`
	输出最后 K 行，而不是最后 10 行；或使用-n +K 输出从第 K 行开始的行

#### cat 

#### tac

#### cut

```sh
cut OPTION... [FILE]...
```

从每个 FILE 中打印选定行的一部分到标准输出。

参数：
- `-d, --delimiter=分隔符`
	指定分隔符代替 TAB 作为字段分隔符
- `-f, --fields=LIST`
	指定*字段*编号；如果未指定-s 选项，也会打印包含无分隔符字符的任何行

#### more - 文件浏览过滤器，用于 CRT 查看

`more [-dlfpcsu] [-num] [+/pattern] [+linenum] [file ...]`

逐屏分页浏览文本的过滤器。这个版本特别原始。

#### less

```
less [-[+]aBcCdeEfFgGiIJKLmMnNqQrRsSuUVwWX~]
[-b space] [-h lines] [-j line] [-k keyfile]
[-{oO} logfile] [-p pattern] [-P prompt] [-t tag]
[-T tagsfile] [-x tab,...] [-y lines] [-[z] lines]
[-# shift] [+[+]cmd] [--] [filename]...
```

逐屏分页浏览文本的过滤器，但允许在文件中向前和向后移动。
此外，不需要在开始前读取整个输入文件，因此对于大型输入文件，它比文本编辑器（如）启动更快。

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

#### wc - 打印每个文件的行数、单词数和字节数

```
wc [OPTION]... [FILE]...
wc [OPTION]... --files0-from=F
```

为每个 FILE 打印换行符、单词和字节数，如果指定了多个 FILE，则还会打印总计行。如果没有 FILE，或者 FILE 是-，则读取标准输入。

- `--files0-from=F`
	从文件 F 中读取由 NUL 终止的名称指定的输入文件；如果 F 是 -，则从标准输入读取名称。（信息泄露）
	- `wc --files0-from=/flag`

### 过滤 & 匹配

#### grep

[手册](https://www.man7.org/linux/man-pages/man1/grep.1.html)

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
- `-E, --extended-regexp` 
	将模式解释为扩展正则表达式。
- `-P, --perl-regexp`
	将模式解释为 perl 正则表达式。
	- `(?<=foo)`
		匹配 foo 但不包含在结果中
- `-o, --only-matching`
	仅打印匹配（非空）的行部分，每个这样的部分单独输出在一行上。

匹配控制：
- `-v, --invert-match`  
	反转匹配的意义，选择不匹配的行。(-v 由 POSIX 指定。)

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

#### sed

```sh
sed [OPTION]... {script-only-if-no-other-script} [input-file]...
```
Sed 是一个流编辑器。流编辑器用于对输入流（文件或来自管道的输入）执行基本的文本转换。

选项：
- `-n, --quiet, --silent`
	抑制自动打印模式空间
- `'s/regexp/replacement/g'`  
	尝试将 regexp 的匹配项替换为 replacement。  
	`g` 表示“全局”替换（所有出现的都删掉）
- `-e script, --expression=script`
	将脚本添加到要执行的命令中  
	即，添加多个处理

命令：
- `p` 将当前模式空间中的内容立即打印出来

示例：
- `sed '' /flag`
- `sed -n 'p' /flag`

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

#### tr

```sh
tr [选项]... 集合 1 [集合 2]
```

从标准输入修改字符，并写入标准输出。

选项：
- `-d, --delete`
	删除 SET1 中的字符，不进行翻译

SETs 是用字符字符串指定的。大多数字符表示它们自己。解释序列有：
- `CHAR1-CHAR2`
	从 CHAR1 到 CHAR2 的所有字符按升序排列

- `[:lower:]`
    all lower case letters

- `[:upper:]`
   all upper case letters

例：
- 字符串大写转小写
	`tr [:upper:] [:lower:]`


### 比较 & 排序

#### diff

```sh
diff [OPTION]... FILES
```

逐行比较文件。

输出示例：
- `2a3` 在第一个文件的第2行后追加第二个文件的第3行
- `5c5` 第一个文件的第5行被替换为第二个文件的第5行

#### sort - 排序文本文件的行

```sh
sort [OPTION]... [FILE]...
sort [OPTION]... --files0-from=F
```

将所有 FILE(s) 的排序后连接结果写入标准输出。

参数：
- `-r`：反向排序（从Z到A）  
- `-n`：数值排序（针对数字）  
- `-u`：仅保留唯一行（*删除重复项*）  
- `-R`：随机顺序！

#### uniq

#### rev - 反转文件或多个文件的行

`rev [file ...]`

指定的文件复制到标准输出，反转每行中的字符顺序。如果没有指定文件，则读取标准输入。

### 生成 & 组合

#### echo

参数
- `-n` 不输出尾随的换行符
- `-e` 启用反斜杠转义的解释

#### yes

```sh
yes [STRING]...
yes OPTION
```

反复输出所有指定的 STRING(s)或'y'。

#### seq

```sh
seq [OPTION]... LAST
seq [OPTION]... FIRST LAST
seq [OPTION]... FIRST INCREMENT LAST
```

从 FIRST 到 LAST 按 INCREMENT 的步长打印数字。
可搭配循环使用。

#### tee

`tee [选项]... [文件列表]...`

把标准输入的数据复制到文件列表中的每一个文件，同时送往标准输出。

参数：
- `-a, --append`  
	追加到给出的文件，而不是覆盖

#### mkfifo （命名管道）

```bash
mkfifo [选项]... 名称...
```

使用指定的名称创建持久化命名管道（FIFO）。  
阻塞，读取前需写入，并且写入后阻塞到被读取为止。  
想象容量为1的栈，入栈后需出栈。

## 进程 & 终端控制

### 进程

#### ps

```sh
ps [选项]
```

`ps` 显示关于部分活动进程的信息

- `-o` 选项启用自定义 `stat` 列
	- `T`  表示进程因 `Ctrl-Z` 操作而被挂起
	- `S` 表示其正在等待输入时处于睡眠状态
	- `R` 表示该进程正在活跃运行
	- `+` 号代表其处于前台

**“标准”语法：**  
此语法中，`-e` 用于列出“所有”进程，`-f` 用于显示“完整格式”输出（包括参数）。二者可合并为单一参数 `-ef`。


**“BSD”语法：**  
此语法中，`a` 用于列出所有用户的进程，`x` 用于显示非终端运行的进程，`u` 用于“用户易读”格式输出。三者可合并为单一参数 `aux`。

`ps -ef` 额外输出*父进程 ID*（`ppid`），即启动该进程的父进程 pid；而 `ps aux` 则输出进程占用的系统总 CPU 和内存百分比。

`ps -ef` 和 `ps aux` 默认会根据终端宽度截断命令列表， 传递两次 `w` 参数（如 `ps -efww` 或 `ps auxww`）来禁用截断。

#### kill

```sh
kill [-s 信号|-p] [--] 进程 ID...
kill -l [信号]
```

命令 kill 向指定的进程或进程组发送指定的信号。如果没有指定信号，将发送 TERM 信号。TERM 信号会杀死那些不捕获此信号的进程。对于其他进程，可能需要使用 KILL（9）信号，因为该信号无法被捕获。

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

- `nice cat /flag`

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




### 终端快捷键 & 作业控制（概念）

#### 终端快捷键与命令

`Ctrl-C`（即按住 `Ctrl` 键的同时按下 `C`）会向正在等待终端输入的应用发送"*中断*"信号，通常这将促使应用程序正常退出。

`Ctrl-Z` 将进程*挂起*至后台。

`fg` 命令——这是一个*内置命令*，它会获取被挂起的进程，将其恢复并放回你终端的*前台*。
`bg` 命令在*后台*恢复进程。

在命令末尾追加 `&` 符号可直接启动即进入*后台*运行！

`$?` 使用特殊的 `?` 变量获取最近终止命令的退出码（注意读取值时需前缀 `$` 符号）

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

#### tmux

```sh
tmux [-28lquvV] [-c shell-command] [-f file] [-L socket-name] [-S socket-path] [command [flags]]
```

tmux 是一个终端复用器：它允许创建、访问和控制多个终端，所有这些终端都可以从单个屏幕进行管理。tmux 可以从屏幕中分离出来，在后台继续运行，稍后可以重新附加到屏幕上。

tmux 使用 `Ctrl-B` 作为其命令前缀，而不是 `Ctrl-A`。  
因此，要从 tmux 分离，您需要按下 `Ctrl-B`，然后按 `d`。

命令：
- `tmux ls` - 列出会话
- `tmux attach` 或 `tmux a` - 重新连接到会话

组合键：
- `Ctrl-B c` - 创建一个新窗口
- `Ctrl-B n` - 切换到下一个窗口
- `Ctrl-B p` - 切换到上一个窗口
- `Ctrl-B 0` 到 `Ctrl-B 9` - 跳转到窗口 0-9
- `Ctrl-B w` - 查看一个便捷的窗口选择器
- `Ctrl + D`   
	发送文件结束（EOF）信号

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

### 身份切换 & 认证

#### su

```sh
su [OPTION]... [-] [USER [ARG]...]
```

切换至目标 USER  
单独使用 `-` 表示 `-l`。
如果未给出 USER，则假设为 root。

`su` 是一个 setuid 二进制文件：

```sh
ls -l /usr/bin/su
-rwsr-xr-x 1 root root 232416 Dec 1 11:45 /usr/bin/su
```

由于设置了 SUID 位，`su` 会以 `root` 身份运行。以 `root` 身份运行时，它可以启动一个 `root` shell！当然，`su` 具有辨别能力：在允许用户将权限提升至 `root` 之前，它会验证用户是否知道 `root` 密码

#### sudo

`sudo` 默认以 `root` 身份运行命令.  
`sudo` 通过检查策略来确定用户是否被授权以 `root` 身份运行命令。这些策略在 `/etc/sudoers` 文件中定义

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

### 相关配置文件

#### /etc/passwd

Linux 系统上的完整用户列表定义在 `/etc/passwd` 文件中

```sh
root:x:0:0:root:/root:/bin/bash
hacker:x:1000:1000::/home/hacker:/bin/bash
```

每行内容按 `:` 分隔，依次包含：
1. 用户名
2. 密码*曾经*存储位置的占位符 `x`，若为空则无密码
3. 数字用户 ID，UID 为 0 的用户是超级管理员，若设置或创建 UID 为 0 的账户将得到 root 权限
4. 数字默认组 ID
5. 可选的注释或描述字段
6. 主目录，若设置或创建账户的主目录为 /root，用户登录后直接进入系统最高权限的目录。
7. 默认 shell

#### /etc/shadow

https://www.cyberciti.biz/faq/understanding-etcshadow-file/

由于 `/etc/passwd` 是全局可读文件，不利于密码安全，因此密码数据被移至 `/etc/shadow`。
shadow 存储了 Linux 用户账户的哈希密码（或“哈希”）格式，以及与用户密码相关的其他属性。
只能被 root 用户直接访问

```sh
root:$6$s74oZg/4.RnUvwo2$hRmCHZ9rxX56BbjnXcxa0MdOsW2moiW8qcAl/Aoc7NEuXl2DmJXPi3gLp7hmyloQvRhjXJ.wjqJ7PprVKLDtg/:19921:0:99999:7:::
hacker::19916:0:99999:7:::
zardus:$6$bEFkpM0w/6J0n979$47ksu/JE5QK6hSeB7mmuvJyY05wVypMhMMnEPTIddNUb5R9KXgNTYRTm75VOu1oRLGLbAql3ylkVa5ExuPov1.:19921:0:99999:7:::
```

每行内容按 `:` 分隔：
1. 用户名
2. 密码，通常密码格式设置为 `$id$salt$hashed`。  
	`$id` 是 GNU/Linux 上使用的算法前缀。  
	字段值为 `*` 或 `!` 实际表示该账户的密码登录功能已被禁用；空白字段表示未设置密码（某些配置下可能允许无密码 `su`，这是较常见的错误配置）；而长字符串是密码经过单向加密（哈希）后的结果。
- 其余字段为密码修改日期与状态

#### /etc/sudoers

https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file

`visudo [-chqsV] [-f sudoers]`

visudo 以安全的方式编辑 sudoers 文件，类似于 vipw(8)。visudo 锁定 sudoers 文件以防止多个同时编辑，提供基本的合理性检查，并检查解析错误。如果 sudoers 文件当前正在被编辑，你会收到一条消息提示稍后再试。

## Shell 编程 & 命令组合

### 命令链 & 控制

- `;`  
	命令链式组合的最简单方式是使用 `;`。在大多数上下文中，`;` 分隔命令的方式类似于用 Enter 键分隔行。

- `&&`  
	`&&` 运算符允许您仅在第一个命令成功时（遵循Linux惯例，即退出码为0）才运行第二个命令。这被称为"AND"运算符，因为需要同时满足两个条件：第一个命令必须成功*且*第二个命令才会运行。这对于需要特定操作依赖于其他操作成功执行的复杂命令行工作流非常有用。

- `||`  
	`||`运算符允许您在第一个命令失败（以非零代码退出）时才运行第二个命令。这被称为*OR*运算符，因为要么第一个命令成功*要么*第二个命令将运行。`||`运算符对于提供回退命令或错误处理非常有用！

- `bash [options] [file]`  
	Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。

### 重定向 & 管道（操作符）

重定向到文件：
`命令 > 文件`
- `>`将重定向的数据覆盖写入文件。如果指定的文件不存在，则创建。  
	权限为 `rw-rw-rw-` (`0666`)

	`>` 默认会重定向标准输出，但你可以通过在重定向符号前放置适当的标准文件描述符来指定是重定向标准输出还是标准错误：
	- `1>` stdout（默认）
	- `2>` stderr

重定向到文件并追加数据:
`命令 >> 文件`
- `>>` 被重定向的输出追加到文件中。同样，可以使用文件描述符来指定是将标准输出还是标准错误写入指定的文件。

从文件重定向输入：
`命令 < 文件` 或 `< 文件 命令`
- `<`也可以用来将文件重定向到程序的标准输入。

将一个程序的输出管道传输到另一个程序:
`命令 | 命令`
- `|` （管道符）用于将一个命令的标准输出重定向到另一个命令的标准输入。管道符`|`不被视为重定向操作符，而是一个控制操作符。


将标准错误重定向到标准输出:
- `2>&1` 在使用重定向时，你可以使用`&N`（其中 N=文件描述符）将两种输出方式重定向到同一个路径。这也可以与`|`控制运算符一起使用。

### 模式与技巧

- `2>/dev/null`  
	丢弃错误信息
- `if ! 命令 >/dev/null 2>&1; then`  
	将命令的标准输出重定向到黑洞丢弃，将标准错误重定向到标准输出（当前为黑洞丢弃）。
	使用命令的返回状态码进行判断

#### 交互性 / 易用性功能（Shell 前端行为）

##### tab 键补全

如果你在 shell 中按 tab 键，它会尝试推断你将要输入的内容并自动补全。  
默认情况下，`bash` 会在出现多个匹配选项时自动扩展到第一个分歧点（在此例中为 `fl`）。  
当你*第二次*按下 tab 键时，它会列出这些匹配选项。  

补全选项根据位置，即上下文不同，对应不同文件:
- 命令位置：补的是“可执行命令”（过滤掉普通文件）。
- 参数位置：补的是“文件名/路径”（不过滤普通文件）。

#### Shell 语法与展开机制（Shell 解析阶段）

当 shell 遇到空格时，它会结束变量赋值

默认情况下，在 Shell 会话中设置的变量仅在该 Shell 进程内局部有效。  
使用`export VAR`导出到子进程的环境变量后可被使用。

`env` 命令打印出 Shell 中设置的每一个*导出的*变量


##### 内置命令

- `read` 从标准输入*读取*到变量中  `read 变量`  
	注，仅读一行。
	- `-p` 参数的示例，该参数允许您指定提示信息  
		`read -p "输入提示" 变量`  

- `echo` 打印到标准输出  
	- `echo $VAR` 做单词分割：把换行当空格处理
	- `echo "$VAR"` 使用双引号展开变量到一个字符串中

##### 展开

- 参数展开  
	`$var` 和 `${var}`   
	变量名前加 `$` 符号，触发变量展开来引用变量。  
	用变量的值替换变量名，后面紧跟其他字符时，使用 `${}` 才能区分变量名边界。

- 命令替换  
	`$(command)` 或（已弃用）  `command`.  
	命令替换允许命令的输出替换命令本身，同时删除任何尾随的换行符。  
	命令替换 `$(cat file)` 可以被替换为等效但更快的 `$(< file)`  

- 算术展开  
	`$(( expression ))`   
	在 shell 中做整数运算。

- 花括号展开  
	`{a,b,c}`，`{1..5}` 等  
	生成一组字符串，例如：

	```sh
	echo {1..3}
	1 2 3
	```

- 路径名展开 / 通配符  
	`*`、`?`、`[abc]`、`[a-z]` 等  
	把模式匹配到的文件名列出来。

- 波浪线展开  
	`~`  
	展开为用户的 home 目录。

- 历史展开  
	`!`   
	用历史命令或历史参数替换。

-  进程替换  
	`<(command)`、`>(command)`
	连接到一个命令输出创建的临时文件

- 单双引号  
	在 Shell 中，所有引号都必须*成对匹配*，否则命令无效。
	- 单引号 `'...'` 几乎禁止一切展开
	- 双引号 `"..."` 保留大部分展开，但不解析为转义序列（`\n`）

- C 语言风格的转义  
	`$'...'`  
	得到真实字节，潜在用法：`VAL=$''`得到转义序列后使用 `echo "$VAL"`打印出回车换行

有一个特殊的 shell 变量，名为 *`PATH`*，由一系列用冒号分隔的绝对路径组成，它在纯文本文件中存储了一系列绝对目录路径，shell 会在此目录列表中搜索与命令对应的程序。   
通过向此列表添加或替换目录，您可以让这些程序支持裸命令名启动！
要永久添加用户的 PATH 变量，可以将其添加到该用户的`.bash_profile` 文件中。

#### 进程替换

- `命令B <(命令A)`  
	将命令A的输出连接到命令B的*参数*，即命令A的输出作为命令B的参数  
	当写入 `<(command)` 时，bash 将运行该命令并将其输出连接到一个它将创建的临时文件，它被称为*命名管道*
- `命令B >(命令A)`
	将命令B的输出连接到命令A的标准输入  
	当写入一个 `>(command)` 参数，bash 将运行 `command` 命令，但将其输入连接到一个临时命名管道文件。当命令B写入此文件时，数据会传送到命令A的标准输入

### whiptail - 从 shell 脚本中显示对话框

```
whiptail [ --title title ] [ --backtitle backtitle ] [ --clear ] [ --default-item string ] [ --defaultno ] [ --fb ] [ --nocancel ] [ --yes-button text ] [ --no-button text ] [ --ok-button text ] [ --cancel-button text ] [ --noitem [ ] --output-fd fd ] [ --separate-output ] [ --scrolltext ] [ --topleft ] box-options
```

whiptail 是一个程序，它允许你使用从 shell 脚本中的对话框来提出各种问题或显示消息。目前，这些类型的对话框已经实现：
是/否框、菜单框、输入框、消息框、文本框、信息框、复选框、单选框、进度条框和密码框。

- `--textbox file height width`
	文本框允许你在对话框中显示文本文件的内容，类似于一个简单的文本文件查看器。
	- `whiptail --textbox /flag 10 70`

### awk - 模式扫描和处理语言

`gawk [ POSIX or GNU style options ] -f program-file [ -- ] file ...`

`awk 'pattern { action }' input_file`
- 模式:
	可以是正则表达式（如 /error/）、条件表达式（如 $3 > 100）或特殊模式 BEGIN / END。
	- `BEGIN{ }`：在处理任何输入行之前执行一次。常用于初始化变量。
	- `END{ }`：在处理完所有输入行之后执行一次。常用于汇总输出。

示例：
- `awk '{print}' /flag`

## 网络 & 安全工具

### 状态信息 & 配置

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
	

#### nft

### 基础下载/请求

#### curl

```curl [options / URLs]```

[手册](https://curl.se/docs/manpage.html)

参数
- ```-d, --data <data>```
    以 POST 方法发送 data
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
- `-H, --header <header/@file>`  
	在发送的信息中包含的额外头部

	```sh
	curl -H "Host: your.host" https://example.com
	```
- `-v, --verbose`  
	输出详细信息

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

示例：
- `tcpdump -ni eth0 -vv 'arp or icmp or (udp and host 10.0.0.2)'`

### 网络扫描 & 连接

#### socat - 多用途中继 (SOcket CAT)

`CWsocat [options] <address> <address>`

Socat 是一个基于命令行的工具，用于建立两个双向字节流并在它们之间传输数据。由于这些流可以由多种不同类型的数据接收端和发送端（参见地址类型）构建，并且可以应用许多地址选项到这些流上，因此 socat 可以用于多种不同的目的。

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

#### nmap - 网络探索工具和安全/端口扫描器

[文档](https://nmap.org/book/man.html)

```nmap [Scan Type(s)] [Options] {target specification}```

Nmap ("网络映射器") 是一个开源的网络探索和安全审计工具。它被设计用于快速扫描大型网络，虽然它对单个主机也工作得很好。Nmap 以新颖的方式使用原始 IP 数据包来确定网络上的哪些主机可用，这些主机提供哪些服务（应用程序名称和版本），它们运行哪些操作系统（以及操作系统版本），使用哪些类型的包过滤器/防火墙，以及其他几十个特性。

参数

- ```-sS/sT/sA/sW/sM``` 分别对应TCP SYN/Connect()/ACK/Window/Maimon scans
- ```-sV``` 探测开放端口以识别服务/版本信息


主机发现:
默认情况下，Nmap 会进行主机发现，然后对每个确定在线的主机执行端口扫描。
- `-sn` 
	不进行端口扫描
- `-Pn` 
	将所有主机视为在线，跳过主机发现
- `-n` 
	不进行 DNS 解析

Port Specification And Scan Order
端口规范和扫描顺序：
- `-p port ranges`  
	仅扫描指定端口。可以单独指定端口编号，也可以使用连字符分隔的范围（例如 1-1023）


Timing And Performance
时间和性能：
- `--min-rate number; --max-rate number`  
	直接控制扫描速率。
	参数是一个表示每秒数据包数的正实数。例如，指定--min-rate 300 意味着 Nmap 会尝试将发送速率保持在 300 包/秒或更高。

- `--min-parallelism numprobes; --max-parallelism numprobes`   
	调整探测并行化，控制针对一个主机组可能同时发出的探测总数。它们用于端口扫描和主机发现。  
	最常见的用法是将--min-parallelism 设置为大于 1 的数值，以加快性能较差的主机或网络的扫描速度。这是一个有风险的选择，因为设置过高可能会影响准确性。设置此选项也会降低 Nmap 根据网络条件动态控制并行度的能力。10 可能是一个合理的值，但我仅会在万不得已时调整此值。

- `-T paranoid|sneaky|polite|normal|aggressive|insane`  
	六种时间模板允许用户指定他们希望采取的攻击强度: 偏执狂（0）、鬼祟（1）、礼貌（2）、正常（3）、侵略（4）和疯狂（5）。
	前两种用于入侵检测系统（IDS）规避。
	礼貌模式会减慢扫描速度以减少带宽和目标机器资源的使用。
	正常模式是默认设置，所以-T3 不会产生任何效果。
	侵略模式通过假设你处于一个相当快且可靠的网络上来加速扫描。
	最后是疯狂模式，它假设你处于一个异常快的网络上，或者愿意为了速度牺牲一些准确性。

Verbosity and debugging options
详细级别和调试选项：
- `-v`
	增加详细级别

- `--open`  
	仅显示开放（或可能开放）的端口




#### Ncat

[手册](https://nmap.org/book/ncat-man.html)
参数：
- `-l, --listen`  
	绑定并监听传入连接

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

#### dig

域名信息收集器（domain information groper）

参数
- `+short` 简洁信息

#### whois

查询对象的 whois 数据库

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



#### hashcat

[文档](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat)


#### ssh - OpenSSH SSH 客户端（远程登录程序）

参数：
- `-i identity_file`  
	选择一个文件，从中读取用于 RSA 或 DSA 身份验证的身份（私钥）。
	
示例：
- `ssh -i key hacker@dojo.pwn.college`  

#### ssh-keygen - 认证密钥生成、管理和转换

[文档](https://www.ssh.com/academy/ssh/keygen)

参数：
- `-f <filename>`
	选择存储密钥的文件
- `-N "新"` 	
	为密钥提供一个新的密码短语
- `-i "输入"` 	
	访问现有密钥文件
- `-D pkcs11`
	从 PKCS#11 共享库 pkcs11 中下载其提供的公钥。与 -s 选项一起使用时，该选项表示某个 CA 的密钥位于一个 PKCS#11 令牌中。（需使用相对或绝对路径）

	- `dlopen()`加载指定共享库后会找一个固定导出符号：`C_GetFunctionList`，于是设置的共享库中应当包含此结构（导入头部或设置最小对应结构）

示例：
- `ssh-keygen -f key -N ''`	
	生成一个 以 `key` 为名称的 ssh 密钥，私钥 `key`，公钥 `key.pub`。密码为 `''`

## 容器与虚拟化

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



## /bin/bash

- `bash -p`
	直接执行 `/bin/bash` 时，`bash` 会自动丢弃特权。但如果传递 `-p` 参数，可以维持权限。

## bash 脚本

bash中无数据类型的概念、无需声明变量。

关键字**local**创建局部变量

变量名仅限字母数字下划线，于是`$VAL`将读取直到有效变量名外的字符。如：
`export PATH=$PATH:/usr/sbin`
变量在`:`符号终止，即使没有使用显式的分隔`${}`也可被shell识别。

在 Bash 里，单引号 `'` 和 双引号 `"` 的区别：

- 单引号：几乎什么都不展开，按字面原样保留。
    即，不触发 `!` 历史扩展
- 双引号：会做变量、命令替换、历史扩展等部分展开。

`bash [options] [file]`
Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。

按照惯例，Shell脚本通常以 `sh` 作为后缀命名
然后通过将其作为参数传递给新的Shell实例（`bash`）来执行！
当以这种方式调用Shell时，它不会从用户处获取命令，而是从文件中读取命令。

```sh
hacker@dojo:~$ bash pwn.sh
```

如果您的Shell脚本文件是*可执行的*（请回顾 linux-文件权限），您可以直接通过其相对路径或绝对路径调用它

```sh
echo 'hack the planet' > solve.sh && chmod u+x solve.sh
```
### 参数

```sh
hacker@dojo:~$ bash myscript.sh hello world
```

脚本可以通过特殊变量访问这些参数：
- `$1` 包含第一个参数（"hello"）
- `$2` 包含第二个参数（"world"）
- `$3` 将包含第三个参数（如果存在）
- ...以此类推

以下是一个简单示例：

```bash
hacker@dojo:~$ cat myscript.sh
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
hacker@dojo:~$ bash myscript.sh hello world
First argument: hello
Second argument: world
hacker@dojo:~$
```

### 条件

```bash
if [ "$1" == "one" ]
then
    echo "1"
elif [ "$1" == "two" ]
then
    echo "2"
else
    echo "unknown"
fi
```

语法规则较为严格，主要有以下原因：
首先，*必须*在`if`后、`[`后以及`]`前保留空格（如果您熟悉C等语言，这点有所不同）；
其次，`if`、`then`和`fi`必须位于不同行（或用分号分隔），不能将它们合并到同一语句中。
另一个特殊之处是：`if`语句的结束标记是`fi`（即*if*的倒写），而非`endif`或`end`等常见形式。


与`if`类似，*必须*在`elif`后使用`then`

`else`没有条件——它会捕获所有之前未匹配的情况。它也不需要`then`语句。最后，`fi`需放置在`else`代码块之后，表示整个复合语句的结束

`if [ 条件 ]; then` 这里的 `[` 实际上是一个命令，等价于：
`test 条件`

### 循环

```bash
# 从1开始，间隔5，直到100
for i in $(seq 1 5 100); do
    echo "select substr(datum, $i, 5) from dataset;" \
    | /challenge/sql \
    | grep "substr(datum" \
    | sed -e "s/.*, 5)': '//" -e "s/'}.*//"
    
done | tr -d '\n'
```

### 操作符

```sh
[ -n "$var" ]   # var 非空？
[ -z "$var" ]   # var 为空？（-z 是 is zero-length）
```

`-n`、`-z` 是 字符串测试 的一元（单目）操作符

判断文件是否存在:
`-e path`：存在（不管是文件还是目录）
`-f path`：存在且是普通文件
`-d path`：存在且是目录

## 程序调试

### 跟踪系统调用

#### strace 与 ltrace

<https://linux.die.net/man/1/strace>

```sh
strace [ -dDffhiqrtttTvVxx ] [ -acolumn ] [ -eexpr ] ... [ -ofile ] [ -ppid ] ... [ -sstrsize ] [ -uusername ] [ -Evar=val ] ... [ -Evar ] ... [ command [ arg ... ] ]

strace -c [ -D ] [ -eexpr ] ... [ -Ooverhead ] [ -Ssortby ] [ command [ arg ... ] ]
```

strace 运行指定的命令直到它退出。它会拦截并记录进程调用的系统调用以及进程接收到的信号。每个系统调用的名称、参数和返回值会打印到标准错误或通过 `-o` 选项指定的文件中。

### 设置环境

#### env - 在修改后的环境中运行程序

`env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]`

- `-i, --ignore-environment`
	以空环境开始
	- `env -i PATH=/usr/bin:/bin`
		在“干净环境”下，确保只从系统目录找到工具链组件

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
- `del break 1`：删除断点1
- `catch syscall 系统调用名` 在“系统调用”发生时自动中断（设置一种特殊的断点）。
	- `catch syscall read` 每次程序执行 read 系统调用，gdb 都会停下来。
- `continue`：继续执行直至遇到断点
- `info register`或缩写`info reg`：查看所有寄存器信息
	- `info break` 查看断点信息
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
	- `undisplay 1` 或 `delete display 1` 删除自动显示项目
	- `disable display 1` 与 `enable display 1` 禁用与启用显示项目
- `finish` 执行完成当前函数
- `$变量`使用变量，包括寄存器变量与保存的打印值变量
- `set $变量 = $rdi`创建并设置自定义变量
	- 也可以修改目标程序的状态。例如：
		- `set $rdi = 0` 可将 $rdi 清零
		- `set *((uint64_t *) $rsp) = 0x1234` 可将栈顶第一个值设为 0x1234  
		- `set *((uint16_t *) 0x31337000) = 0x1337` 可将地址 0x31337000 处的 2 字节设为 0x1337
	- `set args 参数` 设置参数
	- `set environment` 设置环境（如，库打桩）
- `q`退出
- `record` 录制功能
	- `rsi` 启用录制功能后可回退（然而回退时的寄存器状态可能不准确）
	- `record stop` 停止录制

使用参数化命令 `x/<n><u><f> <address>` 来检查内存内容。此格式中：
- `<u>` 表示显示的单位大小
- `<f>` 表示显示的格式  
- `<n>` 表示要显示的元素数量

有效的单位大小包括：`b`（1 字节）、`h`（2 字节）、`w`（4 字节）和 `g`（8 字节）。有效的格式包括：`d`（十进制）、`x`（十六进制）、`s`（字符串）和 `i`（指令）。地址可以通过寄存器名、符号名或绝对地址指定。此外，在指定地址时还可以使用数学表达式。

例，从rsp保存的地址读取十六进制的八字节整数：
`p/x *(long *) $rsp`
等效于
`x/gx $rsp`


汇编语法查看指令，可通过命令 `set disassembly-flavor intel` 设置。

`info`命令：
- `info proc mappings` 
	查看进程内存映射
| 命令                | 作用说明                                      |
|---------------------|-----------------------------------------------|
| info functions      | 列出所有已知函数                              |
| info functions PAT  | 列出匹配 PAT 的函数（如 `info functions win`) |
| info variables      | 列出全局/静态变量                            |
| info locals         | 查看当前栈帧里的局部变量                      |
| info args           | 查看当前函数的参数                            |
| info registers      | 查看所有寄存器值                              |
| info registers REG  | 查看指定寄存器值（如 `info registers rax`)    |
| info frame          | 查看当前栈帧信息                              |
| info stack          | 查看调用栈（等价于 `backtrace` 简版）        |
| info breakpoints    | 列出所有断点/观察点                          |
| info watchpoints    | 列出观察点                                  |
| info threads        | 列出所有线程                                  |
| info files          | 查看当前加载的可执行文件及调试符号            |
| info proc           | 查看被调试进程的信息（PID 等）                |
| info sharedlibrary  | 查看已加载的共享库                            |
| info line *ADDR     | 查看某地址对应的源码行                        |
| info symbol ADDR    | 查看某地址对应的符号名                        |
| info address NAME   | 查看某符号（如函数）所在地址                  |
| info sources        | 列出已知的源码文件                            |
| info display        | 查看自动显示表达式（`display` 设置的）        |
| info target         | 查看当前调试目标相关信息                      |
| info inferiors      | 查看被调试的进程列表                          |

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

.gdbinit
```
set disassembly-flavor intel

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

创建gdb脚本后的使用：
- 在gdb内 `source 脚本名.gdb`，也可将此命令放入 `.gdbinit`
- 在命令行启动gdb `gdb 文件 -x 脚本名.gdb`


为了在 .gdbinit 里自动化，一种常见做法是用 hook，在“程序已经开始运行”之后再下 display，例如：

用 `hookpost-start` 或 `hookpost-run` 在你敲 `start` / `run` 之后自动执行一些命令；
在这个 hook 里再下 `display/3i $rip`（那时寄存器已经存在了）。

```
set disassembly-flavor intel

define hookpost-start
    display/3i $rip
end
```

**插件**

- GEF

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


### 时间日期

#### date

- `-f` 
	读取指定文件的每一行并尝试解析为日期。（信息泄露）

## 参考

### 文档

https://www.gnu.org/software/bash/manual/

https://bash.cyberciti.biz/guide/Main_Page

### 手册

https://man.archlinux.org/

https://linux.die.net/man

### 文章

https://pwn.college/

[Linux Shell 中 I/O 重定向](https://web.archive.org/web/20220629044814/http://bencane.com:80/2012/04/16/unix-shell-the-art-of-io-redirection/)