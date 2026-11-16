https://man7.org/linux/man-pages/man8/sudo.8.html

# `sudo`、`sudoedit` — 以另一个用户身份执行命令

## 概要

```sh
sudo -h | -K | -k | -V
sudo -v [-ABkNnS] [-g group] [-h host] [-p prompt] [-u user]
sudo -l [-ABkNnS] [-g group] [-h host] [-p prompt] [-U user] [-u user]
    [command [arg ...]]
sudo [-ABbEHnPS] [-C num] [-D directory] [-g group] [-h host] [-p prompt]
    [-R directory] [-T timeout] [-u user] [VAR=value] [-i | -s]
    [command [arg ...]]
sudoedit [-ABkNnS] [-C num] [-D directory] [-g group] [-h host] [-p prompt]
    [-R directory] [-T timeout] [-u user] file ...
```

## 描述

`sudo` 允许被许可的用户以超级用户或安全策略指定的其他用户身份执行 `command`。调用用户的实际（*而非*有效）用户 ID 用于确定查询安全策略时使用的用户名。

`sudo` 支持用于安全策略、审计和输入/输出日志记录的插件架构。第三方可以开发和分发自己的插件，与 `sudo` 前端无缝协作。默认安全策略是 `sudoers`，通过文件 `/etc/sudoers` 或 LDAP 进行配置。更多信息参见“插件”一节。

安全策略决定用户运行 `sudo` 所拥有的权限（如果有）。策略可能要求用户使用密码或其他身份验证机制进行身份验证。如果需要身份验证，且用户未在可配置的时间限制内输入密码，`sudo` 将退出。此限制因策略而异；`sudoers` 安全策略的默认密码提示超时为 5 分钟。

安全策略可能支持凭据缓存，允许用户在一段时间内再次运行 `sudo` 而无需身份验证。默认情况下，`sudoers` 策略以每个终端为基础缓存凭据 5 分钟。更多信息参见 `sudoers(5)` 中的 `timestamp_type` 和 `timestamp_timeout` 选项。通过使用 `-v` 选项运行 `sudo`，用户可以在不运行 `command` 的情况下更新缓存的凭据。

在 `sudo` 是获取超级用户权限的主要方法的系统上，必须避免安全策略配置文件中的语法错误。对于默认安全策略 `sudoers(5)`，应使用 `visudo(8)` 实用程序对配置文件进行更改，以确保不会引入语法错误。

当以 `sudoedit` 调用时，隐含 `-e` 选项（如下所述）。

安全策略和审计插件可以记录运行 `sudo` 的成功和失败尝试。如果配置了 I/O 插件，正在运行的 `command` 的输入和输出也可能被记录。

选项如下：

- `-A`, `--askpass`  
    通常，如果 `sudo` 需要密码，它会从用户终端读取。如果指定了 `-A`（`askpass`）选项，则执行一个（可能是图形化的）辅助程序来读取用户密码并将密码输出到标准输出。如果设置了 `SUDO_ASKPASS` 环境变量，则它指定辅助程序的路径。否则，如果 `sudo.conf(5)` 包含指定 askpass 程序的行，则使用该值。例如：

    ```text
    # askpass 辅助程序的路径
    Path askpass /usr/X11R6/bin/ssh-askpass
    ```

    如果没有可用的 askpass 程序，`sudo` 将以错误退出。

- `-B`, `--bell`  
    当存在终端时，在密码提示中响铃。如果使用 askpass 程序，此选项无效。

- `-b`, `--background`  
    在后台运行给定的 `command`。无法使用 shell 作业控制来操作由 `sudo` 启动的后台进程。大多数交互式 `command` 在后台模式下将无法正常工作。

- `-C num`, `--close-from=num`  
    在执行 `command` 之前关闭所有大于或等于 `num` 的文件描述符。不允许小于三的值。默认情况下，`sudo` 在执行 `command` 时会关闭除标准输入、标准输出和标准错误之外的所有打开文件描述符。安全策略可能限制用户使用此选项的能力。`sudoers` 策略仅在管理员启用了 `closefrom_override` 选项时才允许使用 `-C` 选项。

- `-D directory`, `--chdir=directory`  
    在指定的 `directory` 中而不是当前工作目录中运行 `command`。如果用户没有权限指定工作目录，安全策略可能返回错误。

