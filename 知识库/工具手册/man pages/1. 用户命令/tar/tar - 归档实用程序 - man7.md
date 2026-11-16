https://www.man7.org/linux/man-pages/man1/tar.1.html

## 名称

`tar` - 归档实用程序

## 概要

**传统用法**

```sh
tar {A|c|d|r|t|u|x}[GnSkUWOmpsMBiajJzZhPlRvwo] [ARG...]
```

**UNIX 风格用法**

```sh
tar -A [OPTIONS] -f ARCHIVE ARCHIVE...

tar -c [-f ARCHIVE] [OPTIONS] [FILE...]

tar -d [-f ARCHIVE] [OPTIONS] [FILE...]

tar -r [-f ARCHIVE] [OPTIONS] [FILE...]

tar -t [-f ARCHIVE] [OPTIONS] [MEMBER...]

tar -u [-f ARCHIVE] [OPTIONS] [FILE...]

tar -x [-f ARCHIVE] [OPTIONS] [MEMBER...]
```

**GNU 风格用法**

```sh
tar {--catenate|--concatenate} [OPTIONS] --file ARCHIVE ARCHIVE...

tar --create [--file ARCHIVE] [OPTIONS] [FILE...]

tar {--diff|--compare} [--file ARCHIVE] [OPTIONS] [FILE...]

tar --delete [--file ARCHIVE] [OPTIONS] [MEMBER...]

tar --append [--file ARCHIVE] [OPTIONS] [FILE...]

tar --list [--file ARCHIVE] [OPTIONS] [MEMBER...]

tar --test-label [--file ARCHIVE] [OPTIONS] [LABEL...]

tar --update [--file ARCHIVE] [OPTIONS] [FILE...]

tar {--extract|--get} [--file ARCHIVE] [OPTIONS] [MEMBER...]
```

## 注意

本手册页是 GNU `tar` 的简要说明。详细讨论（包括示例和使用建议）请参阅以 texinfo 格式提供的 **GNU Tar 手册**。如果系统上正确安装了 `info` 阅读器和 tar 文档，命令

```sh
info tar
```

应能让您访问完整手册。

您也可以使用 `“emacs”(1)` 中的 info 模式查看手册，或在以下网址找到各种格式的手册：

<https://www.gnu.org/software/tar/manual>

如果本手册页与 **GNU Tar 手册**之间存在任何差异，以后者为准。

## 描述

GNU `tar` 是一个归档程序，设计用于将多个文件存储在单个文件（**归档**）中，并操作此类归档。归档可以是常规文件或设备（例如磁带驱动器，程序名称由此而来，即 **t**ape **ar**chiver 的缩写），可位于本地或远程机器上。

### 选项风格

GNU `tar` 的选项可以用三种不同风格给出。在**传统风格**中，第一个参数是一组选项字母，所有后续参数为需要参数的选项提供参数。参数按与选项字母相同的顺序读取。所有选项处理完毕后剩余的任何命令行单词被视为非选项参数：文件或归档成员名。

例如，`c` 选项要求创建归档，`v` 选项请求详细操作，`f` 选项接受一个参数来设置要操作的归档名称。以下命令以传统风格编写，指示 tar 将目录 `/etc` 中的所有文件存储到归档文件 `etc.tar` 中，并详细列出正在归档的文件：

```sh
tar cfv etc.tar /etc
```

在 **UNIX** 或**短选项风格**中，每个选项字母以单个短横线为前缀，与其他命令行实用程序一样。如果选项接受参数，参数跟在选项后面，可以作为单独的命令行单词，也可以紧跟在选项后面。但是，如果选项接受**可选**参数，参数必须紧跟在选项字母后面，中间不能有任何空白，如 `-g/tmp/snar.db`。

任意数量的不带参数的选项可以在单个短横线后聚在一起，例如 `-vkp`。接受参数（无论强制还是可选）的选项可以出现在此类聚集的末尾，例如 `-vkpf a.tar`。

上述示例命令以**短选项风格**编写可以是：

```sh
tar -cvf etc.tar /etc
```

或

```sh
tar -c -v -f etc.tar /etc
```

在 **GNU** 或**长选项风格**中，每个选项以两个短横线开头，并具有由小写字母和短横线组成的有意义名称。使用时，长选项可以缩写为其首字母，前提是不会产生歧义。长选项的参数可以作为单独的命令行单词紧跟在选项后面提供，也可以用等号与选项分隔，中间不能有空白。可选参数必须始终使用后一种方法。

以下是以此风格编写示例命令的几种方式：

```sh
tar --create --file etc.tar --verbose /etc
```

或（缩写一些选项）：

```sh
tar --cre --file=etc.tar --verb /etc
```

所有三种风格的选项可以混合使用，但不鼓励与旧选项混用。

### 操作模式

下表列出的选项告诉 GNU `tar` 要执行什么操作。必须恰好给出其中一个。非选项参数的含义取决于所请求的操作模式。

