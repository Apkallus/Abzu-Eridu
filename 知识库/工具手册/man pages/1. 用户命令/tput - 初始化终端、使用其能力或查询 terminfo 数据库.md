https://man7.org/linux/man-pages/man1/tput.1.html

# `tput` - 初始化终端、使用其能力或查询 `terminfo` 数据库

## SYNOPSIS

```sh
tput [-v] [-T terminal-type] {cap-code [parameter ...]} ...

tput [-v] [-T terminal-type] [-x] clear

tput [-v] [-T terminal-type] init

tput [-v] [-T terminal-type] reset

tput [-v] [-T terminal-type] longname

tput [-v] -S

tput [-v] -V
```

## DESCRIPTION

`tput` 使用 `terminfo` 库和数据库，使终端特定的能力和信息可供 shell 使用，用于初始化或重置终端，或者报告当前（或指定）终端类型的描述。终端能力通过 `cap-code` 访问。

`terminfo(5)` 详细讨论了终端能力，并给出了标准化 `cap-code` 的完整列表。`user_caps(5)` 介绍了其他广泛使用但非标准的能力。

检索能力值时，结果取决于能力的类型。

- `Boolean`  
    ​`tput` 在终端具有 `cap-code` 时将退出状态设为 `0`，否则设为 `1`。

- `numeric`  
    ​`tput` 若已定义，则将 `cap-code` 的十进制值写入标准输出流（若未定义则为 `-1`），后跟一个换行。

- `string`  
    ​`tput` 若已定义，则将 `cap-code` 的值写入标准输出流，不附加尾随换行。

在应用程序使用标准输出返回的值之前，应检查 `tput` 的退出状态以确保其为 `0`；见下文“EXIT STATUS”一节。

### 操作数

通常，操作数是 `cap-code`、终端数据库中的能力代码，或该能力的参数。另外三种操作数由 `tput` 特别识别：`init`、`reset` 和 `longname`。尽管它们看起来像能力代码，但实际上会接受特殊处理；我们称它们为“伪能力”。

#### `cap-code`

表示终端数据库中的一项能力。

如果 `cap-code` 是 string 类型并接受参数，则 `tput` 将 `cap-code` 后面的参数解释为该能力的参数，直到该能力所需的（固定）数量为止。

大多数参数是 numeric。只有少数终端能力需要 string 参数；`tput` 使用一张表来决定哪些参数作为 string 传递。通常 `tput` 使用 `tparm(3X)` 执行替换。如果没有为该能力提供参数，`tput` 会写出字符串而不执行替换。

#### `init`

初始化终端。如果终端数据库存在，并且存在用户终端类型的条目，则会发生以下操作。

1. `tput` 检索终端的模式设置。它依次测试与以下对象对应的文件描述符：

    - 标准错误流，

    - 标准输出流，

    - 标准输入流，以及

    - `/dev/tty`

    以获取终端设置。检索到这些设置后，`tput` 会记住用于后续更新的是哪个描述符。

2. 如果无法从操作系统获得终端尺寸，但环境或终端类型数据库条目描述了这些尺寸，则 `tput` 会更新操作系统对终端尺寸的认知。

3. `tput` 更新终端模式。

    - 根据条目中的规范开启或关闭制表符扩展，并且

    - 如果制表符不展开，则设置标准制表位（每 8 个空格）。

4. 如果存在初始化能力（详见 `terminfo(5)` 的“Tabs and Initialization”小节），`tput` 会将它们写入标准输出流。

5. `tput` 刷新标准输出流。

如果条目缺少上述某项活动所需的信息，则该活动会被静默跳过。

#### `reset`

重新初始化终端。重置与初始化的区别有两点。

1. `tput` 将终端模式设置为“正常”状态，

    - 启用规范（“cooked”）和回显模式，

    - 禁用 cbreak 和 raw 模式，

    - 启用换行转换，并且

    - 将任何特殊输入字符设置为默认值。

2. 如果为该终端类型定义了任何重置能力，`tput` 会将它们写入输出流。否则，`tput` 会使用任何已定义的初始化能力。重置能力详见 `terminfo(5)` 的“Tabs and Initialization”小节。

