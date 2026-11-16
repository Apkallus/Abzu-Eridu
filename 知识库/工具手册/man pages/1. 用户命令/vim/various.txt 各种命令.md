https://vimhelp.org/various.txt.html

# various.txt

适用于 **Vim 版本 9.2**。最后更改：2026 年 9 月 30 日

*VIM 参考手册*  
作者：Bram Moolenaar

## 各种命令

1. 各种命令  
2. 像 `less` 或 `more` 一样使用 Vim

---

## 1. 各种命令

### `CTRL-L`

清除并重绘屏幕。重绘可能会在处理预输入（typeahead）之后发生。

### `:redr[aw][!]`

立即重绘屏幕。包含 `!` 时先清除屏幕。可用于在脚本或函数中重绘屏幕；如果在映射中使用，则需设置 `'lazyredraw'`。

### `:redraws[tatus][!]`

重绘当前窗口的状态行。包含 `!` 时重绘所有状态行。当 `'statusline'` 包含不会自动更新的项目时，这可用于更新状态行。若最后一个窗口没有状态行，则改为重绘标尺；当 `'rulerformat'` 包含此类项目时，这很有用。如果命令行正在编辑，则重绘会推迟到稍后。

### `:redrawt[abline]`

重绘标签行。当 `'tabline'` 包含不会触发自动更新的项目时，这可用于更新标签行。

### `:redrawtabp[anel]`

重绘 `tabpanel`。当 `'tabpanel'` 包含不会触发自动更新的项目时，这可用于更新 `tabpanel`。

### `N<Del>`

输入数字时：删除最后一位数字。  
**注意**：如果你希望用 `<BS>` 实现此功能，请将以下映射添加到 `.vimrc`：

```vim
:map CTRL-V <BS>   CTRL-V <Del>
```

如果你的 `<Del>` 键没有执行预期操作，请参阅 `:fixdel`。

### `:as[cii]` 或 `ga`

以十进制、十六进制和八进制打印光标下字符的 ASCII 值。助记：Get Ascii value。

例如，当光标位于字符 `R` 上时：

```text
<R>  82,  Hex 52,  Octal 122
```

当字符是非标准 ASCII 字符，但根据 `'isprint'` 选项可打印时，还会给出其不可打印版本。

当字符大于 127 时：

```text
<<81>>  129,  Hex 0081,  Octal 201
 <p>    254,  Hex 00fe,  Octal 376
```

其中 `<p>` 是特殊字符。

文件中的 `<Nul>` 字符在内部存储为 `<NL>`，但会显示为：

```text
<^@>  0,  Hex 00,  Octal 000
```

如果字符带有组合字符，也会一并显示。`'maxcombine'` 的值无关紧要。

如果该字符可以作为二合字母（digraph）插入，还会输出可用于创建该字符的两个字符：

```text
<ö> 246, Hex 00f6, Oct 366, Digr o:
```

这表示你可以输入 `CTRL-K` `o` `:` 来插入 `ö`。

### `g8`

打印光标下字符所用字节的十六进制值，假定其采用 UTF-8 编码。也会显示组合字符。`'maxcombine'` 的值无关紧要。带两个组合字符的字符示例：

```text
e0 b8 81 + e0 b8 b9 + e0 b9 89
```

### `8g8`

在光标处或之后查找非法的 UTF-8 字节序列。适用于两种情况：

1. 当 `'encoding'` 是任意 8 位编码时；
2. 当 `'encoding'` 是 `"utf-8"` 且 `'fileencoding'` 是任意 8 位编码时。

因此，它可用于编辑本应为 UTF-8、但因包含非法字节而被当作 8 位编码读取的文件。不会绕回文件末尾。**注意**：当光标位于非法字节上，或光标位于多字节字符中间时，该命令不会移动光标。

### `:[range]p[rint] [flags]`

打印 `[range]` 行（默认当前行）。由于 Vi 兼容性，也可拼写为 `:[range]|`（参见 `:bar`）。在空缓冲区中会报错。  
**注意**：如果你想在纸上打印文本，请参阅 `:hardcopy`。在 GUI 中可以使用 File.Print 菜单项。  
`[flags]` 参见 `ex-flags`。可以使用 `:filter` 命令只显示匹配某模式的行。

### `:[range]p[rint] {count} [flags]`

从 `[range]` 开始打印 `{count}` 行（默认当前行，参见 `cmdline-ranges`）。`[flags]` 参见 `ex-flags`。

### `:[range]P[rint] [count] [flags]`

与 `:print` 相同。显然是为那些按住 Shift 键太久的人而加入 Vi 的……  
该命令在 Vim9 脚本中不受支持。  
**注意**：用户命令可以覆盖此命令。`[flags]` 参见 `ex-flags`。