- `-A`, `--catenate`, `--concatenate`  
    将归档追加到另一个归档末尾。参数被视为要追加的归档名称。所有归档必须与它们所追加到的归档格式相同，否则生成的归档可能无法被非 GNU 实现的 `tar` 使用。另请注意，当给出多个归档时，仅在使 `-i`（`--ignore-zeros`）选项时，才能在结果归档中访问第一个归档以外的归档成员。

    压缩归档无法连接。

- `-c`, `--create`  
    创建新归档。参数提供要归档的文件名称。除非给出 `--no-recursion` 选项，否则目录会被递归归档。

- `-d`, `--diff`, `--compare`  
    查找归档与文件系统之间的差异。参数是可选的，指定要比较的归档成员。如果未给出，则假定为工作目录。

- `--delete`  
    从归档中删除。参数提供要移除的归档成员名称。必须至少给出一个参数。

    此选项不对压缩归档操作。没有等价的短选项。

- `-r`, `--append`  
    将文件追加到归档末尾。参数含义与 `-c`（`--create`）相同。

- `-t`, `--list`  
    列出归档内容。参数是可选的。给出时，它们指定要列出的成员名称。

- `--test-label`  
    测试归档卷标并退出。不带参数使用时，打印卷标（如果有）并以状态 `0` 退出。当给出一个或多个命令行参数时，`tar` 将卷标与每个参数比较。如果找到匹配则退出码为 `0`，否则为 `1`。除非与 `-v`（`--verbose`）选项一起使用，否则不显示输出。

    此选项没有等价的短选项。

- `-u`, `--update`  
    追加比归档中相应副本更新的文件。参数含义与 `-c` 和 `-r` 选项相同。注意，较新的文件不会替换其旧归档副本，而是追加到归档末尾。因此结果归档可能包含多个同名成员，对应该文件的各个版本。

- `-x`, `--extract`, `--get`  
    从归档中提取文件。参数是可选的。给出时，它们指定要提取的归档成员名称。

- `--show-defaults`  
    显示各种 `tar` 选项的内置默认值并退出。

- `-?`, `--help`  
    显示简短选项摘要并退出。

- `--usage`  
    显示可用选项列表并退出。

- `--version`  
    打印程序版本和版权信息并退出。

## 选项

### 操作修饰符

- `--check-device`  
    创建增量归档时检查设备号（默认）。

- `-g`, `--listed-incremental=FILE`  
    处理新的 GNU 格式增量备份。`FILE` 是**快照文件**的名称，`tar` 在其中存储附加信息，用于决定自上次增量转储以来哪些文件发生了更改，从而必须再次转储。如果创建归档时 `FILE` 不存在，则会创建它并将所有文件添加到结果归档（**level 0** 转储）。要创建非零级别 **N** 的增量归档，需要级别 **N-1** 创建的快照文件副本，并将其用作 `FILE`。

    列出或提取时，不会检查 `FILE` 的实际内容，仅因语法要求才需要它。因此通常使用 `/dev/null` 代替。

- `--hole-detection=METHOD`  
    使用 `METHOD` 检测稀疏文件中的空洞。此选项隐含 `--sparse`。`METHOD` 的有效值为 `seek` 和 `raw`。默认是 `seek`，不适用时回退到 `raw`。

- `-G`, `--incremental`  
    处理旧 GNU 格式增量备份。

- `--ignore-failed-read`  
    对不可读文件不以非零状态退出。

- `--level=NUMBER`  
    为创建的 listed-incremental 归档设置转储级别。目前仅 `--level=0` 有意义：它指示 `tar` 在转储前截断快照文件，从而强制执行级别 0 转储。

- `-n`, `--seek`  
    假定归档可 seek。通常 `tar` 会自动确定归档是否可 seek。此选项适用于此类识别失败的情况。仅当归档打开以供读取（例如使用 `--list` 或 `--extract` 选项）时生效。

- `--no-check-device`  
    创建增量归档时不检查设备号。

- `--no-seek`  
    假定归档不可 seek。

- `--occurrence[=N]`  
    仅处理归档中每个文件的第 `N` 次出现。此选项仅在与以下子命令之一一起使用且命令行或通过 `-T` 选项给出文件列表时有效：`--delete`、`--diff`、`--extract` 或 `--list`。默认 `N` 为 `1`。

- `--restrict`  
    禁用某些可能有害的选项。

- `--sparse-version=MAJOR[.MINOR]`  
    设置要使用的稀疏格式版本。此选项隐含 `--sparse`。有效参数值为 `0.0`、`0.1` 和 `1.0`。有关稀疏格式的详细讨论，请参阅 **GNU Tar 手册**附录 **D**“**稀疏格式**”。使用 `info` 阅读器，可以通过运行以下命令访问：`info tar 'Sparse Formats'`。

- `-S`, `--sparse`  
    高效处理稀疏文件。文件系统中的某些文件可能包含实际上从未写入的段（通常是 `DBM` 等系统创建的数据库文件）。给出此选项时，`tar` 尝试在归档前确定文件是否稀疏，如果是，则通过不转储文件的空部分来减小结果归档的大小。

