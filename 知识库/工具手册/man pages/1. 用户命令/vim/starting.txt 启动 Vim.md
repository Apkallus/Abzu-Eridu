https://vimhelp.org/starting.txt.html

# 启动 Vim

`starting.txt` 适用于 `Vim version 9.2`。最后更改：2026 Sep 08

*VIM 参考手册* 作者 Bram Moolenaar

## 目录

1. Vim 参数 `vim-arguments`
2. Amiga 上的 Vim `starting-amiga`
3. 运行 eVim `evim-keys`
4. 初始化 `initialization`
5. `$VIM` 与 `$VIMRUNTIME` `$VIM`
6. 挂起 `suspend`
7. 退出 `exiting`
8. 保存设置 `save-settings`
9. 视图与会话 `views-sessions`
10. `viminfo` 文件 `viminfo-file`

---

## 1. Vim 参数 `vim-arguments`

最常见的情况是使用以下命令启动 Vim 来编辑单个文件：

```sh
vim filename
```

更一般地，Vim 的启动方式为：

```sh
vim [option | filename] ..
```

选项参数和文件名参数可以混合出现，并且可以给出任意数量。但要注意那些需要参数的选项。

关于与各种 Vi 版本的兼容性，见 `cmdline-arguments`。

以下五项中必须且只能使用一项来选择如何开始编辑：

### `filename` `--`

一个或多个文件名。第一个文件会成为当前文件并读入缓冲区。光标会定位到缓冲区的第一行。

为避免以 `-` 开头的文件名被解释为选项，可在参数列表前加上 `--`，例如：

```sh
vim -- -filename
```

`--` 之后的所有参数都会被解释为文件名，后面不能再跟其他选项或 `+command` 参数。

关于 MS-Windows 上引号的行为，见 `win32-quotes`。

### `-`

这个参数有两种含义，取决于是否使用 Ex 模式。

以 Normal 模式启动：

```sh
vim -
ex -v -
```

开始编辑一个新缓冲区，其内容从 stdin 读取。原本从 stdin 读取的命令现在改为从 stderr 读取。例如：

```sh
find . -name "*.c" -print | vim -
```

该缓冲区会被标记为已修改，以便在你尝试退出时提醒你保存文本。如果你不喜欢这样，可以把以下行放入 vimrc：

```vim
" 从 stdin 读取时不要设置 'modified'
au StdinReadPost * set nomodified
```

以 Ex 模式启动：

```sh
ex -
vim -e -
exim -
vim -E
```

以静默模式开始编辑。见 `-s-ex`。

### `-t {tag}` `-tag`

在 tags 文件中查找标签 `{tag}`，关联文件会成为当前文件，并执行关联命令。这主要用于 C 程序，其中 `tag` 通常是函数名。效果是包含该函数的文件成为当前文件，光标定位到函数开头（见 `tags`）。

### `-q [errorfile]` `-qf`

QuickFix 模式。读取名为 `[errorfile]` 的文件并显示第一个错误。见 `quickfix`。

如果没有给出 `[errorfile]`，则使用 `'errorfile'` 选项作为文件名。默认值见 `'errorfile'`。

### （无）

如果没有上述四项中的任何一项，Vim 会开始编辑一个新缓冲区。该缓冲区为空，且没有文件名。

启动模式可以通过使用 “vim” 之外的其他名称来改变，这等价于给出选项：

- `ex` → `vim -e`：以 Ex 模式启动（见 `Ex-mode`）。`ex`
- `exim` → `vim -E`：以改进的 Ex 模式启动（见 `Ex-mode`）。通常不安装。`exim`
- `view` → `vim -R`：以只读模式启动（见 `-R`）。`view`
- `gvim` → `vim -g`：启动 GUI（见 `gui`）。`gvim`
- `gex` → `vim -eg`：以 Ex 模式启动 GUI。`gex`
- `gview` → `vim -Rg`：以只读模式启动 GUI。`gview`
- `rvim` → `vim -Z`：类似 “vim”，但处于受限模式（见 `-Z`）。`rvim`
- `rview` → `vim -RZ`：类似 “view”，但处于受限模式。`rview`
- `rgvim` → `vim -gZ`：类似 “gvim”，但处于受限模式。`rgvim`
- `rgview` → `vim -RgZ`：类似 “gview”，但处于受限模式。`rgview`
- `evim` → `vim -y`：简易 Vim：设置 `'insertmode'`（见 `-y`）。`evim`
- `eview` → `vim -yR`：类似 “evim”，但处于只读模式。`eview`
- `vimdiff` → `vim -d`：以差异模式启动 `diff-mode`。
- `gvimdiff` → `vim -gd`：以差异模式启动 `diff-mode`。

后面可以跟其他字符，它们会被忽略。例如，可以用 “gvim-8” 启动 GUI。当然，你必须有一个该名称的可执行文件。

在 Unix 上，通常只有一个名为 “vim” 的可执行文件，并从不同的启动名称链接到该可执行文件。如果你的系统不支持链接，并且你不想保留多份可执行文件副本，可以使用别名。例如，在 C shell 及其衍生 shell 中：

```sh
alias view   vim -R
alias gvim   vim -g
```

选项参数可以按任意顺序给出。单字母选项可以合并在一个破折号后。`--` 参数之后不能再有选项参数。

在 VMS 上，所有选项参数都被假定为小写，除非前面带有斜杠。因此 `-R` 表示恢复，而 `-/R` 表示只读。

### `--help` `-h` `-?`

显示用法（帮助）消息并退出。关于捕获文本，见 `info-message`。

### `--version`

打印版本信息并退出。输出与 `:version` 命令相同。关于捕获文本，见 `info-message`。

### `--noplugin`

跳过加载插件。重置 `'loadplugins'` 选项。

注意，`-u` 参数也可能禁用加载插件：

| 参数 | 加载：vimrc 文件 | 插件 | `defaults.vim` |
| --- | --- | --- | --- |
| （无） | 是 | 是 | 是 |
| `-u NONE` | 否 | 否 | 否 |
| `-u DEFAULTS` | 否 | 否 | 是 |
| `-u NORC` | 否 | 是 | 否 |
| `--noplugin` | 是 | 否 | 是 |

### `--startuptime {fname}`

在启动期间将计时消息写入文件 `{fname}`。这可用于找出加载 .vimrc、插件和打开第一个文件时时间花在哪里。如果 `{fname}` 已存在，新消息会追加。

{仅当编译时包含 `+startuptime` 特性时可用}

### `--literal`

按字面处理文件名，不展开通配符。在 Unix 上不需要，因为 Vim 总是按字面处理文件名（通配符由 shell 展开）。适用于所有名称，也包括出现在此参数之前的名称。

### `+[num]`

光标会定位到第一个正在编辑文件的第 “num” 行。如果省略 “num”，光标会定位到最后一行。

### `+/{pat}`

光标会定位到第一个正在编辑文件中包含 “pat” 的第一行（可用搜索模式见 `pattern`）。搜索从光标位置开始，可能是第一行，也可能是从 viminfo 上次使用的光标位置开始。要强制从第一行开始搜索，使用 `+1 +/pat`。

### `+{command}` `-c {command}`

`{command}` 会在第一个文件读入后执行（并且在该文件的自动命令和模式行处理之后）。`command` 被解释为 Ex 命令。如果 `command` 包含空格，必须用双引号括起来（取决于所使用的 shell）。例如：

```sh
vim  "+set si"  main.c
vim  "+find stdio.h"
vim  -c "set ff=dos"  -c wq  mine.mak
```

注意：在一个 Vim 命令中最多可以使用 10 个 `+` 或 `-c` 参数。它们按给定顺序执行。`-S` 参数也算作一个 `-c` 参数。

### `--cmd {command}`

`{command}` 会在处理任何 vimrc 文件之前执行。除此之外，它像 `-c {command}` 一样工作。最多可以使用 10 个此类命令，独立于 `-c` 命令。

### `-S {file}`

`{file}` 会在第一个文件读入后执行。这是实现以下等价操作的简便方式：

```sh
-c "source {file}"
```

它可以与 `-c` 参数混合使用，并且可以像 `-c` 一样重复。10 个 `-c` 参数的限制同样适用。`{file}` 不能以 `-` 开头。

不要用它来运行一个完成某些工作并退出 Vim 的脚本，因为你看不到错误消息。请改用 `-u`。

### `-S`

工作方式类似 `-S Session.vim`。仅当它作为最后一个参数使用，或后面跟着另一个 `-` 选项时有效。

### `-r`

恢复模式。没有文件名参数时，会给出一个现有交换文件列表。有文件名时，会读取交换文件以恢复崩溃的编辑会话。见 `crash-recovery`。

### `-L`

与 `-r` 相同。

### `-R`

只读模式。正在编辑的所有文件都会设置 `'readonly'` 选项。你仍然可以编辑缓冲区，但会阻止意外覆盖文件。如果你忘了自己处于 View 模式并做了修改，可以在 Ex 命令后加感叹号来覆盖文件，例如 `:w!`。`'readonly'` 选项可以用 `:set noro` 重置（见选项章节 `options`）。后续编辑将不再以只读模式进行。将可执行文件称为 `view` 与使用 `-R` 参数效果相同。`'updatecount'` 选项会被设置为 10000，这意味着交换文件不会非常频繁地自动更新。关于禁止修改，见 `-M`。

### `-m`

不允许写入修改。会重置 `'write'` 选项，从而禁用写入文件。但是可以设置 `'write'` 选项来重新启用写入。

### `-M`

不允许修改。会重置 `'modifiable'` 选项，从而不允许更改。也会重置 `'write'` 选项，从而禁用写入文件。但是可以设置 `'modifiable'` 和 `'write'` 选项来启用更改和写入。

### `-Z` `restricted-mode` `E145` `E981`