### `:[range]l[ist] [count] [flags]`

与 `:print` 相同，但用 `^` 显示不可打印字符，并在行尾放置 `$`。这可以通过 `'listchars'` 选项进一步改变。`[flags]` 参见 `ex-flags`。

### `:[range]nu[mber] [count] [flags]`

与 `:print` 相同，但在每行前加上行号。（另请参见 `'highlight'` 和 `'numberwidth'` 选项。）`[flags]` 参见 `ex-flags`。

### `:[range]# [count] [flags]`

`:number` 的同义词。

### `:#!{anything}`

被忽略，因此你可以用以下内容开始一个 Vim 脚本：

```vim
#!vim -S
let mylogbook='$HOME/logbook.md'
exe $':e {mylogbook}'
$
put ='## ' .. strftime('%d. %b %Y')
norm! o
```

使该脚本可执行并运行它，即可创建新的日记条目。

### `:[range]z[+-^.=][count]`

显示围绕 `[range]` 指定行的若干行文本；如果没有 `[range]`，则围绕当前行显示。

如果有 `[count]`，那就是你将看到的行数；如果没有 `[count]` 且只有一个窗口，则使用 `'scroll'` 选项值的两倍；否则使用当前窗口高度减 3。这就是下表中的 `scr` 值。

如果有 `[count]`，则 `'window'` 选项会被设置为其值。

`:z` 可以单独使用，也可以后跟若干标记之一。这些标记的效果如下：

| 标记 | 首行 | 末行 | 新光标行 |
|---|---|---|---|
| `+` | 当前行 | 向前 1 scr | 向前 1 scr |
| `-` | 向后 1 scr | 当前行 | 当前行 |
| `^` | 向后 2 scr | 向后 1 scr | 向后 1 scr |
| `.` | 向后 1/2 scr | 向前 1/2 scr | 向前 1/2 scr |
| `=` | 向后 1/2 scr | 向前 1/2 scr | 当前行 |

完全不指定标记等同于 `+`。如果标记是 `=`，则在当前行周围打印一行破折号。

如果设置了 `'number'` 选项，输出中将包含绝对行号。

### `:[range]z![+-^.=][count]`

类似 `:z`，但当未指定 `[count]` 时，默认值为 Vim 窗口高度减一。

### `:[range]z[!]#[+-^.=][count]`

类似 `:z` 或 `:z!`，但会给行编号。

### `:= [flags]`

打印最后一行行号。`[flags]` 参见 `ex-flags`。

### `:{range}= [flags]`

打印 `{range}` 中最后一行的行号。例如，下面会打印当前行号：

```vim
:.=
```

`[flags]` 参见 `ex-flags`。

### `:norm[al][!] {commands}`

执行普通模式命令 `{commands}`。这使得可以在命令行上执行普通模式命令。`{commands}` 会像被输入一样执行。撤销时，所有命令会一起撤销。遇到错误时执行停止。

如果给出 `[!]`，则不会使用映射。否则，当此命令从不可重映射的映射（`:noremap`）中调用时，参数仍可被映射。

`{commands}` 应该是完整命令。如果 `{commands}` 未完成一个命令，最后一个命令会像输入了 `<Esc>` 或 `<C-C>` 一样被中止。这意味着插入命令必须完成（要进入插入模式，请参见 `:startinsert`）。`:` 命令也必须完成。并且不能使用 `Q` 或 `gQ` 启动 Ex 模式。

执行 `:normal` 期间不会更新显示。

`{commands}` 不能以空格开头。请在它前面放一个计数 1，`1 ` 表示一个空格。

对于 `{commands}`，`'insertmode'` 选项会被忽略。

此命令不能后跟另一个命令，因为任何 `|` 都会被视为该命令的一部分。

此命令可以递归使用，但深度受 `'maxmapdepth'` 限制。

另一种方法是使用 `:execute`，它使用表达式作为参数。这允许使用可打印字符表示特殊字符。

示例：

```vim
:exe "normal \<c-w>\<c-w>"
```

### `:{range}norm[al][!] {commands}`

对 `{range}` 中的每一行执行普通模式命令 `{commands}`。在执行 `{commands}` 之前，光标会定位到该范围第一列，并对每一行执行。其他方面与不带范围的 `:normal` 命令相同。

### `:sh[ell]`

启动一个 shell。当 shell 退出（执行 `exit` 命令后）时，你会返回 Vim。shell 命令的名称来自 `'shell'` 选项。  
**注意**：如果 Vim 在 Amiga 上由编译器以 QuickFix 模式启动，则此命令不起作用，因为编译器会将 stdin 设置为非交互模式。

### `:!{cmd}`

