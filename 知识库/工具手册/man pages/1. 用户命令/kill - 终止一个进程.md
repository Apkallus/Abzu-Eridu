https://www.man7.org/linux/man-pages/man1/kill.1.html

# `kill` - 终止一个进程

## 概要

```sh
kill  [-signal|-s signal|-p]  [-q value] [-a] [--timeout
milliseconds signal] [--] PID[:_inode_]...

kill  [-signal|-s signal] PID[:_inode_]...

kill -l [number|0xsigmask] | -L

kill -d PID[:_inode_]
```

## 描述

`kill` 命令向指定的进程或进程组发送指定的信号。

如果未指定信号，则发送 `TERM` 信号。该信号的默认动作是终止进程。应优先使用此信号而不是 `KILL` 信号（编号 9），因为进程可以为 `TERM` 信号安装处理程序，以便在有序终止之前执行清理步骤。如果在发送 `TERM` 信号后进程仍未终止，则可以使用 `KILL` 信号；请注意，后一种信号无法被捕获，因此不会给目标进程在终止前执行任何清理的机会。

大多数现代 shell 都有内置的 `kill` 命令，其用法与此处描述的命令相当相似。`--all`、`--pid` 和 `--queue` 选项，以及通过命令名指定进程的可能性，是本地扩展。

如果 `signal` 为 0，则不会实际发送信号，但仍会执行错误检查。

## 参数

要发送信号的进程列表可以是名称和 PID 的混合。

- `PID`  
    每个 `PID` 可以用以下方式之一表示：

    - `n`  
        其中 `n` 大于 0。向 PID 为 `n` 的进程发送信号。

    - `0`  
        向调用进程组中的所有进程发送信号。

    - `-1`  
        向 PID 大于 1 的所有进程发送信号。

    - `-n`  
        其中 `n` 大于 1。向进程组 `n` 中的所有进程发送信号。当给出形式为 `-n` 的参数且意图表示进程组时，必须先指定信号，或者该参数前必须带有 `--` 选项，否则它将被视为要发送的信号。

- `PID:_inode_`  
    进程可以用 `PID:inode` 格式引用，其中 `inode` 在 `pidfs` 中唯一标识进程身份。此特性支持无竞争地发送进程信号，并且需要内核版本 6.9 或更高。请注意，这仅适用于 `--signal` 选项和 `-signal` 表示法。最后，要获取进程的 inode 编号，可以使用 `getino(1)` 工具。

- `name`  
    所有使用此名称调用的进程都将收到信号。

## 选项

- `-s, --signal signal`  
    要发送的信号。可以给出名称或编号。

- `-l, --list [number|0xsigmask]`  
    打印信号名称列表，将给定的信号编号转换为名称，或将给定的信号掩码转换为名称。信号可以在 `/usr/include/linux/signal.h` 中找到。

    ```console
    $ ps s $$
      UID     PID          PENDING          BLOCKED          IGNORED           CAUGHT STAT TTY        TIME COMMAND
     1000 1608069 0000000000000000 0000000000000002 0000000000384000 0000000008013003 Ss   pts/44     0:02 zsh
    $ kill -l 0x0000000000384000
    TERM
    TSTP
    TTIN
    TTOU
    ```

    如果既未给出 `NUMBER` 也未给出 `0xSIGMASK`，则列出所有信号名称。在这种情况下，当输出不是终端时，每行打印一个信号。

- `-L, --table`  
    类似于 `-l`，但会打印信号名称及其对应编号。当输出不是终端时，每行打印一个信号。

- `-a, --all`  
    不将命令名到 PID 的转换限制为与当前进程具有相同 UID 的进程。

- `-p, --pid`  
    仅打印指定进程的进程 ID（PID），不发送任何信号。

- `-r, --require-handler`  
    如果被发送信号的进程未在用户空间捕获该信号，则不发送该信号。

