https://linux.die.net/man/1/cpio

## 名称

`cpio` - 将文件复制到归档中或从归档中复制

## 概要

**Copy-out 模式**

在 copy-out 模式中，`cpio` 将文件复制到归档中。它从标准输入读取文件名列表（每行一个），并将归档写入标准输出。生成文件名列表的典型方法是使用 `find` 命令；应给 `find` 加上 `-depth` 选项，以尽量减少不可读目录权限带来的问题。参见“选项”。

```sh
cpio {-o|--create} [-0acvABLV] [-C bytes] [-H format] [-M message] [-O [[user@]host:]archive] [-F [[user@]host:]archive] [--file=[[user@]host:]archive] [--format=format] [--message=message] [--null] [--reset-access-time] [--verbose] [--dot] [--append] [--block-size=blocks] [--dereference] [--io-size=bytes] [--rsh-command=command] [--help] [--version] < name-list [> archive]
```

**Copy-in 模式**

在 copy-in 模式中，`cpio` 从归档中复制文件或列出归档内容。它从标准输入读取归档。任何非选项命令行参数都是 shell 通配模式；只有归档中名称匹配一个或多个这些模式的文件才会从归档中复制。与 shell 不同，文件名开头的 `.` 会匹配模式开头的通配符，文件名中的 `/` 可以匹配通配符。如果未给出模式，则提取所有文件。参见“选项”。

```sh
cpio {-i|--extract} [-bcdfmnrtsuvBSV] [-C bytes] [-E file] [-H format] [-M message] [-R [user][:.][group]] [-I [[user@]host:]archive] [-F [[user@]host:]archive] [--file=[[user@]host:]archive] [--make-directories] [--nonmatching] [--preserve-modification-time] [--numeric-uid-gid] [--rename] [-t|--list] [--swap-bytes] [--swap] [--dot] [--unconditional] [--verbose] [--block-size=blocks] [--swap-halfwords] [--io-size=bytes] [--pattern-file=file] [--format=format] [--owner=[user][:.][group]] [--no-preserve-owner] [--message=message] [--force-local] [--no-absolute-filenames] [--absolute-filenames] [--sparse] [--only-verify-crc] [--to-stdout] [--quiet] [--rsh-command=command] [--help] [--version] [pattern...] [< archive]
```

**Copy-pass 模式**

在 copy-pass 模式中，`cpio` 将文件从一个目录树复制到另一个目录树，结合 copy-out 和 copy-in 步骤而不实际使用归档。它从标准输入读取要复制的文件列表；要复制到的目录作为非选项参数给出。参见“选项”。

```sh
cpio {-p|--pass-through} [-0adlmuvLV] [-R [user][:.][group]] [--null] [--reset-access-time] [--make-directories] [--link] [--quiet] [--preserve-modification-time] [--unconditional] [--verbose] [--dot] [--dereference] [--owner=[user][:.][group]] [--no-preserve-owner] [--sparse] [--help] [--version] destination-directory < name-list
```

## 描述

GNU `cpio` 是用于创建和解压归档，或将文件从一个位置复制到另一个位置的工具。它处理多种 `cpio` 格式，以及读取和写入 tar 文件。

支持以下归档格式：binary、old ASCII、new ASCII、crc、HPUX binary、HPUX old ASCII、old tar 和 POSIX.1 tar。提供 tar 格式是为了与 tar 程序兼容。默认情况下，`cpio` 创建 binary 格式归档，以与旧版 `cpio` 程序兼容。从归档提取时，`cpio` 会自动识别正在读取的归档类型，并且可以读取在不同字节序机器上创建的归档。

## 选项

- `-0`, `--null`  
    从标准输入读取以 null 字符（而不是换行符）终止的文件名列表，以便名称中包含换行符的文件也可以被归档。GNU `find` 是生成以 null 终止的文件名列表的一种方式。此选项可用于 copy-out 和 copy-pass 模式。

- `-a`, `--reset-access-time`  
    在读取文件后重置文件的访问时间，使其看起来不像刚被读取过。

- `-A`, `--append`  
    追加到现有归档。仅在 copy-out 模式下工作。归档必须是通过 `-O` 或 `-F`（`--file`）选项指定的磁盘文件。

- `-b`, `--swap`  
    交换数据中字的两个半字以及半字的字节。等同于 `-sS`。此选项可用于 copy-in 模式。使用此选项可在 big-endian 和 little-endian 机器之间转换 32 位整数。

- `-B`  
    将 I/O 块大小设置为 5120 字节。初始块大小为 512 字节。

- `--block-size=BLOCK-SIZE`  
    将 I/O 块大小设置为 `BLOCK-SIZE` * 512 字节。

- `-c`  
    等同于 `-H newc`，使用新的（SVR4）可移植格式。如果希望使用旧的可移植（ASCII）归档格式，请改用 `-H odc`。

- `-C IO-SIZE`, `--io-size=IO-SIZE`  
    将 I/O 块大小设置为 `IO-SIZE` 字节。