#### `longname`

`terminfo` 条目以一个或多个名称开头，应用程序可通过这些名称引用该条目，之后是终端能力列表。名称之间用 `|` 字符分隔。X/Open Curses 将最后一个名称称为“长名称”，并指出它可以包含空格。

`tic` 会在最后一个名称不包含空格时发出警告，以兼容那些将长名称视为可选特性的旧 `terminfo` 条目。长名称通常称为描述字段。

如果终端数据库存在，并且存在用户终端类型的条目，`tput` 会将其描述报告到标准输出流，不附加尾随换行。参见 `terminfo(5)`。

> **注意**：将 `tput init` 或 `tput reset` 的输出重定向到文件只会捕获其部分操作。对终端模式的更改不受文件描述符重定向影响，因为终端模式是通过 `ioctl(2)` 修改的。

### 别名

如果通过名为 `clear`、`init` 或 `reset` 的链接调用 `tput`，则它的行为就如同使用相应的（伪）能力操作数运行一样。例如，执行一个指向 `tput` 的名为 `reset` 的链接，效果等同于 `tput reset`。

此特性由 `ncurses` 5.2 于 2000 年引入。它很少使用。

- `clear`  
    是一个单独程序，它更小且更常被执行。

- `init`  
    与另一个广泛使用的程序同名。

- `reset`  
    由 `tset(1)` 工具提供（也通过名为 `reset` 的链接提供）。

### 终端大小

除了伪能力（例如 `init`）之外，`tput` 还会特殊处理 `lines` 和 `cols` 这两个 `cap-code`：它可能调用 `setupterm(3X)` 来获取终端大小。

- 首先，`tput` 尝试从终端数据库获取这些能力。对于终端模拟器，这通常会失败，因为它们没有固定窗口大小，因而省略了这些能力。

- 然后，它向操作系统询问终端大小；这通常有效，除非连接是通过不支持“NAWS”（窗口大小协商）的串行线路。

- 最后，它检查环境变量 `LINES` 和 `COLUMNS`，它们可能覆盖终端大小。

如果给出了 `-T` 选项，`tput` 会通过调用 `use_tioctl(TRUE)` 忽略环境变量，转而依赖操作系统（或最终依赖终端数据库）。

## OPTIONS

- `-S`  
    每次调用 `tput` 检索多个能力。能力必须从标准输入流而不是命令行传递给 `tput`（见下文“EXAMPLES”一节）。每行只允许一个 `cap-code`。`-S` 选项会改变退出状态 `0` 和 `1` 的含义（见下文“EXIT STATUS”一节）。

    有些能力使用 string 参数而不是 numeric 参数。`tput` 使用内置表以及输入中是否存在参数来决定如何解释它们，以及是否使用 `tparm(3X)`。

- `-T type`  
    指示终端的 `type`。通常不需要此选项，因为默认值取自 `TERM` 环境变量。如果指定了此选项，则也会忽略环境变量 `LINES` 和 `COLUMNS`。

- `-v`  
    使 `tput` 以详细模式运行，报告警告。

- `-V`  
    报告与 `tput` 关联的 `ncurses` 版本，并以成功状态退出。

- `-x`  
    阻止 `tput clear` 尝试清除回滚缓冲区。

## EXIT STATUS

通常，应按如下方式解释 `tput` 的退出状态。

状态，未指定 `-S` 时的含义

- `0`  
    Boolean 或 string 能力存在

- `1`  
    Boolean 或 numeric 能力不存在

- `2`  
    用法错误或未指定终端类型

- `3`  
    无法识别的终端类型

- `4`  
    无法识别的能力代码

- `>4`  
    系统错误（`4 + errno`）

使用 `-S` 选项时，某些状态的含义会改变。

状态，指定 `-S` 时的含义

- `0`  
    所有操作数均已解释

- `1`  
    未使用

- `4`  
    某些操作数未解释

## ENVIRONMENT

如果未指定 `-T` 选项，`tput` 最多读取三个环境变量。