用 shell 执行 `{cmd}`。另请参见 `'shell'` 和 `'shelltype'` 选项。过滤命令请参见 `:range!`。

Vim 按以下顺序使用 `'shell'`、`'shcf'`、`'sxq'` 和 `'shq'` 选项构建命令行：

```text
`&sh &shcf &sxq &shq {cmd} &shq &sxq`
```

因此同时设置 `'sxq'` 和 `'shq'` 是可能的，但很少有用。`{cmd}` 内部的额外转义也可能由 `'sxe'` 选项造成。

此外，`{cmd}` 中的所有 `cmdline-special` 字符会在传递给 shell 之前由 Vim 替换。

`{cmd}` 中的任何 `!` 都会替换为上一个外部命令（另请参见 `'cpoptions'`）。但如果 `!` 前有反斜杠，则移除该反斜杠。示例：`:!ls` 后跟 `:!echo ! \! \\!` 会执行 `echo ls ! \!`。

`{cmd}` 中的 `|` 会传递给 shell，不能用于追加 Vim 命令。参见 `:bar`。

如果 `{cmd}` 包含 `%`，它会展开为当前文件名；`#` 会展开为备用文件名。文件名中的特殊字符不会被转义，请使用引号避免其特殊含义：

```vim
:!ls "%"
```

如果文件名包含 `$`，单引号可能更合适，但这仅在文件名不包含单引号时有效：

```vim
:!ls '%'
```

下面这种方式应该总是有效，但输入更多：

```vim
:exe "!ls " .. shellescape(expand("%"),1)
```

要获得字面量 `%` 或 `#`，请在其前加反斜杠。例如，列出所有以 `%` 开头的文件：

```vim
:!ls \%*
```

换行符会结束 `{cmd}`，其后的内容会被解释为后续的 `:` 命令。但是，如果换行符前有反斜杠，则会移除该反斜杠并继续 `{cmd}`。无论换行符前有多少个反斜杠，只移除一个。

在 Unix 上，命令通常运行在非交互式 shell 中。如果你希望使用交互式 shell（以使用别名），请将 `'shellcmdflag'` 设置为 `-ic`。对于 Win32，另请参见 `:!start`。

命令执行后，会检查当前文件的时间戳和大小（`timestamp`）。

命令完成后，Vim 会重绘屏幕，因为它可能打印了任何文本。这需要 `hit-enter` 提示，以便你阅读消息。要避免这一点，请使用：

```vim
:silent !{cmd}
```

此时屏幕不会重绘，因此如果命令确实显示了内容，你必须使用 `CTRL-L` 或 `:redraw!`。不过，这取决于 `t_ti` 和 `t_te` termcap 条目的设置。

提示：如果你想在 Vim 窗口中运行 `{cmd}`，请使用 `:terminal` 命令。`:term ++shell ++close {cmd}` 可以近似 `:!{cmd}` 的行为。

### `:!!`

重复上一个 `:!{cmd}`。

### `:ve[rsion]`

打印编辑器版本号。如果编译器理解 `__DATE__`，会提及编译日期；否则显示固定的发布日期。以下各行包含 Vim 编译时启用的功能信息。如果前面有 `+`，表示包含该功能；如果有 `-`，表示排除该功能。要改变这一点，必须编辑 `feature.h` 并重新编译 Vim。要在表达式中检查这一点，请参见 `has()`。以下是功能概览。第一列显示包含它们的最小版本：

- `T`：tiny（始终）
- `N`：normal
- `H`：huge
- `m`：手动启用或取决于其他功能
- `-`：从不，功能已被移除
- （无）：取决于系统

因此，如果某功能标记为 `N`，则它包含在 Vim 的 normal 和 huge 版本中。

#### `+feature-list`

