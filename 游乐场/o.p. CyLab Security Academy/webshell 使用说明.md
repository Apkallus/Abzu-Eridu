# 欢迎使用 CyLab Security Academy WebShell！

使用方向键或空格键滚动，输入 `q` 退出。

这是一个可通过浏览器访问的 Linux shell，可用于解决 CyLab Security Academy 的挑战。

请注意，WebShell 并非解决挑战的必需品。所有文件和程序要么可供下载，要么可通过远程端口访问。WebShell 主要面向无法使用自己本地 shell 环境的用户，例如使用学校提供硬件的学生。

WebShell 提供了许多用于解决 CTF 挑战的常用工具。受 WebShell 限制，通常无法安装额外软件。不过，如果你认为某个特定工具会有所帮助，可以在 Discord 上留言，或发送邮件至 support@cylabacademy.org，我们会考虑添加。

WebShell 设有多种限制以防止滥用。部分资源限制可通过输入 `usage` 查看。请注意，所有 WebShell 会话均会被记录和监控，因此请勿输入任何敏感信息。滥用 WebShell 基础设施可能导致账号终止和取消资格。

## 面向初学者的通用 shell 提示

- 当前目录会显示在 shell 提示符中。
- `~` 表示你的家目录，适合存放正在处理的文件。你可以随时输入 `cd ~` 返回这里。存放在家目录之外的文件不会在 WebShell 会话之间保留。
- 有些文件太大，无法存放在家目录中！如果解决挑战需要用到它们，可以尝试存放到 `/tmp`，但请注意，这些文件不会在 WebShell 会话之间保留。
- 输入 `ls` 列出当前目录中的文件。
- 输入 `cd <path>` 切换到该路径。路径相对于当前目录，若以 `/` 开头则为绝对路径。输入 `cd ..` 返回上一级目录。
- 输入 `cat <file>` 打印文本文件的内容。
- 输入 `./<file>` 运行当前目录中的可执行文件。你可能需要先输入 `chmod +x <file>` 授予自己执行权限。
- 输入 `<Control-C>` 终止正在运行的进程。
- 输入 `man <command>` 了解任意命令的更多信息。按 `q` 可退出手册页。
- 如果终端提示符开始出现异常，输入 `reset` 清屏。
- 输入 `exit` 或关闭标签页即可结束 WebShell 会话。

## 解题提示

- 部分挑战需要下载文件。你可以不点击链接，而是使用 `wget` 将文件下载到 WebShell 中，例如 `wget <file-URL>`。右键点击链接可复制文件 URL。
- 部分挑战需要连接远程端口，通常使用 netcat 完成，例如 `nc <server-name> <port>`。不过，某些挑战可能需要使用 netcat 之外的程序。
- 虽然大多数挑战都可以使用 WebShell 解决，但有些挑战在没有额外资源的情况下可能难以完成或无法完成。例如，某些挑战 intended to be solved using GUI programs。
- 可以使用 `sz <filename>` / `rz` 在 WebShell 与浏览器之间导出/导入文件。

## 附加说明

- 你可以从多个标签页/设备连接 WebShell，它们会共享同一会话。但请注意，关闭其中**任意一个**标签页都会结束你在所有标签页上的 WebShell 会话。
- 如果看到“Killed”消息，说明某个长时间运行的进程已被终止，以确保所有玩家公平分配资源。解决 CyLab Security Academy 挑战并不需要进行大量暴力破解。
- 如果遇到其他意外错误，可能是触发了 WebShell 的某项资源限制。请查看 `usage` 命令，必要时使用 `exit` 结束当前会话。
- 如果你通过 CyLab Security Academy 网站更改了用户名，下次登录 WebShell 时会创建一个新的家目录。不过，你之前用户名下的文件仍可通过 `/home/<old-username>` 访问。