# termios

https://man7.org/linux/man-pages/man3/termios.3.html

## 名称

`termios`, `tcgetattr`, `tcsetattr`, `tcsendbreak`, `tcdrain`, `tcflush`, `tcflow`, `cfmakeraw`, `cfgetospeed`, `cfgetispeed`, `cfsetispeed`, `cfsetospeed`, `cfsetspeed` - 获取和设置终端属性、线路控制、获取和设置波特率

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#include <termios.h>
#include <unistd.h>

int tcgetattr(int fd, struct termios *termios_p);
int tcsetattr(int fd, int optional_actions,
              const struct termios *termios_p);

int tcsendbreak(int fd, int duration);
int tcdrain(int fd);
int tcflush(int fd, int queue_selector);
int tcflow(int fd, int action);

void cfmakeraw(struct termios *termios_p);

speed_t cfgetispeed(const struct termios *termios_p);
speed_t cfgetospeed(const struct termios *termios_p);

int cfsetispeed(struct termios *termios_p, speed_t speed);
int cfsetospeed(struct termios *termios_p, speed_t speed);
int cfsetspeed(struct termios *termios_p, speed_t speed);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）：

```c
cfsetspeed(), cfmakeraw():
    Since glibc 2.19:
        _DEFAULT_SOURCE
    glibc 2.19 and earlier:
        _BSD_SOURCE
```

## 描述

`termios` 函数描述了一个通用终端接口，用于控制异步通信端口。

### termios 结构体

这里描述的许多函数都有一个 `termios_p` 参数，它是指向 `termios` 结构体的指针。该结构体至少包含以下成员：

```c
tcflag_t c_iflag;      /* 输入模式 */
tcflag_t c_oflag;      /* 输出模式 */
tcflag_t c_cflag;      /* 控制模式 */
tcflag_t c_lflag;      /* 本地模式 */
cc_t     c_cc[NCCS];   /* 特殊字符 */
```

可以赋给这些字段的值如下所述。对于前四个位掩码字段，某些可设置关联标志的定义只有在定义了特定特性测试宏时才会暴露（参见 [feature_test_macros(7)]），如方括号（`[]`）中所述。

在下面的描述中，“不在 POSIX 中”表示该值未在 POSIX.1-2001 中规定，“XSI”表示该值在 POSIX.1-2001 中作为 XSI 扩展的一部分规定。

`c_iflag` 标志常量：

- `IGNBRK` 忽略输入中的 BREAK 条件。
- `BRKINT` 如果设置了 `IGNBRK`，则忽略 BREAK。如果未设置 `IGNBRK` 但设置了 `BRKINT`，则 BREAK 会导致输入和输出队列被刷新；如果终端是前台进程组的控制终端，则会导致向前台进程组发送 `SIGINT`。当 `IGNBRK` 和 `BRKINT` 都未设置时，BREAK 读作空字节（`'\0'`），除非设置了 `PARMRK`，此时读作序列 `\377 \0 \0`。
- `IGNPAR` 忽略帧错误和奇偶校验错误。
- `PARMRK` 如果设置了此位，带奇偶校验错误或帧错误的输入字节在传给程序时会被标记。此位仅在设置了 `INPCK` 且未设置 `IGNPAR` 时有意义。错误字节的标记方式是前置两个字节 `\377` 和 `\0`。因此，对于从终端接收的一个错误字节，程序实际会读取三个字节。如果某个有效字节的值为 `\377`，且未设置 `ISTRIP`（见下文），程序可能将其与标记奇偶校验错误的前缀混淆。因此，在这种情况下，有效字节 `\377` 会以两个字节 `\377 \377` 传给程序。如果 `IGNPAR` 和 `PARMRK` 都未设置，则带奇偶校验错误或帧错误的字符读作 `\0`。
- `INPCK` 启用输入奇偶校验检查。
- `ISTRIP` 去掉第八位。
- `INLCR` 在输入时将 NL 转换为 CR。
- `IGNCR` 忽略输入中的回车符。
- `ICRNL` 在输入时将回车符转换为换行符（除非设置了 `IGNCR`）。
- `IUCLC`（不在 POSIX 中）在输入时将大写字符映射为小写。
- `IXON` 在输出上启用 XON/XOFF 流控制。
- `IXANY`（XSI）输入任何字符都会重新启动已停止的输出。（默认只允许 START 字符重新启动输出。）
- `IXOFF` 在输入上启用 XON/XOFF 流控制。
- `IMAXBEL`（不在 POSIX 中）输入队列满时响铃。Linux 未实现此位，行为如同它始终被设置。
- `IUTF8`（自 Linux 2.6.4 起）（不在 POSIX 中）输入为 UTF8；这允许在熟模式下正确执行字符擦除。