- `COLUMNS`  
    指定屏幕宽度（字符数）。

- `LINES`  
    指定屏幕高度（字符数）。

- `TERM`  
    表示终端类型。每种终端类型都不同，尽管许多类型相似。

## FILES

- `datadir/tabset`  
    制表位初始化数据库

- `terminfo`  
    编译后的终端描述数据库

## PORTABILITY

长期以来，`ncurses` 的 `tput` 与 System V 的 `tput` 在两个重要方面有所不同，其中一个如今基本只具有历史意义。

- `tput cap-code` 会写入标准输出，而标准输出不必是终端设备。不过，用于操作终端模式的操作数可能不会使用标准输出。

    System V `tput` 的 `init` 和 `reset` 操作数使用来自 4.1cBSD `tset` 的逻辑，操作终端模式。它会像现在的 `ncurses` 那样，检查相同的文件描述符（以及 `/dev/tty`）是否关联到终端设备；如果都没有，最后假定为 1200 波特终端。更新终端模式时，它会忽略错误。

    在 `ncurses` 6.1 之前（见下文“HISTORY”一节），`tput` 不修改终端模式。现在它采用与 System V 类似的方案，使用与 `tset` 共享的函数（最终基于 4.4BSD `tset`）。如果它无法打开终端（例如由 `cron(1)` 运行时），`tput` 会以错误状态退出。

- System V `tput` 假定：如果 `cap-code` 操作数值的所有字符都是十进制数字，则其类型为 numeric；否则将 `cap-code` 视为 string 能力。

    大多数支持 `cap-code` 操作数的实现都使用 `tparm(3X)` 函数展开其参数。该函数期望 numeric 和 string 参数混合，因此要求 `tput` 知道应使用哪种类型。

    `ncurses` 的 `tput` 使用一张表来确定标准 `cap-code` 操作数的参数类型，并使用一个内部函数分析非标准 `cap-code` 操作数。

    虽然这比 System V 的工具更可靠，但这种分析引入了可移植性问题。一位 OpenBSD 开发者改编了 `ncurses` 的内部库函数，将 NetBSD 基于 `termcap` 的 `tput` 移植到 `terminfo`，并修改它以便在命令行上解释多个 `cap-code`（和参数）。可移植应用程序不应依赖此特性；`ncurses` 提供它是为了支持专门为 OpenBSD 编写的应用程序。

与其他实现不同，`ncurses` 的 `tput` 实现如果编译时包含 `termcap` 支持，则同时接受 `termcap` 和 `terminfo` 的 `cap-code`。但在这种情况下，`termcap` 和 `terminfo` 代码有两种歧义；`ncurses` 假定为 `terminfo` 代码。

- `cap-code` `dl` 在 `termcap` 中表示 `delete_line`，但在 `terminfo` 中表示 `parm_delete_line`。`termcap` 使用代码 `DL` 表示 `parm_delete_line`。`terminfo` 使用代码 `dl1` 表示 `delete_line`。

- `cap-code` `ed` 在 `termcap` 中表示 `exit_delete_mode`，但在 `terminfo` 中表示 `clr_eos`。`termcap` 使用代码 `cd` 表示 `clr_eos`。`terminfo` 使用代码 `rmdc` 表示 `exit_delete_mode`。

`longname` 操作数、`-S` 选项以及下面 `cup` 示例中使用的参数替换特性，在 SVr4（1989）之前的 AT&T/USL `curses` 中不受支持。后来，4.3BSD-Reno（1990）增加了对 `longname` 的支持，1994 年 NetBSD 增加了对参数替换特性的支持。

IEEE Std 1003.1/The Open Group Base Specifications Issue 7（POSIX.1-2008）只记录了 `clear`、`init` 和 `reset` 操作数。从这一选择中可以得出一些有趣的观察。

- `ncurses` 支持 `clear`，就像支持任何其他标准 `cap-code` 一样。其他项（`init` 和 `longname`）不对应终端能力。

- 在基于 SVr4 的系统（如 Solaris、IRIX64 和 HP-UX）以及其他系统（如 AIX 和 Tru64）上，`tput` 也支持标准 `cap-code` 操作数。