- `-E`, `--preserve-env`  
    向安全策略指示用户希望保留其现有环境变量。如果用户没有权限保留环境，安全策略可能返回错误。

- `--preserve-env=list`  
    向安全策略指示用户希望将逗号分隔的环境变量列表添加到从用户环境保留的变量中。如果用户没有权限保留环境，安全策略可能返回错误。此选项可以多次指定。

- `-e`, `--edit`  
    编辑一个或多个 `file` 而不是运行 `command`。在咨询安全策略时，使用字符串 "sudoedit" 代替路径名。如果用户被策略授权，则采取以下步骤：

    1. 创建要编辑的文件的临时副本，所有者设置为调用用户。
    2. 运行策略指定的编辑器来编辑临时文件。`sudoers` 策略使用 `SUDO_EDITOR`、`VISUAL` 和 `EDITOR` 环境变量（按此顺序）。如果 `SUDO_EDITOR`、`VISUAL` 或 `EDITOR` 均未设置，则使用 `editor` `sudoers(5)` 选项中列出的第一个程序。
    3. 如果临时文件已被修改，则将临时文件复制回其原始位置并删除临时版本。

    为帮助防止编辑未经授权的文件，除非安全策略明确允许，否则强制执行以下限制：

    - 不得编辑符号链接（版本 1.8.15 及更高版本）。
    - 当父目录可被调用用户写入时，不跟随要编辑路径上的符号链接，除非该用户是 root（版本 1.8.16 及更高版本）。
    - 除非该用户是 root，否则不得编辑位于调用用户可写目录中的文件（版本 1.8.16 及更高版本）。

    绝不允许用户编辑设备特殊文件。

    如果指定的文件不存在，则会创建它。与 `sudo` 运行的大多数 `command` 不同，编辑器在调用用户的环境未修改的情况下运行。如果编辑后临时文件变为空，则会在安装前提示用户。如果由于某种原因 `sudo` 无法用其编辑版本更新文件，用户将收到警告，编辑副本将保留在临时文件中。

- `-g group`, `--group=group`  
    以主组设置为 `group` 而不是目标用户密码数据库条目指定的主组来运行 `command`。`group` 可以是组名或前缀为 `#` 字符的数字组 ID（GID）（例如，`#0` 表示 GID 0）。以 GID 运行 `command` 时，许多 shell 要求用反斜杠（`\`）转义 `#`。如果未指定 `-u` 选项，`command` 将以调用用户身份运行。无论哪种情况，主组都将设置为 `group`。只要不使用 `-P` 选项，`sudoers` 策略允许通过 `-g` 选项指定目标用户的任何组。

- `-H`, `--set-home`  
    请求安全策略将 `HOME` 环境变量设置为目标用户密码数据库条目指定的主目录。取决于策略，这可能是默认行为。

- `-h`, `--help`  
    向标准输出显示简短帮助消息并退出。

- `-h host`, `--host=host`  
    如果安全策略插件支持远程 `command`，则在指定的 `host` 上运行 `command`。`sudoers` 插件目前不支持运行远程 `command`。这也可以与 `-l` 选项结合使用，以列出用户在远程主机上的权限。

