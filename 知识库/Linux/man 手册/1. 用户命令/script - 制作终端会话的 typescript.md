https://www.man7.org/linux/man-pages/man1/script.1.html

# `script` - 制作终端会话的 typescript

## 概要

```sh
script [options] [file] [-- command [argument...]]
```

## 描述

`script` 会制作终端会话中所有内容的 typescript。终端数据以原始形式存储到日志文件，计时信息存储到另一个（可选的）结构化日志文件。计时日志文件对于之后由 [scriptreplay(1)] 重放会话以及存储会话附加信息是必要的。

自 2.35 版本起，`script` 支持多流，并允许将输入和输出记录到单独文件或同一个文件。此版本还支持一种新的计时文件，用于记录附加信息。命令 `scriptreplay --summary` 随后会提供所有信息。

如果给出参数 `file` 或选项 `--log-out` `file`，`script` 会将对话保存到该 `file`。如果未给出文件名，对话将保存到文件 `typescript`。

注意，使用 `--log-in` 或 `--log-io` 记录输入可能会记录安全敏感信息，因为日志文件包含所有终端会话输入（例如密码），且与终端回显标志设置无关。

## 选项

下面，`size` 参数后面可以跟乘法后缀 `KiB`（=1024）、`MiB`（=1024*1024），以及 `GiB`、`TiB`、`PiB`、`EiB`、`ZiB` 和 `YiB`（`iB` 是可选的，例如 `K` 与 `KiB` 含义相同），或者后缀 `KB`（=1000）、`MB`（=1000*1000），以及 `GB`、`TB`、`PB`、`EB`、`ZB` 和 `YB`。

- `-a`, `--append`  
  将输出追加到 `file` 或 `typescript`，保留先前内容。

- `-c`, `--command` `command`  
  运行 `command`，而不是交互式 shell。这使脚本可以轻松捕获那些在 stdout 不是 tty 时行为不同的程序的输出。除了使用 `-c` 选项，也可以在双短横线（`--`）之后指定 `command`。

- `-E`, `--echo` `when`  
  此选项控制会话伪终端从端的 `ECHO` 标志。支持的模式为 `always`、`never` 或 `auto`。  
  
  默认值为 `auto`——在这种情况下，伪终端从端启用 `ECHO`；如果当前标准输入是终端，则对其禁用 `ECHO` 以防止双重回显；如果当前标准输入不是终端（例如管道：`echo date | script`），则保持伪终端从端启用 `ECHO`，使标准输入数据在记录到会话日志的同时也显示在屏幕上。  
  
  注意，`never` 模式会影响会话输出日志的内容，因为用户输入不会在输出中重复。

- `-e`, `--return`  
  返回子进程的退出状态。使用与 bash 因信号终止时相同的格式（即退出状态为 128 + 信号编号）。子进程的退出状态也始终存储在 typescript 文件中。

- `-f`, `--flush`  
  每次写入后刷新输出。这非常适合远程协作：一个人执行 `mkfifo foo; script -f foo`，另一个人可以使用 `cat foo` 实时监督正在进行的操作。注意，刷新会影响性能；可以按需使用 `SIGUSR1` 刷新日志。

- `--force`  
  允许默认输出文件 `typescript` 是硬链接或符号链接。命令将跟随符号链接。

- `-B`, `--log-io` `file`  
  将输入和输出记录到同一个 `file`。注意，仅当同时指定 `--log-timing` 时此选项才有意义，否则无法从日志 `file` 中分离输出流和输入流。

- `-I`, `--log-in` `file`  
  将输入记录到 `file`。如果仅指定 `--log-in`，则禁用输出日志记录。  
  
  请谨慎使用此日志功能，因为它会记录所有输入，包括终端已禁用回显标志时的输入（例如密码输入）。

- `-O`, `--log-out` `file`  
  将输出记录到 `file`。如果未给出 `--log-out` 或 `--log-in` 选项，默认将输出记录到名为 `typescript` 的文件。如果仅指定 `--log-in`，则禁用输出日志记录。