### 覆盖控制

这些选项控制 `tar` 在提取文件覆盖磁盘上现有副本时的操作。

- `-k`, `--keep-old-files`  
    提取时不替换现有文件。

- `--keep-newer-files`  
    不替换比其归档副本更新的现有文件。

- `--keep-directory-symlink`  
    提取时不替换指向目录的现有符号链接。

- `--no-overwrite-dir`  
    保留现有目录的元数据。

- `--one-top-level[=DIR]`  
    将所有文件提取到 `DIR`，或者如果未使用参数，则提取到以归档基名命名的子目录（减去 `--auto-compress` 可识别的标准压缩后缀）。

- `--overwrite`  
    提取时覆盖现有文件。

- `--overwrite-dir`  
    提取时覆盖现有目录的元数据（默认）。

- `--recursive-unlink`  
    在提取目录之前递归移除该目录中的所有文件。

- `--remove-files`  
    将文件添加到归档后从磁盘移除这些文件。

- `--skip-old-files`  
    提取时不替换现有文件，静默跳过它们。

- `-U`, `--unlink-first`  
    在提取覆盖每个文件之前先移除它。

- `-W`, `--verify`  
    写入归档后验证归档。

### 输出流选择

- `--ignore-command-error`  
    忽略子进程退出码。

- `--no-ignore-command-error`  
    将子进程的非零退出码视为错误（默认）。

- `-O`, `--to-stdout`  
    将文件提取到标准输出。

- `--to-command=COMMAND`  
    将提取的文件管道传输到 `COMMAND`。参数是外部程序的路径名，可选地带有命令行参数。程序将被调用，正在提取的文件内容通过其标准输入提供。附加数据将通过以下环境变量提供：

    - `TAR_FILETYPE`  
        文件类型。它是具有以下含义的单个字母：
        
        - `f` - 常规文件
        - `d` - 目录
        - `l` - 符号链接
        - `h` - 硬链接
        - `b` - 块设备
        - `c` - 字符设备
        
        目前仅支持常规文件。
    
    - `TAR_MODE`  
        文件模式，八进制数。
    
    - `TAR_FILENAME`  
        文件名。
    
    - `TAR_REALNAME`  
        归档中存储的文件名。
    
    - `TAR_UNAME`  
        文件所有者名称。
    
    - `TAR_GNAME`  
        文件所有者组名称。
    
    - `TAR_ATIME`  
        最后访问时间。它是十进制数，表示自纪元以来的秒数。如果归档提供纳秒精度的时间，纳秒会附加到时间戳小数点后。
    
    - `TAR_MTIME`  
        最后修改时间。
    
    - `TAR_CTIME`  
        最后状态更改时间。
    
    - `TAR_SIZE`  
        文件大小。
    
    - `TAR_UID`  
        文件所有者 UID。
    
    - `TAR_GID`  
        文件所有者 GID。
    
    此外，以下变量包含有关 `tar` 操作模式和正在处理的归档的信息：
    
    - `TAR_VERSION`  
        GNU `tar` 版本号。
    
    - `TAR_ARCHIVE`  
        `tar` 正在处理的归档名称。
    
    - `TAR_BLOCKING_FACTOR`  
        当前块因子，即记录中的 512 字节块数。
    
    - `TAR_VOLUME`  
        `tar` 正在处理的卷的序号（读取多卷归档时设置）。
    
    - `TAR_FORMAT`  
        正在处理的归档格式。之一：`gnu`、`oldgnu`、`posix`、`ustar`、`v7`。
    
    - `TAR_SUBCOMMAND`  
        描述 `tar` 正在执行的操作的短选项（带前导短横线）。

### 文件属性处理

- `--atime-preserve[=METHOD]`  
    保留转储文件的访问时间，可以通过读取后恢复时间（`METHOD`=`replace`，这是默认值）或不最初设置时间（`METHOD`=`system`）。

- `--delay-directory-restore`  
    延迟设置提取目录的修改时间和权限，直到提取结束。当从成员顺序不寻常的归档中提取时使用此选项。

- `--group=NAME[:GID]`  
    强制将 `NAME` 作为添加文件的组。如果未提供 `GID`，`NAME` 可以是用户名或数字 GID。在这种情况下，缺失部分（GID 或名称）将从当前主机的组数据库推断。

    与 `--group-map=FILE` 一起使用时，仅影响所有者组未列在 `FILE` 中的文件。

- `--group-map=FILE`  
    从 `FILE` 读取组翻译映射。忽略空行。注释以 `#` 符号引入并延伸到行尾。`FILE` 中的每个非空行定义单个组的翻译。它必须由两个字段组成，由任意数量的空白分隔：

    `OLDGRP NEWGRP[:NEWGID]`

    `OLDGRP` 是有效的组名或以 `+` 为前缀的 GID。除非提供 `NEWGID`，否则 `NEWGRP` 也必须是有效的组名或 `+GID`。否则，`NEWGRP` 和 `NEWGID` 都不需要列在系统组数据库中。

    因此，所有者组为 `OLDGRP` 的每个输入文件将以所有者组 `NEWGRP` 和 GID `NEWGID` 存储在归档中。