`c_oflag` 标志常量：

- `OPOST` 启用实现定义的输出处理。
- `OLCUC`（不在 POSIX 中）在输出时将小写字符映射为大写。
- `ONLCR`（XSI）在输出时将 NL 映射为 CR-NL。
- `OCRNL` 在输出时将 CR 映射为 NL。
- `ONOCR` 不在第 0 列输出 CR。
- `ONLRET` 假定 NL 字符执行回车功能；在 NL 和 CR 之后，内核认为的当前列都设为 0。
- `OFILL` 为延迟发送填充字符，而不是使用定时延迟。
- `OFDEL` 填充字符为 ASCII DEL（0177）。如果未设置，填充字符为 ASCII NUL（`'\0'`）。（Linux 未实现。）
- `NLDLY` 换行延迟掩码。值为 `NL0` 和 `NL1`。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]
- `CRDLY` 回车延迟掩码。值为 `CR0`、`CR1`、`CR2` 或 `CR3`。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]
- `TABDLY` 水平制表符延迟掩码。值为 `TAB0`、`TAB1`、`TAB2`、`TAB3`（或 `XTABS`，但请参见“缺陷”一节）。`TAB3`（即 `XTABS`）会将制表符展开为空格（每 8 列一个制表位）。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]
- `BSDLY` 退格延迟掩码。值为 `BS0` 或 `BS1`。（从未实现。）[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]
- `VTDLY` 垂直制表符延迟掩码。值为 `VT0` 或 `VT1`。
- `FFDLY` 换页延迟掩码。值为 `FF0` 或 `FF1`。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]

`c_cflag` 标志常量：

- `CBAUD`（不在 POSIX 中）波特速度掩码（4+1 位）。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `CBAUDEX`（不在 POSIX 中）额外波特速度掩码（1 位），包含在 `CBAUD` 中。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]（POSIX 规定波特速度存储在 `termios` 结构体中，但不规定具体位置，并提供 `cfgetispeed()` 和 `cfsetispeed()` 来获取它。有些系统使用 `c_cflag` 中由 `CBAUD` 选择的位，其他系统使用单独字段，例如 `sg_ispeed` 和 `sg_ospeed`。）
- `CSIZE` 字符大小掩码。值为 `CS5`、`CS6`、`CS7` 或 `CS8`。
- `CSTOPB` 设置两个停止位，而不是一个。
- `CREAD` 启用接收器。
- `PARENB` 在输出上启用奇偶校验生成，在输入上启用奇偶校验检查。
- `PARODD` 如果设置，则输入和输出的奇偶校验为奇校验；否则使用偶校验。
- `HUPCL` 在最后一个进程关闭设备后拉低调制解调器控制线（挂断）。
- `CLOCAL` 忽略调制解调器控制线。
- `LOBLK`（不在 POSIX 中）阻止来自非当前 shell 层的输出。供 `shl`（shell 层）使用。（Linux 未实现。）
- `CIBAUD`（不在 POSIX 中）输入速度掩码。`CIBAUD` 位的值与 `CBAUD` 位的值相同，但左移 `IBSHIFT` 位。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]（glibc 未实现，Linux 通过 `TCGET*` 和 `TCSET*` ioctl 支持；参见 [ioctl_tty(2)]）
- `CMSPAR`（不在 POSIX 中）使用“stick”（mark/space）奇偶校验（某些串行设备支持）：如果设置了 `PARODD`，奇偶校验位始终为 1；如果未设置 `PARODD`，则奇偶校验位始终为 0。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `CRTSCTS`（不在 POSIX 中）启用 RTS/CTS（硬件）流控制。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]