受限模式。所有使用外部 shell 的命令都被禁用。这包括使用 `CTRL-Z` 挂起、`:sh`、过滤、`system()` 函数、反引号展开和 `libcall()`。也被禁用的包括 `delete()`、`rename()`、`mkdir()`、`job_start()`、`setenv()` 以及设置环境变量等。接口，例如 Python、Ruby 和 Lua，也被禁用，因为它们可能被用来执行 shell 命令。Perl 使用 Safe 模块。

对于 Unix，受限模式在 `$SHELL` 的最后一部分是 “nologin” 或 “false” 时使用。注意，用户仍然可能找到漏洞来执行 shell 命令，只是被弄得困难了。

### `-g`

以 GUI 模式启动 Vim。见 `gui`。相反的是 `-v`。

### `-v`

以 Vi 模式启动 Ex。仅当可执行文件名为 `ex` 或 `gvim` 时才有区别。对于 `gvim`，如果可能，不会启动 GUI。

### `-e`

以 Ex 模式启动 Vim，见 `Ex-mode`。仅当可执行文件不叫 `ex` 时才有区别。

### `-E`

以改进的 Ex 模式启动 Vim `gQ`。仅当可执行文件不叫 `exim` 时才有区别。

### `-s` `-s-ex`

静默或批处理模式。仅当 Vim 以 `ex` 启动，或前面带有 `-e` 参数时有效。否则，见 `-s`，那种用法需要参数，而这种 `-s` 用法不需要参数。

当 Vim 用于从文件执行 Ex 命令而不是从终端执行时使用。关闭大多数提示和信息消息，也关闭警告和错误消息。以下命令的输出会显示（到 stdout）：

- `:print`
- `:list`
- `:number`
- `:set` 用于显示选项值。

当 `'verbose'` 非零时，消息会打印出来（用于调试，输出到 stderr）。不使用 `'term'` 和 `$TERM`。

如果 Vim 似乎卡住了，尝试输入 “qa!<Enter>”。你不会得到提示，因此看不到 Vim 正在等待你输入。初始化会被跳过（除非使用 `-u` 参数给出的初始化）。示例：

```sh
vim -e -s  < thefilter  thefile
```

相反，要查看脚本中的错误，可使用 `-u` 标志执行文件：

```sh
vim -u thefilter thefile
```

### `-b`

二进制模式。文件 I/O 只识别 `<NL>` 作为行分隔符。会重置 `'expandtab'` 选项。`'textwidth'` 选项设置为 0。`'modeline'` 被重置。`'binary'` 选项被设置。这些在读取 vimrc/exrc 文件之后、读取参数列表中任何文件之前完成。另见 `edit-binary`。

### `-l`

Lisp 模式。打开 `'lisp'` 和 `'showmatch'` 选项。

### `-A`

阿拉伯语模式。打开 `'arabic'` 选项。{仅当编译时包含 `+arabic` 特性（包括 `+rightleft`）时可用，否则 Vim 会给出错误消息并退出}

### `-F`

这曾用于 Farsi 模式，该模式已被移除。见 `farsi.txt`。

### `-H`

希伯来语模式。打开 `'hkmap'` 和 `'rightleft'` 选项。{仅当编译时包含 `+rightleft` 特性时可用，否则 Vim 会给出错误消息并退出}

### `-V[N]` `verbose`

详细模式。将 `'verbose'` 选项设置为 `[N]`（默认：10）。每 `:source` 一个文件以及读写 viminfo 文件时都会给出消息。可用于查明启动和退出时发生了什么。例如：

```sh
vim -V8 foobar
```

### `-V[N]{filename}`

类似 `-V`，并将 `'verbosefile'` 设置为 `{filename}`。结果是消息不显示，而是写入文件 `{filename}`。`{filename}` 不能以数字开头。例如：

```sh
vim -V20vimlog foobar
```

### `--log {filename}`

开始记录日志并将条目写入 `{filename}`。工作方式类似于在启动早期调用 `ch_logfile({filename}, 'ao')`。

{仅当包含 `+eval` 和 `+channel` 特性时可用}

### `-D`

调试。执行脚本中的第一条命令时进入调试模式。`debug-mode`

{编译时不含 `+eval` 特性时不可用}

### `-C`

兼容模式。设置 `'compatible'` 选项。即使存在 .vimrc 文件，也可以用这个得到 `'compatible'`。请记住，某些插件或启动脚本中的 `:set nocompatible` 命令会覆盖它，因此最终可能仍是 `'nocompatible'`。要查明，使用：

```vim
:verbose set compatible?
```

若干插件在设置了 `'compatible'` 时无法工作。你可能想在启动后这样设置：

```sh
vim "+set cp" filename
```

另见 `compatible-default`。

### `-N`

非兼容模式。重置 `'compatible'` 选项。当没有 .vimrc 文件或使用 `-u NONE` 时，可以用这个得到 `'nocompatible'`。另见 `compatible-default`。

### `-y` `easy`

简易模式。对 `evim` 和 `eview` 隐含。启动时设置 `'insertmode'`，行为像点击输入式编辑器。这会 source `$VIMRUNTIME/evim.vim` 脚本。映射被设置为像大多数点击输入式编辑器一样工作，见 `evim-keys`。如果可用，会启动 GUI。

### `-n`

不使用交换文件。崩溃后恢复将不可能。如果你想在非常慢的介质（例如软盘）上查看或编辑文件，这会很方便。也可以用 `:set updatecount=0` 做到。可以通过将 `'updatecount'` 选项设置为某个值来重新打开它，例如 `:set uc=100`。

注意：不要把 `-n` 与 `-b` 组合成 `-nb`，因为那有不同的含义：`-nb`。`'updatecount'` 在从 vimrc 文件执行命令之后、GUI 初始化之前被设置为 0。因此它会覆盖 vimrc 文件中对 `'updatecount'` 的设置，但不会覆盖 gvimrc 文件中的设置。见 `startup`。

当你想减少对磁盘的访问（例如笔记本电脑），不要使用 `-n`，而是将 `'updatetime'` 和 `'updatecount'` 设置为非常大的数字，并在想保存工作时输入 `:preserve`。这样你保留了崩溃恢复的可能性。

### `-o[N]`

打开 N 个窗口，水平分割。如果未给出 `[N]`，则为作为参数给出的每个文件打开一个窗口。如果没有足够空间，只有前几个文件获得窗口。如果窗口数多于参数，最后几个窗口将编辑空文件。

### `-O[N]`

打开 N 个窗口，垂直分割。其他方面类似 `-o`。如果同时给出 `-o` 和 `-O`，命令行上最后一个决定窗口如何分割。

### `-p[N]`

打开 N 个标签页。如果未给出 `[N]`，则为作为参数给出的每个文件打开一个标签页。最大数量由 `'tabpagemax'` 页设置（默认 10）。如果标签页数多于参数，最后几个标签页将编辑空文件。另见 `tabpage`。

### `-T {terminal}`

将终端类型设置为 `{terminal}`。这会影响 Vim 发送到终端的代码。通常不需要，因为 Vim 能找出你使用的终端类型。（见 `terminal-info`。）

### `--not-a-term`

告诉 Vim 用户知道输入和/或输出未连接到终端。这会避免警告和原本会发生的两秒延迟。也避免 “Reading from stdin...” 以及 “N files to edit” 消息。

### `--gui-dialog-file {name}`

使用 GUI 时，不显示对话框，而是将对话框的标题和消息写入文件 `{name}`。该文件会被创建或追加。仅用于测试，避免测试因看不见的对话框而卡住。没有 GUI 时该参数被忽略。

### `--ttyfail`

当 stdin 或 stdout 不是终端（tty）时立即退出。

### `--stdio-channel`

将 Vim 的 stdin 和 stdout 用作通道，而不是用作终端。隐含 `-es`：不显示任何内容，不读取 Ex 命令，不启动 GUI。脚本用 `ch_open()` 和地址 “stdio” 打开通道。见 `channel-stdio`。在启动命令和脚本执行完后，Vim 等待通道上的消息，并在通道关闭时退出。

{仅当编译时包含 `+channel` 特性时可用}

### `-d`

以差异模式启动，类似 `vimdiff`。

{编译时不含 `+diff` 特性时不可用}

### `-d {device}`

仅在 Amiga 上，且编译时不含 `+diff` 特性时。工作方式类似 `-dev`。

### `-dev {device}`

仅在 Amiga 上：打开 `{device}` 用于编辑。通常你会用它设置窗口位置和大小：`-d con:x/y/width/height`，例如 `-d con:30/10/600/150`。但你也可以用它开始在另一个设备上编辑，例如 `AUX:`。

### `-f`

GUI：不要与启动 Vim 的程序断开连接。'f' 代表 “foreground”。如果省略，GUI 会 fork 一个新进程并退出当前进程。当 gvim 由会等待编辑会话结束的程序（例如 mail 或 readnews）启动时，应使用 `-f`。如果你希望 gvim 永远不 fork，在 gvimrc 的 `'guioptions'` 中包含 'f'。

小心：你可以使用 `-gf` 在前台启动 GUI，但 `-fg` 用于指定前景色。`gui-fork`

Amiga：不要重启 Vim 来打开新窗口。当 Vim 由会等待编辑会话结束的程序（例如 mail 或 readnews）启动时，应使用此选项。见 `amiga-window`。

MS-Windows：不支持此选项。但是，当使用已安装的 vim.bat 或 gvim.bat 文件运行 Vim 时，它可以工作。

### `--nofork`

GUI：不要 fork。与 `-f` 相同。

### `-u {vimrc}` `E282`

读取文件 `{vimrc}` 进行初始化。大多数其他初始化会被跳过；见 `initialization`。

这可用于以特殊模式启动 Vim，带有特殊映射和设置。可以使用 shell 别名使其易于使用。例如，在 C shell 及其衍生 shell 中：

```sh
alias vimc 'vim -u ~/.c_vimrc \!*'
```

在 Bash shell 中：

```sh
alias vimc='vim -u ~/.c_vimrc'
```

也可以考虑使用自动命令；见 `autocommand`。

当 `{vimrc}` 等于 “NONE”（全大写）时，跳过所有来自文件和环境变量的初始化，包括 GUI 启动时读取 gvimrc 文件。加载插件也会被跳过。