- `--mode=CHANGES`  
    强制为添加文件使用符号模式 `CHANGES`。

- `--mtime=DATE-OR-FILE`  
    为添加文件设置 mtime。`DATE-OR-FILE` 是几乎任意格式的日期/时间，或现有文件的名称。在后一种情况下，将使用该文件的 mtime。

- `-m`, `--touch`  
    不提取文件修改时间。

- `--no-delay-directory-restore`  
    取消先前 `--delay-directory-restore` 选项的效果。

- `--no-same-owner`  
    以自己的身份提取文件（普通用户的默认值）。

- `--no-same-permissions`  
    从归档提取权限时应用用户的 umask（普通用户的默认值）。

- `--numeric-owner`  
    始终对用户/组名使用数字。

- `--owner=NAME[:UID]`  
    强制将 `NAME` 作为添加文件的所有者。如果未提供 `UID`，`NAME` 可以是用户名或数字 UID。在这种情况下，缺失部分（UID 或名称）将从当前主机的用户数据库推断。

    与 `--owner-map=FILE` 一起使用时，仅影响所有者未列在 `FILE` 中的文件。

- `--owner-map=FILE`  
    从 `FILE` 读取所有者翻译映射。忽略空行。注释以 `#` 符号引入并延伸到行尾。`FILE` 中的每个非空行定义单个 UID 的翻译。它必须由两个字段组成，由任意数量的空白分隔：

    `OLDUSR NEWUSR[:NEWUID]`

    `OLDUSR` 是有效的用户名或以 `+` 为前缀的 UID。除非提供 `NEWUID`，否则 `NEWUSR` 也必须是有效的用户名或 `+UID`。否则，`NEWUSR` 和 `NEWUID` 都不需要列在系统用户数据库中。

    因此，由 `OLDUSR` 拥有的每个输入文件将以所有者名 `NEWUSR` 和 UID `NEWUID` 存储在归档中。

- `-p`, `--preserve-permissions`, `--same-permissions`  
    将提取文件的权限设置为归档中记录的权限（超级用户的默认值）。

- `--same-owner`  
    尝试以与归档中存在的相同所有权提取文件（超级用户的默认值）。

- `-s`, `--preserve-order`, `--same-order`  
    告诉 `tar` 要处理的文件名列表按与归档中文件相同的顺序排序。

- `--sort=ORDER`  
    创建归档时，根据 `ORDER` 对目录条目排序，`ORDER` 是 `none`、`name` 或 `inode` 之一。

    默认是 `--sort=none`，按照操作系统返回的顺序存储归档成员。

    使用 `--sort=name` 确保创建归档中的成员顺序统一且可重现。

    使用 `--sort=inode` 减少创建归档时的磁盘 seek 次数，从而可以显著加快归档速度。仅当底层系统提供必要信息时才支持此排序顺序。

### 扩展文件属性

- `--acls`  
    启用 POSIX ACL 支持。

- `--no-acls`  
    禁用 POSIX ACL 支持。

- `--selinux`  
    启用 SELinux 上下文支持。

- `--no-selinux`  
    禁用 SELinux 上下文支持。

- `--xattrs`  
    启用扩展属性支持。

- `--no-xattrs`  
    禁用扩展属性支持。

- `--xattrs-exclude=PATTERN`  
    指定 xattr 键的排除模式。`PATTERN` 是 glob 模式，例如 `--xattrs-exclude='user.*'` 仅包含来自 user 命名空间的属性。

- `--xattrs-include=PATTERN`  
    指定 xattr 键的包含模式。`PATTERN` 是 glob 模式。

### 设备选择和切换

- `-f`, `--file=ARCHIVE`  
    使用归档文件或设备 `ARCHIVE`。如果未给出此选项，`tar` 将首先检查环境变量 `TAPE`。如果设置了，其值将用作归档名称。否则，`tar` 将假定编译时的默认值。可以使用 `--show-defaults` 选项或在 `tar --help` 输出末尾检查默认值。

    包含冒号的归档名称指定远程机器上的文件或设备。冒号前的部分被视为机器名或 IP 地址，冒号后的部分被视为文件或设备路径名，例如：

    `--file=remotehost:/dev/sr0`

    可选用户名可以加在主机名前，两者之间用 `@` 符号分隔。

    默认情况下，远程主机通过 `rsh`(1) 命令访问。如今通常使用 `ssh`(1) 代替。可以通过给出以下命令行选项来实现：

    `--rsh-command=/usr/bin/ssh`

    远程机器应安装 `rmt`(8) 命令。如果其路径名与 `tar` 的默认值不匹配，可以使用 `--rmt-command` 选项告知 `tar` 正确的路径名。

- `--force-local`  
    归档文件是本地的，即使包含冒号。