- `+acl`：包含 ACL 支持
- `+ARP`：仅 Amiga：包含 ARP 支持
- `H` `+arabic`：阿拉伯语语言支持
- `N` `+autochdir`：支持 `'autochdir'` 选项
- `T` `+autocmd`：`:autocmd`，自动命令。自 8.0.1564 起始终启用
- `H` `+autoservername`：自动启用 `clientserver`
- `m` `+balloon_eval`：GUI 中的 balloon-eval 支持。使用受支持的 GUI（Motif、GTK、GUI）编译，并且具有 Netbeans/Sun Workshop 集成或 `+eval` 功能时包含。
- `H` `+balloon_eval_term`：终端中的 balloon-eval 支持，`'balloonevalterm'`
- `N` `+browse`：`:browse` 命令
- `T` `++builtin_terms`：最大终端内置 `builtin-terms`。自 9.0.0280 起始终启用
- `N` `+byte_offset`：支持 `'statusline'` 选项中的 `o` 标志、`go` 和 `:goto` 命令。
- `m` `+channel`：进程间通信 `channel`
- `T` `+cindent`：`'cindent'`、C 缩进；始终启用
- `N` `+clientserver`：Unix 和 Win32：远程调用 `clientserver`
- `+clipboard`：编译包含剪贴板支持
- `+clipboard_working`：编译包含剪贴板支持且可用
- `+clipboard_provider`：编译包含 `clipboard-providers` 支持
- `T` `+cmdline_compl`：命令行补全 `cmdline-completion`
- `T` `+cmdline_hist`：命令行历史 `cmdline-history`
- `T` `+cmdline_info`：`'showcmd'` 和 `'ruler'`；自 9.0.0747 起始终启用
- `T` `+cmdwin`：`cmdline-window` 支持；自 9.0.0657 起始终启用
- `T` `+comments`：支持 `'comments'`
- `N` `+conceal`：`conceal` 支持，参见 `conceal`、`:syn-conceal` 等。
- `N` `+cryptv`：加密支持 `encryption`
- `H` `+cscope`：cscope 支持
- `T` `+cursorbind`：支持 `'cursorbind'`
- `m` `+cursorshape`：支持 `termcap-cursor-shape`
- `m` `+debug`：为调试而编译。
- `N` `+dialog_gui`：支持带 GUI 对话框的 `:confirm`。
- `N` `+dialog_con`：支持带控制台对话框的 `:confirm`。
- `N` `+dialog_con_gui`：支持带 GUI 和控制台对话框的 `:confirm`。
- `N` `+diff`：`vimdiff` 和 `'diff'`
- `N` `+digraphs`：二合字母 `digraphs`
- `+directx`：仅 Win32 GUI：DirectX 和 `'renderoptions'`
- `+dnd`：支持将 DnD 拖入 `~` 寄存器 `quote_~`。
- `H` `+emacs_tags`：`emacs-tags` 文件
- `N` `+eval`：表达式求值 `eval.txt`
- `T` `+ex_extra`：现在始终开启，过去用于 Vim 的额外 Ex 命令
- `N` `+extra_search`：`'hlsearch'` 和 `'incsearch'` 选项。
- `-` `+farsi`：已移除：波斯语语言
- `T` `+file_in_path`：`gf`、`CTRL-W_f` 和 `<cfile>`。自 9.0.265 起始终启用
- `N` `+find_in_path`：包含文件搜索：`[I`、`:isearch`、`CTRL-W_CTRL-I`、`:checkpath` 等。
- `N` `+folding`：折叠 `folding`
- `+footer`：`gui-footer`
- `+fork`：仅 Unix：fork shell 命令
- `T` `+float`：浮点支持。自 9.0.0491 起始终启用
- `N` `+gettext`：消息翻译 `multi-lang`
- `-` `+GUI_Athena`：仅 Unix：Athena GUI
- `+GUI_neXtaw`：仅 Unix：neXtaw GUI
- `+GUI_GTK`：仅 Unix：GTK+ GUI
- `+GUI_Motif`：仅 Unix：Motif GUI
- `+GUI_Photon`：仅 QNX：Photon GUI
- `m` `+hangul_input`：韩文输入支持 `hangul`
- `+iconv`：使用 `iconv()` 函数编译
- `+iconv/dyn`：同样 `iconv-dynamic` `/dyn`
- `H` `+image`：图像渲染，`image`
- `H` `+image_popup`：弹出窗口图像渲染，`popup-image`
- `T` `+insert_expand`：`insert_expand` 插入模式补全
- `m` `+ipv6`：支持 IPv6 网络 `channel`
- `m` `+job`：启动和停止作业 `job`
- `T` `+jumplist`：跳转列表 `jumplist`；自 8.2.3795 起始终启用
- `H` `+keymap`：`'keymap'`
- `N` `+lambda`：`lambda` 和 `closure`
- `H` `+langmap`：`'langmap'`
- `N` `+libcall`：`libcall()`
- `N` `+linebreak`：`'linebreak'`、`'breakat'` 和 `'showbreak'`
- `T` `+lispindent`：`'lisp'`
- `T` `+listcmds`：用于缓冲区列表和参数列表的 Vim 命令 `buffer-hidden` 和 `:argdelete`
- `T` `+localmap`：支持缓冲区本地映射 `:map-local`
- `m` `+lua`：Lua 接口
- `m` `+lua/dyn`：Lua 接口 `/dyn`
- `N` `+menu`：`:menu`
- `N` `+mksession`：`:mksession`
- `T` `+modify_fname`：`filename-modifiers`
- `T` `+mouse`：鼠标处理 `mouse-using`
- `N` `+mouseshape`：`'mouseshape'`
- `N` `+mouse_dec`：仅 Unix：Dec 终端鼠标处理 `dec-mouse`
- `N` `+mouse_gpm`：仅 Unix：Linux 控制台鼠标处理 `gpm-mouse`
- `m` `+mouse_gpm/dyn`：同 `+mouse_gpm`，但库依赖可选 `/dyn`
- `N` `+mouse_jsbterm`：JSB 鼠标处理 `jsbterm-mouse`
- `N` `+mouse_netterm`：仅 Unix：netterm 鼠标处理 `netterm-mouse`
- `N` `+mouse_pterm`：仅 QNX：pterm 鼠标处理 `qnx-terminal`
- `N` `+mouse_sysmouse`：仅 Unix：*BSD 控制台鼠标处理 `sysmouse`
- `N` `+mouse_sgr`：仅 Unix：sgr 鼠标处理 `sgr-mouse`
- `N` `+mouse_urxvt`：仅 Unix：urxvt 鼠标处理 `urxvt-mouse`
- `N` `+mouse_xterm`：仅 Unix：xterm 鼠标处理 `xterm-mouse`
- `T` `+multi_byte`：Unicode 支持，16 位和 32 位字符 `multibyte`。自 8.1.0811 起始终启用
- `+multi_byte_ime`：Win32 多字节字符输入法 `multibyte-ime`
- `N` `+multi_lang`：非英语语言支持 `multi-lang`
- `m` `+mzscheme`：MzScheme 接口 `mzscheme`
- `m` `+mzscheme/dyn`：MzScheme 接口 `mzscheme-dynamic` `/dyn`
- `m` `+netbeans_intg`：`netbeans`
- `T` `+num64`：64 位 Number 支持 `Number`。自 8.2.0271 起始终启用，使用 `v:numbersize` 检查 Number 的实际大小。
- `m` `+ole`：仅 Win32 GUI：`ole-interface`
- `N` `+packages`：加载包 `packages`
- `T` `+path_extra`：在 `'path'` 和 `'tags'` 中向上/向下搜索。自 9.0.0270 起始终启用
- `m` `+perl`：Perl 接口 `perl`
- `m` `+perl/dyn`：Perl 接口 `perl-dynamic` `/dyn`
- `N` `+persistent_undo`：持久化撤销 `undo-persistence`
- `N` `+popupwin`：弹出窗口 `popup-window`
- `+postscript`：`:hardcopy` 写入 PostScript 文件
- `+pango`：`:hardcopy` 使用 Pango 和 Cairo 渲染页面
- `N` `+printer`：`:hardcopy` 命令
- `H` `+profile`：`:profile` 命令
- `m` `+python`：Python 2 接口 `python`
- `m` `+python/dyn`：Python 2 接口 `python-dynamic` `/dyn`
- `m` `+python3`：Python 3 接口 `python`
- `m` `+python3/dyn`：Python 3 接口 `python-dynamic` `/dyn`
- `m` `+python3/dyn-stable`：Python 3 接口 `python-dynamic` `python-stable` `/dyn`
- `N` `+quickfix`：`:make` 和 quickfix 命令
- `N` `+reltime`：`reltime()` 函数、`'hlsearch'`/`'incsearch'` 超时、`'redrawtime'` 选项
- `H` `+rightleft`：从右到左输入 `'rightleft'`
- `m` `+ruby`：Ruby 接口 `ruby`
- `m` `+ruby/dyn`：Ruby 接口 `ruby-dynamic` `/dyn`
- `T` `+scrollbind`：`'scrollbind'`
- `N` `+signs`：`:sign`
- `T` `+smartindent`：`'smartindent'`
- `N` `+socketserver`：仅 Unix：用于 clientserver 功能的 socket 服务器后端
- `H` `+sodium`：使用 libsodium 编译，以获得更好的加密支持
- `H` `+sound`：`sound_playevent()`、`sound_playfile()` 函数等。
- `N` `+spell`：拼写检查支持，参见 `spell`
- `N` `+startuptime`：`--startuptime` 参数
- `N` `+statusline`：选项 `'statusline'`、`'rulerformat'` 以及 `'titlestring'` 和 `'iconstring'` 的特殊格式
- `-` `+sun_workshop`：已移除：`workshop`
- `N` `+syntax`：语法高亮 `syntax`
- `+system()`：仅 Unix：`+fork` 的反面
- `H` `+tabpanel`：支持 `tabpanel`
- `T` `+tag_binary`：在 tags 文件中进行二进制搜索 `tag-binary-search`
- `-` `+tag_old_static`：已移除；静态 tags 的方法 `tag-old-static`
- `-` `+tag_any_white`：已移除；曾允许 tags 文件中有任意空白
- `m` `+tcl`：Tcl 接口 `tcl`
- `m` `+tcl/dyn`：Tcl 接口 `tcl-dynamic` `/dyn`
- `m` `+terminal`：支持终端窗口 `terminal`
- `+terminfo`：使用 `terminfo` 而不是 `termcap`
- `N` `+termresponse`：支持 `t_RV` 和 `v:termresponse`
- `N` `+termguicolors`：xterm 兼容终端中的 24 位颜色支持
- `T` `+textobjects`：文本对象选择。自 9.0.0222 起始终启用。
- `N` `+textprop`：文本属性 `text-properties`
- `+tgetent`：仅非 Unix：能够使用外部 `termcap`
- `N` `+timers`：`timer_start()` 函数
- `T` `+title`：设置窗口 `'title'` 和 `'icon'`；始终启用
- `N` `+toolbar`：`gui-toolbar`
- `T` `+user_commands`：用户定义命令。`user-commands`。自 8.1.1210 起始终启用。
- `H` `+vartabs`：可变宽度制表位。`'vartabstop'`
- `T` `+vertsplit`：垂直分割窗口 `:vsplit`；自 8.0.1118 起始终启用。
- `T` `+vim9script`：Vim9 脚本
- `N` `+viminfo`：`'viminfo'`
- `T` `+virtualedit`：`'virtualedit'`。自 8.1.826 起始终启用。
- `T` `+visual`：可视模式 `Visual-mode`。自 7.4.200 起始终启用。
- `T` `+visualextra`：额外可视模式命令 `blockwise-operators`
- `T` `+vreplace`：`gR` 和 `gr`
- `+vtp`：在 MS-Windows 控制台：支持 `'termguicolors'`
- `N` `+wayland`：仅 Unix：支持 Wayland 协议。
- `N` `+wayland_clipboard`：仅 Unix：支持 Wayland 选择/剪贴板。
- `T` `+wildignore`：`'wildignore'`。自 9.0.0278 起始终启用
- `T` `+wildmenu`：`'wildmenu'`。自 9.0.0279 起始终启用
- `T` `+windows`：多个窗口；自 8.0.1118 起始终启用。
- `m` `+writebackup`：`'writebackup'` 默认开启
- `m` `+xim`：X 输入法 `xim`
- `+xfontset`：X 字体集支持 `xfontset`
- `N` `+xattr`：使用扩展属性支持编译（仅 Linux）
- `+xpm`：pixmap 支持
- `m` `+xpm_w32`：仅 Win32 GUI：pixmap 支持 `w32-xpm-support`
- `+xsmp`：XSMP（X 会话管理）支持
- `+xsmp_interact`：交互式 XSMP（X 会话管理）支持
- `N` `+xterm_clipboard`：仅 Unix：xterm 剪贴板处理
- `m` `+xterm_save`：保存和恢复 xterm 屏幕 `xterm-screens`
- `N` `+X11`：仅 Unix：可以恢复窗口标题 `X11`