- `-i`, `--login`  
    将目标用户密码数据库条目指定的 shell 作为登录 shell 运行。这意味着 shell 将读取登录特定的资源文件，如 `.profile`、`.bash_profile` 或 `.login`。如果指定了 `command`，则使用 `-c` 选项将其作为简单 `command` 传递给 shell。`command` 和任何 `arg` 在将每个字符（包括空白）用反斜杠（`\`）转义后（字母数字、下划线、连字符和美元符号除外）用空格连接。如果未指定 `command`，则执行交互式 shell。`sudo` 尝试在运行 shell 之前切换到该用户的主目录。`command` 在类似于用户在登录时收到的环境中运行。大多数 shell 在指定 `command` 时与交互式会话相比行为不同；详情请查阅 shell 手册。`sudoers(5)` 手册中的*命令环境*一节记录了在使用 `sudoers` 策略时 `-i` 选项如何影响运行 `command` 的环境。

- `-K`, `--remove-timestamp`  
    类似于 `-k` 选项，但它移除用户的所有缓存凭据，无论终端或父进程 ID 如何。下次运行 `sudo` 时，如果安全策略要求身份验证，则必须输入密码。不能将 `-K` 选项与 `command` 或其他选项一起使用。此选项不需要密码。并非所有安全策略都支持凭据缓存。

- `-k`, `--reset-timestamp`  
    在没有 `command` 使用时，使当前会话的用户缓存凭据失效。下次在会话中运行 `sudo` 时，如果安全策略要求身份验证，则必须输入密码。默认情况下，`sudoers` 策略在凭据缓存中为每个终端（如果没有终端，则为父进程 ID）使用单独记录。这防止 `-k` 选项干扰在不同终端会话中运行的 `sudo` 命令。更多信息参见 `sudoers(5)` 中的 `timestamp_type` 选项。此选项不需要密码，添加它是为了允许用户从 `.logout` 文件撤销 `sudo` 权限。

    当与可能需要密码的 `command` 或选项一起使用时，此选项将导致 `sudo` 忽略用户的缓存凭据。因此，`sudo` 将提示输入密码（如果安全策略要求），并且不会更新用户的缓存凭据。

    并非所有安全策略都支持凭据缓存。

- `-l`, `--list`  
    如果未指定 `command`，则列出调用用户（或 `-U` 选项指定的 `user`）在当前主机上的权限。如果多次指定此选项且安全策略支持详细输出格式，则使用更长的列表格式。

    如果指定了 `command` 并且安全策略允许调用用户（或 `-U` 选项指定的 `user`）在当前主机上运行，则显示 `command` 的完全限定路径以及任何 `arg`。如果多次指定 `-l`（且安全策略支持），则匹配规则以详细格式与 `command` 一起显示。如果指定了 `command` 但策略不允许，`sudo` 将以状态值 1 退出。

- `-N`, `--no-update`  
    即使用户成功通过身份验证，也不更新用户的缓存凭据。与 `-k` 标志不同，如果现有缓存凭据有效，则使用它们。要检测用户的缓存凭据何时有效（或何时不需要身份验证），可以使用以下命令：

    ```sh
    sudo -Nnv
    ```

    并非所有安全策略都支持凭据缓存。

- `-n`, `--non-interactive`  
    避免以任何形式提示用户输入。如果运行 `command` 需要密码，`sudo` 将显示错误消息并退出。

- `-P`, `--preserve-groups`  
    原样保留调用用户的组向量。默认情况下，`sudoers` 策略将组向量初始化为目标用户所属的组列表。但是，实际和有效组 ID 仍设置为与目标用户匹配。

- `-p prompt`, `--prompt=prompt`  
    使用带可选转义序列的自定义密码提示。`sudoers` 策略支持以下百分号（`%`）转义序列：

    - `%H` 展开为主机名（包括域名）（仅当机器的主机名是完全限定名称或在 `sudoers(5)` 中设置了 `fqdn` 选项时）
    - `%h` 展开为不带域名的本地主机名
    - `%p` 展开为正在请求其密码的用户名称（遵循 `sudoers(5)` 中的 `rootpw`、`targetpw` 和 `runaspw` 标志）
    - `%U` 展开为将运行 `command` 的用户的登录名（默认为 root，除非还指定了 `-u` 选项）
    - `%u` 展开为调用用户的登录名
    - `%%` 两个连续的 `%` 字符合并为单个 `%` 字符

    自定义提示将覆盖安全策略或 `SUDO_PROMPT` 环境变量指定的默认提示。在使用 PAM 的系统上，自定义提示还将覆盖 PAM 模块指定的提示，除非在 `sudoers` 中禁用了 `passprompt_override` 标志。

- `-R directory`, `--chroot=directory`  
    在运行 `command` 之前切换到指定的根 `directory`（参见 `chroot(8)`）。如果用户没有权限指定根目录，安全策略可能返回错误。

    此选项已弃用，将在未来版本的 `sudo` 中移除。

- `-S`, `--stdin`  
    将提示写入标准错误并从标准输入读取密码，而不是使用终端设备。

- `-s`, `--shell`  
    如果设置了 `SHELL` 环境变量，则运行它指定的 shell；否则运行调用用户密码数据库条目指定的 shell。如果指定了 `command`，则使用 `-c` 选项将其作为简单命令传递给 shell。`command` 和任何 `arg` 在将每个字符（包括空白）用反斜杠（`\`）转义后（字母数字、下划线、连字符和美元符号除外）用空格连接。如果未指定 `command`，则执行交互式 shell。大多数 shell 在指定 `command` 时与交互式会话相比行为不同；详情请查阅 shell 手册。

- `-U user`, `--other-user=user`  
    与 `-l` 选项一起使用，以列出 `user` 的权限而不是调用用户的权限。安全策略可能限制列出其他用户的权限。使用 `sudoers` 策略时，`-U` 选项仅限于 root 用户以及具有指定 `user` 的 "list" 特权或能够在当前主机上以 root 或 `user` 身份运行任何 `command` 的用户。

- `-T timeout`, `--command-timeout=timeout`  
    用于设置 `command` 的超时时间。如果超时在 `command` 退出之前到期，`command` 将被终止。安全策略可能限制用户设置超时的能力。`sudoers` 策略要求显式启用用户指定的超时。

- `-u user`, `--user=user`  
    以默认目标用户（通常为 `root`）以外的用户身份运行 `command`。`user` 可以是用户名或前缀为 `#` 字符的数字用户 ID（UID）（例如，`#0` 表示 UID 0）。以 UID 运行 `command` 时，许多 shell 要求用反斜杠（`\`）转义 `#`。某些安全策略可能将 UID 限制为密码数据库中列出的那些。只要未设置 `targetpw` 选项，`sudoers` 策略允许不在密码数据库中的 UID。其他安全策略可能不支持此功能。