当 `{vimrc}` 等于 “NORC”（全大写）时，效果与 “NONE” 相同，但不会跳过加载插件。

当 `{vimrc}` 等于 “DEFAULTS”（全大写）时，效果与 “NONE” 相同，但会加载 `defaults.vim` 脚本，它还会设置 `'nocompatible'`。另见 `--clean`。

使用 `-u` 参数且值不是 DEFAULTS 时，会有副作用：`'compatible'` 选项默认会打开。这可能会产生意外效果。见 `'compatible'`。

### `-U {gvimrc}` `E230`

GUI 启动时读取文件 `{gvimrc}` 进行初始化。其他 GUI 初始化会被跳过。当 `{gvimrc}` 等于 “NONE” 时，完全不会读取任何文件进行 GUI 初始化。`gui-init`

例外：始终会读取系统级菜单文件。

### `-i {viminfo}`

使用文件 `{viminfo}` 代替默认 viminfo 文件。如果使用名称 “NONE”（全大写），则不读取也不写入 viminfo 文件，即使设置了 `'viminfo'`，或使用 `:rv` / `:wv` 时也是如此。另见 `viminfo-file`。

### `--clean`

类似于 `-u DEFAULTS -U NONE -i NONE`：

- 跳过来自文件和环境变量的初始化
- 将 `'runtimepath'` 和 `'packpath'` 设置为排除 home 目录条目（使用 `-u DEFAULTS` 时不会发生）
- 加载 `defaults.vim` 脚本，这意味着 `'nocompatible'`：使用 Vim 默认值
- 不加载 gvimrc 脚本
- 不读取也不写入 viminfo 文件

注意，后面的 `-u` 参数会覆盖 `-u DEFAULTS` 的效果。

### `-x`

使用加密读写文件。会提示输入密钥，然后存入 `'key'` 选项。之后所有写入都会使用该密钥加密文本。读取文件时不需要 `-x` 参数，因为 Vim 会检查正在读取的文件是否已加密，并自动询问密钥。`encryption`

{仅当编译时包含 `+cryptv` 特性时可用}

### `-X`

不要尝试连接 X 服务器来获取当前窗口标题以及使用 X 剪贴板进行复制/粘贴。当在终端模拟器中运行 Vim 且与 X 服务器的连接很慢时，这可以避免启动时间过长。见 `--startuptime` 了解这是否影响你。仅在 Unix 或 VMS 上，且编译时包含 `+X11` 特性时才有区别。否则会被忽略。要仅对特定终端禁用连接，见 `'clipboard'` 选项。当内置了 X11 Session Management Protocol (XSMP) 处理器时，`-X` 选项也会禁用该连接，因为它也可能产生不良延迟。如果之后仍然需要连接（例如用于客户端-服务器消息），调用 `serverlist()` 函数。不过这不会启用 XSMP 处理器。

### `-Y`

不要尝试连接 Wayland 合成器。仅对 Unix 相关，且编译时包含 `+wayland` 特性时有效，否则被忽略。注意，这会使任何使用 Wayland 的功能不可用，例如剪贴板。

### `-s {scriptin}`

读取脚本文件 “scriptin”。文件中的字符会被解释为仿佛是你输入的。也可以用命令 `:source! {scriptin}` 做到相同的事。如果在编辑器退出前到达文件末尾，后续字符会从键盘读取。仅在不是以 Ex 模式启动时有效，见 `-s-ex`。另见 `complex-repeat`。

### `-w {number}`

将 `'window'` 选项设置为 `{number}`。

### `-w {scriptout}`

你输入的所有字符都会记录到文件 “scriptout”，直到退出 Vim。如果你想创建用于 `vim -s` 或 `:source!` 的脚本文件，这会很有用。当 “scriptout” 文件已存在时，新字符会追加。另见 `complex-repeat`。`{scriptout}` 不能以数字开头。如果你想以人类可读形式记录输入内容，可以使用 `ch_logfile()`。它会添加 “raw key input” 行。另见 `--log`。

### `-W {scriptout}`

类似 `-w`，但不追加，而是覆盖现有文件。

### `--remote [+{cmd}] {file} ...`

在另一个作为服务器运行的 Vim 中打开 `{file}`。任何非文件参数必须放在此参数之前。见 `--remote`。

### `--remote-silent [+{cmd}] {file} ...`

类似 `--remote`，但没有服务器时不报错。见 `--remote-silent`。

### `--remote-wait [+{cmd}] {file} ...`

类似 `--remote`，但等待服务器完成编辑文件。见 `--remote-wait`。

### `--remote-wait-silent [+{cmd}] {file} ...`

类似 `--remote-wait`，但没有服务器时不报错。见 `--remote-wait-silent`。

### `--servername {name}`

指定要发送到的或要成为的 Vim 服务器名称。见 `--servername`。

### `--remote-send {keys}`

将 `{keys}` 发送到 Vim 服务器并退出。见 `--remote-send`。

### `--remote-expr {expr}`

在另一个作为服务器运行的 Vim 中求值 `{expr}`。结果打印到 stdout。见 `--remote-expr`。

### `--serverlist`

输出 Vim 服务器名称列表并退出。见 `--serverlist`。

### `--socketid {id}`

仅 GTK+ GUI Vim。让 gvim 尝试使用 GtkPlug 机制，以便在另一个窗口中运行。详情见 `gui-gtk-socketid`。

### `--windowid {id}`

仅 Win32 GUI Vim。让 gvim 尝试使用窗口 `{id}` 作为父窗口，以便在该窗口中运行。详情见 `gui-w32-windowid`。

### `--echo-wid`

仅 GTK+ GUI Vim。让 gvim 在 stdout 上回显 Window ID，可用于在 kpart 部件中运行 gvim。输出格式为：

```log
WID: 12345\n
```

### `--display {display}`

在 `{display}` 上运行 Vim，连接到该 X 服务器而不是 `$DISPLAY` 中的服务器。长格式 `--display` 仅被 GTK+ 2 或 GTK+ 3 GUI 接受，另见 `-display`。

{仅当包含 `+xterm_clipboard` 特性时可用}

### `--role {role}`

仅 GTK+ 2 GUI。将主窗口的角色设置为 `{role}`。窗口角色可被窗口管理器用来唯一标识窗口，以便恢复窗口位置等。登录时恢复会话会自动传递 `--role` 参数。见 `gui-gnome-session`。

### `-P {parent-title}` `MDI` `E671` `E672`

仅 Win32：指定父应用程序的标题。如果可能，Vim 会在应用程序内的 MDI 窗口中运行。`{parent-title}` 必须出现在父应用程序的窗口标题中。确保它足够具体。注意，实现仍很原始。它不会对所有应用程序有效，菜单也不能工作。

### `-nb`

`-nb={fname}`  
`-nb:{hostname}:{addr}:{password}`

尝试连接 Netbeans 并成为其编辑器服务器。第二种形式指定要从其读取连接信息的文件。第三种形式指定用于连接 Netbeans 的主机名、地址和密码。`netbeans-run`

{仅当编译时包含 `+netbeans_intg` 特性时可用；如果没有，`-nb` 会使 Vim 退出}

如果可执行文件名为 `view`，Vim 会以只读模式启动。如果你能创建从 `view` 到 `vim` 的硬链接或符号链接，这会很有用。也可以使用 `vim -R` 以只读模式启动。

如果可执行文件名为 `ex`，Vim 会以 Ex 模式启动。这意味着它只接受 `:` 命令。但是当给出 `-v` 参数时，Vim 仍会以 Normal 模式启动。

在类 Unix 系统上，如果编译时包含 X11 GUI 支持，还有额外参数可用。见 `gui-resources`。

---

## 2. Amiga 上的 Vim `starting-amiga`

### 从 Workbench 启动 Vim `workbench`

可以通过双击 Vim 图标从 Workbench 启动 Vim。然后它会以一个空缓冲区启动。

可以使用 “Project” 图标启动 Vim 来编辑一个或多个文件。图标的 “Default Tool” 必须是 Vim 可执行文件的完整路径名。“.info” 文件的名称必须与文本文件名称相同。双击此图标时，Vim 会以该文件名作为当前文件名启动，并将其读入缓冲区（如果存在）。你可以在点击图标时按住 Shift 键，并双击最后一个图标来编辑多个文件。所有这些图标的 “Default Tool” 必须相同。

无法从 Workbench 向 Vim 提供除文件名以外的参数。

### Vim 窗口 `amiga-window`

Vim 会在启动它的 CLI 窗口中运行。如果 Vim 是用 “run” 或 “runback” 命令启动的，或者从 Workbench 启动，它会打开自己的窗口。

技术细节：为了打开新窗口，使用了一个小技巧。一旦 Vim 识别出它不在普通 CLI 窗口中运行，它会在 `t:` 中创建一个脚本文件。该脚本文件包含与启动 Vim 时相同的命令，以及一个 “endcli” 命令。然后使用 “newcli” 命令执行该脚本文件（需要 “c:run” 和 “c:newcli” 命令才能工作）。脚本文件会一直保留到重启，或直到你删除它。需要此方法才能让 `:sh` 和 `:!` 命令正常工作。但是当 Vim 使用 `-f` 选项（前台模式）启动时，不使用此方法。原因是当程序使用 `-f` 选项启动 Vim 时，它会等待 Vim 退出。使用脚本技巧时，调用程序不知道 Vim 何时退出。当 Vim 由也会等待编辑会话结束的邮件程序启动时，可以使用 `-f` 选项。因此，使用 `-f` 选项时，`:sh` 和 `:!` 命令不可用。

Vim 会自动识别窗口大小并响应窗口大小变化。在 Amiga DOS 1.3 下，建议使用快速字体程序 “FF” 来加速显示重绘。

---

## 3. 运行 eVim `evim-keys`

EVim 将 Vim 作为点击输入式编辑器运行。这与原始 Vi 理念非常不同。但它对不常使用 Vim、没时间学习命令的人有帮助。希望他们会发现，学习使用 Normal 模式命令会让编辑更加高效。