- `--verbose`  
    打印将通过 `kill` 发送信号的 PID 以及信号。

- `-q, --queue value`  
    使用 `sigqueue(3)` 而不是 `kill(2)` 发送信号。`value` 参数是一个整数，随信号一起发送。如果接收进程使用 `sigaction(2)` 的 `SA_SIGINFO` 标志为此信号安装了处理程序，则它可以通过 `siginfo_t` 结构的 `si_sigval` 字段获取此数据。

- `--timeout milliseconds signal`  
    以通常方式向进程发送一个信号，并在指定延迟后发送一个附加信号。`--timeout` 选项使 `kill` 等待 `milliseconds` 中定义的时间段，然后再向进程发送后续 `signal`。此特性使用 Linux 内核 PID 文件描述符特性实现，以保证后续信号发送到同一进程，或者如果进程已不存在则不发送。

    请注意，操作系统可能会重用 PID，在 shell 中使用 `kill` 和 `sleep` 实现等效特性会受到竞争条件影响，后续信号可能会发送到使用了回收 PID 的不同进程。

    `--timeout` 选项可以多次指定：信号将按顺序发送，并使用指定的超时。`--timeout` 选项可以与 `--queue` 选项组合使用。

    例如，以下命令依次发送信号 `QUIT`、`TERM` 和 `KILL`，并在发送信号之间等待 1000 毫秒：

    ```sh
    kill --verbose --timeout 1000 TERM --timeout 1000 KILL \
            --signal QUIT 12345
    ```

- `-d, --show-process-state pid`  
    解码 `/proc/pid/status` 中与信号相关的字段。

    ```console
    $ kill -d $$
    Blocked: INT
    Ignored: TERM TSTP TTIN TTOU
    Caught: HUP INT PIPE ALRM CHLD WINCH
    ```

- `-h, --help`  
    显示帮助文本并退出。

- `-V, --version`  
    显示版本并退出。

## 退出状态

`kill` 具有以下退出状态值：

- `0`  
    成功

- `1`  
    失败

- `64`  
    部分成功（当指定了多个进程时）

## 说明

尽管可以将多线程进程中某个线程的 TID（线程 ID，参见 `gettid(2)`）指定为 `kill` 的参数，但信号仍然指向进程（即整个线程组）。换句话说，无法向多线程进程中显式选择的线程发送信号。信号将被递送到目标进程中任意选择的未阻塞该信号的线程。更多细节请参见 `signal(7)` 以及 `clone(2)` 中 `CLONE_THREAD` 的描述。

各种 shell 都提供了内置的 `kill` 命令，相对于本手册描述的 `kill(1)` 可执行文件，通常优先使用内置命令。确保执行的是本页描述的命令的最简单方法是在调用命令时使用完整路径，例如：`/bin/kill --version`

## 作者

Salvatore Valente <svalente@mit.edu>，Karel Zak <kzak@redhat.com>

原始版本取自 BSD 4.4。

## 另请参阅

`bash(1)`、`tcsh(1)`、`getino(1)`、`sigaction(2)`、`kill(2)`、`sigqueue(3)`、`signal(7)`、`proc(5)`、`proc_pid_status(5)`

## 报告错误

有关错误报告，请使用问题跟踪器
<https://github.com/util-linux/util-linux/issues>。

## 可用性

`kill` 命令是 util-linux 包的一部分，可以从 Linux Kernel Archive
<https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页面是 *util-linux*（一个 Linux 实用程序的随机集合）项目的一部分。有关该项目的信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果你对本手册页有错误报告，请发送至 util-linux@vger.kernel.org。本页面取自项目的上游 Git 仓库
⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面存在任何渲染问题，或者你认为有更好或更新的页面来源，或者你对本版本说明中的信息（该信息*不*属于原始手册页的一部分）有更正或改进，请发送邮件至 man-pages@man7.org

```
util-linux 2.43.devel-739-eee2e 2026-05-24                        KILL(1)
```