#### `/dyn`

对于其中一些功能，会添加 `/dyn`，表示该功能仅在相关库可以动态加载时可用。

### `:ve[rsion] {nr}`

现在会被忽略。以前用于检查 `.vimrc` 文件的版本号。该功能已被移除，因为现在可以使用 `:if` 命令实现依赖版本的行为。

### `:redi[r]`

- 
    ```vim
    :redi[r][!] > {file}
    ```
    将消息重定向到文件 `{file}`。作为命令输出的消息会写入该文件，直到重定向结束。消息仍会显示在屏幕上。包含 `[!]` 时，会覆盖已存在的文件。省略 `[!]` 且 `{file}` 已存在时，此命令失败。

    同一时间只能有一个 `:redir` 处于活动状态。调用 `:redir` 会在开始重定向到新目标之前关闭任何活动重定向。递归使用时请查看 `execute()`。

    要停止将消息和命令回显到屏幕，请将命令放入函数，并用 `:silent call Function()` 调用它。另一种方法是使用 `'verbosefile'` 选项，它可以与 `:redir` 组合使用。

- 
    ```vim
    :redi[r] >> {file}
    ```
    将消息重定向到文件 `{file}`。如果 `{file}` 已存在，则追加。

- 
    ```vim
    :redi[r] @{a-zA-Z}
    :redi[r] @{a-zA-Z}>
    ```
    将消息重定向到寄存器 `{a-z}`。如果寄存器名大写 `{A-Z}`，则追加到寄存器内容。寄存器名后的 `>` 是可选的。