- `-F`, `--info-script=COMMAND`, `--new-volume-script=COMMAND`  
    在每个磁带末尾运行 `COMMAND`（隐含 `-M`）。命令可以包含参数。启动时，它将继承 `tar` 的环境以及以下变量：

    - `TAR_VERSION`  
        GNU `tar` 版本号。
    - `TAR_ARCHIVE`  
        `tar` 正在处理的归档名称。
    - `TAR_BLOCKING_FACTOR`  
        当前块因子，即记录中的 512 字节块数。
    - `TAR_VOLUME`  
        `tar` 正在处理的卷的序号（读取多卷归档时设置）。
    - `TAR_FORMAT`  
        正在处理的归档格式。之一：`gnu`、`oldgnu`、`posix`、`ustar`、`v7`。
    - `TAR_SUBCOMMAND`  
        描述 `tar` 正在执行的操作的短选项（带前导短横线）。
    - `TAR_FD`  
        可用于将新卷名称传达给 `tar` 的文件描述符。

    如果 info 脚本失败，`tar` 退出；否则，它开始写入下一个卷。

- `-L`, `--tape-length=N`  
    写入 `N`x1024 字节后更换磁带。如果 `N` 后跟大小后缀（参见下文**大小后缀**子节），后缀指定要使用的乘数代替 1024。

    此选项隐含 `-M`。

- `-M`, `--multi-volume`  
    创建/列出/提取多卷归档。

- `--rmt-command=COMMAND`  
    访问远程归档时使用 `COMMAND` 代替 `rmt`。参见上面的 `-f` 选项描述。

- `--rsh-command=COMMAND`  
    访问远程归档时使用 `COMMAND` 代替 `rsh`。参见上面的 `-f` 选项描述。

- `--volno-file=FILE`  
    当此选项与 `--multi-volume` 一起使用时，`tar` 将在 `FILE` 中跟踪它正在处理多卷归档的哪个卷。

### 设备块处理

- `-b`, `--blocking-factor=BLOCKS`  
    将记录大小设置为 `BLOCKS`x`512` 字节。

- `-B`, `--read-full-records`  
    列出或提取时，接受文件结束标记后的不完整输入记录。

- `-i`, `--ignore-zeros`  
    忽略归档中的零块。通常两个连续的填充零的 512 块表示 EOF，`tar` 在遇到它们后停止读取。此选项指示它继续读取，在读取使用 `-A` 选项创建的归档时很有用。

- `--record-size=NUMBER`  
    设置记录大小。`NUMBER` 是每条记录的字节数。必须是 `512` 的倍数。可以带**大小后缀**，例如 `--record-size=10K` 表示 10 KB。有效后缀列表请参见**大小后缀**子节。

### 归档格式选择

- `-H`, `--format=FORMAT`  
    创建给定格式的归档。有效格式为：

    - `gnu` - GNU tar 1.13.x 格式
    - `oldgnu` - 按照 tar <= 1.12 的 GNU 格式。
    - `pax`, `posix` - POSIX 1003.1-2001（pax）格式。
    - `ustar` - POSIX 1003.1-1988（ustar）格式。
    - `v7` - 旧 V7 tar 格式。

- `--old-archive`, `--portability`  
    等同于 `--format=v7`。

- `--pax-option=keyword[[:]=value][,keyword[[:]=value]]...`  
    创建 **PAX** 归档（`-H pax`）时控制 pax 关键字。此选项等价于 `pax`(1) 实用程序的 `-o` 选项。

- `--posix`  
    等同于 `--format=posix`。

- `-V`, `--label=TEXT`  
    创建卷名为 `TEXT` 的归档。如果列出或提取，使用 `TEXT` 作为卷名的 glob 模式。

### 压缩选项

- `-a`, `--auto-compress`  
    使用归档后缀确定压缩程序。

- `-I`, `--use-compress-program=COMMAND`  
    通过 `COMMAND` 过滤数据。它必须接受 `-d` 选项以进行解压。参数可以包含命令行选项。

- `-j`, `--bzip2`  
    通过 `bzip2`(1) 过滤归档。

- `-J`, `--xz`  
    通过 `xz`(1) 过滤归档。

- `--lzip`  
    通过 `lzip`(1) 过滤归档。

- `--lzma`  
    通过 `lzma`(1) 过滤归档。

- `--lzop`  
    通过 `lzop`(1) 过滤归档。

- `--no-auto-compress`  
    不使用归档后缀确定压缩程序。

- `-z`, `--gzip`, `--gunzip`, `--ungzip`  
    通过 `gzip`(1) 过滤归档。

- `-Z`, `--compress`, `--uncompress`  
    通过 `compress`(1) 过滤归档。

- `--zstd`  
    通过 `zstd`(1) 过滤归档。

### 本地文件选择

- `--add-file=FILE`  
    将 `FILE` 添加到归档（当其名称以短横线开头时有用）。

- `--backup[=CONTROL]`  
    移除前备份。如果提供，`CONTROL` 参数控制备份策略。其有效值为：

    - `none`, `off` - 从不备份。
    - `t`, `numbered` - 制作编号备份。
    - `nil`, `existing` - 如果存在编号备份则制作编号备份，否则制作简单备份。
    - `never`, `simple` - 始终制作简单备份

    如果未给出 `CONTROL`，则从 `VERSION_CONTROL` 环境变量获取值。如果未设置，则假定为 `existing`。

