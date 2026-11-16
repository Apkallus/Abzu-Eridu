https://man7.org/linux/man-pages/man3/cbreak.3x.html

# `cbreak`、`echo`、`halfdelay`、`intrflush`、`is_cbreak`、`is_echo`、`is_nl`、`is_raw`、`keypad`、`meta`、`nl`、`nocbreak`、`nodelay`、`noecho`、`nonl`、`noqiflush`、`noraw`、`notimeout`、`qiflush`、`raw`、`timeout`、`wtimeout`、`typeahead` — 获取和设置 `curses` 终端输入选项

## 概要

```c
#include <curses.h>

int cbreak(void);
int nocbreak(void);

int echo(void);
int noecho(void);

int intrflush(WINDOW * win /* 忽略 */, bool bf);
int keypad(WINDOW * win, bool bf);
int meta(WINDOW * win /* 忽略 */, bool bf);
int nodelay(WINDOW * win, bool bf);
int notimeout(WINDOW * win, bool bf);

int nl(void);
int nonl(void);

void qiflush(void);
void noqiflush(void);

int raw(void);
int noraw(void);

int halfdelay(int tenths);
void timeout(int delay);
void wtimeout(WINDOW * win, int delay);

int typeahead(int fd);

/* 扩展 */
int is_cbreak(void);
int is_echo(void);
int is_nl(void);
int is_raw(void);
```

## 描述

`curses` 提供可配置参数，允许应用程序控制终端输入的处理。某些参数（例如影响终端 `mode` 或线路规程的参数）是全局的，适用于所有窗口；其他参数仅适用于特定窗口。库不会自动将这些参数应用到新窗口或派生窗口；应用程序必须为每个窗口配置所需行为。

下面某些描述会提到 `input character reading function`（输入字符读取函数）：在非宽字符 `curses` API 中是 `wgetch(3X)`，在宽字符 API 中是 `wget_wch(3X)`。除了 `ncurses(3X)` 中描述的这些函数的变体形式外，`curses` 函数 `wgetstr(3X)` 和 `wget_wstr(3X)` 及其自身变体也会调用相应的输入字符读取函数。

### cbreak, nocbreak

```c
int cbreak(void);
int nocbreak(void);
```

通常，终端驱动程序会缓冲输入的字符，直到输入换行或回车才将其传递给应用程序。这种规范（“cooked”）线路规程还支持软件流控制、简单的行编辑功能（字符和单词擦除，以及整行擦除或“kill”）和作业控制。`cbreak` 将终端配置为 `cbreak mode`，该模式禁用行缓冲以及擦除和 kill 字符处理——中断、退出、挂起和流控制字符不受影响——并使用户输入的字符立即可供程序使用。`nocbreak` 恢复规范（“cooked”）模式。

`curses` 应用程序启动时终端状态是未知的；因此，程序应显式调用 `cbreak` 或 `nocbreak`。大多数使用 `curses` 的交互式程序会设置 cbreak 模式。调用 `cbreak` 会覆盖 `raw`。输入字符读取函数的 man 页讨论了 `cbreak` 和 `nocbreak` 如何与 `echo` 和 `noecho` 交互。

### echo, noecho

```c
int echo(void);
int noecho(void);
```

`echo` 和 `noecho` 决定用户输入的字符在输入时是否由输入字符读取函数写入 `curses` 窗口。`curses` 始终禁用终端驱动程序自身的回显。默认情况下，`curses` 屏幕的回显选项是设置的。大多数交互式程序的作者倾向于在屏幕的受控区域自行回显，或者完全不回显，因此他们会调用 `noecho`。输入字符读取函数的 man 页讨论了 `echo` 和 `noecho` 如何与 `cbreak` 和 `nocbreak` 交互。

### halfdelay()

```c
int halfdelay(int tenths);
```

`halfdelay` 配置 `half-delay mode`，它类似于 cbreak 模式，因为用户输入的字符立即可供程序使用。然而，在阻塞 `tenths` 个十分之一秒后，如果没有待处理的输入，输入字符读取函数会返回 `ERR`。`tenths` 的值必须在 1 到 255 之间。使用 `nocbreak` 离开半延迟模式。

### intrflush()

```c
int intrflush(WINDOW * win /* 忽略 */, bool bf);
```

如果 `bf` 为 `TRUE`，`intrflush` 调用 `qiflush`（见下文）；如果 `bf` 为 `FALSE`，则调用 `noqiflush`。它忽略其 `win` 参数。

### keypad()

```c
int keypad(WINDOW * win, bool bf);
```