- 
    ```vim
    :redi[r] @{a-z}>>
    ```
    将消息追加到寄存器 `{a-z}`。

- 
    ```vim
    :redi[r] @*>
    :redi[r] @+>
    ```
    将消息重定向到选择区或剪贴板。为向后兼容，寄存器名后的 `>` 可以省略。参见 `quotestar` 和 `quoteplus`。

- 
    ```vim
    :redi[r] @*>>
    :redi[r] @+>>
    ```
    将消息追加到选择区或剪贴板。

- 
    ```vim
    :redi[r] @">
    ```
    将消息重定向到无名寄存器。为向后兼容，寄存器名后的 `>` 可以省略。

- 
    ```vim
    :redi[r] @">>
    ```
    将消息追加到无名寄存器。

- 
    ```vim
    :redi[r] => {var}
    ```
    将消息重定向到变量。在旧式脚本中：如果变量不存在，则创建它。如果变量已存在，则初始化为空字符串。重定向开始后，如果变量被删除、锁定或变量类型改变，则后续命令输出消息会导致错误。使用局部变量（函数中的 `l:var` 或脚本中的 `s:var`）时，如果另一个 `:redir` 导致当前重定向结束，作用域可能不同，赋值会失败。在 Vim9 脚本中：变量必须已声明为字符串。重定向结束前变量将保持为空。只能使用字符串变量。要获取单个命令的输出，可以使用 `execute()` 函数代替重定向。