- `-C`, `--directory=DIR`  
    在执行任何操作之前切换到 `DIR`。此选项对位置敏感，即它影响其后的所有命令行参数，因此其后出现的任何相对文件名将被视为相对于 `DIR`。但是，它不影响其后*命令行选项*的参数，例如 `-f`、`-T` 或 `-N`。

- `--exclude=PATTERN`  
    排除匹配 `PATTERN` 的文件，`PATTERN` 是 `glob(3)` 风格的通配符模式。

- `--exclude-backups`  
    排除备份和锁文件。

- `--exclude-caches`  
    排除包含文件 `CACHEDIR.TAG` 的目录内容，但标签文件本身除外。`CACHEDIR.TAG` 文件必须是常规文件，其内容以下列 43 个字符开头：

    `Signature: 8a477f597d28d172789f06886806bc55`

- `--exclude-caches-all`  
    排除包含文件 `CACHEDIR.TAG` 的目录及文件本身。

- `--exclude-caches-under`  
    排除包含 `CACHEDIR.TAG` 的目录下的所有内容。

- `--exclude-ignore=FILE`  
    在转储目录之前，检查它是否包含 `FILE`。如果是，则从该文件读取排除模式。模式仅影响目录本身。

- `--exclude-ignore-recursive=FILE`  
    与 `--exclude-ignore` 相同，但 `FILE` 中的模式影响目录及其所有子目录。

- `--exclude-tag=FILE`  
    排除包含 `FILE` 的目录内容，但 `FILE` 本身除外。

- `--exclude-tag-all=FILE`  
    排除包含 `FILE` 的目录。

- `--exclude-tag-under=FILE`  
    排除包含 `FILE` 的目录下的所有内容。

- `--exclude-vcs`  
    排除版本控制系统目录。

- `--exclude-vcs-ignores`  
    排除匹配从 VCS 特定忽略文件读取的模式的文件。支持的文件为：`.cvsignore`、`.gitignore`、`.bzrignore` 和 `.hgignore`。

- `-h`, `--dereference`  
    跟随符号链接；归档并转储它们指向的文件。

- `--hard-dereference`  
    跟随硬链接；归档并转储它们引用的文件。

- `-K`, `--starting-file=MEMBER`  
    从归档中的给定成员开始。

- `--newer-mtime=DATE`  
    处理数据在 `DATE` 之后更改的文件。如果 `DATE` 以 `/` 或 `.` 开头，则被视为文件名；该文件的 mtime 用作日期。

- `--no-null`  
    禁用先前 `--null` 选项的效果。

- `--no-recursion`  
    避免自动进入目录。

- `--no-unquote`  
    不对输入文件或成员名进行去引号。

- `--no-verbatim-files-from`  
    将从文件列表读取的每一行视为在命令行中提供的一样。即，移除前导和尾随空白，并且如果结果字符串以短横线开头，则将其视为 `tar` 命令行选项。

    这是默认行为。`--no-verbatim-files-from` 选项提供了一种在 `--verbatim-files-from` 选项之后恢复它的方法。

    此选项对位置敏感：它影响其后出现的所有 `--files-from` 选项，直到 `--verbatim-files-from` 选项或行尾（以先出现者为准）。

    它由 `--null` 选项隐含。

- `--null`  
    指示后续 `-T` 选项按原样读取以 null 结尾的名称（禁用对以短横线开头的名称的特殊处理）。

    另请参见 `--verbatim-files-from`。

- `-N`, `--newer=DATE`, `--after-date=DATE`  
    仅存储比 DATE 新的文件。如果 `DATE` 以 `/` 或 `.` 开头，则被视为文件名；该文件的 mtime 用作日期。

- `--one-file-system`  
    创建归档时停留在本地文件系统。

- `-P`, `--absolute-names`  
    创建归档时不剥离文件名的前导斜杠。

- `--recursion`  
    递归进入目录（默认）。

- `--suffix=STRING`  
    移除前备份，覆盖通常的后缀。默认后缀是 `~`，除非被环境变量 `SIMPLE_BACKUP_SUFFIX` 覆盖。

- `-T`, `--files-from=FILE`  
    从 `FILE` 获取要提取或创建的名称。

    除非另有指定，`FILE` 必须包含以 ASCII `LF` 分隔的名称列表（即每行一个名称）。读取的名称与命令行参数处理方式相同。它们经历去引号和单词拆分，任何以 `-` 开头的字符串都作为 `tar` 命令行选项处理。

    如果此行为不理想，可以使用 `--verbatim-files-from` 选项关闭它。

    `--null` 选项指示 `tar`，`FILE` 中的名称由 ASCII `NUL` 字符分隔，而不是 `LF`。如果列表由 `find(1) -print0` 谓词生成，则很有用。

    除了文件名，`FILE` 还可以包含 `tar` 命令行选项的子集，特别是 `-C` 和 `-T`。详细列表请参见 **GNU tar 手册**第 6.3 节“**从文件读取名称**”。