- `-V`, `--version`  
    打印 `sudo` 版本字符串以及任何已配置插件的版本字符串。如果调用用户已经是 root，`-V` 选项将显示构建 `sudo` 时传递给 configure 的选项；插件可能显示额外信息，如默认选项。

- `-v`, `--validate`  
    更新用户的缓存凭据，必要时对用户进行身份验证。对于 `sudoers` 插件，这默认将 `sudo` 超时再延长 5 分钟，但不运行 `command`。并非所有安全策略都支持缓存凭据。

- `--`  
    `--` 用于分隔 `sudo` 选项的结束。后续选项传递给 `command`。

取值的选项只能指定一次，除非描述中另有说明。这有助于防止编写不良的脚本使用用户控制的输入调用 `sudo` 所导致的问题。

要为 `command` 设置的环境变量也可以以 `VAR=value` 的形式作为选项传递给 `sudo`，例如 `LD_LIBRARY_PATH=/usr/local/pkg/lib`。环境变量可能受到安全策略插件施加的限制。`sudoers` 策略对作为选项传递的环境变量施加与现有环境变量相同的限制，但有一个重要区别。如果在 `sudoers` 中设置了 `setenv` 选项，要运行的 `command` 设置了 `SETENV` 标签，或者匹配的 `command` 是 `ALL`，则用户可以设置原本会被禁止的变量。更多信息参见 `sudoers(5)`。

## 命令执行

当 `sudo` 执行 `command` 时，安全策略指定 `command` 的执行环境。通常，实际和有效用户及组 ID 设置为与目标用户匹配（如密码数据库中指定），并且组向量根据组数据库初始化（除非指定了 `-P` 选项）。

安全策略可以指定以下参数：

- 实际和有效用户 ID
- 实际和有效组 ID
- 补充组 ID
- 环境列表
- 当前工作目录
- 文件创建模式掩码（umask）
- 调度优先级（即 nice 值）

### 进程模型

`sudo` 可以通过两种不同的方式运行 `command`。

如果配置了 I/O 日志记录插件来记录终端 I/O，或者安全策略明确要求，则分配新的伪终端（"pty"），并使用 `fork(2)` 创建第二个 `sudo` 进程，称为*监视器*。监视器创建一个新的终端会话，以自身为领导者、pty 为其控制终端，再次调用 `fork(2)`，如上所述设置执行环境，然后使用 `execve(2)` 系统调用在子进程中运行 `command`。监视器的存在是为了在用户终端和运行 `command` 的 pty 之间中继作业控制信号。这使得可以正常挂起和恢复 `command`。没有监视器，`command` 将处于 POSIX 术语中的"孤儿进程组"中，并且不会从内核接收任何作业控制信号。当 `command` 退出或被信号终止时，监视器将 `command` 的退出状态传递给主 `sudo` 进程并退出。收到 `command` 的退出状态后，主 `sudo` 进程将 `command` 的退出状态传递给安全策略的关闭函数以及任何已配置审计插件的关闭函数，然后退出。在使用 `sudoers` 策略时，这是 sudo 1.9.14 及以上版本的默认模式。

