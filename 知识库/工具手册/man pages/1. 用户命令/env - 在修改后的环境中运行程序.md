https://www.man7.org/linux/man-pages/man1/env.1.html

# `env` - 在修改后的环境中运行程序

## 概要

```sh
env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]
```

## 描述

在环境中将每个 `NAME` 设置为 `VALUE`，并运行 `COMMAND`。

长选项的必需参数对短选项也是必需的。

- `-a, --argv0=ARG`  
    将 `ARG` 作为 `COMMAND` 的第零个参数传递

- `-i, --ignore-environment`  
    以空环境开始

- `-0, --null`  
    以 `NUL`（而不是换行符）结束每个输出行

- `-u, --unset=NAME`  
    从环境中移除变量 `NAME`

- `-C, --chdir=DIR`  
    将工作目录更改为 `DIR`

- `-S, --split-string=S`  
    处理并将 `S` 拆分为单独的参数；用于在 `shebang` 行上传递多个参数

- `--block-signal[=SIG]`  
    阻止向 `COMMAND` 传递 `SIG` 信号

- `--default-signal[=SIG]`  
    将 `SIG` 信号的处理重置为默认值

- `--ignore-signal[=SIG]`  
    将 `SIG` 信号的处理设置为不执行任何操作

- `--list-signal-handling`  
    将非默认信号处理列出到标准错误

- `-v, --debug`  
    为每个处理步骤打印详细的信息

- `--help`  
    显示此帮助并退出

- `--version`  
    输出版本信息并退出

单独的 `-` 意味着 `-i`。如果没有 `COMMAND`，则打印结果环境。

`SIG` 可以是类似 `'PIPE'` 的信号名，或类似 `'13'` 的信号编号。没有 `SIG` 时，包含所有已知信号。多个信号可以用逗号分隔。空的 `SIG` 参数是空操作。

### 退出状态

- `125`  
    如果 `env` 命令本身失败

- `126`  
    如果找到 `COMMAND` 但无法调用

- `127`  
    如果无法找到 `COMMAND`

- `-`  
    否则为 `COMMAND` 的退出状态

## 脚本选项处理

`-S` 选项允许在脚本中指定多个参数。运行名为 `1.pl` 的脚本，其首行如下：

```sh
#!/usr/bin/env -S perl -w -T
...
```

将执行 `perl -w -T 1.pl`。

没有 `-S` 参数时，脚本很可能失败并显示：

```log
/usr/bin/env: 'perl -w -T': No such file or directory
```

更多详细信息请参见完整文档。

## 注意事项

POSIX 的 “exec(3p)” 页面说：

> “许多现有应用程序错误地假定它们启动时某些信号被设置为默认操作和/或未被阻塞……因此，最好不要在没有明确理由的情况下跨 `exec` 阻塞或忽略信号，尤其不要跨任意（非紧密协作）程序的 `exec` 阻塞信号。”

## 作者

由 Richard Mlynarik、David MacKenzie 和 Assaf Gordon 编写。

## 报告缺陷

- 将缺陷报告发送至：`bug-coreutils@gnu.org`
- GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
- 使用 GNU 软件的一般帮助：<https://www.gnu.org/gethelp/>
- 将任何翻译缺陷报告至：<https://translationproject.org/team/>

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 `GPLv3+`：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参见

“sigaction(2)”、“sigprocmask(2)”、“signal(7)”

完整文档：<https://www.gnu.org/software/coreutils/env>，或通过以下命令在本地获取：`info '(coreutils) env invocation'`

## 版本说明

本页是 `coreutils`（基本文件、shell 和文本操作实用程序）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页获取自 2026-08-03 从 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩ 下载的 tarball `coreutils-9.11.tar.xz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
GNU coreutils 9.11              April 2026                         ENV(1)
```