- `--unquote`  
    对文件或成员名去引号（默认）。

- `--verbatim-files-from`  
    将从文件列表获得的每一行视为文件名，即使它以短横线开头。文件列表由 `--files-from`（`-T`）选项提供。默认行为是将文件列表中提供的名称视为在命令行中输入的一样，即任何以短横线开头的名称都被视为 `tar` 选项。`--verbatim-files-from` 选项禁用此行为。

    此选项影响命令行中其后出现的所有 `--files-from` 选项。其效果由 `--no-verbatim-files-from` 选项恢复。

    此选项由 `--null` 选项隐含。

    另请参见 `--add-file`。

- `-X`, `--exclude-from=FILE`  
    排除匹配 FILE 中列出的模式的文件。

### 文件名转换

- `--strip-components=NUMBER`  
    提取时从文件名中剥离 `NUMBER` 个前导组件。

- `--transform=EXPRESSION`, `--xform=EXPRESSION`  
    使用 sed 替换 `EXPRESSION` 转换文件名。

### 文件名匹配选项

这些选项影响排除和包含模式。

- `--anchored`  
    模式匹配文件名开头。

- `--ignore-case`  
    忽略大小写。

- `--no-anchored`  
    模式在任意 `/` 后匹配（排除的默认值）。

- `--no-ignore-case`  
    区分大小写匹配（默认）。

- `--no-wildcards`  
    逐字字符串匹配。

- `--no-wildcards-match-slash`  
    通配符不匹配 `/`。

- `--wildcards`  
    使用通配符（排除的默认值）。

- `--wildcards-match-slash`  
    通配符匹配 `/`（排除的默认值）。

### 信息输出

- `--checkpoint[=N]`  
    每第 `N` 条记录显示进度消息（默认 10）。

- `--checkpoint-action=ACTION`  
    在每个检查点运行 `ACTION`。

- `--clamp-mtime`  
    仅当文件比 `--mtime` 给出的时间更新时才设置时间。

- `--full-time`  
    以其完整分辨率打印文件时间。

- `--index-file=FILE`  
    将详细输出发送到 `FILE`。

- `-l`, `--check-links`  
    如果不是所有链接都被转储，则打印消息。

- `--no-quote-chars=STRING`  
    对 `STRING` 中的字符禁用引号。

- `--quote-chars=STRING`  
    额外对 `STRING` 中的字符加引号。

- `--quoting-style=STYLE`  
    设置文件和成员名的引号风格。`STYLE` 的有效值为 `literal`、`shell`、`shell-always`、`c`、`c-maybe`、`escape`、`locale`、`clocale`。

- `-R`, `--block-number`  
    在每条消息中显示归档内的块号。

- `--show-omitted-dirs`  
    列出或提取时，列出每个不匹配搜索条件的目录。

- `--show-transformed-names`, `--show-stored-names`  
    显示经过 `--strip` 和 `--transform` 选项转换后的文件或归档名称。

- `--totals[=SIGNAL]`  
    处理归档后打印总字节数。如果给出 `SIGNAL`，则在此信号传递时打印总字节数。允许的信号为：`SIGHUP`、`SIGQUIT`、`SIGINT`、`SIGUSR1` 和 `SIGUSR2`。`SIG` 前缀可以省略。

- `--utc`  
    以 UTC 打印文件修改时间。

- `-v`, `--verbose`  
    详细列出已处理的文件。命令行中此选项的每个实例将详细级别提高一。最大详细级别为 3。关于各种详细级别如何影响 tar 输出的详细讨论，请参阅 **GNU Tar 手册**第 2.5.2 小节“**`--verbose` 选项**”。