- `-d`, `--make-directories`  
    根据需要创建前导目录。

- `-E FILE`, `--pattern-file=FILE`  
    从 `FILE` 读取指定要提取或列出的文件名的附加模式。`FILE` 的行被视为如同它们是 `cpio` 的非选项参数。此选项用于 copy-in 模式。

- `-f`, `--nonmatching`  
    仅复制不匹配任何给定模式的文件。

- `-F`, `--file=archive`  
    要使用的归档文件名，而不是标准输入或输出。要使用另一台机器上的磁带驱动器作为归档，请使用以 `HOSTNAME:` 开头的文件名。主机名前面可以加上用户名和 `@`，以便以该用户身份访问远程磁带驱动器（如果你有相应权限，通常是该用户的 `~/.rhosts` 文件中的条目）。

- `--force-local`  
    与 `-F`、`-I` 或 `-O` 一起使用时，将归档文件名视为本地文件，即使它包含冒号（通常冒号表示远程主机名）。

- `-H FORMAT`, `--format=FORMAT`  
    使用归档格式 `FORMAT`。有效格式列在下面；相同名称也以全大写形式识别。copy-in 模式的默认值是自动检测归档格式，copy-out 模式的默认值是 `bin`。

- `bin`  
    过时的 binary 格式。

- `odc`  
    旧的（POSIX.1）可移植格式。

- `newc`  
    新的（SVR4）可移植格式，支持 inode 数超过 65536 的文件系统。

- `crc`  
    带校验和的新的（SVR4）可移植格式。

- `tar`  
    旧的 tar 格式。

- `ustar`  
    POSIX.1 tar 格式。也识别 GNU tar 归档，其相似但不完全相同。

- `hpbin`  
    HPUX 的 `cpio` 使用的过时 binary 格式（存储设备文件的方式不同）。

- `hpodc`  
    HPUX 的 `cpio` 使用的可移植格式（存储设备文件的方式不同）。

- `-i`, `--extract`  
    以 copy-in 模式运行。参见“Copy-in 模式”。

- `-I archive`  
    要使用的归档文件名，而不是标准输入。要使用另一台机器上的磁带驱动器作为归档，请使用以 `HOSTNAME:` 开头的文件名。主机名前面可以加上用户名和 `@`，以便以该用户身份访问远程磁带驱动器（如果你有相应权限，通常是该用户的 `~/.rhosts` 文件中的条目）。

- `-k`  
    忽略；用于与其他版本的 `cpio` 兼容。

- `-l`, `--link`  
    在可能的情况下链接文件，而不是复制它们。

- `-L`, `--dereference`  
    复制符号链接指向的文件，而不是符号链接本身。

- `-m`, `--preserve-modification-time`  
    创建文件时保留先前的文件修改时间。

- `-M MESSAGE`, `--message=MESSAGE`  
    当到达备份介质（如磁带或软盘）的卷末时打印 `MESSAGE`，提示用户插入新卷。如果 `MESSAGE` 包含字符串 `%d`，它将被当前卷号（从 1 开始）替换。

- `-n`, `--numeric-uid-gid`  
    使用 `--verbose` 选项时，显示数字 `UID` 和 `GID`，而不是将其转换为名称。

- `--no-absolute-filenames`  
    在 copy-in 模式下，相对于当前目录创建所有文件，即使它们在归档中具有绝对文件名。

- `--absolute-filenames`（默认）  
    在 copy-in 模式下，不剥离文件名中包含 `..` 的前导文件名组件和前导斜杠。

- `--no-preserve-owner`  
    不更改文件的所有权；让它们由提取它们的用户拥有。这是非 root 用户的默认值，这样 System V 上的用户就不会无意中泄露文件。此选项可用于 copy-in 模式和 copy-pass 模式。

- `-o`, `--create`  
    以 copy-out 模式运行。参见“Copy-out 模式”。

- `-O archive`  
    要使用的归档文件名，而不是标准输出。要使用另一台机器上的磁带驱动器作为归档，请使用以 `HOSTNAME:` 开头的文件名。主机名前面可以加上用户名和 `@`，以便以该用户身份访问远程磁带驱动器（如果你有相应权限，通常是该用户的 `~/.rhosts` 文件中的条目）。

- `--only-verify-crc`  
    读取 CRC 格式归档时，验证归档中每个文件的 `CRC`。不实际提取文件。

- `-p`, `--pass-through`  
    以 copy-pass 模式运行。参见“Copy-pass 模式”。

- `--quiet`  
    不打印复制的块数。

- `-r`, `--rename`  
    交互式重命名文件。

- `-R [user][:.][group]`, `--owner [user][:.][group]`  
    在 copy-out 和 copy-pass 模式下，将所有创建文件的所有权设置为指定用户和/或组。用户、组或两者必须存在。如果省略组但给出了 `:` 或 `.` 分隔符，则使用给定用户的登录组。只有超级用户可以更改文件的所有权。

- `--rsh-command=COMMAND`  
    通知 `cpio` 应使用 `COMMAND` 与远程设备通信。

