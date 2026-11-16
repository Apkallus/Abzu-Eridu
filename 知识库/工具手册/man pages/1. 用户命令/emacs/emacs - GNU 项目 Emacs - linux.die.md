https://linux.die.net/man/1/emacs

# emacs(1) - Linux 手册页

## 名称

`emacs` - GNU 项目 Emacs

## 概要

```sh
emacs [ 命令行开关 ] [ 文件 ... ]
```

## 描述

`GNU Emacs` 是 `Emacs` 的一个版本，由原始（PDP-10）`Emacs` 的作者 Richard Stallman 编写。

GNU Emacs 的主要文档位于 GNU Emacs 手册中，你可以通过 `Info` 阅读，既可以从 Emacs 内阅读，也可以作为独立程序阅读。请在那里查找完整且最新的文档。本手册页仅在有人自愿更新时才会更新；Emacs 维护者的优先目标是尽量减少本手册页从其他更有用项目上占用的时间。

GNU Emacs 的用户功能涵盖其他 `Emacs` 编辑器所做的一切，并且由于它的编辑命令用 Lisp 编写，因此易于扩展。

`Emacs` 具有广泛的交互式帮助设施，但该设施假定你知道如何操作 `Emacs` 窗口和缓冲区。`CTRL-h` 或 `F1` 进入帮助设施。帮助教程（`CTRL-h t`）会启动一个交互式教程，可以在几分钟内教会初学者 `Emacs` 的基础知识。帮助 Apropos（`CTRL-h a`）可帮助你根据功能查找命令，帮助字符（`CTRL-h c`）描述给定字符的效果，帮助函数（`CTRL-h f`）描述按名称指定的给定 Lisp 函数。

`Emacs` 的撤销功能可以撤销对缓冲区的多步修改，因此很容易从编辑错误中恢复。

`GNU Emacs` 的许多特殊包处理邮件读取（`RMail`）和发送（`Mail`）、大纲编辑（`Outline`）、编译（`Compile`）、在 `Emacs` 窗口中运行子 shell（`Shell`）、运行 Lisp 读取-求值-打印循环（`Lisp-Interaction-Mode`）、自动心理治疗（`Doctor`）等等。

有一本详尽的参考手册，但其他 Emacses 的用户即使没有副本也应该不难适应。刚接触 `Emacs` 的用户通过研究教程并使用自文档功能，将能够相当快地使用基本功能。

### Emacs 选项

以下选项具有普遍意义：

- `file`  
    编辑 `file`。

- `--file file`、`--find-file file`、`--visit file`  
    与直接将 `file` 作为参数指定相同。

- `+number`  
    转到由 `number` 指定的行（不要在 `+` 号和数字之间插入空格）。这仅适用于下一个指定的文件。

- `+line:column`  
    转到指定的 `line` 和 `column`。

- `-q`、`--no-init-file`  
    不加载初始化文件。

- `--no-site-file`  
    不加载站点范围的启动文件。

- `--no-desktop`  
    不加载已保存的桌面。

- `-nl`、`--no-shared-memory`  
    不使用共享内存。

- `-Q`、`--quick`  
    等同于 `-q --no-site-file --no-splash`。

- `--no-splash`  
    启动时不显示启动画面。

- `--debug-init`  
    在处理用户初始化文件 `~/.emacs` 期间启用 `Emacs` Lisp 调试器。这对于调试初始化文件中的问题很有用。

- `-u user`、`--user user`  
    加载 `user` 的初始化文件。

- `-t file`、`--terminal file`  
    使用指定的 `file` 作为终端，而不是使用 stdin/stdout。这必须是命令行中指定的第一个参数。

- `--multibyte`、`--no-unibyte`  
    启用多字节模式（默认启用）。

- `--unibyte`、`--no-multibyte`  
    启用单字节模式。

- `--version`  
    显示 `Emacs` 版本信息并退出。

- `--help`  
    显示此帮助并退出。

以下选项面向 Lisp（这些选项按遇到的顺序处理）：