在 Evim 中，以下选项会从默认值更改：

- `:set nocompatible`：使用 Vim 改进
- `:set insertmode`：大多数时间保持 Insert 模式
- `:set hidden`：保持不可见缓冲区已加载
- `:set backup`：保留备份文件（VMS 除外）
- `:set backspace=2`：退格可以删除所有内容
- `:set autoindent`：新行自动缩进
- `:set history=50`：保留 50 行 Ex 命令历史
- `:set ruler`：显示光标位置
- `:set incsearch`：输入模式时显示匹配
- `:set mouse=a`：所有模式下使用鼠标
- `:set hlsearch`：高亮显示搜索模式的所有匹配
- `:set whichwrap+=<,>,[,]`：`<Left>` 和 `<Right>` 在换行处环绕
- `:set guioptions-=a`：仅非 Unix：不自动选择

键映射：

- `CTRL-Q`：退出，如果有更改则使用 `:confirm` 提示
- `<Down>`：按屏幕行移动，而不是文件行
- `<Up>`：同上
- `Q`：执行 `gq`，即格式化，而不是进入 Ex 模式
- `<BS>`：在 Visual 模式中删除选择
- `CTRL-X`：在 Visual 模式中剪切到剪贴板
- `<S-Del>`：同上
- `CTRL-C`：在 Visual 模式中复制到剪贴板
- `<C-Insert>`：同上
- `CTRL-V`：从剪贴板粘贴（任何模式）
- `<S-Insert>`：同上
- `CTRL-Z`：撤销
- `CTRL-Y`：重做
- `<M-Space>`：系统菜单
- `CTRL-A`：全选
- `<C-Tab>`：下一个窗口，`CTRL-W w`
- `<C-F4>`：关闭窗口，`CTRL-W c`

另外：

- 使用 `:behave mswin` `:behave`
- 启用语法高亮
- 启用文件类型检测、文件类型插件和缩进
- 在文本文件中，`'textwidth'` 设置为 78

一个提示：如果你想进入 Normal 模式来输入一系列命令，使用 `CTRL-L`。`i_CTRL-L`

没有办法停止 “easy 模式”，你需要退出 Vim。

---

## 4. 初始化 `initialization` `startup`

本节关于非 GUI 版本的 Vim。关于启动 GUI 时的额外初始化，见 `gui-fork`。

启动时，Vim 检查环境变量和文件，并相应地设置值。Vim 按以下顺序进行：

1. 设置 `'shell'` 和 `'term'` 选项 `SHELL` `COMSPEC` `TERM`

   如果存在环境变量 `SHELL`，则用它设置 `'shell'` 选项。在 Win32 上，如果未设置 `SHELL`，则使用 `COMSPEC` 变量。如果存在环境变量 `TERM`，则用它设置 `'term'` 选项。但是，当启动 GUI 时（下面第 8 步），`'term'` 稍后会改变。

2. 处理参数

   检查启动 Vim 的命令中的选项和文件名。`-V` 参数可用于显示或记录接下来发生什么，便于调试初始化。执行 `--cmd` 参数。为所有文件创建缓冲区（但尚未加载）。

3. 从环境变量和/或文件执行 Ex 命令

   环境变量会作为一行 Ex 命令读取，其中多个命令必须用 `'|'` 或 `<NL>` 分隔。

   `vimrc` `exrc`

   包含初始化命令的文件称为 “vimrc” 文件。vimrc 文件中的每一行都作为一行 Ex 命令执行。它有时也称为 “exrc” 文件。它们是同一类型的文件，但 “exrc” 是 Vi 一直使用的，“vimrc” 是 Vim 特有的名称。另见 `vimrc-intro`。

   个人初始化的位置：

   - Unix：`$HOME/.vimrc`、`$HOME/.vim/vimrc` 或 `$XDG_CONFIG_HOME/vim/vimrc`
   - MS-Windows：`$HOME/_vimrc`、`$HOME/vimfiles/vimrc` 或 `$VIM/_vimrc`
   - Amiga：`s:.vimrc`、`home:.vimrc`、`home:vimfiles:vimrc` 或 `$VIM/.vimrc`
   - Haiku：`$HOME/config/settings/vim/vimrc`

   文件按上述顺序搜索，只读取找到的第一个。

   建议：将所有 Vim 配置内容放在 `$HOME/.vim/` 目录中（MS-Windows 为 `$HOME/vimfiles/`）。这样易于复制到另一个系统。

   如果 Vim 以 `-u filename` 启动，则使用文件 “filename”。直到第 4 步之前的所有后续初始化都会被跳过。不会设置 `$MYVIMRC` 和 `$MYVIMDIR`（但如果更新了 `'rtp'`，`$MYVIMDIR` 会被设置）。

   `vim -u NORC` 可用于跳过这些初始化而不读取文件。`vim -u NONE` 还会跳过加载插件。`-u`

   如果 Vim 以 Ex 模式并使用 `-s` 参数启动，则直到第 4 步之前的所有后续初始化都会被跳过。只会解释 `-u` 选项。

   在此步骤完成后，`v:vim_did_init` 变量被设置为 1。

   `evim.vim`

   a. 如果 Vim 以 `evim` 或 `eview` 启动，或带有 `-y` 参数，则会加载脚本 `$VIMRUNTIME/evim.vim`。

   `system-vimrc`

   b. 对于 Unix、MS-Windows、VMS、Macintosh 和 Amiga，会读取系统 vimrc 文件进行初始化。该文件的路径由 `:version` 命令显示。通常是 `$VIM/vimrc`。注意，此文件总是在 `'compatible'` 模式下读取，因为自动重置 `'compatible'` 只会在稍后进行。如果你愿意，可以添加 `:set nocp` 命令。对于 Macintosh，会读取 `$VIMRUNTIME/macmap.vim`。

   `VIMINIT` `.vimrc` `_vimrc` `EXINIT` `.exrc` `_exrc` `$MYVIMRC` `$MYVIMDIR`

   c. 搜索五个位置进行初始化。使用第一个存在的，忽略其他。`$MYVIMRC` 环境变量被设置为首先找到的文件，除非在使用 VIMINIT 时已经设置了 `$MYVIMRC`。`$MYVIMDIR` 环境变量被设置为个人 `'rtp'` 目录，但不验证该目录是否实际存在。

   I. 环境变量 `VIMINIT`（另见 `compatible-default`）  
      `$VIMINIT` 的值作为一行 Ex 命令使用。

   II. 用户 vimrc 文件：
      - `$HOME/.vimrc`（Unix）
      - `$HOME/.vim/vimrc`（Unix）
      - `$XDG_CONFIG_HOME/vim/vimrc`（Unix）
      - `s:.vimrc`（Amiga）
      - `home:.vimrc`（Amiga）
      - `home:vimfiles:vimrc`（Amiga）
      - `$VIM/.vimrc`（Amiga）
      - `$HOME/_vimrc`（Win32）
      - `$HOME/vimfiles/vimrc`（Win32）
      - `$VIM/_vimrc`（Win32）
      - `$HOME/config/settings/vim/vimrc`（Haiku）

   注意：对于 Unix 和 Amiga，当 “.vimrc” 不存在时，还会尝试 “_vimrc”，以防使用 MS-DOS 兼容文件系统。对于 MS-Windows，在 “_vimrc” 之后检查 “.vimrc”，以防使用长文件名。注意：对于 Win32，首先检查 `$HOME`。如果在那里找不到 “_vimrc” 或 “.vimrc”，则尝试 `$VIM`。关于 `$VIM` 未设置时的情况，见 `$VIM`。

   III. 环境变量 `EXINIT`。  
      `$EXINIT` 的值作为一行 Ex 命令使用。

   IV. 用户 exrc 文件。与用户 vimrc 文件相同，但将 “vimrc” 替换为 “exrc”。但 “.exrc” 和 “_exrc” 中只使用一个，取决于系统。并且不带上面提到的 `(*)`。

   V. 默认 vimrc 文件 `$VIMRUNTIME/defaults.vim`。这会设置选项值，并包含 “syntax on” 和 “filetype on” 命令，这是大多数新用户想要的。见 `defaults.vim`。

   d. 如果 `'exrc'` 选项打开（这不是默认值），则搜索当前目录中的三个文件。使用第一个存在的，忽略其他。

   - 文件 “.vimrc”（Unix、Amiga）  
     “_vimrc”（Win32）
   - 文件 “_vimrc”（Unix、Amiga）  
     “.vimrc”（Win32）
   - 文件 “.exrc”（Unix、Amiga）  
     “_exrc”（Win32）

   `(*)` 使用此文件或环境变量会导致 `'compatible'` 默认关闭。见 `compatible-default`。

   注意：使用 mzscheme 接口时，它会在加载 vimrc 文件之后初始化。之后更改 `'mzschemedll'` 没有效果。

4. 加载插件脚本 `load-plugins`

   这与命令 `:runtime! plugin/**/*.vim` 做相同的事。结果是，将搜索 `'runtimepath'` 选项中的所有目录中的 “plugin” 子目录，并 source 所有以 “.vim” 结尾的文件（每个目录按字母顺序），也包括子目录。

   但是，`'runtimepath'` 中以 “after” 结尾的目录会在此处跳过，只在包之后加载，见下文。

   以下情况下不会加载插件：

   - 在 vimrc 文件中重置了 `'loadplugins'` 选项。
   - 使用了 `--noplugin` 命令行参数。
   - 使用了 `--clean` 命令行参数。
   - 使用了 `-u NONE` 命令行参数 `-u`。
   - Vim 编译时不含 `+eval` 特性。

   注意，使用 `-c 'set noloadplugins'` 不起作用，因为命令行中的命令尚未执行。你可以使用 `--cmd 'set noloadplugins'` 或 `--cmd 'set loadplugins'` `--cmd`。

   加载包。这些是插件，如上所述，但在 `'packpath'` 每个条目的 “start” 目录中找到。找到的每个插件目录都会被添加到 `'runtimepath'`，然后 source 插件。见 `packages`。

   加载插件脚本，如上所述，但现在只使用以 “after” 结尾的目录。注意，如果找到了包，`'runtimepath'` 会改变，但不应添加以 “after” 结尾的目录。

