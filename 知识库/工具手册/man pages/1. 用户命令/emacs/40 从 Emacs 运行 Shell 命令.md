https://www.gnu.org/software/emacs/manual/html_node/emacs/Shell.html

# 40 从 Emacs 运行 Shell 命令

Emacs 提供了将单条命令行传递给 shell 子进程的命令，也提供了以 Emacs 缓冲区作为输入输出来交互运行 shell 的命令，以及在终端模拟器窗口中运行 shell 的命令。

- 
    ```
    M-! cmd RET
    ```
    运行 shell 命令 `cmd` 并显示输出（`shell-command`）。

- 
    ```
    M-| cmd RET
    ```
    以区域内容作为输入运行 shell 命令 `cmd`；可选择用输出替换该区域（`shell-command-on-region`）。

- 
    ```
    M-& cmd RET
    ```
    异步运行 shell 命令 `cmd`，并显示输出（`async-shell-command`）。

- 
    ```
    M-x shell
    ```
    通过 Emacs 缓冲区进行输入和输出，运行子 shell。然后可以交互式输入命令。

- 
    ```
    M-x term
    ```
    通过 Emacs 缓冲区进行输入和输出，运行子 shell。然后可以交互式输入命令。提供完整的终端模拟。

无论何时为可执行程序指定相对文件名（无论是在上述命令之一的 `cmd` 参数中，还是在其他上下文中），Emacs 都会在变量 `exec-path` 指定的目录中搜索该程序。此变量的值必须是目录列表；默认值取决于 Emacs 启动时的环境变量 `PATH`（参见“通用变量”）。

`M-x eshell` 会调用一个完全用 Emacs 实现的 shell。它有自己的手册文档。参见《Eshell: The Emacs Shell》中的 [Eshell](https://www.gnu.org/software/emacs/manual/html_node/eshell/index.html#Top)。

- “单条 Shell 命令”
- “交互式子 shell”
- “Shell 模式”
- “Shell 提示符”
- “Shell 命令历史”
- “目录跟踪”
- “Shell 书签”
- “Shell 模式选项”
- “Emacs 终端模拟器”
- “Term 模式”
- “远程主机 Shell”
- “串口终端”