- `-f function`、`--funcall function`  
    执行 Lisp 函数 `function`。

- `-l file`、`--load file`  
    加载 `file` 中的 Lisp 代码。

- `--eval expr`、`--execute expr`  
    求值 Lisp 表达式 `expr`。

以下选项在以批处理编辑器运行 `Emacs` 时有用：

- `--batch`  
    以批处理模式编辑。编辑器将向 stderr 发送消息。此选项必须是参数列表中的第一个。你必须使用 `-l` 和 `-f` 选项来指定要执行的文件和要调用的函数。

- `--script file`  
    将 `file` 作为 Emacs Lisp 脚本运行。

- `--insert file`  
    将 `file` 的内容插入当前缓冲区。

- `--kill`  
    在批处理模式下退出 `Emacs`。

- `-L dir`、`--directory dir`  
    将 `dir` 添加到 `Emacs` 搜索 Lisp 文件的目录列表中。

### 在 X 下使用 Emacs

`Emacs` 已经过调整，可以与 X 窗口系统良好配合。如果你在 X 窗口下运行 `Emacs`，它会创建自己的 X 窗口用于显示。你可能希望将编辑器作为后台进程启动，以便可以继续使用原来的窗口。

`Emacs` 可以使用以下 X 开关启动：

- `--name name`  
    指定应分配给初始 `Emacs` 窗口的名称。这控制 X 资源查找以及窗口标题。

- `-T name`、`--title name`  
    指定初始 X 窗口的标题。

- `-r`、`-rv`、`--reverse-video`  
    以反色显示 `Emacs` 窗口。

- `-fn font`、`--font font`  
    将 `Emacs` 窗口的字体设置为 `font` 指定的字体。你可以在 `/usr/lib/X11/fonts` 目录中找到各种 `X` 字体。注意 `Emacs` 只接受等宽字体。在 X11 Release 4 字体命名约定下，字体名称第十一个字段中值为 “m” 或 “c” 的任何字体都是等宽字体。此外，名称形式为 `width`x`height` 的字体通常是等宽的，字体 `fixed` 也是如此。更多信息请参见 `xlsfonts(1)`。

    指定字体时，请确保在开关和字体名称之间放置一个空格。

- `--xrm resources`  
    设置额外的 X 资源。

- `--color`、`--color=mode`  
    覆盖字符终端的颜色模式；`mode` 默认为 `'auto'`，也可以是 `'never'`、`'auto'`、`'always'`，或像 `'ansi8'` 这样的模式名。

- `-bw pixels`、`--border-width pixels`  
    将 `Emacs` 窗口的边框宽度设置为 `pixels` 指定的像素数。默认为窗口每边一像素。

- `-ib pixels`、`--internal-border pixels`  
    将窗口的内部边框宽度设置为 `pixels` 指定的像素数。默认为窗口每边一像素的内边距。

- `-g geometry`、`--geometry geometry`  
    按指定设置 `Emacs` 窗口的宽度、高度和位置。几何规格采用标准 X 格式；更多信息请参见 `x(7)`。宽度和高度以字符为单位指定；默认是 80x24。有关窗口大小与选择或取消选择工具栏和菜单栏如何交互的信息，请参见 Emacs 手册中的 “Options for Window Size and Position” 一节。

- `-lsp pixels`、`--line-spacing pixels`  
    在行之间增加额外空间。

- `-vb`、`--vertical-scroll-bars`  
    启用垂直滚动条。

- `-fh`、`--fullheight`  
    使第一帧与屏幕一样高。

- `-fs`、`--fullscreen`  
    使第一帧全屏。

- `-fw`、`--fullwidth`  
    使第一帧与屏幕一样宽。

- `-fg color`、`--foreground-color color`  
    在彩色显示上，设置文本颜色。

    使用命令 `M-x list-colors-display` 获取有效颜色名称列表。

- `-bg color`、`--background-color color`  
    在彩色显示上，设置窗口背景颜色。

