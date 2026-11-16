https://man7.org/linux/man-pages/man1/stdbuf.1.html

# `stdbuf` - 运行 `COMMAND`，并修改其标准流的缓冲操作。

## 概要

```sh
stdbuf OPTION... COMMAND
```

## 描述

运行 `COMMAND`，并修改其标准流的缓冲操作。

长选项的必需参数对短选项也是必需的。

- `-i, --input=MODE`  
    调整标准输入流缓冲

- `-o, --output=MODE`  
    调整标准输出流缓冲

- `-e, --error=MODE`  
    调整标准错误流缓冲

- `--help`  
    显示此帮助并退出

- `--version`  
    输出版本信息并退出

如果 `MODE` 为 `L`，则相应流将采用行缓冲。此选项对标准输入无效。

如果 `MODE` 为 `0`，则相应流将不缓冲。

否则，`MODE` 是一个数字，后面可以跟以下之一：`KB` 表示 1000，`K` 表示 1024，`MB` 表示 1000*1000，`M` 表示 1024*1024，对于 `G`、`T`、`P`、`E`、`Z`、`Y`、`R`、`Q` 依此类推。也可以使用二进制前缀：`KiB=K`、`MiB=M` 等。在这种情况下，相应流将采用完全缓冲，缓冲区大小设置为 `MODE` 字节。

注意：如果 `COMMAND` 调整其标准流的缓冲（例如 `tee` 会这样做），那么这将覆盖 `stdbuf` 的相应更改。此外，某些过滤器（如 `dd` 和 `cat` 等）不使用流进行 I/O，因此不受 `stdbuf` 设置的影响。

**退出状态：**

- `125`  
    如果 `stdbuf` 命令本身失败

- `126`  
    如果找到 `COMMAND` 但无法调用

- `127`  
    如果无法找到 `COMMAND`

- `-`  
    否则为 `COMMAND` 的退出状态

## 示例

```sh
tail -f access.log | stdbuf -oL cut -d ' ' -f1 | uniq
```

这将立即显示 `access.log` 中的唯一条目。

## 缺陷

在 GLIBC 平台上，指定缓冲区大小（即使用完全缓冲模式）将导致未定义操作。

## 作者

由 Padraig Brady 编写。

## 报告缺陷

- 将缺陷报告发送至：`bug-coreutils@gnu.org`
- GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
- 使用 GNU 软件的一般帮助：<https://www.gnu.org/gethelp/>
- 将任何翻译缺陷报告至：<https://translationproject.org/team/>

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 `GPLv3+`：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参见

完整文档：<https://www.gnu.org/software/coreutils/stdbuf>，或通过以下命令在本地获取：`info '(coreutils) stdbuf invocation'`

## 版本说明

本页是 `coreutils`（基本文件、shell 和文本操作实用程序）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页获取自 2026-08-03 从 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩ 下载的 tarball `coreutils-9.11.tar.xz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
GNU coreutils 9.11              April 2026                      STDBUF(1)
```