如果不使用 pty，`sudo` 调用 `fork(2)`，如上所述设置执行环境，并使用 `execve(2)` 系统调用在子进程中运行 `command`。主 `sudo` 进程等待直到 `command` 完成，然后将 `command` 的退出状态传递给安全策略的关闭函数以及任何已配置审计插件的关闭函数，并退出。作为特殊情况，如果策略插件未定义关闭函数，`sudo` 将直接执行 `command` 而不是先调用 `fork(2)`。`sudoers` 策略插件仅在启用 I/O 日志记录、需要 pty、指定了 SELinux 角色、`command` 具有关联超时，或启用了 `pam_session` 或 `pam_setcred` 选项时才定义关闭函数。在使用 PAM 的系统上，`pam_session` 和 `pam_setcred` 默认都启用。在使用 `sudoers` 策略时，这是 sudo 1.9.14 之前版本的默认模式。

在使用 PAM 的系统上，安全策略的关闭函数负责关闭 PAM 会话。它还可能记录 `command` 的退出状态。

### 信号处理

当 `command` 作为 `sudo` 进程的子进程运行时，`sudo` 将其收到的信号中继给 `command`。SIGINT 和 SIGQUIT 信号仅在 `command` 在新 pty 中运行或信号由用户进程（而非内核）发送时才会中继。这防止 `command` 在用户每次输入 control-C 时收到两次 SIGINT。某些信号（如 SIGSTOP 和 SIGKILL）无法被捕获，因此不会中继给 `command`。作为一般规则，当你希望挂起由 `sudo` 运行的 `command` 时，应使用 SIGTSTP 而不是 SIGSTOP。

作为特殊情况，`sudo` 不会中继由其正在运行的 `command` 发送的信号。这防止 `command` 意外杀死自己。在某些系统上，`reboot(8)` 实用程序在重新启动系统之前向除自身以外的所有非系统进程发送 SIGTERM。这防止 `sudo` 将其收到的 SIGTERM 信号中继回 `reboot(8)`，后者可能因此在系统实际重新启动之前退出，使其处于类似于单用户模式的半死状态。但请注意，此检查仅适用于由 `sudo` 运行的 `command`，而不适用于 `command` 可能创建的任何其他进程。因此，通过 `sudo` 运行调用 `reboot(8)` 或 `shutdown(8)` 的脚本可能导致系统最终处于此未定义状态，除非使用 `exec()` 函数族而不是 `system()`（后者在 `command` 和调用进程之间插入一个 shell）来运行 `reboot(8)` 或 `shutdown(8)`。

### 插件

可以通过 `sudo.conf(5)` 文件中的 `Plugin` 指令指定插件。它们可以作为动态共享对象加载（在支持的系统上），或直接编译到 `sudo` 二进制文件中。如果不存在 `sudo.conf(5)` 文件，或者它不包含任何 `Plugin` 行，`sudo` 将使用 `sudoers(5)` 作为策略、审计和 I/O 日志记录插件。关于 `/etc/sudo.conf` 文件的详细信息，参见 `sudo.conf(5)` 手册；关于 `sudo` 插件架构的更多信息，参见 `sudo_plugin(5)` 手册。

## 退出值

成功执行 `command` 后，`sudo` 的退出状态将是所执行程序的退出状态。如果 `command` 因收到信号而终止，`sudo` 将向自身发送终止 `command` 的相同信号。

如果在没有 `command` 的情况下指定了 `-l` 选项，则如果用户被允许运行 `sudo` 且成功通过身份验证（按安全策略要求），`sudo` 将以值 0 退出。如果使用 `-l` 选项指定了 `command`，则仅当安全策略允许该 `command` 时退出值才为 0，否则为 1。

如果存在身份验证失败、配置/权限问题，或者无法执行给定的 `command`，`sudo` 将以值 1 退出。在后一种情况下，错误字符串将打印到标准错误。如果 `sudo` 无法 `stat(2)` 用户 PATH 中的一个或多个条目，则向标准错误打印错误。（如果目录不存在或实际上不是目录，则忽略该条目并且不打印错误。）这不应在正常情况下发生。`stat(2)` 返回"权限被拒绝"的最常见原因是，如果你正在运行自动挂载器，并且 PATH 中的某个目录位于当前无法访问的机器上。