- `-bd color`、`--border-color color`  
    在彩色显示上，设置窗口边框颜色。

- `-cr color`、`--cursor-color color`  
    在彩色显示上，设置窗口文本光标的颜色。

- `-ms color`、`--mouse-color color`  
    在彩色显示上，设置窗口鼠标光标的颜色。

- `-d displayname`、`--display displayname`  
    在 `displayname` 指定的显示上创建 `Emacs` 窗口。必须是命令行中指定的第一个选项。

- `-nbi`、`--no-bitmap-icon`  
    不使用 gnu 图片作为 Emacs 图标。

- `--iconic`  
    以图标化状态启动 `Emacs`。

- `-nbc`、`--no-blinking-cursor`  
    禁用闪烁光标。

- `-nw`、`--no-window-system`  
    告诉 `Emacs` 不要使用其特殊的 X 接口。如果你从 `xterm(1)` 窗口调用 `Emacs` 时使用此开关，显示会在该窗口中完成。

- `-D`、`--basic-display`  
    此选项禁用许多显示功能；用于调试 Emacs。

你可以在 `.Xresources` 文件中为 `Emacs` 窗口设置 `X` 默认值（参见 `xrdb(1)`）。使用以下格式：

```text
emacs.keyword:value
```

其中 `value` 指定 `keyword` 的默认值。`Emacs` 允许你为以下关键字设置默认值：

- `background`（类 `Background`）  
    对于彩色显示，设置窗口的背景颜色。

- `bitmapIcon`（类 `BitmapIcon`）  
    如果 `bitmapIcon` 的值设置为 `on`，窗口将图标化为 “kitchen sink”。

- `borderColor`（类 `BorderColor`）  
    对于彩色显示，设置窗口边框的颜色。

- `borderWidth`（类 `BorderWidth`）  
    以像素为单位设置窗口的边框宽度。

- `cursorColor`（类 `Foreground`）  
    对于彩色显示，设置窗口文本光标的颜色。

- `cursorBlink`（类 `CursorBlink`）  
    指定是否使光标闪烁。默认是 `on`。使用 `off` 或 `false` 关闭光标闪烁。

- `font`（类 `Font`）  
    设置窗口的文本字体。

- `foreground`（类 `Foreground`）  
    对于彩色显示，设置窗口的文本颜色。

- `fullscreen`（类 `Fullscreen`）  
    所需的全屏大小。值可以是 `fullboth`、`fullwidth` 或 `fullheight` 之一，分别对应命令行选项 `-fs`、`-fw` 和 `-fh`。注意这仅适用于初始帧。

- `geometry`（类 `Geometry`）  
    设置 `Emacs` 窗口的几何规格（如上所述）。

- `iconName`（类 `Title`）  
    设置 `Emacs` 窗口图标的图标名称。

- `internalBorder`（类 `BorderWidth`）  
    以像素为单位设置窗口的内部边框宽度。

- `lineSpacing`（类 `LineSpacing`）  
    行之间的额外空间（“leading”），以像素为单位。

- `menuBar`（类 `MenuBar`）  
    如果为 `on`，则为帧提供菜单栏；如果为 `off`，则没有菜单栏。有关如果有菜单栏时如何控制其外观，请参见 Emacs 手册中的 “Lucid Resources” 和 “LessTif Resources” 一节。

- `minibuffer`（类 `Minibuffer`）  
    如果为 `none`，则在此帧中不创建 minibuffer。它将改为使用单独的 minibuffer 帧。

- `paneFont`（类 `Font`）  
    非 toolkit 版本 `Emacs` 中菜单窗格标题的字体名称。

- `pointerColor`（类 `Foreground`）  
    对于彩色显示，设置窗口鼠标光标的颜色。

- `privateColormap`（类 `PrivateColormap`）  
    如果为 `on`，在 “default visual” 为 `PseudoColor` 类且 `Emacs` 正在使用它的情况下，使用私有颜色映射。