- `-T`, `--log-timing` `file`  
  将计时信息记录到 `file`。目前支持两种计时文件格式。当仅启用一个流（输入或输出）日志记录时，使用经典格式。在 `--log-io` 或同时使用 `--log-in` 和 `--log-out` 时，使用多流格式。另请参见 `--logging-format`。

- `-m`, `--logging-format` `format`  
  强制使用 `advanced` 或 `classic` 计时日志格式。默认情况下，仅记录输出时使用经典格式；当同时请求输入和输出日志记录时使用高级格式。  
  
  **经典格式**  
  计时日志包含两个字段，由空格分隔。第一个字段表示自上一次输出以来经过了多少时间。第二个字段表示本次输出了多少个字符。  
  
  **高级（多流）格式**  
  第一个字段是条目类型标识符（`I` 表示输入，`O` 表示输出，`H` 表示头部，`S` 表示信号）。第二个字段是自上一项以来经过了多少时间，条目其余部分是类型特定数据。

- `-o`, `--output-limit` `size`  
  将 typescript 和计时文件的大小限制为 `size`，并在超过此大小后停止子进程。计算的文件大小不包括 `script` 命令在子进程输出前后添加的开始和完成消息。由于缓冲，生成的输出文件可能大于指定值。

- `-q`, `--quiet`  
  安静模式（不向标准输出写入开始和完成消息）。

- `-t[file]`, `--timing[=file]`  
  将计时数据输出到标准错误，或在给出时输出到 `file`。此选项已弃用，推荐使用 `--log-timing`，其中 `file` 参数不是可选的。

- `-h`, `--help`  
  显示帮助文本并退出。

- `-V`, `--version`  
  显示版本并退出。

## 信号

收到 `SIGUSR1` 后，`script` 会立即刷新输出文件。

## 环境

- `SCRIPT_DEBUG=all`  
  启用 script 调试输出。

- `SHELL`  
  覆盖默认 shell。如果未设置 `SHELL`，则使用用户 [passwd(5)] 条目中的 shell。如果那里也未定义 shell，则使用 `/bin/sh` 作为回退。

- `ULPTY_DEBUG=all`  
  启用 pty 调试输出。

## 注意事项

当 fork 的 shell 退出时，`script` 结束（Bourne shell [sh(1p)] 使用 `control-D`，而 C-shell `csh(1)` 使用 `exit`、`logout` 或 `control-d`（如果未设置 `ignoreeof`））。

某些交互式命令（如 `vi(1)`）会在 typescript 文件中产生乱码。`script` 最适合不操作屏幕的命令，其结果旨在模拟硬拷贝终端。

不建议在非交互式 shell 中运行 `script`。`script` 的内部 shell 始终是交互式的，这可能导致意外结果。如果在 shell 初始化文件中使用 `script`，必须避免进入无限循环。例如，可以使用 `.profile` 文件，它仅由登录 shell 读取：

```sh
if test -t 0 ; then
    script
    exit
fi
```

还应避免在命令管道中使用 `script`，因为 `script` 可能读取比预期更多的输入。

## 历史

`script` 命令出现在 `3.0BSD` 中。

## 缺陷

`script` 会将*所有内容*放入日志文件，包括换行符和退格符。这不是普通用户所期望的。

`script` 主要设计用于交互式终端会话。当 `stdin` 不是终端（例如 `echo foo | script`）时，会话可能挂起，因为 script 会话内的交互式 shell 错过了 `EOF`，而 `script` 不知道何时关闭会话。更多信息参见“注意事项”部分。

## 另请参阅

[csh(1)]（用于 history 机制）、[scriptreplay(1)]、[scriptlive(1)]

## 报告缺陷

如需报告缺陷，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`script` 命令是 util-linux 软件包的一部分，可从 Linux 内核归档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 *util-linux*（Linux 实用工具的随机集合）项目的一部分。项目信息可在 <https://www.kernel.org/pub/linux/utils/util-linux/> 找到。若对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页取自该项目上游 Git 仓库 <git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-08-03。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`util-linux 2.43.devel-739-eee2e` · 2026-05-24 · `SCRIPT(1)`