`c_lflag` 标志常量：

- `ISIG` 当收到 INTR、QUIT、SUSP 或 DSUSP 中任一字符时，生成相应信号。
- `ICANON` 启用规范模式（下文描述）。
- `XCASE`（不在 POSIX 中；Linux 不支持）如果还设置了 `ICANON`，则终端仅支持大写。输入会转换为小写，但前面有 `\` 的字符除外。输出时，大写字符前会加上 `\`，小写字符会转换为大写。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE` 或 `_XOPEN_SOURCE`]
- `ECHO` 回显输入字符。
- `ECHOE` 如果还设置了 `ICANON`，ERASE 字符会擦除前一个输入字符，WERASE 会擦除前一个单词。
- `ECHOK` 如果还设置了 `ICANON`，KILL 字符会擦除当前行。
- `ECHONL` 如果还设置了 `ICANON`，即使未设置 ECHO，也回显 NL 字符。
- `ECHOCTL`（不在 POSIX 中）如果还设置了 `ECHO`，除 TAB、NL、START 和 STOP 之外的终端特殊字符会回显为 `^X`，其中 X 是 ASCII 码比该特殊字符大 0x40 的字符。例如，字符 0x08（BS）会回显为 `^H`。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `ECHOPRT`（不在 POSIX 中）如果还设置了 `ICANON` 和 `ECHO`，字符在被擦除时会打印出来。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `ECHOKE`（不在 POSIX 中）如果还设置了 `ICANON`，KILL 会按照 `ECHOE` 和 `ECHOPRT` 的规定，通过擦除行上的每个字符来回显。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `DEFECHO`（不在 POSIX 中）仅当进程正在读取时回显。（Linux 未实现。）
- `FLUSHO`（不在 POSIX 中；Linux 不支持）正在刷新输出。此标志通过输入 DISCARD 字符来切换。[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `NOFLSH` 在为 INT、QUIT 和 SUSP 字符生成信号时，禁止刷新输入和输出队列。
- `TOSTOP` 向尝试写入其控制终端的后台进程的进程组发送 `SIGTTOU` 信号。
- `PENDIN`（不在 POSIX 中；Linux 不支持）当下一个字符被读取时，重新打印输入队列中的所有字符。（`bash(1)` 以这种方式处理预输入。）[需要 `_BSD_SOURCE` 或 `_SVID_SOURCE`]
- `IEXTEN` 启用实现定义的输入处理。必须启用此标志以及 `ICANON`，才能解释特殊字符 EOL2、LNEXT、REPRINT、WERASE，并使 `IUCLC` 标志生效。

`c_cc` 数组定义终端特殊字符。符号索引（初始值）和含义如下：

- `VDISCARD`（不在 POSIX 中；Linux 不支持；017，SI，Ctrl-O）切换：开始/停止丢弃待处理输出。在设置了 `IEXTEN` 时识别，然后不作为输入传递。
- `VDSUSP`（不在 POSIX 中；Linux 不支持；031，EM，Ctrl-Y）延迟挂起字符（DSUSP）：当用户程序读取该字符时发送 `SIGTSTP` 信号。在设置了 `IEXTEN` 和 `ISIG`、系统支持作业控制时识别，然后不作为输入传递。
- `VEOF`（004，EOT，Ctrl-D）文件结束字符（EOF）。更准确地说：此字符使待处理的 tty 缓冲区被发送给等待的用户程序，而不等待行结束。如果它是行的第一个字符，用户程序中的 `read(2)` 返回 0，表示文件结束。在设置了 `ICANON` 时识别，然后不作为输入传递。
- `VEOL`（0，NUL）附加行结束字符（EOL）。在设置了 `ICANON` 时识别。
- `VEOL2`（不在 POSIX 中；0，NUL）又一个行结束字符（EOL2）。在设置了 `ICANON` 时识别。
- `VERASE`（0177，DEL，rubout，或 010，BS，Ctrl-H，或也是 #）擦除字符（ERASE）。这会擦除前一个尚未擦除的字符，但不会擦除到 EOF 或行首之前。在设置了 `ICANON` 时识别，然后不作为输入传递。
- `VINTR`（003，ETX，Ctrl-C，或也是 0177，DEL，rubout）中断字符（INTR）。发送 `SIGINT` 信号。在设置了 `ISIG` 时识别，然后不作为输入传递。
- `VKILL`（025，NAK，Ctrl-U，或 Ctrl-X，或也是 @）终止字符（KILL）。这会擦除自上一个 EOF 或行首以来的输入。在设置了 `ICANON` 时识别，然后不作为输入传递。
- `VLNEXT`（不在 POSIX 中；026，SYN，Ctrl-V）字面下一个字符（LNEXT）。引用下一个输入字符，剥夺其可能的特殊含义。在设置了 `IEXTEN` 时识别，然后不作为输入传递。
- `VMIN` 非规范读取的最小字符数（MIN）。
- `VQUIT`（034，FS，Ctrl-\）退出字符（QUIT）。发送 `SIGQUIT` 信号。在设置了 `ISIG` 时识别，然后不作为输入传递。
- `VREPRINT`（不在 POSIX 中；022，DC2，Ctrl-R）重新打印未读字符（REPRINT）。在设置了 `ICANON` 和 `IEXTEN` 时识别，然后不作为输入传递。
- `VSTART`（021，DC1，Ctrl-Q）启动字符（START）。重新启动由停止字符停止的输出。在设置了 `IXON` 时识别，然后不作为输入传递。
- `VSTATUS`（不在 POSIX 中；Linux 不支持；状态请求：024，DC4，Ctrl-T）状态字符（STATUS）。在终端显示状态信息，包括前台进程状态及其消耗的 CPU 时间量。还向前台进程组发送 `SIGINFO` 信号（Linux 不支持）。
- `VSTOP`（023，DC3，Ctrl-S）停止字符（STOP）。停止输出，直到输入启动字符。在设置了 `IXON` 时识别，然后不作为输入传递。
- `VSUSP`（032，SUB，Ctrl-Z）挂起字符（SUSP）。发送 `SIGTSTP` 信号。在设置了 `ISIG` 时识别，然后不作为输入传递。
- `VSWTCH`（不在 POSIX 中；Linux 不支持；0，NUL）切换字符（SWTCH）。在 System V 中用于在 shell 层中切换 shell，这是 shell 作业控制的前身。
- `VTIME` 非规范读取的超时时间（以十分之一秒为单位）（TIME）。
- `VWERASE`（不在 POSIX 中；027，ETB，Ctrl-W）单词擦除（WERASE）。在设置了 `ICANON` 和 `IEXTEN` 时识别，然后不作为输入传递。

可以通过将相应 `c_cc` 元素的值设置为 `_POSIX_VDISABLE` 来禁用单个终端特殊字符。

上述符号下标值都不同，但 `VTIME`、`VMIN` 可能分别与 `VEOL`、`VEOF` 具有相同的值。在非规范模式下，特殊字符含义被超时含义取代。关于 `VMIN` 和 `VTIME` 的说明，请参见下文非规范模式的描述。

### 获取和更改终端设置

`tcgetattr()` 获取与 `fd` 所引用对象关联的参数，并将它们存储在 `termios_p` 引用的 `termios` 结构体中。此函数可以从后台进程调用；不过，终端属性随后可能被前台进程更改。

`tcsetattr()` 从 `termios_p` 引用的 `termios` 结构体中设置与终端关联的参数（除非需要底层硬件支持而该支持不可用）。`optional_actions` 指定更改何时生效：

- `TCSANOW` 更改立即生效。
- `TCSADRAIN` 在写入 `fd` 的所有输出都已传输后更改生效。更改影响输出的参数时应使用此选项。
- `TCSAFLUSH` 在写入 `fd` 所引用对象的所有输出都已传输后更改生效，并且在更改前将丢弃所有已接收但未读取的输入。

### 规范模式和非规范模式

`c_lflag` 中 `ICANON` 规范标志的设置决定终端是以规范模式（设置了 `ICANON`）还是非规范模式（未设置 `ICANON`）运行。默认情况下，`ICANON` 被设置。

在规范模式下：

- 输入逐行可用。当输入行分隔符之一（NL、EOL、EOL2；或行首的 EOF）被输入时，一行输入即可用。除 EOF 情况外，行分隔符会包含在 `read(2)` 返回的缓冲区中。
- 启用行编辑（ERASE、KILL；如果设置了 `IEXTEN` 标志：WERASE、REPRINT、LNEXT）。`read(2)` 最多返回一行输入；如果 `read(2)` 请求的字节数少于当前输入行中可用的字节数，则只读取请求的字节数，其余字符可供将来的 `read(2)` 使用。
- 最大行长度为 4096 个字符（包括终止换行符）；超过 4096 个字符的行会被截断。超过 4095 个字符后，输入处理（例如 `ISIG` 和 `ECHO*` 处理）继续，但 4095 个字符之后直到任何终止换行符（不包括该换行符）之前的任何输入数据都会被丢弃。这确保终端始终能接收更多输入，直到至少可以读取一行。

在非规范模式下，输入立即可用（用户无需输入行分隔符），不执行输入处理，并禁用行编辑。读取缓冲区只接受 4095 个字符；如果输入模式切换为规范模式，这为换行符提供了必要空间。`MIN`（`c_cc[VMIN]`）和 `TIME`（`c_cc[VTIME]`）的设置决定 `read(2)` 在何种情况下完成；有四种不同情况：

- `MIN == 0, TIME == 0`（轮询读取）  
  如果有数据可用，`read(2)` 立即返回，返回可用字节数和请求字节数中较小者。如果没有数据可用，`read(2)` 返回 0。
- `MIN > 0, TIME == 0`（阻塞读取）  
  `read(2)` 阻塞直到有 `MIN` 个字节可用，并最多返回请求的字节数。
- `MIN == 0, TIME > 0`（带超时读取）  
  `TIME` 指定定时器限制，单位为十分之一秒。定时器在调用 `read(2)` 时启动。`read(2)` 在至少一个字节数据可用时或定时器到期时返回。如果定时器到期仍无输入可用，`read(2)` 返回 0。如果调用 `read(2)` 时数据已经可用，则该调用的行为如同数据在调用后立即收到。
- `MIN > 0, TIME > 0`（带字节间超时读取）  
  `TIME` 指定定时器限制，单位为十分之一秒。一旦初始输入字节可用，每收到后续字节后都会重新启动定时器。`read(2)` 在满足以下任一条件时返回：  
  - 已收到 `MIN` 个字节。  
  - 字节间定时器到期。  
  - 已收到 `read(2)` 请求的字节数。（POSIX 未规定此终止条件，在某些其他实现上，`read(2)` 在这种情况下不会返回。）  
  由于定时器仅在初始字节可用后启动，因此至少会读取一个字节。如果调用 `read(2)` 时数据已经可用，则该调用的行为如同数据在调用后立即收到。

POSIX 未规定 `O_NONBLOCK` 文件状态标志的设置是否优先于 MIN 和 TIME 设置。如果设置了 `O_NONBLOCK`，非规范模式下的 `read(2)` 可能立即返回，而不管 MIN 或 TIME 的设置。此外，如果没有数据可用，POSIX 允许非规范模式下的 `read(2)` 返回 0，或返回 -1 并将 `errno` 设置为 `EAGAIN`。

### 原始模式

`cfmakeraw()` 将终端设置为类似旧 Version 7 终端驱动程序的“原始”模式：输入逐字符可用，回显被禁用，终端输入和输出字符的所有特殊处理都被禁用。终端属性设置如下：

```c
termios_p->c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP
                | INLCR | IGNCR | ICRNL | IXON);
termios_p->c_oflag &= ~OPOST;
termios_p->c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
termios_p->c_cflag &= ~(CSIZE | PARENB);
termios_p->c_cflag |= CS8;
```

### 线路控制

如果终端使用异步串行数据传输，`tcsendbreak()` 会在特定持续时间内发送连续的零值位流。如果 `duration` 为零，则发送零值位至少 0.25 秒，不超过 0.5 秒。如果 `duration` 不为零，则发送零值位一段实现定义的时间。

如果终端未使用异步串行数据传输，`tcsendbreak()` 不执行任何操作并返回。

`tcdrain()` 等待写入 `fd` 所引用对象的所有输出都已传输。

`tcflush()` 根据 `queue_selector` 的值，丢弃写入 `fd` 所引用对象但尚未传输的数据，或已接收但未读取的数据：

- `TCIFLUSH` 刷新已接收但未读取的数据。
- `TCOFLUSH` 刷新已写入但未传输的数据。
- `TCIOFLUSH` 同时刷新已接收但未读取的数据，以及已写入但未传输的数据。

`tcflow()` 根据 `action` 的值，暂停或恢复 `fd` 所引用对象上的数据传输或接收：

- `TCOOFF` 暂停输出。
- `TCOON` 重新启动暂停的输出。
- `TCIOFF` 发送 STOP 字符，停止终端设备向系统传输数据。
- `TCION` 发送 START 字符，启动终端设备向系统传输数据。

打开终端文件时的默认状态是输入和输出都未暂停。

### 线路速度

提供波特率函数是为了获取和设置 `termios` 结构体中的输入和输出波特率值。新值在成功调用 `tcsetattr()` 之前不会生效。

将速度设置为 `B0` 会指示调制解调器“挂断”。`B38400` 对应的实际比特率可以用 `setserial(8)` 修改。

输入和输出波特率存储在 `termios` 结构体中。

`cfgetospeed()` 返回存储在 `termios_p` 所指向的 `termios` 结构体中的输出波特率。

`cfsetospeed()` 将存储在 `termios_p` 所指向的 `termios` 结构体中的输出波特率设置为 `speed`，它必须是以下常量之一：

```text
B0
B50
B75
B110
B134
B150
B200
B300
B600
B1200
B1800
B2400
B4800
B9600
B19200
B38400
B57600
B115200
B230400
B460800
B500000
B576000
B921600
B1000000
B1152000
B1500000
B2000000
```

这些常量在 SPARC 架构上额外支持：

```text
B76800
B153600
B307200
B614400
```

这些常量在非 SPARC 架构上额外支持：

```text
B2500000
B3000000
B3500000
B4000000
```

由于架构之间的差异，可移植应用程序在使用特定 `Bnnn` 常量之前应检查其是否已定义。

零波特率 `B0` 用于终止连接。如果指定了 `B0`，则不再置位调制解调器控制线。通常，这会断开线路。`CBAUDEX` 是 POSIX.1 定义之外的速度（57600 及以上）的掩码。因此，`B57600 & CBAUDEX` 非零。

可以通过 `TCSETS2` ioctl 将波特率设置为 `Bnnn` 常量定义之外的值；参见 [ioctl_tty(2)]。

`cfgetispeed()` 返回存储在 `termios` 结构体中的输入波特率。

`cfsetispeed()` 将存储在 `termios` 结构体中的输入波特率设置为 `speed`，它必须指定为上面为 `cfsetospeed()` 列出的 `Bnnn` 常量之一。如果输入波特率设置为字面常量 `0`（不是符号常量 `B0`），则输入波特率将等于输出波特率。

`cfsetspeed()` 是 4.4BSD 扩展。它接受与 `cfsetispeed()` 相同的参数，并同时设置输入和输出速度。

## 返回值

`cfgetispeed()` 返回存储在 `termios` 结构体中的输入波特率。

`cfgetospeed()` 返回存储在 `termios` 结构体中的输出波特率。

所有其他函数返回：

- `0` 成功。
- `-1` 失败，并设置 `errno` 以指示错误。

注意，如果请求的更改中*任何*一项能够成功执行，`tcsetattr()` 就返回成功。因此，在进行多项更改时，可能需要在调用之后再次调用 `tcgetattr()`，以检查所有更改是否都已成功执行。

## 属性

关于本节所用术语的解释，参见 [attributes(7)]。

| 接口 | 属性 | 值 |
| --- | --- | --- |
| `tcgetattr()`, `tcsetattr()`, `tcdrain()`, `tcflush()`, `tcflow()`, `tcsendbreak()`, `cfmakeraw()`, `cfgetispeed()`, `cfgetospeed()`, `cfsetispeed()`, `cfsetospeed()`, `cfsetspeed()` | 线程安全 | MT-Safe |

## 标准

`tcgetattr()`、`tcsetattr()`、`tcsendbreak()`、`tcdrain()`、`tcflush()`、`tcflow()`、`cfgetispeed()`、`cfgetospeed()`、`cfsetispeed()`、`cfsetospeed()`  
POSIX.1-2008。

`cfmakeraw()`、`cfsetspeed()`  
BSD。

## 历史

`tcgetattr()`、`tcsetattr()`、`tcsendbreak()`、`tcdrain()`、`tcflush()`、`tcflow()`、`cfgetispeed()`、`cfgetospeed()`、`cfsetispeed()`、`cfsetospeed()`  
POSIX.1-2001。

`cfmakeraw()`、`cfsetspeed()`  
BSD。

## 注释

UNIX V7 及若干后续系统有一个波特率列表，在值 `B0` 到 `B9600` 之后可以找到两个常量 `EXTA`、`EXTB`（“External A”和“External B”）。许多系统用高得多的波特率扩展了该列表。

`tcsendbreak()` 中非零 `duration` 的效果各不相同。SunOS 规定中断持续 `duration * N` 秒，其中 `N` 至少为 0.25，不超过 0.5。Linux、AIX、DU、Tru64 发送持续 `duration` 毫秒的中断。FreeBSD 和 NetBSD 以及 HP-UX 和 MacOS 忽略 `duration` 的值。在 Solaris 和 UnixWare 下，带非零 `duration` 的 `tcsendbreak()` 行为类似于 `tcdrain()`。

## 缺陷

在 Linux 4.16 之前的 Alpha 架构上（以及 glibc 2.28 之前的 glibc），`XTABS` 的值与 `TAB3` 不同，因此终端驱动程序的 `N_TTY` 线路规程代码会忽略它（因为它不属于 `TABDLY` 掩码）。

## 另见

[reset(1)], [setterm(1)], [stty(1)], [tput(1)], [tset(1)], [tty(1)], [ioctl_console(2)], [ioctl_tty(2)], [cc_t(3type)], [speed_t(3type)], [tcflag_t(3type)], `setserial(8)`

## 版本信息

本页是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/doc/man-pages/>⟩ 找到。如果你对本手册页有错误报告，请参见 ⟨<https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>⟩。本页取自 2026-05-24 从 ⟨<https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/>⟩ 获取的 man-pages-6.18.tar.gz tarball。如果你发现此 HTML 版本页面中的渲染问题，或认为有更好或更新的页面来源，或对 COLOPHON 中的信息（其 *不是* 原始手册页的一部分）有更正或改进，请发送邮件至 man-pages@man7.org。

```text
Linux man-pages 6.18            2026-02-08                     termios(3)
```