5. 设置 `'shellpipe'` 和 `'shellredir'`

   `'shellpipe'` 和 `'shellredir'` 选项根据 `'shell'` 选项的值设置，除非之前已经设置过。这意味着 Vim 会为你计算 `'shellpipe'` 和 `'shellredir'` 的值，除非你自己设置了它们。

6. 如果使用了 `-n` 命令参数，则将 `'updatecount'` 设置为零。

7. 设置二进制选项

   如果给 Vim 提供了 `-b` 标志，现在会设置用于二进制编辑的选项。见 `-b`。

8. 执行 GUI 初始化

   仅在启动 “gvim” 时执行 GUI 初始化。见 `gui-init`。

9. 读取 viminfo 文件

   如果 `'viminfo'` 选项不为空，则读取 viminfo 文件。见 `viminfo-file`。

10. 读取 quickfix 文件

    如果给 Vim 提供了 `-q` 标志，则读取 quickfix 文件。如果失败，Vim 退出。

11. 打开所有窗口

    当给出 `-o` 标志时，会打开窗口（但尚未显示）。当给出 `-p` 标志时，会创建标签页（但尚未显示）。切换屏幕时，现在发生。重绘开始。如果给 Vim 提供了 `-q` 标志，会跳转到第一个错误。所有窗口的缓冲区会被加载，但不会触发 `BufAdd` 自动命令。

12. 执行启动命令

    如果给 Vim 提供了 `-t` 标志，会跳转到标签。执行用 `-c` 和 `+cmd` 参数给出的命令。如果设置了 `'insertmode'` 选项，则进入 Insert 模式。启动标志被重置，`has("vim_starting")` 现在返回零。`v:vim_did_enter` 变量被设置为 1。执行 `VimEnter` 自动命令。

`$MYVIMRC` 或 `$MYGVIMRC` 环境变量会被设置为首先找到的 vimrc 和/或 gvimrc 文件，而 `$MYVIMDIR` 被设置为用户的个人运行时目录 `'rtp'`（通常是 `'runtimepath'` 中的第一个条目）。如果 `'rtp'` 改变，`$MYVIMDIR` 会更新。注意：这些环境变量会解析符号链接，但 `'rtp'` 不会。

### 使用初始化的一些提示

标准设置：

创建一个 vimrc 文件，为所有编辑会话设置默认设置和映射。把它放在能被 3b 找到的位置：

- `~/.vimrc`（Unix）
- `s:.vimrc`（Amiga）
- `$VIM\_vimrc`（Win32）
- `~/config/settings/vim/vimrc`（Haiku）

注意，创建 vimrc 文件会导致 `'compatible'` 选项默认关闭。见 `compatible-default`。

本地设置：

将仅编辑特定目录所需的命令放入一个 vimrc 文件，并以 “.vimrc”（Win32 为 “_vimrc”）的名称放在该目录中。注意：要让 Vim 查找这些特殊文件，必须打开 `'exrc'` 选项。另见 `trojan-horse`。

系统设置：

仅当你管理一个多用户 Unix 系统并想为所有用户设置默认值时适用。创建一个包含默认设置和映射命令的 vimrc 文件，并放在 `:version` 命令给出的位置。

### 将 Vim 当前状态保存到文件

每当你更改了选项值或创建了映射，可能想将它们保存到 vimrc 文件中以供以后使用。关于将当前设置状态保存到文件，见 `save-settings`。

### 避免 Vi 用户的设置问题

Vi 使用变量 `EXINIT` 和文件 “~/.exrc”。因此，如果你不想干扰 Vi，请改用变量 `VIMINIT` 和文件 “vimrc”。

### Amiga 环境变量

在 Amiga 上存在两种环境变量。使用 DOS 1.3（或更高）setenv 命令设置的变量会被识别。见 AmigaDos 1.3 手册。使用旧 Manx Set 命令（5.0 版本之前）设置的环境变量不会被识别。

### MS-Windows 行分隔符

在 MS-Windows 上，Vim 假定所有 vimrc 文件使用 `<CR><NL>` 对作为行分隔符。如果你有一个只有 `<NL>` 的文件，并且有一行像 `:map xx yy^M`，这会产生问题。末尾的 ^M 会被忽略。

### Vi 兼容默认值 `compatible-default`

Vim 启动时，`'compatible'` 选项是打开的。Vim 开始初始化时会使用它。但一旦出现以下情况：

- 找到用户 vimrc 文件，或
- 找到当前目录中的 vimrc 文件，或
- 设置了 “VIMINIT” 环境变量，或
- 给出了 `-N` 命令行参数，或
- 给出了 `--clean` 命令行参数，或
- 加载了 `defaults.vim` 脚本，或
- 找到了 gvimrc 文件，

该选项就会被设置为 `'nocompatible'`。

注意，当找到系统级 vimrc 文件时不会发生这种情况。

这有设置或重置其他选项的副作用（见 `'compatible'`）。但只有尚未设置或重置的选项会被改变。这与启动 Vim 时 `'compatible'` 已经具有该值的效果相同。

以下情况不会重置 `'compatible'`，也不会加载 `defaults.vim`：

- 当 Vim 使用 `-u` 命令行参数启动时，尤其是 `-u NONE`，或
- 当使用 `-C` 命令行参数启动时，或
- 当可执行文件名以 “ex” 结尾时。（这样做是为了让 Vim 在以 “ex” 启动时像 “ex” 一样行为。）

但在找到 .vimrc 文件的那一刻设置或重置 `'compatible'` 有一个副作用：映射在遇到时就被解释。当使用 `<CR>` 之类的东西时会产生区别。如果映射依赖于 `'compatible'` 的某个值，请在给出映射之前设置或重置它。

### 没有 .vimrc 文件时的默认值 `defaults.vim` `E1187`

如果 Vim 正常启动且没有找到用户 vimrc 文件，则会加载 `$VIMRUNTIME/defaults.vim` 脚本。它会关闭 `'compatible'`，打开语法高亮以及一些其他东西。详情见该脚本。注意：这是从 Vim 8.0 开始做的，Vim 7.4 中没有（准确地说是在补丁 7.4.2111 中添加的）。

这对新的 Vim 用户应该很有效。如果你创建自己的 .vimrc，建议在靠近顶部的位置添加以下行：

```vim
unlet! skip_defaults_vim
source $VIMRUNTIME/defaults.vim
```

然后 Vim 会像你拥有 .vimrc 之前一样工作。将 `$VIMRUNTIME/vimrc_example.vim` 复制到你的 .vimrc 是另一种方法。或者，你可以将 `defaults.vim` 复制到你的 .vimrc 并修改它（但这样当它变化时你不会得到更新）。

如果你不喜欢某些默认值，你仍然可以 source `defaults.vim`，然后还原个别设置。关于如何还原每一项的提示，见 `defaults.vim` 文件。

`skip_defaults_vim`

如果你使用系统级 vimrc 并且不希望 `defaults.vim` 更改设置，请设置 “skip_defaults_vim” 变量。如果设置了它，而你想从 .vimrc 加载 `defaults.vim`，请先 unlet skip_defaults_vim，如上面的示例所示。

### XDG 基础目录规范 `xdg-base-dir` `$XDG_CONFIG_HOME`

XDG 基础目录规范旨在为应用程序使用的配置文件定义标准位置。这样做主要是为了防止将一切内容都倾倒到用户主目录的旧行为。该规范可在线找到：<https://specifications.freedesktop.org/basedir-spec/latest/>

这个标准配置目录的位置可由用户通过环境变量配置，但在这些变量未设置时也应提供回退。

这不是这些目录的详尽列表：

| 环境变量 | 默认位置 | 描述 |
| --- | --- | --- |
| `$XDG_CACHE_HOME` | `$HOME/.cache` | 临时数据文件 |
| `$XDG_CONFIG_HOME` | `$HOME/.config` | 配置文件 |
| `$XDG_DATA_HOME` | `$HOME/.local/share` | 持久数据文件 |
| `$XDG_STATE_HOME` | `$HOME/.local/state` | 状态数据文件 |

`xdg.vim`

Vim 本身只会使用 `$XDG_CONFIG_HOME` 目录。对其他 XDG 目录的支持由 `$VIMRUNTIME/xdg.vim` 脚本提供。注意：`xdg.vim` 仅在 `$XDG_CONFIG_HOME/vim` 目录（或其默认回退）存在时有效。默认情况下，它只设置 `'viminfofile'` 选项。其他选项设置被注释掉，详情见该脚本以了解如何启用它们。

`xdg-vimrc`

在 Unix 系统上，Vim 会在 `$XDG_CONFIG_HOME/vim/vimrc` 查找配置（见 `vimrc`），但只有在 `$HOME` 或 `$HOME/.vim` 中未找到其他初始化文件时才会 source 它（因此使此功能向后兼容）。但是，如果你想迁移到使用 `$XDG_CONFIG_HOME/vim/` 目录，你必须移走 `~/.vimrc` 和 `~/.vim/vimrc` 文件。

`xdg-runtime`

当使用 `xdg-vimrc` 时，`'runtimepath'` 和 `'packpath'` 选项会相应修改以遵循 `xdg-base-dir`：

```text
"$XDG_CONFIG_HOME/vim,$VIM/vimfiles,$VIMRUNTIME,$VIM/vimfiles/after,
 $XDG_CONFIG_HOME/vim/after"
```

### 避免特洛伊木马 `trojan-horse`

在读取当前目录中的 “vimrc” 或 “exrc” 文件时，出于安全原因，可以通过设置 `'secure'` 选项禁用某些命令。从 tags 文件执行命令时总是这样做。否则，你可能意外使用别人创建的 vimrc 或 tags 文件，其中包含恶意命令。被禁用的命令包括启动 shell 的命令、写入文件的命令以及 `:autocmd`。`:map` 命令会被回显，因此你可以看到哪些键被映射。