`keypad` 启用对终端功能键的识别。如果启用（`bf` 为 `TRUE`），则当输入字符读取函数读取到 ESC 时，它会等待与终端类型描述定义的转义序列相对应的进一步输入。如果有效序列填充了输入流，输入字符读取函数会返回表示功能键的值，例如 `KEY_LEFT`。（宽字符 API 用户：`wget_wch(3X)` 返回 `KEY_CODE_YES`，以指示其 `wch` 参数中功能键代码的可用性。）如果序列无效，输入字符读取函数只返回其最后一个字符。如果禁用（`bf` 为 `FALSE`），`curses` 不会特殊处理功能键，程序必须自行解释转义序列。如果终端类型描述定义了 `keypad_local`（`rmkx`）和 `keypad_xmit`（`smkx`）能力，启用窗口的 keypad 模式会设置终端的 keypad 为传输模式，禁用 keypad 模式会设置终端的 keypad 为本地工作。默认情况下，窗口的 keypad 模式是关闭的。

### meta()

```c
int meta(WINDOW * win /* 忽略 */, bool bf);
```

最初，终端在输入时返回 7 位还是 8 位字符代码取决于终端驱动程序的配置；在 POSIX 系统上，参见 `termios(3)`。要强制返回 8 位，调用 `meta(..., TRUE)`；在 POSIX 系统上，这等价于在终端上设置 CS8 标志。要强制返回 7 位，调用 `meta(..., FALSE)`；在 POSIX 系统上，这等价于在终端上设置 CS7 标志。`curses` 忽略窗口参数 `win`。如果为终端类型定义了 `terminfo` 字符串能力 `meta_on`（`smm`）和 `meta_off`（`rmm`），启用 meta 模式会将 `smm` 的值发送到终端，禁用则会将 `rmm` 的值发送到终端。

### nl, nonl

```c
int nl(void);
int nonl(void);
```

最初，终端在 cbreak 或 raw 模式下是否使用换行字符代码报告回车，取决于终端驱动程序的配置；参见 `termios(3)`。`nl` 配置终端执行此转换。`nonl` 禁用它。在其规范（“cooked”）线路规程下，终端驱动程序始终将回车转换为换行。

### nodelay()

```c
int nodelay(WINDOW * win, bool bf);
```

`nodelay` 将窗口 `win` 的输入字符读取函数配置为非阻塞。如果没有准备好的输入，读取函数返回 `ERR`。如果禁用（`bf` 为 `FALSE`），读取函数在获得输入之前不会返回。

### notimeout()

```c
int notimeout(WINDOW * win, bool bf);
```

当对窗口调用了 `keypad`，并且输入字符读取函数从该窗口读取到 ESC 字符时，`curses` 会在等待下一个字符时设置一个定时器。如果定时器超时，`curses` 会将 ESC 解释为显式按下终端的 Escape 键（或等效操作）。`notimeout(win, TRUE)` 禁用此定时器。超时的目的是区分功能键产生的序列和用户键入的序列。如果禁用此定时器，`curses` 会永远等待后续击键，直到确定转义序列有效或无效。

### qiflush, noqiflush

```c
void qiflush(void);
void noqiflush(void);
```

在 POSIX 系统上，在规范（“cooked”）或 cbreak 线路规程下，`qiflush` 和 `noqiflush` 配置终端驱动程序在处理中断、挂起或退出字符时对其输入和输出队列的处理方式；参见 `termios(3)`。默认行为继承自终端驱动程序设置。调用 `qiflush` 会配置终端在发生任何此类事件时 `flush` 队列（丢弃其内容），给人一种对用户输入响应更快的印象，但会使库对屏幕内容的模型不正确。调用 `noqiflush` 会阻止这种刷新，但如果在事件发生时 `curses` 正在更新屏幕，可能会让慢速连接上的不耐烦用户感到沮丧；有关此问题的缓解方法，请参见下面的 `typeahead`。如果你希望在处理程序退出后输出继续，就像信号未发生一样，可能需要在信号处理程序中调用 `noqiflush`。

### raw, noraw

```c
int raw(void);
int noraw(void);
```

`raw` 将终端配置为以 `raw mode` 读取输入，它类似于 cbreak 模式（参见上面的 `cbreak`），不同之处在于它还会将终端配置的中断、退出、挂起和流控制字符未解释地传递给应用程序，而不是生成信号或作用于 I/O 流。终端“Break”键（如果有）的行为取决于 `curses` 不处理的终端驱动程序配置参数。`noraw` 恢复终端的规范（“cooked”）线路规程。

### timeout, wtimeout

```c
void timeout(int delay);
void wtimeout(WINDOW * win, int delay);
```