## 安全注意事项

`sudo` 在执行外部 `command` 时尽量保证安全。

为防止命令欺骗，`sudo` 在用户 PATH 中搜索 `command` 时最后检查 "." 和 ""（两者都表示当前目录）（如果其中一个或两个在 PATH 中）。取决于安全策略，用户的 PATH 环境变量可能被修改、替换或原样传递给 `sudo` 执行的程序。

*绝不应*授予用户执行用户可写文件或位于用户可写目录中的文件的 `sudo` 权限。如果用户可以修改或替换 `command`，则无法限制他们可以运行的其他 `command`。

默认情况下，`sudo` 仅记录它显式运行的 `command`。如果用户运行诸如 `sudo su` 或 `sudo sh` 之类的 `command`，从该 shell 运行的后续 `command` 不受 `sudo` 安全策略的约束。对于提供 shell 转义（包括大多数编辑器）的 `command` 也是如此。如果启用了 I/O 日志记录，后续 `command` 的输入和/或输出将被记录，但不会有针对这些 `command` 的传统日志。因此，在通过 `sudo` 授予用户访问 `command` 的权限时，必须小心验证该 `command` 不会无意中给用户一个有效的 root shell。关于解决此问题的方法，参见 `sudoers(5)` 中的*防止 shell 转义*一节。

为防止泄露潜在敏感信息，`sudo` 在执行期间默认禁用核心转储（对于运行的 `command` 会重新启用）。这一历史惯例可追溯到大多数操作系统默认允许 set-user-ID 进程转储核心的时代。为帮助调试 `sudo` 崩溃，你可能希望通过在 `sudo.conf(5)` 文件中将 "disable_coredump" 设置为 false 来重新启用核心转储，如下所示：

```text
Set disable_coredump false
```

更多信息参见 `sudo.conf(5)` 手册。

## 环境

`sudo` 使用以下环境变量。安全策略对 `command` 环境的实际内容有控制权。

- `EDITOR`  
    如果 `SUDO_EDITOR` 和 `VISUAL` 均未设置，则在 `-e`（sudoedit）模式下使用的默认编辑器。

- `MAIL`  
    当指定 `-i` 选项时，或在 `sudoers` 中启用了 `env_reset` 时（除非 `MAIL` 出现在 `env_keep` 列表中），设置为目标用户的邮件假脱机。

- `HOME`  
    当指定 `-i` 或 `-H` 选项时，当指定 `-s` 选项且在 `sudoers` 中设置了 `set_home` 时，当在 `sudoers` 中启用了 `always_set_home` 时，或者在 `sudoers` 中启用了 `env_reset` 且 `HOME` 不在 `env_keep` 列表中时，设置为目标用户的主目录。

- `LOGNAME`  
    当指定 `-i` 选项时，当在 `sudoers` 中启用了 `set_logname` 选项时，或者在 `sudoers` 中启用了 `env_reset` 选项时（除非 `LOGNAME` 出现在 `env_keep` 列表中），设置为目标用户的登录名。

- `PATH`  
    可能被安全策略覆盖。

- `SHELL`  
    用于确定使用 `-s` 选项运行的 shell。

- `SUDO_ASKPASS`  
    指定用于在没有终端可用或指定 `-A` 选项时读取密码的辅助程序的路径。

- `SUDO_COMMAND`  
    设置为 `sudo` 运行的 `command`，包括任何 `arg`。`arg` 在 4096 个字符处截断，以防止潜在的执行错误。

- `SUDO_EDITOR`  
    在 `-e`（sudoedit）模式下使用的默认编辑器。

- `SUDO_GID`  
    设置为调用 `sudo` 的用户的组 ID。

- `SUDO_HOME`  
    设置为调用 `sudo` 的用户的主目录。

- `SUDO_PROMPT`  
    除非指定了 `-p` 选项，否则用作默认密码提示。

- `SUDO_PS1`  
    如果设置，`PS1` 将设置为其值用于正在运行的程序。

- `SUDO_TTY`  
    如果存在，设置为调用 `sudo` 的用户的终端设备。