- 少数平台（如 FreeBSD）在其各自的 `tput` 命令中识别 `termcap` 代码而不是 `terminfo` 能力代码。自 2010 年起，NetBSD 的 `tput` 使用 `terminfo` 代码。在此之前，它（像 FreeBSD 一样）识别 `termcap` 代码。

    从 2021 年开始，FreeBSD 使用 `ncurses` 的 `tput`，并配置为同时支持 `terminfo`（先测试）和 `termcap`（作为回退）。

由于（显然）所有认证的 Unix 系统都支持完整的能力代码集，只记录少数几个的原因可能并不明显。

- X/Open Curses Issue 7 对 `tput` 的记录方式不同，包含 `cap-code` 以及本实现中使用的其他特性。

- 也就是说，`tput` 有两个标准：POSIX（子集）和 X/Open Curses（完整实现）。POSIX 记录一个子集，以避免引入 X/Open Curses 和终端能力数据库的复杂性。

- 虽然完全可以在不使用 `curses` 的情况下编写 `tput` 程序，但没有任何带有 `curses` 实现的系统会提供一个不支持标准 `cap-codes` 的 `tput` 工具。

X/Open Curses Issue 7（2009）是第一个记录这些工具的版本。然而，X/Open Curses 的这一部分并未遵循既有实践（即 System V `curses` 行为）。

- 它将“无效操作数”的退出状态指定为 4，这可能与“未知能力”含义相同。例如，Solaris `xcurses` 的源代码在这种情况下使用术语“invalid”。

- 它将未在 `terminfo` 数据库中指定的 numeric 变量的退出状态指定为 255。这很可能是文档错误，将写入标准输出以表示缺失或取消的 numeric 能力的“-1”误认为（无符号）退出状态。

各种 System V 实现（AIX、HP-UX、Solaris）使用与 `ncurses` 相同的退出状态。

NetBSD `curses` 记录的退出状态既不 correspond to `ncurses`，也不对应 X/Open Curses。

## HISTORY

Bill Joy 于 1980 年 10 月在 4BSD 开发期间编写了一个 `tput` 命令。这个初始版本只清除屏幕，并未随官方发行版发布。

System V 开发了一个不同的 `tput` 命令。

- SVr2（1984）提供了一个基本的 `tput`，它会检查参数与每个能力名称，并返回相应的值。此版本的 `tput` 未对参数化能力使用 `tparm(3X)`。

- SVr3（1987）用一个更广泛的程序取代了它，该程序对 `init` 和 `reset` 操作数的支持（超过程序的一半）融入了 Eric Allman 编写的 BSD `tset` 的 `reset` 特性。

- SVr4（1989）在其 `init` 逻辑中使用 `orig_colors`（`oc`）和 `orig_pair`（`op`）能力增加了颜色初始化。

Keith Bostic 为 4.3BSD-Reno（1990）的发布重构了 BSD `tput`，使其遵循 System V `tput` 的接口，接受一些以 `terminfo`（伪）能力命名的参数：`clear`、`init`、`longname` 和 `reset`。然而，由于他只有 `termcap` 可用，它接受 `termcap` 代码用于其他能力。此外，Bostic 的 BSD `tput` 不像早期的 BSD `tset` 那样修改终端模式。同时，Bostic 添加了一个名为“clear”的 shell 脚本，使用 `tput` 清除屏幕。这些成为 `tput` 的“现代”BSD 实现。

`ncurses` 的 `tput` 起源既不在 System V 也不在 BSD，而在 Ross Ridge 的 `mytinfo` 包中，该包于 1992 年 12 月发布在 `comp.sources.unix` 上。Ridge 的程序比 BSD 程序更精细地使用了终端能力。Eric Raymond 于 1995 年 6 月在 `ncurses` 中使用了该 `tput` 程序（以及 `mytinfo` 的其他部分）。Raymond 几乎未加修改地融入了处理终端能力的部分，并改进了命令行参数的处理方式。

在 `ncurses` 6.1（2018）之前，其 `tset` 和 `tput` 工具有所不同。