- `reverseVideo`（类 `ReverseVideo`）  
    如果 `reverseVideo` 的值设置为 `on`，窗口将以反色显示。

- `screenGamma`（类 `ScreenGamma`）  
    颜色的 gamma 校正，等同于帧参数 `'screen-gamma'`。

- `scrollBarWidth`（类 `ScrollBarWidth`）  
    滚动条宽度，以像素为单位，等同于帧参数 `'scroll-bar-width'`。

- `selectionFont`（类 `SelectionFont`）  
    非 toolkit 版本 `Emacs` 中弹出菜单项的字体名称。（对于 toolkit 版本，请参见 Emacs 手册中的 “Lucid Resources” 和 “LessTif Resources” 一节。）

- `selectionTimeout`（类 `SelectionTimeout`）  
    等待选择回复的毫秒数。值为 0 表示尽可能长时间等待。

- `synchronous`（类 `Synchronous`）  
    如果为 `on`，则以同步模式运行 Emacs。同步模式对于调试 X 问题很有用。

- `title`（类 `Title`）  
    设置 `Emacs` 窗口的标题。

- `toolBar`（类 `ToolBar`）  
    为工具栏保留的行数。

- `useXIM`（类 `UseXIM`）  
    如果为 `false` 或 `off`，则关闭 X 输入法（XIM）的使用。

- `verticalScrollBars`（类 `ScrollBars`）  
    如果为 `on`，则为帧提供滚动条；如果为 `off`，则抑制滚动条。

- `visualClass`（类 `VisualClass`）  
    指定 X 应使用的 “visual”。这告诉 X 如何处理颜色。值应以 `TrueColor`、`PseudoColor`、`DirectColor`、`StaticColor`、`GrayScale` 和 `StaticGray` 之一开头，后跟 `-depth`，其中 `depth` 是颜色平面的数量。

如果你在黑白显示上尝试设置颜色值，窗口的特性将默认如下：前景色设置为黑色，背景色设置为白色，边框色设置为灰色，文本和鼠标光标设置为黑色。

### 使用鼠标

以下列出 X11 下 `Emacs` 窗口的一些鼠标按钮绑定。

鼠标按钮，功能

- `left`  
    设置 point。

- `middle`  
    粘贴文本。

- `right`  
    将文本剪切到 X cut buffer。

- `SHIFT-middle`  
    将文本剪切到 X cut buffer。

- `SHIFT-right`  
    粘贴文本。

- `CTRL-middle`  
    将文本剪切到 X cut buffer 并 kill 它。

- `CTRL-right`  
    选择此窗口，然后将其拆分为两个窗口。与输入 `CTRL-x 2` 相同。

- `CTRL-SHIFT-left`  
    X buffer 菜单——按住按钮和键，等待菜单出现，选择 buffer，然后释放。将鼠标移出菜单并释放以取消。

- `CTRL-SHIFT-middle`  
    X 帮助菜单——弹出 Emacs 帮助的索引卡菜单。

- `CTRL-SHIFT-right`  
    用鼠标选择窗口，并删除所有其他窗口。与输入 `CTRL-x 1` 相同。

## 手册

你可以从开发 GNU 软件的自由软件基金会订购 GNU Emacs 手册的印刷副本。有关订购信息，请参见文件 `ORDERS`。

你本地的 Emacs 维护者也可能有副本可用。与 FSF 的所有软件和出版物一样，允许所有人制作和分发 Emacs 手册的副本。手册的 TeX 源码也包含在 Emacs 源码发行版中。

## 文件

`/usr/local/share/info` -- Info 文档浏览器的文件。Emacs 参考手册的完整文本以方便的树形结构形式包含在其中。还包括 Emacs Lisp 参考手册，对任何希望用 Emacs Lisp 扩展语言编写程序的人都有用。

`/usr/local/share/emacs/$VERSION/lisp` -- 定义大多数编辑命令的 Lisp 源文件和编译文件。有些是预加载的；其他在使用时从该目录自动加载。