- `SUDO_UID`  
    设置为调用 `sudo` 的用户的用户 ID。

- `SUDO_USER`  
    设置为调用 `sudo` 的用户的登录名。

- `USER`  
    设置为与上述 `LOGNAME` 相同的值。

- `VISUAL`  
    如果未设置 `SUDO_EDITOR`，则在 `-e`（sudoedit）模式下使用的默认编辑器。

## 文件

`/etc/sudo.conf`  
`sudo` 前端配置

## 示例

以下示例假定安全策略配置正确。

要获取不可读目录的文件列表：

```console
$ sudo ls /usr/local/protected
```

要在文件系统 ~yaz 未作为 root 导出的机器上列出用户 yaz 的主目录：

```console
$ sudo -u yaz ls ~yaz
```

要以用户 www 编辑 `index.html` 文件：

```console
$ sudoedit -u www ~www/htdocs/index.html
```

要查看仅 root 和 adm 组成员可访问的系统日志：

```console
$ sudo -g adm more /var/log/syslog
```

要以 jim 身份并使用不同的主组运行编辑器：

```console
$ sudoedit -u jim -g audio ~jim/sound.txt
```

要关闭机器：

```console
$ sudo shutdown -r +15 "quick reboot"
```

要生成 /home 分区中目录的用法列表。这些 `command` 在子 shell 中运行，以允许 `cd` 命令和文件重定向正常工作。

```console
$ sudo sh -c "cd /home ; du -s * | sort -rn > USAGE"
```

## 诊断

`sudo` 产生的错误消息包括：

- `editing files in a writable directory is not permitted`  
    默认情况下，当任何父目录可被调用用户写入时，`sudoedit` 不允许编辑文件。这避免了可能允许用户覆盖任意文件的竞争条件。更多信息参见 `sudoers(5)` 中的 `sudoedit_checkdir` 选项。

- `editing symbolic links is not permitted`  
    默认情况下，`sudoedit` 在打开文件时不跟随符号链接。更多信息参见 `sudoers(5)` 中的 `sudoedit_follow` 选项。

- `effective uid is not 0, is sudo installed setuid root?`  
    `sudo` 未以 root 权限运行。`sudo` 二进制文件必须由 root 用户拥有并设置 set-user-ID 位。此外，它不能位于使用 `nosuid` 选项挂载的文件系统上，也不能位于将 uid 0 映射到非特权 uid 的 NFS 文件系统上。

- `effective uid is not 0, is sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?`  
    `sudo` 未以 root 权限运行。`sudo` 二进制文件具有正确的所有者和权限，但仍未以 root 权限运行。最常见的原因是 `sudo` 二进制文件所在的文件系统使用 `nosuid` 选项挂载，或者它是将 uid 0 映射到非特权 uid 的 NFS 文件系统。

- `fatal error, unable to load plugins`  
    加载或初始化 `sudo.conf(5)` 中指定的插件时发生错误。

- `invalid environment variable name`  
    通过 `-E` 选项指定的一个或多个环境变量名包含等号（`=`）。`-E` 选项的参数应为不带关联值的环境变量名。

- `no password was provided`  
    当 `sudo` 尝试读取密码时，它没有收到任何字符。如果终端不可用（或指定了 `-S` 选项）且标准输入已从 `/dev/null` 重定向，则可能发生这种情况。

- `a terminal is required to read the password`  
    `sudo` 需要读取密码，但没有可用的机制来执行此操作。通过 `ssh(1)` 运行的远程命令默认没有可用的终端；向 `ssh(1)` 传递 `-t` 选项将导致它分配一个终端，这应允许 `sudo` 读取密码。要允许 `sudo` 在没有终端的情况下运行本地命令，可以使用 `-S` 选项从标准输入读取密码，或者通过 `sudo.conf(5)` 文件或设置 `SUDO_ASKPASS` 环境变量来配置 askpass 辅助程序。

- `no writable temporary directory found`  
    `sudoedit` 无法找到可用于存储中间文件的临时目录。

- `The "no new privileges" flag is set, which prevents sudo from running as root.`  
    `sudo` 由设置了 Linux "no new privileges" 标志的进程运行。这导致在运行可执行文件时忽略 set-user-ID 位，这将阻止 `sudo` 正常工作。最可能的原因是在设置了此标志的容器中运行 `sudo`。请查看文档，了解是否可以将容器配置为不设置该标志。