如果你想让 Vim 执行本地 vimrc 文件中的所有命令，可以在 `EXINIT` 或 `VIMINIT` 环境变量中，或在全局 “exrc” 或 “vimrc” 文件中重置 `'secure'` 选项。在当前目录的 “vimrc” 或 “exrc” 中不可能这样做，原因很明显。

在 Unix 系统上，仅当你不是 vimrc 文件的所有者时才会发生这种情况。警告：如果你解压一个包含 vimrc 或 exrc 文件的归档，它会被你拥有。你将没有安全保护。在该目录中启动 Vim 之前检查 vimrc 文件，或重置 `'exrc'` 选项。某些 Unix 系统允许用户对文件执行 “chown”。这使另一个用户可能创建一个恶意的 vimrc 并让你成为所有者。小心！

使用标签搜索命令时，执行搜索命令（tags 文件中该行的最后部分）总是在安全模式下进行。工作方式类似于从当前目录的 vimrc/exrc 执行命令。

### 如果 Vim 启动很慢 `slow-start`

如果 Vim 启动时间很长，使用 `--startuptime` 参数查明发生了什么。有几个常见原因：

- 如果 Unix 版本编译了 GUI 和/或 X11（检查 `:version` 输出中的 “+GUI” 和 “+X11”），它可能需要加载共享库并连接 X11 服务器。尝试编译禁用 GUI 和 X11 的版本。这也应该使可执行文件更小。在终端中运行时，使用 `-X` 命令行参数避免连接 X 服务器。
- 如果启用了 “viminfo”，加载 viminfo 文件可能需要一段时间。你可以通过暂时禁用 viminfo 来查明这是否是问题（使用 Vim 参数 `-i NONE`，`-i`）。尝试减少寄存器中存储的行数：`:set viminfo='20,<50,s10`。`viminfo-file`。

### 介绍消息 `:intro`

当 Vim 不带文件名启动时，会显示一条介绍消息（面向不知道 Vim 是什么的人）。一旦显示以任何方式重绘，它就会被移除。要再次看到该消息，使用 `:intro` 命令（如果没有足够空间，你只会看到一部分）。要避免启动时的介绍消息，将 'I' 标志添加到 `'shortmess'`。

### 信息消息 `info-message`

`--help` 和 `--version` 参数会使 Vim 打印消息然后退出。通常消息发送到 stdout，因此可以重定向到文件：

```sh
vim --help >file
```

在 Vim 内部：

```vim
:read !vim --help
```

使用 gvim 时，它会检测到自己可能是从桌面启动的，没有终端显示消息。当 stdout 和 stderr 都不是 tty 时会检测到这种情况。这会破坏 `:read` 命令，如上面示例所用。要让它再次工作，将 `'shellredir'` 设置为 `>` 而不是默认的 `>&`：

```vim
:set shellredir=>
:read !gvim --help
```

不过，对于 gvim 根本不使用 stdout 的系统，这仍然不起作用。

---

## 5. `$VIM` 与 `$VIMRUNTIME`

`$VIM`

环境变量 `$VIM` 用于定位 Vim 的各种用户文件，例如用户启动脚本 “.vimrc”。这取决于系统，见 `startup`。

为避免每个用户都需要设置 `$VIM` 环境变量，Vim 会按以下顺序尝试获取 `$VIM` 的值：

1. 由 `$VIM` 环境变量定义的值。你可以用它让 Vim 在特定目录中查找支持文件。例如：

```sh
setenv VIM /home/paul/vim
```

2. 使用 `'helpfile'` 的路径，除非它也包含某个环境变量（默认是 `$VIMRUNTIME/doc/help.txt`：先有鸡还是先有蛋的问题）。文件名（`help.txt` 或其他）被移除。然后按以下顺序移除尾部目录名：“doc”、“runtime” 和 “vim{version}”（例如 “vim82”）。

3. 对于 Win32，Vim 尝试使用可执行文件所在目录名。如果它以 “/src” 结尾，则移除。如果你将 .zip 文件解压到某个目录并调整搜索路径以找到 vim 可执行文件，这会很有用。按以下顺序移除尾部目录名：“runtime” 和 “vim{version}”（例如 “vim82”）。

4. 对于 Unix，使用编译时定义的安装目录（见 `:version` 输出）。

一旦 Vim 执行了一次，它会设置 `$VIM` 环境变量。之后要更改它，使用 `:let` 命令，如下：

```vim
:let $VIM = "/home/paul/vim/"
```

`$VIMRUNTIME`

环境变量 `$VIMRUNTIME` 用于定位各种支持文件，例如在线文档和用于语法高亮的文件。例如，主帮助文件通常是 `$VIMRUNTIME/doc/help.txt`。

你通常不自己设置 `$VIMRUNTIME`，而是让 Vim 计算出来。以下是查找 `$VIMRUNTIME` 值的顺序：

1. 如果设置了环境变量 `$VIMRUNTIME`，则使用它。当运行时文件位于不寻常位置时可以使用。
2. 如果 `$VIM/vim{version}` 存在，则使用它。`{version}` 是 Vim 版本号，不带任何 '-' 或 '.'。例如：`$VIM/vim82`。这是 `$VIMRUNTIME` 的常规值。
3. 如果 `$VIM/runtime` 存在，则使用它。
4. 使用 `$VIM` 的值。这是为了向后兼容旧版本。
5. 当设置了 `'helpfile'` 选项且其值不含 `$` 时，使用其值，并移除末尾的 “doc/help.txt”。

对于 Unix，当存在编译时默认的 `$VIMRUNTIME` 时（检查 `:version` 输出），会跳过步骤 2、3 和 4，并在步骤 5 之后使用编译时默认值。这意味着编译时默认值会覆盖 `$VIM` 的值。如果 `$VIM` 是 “/etc” 而运行时文件在 “/usr/share/vim/vim82”，这会很有用。

一旦 Vim 执行了一次，它会设置 `$VIMRUNTIME` 环境变量。之后要更改它，使用 `:let` 命令，如下：

```vim
:let $VIMRUNTIME = "/home/piet/vim/vim82"
```

如果你需要在 shell 中获取 `$VIMRUNTIME` 的值（例如用于在帮助文件中 grep 的脚本），可能可以使用：

```sh
VIMRUNTIME=$(vim -es '+put=$VIMRUNTIME|print|quit!')
```

不要把 `$VIMRUNTIME` 设置为空值，否则某些功能可能会停止工作。

---

## 6. 挂起 `suspend`

`iconize` `iconise` `CTRL-Z` `v_CTRL-Z`

`CTRL-Z`：挂起 Vim，类似 `:stop`。在 Normal 和 Visual 模式中有效。在 Insert 和 Command-line 模式中，`CTRL-Z` 会作为普通字符插入。在 Visual 模式中，Vim 会在挂起前回到 Normal 模式。注意：如果 `CTRL-Z` 撤销了更改，见 `mswin.vim`。

`:sus[pend][!]` 或 `:st[op][!]`：挂起 Vim。如果没有给出 '!' 且设置了 `'autowrite'`，则每个有更改且有文件名的缓冲区都会写出。如果给出了 '!' 或未设置 `'autowrite'`，已更改的缓冲区不会被写入，别忘了稍后将 Vim 带回前台！

在 GUI 中，挂起实现为将 gvim 图标化。在 MS-Windows 中，gvim 被最小化。

在许多 Unix 系统上，可以使用 `CTRL-Z` 挂起 Vim。这仅在 Normal 和 Visual 模式中可行（见下一章 `vim-modes`）。如果你让它再次成为前台作业，Vim 会继续。在其他系统上，`CTRL-Z` 会启动一个新 shell。这与 `:sh` 命令相同。如果你退出 shell，Vim 会继续。

在 X Window System 环境中，Vim 挂起时会放弃选择。这意味着你无法将其粘贴到另一个应用程序中（由于 Vim 将休眠，尝试获取选择会使程序挂起）。

---

## 7. 退出 `exiting`

有几种退出 Vim 的方式：

- 使用 `:quit` 关闭最后一个窗口。仅在没有更改时。
- 使用 `:quit!` 关闭最后一个窗口。即使有更改也关闭。
- 使用 `:qall` 关闭所有窗口。仅在没有更改时。
- 使用 `:qall!` 关闭所有窗口。即使有更改也关闭。
- 使用 `:cquit`。即使有更改也退出。

使用 `:cquit` 或出现错误消息时，Vim 以退出码 1 退出。可以通过使用 `:silent!` 或 `:catch` 避免错误。

---

## 8. 保存设置 `save-settings`

大多数情况下，你会手动编辑 vimrc 文件。这给你最大的灵活性。有几个命令可以自动生成 vimrc 文件。你可以按原样使用这些文件，或复制/粘贴行以包含到另一个 vimrc 文件中。

`:mk[exrc] [file]`：将当前键映射和已更改的选项写入 `[file]`（默认是当前目录中的 “.exrc”），除非它已存在。

`:mk[exrc]! [file]`：始终将当前键映射和已更改的选项写入 `[file]`（默认是当前目录中的 “.exrc”）。

`:mkv[imrc][!] [file]`：类似 `:mkexrc`，但默认是当前目录中的 “.vimrc”。还会将 `:version` 命令写入文件。

这些命令会将 `:map` 和 `:set` 命令写入文件，使得执行这些命令时，当前键映射和选项会被设置为相同的值。选项 `'columns'`、`'endofline'`、`'fileformat'`、`'key'`、`'lines'`、`'modified'`、`'scroll'`、`'term'`、`'textmode'`、`'ttyfast'` 和 `'ttymouse'` 不会包含在内，因为它们依赖于终端或文件。注意，选项 `'binary'`、`'paste'` 和 `'readonly'` 会被包含，这可能不总是你想要的。

当映射中使用特殊键时，`'cpoptions'` 选项会被临时设置为其 Vim 默认值，以避免映射被错误解释。这使文件与 Vi 不兼容，但确保它可以用于不同的终端。

