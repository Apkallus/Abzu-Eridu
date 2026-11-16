https://man7.org/linux/man-pages/man1/watch.1.html

# `watch` - 定期执行程序，全屏显示输出

## 概要

```sh
watch [option ...] command
```

## 描述

`watch` 重复运行 `command`，显示其输出和错误（第一屏内容）。这允许你观察程序输出随时间的变化。默认情况下，`command` 每 2 秒运行一次，`watch` 将一直运行直到被中断。标题栏会显示 `command` 的启动时间、运行时间以及退出码。

## 选项

- `-b`, `--beep`  
    如果 `command` 以非零退出，则发出蜂鸣声。

- `-c`, `--color`  
    解释 ANSI 颜色和样式序列。

- `-C`, `--no-color`  
    不解释 ANSI 颜色和样式序列。

- `-d`, `--differences[=permanent]`  
    高亮显示连续更新之间的差异。如果指定了可选的 `permanent` 参数，则 `watch` 将显示自第一次迭代以来的所有更改。`permanent` 参数需要与选项连接，如 `-d1` 或 `--differences=1`。

- `-e`, `--errexit`  
    在 `command` 出错时冻结更新，并在按键后退出。`watch` 的退出码将是 `command` 退出时的代码。如果信号 `n` 是 `command` 终止的原因，则退出码为 128 + `n`。

- `-f`, `--follow`  
    不在每次更新时清屏，而是像 `tail -f` 那样滚动输出。此选项与任何跟踪屏幕输出的选项不兼容，例如 `--differences`、`--chgexit` 和 `--eqexit` 选项。

- `-g`, `--chgexit`  
    当 `command` 的可见输出发生变化时退出。由于屏幕尺寸小或输出量大而位于屏幕外的更改不会导致 `watch` 退出。

- `-n`, `--interval` `seconds`  
    指定更新间隔。小于 0.1 和大于 2678400（31 天）的值将被转换为这些相应的边界。在任何区域设置下，`.` 和 `,` 都可以使用。`WATCH_INTERVAL` 环境变量可用于持久设置非默认间隔（遵循相同的规则和格式）。

- `-p`, `--precise`  
    在上次运行开始后的 `--interval` 秒执行 `command`，而不是在上次运行结束后的 `--interval` 秒执行。如果 `command` 完成时间超过 `--interval` 秒，则在两种情况下都会等待其完成。

- `-q`, `--equexit` `<cycles>`  
    当 `command` 的输出在给定周期数内没有变化时退出。

- `-r`, `--no-rerun`  
    不要在终端调整大小时运行程序，程序输出将在下一个常规运行时间重新出现。

- `-s`, `--shotsdir`  
    保存截图的目录。

- `-t`, `--no-title`  
    关闭通常显示在屏幕顶部的标题栏。

- `-w`, `--no-wrap`  
    关闭行换行。长行将被截断而不是换行到下一行。

- `-x`, `--exec`  
    将 `command` 传递给 `exec(3)` 调用而不是 `sh -c`。程序将启动得更快。Shell 功能（环境设置、变量和路径名展开等）将不可用。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-v`, `--version`  
    显示版本信息并退出。

## 按键控制

- `spacebar`  
    立即执行 `command`。如果它当前正在运行，则不会中断，其下一轮将立即开始。

- `q`  
    退出 `watch`。它目前不会中断正在运行的 `command`（与终止信号相反，例如 Ctrl+C 后的 SIGKILL）。

- `s`  
    截取屏幕截图。截图将保存在工作目录中，除非通过 `--shotsdir` 另行指定。如果 `command` 当前正在运行，则截图将在其完成后立即截取。

## 退出状态

- `0`  
    成功。不表示 `command` 的退出码。

- `1`  
    与 `command` 操作无关的错误。

- `2`  
    与 `command` 执行和管理相关的错误（不是其退出码）。

- `any non-zero (--errexit)`  
    使用 `--errexit` 时，返回 `command` 的最后一个退出码。

## 环境

`watch` 的行为受以下环境变量影响。

- `WATCH_INTERVAL`  
    更新间隔，遵循与 `--interval` 命令行选项相同的规则。

- `COLUMNS`  
    终端屏幕字符宽度。设置以覆盖自动检测。

- `LINES`  
    终端屏幕字符高度。设置以覆盖自动检测。

## 注意事项

使用 POSIX 选项处理（即选项处理在第一个非选项参数处停止）。这意味着 `command` 之后的标志不会由 `watch` 本身解释。

非打印字符会从程序输出中剥离。如果你想看到它们，请在命令管道中使用 `cat -v`。

## 示例

要观察目录内容的变化，你可以使用

```sh
watch -d ls -l
```

如果你有动态频率的 CPU 并希望观察其变化，请尝试以下命令。命令被传递给 shell，这允许你构建管道。引号也是 shell 的功能。

```sh
watch -n1 'grep "^cpu MHz" /proc/cpuinfo | sort -nrk4'
```

要监控服务器的 up 状态，将每次运行的输出副本保存到文件，你可以使用以下命令。`-p` 使命令每 10 秒执行一次，无论上次运行完成花了多长时间。

```sh
watch -n10 -p -d '{ date; for i in 10.0.0.31 10.0.0.32
10.0.0.33; do R=OK; ping -c2 -W2 "$i" &>/dev/null ||
R=FAIL; echo "$i: $R"; done } | tee -a ~/log'
```

你可以用以下命令观察管理员安装最新内核

```sh
watch uname -r
```

## 缺陷

当终端尺寸变化时，其内容变化不会在下一个 `command` 运行时被记录。`--chgexit` 不会触发该轮次，`--equexit` 的计数器也不会重新开始，即使 `command` 输出在此期间发生变化。`--differences` 高亮显示会被重置。

## 报告缺陷

请将缺陷报告发送至 ⟨procps@freelists.org⟩。

## 版本说明

本页是 `procps-ng`（/proc 文件系统实用程序）项目的一部分。项目信息可在 ⟨https://gitlab.com/procps-ng/procps⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨https://gitlab.com/procps-ng/procps/blob/master/Documentation/bugs.md⟩。本页获取自项目上游 Git 仓库 ⟨https://gitlab.com/procps-ng/procps.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-07-30。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
procps-ng                       2025-04-16                       WATCH(1)
```