`/usr/local/libexec/emacs/$VERSION/$ARCH` -- 与 GNU Emacs 一起使用的各种程序。

`/usr/local/share/emacs/$VERSION/etc` -- 各种信息文件。

`/usr/local/share/emacs/$VERSION/etc/DOC.*` -- 包含 GNU Emacs 的 Lisp 原语和预加载 Lisp 函数的文档字符串。它们存储在这里以减少 Emacs 本体的体积。

`/usr/local/share/emacs/$VERSION/etc/SERVICE` 列出了提供各种服务以帮助 GNU Emacs 用户的人，包括教育、故障排除、移植和定制。

## 缺陷

有一个邮件列表 [bug-gnu-emacs@gnu.org](mailto:bug-gnu-emacs@gnu.org)，用于报告 Emacs 缺陷和修复。但在将某事报告为缺陷之前，请尽量确认它确实是缺陷，而不是误解或有意设计的功能。我们要求你阅读参考手册（或 Info 系统）末尾附近的 “Reporting Emacs Bugs” 一节，了解如何以及何时报告缺陷的提示。另外，在你发送的每一份缺陷报告中，请包含你正在运行的 Emacs 版本号。如果能被隔离，缺陷往往确实会被修复，因此以易于复现的方式报告缺陷符合你的利益。

不要期望对缺陷报告给出个人答复。报告缺陷的目的是，如果可能的话，在下一个版本中为所有人修复它们。如需个人帮助，请查看 `SERVICE` 文件（见上文）中提供帮助的人员列表。

请不要向此邮件列表发送除缺陷报告之外的任何内容。有关 Emacs 邮件列表的更多信息，请参见文件 `/usr/local/share/emacs/$VERSION/etc/MAILINGLISTS`。

## 无限制

`Emacs` 是自由的；任何人都可以根据 `Emacs` General Public License 中规定的条款，将 `Emacs` 的副本重新分发给任何人，该许可证的副本随每份 `Emacs` 副本附带，也出现在参考手册中。

`Emacs` 的副本有时可能随 Unix 系统的发行版一起打包提供，但它从不包含在任何涵盖这些系统的许可证范围内。这种包含违反了允许分发的条款。事实上，General Public License 的主要目的是禁止任何人对 `Emacs` 的再分发附加任何其他限制。

Richard Stallman 鼓励你改进和扩展 `Emacs`，并敦促你将扩展贡献给 GNU 库。最终 GNU（Gnu's Not Unix）将成为 Unix 的完整替代品。每个人都将可以自由使用、复制、研究和更改 GNU 系统。

## 另见

`emacsclient(1)`、`etags(1)`、`x(7)`、`xlsfonts(1)`、`xterm(1)`、`xrdb(1)`

## 作者

`Emacs` 由 Richard Stallman 和自由软件基金会编写。Joachim Martillo 和 Robert Krawitz 添加了 X 功能。

## 复制

Copyright © 1995, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009 Free Software Foundation, Inc.

允许制作和分发本文档的逐字副本，前提是所有副本上保留版权声明和此许可声明。

允许在逐字复制的条件下复制和分发本文档的修改版本，前提是整个由此产生的衍生作品根据与此相同的许可声明分发。

允许在修改版本的上述条件下复制和分发本文档的翻译，但此许可声明可以在自由软件基金会批准的翻译中声明。

## 被引用

`ash(1)`、`bgltags(1)`、`byobu-ctrl-a(1)`、`cdecl(1)`、`ci(1)`、`clisp(1)`、`csh(1)`、`dash(1)`、`ebrowse(1)`、`eplain(1)`、`gp(1)`、`gqview(1)`、`groff_out(5)`、`hebcal(1)`、`info(5)`、`ksh93(1)`、`lacheck(1)`、`lbdbq(1)`、`ldp(7)`、`mksh(1)`、`perldl(1)`、`powwow(6)`、`pure(1)`、`roff(7)`、`sh(1)`、`texinfo(5)`、`unzip(1)`、`xemacs(1)`、`zile(1)`