只存储全局映射，不存储缓冲区局部映射。

一个常见方法是使用默认的 “.vimrc” 文件，用 `:map` 和 `:set` 命令做一些修改，然后写入修改后的文件。首先用类似 `:source ~piet/.vimrc.Cprogs` 的命令读入默认 “.vimrc”，更改设置，然后用 `:mkvimrc!` 保存到当前目录。如果你想让这个文件成为默认 .vimrc，将它移动到你的主目录（Unix）、s:（Amiga）或 `$VIM` 目录（MS-Windows）。你也可以使用自动命令 `autocommand` 和/或模式行 `modeline`。

`vimrc-option-example`

如果你只想向 vimrc 添加单个选项设置，可以使用以下步骤：

1. 用 Vim 编辑你的 vimrc 文件。
2. 调整选项直到正确。例如，尝试 `'guifont'` 的不同值。
3. 追加一行来设置选项值，使用表达式寄存器 '=' 输入值。例如，对于 `'guifont'` 选项：

```vim
o:set guifont=<C-R>=&guifont<CR><Esc>
```

[`<C-R>` 是 `CTRL-R`，`<CR>` 是回车，`<Esc>` 是 Escape 键] 你需要转义特殊字符，尤其是空格。

注意，当你创建 .vimrc 文件时，这会影响 `'compatible'` 选项，它有几个副作用。见 `'compatible'`。`:mkvimrc`、`:mkexrc` 和 `:mksession` 会首先将设置或重置 `'compatible'` 选项的命令写入输出文件，因为这些副作用。

---

## 9. 视图与会话 `views-sessions`

这在用户手册第 21.4 和 21.5 节中介绍。

`View` `view-file`

视图是应用于一个窗口的一组设置。你可以保存一个视图，之后恢复它时，文本会以相同方式显示。此窗口中的选项和映射也会被恢复，以便你可以像保存视图时一样继续编辑。

`Session` `session-file`

会话保留所有窗口的视图，以及全局设置。你可以保存一个会话，之后恢复它时，窗口布局看起来相同。你可以使用会话在不同项目之间快速切换，自动加载你上次在该项目中工作的文件。

视图和会话是 viminfo 文件的有益补充，viminfo 文件用于为所有视图和会话一起记住信息 `viminfo-file`。

你可以使用 `-S` 参数快速开始编辑之前保存的视图或会话：

```sh
vim -S Session.vim
```

所有这些 {编译时不含 `+mksession` 特性时不可用}。

`:mks[ession][!] [file]`：写入一个 Vim 脚本，恢复当前编辑会话。如果包含 [!]，则覆盖现有文件。如果省略 `[file]`，则使用 “Session.vim”。

`:mksession` 的输出类似 `:mkvimrc`，但会向文件添加额外命令。哪些命令取决于 `'sessionoptions'` 选项。生成的文件在用 `:source` 命令执行时：

1. 如果 `'sessionoptions'` 包含 “options”，则恢复全局映射和选项。脚本局部映射不会被写入。
2. 如果 `'sessionoptions'` 包含 “globals”，则恢复以大写字母开头且至少包含一个小写字母的全局变量。
3. 关闭当前标签页中除当前窗口外的所有窗口；关闭除当前标签页外的所有标签页（这会导致当前加载的缓冲区被卸载，如果设置了 `'hidden'` 或另有指定，一些可能变为隐藏）；如果当前缓冲区为空且未命名，则清除它。
4. 如果 `'sessionoptions'` 包含 “curdir”，则恢复当前目录；如果包含 “sesdir”，则将当前目录设置为会话文件所在位置。
5. 如果 `'sessionoptions'` 包含 “winpos”，则恢复 GUI Vim 窗口位置。
6. 如果 `'sessionoptions'` 包含 “resize”，则恢复屏幕大小。
7. 重新加载缓冲区列表，使用最后的 cursor 位置。如果 `'sessionoptions'` 包含 “buffers”，则恢复所有缓冲区，包括隐藏和未加载的缓冲区。否则，只恢复窗口中的缓冲区。
8. 恢复所有具有相同布局的窗口。如果 `'sessionoptions'` 包含 “help”，则恢复帮助窗口。如果 `'sessionoptions'` 包含 “blank”，则恢复编辑无名缓冲区的窗口。如果 `'sessionoptions'` 包含 “winsize” 且没有（帮助/空白）窗口被遗漏，则恢复窗口大小（相对于屏幕大小）。否则，只给窗口合理的大小。
9. 为所有窗口恢复视图，如同 `:mkview`。但使用 `'sessionoptions'` 而不是 `'viewoptions'`。
10. 如果存在与会话文件同名但以 “x.vim” 结尾的文件（eXtra），也会执行它。你可以使用 *x.vim 文件指定与给定会话关联的额外设置和操作，例如在 GUI 版本中创建菜单项。

恢复会话后，当前会话的完整文件名可在内部变量 `v:this_session` 中获得 `this_session-variable`。一个示例映射：

```vim
:nmap <F2> :wa<Bar>exe "mksession! " .. v:this_session<CR>:so ~/sessions/
```

这会保存当前会话，并开始加载另一个会话的命令。

会话包含所有标签页，除非从 `'sessionoptions'` 中移除了 “tabpages”。`tab-page`

`SessionLoadPre` 自动命令事件在会话文件加载/source 之前触发，`SessionLoadPost` 自动命令事件在之后触发。

`SessionLoad-variable`

在会话文件加载期间，SessionLoad 全局变量被设置为 1。插件可以用它来推迟一些工作，直到触发 `SessionLoadPost` 事件。

`:mkvie[w][!] [file]`：写入一个 Vim 脚本，恢复当前窗口的内容。如果包含 [!]，则覆盖现有文件。如果省略 `[file]` 或是 1 到 9 的数字，则生成名称并前置 `'viewdir'`。当 `'viewdir'` 的最后路径部分不存在时，会创建该目录。例如，当 `'viewdir'` 是 `$VIM/vimfiles/view` 时，会在 `$VIM/vimfiles` 中创建 “view”。然后始终覆盖现有文件。使用 `:loadview` 再次加载此视图。当 `[file]` 是文件名（不使用 `'viewdir'`）时，会向生成的文件添加编辑该文件的命令。

`:mkview` 的输出包含以下项：

1. 窗口中使用的参数列表。当使用全局参数列表时，会重置为全局列表。参数列表中的索引也会恢复。
2. 窗口中正在编辑的文件。如果没有文件，窗口被设为空。
3. 如果 `'viewoptions'` 包含 “options” 或 “localoptions”，则恢复窗口局部映射、缩写和选项。只恢复当前缓冲区和当前窗口局部的选项值。当作为会话的一部分存储视图且 `'sessionoptions'` 中包含 “options” 时，局部选项的全局值也会被存储。
4. 当使用手动折叠且 `'viewoptions'` 包含 “folds” 时，恢复折叠。恢复手动打开和关闭的折叠。
5. 文件中的滚动位置和光标位置。当有闭合折叠时效果不太好。
6. 如果局部当前目录与全局当前目录不同且 `'viewoptions'` 包含 “curdir”，则恢复局部当前目录。

注意，视图和会话并不完美：

- 它们不会恢复所有内容。例如，定义的函数、自动命令和 “:syntax on” 不包含在内。寄存器内容和命令行历史等内容在 viminfo 中，而不是在会话或视图中。
- 全局选项值仅在它们与默认值不同时设置。当当前值不是默认值时，加载会话不会将其设回默认值。但局部选项会被设回默认值。
- 现有映射会被无警告覆盖。现有映射可能导致歧义错误。
- 当存储手动折叠以及存储手动打开/关闭的折叠时，保存和加载视图之间文件的变化会搞乱它。
- Vim 脚本效率不高。但仍然比你自己输入命令快！

`:lo[adview] [nr]`：加载当前文件的视图。当省略 `[nr]` 时，加载用 `:mkview` 存储的视图。当指定 `[nr]` 时，加载用 `:mkview [nr]` 存储的视图。

`:mkview` 和 `:loadview` 的组合可用于存储一个文件最多十个不同视图。它们记在 `'viewdir'` 选项指定的目录中。视图使用文件名存储。如果文件被重命名或通过（符号）链接访问，视图将找不到。

你可能想不时清理 `'viewdir'` 目录。

要为 *.c 文件自动保存和恢复视图：

```vim
au BufWinLeave *.c mkview
au BufWinEnter *.c silent loadview
```

---

## 10. `viminfo` 文件 `viminfo` `viminfo-file` `E136` `E575` `E576` `E577`

如果你退出 Vim 然后稍后再次启动它，通常会丢失大量信息。viminfo 文件可用于记住这些信息，使你能够从上次离开的地方继续。

这在用户手册第 21.3 节中介绍。

viminfo 文件用于存储：

- 命令行历史。
- 搜索字符串历史。
- 输入行历史。
- 非空寄存器的内容。
- 多个文件的标记。
- 文件标记，指向文件中的位置。
- 最后搜索/替换模式（用于 'n' 和 '&'）。
- 缓冲区列表。
- 全局变量。

如果编译时禁用了 `+viminfo` 特性，则不支持 viminfo 文件。

你也可以使用会话文件。区别在于 viminfo 文件不依赖于你正在处理的内容。通常只有一个 viminfo 文件。会话文件用于保存特定编辑会话的状态。你可以有多个会话文件，每个项目一个。viminfo 和会话文件一起使用可以有效地进入 Vim 并直接在你想要的设置中开始工作。`session-file`

`viminfo-security`

Vim 写入的 viminfo 文件是纯文本，包含 List、Dictionary 和 Tuple 值的 Vim 表达式。当 Vim 将文件作为 viminfo 文件处理时，如果 `'viminfo'` 中包含 “!”，这些表达式会被求值。`'viminfo'` 的默认值不包含 “!”，因此默认不会进行表达式求值。

在缓冲区中打开 viminfo 文件（例如使用 `:edit`）是无害的；Vim 只显示文件内容。风险在于让 Vim 通过 viminfo 机制处理不受信任的文件，这发生在：

