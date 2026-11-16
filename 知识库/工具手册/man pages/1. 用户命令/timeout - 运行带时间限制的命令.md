https://man7.org/linux/man-pages/man1/timeout.1.html

# `timeout` - 运行带时间限制的命令

## 概要

```sh
timeout [OPTION]... DURATION COMMAND [ARG]...
```

## 描述

启动 `COMMAND`，如果它在 `DURATION` 之后仍在运行，则将其杀死。

长选项的必需参数对短选项也是必需的。

- `-f`, `--foreground`  
    当不是直接从 shell 提示符运行 `timeout` 时，允许 `COMMAND` 从 TTY 读取并获取 TTY 信号；在此模式下，`COMMAND` 的子进程不会超时

- `-k`, `--kill-after=DURATION`  
    如果 `COMMAND` 在初始信号发送后经过这么长时间仍在运行，也发送 `KILL` 信号

- `-p`, `--preserve-status`  
    以与 `COMMAND` 相同的状态退出，即使命令超时

- `-s`, `--signal=SIGNAL`  
    指定超时时要发送的信号；`SIGNAL` 可以是类似 `HUP` 的名称或数字；关于信号列表，参见 `kill -l`

- `-v`, `--verbose`  
    将超时时发送的任何信号诊断到标准错误

- `--help`  
    显示此帮助并退出

- `--version`  
    输出版本信息并退出

`DURATION` 是浮点数，可选后缀：`s` 表示秒（默认），`m` 表示分钟，`h` 表示小时，`d` 表示天。持续时间为 0 会禁用关联的超时。

超时时，如果没有指定其他 `SIGNAL`，则向 `COMMAND` 发送 `TERM` 信号。`TERM` 信号会杀死任何不阻塞或捕获该信号的进程。可能有必要使用 `KILL` 信号，因为此信号无法被捕获。

**退出状态：**

- `124`  
    如果 `COMMAND` 超时，且未指定 `--preserve-status`

- `125`  
    如果 `timeout` 命令本身失败

- `126`  
    如果找到 `COMMAND` 但无法调用

- `127`  
    如果无法找到 `COMMAND`

- `137`  
    如果 `COMMAND`（或 `timeout` 本身）被发送 `KILL` (9) 信号（128+9）

- `-`  
    否则为 `COMMAND` 的退出状态

## 缺陷

某些平台目前不支持超过 2038 年的超时。

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

“kill(1)”

完整文档：<https://www.gnu.org/software/coreutils/timeout>，或通过以下命令在本地获取：`info '(coreutils) timeout invocation'`

## 版本说明

本页是 `coreutils`（基本文件、shell 和文本操作实用程序）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页获取自 2026-08-03 从 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩ 下载的 tarball `coreutils-9.11.tar.xz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
GNU coreutils 9.11              April 2026                     TIMEOUT(1)
```