- `-s`, `--swap-bytes`  
    交换文件中每个半字（一对字节）的字节。此选项可用于 copy-in 模式。

- `-S`, `--swap-halfwords`  
    交换文件中每个字（4 字节）的半字。此选项可用于 copy-in 模式。

- `--sparse`  
    将具有大块零的文件写为稀疏文件。此选项用于 copy-in 和 copy-pass 模式。

- `-t`, `--list`  
    打印输入的内容表。

- `--to-stdout`  
    将文件提取到标准输出。此选项可用于 copy-in 模式。

- `-u`, `--unconditional`  
    替换所有文件，而不询问是否用较旧的文件替换现有的较新文件。

- `-v`, `--verbose`  
    列出已处理的文件，或与 `-t` 一起使用时，给出 `ls -l` 风格的内容表列表。在 ustar 归档的详细内容表中，归档中本地系统上不存在的用户和组名称将被替换为与归档中存储的数字 `UID` 和 `GID` 本地对应的名称。

- `-V`, `--dot`  
    为每个处理的文件打印一个 `.`。

- `--version`  
    打印 `cpio` 程序版本号并退出。

## 示例

创建归档时，`cpio` 从标准输入获取要处理的文件列表，然后将归档发送到标准输出，或发送到由 `-F` 选项定义的设备。通常使用 `find` 或 `ls` 将此列表提供给标准输入。在以下示例中，可以看到归档单个目录内容的各种可能性。

```sh
ls | cpio -ov > directory.cpio
```

`-o` 选项创建归档，`-v` 选项在添加文件时打印归档文件的名称。注意，选项可以在单个 `-` 之后组合在一起，也可以在命令行上分开放置。`>` 将 `cpio` 输出重定向到文件 `directory.cpio`。

如果要归档整个目录树，`find` 命令可以提供文件列表给 `cpio`：

```sh
find . -print -depth | cpio -ov > tree.cpio
```

这将获取当前目录及以下目录中的所有文件，并将它们放入归档 `tree.cpio` 中。同样，`-o` 创建归档，`-v` 选项在归档时显示文件名。参见“Copy-out 模式”。在 `find` 语句中使用 `.` 将在进行还原时提供更大的灵活性，因为它以相对路径而非硬编码的绝对路径保存文件名。`-depth` 选项强制 `find` 在打印目录本身之前打印目录中的条目。这通过在目录名本身之前打印目录中的目录条目，限制了限制性目录权限的影响。

提取归档需要多思考一些，因为 `cpio` 默认不会创建目录。另一个特点是，除非你告诉它，否则它不会覆盖现有文件。

```sh
cpio -iv < directory.cpio
```

这将取回归档文件 `directory.cpio` 中的文件并将它们放在当前目录中。`-i` 选项提取归档，`-v` 显示提取时的文件名。如果你处理的是归档的目录树，需要使用 `-d` 选项根据需要创建目录，类似：

```sh
cpio -idv < tree.cpio
```

这将取出归档 `tree.cpio` 的内容并将其提取到当前目录。如果你尝试在已存在的同名文件（且具有相同或更晚的修改时间）之上提取文件，`cpio` 不会提取该文件，除非通过 `-u` 选项告诉它这样做。参见“Copy-in 模式”。

在 copy-pass 模式中，`cpio` 将文件从一个目录树复制到另一个目录树，结合 copy-out 和 copy-in 步骤而不实际使用归档。它从标准输入读取要复制的文件列表；要复制到的目录作为非选项参数给出。参见“Copy-pass 模式”。

```sh
find . -depth -print0 | cpio --null -pvd new-dir
```

该示例展示了将当前目录及子目录的文件复制到名为 `new-dir` 的新目录。一些新选项是 GNU `find` 提供的 `-print0`，与 `cpio` 的 `--null` 选项结合使用。这两个选项一起工作，在 `find` 和 `cpio` 之间传递文件名，即使文件名中嵌入了特殊字符。另一个是 `-p`，它告诉 `cpio` 将找到的文件传递到目录 `new-dir`。

## 缺陷

GNU 人员通常厌恶 man 手册页，而是创建 info 文档。`cpio` 的维护者属于这一类。因此，本 man 手册页可能不完整、不是最新的，它被包含在 Red Hat CVS 树中是因为 man 是一个很棒的工具 :)。

## 报告缺陷

请通过 <https://bugzilla.redhat.com> 报告缺陷。

## 另请参见

`cpio` 的完整文档作为 Texinfo 手册维护。如果 `info` 和 `cpio` 程序在您的站点上正确安装，命令

```sh
info cpio
```

应能让您访问完整手册。文档的在线副本可在以下地址获得：

<http://www.gnu.org/software/cpio/manual>

## 被引用

“afio”(1)、“archivemount”(1)、“attr”(1)、“cpdup”(1)、“febootstrap-to-initramfs”(8)、“libarchive-formats”(5)、“pax”(1)、“star”(1)、“superpaco”(8)