`wtimeout` 配置在窗口 `win` 上调用的 `curses` 输入字符读取函数使用阻塞还是非阻塞读取。如果 `delay` 为负，`curses` 使用阻塞读取，无限期等待输入。如果 `delay` 为零，读取是非阻塞的；如果没有待处理的输入，输入字符读取函数返回 `ERR`。如果 `delay` 为正，输入字符读取函数阻塞 `delay` 毫秒，如果延迟结束仍没有待处理的输入，则返回 `ERR`。`timeout` 在 `stdscr` 上调用 `wtimeout`。

### typeahead()

```c
int typeahead(int fd);
```

通常，`curses` 库在更新屏幕时使用 `poll(2)` 或 `select(2)` 检查终端输入文件描述符的活动；如果发现任何活动，它会将输出推迟到下一次 `wrefresh(3X)` 或 `doupdate(3X)` 调用，从而更快地响应用户击键。库测试传递给 `newterm(3X)` 的 `FILE` 流指针对应的文件描述符（如果调用了 `initscr(3X)`，则为 `stdin`）是否有待处理输入。`typeahead` 指示 `curses` 改为测试文件描述符 `fd`。`fd` 为 `-1` 会禁用检查。

## 返回值

`timeout` 和 `wtimeout` 不返回值。

`cbreak`、`nocbreak`、`echo`、`noecho`、`halfdelay`、`intrflush`、`keypad`、`meta`、`nodelay`、`notimeout`、`nl`、`nonl`、`raw`、`noraw` 和 `typeahead` 成功时返回 `OK`，失败时返回 `ERR`。

在 `ncurses` 中，上一段中的函数在以下情况下返回 `ERR`：

- 设备的库 `TERMINAL` 结构尚未使用 `initscr(3X)`、`newterm(3X)` 或 `setupterm(3X)` 初始化，或者
- `win` 是空指针（`intrflush` 和 `meta` 除外，它们忽略其值）。

此外，如果 `delay` 超出 1..255 范围，`halfdelay` 返回 `ERR`。

有关 `is_cbreak`、`is_echo`、`is_nl` 和 `is_raw` 的返回值，请参见下面的“扩展”一节。

## 注意

`echo`、`noecho`、`halfdelay`、`intrflush`、`meta`、`nl`、`nonl`、`nodelay`、`notimeout`、`noqiflush`、`qiflush`、`timeout` 和 `wtimeout` 可能实现为宏。

`noraw` 和 `nocbreak` 遵循历史实践，它们分别尝试从 raw 和 cbreak 恢复终端的规范（“cooked”）线路规程。将 `raw`/`noraw` 调用与 `cbreak`/`nocbreak` 调用混合使用会导致终端驱动程序控制状态难以预测或理解；不建议这样做。

`curses` 文档随意使用术语“delay”和“timeout”来描述输入处理的两个相关但不同的方面，这可能会让用户困惑。函数 `halfdelay`、`nodelay`、`timeout` 和 `wtimeout` 配置输入字符读取函数（`wgetch(3X)` 或 `wget_wch(3X)`）是否等待键盘输入开始，以及等待多长时间。`keypad` 配置该函数在读取到的第一个字符是 ESC 时是否等待进一步输入。调用 `notimeout`（它与 `timeout` 或 `wtimeout` 无关）会使这种等待进一步字符的延迟实际上变为无限。X/Open Curses 没有提供其他方式配置第二个延迟的长度，但 AIX 和 `ncurses` 扩展 `ESCDELAY` 既可作为环境变量，也可作为全局符号使用，分别允许用户和应用程序进行配置；参见 `ncurses(3X)` 和 `curs_variables(3X)`。

## 扩展

`ncurses` 提供四个与 `cbreak`、`echo`、`nl` 和 `raw` 对应的 `is_` 函数，允许应用程序查询它们的状态。

| 查询 | 设置 | 重置 |
| --- | --- | --- |
| `is_cbreak` | `cbreak` | `nocbreak` |
| `is_echo` | `echo` | `noecho` |
| `is_nl` | `nl` | `nonl` |
| `is_raw` | `raw` | `noraw` |

在每种情况下，函数返回：

- `1`  
    如果选项已设置，
- `0`  
    如果选项未设置，或
- `-1`  
    如果设备的库 `TERMINAL` 结构尚未初始化。

## 可移植性

使用 `ncurses` 扩展的应用程序应将其使用建立在 `NCURSES_VERSION` 预处理器宏的可见性上。

除上面“扩展”一节所述外，X/Open Curses Issue 4 描述了这些函数。它没有为它们指定错误条件。

SVr4 仅将成功返回值描述为“一个不等于 `ERR` 的整数值”。