- `sudo must be owned by uid 0 and have the setuid bit set`  
    `sudo` 未以 root 权限运行。`sudo` 二进制文件没有正确的所有者或权限。它必须由 root 用户拥有并设置 set-user-ID 位。

- `sudoedit is not supported on this platform`  
    只能在支持设置有效用户 ID 的系统上运行 `sudoedit`。

- `timed out reading password`  
    用户未在密码超时（默认 5 分钟）到期之前输入密码。

- `you do not exist in the passwd database`  
    你的用户 ID 未出现在系统 passwd 数据库中。

- `you may not specify environment variables in edit mode`  
    只能在运行 `command` 时指定环境变量。编辑文件时，编辑器在用户环境未修改的情况下运行。

## 另请参见

“su(1)”、“stat(2)”、“login_cap(3)”、“passwd(5)”、“sudo.conf(5)”、“sudo_plugin(5)”、“sudoers(5)”、“sudoers_timestamp(5)”、“sudoreplay(8)”、“visudo(8)”

## 历史

关于 sudo 的简要历史，参见 `sudo` 发行版中的 `HISTORY.md` 文件（<https://www.sudo.ws/about/history/>）。

## 作者

多年来有许多人为 `sudo` 工作；此版本主要由以下人员编写的代码组成：

Todd C. Miller

关于为 `sudo` 做出贡献的人员的详尽列表，参见 `sudo` 发行版中的 `CONTRIBUTORS.md` 文件（<https://www.sudo.ws/about/contributors/>）。

## 注意事项

如果允许用户通过 `sudo` 运行任意 `command`，则没有简单的方法可以阻止该用户获得 root shell。此外，许多程序（如编辑器）允许用户通过 shell 转义运行 `command`，从而避免 `sudo` 的检查。但是，在大多数系统上，可以通过 `sudoers(5)` 插件的 `noexec` 功能来防止 shell 转义。

直接通过 sudo 运行 `cd` 命令没有意义，例如：

```console
$ sudo cd /usr/local/protected
```

因为当 `command` 退出时，父进程（你的 shell）仍然是相同的。可以使用 `-D` 选项在特定 `directory` 中运行 `command`。

通过 `sudo` 运行 shell 脚本可能会暴露与在某些操作系统上使 set-user-ID shell 脚本不安全的相同内核缺陷（如果你的操作系统有 /dev/fd/ 目录，set-user-ID shell 脚本通常是安全的）。

## 缺陷

如果你认为在 `sudo` 中发现了缺陷，可以在 sudo 缺陷数据库 <https://bugzilla.sudo.ws/> 中提交缺陷报告，或在 <https://github.com/sudo-project/sudo/issues> 中打开问题。如果你更喜欢使用电子邮件，可以将消息发送到 sudo-workers 邮件列表 <https://www.sudo.ws/mailman/listinfo/sudo-workers>（公开）或 <sudo@sudo.ws>（私密）。

请勿通过公开的 GitHub 问题、Bugzilla 或邮件列表报告安全漏洞。相反，请通过电子邮件将漏洞报告发送至 <Todd.Miller@sudo.ws>。如果你愿意，可以使用 <https://www.sudo.ws/dist/PGPKEYS> 中的密钥对消息进行 PGP 加密。

## 支持

通过 sudo-users 邮件列表可获得有限的免费支持，参见 <https://www.sudo.ws/mailman/listinfo/sudo-users> 订阅或搜索档案。

## 免责声明

`sudo` 按"原样"提供，任何明示或暗示的担保，包括但不限于对适销性和特定用途适用性的暗示担保，均被否认。完整细节参见随 `sudo` 分发的 `LICENSE.md` 文件或 <https://www.sudo.ws/about/license/>。

## 版本说明

本页是 `sudo`（以另一个用户身份执行命令）项目的一部分。项目信息可在 <https://www.sudo.ws/> 找到。如果对本手册页有缺陷报告，请参见 ⟨<https://bugzilla.sudo.ws/>⟩。本页获取自项目上游 Git 仓库 ⟨<https://github.com/sudo-project/sudo>⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-07-19。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
Sudo 1.9.18                    June 7, 2025                       SUDO(8)
```