- 对该文件使用 `:rviminfo`，或
- `'viminfofile'` 被设置为指向它，或
- 文件被放在 Vim 已经作为 viminfo 文件读取的路径 `viminfo-file-name`

在任何这些情况下，如果你不信任它，就不要在 `'viminfo'` 中包含 “!”。

`viminfo-read`

当 Vim 启动且 `'viminfo'` 选项非空时，会读取 viminfo 文件的内容，信息可在适当位置使用。`v:oldfiles` 变量会被填充。启动时不会读取标记（但会读取文件标记）。关于启动时如何设置 `'viminfo'` 选项，见 `initialization`。

`viminfo-write`

当 Vim 退出且 `'viminfo'` 非空时，信息会存储到 viminfo 文件（如果存在，实际上会与现有文件合并）。`'viminfo'` 选项是一个字符串，包含关于应存储哪些信息以及存储量限制的信息（见 `'viminfo'`）。

合并以两种方式进行。当前 Vim 会话中已更改或设置的大多数项会被存储，未更改的内容会从当前 viminfo 文件中的内容填充。例如：

- Vim 会话 A 读取 viminfo，其中包含变量 START。
- Vim 会话 B 做同样的事。
- Vim 会话 A 设置变量 AAA 和 BOTH 并退出。
- Vim 会话 B 设置变量 BBB 和 BOTH 并退出。

现在 viminfo 中会有：

- START：它在 viminfo 中，且在会话 A 或 B 中未更改
- AAA：来自会话 A 的值，会话 B 保留了它
- BBB：来自会话 B 的值
- BOTH：来自会话 B 的值，会话 A 的值丢失

`viminfo-timestamp`

对于某些项，使用时间戳来保留最后更改的版本。这里 Vim 会话退出的顺序无关紧要，最新的项总是被保留。这用于：

- 命令行历史。
- 搜索字符串历史。
- 输入行历史。
- 非空寄存器的内容。
- 跳转列表。
- 文件标记。

时间戳功能在 Vim 8.0 之前添加。从 7.4.1131 开始的旧版本 Vim 会保留带时间戳的项，但不使用它们。因此，同时使用旧版和新版 Vim 时，会保留最新数据。

Unix 注意事项：

- viminfo 文件的文件保护会被设置为防止其他用户读取，因为它可能包含你处理过的任何文本或命令。
- 如果你想与其他用户共享 viminfo 文件（例如当你 “su” 到另一个用户时），可以将文件设为对组或所有人可写。Vim 在替换 viminfo 文件时会保留这一点。小心，不要让任何人都能读写你的 viminfo 文件！
- Vim 不会覆盖当前 “真实” 用户不可写的 viminfo 文件。这有助于当你 “su” 成为 root，但你的 `$HOME` 仍设置为普通用户的主目录时。否则，Vim 会创建一个由 root 拥有、其他人无法读取的 viminfo 文件。
- viminfo 文件不能是符号链接。这是为了避免安全问题。

标记按文件分别存储。当读取文件且 `'viminfo'` 非空时，会从 viminfo 文件中读取该文件的标记。注意：标记只在退出 Vim 时写入，这没问题，因为标记会为当前编辑会话中打开的所有文件记住，除非使用了 `:bdel`。如果你想保存即将用 `:bdel` 放弃的文件的标记，使用 `:wv`。'[' 和 ']' 标记不会被存储，但 `'"` 标记会。`'"` 标记对于跳转到文件上次退出时的 cursor 位置非常有用。对于以 `'viminfo'` 中 “r” 标志给出的任何字符串开头的文件，不保存标记。这可用于避免为可移动介质上的文件保存标记（对于 MS-Windows 你会使用 “ra:,rb:”，对于 Amiga 使用 “rdf0:,rdf1:,rdf2:”）。`v:oldfiles` 变量会被填充为 viminfo 文件有标记的文件名。

`viminfo-file-marks`

大写标记（'A 到 'Z）在写入 viminfo 文件时存储。编号标记（'0 到 '9）有点特殊。当写入 viminfo 文件时（退出时或使用 `:wviminfo` 命令），'0 被设置为当前 cursor 位置和文件。旧的 '0 移到 '1，'1 移到 '2，依此类推。这类似于 “1 到 “9 删除寄存器的行为。如果当前 cursor 位置已经存在于 '0 到 '9 中，它会被移到 '0，以避免同一位置出现两次。结果是，使用 `'0` 可以跳回你退出 Vim 时的文件和行。要立即这样做，尝试使用以下命令：

```sh
vim -c "normal '0"
```

在 C shell 及其衍生 shell 中，你可以为它创建别名：

```sh
alias lvim vim -c '"'normal "'"0'"'
```

对于类似 Bash 的 shell：

```sh
alias lvim='vim -c "normal '\''0"'
```

使用 `'viminfo'` 中的 “r” 标志指定哪些文件不应记住标记。

### VIMINFO 文件名 `viminfo-file-name`

- Unix 上 viminfo 文件的默认名称是 `$HOME/.viminfo`，Amiga 上是 `s:.viminfo`，Win32 上是 `$HOME\_viminfo`。对于 Win32，当未设置 `$HOME` 时，使用 `$VIM\_viminfo`。当也未设置 `$VIM` 时，使用 `c:\_viminfo`。
- `'viminfo'` 选项中的 'n' 标志可用于指定另一个 viminfo 文件名 `'viminfo'`。
- `-i` Vim 参数可用于设置另一个文件名，`-i`。当给定的文件名是 “NONE”（全大写）时，永远不读取也不写入 viminfo 文件。下面的命令也不会！
- `'viminfofile'` 选项可以像 `-i` 参数一样使用。事实上，`-i` 参数的值存储在 `'viminfofile'` 选项中。
- 对于下面的命令，可以给出另一个文件名，覆盖默认值以及通过 `'viminfo'` 或 `-i` 给出的名称（除非是 NONE）。

### 字符编码 `viminfo-encoding`

viminfo 文件中的文本按 `'encoding'` 选项指定的方式编码。通常你会始终使用相同的 `'encoding'` 值，这工作正常。但是，如果你用与写入时不同的 `'encoding'` 值读取 viminfo 文件，某些文本（非 ASCII 字符）可能无效。如果这不可接受，将 'c' 标志添加到 `'viminfo'` 选项：

```vim
:set viminfo+=c
```

然后 Vim 会尝试将 viminfo 文件中的文本从写入时的 `'encoding'` 值转换为当前 `'encoding'` 值。这要求 Vim 编译时包含 `+iconv` 特性。文件名不会被转换。

### 手动读写 `viminfo-read-write`

有两个命令可用于手动读写 viminfo 文件。这可用于在两个正在运行的 Vim 程序之间交换寄存器：先在一个中输入 `:wv`，然后在另一个中输入 `:rv`。注意，如果寄存器已经包含内容，则需要 `:rv!`。但也要注意，这意味着所有内容都会被第一个 Vim 的信息覆盖，包括命令行历史等。

viminfo 文件本身也可以手动编辑，尽管我们建议从现有文件开始以了解格式。进去后它相当自解释。这对于创建第二个文件（例如 `~/.my_viminfo`）可能有用，其中可以包含你首次启动 Vim 时总是想要的某些设置。例如，你可以预加载具有特定数据的寄存器，或将某些命令放入命令行历史。.vimrc 文件中的一行如：

```vim
:rviminfo! ~/.my_viminfo
```

可用于加载此信息。你甚至可以为不同类型的文件（例如 C 代码）使用不同的 viminfo，并根据文件名使用 `:autocmd` 命令加载它们（见 `:autocmd`）。

`viminfo-errors`

当 Vim 在读取 viminfo 文件时检测到错误，它不会覆盖该文件。如果有超过 10 个错误，Vim 停止读取 viminfo 文件。这样做是为了避免在 viminfo 文件名错误时意外破坏文件。这可能发生在你本想输入 `vim -R file` 却意外输入 `vim -i file` 时（是的，有人意外这样做过！）。如果你想覆盖有错误的 viminfo 文件，你必须修复错误，或删除文件（在 Vim 运行时删除，以便大部分信息会被恢复）。

`:rv[iminfo][!] [file]`：从 viminfo 文件 `[file]` 读取（默认：见上面的 `viminfo-file-name`）。如果给出 [!]，则已设置的任何信息（寄存器、标记、`v:oldfiles` 等）会被覆盖。当 `'viminfofile'` 被设置为 “NONE” 时，可能会给出 “E195”。

`:wv[iminfo][!] [file]`：写入 viminfo 文件 `[file]`（默认：见上面的 `viminfo-file-name`）。当 `'viminfofile'` 被设置为 “NONE” 时，此命令没有效果。文件中的信息会首先被读入，以在旧信息和新信息之间进行合并。当使用 [!] 时，不先读取旧信息，只写入内部信息。如果 `'viminfo'` 为空，则最多写入 100 个文件的标记。当你遇到错误 “E929: Too many viminfo temp files” 时，检查没有留下旧的临时文件（例如 `~/.viminf*`），并且你可以写入 .viminfo 文件所在目录。

`:ol[dfiles]`：列出在 viminfo 文件中存储了标记的文件。此列表在启动时读取，之后仅通过 `:rviminfo!` 更改。另见 `v:oldfiles`。数字可与 `c_#<` 一起使用。输出可以用 `:filter` 过滤，例如：

```vim
filter /\.vim/ oldfiles
```

过滤发生在文件名上。{仅当编译时包含 `+eval` 特性时可用}

`:bro[wse] ol[dfiles][!]`：像 `:oldfiles` 一样列出文件名，然后提示输入数字。当数字有效时，编辑列表中的该文件。如果你得到 `press-enter` 提示，可以按 “q” 并仍然得到输入文件编号的提示。使用 [!] 放弃已修改的缓冲区。`abandon` {编译时不含 tiny 特性时不可用}

```text
vim:tw=78:ts=8:noet:ft=help:norl:
```