- 
    ```vim
    :redi[r] =>> {var}
    ```
    将消息追加到现有变量。只能使用字符串变量。

- 
    ```vim
    :redi[r] END
    ```
    结束重定向消息。

### `:filt[er][!] {pattern} {command}`  
### `:filt[er][!] /{pattern}/ {command}`

将 `{command}` 的输出限制为匹配 `{pattern}` 的行。例如，只列出 XML 文件：

```vim
:filter /\.xml$/ oldfiles
```

如果给出 `[!]`，则将 `{command}` 的输出限制为**不**匹配 `{pattern}` 的行。

`{pattern}` 是 Vim 搜索模式。除了用 `/` 包围外，还可以使用任何非 ID 字符（参见 `'isident'`），只要它不出现在 `{pattern}` 中。没有包围字符时，模式不能包含竖线字符。不使用 `'ignorecase'`。

模式会与输出的相关部分匹配，不一定是整行。只有某些命令支持过滤，请尝试以检查是否有效。支持过滤的一些命令包括：`:#`、`:clist`、`:command`、`:files`、`:highlight`、`:history`、`:jumps`、`:let`、`:list`、`:llist`、`:marks`、`:oldfiles`、`:registers`、`:set`。只有普通消息会被过滤，错误消息不会。

### `:sil[ent][!] {command}`

静默执行 `{command}`。普通消息不会给出，也不会加入消息历史。添加 `[!]` 时，错误消息也会被跳过，检测到错误时命令和映射不会中止。`v:errmsg` 仍会被设置。未使用 `[!]` 时，错误消息会导致后续消息正常显示。用 `:redir` 启动的重定向会照常继续，尽管可能有细微差异。这允许在不屏幕上看到的情况下重定向命令输出。示例：

```vim
:redir >/tmp/foobar
:silent g/Aap/p
:redir END
```

要静默执行普通模式命令，请使用 `:normal` 命令。例如，搜索字符串且不显示消息：

```vim
:silent exe "normal /path\<CR>"
```

`:silent!` 适用于执行可能失败但希望忽略失败的命令。示例：

```vim
:let v:errmsg = ""
:silent! /^begin
:if v:errmsg != ""
: ... pattern was not found
```

`:silent` 还会避免 `hit-enter` 提示。对外部命令使用它时，可能导致屏幕混乱。然后使用 `CTRL-L` 清理。

`:silent menu ...` 定义一个不会回显命令行命令的菜单。命令仍会产生消息。可在命令本身使用 `:silent` 避免这一点：`:silent menu .... :silent command`。

### `:uns[ilent] {command}`

非静默执行 `{command}`。仅当使用 `:silent` 到达此命令时才有区别。使用它可以在使用 `:silent` 时仍给出消息。在此示例中，`:silent` 用于避免读取文件的消息，`:unsilent` 用于列出每个文件的第一行：

```vim
:silent argdo unsilent echo expand('%') .. ": " .. getline(1)
```

### `:[count]verb[ose] {command}`

以设置为 `[count]` 的 `'verbose'` 执行 `{command}`。如果省略 `[count]`，则使用 1。`:0verbose` 可用于将 `'verbose'` 设置为零。额外使用 `:silent` 会生成消息但不显示。`:silent` 和 `:verbose` 的组合可用于生成消息并用 `v:statusmsg` 等检查它们。例如：

```vim
:let v:statusmsg = ""
:silent verbose runtime foobar.vim
:if v:statusmsg != ""
:  " foobar.vim could not be found
:endif
```

连接另一个命令时，`:verbose` 只应用于第一个命令：