- `tset` 更有效，会重置终端的模式和特殊输入字符。

- 另一方面，`tset` 用于重置终端的终端能力集合更有限；它只有 `reset_1string`（`rs1`）、`reset_2string`（`rs2`）和 `reset_file`（`rf`）的等价物，而没有 `tput` 的制表位和边距更新功能。

`reset` 程序传统上是 `tset` 的别名，因为它能够重置终端的模式和特殊输入字符。

从 `ncurses` 6.1 起，两个程序的“reset”特性（大部分）相同。仍存在两个细微差异。

- 发出重置时，`tset` 程序会检查设备是否看起来像伪终端（终端模拟器程序可能使用这种终端），如果不像，则等待一秒，以防它正在与硬件终端通信。

- 两个程序将终端初始化字符串写入不同的流；即 `tset` 写入标准错误，`tput` 写入标准输出。

## EXAMPLES

- 
    ```sh
    tput init
    ```
    根据 `TERM` 环境变量中的终端类型初始化终端。如果系统在登录时不能可靠地初始化终端，可以在导出 `TERM` 环境变量后，将此命令加入 `$HOME/.profile`。

- 
    ```sh
    tput -T5620 reset
    ```
    重置 AT&T 5620 终端，覆盖 `TERM` 环境变量中的终端类型。

- 
    ```sh
    tput cnorm
    ```
    将光标设置为正常可见性。

- 
    ```sh
    tput home
    ```
    将光标移到第 0 行、第 0 列：屏幕左上角，通常称为“home”光标位置。

- 
    ```sh
    tput clear
    ```
    清除屏幕：将 `clear_screen` 能力的值写入标准输出流。

- 
    ```sh
    tput cols
    ```
    报告当前终端类型使用的列数。

- 
    ```sh
    tput -Tadm3a cols
    ```
    报告 ADM-3A 终端使用的列数。

- 
    ```sh
    strong=`tput smso` normal=`tput rmso`
    ```
    将能力值设置到 shell 变量：`strong` 和 `normal`，分别用于开始和结束终端的突出显示模式。可以用它们来显示提示符。

    ```sh
    printf "${strong}Username:${normal} "
    ```

- 
    ```sh
    tput hc
    ```
    通过退出状态指示终端是否为硬拷贝设备。

- 
    ```sh
    tput cup 23 4
    ```
    将光标移到第 23 行、第 4 列。

- 
    ```sh
    tput cup
    ```
    报告 `cursor_address`（`cup`）能力（用于光标移动）的值，不替换参数。

- 
    ```sh
    tput longname
    ```
    报告 `terminfo` 数据库对 `TERM` 环境变量所指定终端类型的描述。

- 
    ```sh
    tput -S
    ```
    处理多个能力。`-S` 选项可以有效地与 shell “here document” 一起使用。

    ```console
    $ tput -S <<!
    > clear
    > cup 10 10
    > bold
    > !
    ```

    上述命令清除屏幕，将光标移到位置 `(10, 10)`，并开启粗体（额外亮度）模式。

- 
    ```sh
    tput clear cup 10 10 bold
    ```
    执行与上面的 `tput -S` 示例相同的操作。

## SEE ALSO

`clear(1)`、`stty(1)`、`tabs(1)`、`tset(1)`、`curs_termcap(3X)`、`terminfo(5)`、`user_caps(5)`

## COLOPHON

本页是 `ncurses`（new curses）项目的一部分。项目信息可在以下地址找到：

<https://invisible-island.net/ncurses/ncurses.html>

如果你对本手册页有错误报告，请发送至 `bug-ncurses@gnu.org`。本页取自 2026-08-04 从以下地址获取的 `ncurses-6.6.tar.gz` 压缩包：

<https://ftp.gnu.org/gnu/ncurses/>

如果你发现本 HTML 版本页面存在渲染问题，或者认为有更好或更最新的页面来源，或者对 COLOPHON 中的信息（该部分 *不是* 原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

*ncurses @NCURSES_MAJOR@.@NCU... 2025-11-11 `tput(1)`*