`ncurses` 遵循 X/Open Curses 和 System V `curses` 的历史实践，在初始化屏幕时清除终端驱动程序的“echo”标志。BSD `curses` 没有这样做，但其 `raw` 函数作为副作用将其关闭。为了获得最佳可移植性，即使在程序保留终端规范（“cooked”）线路规程时，也应在初始化后立即显式调用 `echo` 或 `noecho`。

X/Open Curses 对于 `raw` 是否应禁用由 `nl` 和 `nonl` 控制的车回车和换行转换功能含糊不清。BSD `curses` 关闭了这些转换；System V `curses` 没有。`ncurses` 会关闭它们，假设请求原始输入的程序员希望获得操作系统不会更改的干净（理想情况下是 8 位干净）连接。

当首次为窗口启用 `keypad` 时，`ncurses` 会为其屏幕的终端类型描述加载标准功能键字符串能力；参见 `terminfo(5)` 中以“key_”开头的条目。如果该描述包含扩展字符串能力（例如由 `tic(1)` 的 `-x` 选项产生），则 `ncurses` 还会为代码以“k”开头的能力定义键。`ncurses` 会为每个此类扩展能力生成一个数字键代码；取决于之前加载的终端类型描述，这些代码可能在程序的不同执行之间有所不同。`keyname(3X)` 识别生成的键代码，并返回以“k”开头的名称，表示 `terminfo` 能力名称，而不是用于 `curses` 键名的“KEY_”。另一方面，应用程序可以使用 `define_key(3X)` 将选定的键绑定到程序员选择的字符串。此特性使应用程序能够使用 `tigetstr(3X)` 检查其存在性，并重新分配数字键代码以满足自身需求。

低级应用程序可以使用 `tigetstr(3X)` 获取任何字符串能力的定义。`curses` 应用程序使用输入字符读取函数从输入获取键代码，并依赖于字符串能力加载的顺序。多个键能力字符串可以具有相同的值，但输入字符读取函数只能报告一个键代码。大多数 `curses` 实现（包括 `ncurses`）按照字符串能力名称的 `strfnames` 数组中出现的顺序加载键定义；参见 `term_variables(3X)`。使用特定定义最后读取的能力决定要报告的键代码。在 `ncurses` 中，扩展能力可以解释为键定义。库在其内置定义之后加载这些能力，如果扩展能力的值与之前加载的值相同，库使用较后的定义。

## 历史

4BSD（1980）引入了 `echo`、`noecho`、`nl`、`nonl`、`raw` 和 `noraw`。

SVr2（1984）采用了新的终端驱动程序，扩展了 `curses` API 以支持它，包括 `cbreak`、`nocbreak`、`intrflush`、`keypad`、`meta`、`nodelay` 和 `typeahead`。

SVr3（1987）添加了 `halfdelay`、`notimeout` 和 `wtimeout`。`qiflush` 和 `noqiflush` 出现在 SVr3.1（1987）中，此时 `intrflush` 成为这两个函数之一的包装器，取决于其布尔参数的值。SVr3.1 还添加了 `timeout`。

`ncurses` 6.5（2024）引入了 `is_cbreak`、`is_echo`、`is_nl` 和 `is_raw`。

以前，`ncurses` 使用 `nl` 和 `nonl` 控制输出以及输入时换行到回车/换行的转换。X/Open Curses 仅记录了这些函数用于输入。这一差异源于将 `pcurses` 源代码（1986）从使用 `ioctl(2)` 调用和 `sgttyb` 结构转换为 `termios`（POSIX 终端 API）。在前者中，输入和输出转换都通过单个选项“CRMOD”控制，而后者将这些特性分开。由于该转换会干扰输出优化，`ncurses` 6.2（2020）修改了 `nl` 和 `nonl`，消除了它们对输出的影响。

## 另请参阅

`curses(3X)`、`curs_getch(3X)`、`curs_initscr(3X)`、`curs_util(3X)`、`define_key(3X)`、`termios(3)`、`term_variables(3X)`

## COLOPHON

此页面是 `ncurses`（new curses）项目的一部分。项目信息可在 <https://invisible-island.net/ncurses/ncurses.html> 找到。如果对本手册页有缺陷报告，请发送到 bug-ncurses@gnu.org。此页面从 2026-08-04 获取的 tarball ncurses-6.6.tar.gz 中获得，该 tarball 来自 <https://ftp.gnu.org/gnu/ncurses/>。如果你发现此 HTML 版本页面存在渲染问题，或认为有更好或更新的页面来源，或对 COLOPHON 中的信息（该信息不属于原始手册页）有更正或改进，请发送邮件到 man-pages@man7.org。

```log
ncurses @NCURSES_MAJOR@.@NCU... 2025-10-04                curs_inopts(3X)
```