```text
:4verbose set verbose | set verbose
  verbose=4
  verbose=0
```

要将 verbose 消息记录到文件，请使用 `'verbosefile'` 选项。

#### `:verbose-cmd`

当 `'verbose'` 非零时，列出 Vim 选项、键映射、缩写、用户定义函数、命令、高亮组或自动命令的值时，还会显示它最后定义的位置。如果是手动定义的，则不会有 `Last set` 消息。如果是在执行函数、用户命令或自动命令时定义的，则会报告定义它所在的脚本。

{未编译 `+eval` 功能时不可用}

### `K`

运行程序查找光标下的关键字。程序名称由 `'keywordprg'`（kp）选项给出（默认是 `man`）。关键字由字母、数字和 `'iskeyword'` 中的字符组成。使用光标下或右侧的关键字。也可以使用命令：

```vim
:!{program} {keyword}
```

Vim 的 tools 目录中有一个可用的示例程序。它名为 `ref`，会进行简单的拼写检查。特殊情况：

- 如果 `'keywordprg'` 以 `:` 开头，则将其作为 Vim Ex 命令并带 `[count]` 调用。
- 如果 `'keywordprg'` 为空，则使用 `:help` 命令。此时最好在 `'iskeyword'` 中包含更多字符，以便找到更多帮助。
- 当 `'keywordprg'` 等于 `man` 或以 `:` 开头时，`K` 前的 `[count]` 会插入到 keywordprg 之后、关键字之前。例如，当光标位于 `mkdir` 上时使用 `2K`，结果为：

```text
!man 2 mkdir
```

- 当 `'keywordprg'` 等于 `man -s` 时，`K` 前的计数会插入到 `-s` 之后。如果没有计数，则移除 `-s`。

### `{Visual}K`

类似 `K`，但使用可视高亮的文本作为关键字。仅当高亮文本不超过一行时有效。

### `[N]gs`  
### `:[N]sl[eep] [N][m]`

什么都不做，持续 `[N]` 秒。包含 `[m]` 时，睡眠 `[N]` 毫秒。`gs` 的计数始终使用秒。默认是一秒。

```vim
:sleep       " sleep for one second
:5sleep      " sleep for five seconds
:sleep 100m  " sleep for 100 milliseconds
10gs         " sleep for ten seconds
```

可用 `CTRL-C` 中断（MS-Windows 上为 `CTRL-Break`）。`gs` 代表 `goto sleep`。睡眠期间，如果光标位于可见位置，则会定位在文本中。排队消息和定时器（`+timers`）也会在睡眠期间处理。

### `:[N]sl[eep]! [N][m]`

同上，但隐藏光标。

### `:xr[estore] [display]`

重新初始化与 X11 服务器的连接。在 X 服务器重启后有用，例如在 screen/tmux 中长时间运行 Vim 并从不同机器连接时。`[display]` 应采用 `$DISPLAY` 环境变量的格式（例如 `localhost:10.0`）。如果省略 `[display]`，则使用上次执行此命令时所用的相同值重新初始化与 X11 服务器的连接。如果从未指定过该值，则使用 Vim 启动时的 `$DISPLAY` 环境变量值。这也会更新 `v:clipmethod`。

{仅在使用 `+xterm_clipboard` 功能编译时可用}

### `:clip[reset]`

尝试使用 `'clipmethod'` 选项选择新的剪贴板访问方法。当当前方法变得不可用，而你想尝试另一种方法时很有用。

{仅在使用 `+clipboard` 功能编译时可用}

### `g CTRL-A`

仅当 Vim 编译时定义了 `MEM_PROFILING`（非常罕见）时：打印内存使用统计。仅对调试 Vim 有用。可视模式中的递增请参见 `v_g_CTRL-A`。

---

## 2. 像 `less` 或 `more` 一样使用 Vim

如果你使用 `less` 或 `more` 程序查看文件，就无法获得语法高亮。因此你可能想改用 Vim。可以通过使用 shell 脚本 `$VIMRUNTIME/macros/less.sh` 来实现。

该 shell 脚本使用 Vim 脚本 `$VIMRUNTIME/macros/less.vim`。它设置映射以模拟 `less` 支持的命令。除此之外，你仍然可以使用 Vim 命令。

这并不完美。例如，查看短文件时 Vim 仍会使用整个屏幕。但对大多数用途来说已经足够好，而且你能获得语法高亮。

`h` 键会给你可用命令的简短概览。

如果你希望在使用 less 时以不同方式设置选项，请在 vimrc 中定义 `LessInitFunc`，例如：

```vim
func LessInitFunc()
  set nocursorcolumn nocursorline
endfunc
```

```vim
vim:tw=78:ts=8:noet:ft=help:norl:
```