- `--warning=KEYWORD`  
    启用或禁用由 `KEYWORD` 标识的警告消息。如果 `KEYWORD` 以 `no-` 为前缀则抑制消息，否则启用。

    多个 `--warning` 选项会累积。

    控制一般 `tar` 操作的关键字：

    - `all` - 启用所有警告消息。这是默认值。
    - `none` - 禁用所有警告消息。
    - `filename-with-nuls` - `"%s: file name read contains nul character"`
    - `alone-zero-block` - `"A lone zero block at %s"`

    适用于 `tar --create` 的关键字：

    - `cachedir` - `"%s: contains a cache directory tag %s; %s"`
    - `file-shrank` - `"%s: File shrank by %s bytes; padding with zeros"`
    - `xdev` - `"%s: file is on a different filesystem; not dumped"`
    - `file-ignored` - `"%s: Unknown file type; file ignored"`、`"%s: socket ignored"`、`"%s: door ignored"`
    - `file-unchanged` - `"%s: file is unchanged; not dumped"`
    - `ignore-archive` - `"%s: archive cannot contain itself; not dumped"`
    - `file-removed` - `"%s: File removed before we read it"`
    - `file-changed` - `"%s: file changed as we read it"`
    - `failed-read` - 抑制有关不可读文件或目录的警告。此关键字仅在 `--ignore-failed-read` 选项一起使用时适用。

    适用于 `tar --extract` 的关键字：

    - `existing-file` - `"%s: skipping existing file"`
    - `timestamp` - `"%s: implausibly old time stamp %s"`、`"%s: time stamp %s is %s s in the future"`
    - `contiguous-cast` - `"Extracting contiguous files as regular files"`
    - `symlink-cast` - `"Attempting extraction of symbolic links as hard links"`
    - `unknown-cast` - `"%s: Unknown file type '%c', extracted as normal file"`
    - `ignore-newer` - `"Current %s is newer or same age"`
    - `unknown-keyword` - `"Ignoring unknown extended header keyword '%s'"`
    - `decompress-program` - 控制尝试运行替代解压程序时发生的失败的详细描述。此警告默认禁用（除非使用 `--verbose`）。使用此警告时可能得到的常见示例是：

        ```
        $ tar --warning=decompress-program -x -f archive.Z
        tar (child): cannot run compress: No such file or directory
        tar (child): trying gzip
        ```
        
        这意味着 `tar` 首先尝试使用 `compress` 解压 `archive.Z`，失败后切换到 `gzip`。
    
    - `record-size` - `"Record size = %lu blocks"`

    控制增量提取的关键字：

    - `rename-directory` - `"%s: Directory has been renamed from %s"`、`"%s: Directory has been renamed"`
    - `new-directory` - `"%s: Directory is new"`
    - `xdev` - `"%s: directory is on a different device: not purging"`
    - `bad-dumpdir` - `"Malformed dumpdir: 'X' never used"`

- `-w`, `--interactive`, `--confirmation`  
    对每个操作请求确认。

### 兼容性选项

- `-o`  
    创建时，等同于 `--old-archive`。提取时，等同于 `--no-same-owner`。

### 大小后缀

| 后缀 | 单位 | 字节等效值 |
| --- | --- | --- |
| `b` | 块 | `SIZE` x 512 |
| `B` | 千字节 | `SIZE` x 1024 |
| `c` | 字节 | `SIZE` |
| `G` | 吉字节 | `SIZE` x 1024^3 |
| `K` | 千字节 | `SIZE` x 1024 |
| `k` | 千字节 | `SIZE` x 1024 |
| `M` | 兆字节 | `SIZE` x 1024^2 |
| `P` | 拍字节 | `SIZE` x 1024^5 |
| `T` | 太字节 | `SIZE` x 1024^4 |
| `w` | 字 | `SIZE` x 2 |

## 返回值

Tar 的退出码指示它是否能够成功执行请求的操作，如果不能，则指示发生了什么类型的错误。

- `0` - 成功终止。
- `1` - *某些文件不同。* 如果 `tar` 使用 `--compare`（`--diff`、`-d`）命令行选项调用，这意味着归档中的某些文件与其磁盘对应文件不同。如果 `tar` 被赋予 `--create`、`--append` 或 `--update` 选项之一，此退出码意味着某些文件在归档时发生了更改，因此结果归档不包含文件集的精确副本。
- `2` - *致命错误。* 这意味着发生了某些致命、不可恢复的错误。

如果 `tar` 调用的子进程以非零退出码退出，`tar` 本身也以该代码退出。例如，如果使用了压缩选项（例如 `-z`）且外部压缩程序失败，则可能发生这种情况。另一个例子是备份到远程设备期间 `rmt` 失败。

## 另请参见

`bzip2`(1), `compress`(1), `gzip`(1), `lzma`(1), `lzop`(1), `rmt`(8), `symlink(7)`, `xz`(1), `zstd`(1).

完整 `tar` 手册：运行 `info tar` 或使用 `emacs`(1) info 模式阅读。

各种格式的 **GNU tar** 文档在线副本可在以下网址找到：

<https://www.gnu.org/software/tar/manual>

## 缺陷报告

将缺陷报告发送至 <bug-tar@gnu.org>。

## 版权

版权所有 © 2013–2026 Free Software Foundation, Inc.
许可证 GPLv3+：GNU GPL 版本 3 或更高版本
<http://gnu.org/licenses/gpl.html>
这是自由软件：您可以自由更改和重新分发它。
在法律允许的范围内，不提供任何保证。

## 版本说明

本页面是 *tar*（归档程序）项目的一部分。项目信息可在 <http://savannah.gnu.org/projects/tar/> 找到。如果您对本手册页有缺陷报告，请参见 <http://savannah.gnu.org/bugs/?group=tar>。此页面获取自项目的上游 Git 仓库 [git://git.savannah.gnu.org/tar.git](git://git.savannah.gnu.org/tar.git)，日期为 2026-08-04。（当时在仓库中找到的最新提交日期为 2026-07-29。）如果您发现此 HTML 版页面存在渲染问题，或认为有更好或更新的页面来源，或对版本说明中的信息（不属于原始手册页）有更正或改进，请发送邮件至 man-pages@man7.org。

---

TAR                           June 11, 2026                        *TAR*(1)