[文档](https://docs.python.org/zh-cn/3/library/curses.html)

[howto](https://docs.python.org/zh-cn/3/howto/curses.html)

# curses --- 字符单元显示的终端处理

curses 模块提供了 curses 库的接口，这是可移植高级终端处理的事实标准。

此扩展模块旨在匹配 ncurses 的 API，这是一个部署在 Linux 和 Unix 的 BSD 变体上的开源 curses 库。

Python 的 Windows 版不包括 curses 模块。 第三方的 windows-curses 包在 Windows 上提供相同的接口。

## 使用

### 开始和结束 curses 应用程序

在做任何事情之前，`curses` 必须被初始化。这是通过调用 `initscr()` 函数来完成的，它将确定终端的类型，向终端发送任何必须的设置代码，并创建多种内部数据结构。

调试，导入 `curses.wrapper()` 函数并像这样使用它:

```py
from curses import wrapper

def main(stdscr):
    # 清空屏幕
    stdscr.clear()

    # 当 i == 10 时这将引发 ZeroDivisionError。
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

        stdscr.refresh()
        stdscr.getkey()

wrapper(main)
```

`wrapper()` 函数接受一个可调用对象并进行初始化过程，如果终端支持彩色还会初始化颜色。接下来 `wrapper()` 会运行你提供的可调用对象。当该可调用对象返回时，`wrapper()` 将恢复终端的初始状态。 该可调用对象会在 `try...except` 内被调用以捕获异常，恢复终端状态，然后重新引发该异常。 这样你的终端将不会在发生异常时处于不正常状态，你将能够读取异常的消息和回溯。

### 窗口和面板

窗口是 `curses` 中的基本抽象。一个窗口对象表示了屏幕上的一个矩形区域，并且提供方法来显示文本、擦除文本、允许用户输入字符串等等。

函数 `initscr()` 返回的 `stdscr` 对象覆盖整个屏幕。

函数 `newwin()` 根据给定的尺寸创建一个新窗口，并返回这个新的窗口对象。

注意 `curses` 使用的坐标系统与寻常的不同。坐标始终是以 `y,x` 的顺序传递，并且左上角是坐标 `(0,0)`。这打破了正常的坐标处理约定，即 `x` 坐标在前

你的应用程序能够查明屏幕的尺寸，`curses.LINES` 和 `curses.COLS` 分别代表了 `y` 和 `x` 方向上的尺寸。合理的坐标应位于 `(0,0)` 到 `(curses.LINES - 1, curses.COLS - 1)` 范围内。

当你调用一个方法来显示或擦除文本时，效果并不会立即显示。相反，你必须调用窗口对象的 `refresh()` 方法来更新屏幕。

### 显示文字

属性允许以突出显示形态显示文本，比如加粗、下划线、反相或添加颜色。这些属性将在下一小节详细说明。

`addstr()` 方法接受一个 Python 字符串或字节串作为要显示的值。 字节串的内容会被原样发送到终端。 

方法 `addch()` 接受一个字符，可以是长度为 1 的字符串，长度为 1 的字节串或者一个整数。

窗口会记住上次操作之后光标所在位置，所以如果你忽略 `y,x` 坐标，字符串和字符会出现在上次操作结束的位置。你也可以通过 `move(y,x)` 的方法来移动光标。

如果您的应用程序完全不需要闪烁光标，可以调用 `curs_set(False)` 来使其不可见。

### 属性和颜色

字符可以以不同的方式显示。基于文本的应用程序常常以反相显示状态行，一个文本查看器可能需要突出显示某些单词。为了支持这种用法，`curses` 允许你为屏幕上的每个单元指定一个属性值。

`curses` 库还支持在提供了颜色功能的终端上显示颜色。最常见的此类终端很可能是 Linux 控制台，其次是支持彩色的 `xterm`。

为了使用颜色，你必须在调用完函数 `initscr()` 后尽快调用函数 `start_color()`，来初始化默认颜色集 (`curses.wrapper()` 函数自动完成了这一点)。 当它完成后，如果使用中的终端支持显示颜色， `has_colors()` 会返回真值。

curses 库维护一个有限数量的颜色对，包括一个前景（文本）色和一个背景色。你可以使用函数 `color_pair()` 获得一个颜色对对应的属性值。它可以通过按位或运算与其他属性，比如 `A_REVERSE` 组合。

一个样例，用 1 号颜色对显示一行文本:

```py
stdscr.addstr("Pretty text", curses.color_pair(1))
stdscr.refresh()
```

如前所述，颜色对由前景色和背景色组成。`init_pair(n, f, b)` 函数可改变颜色对 `n` 的定义为前景色 `f` 和背景色 `b`。颜色对 `0` 硬编码为黑底白字，不能改变。

颜色是有编号的，当 `start_color()` 激活颜色模式时会初始化 8 种基本颜色。它们是：0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan 和 7:white。curses 模块为这些颜色定义了相应的名称常量：`curses.COLOR_BLACK`, `curses.COLOR_RED` 等等。

```py
# 将颜色 1 改为红色文本白色背景
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
```

当你改变一个颜色对时，任何已经使用该颜色对来显示的文本将会更改为新的颜色。

```py
# 显示新颜色的文本
stdscr.addstr(0,0, "RED ALERT!", curses.color_pair(1))
```

### 用户输入

C curses 库只提供了非常简单的输入机制。Python 的 curses 模块增加了一个基本的文本输入控件。

## 函数

### curses.napms() - 休眠

```py
curses.napms(ms)
```

休眠 `ms` 毫秒。

### curses.can_change_color()

根据程序员能否改变终端显示的颜色返回 True 或 False。

### curses.init_color() - 更改某个颜色的定义

```py
curses.init_color(color_number, r, g, b)
```

更改某个颜色的定义，接受要更改的颜色编号以及三个 RGB 值（表示红绿蓝三个分量的强度）。 
- `color_number` 的值必须为 `0` 和 `COLORS - 1` 之间的数字。 
- 每个 `r, g, b` 值必须为 `0` 和 `1000` 之间的数字。 

当使用 `init_color()` 时，出现在屏幕上的对应颜色会立即按照新定义来更改。 此函数在大多数终端上都是无操作的；它仅会在 `can_change_color()` 返回 `True` 时生效。

> 可精确调整颜色，但并非通用型功能。避免覆盖原始颜色，使用 8个基础色外的编号。

### curses.init_pair() - 改变前景与背景颜色对

```py
curses.init_pair(pair_number, fg, bg)
```

更改颜色对的定义。 它需要三个参数：要更改的颜色对的编号、前景色编号和背景色编号。

`pair_number` 的值必须介于 `1` 和 `COLOR_PAIRS - 1` 之间。 

`fg` 和 `bg` 参数的值必须介于 `0` 和 `COLORS - 1` 之间，或者在调用 `use_default_colors()` 或 a`ssume_default_colors()` 时使用 `-1`。 如果该颜色对之前已被初始化，则屏幕将被刷新，该颜色对的所有出现都将更改为新定义。

```py
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
```

### curses.initscr()

初始化库。 返回代表整个屏幕的 “窗口” 对象。

请参阅 `setupterm()` 了解关于在此函数之前调用它的注意事项。

### curses.curs_set(visibility)

设置光标状态。 

`visibility` 可设为 0, 1 或 2 表示不可见、正常与高度可见。 在许多终端上，“正常可见”模式为下划线光标而“高度可见”模式为方块形光标。

### curses.start_color()

如果程序员想要使用颜色，则必须在任何其他颜色操作例程被调用之前调用它。 在 `initscr()` 之后立即调用此例程是一个很好的做法。

`start_color()` 初始化八个基础颜色（黑色、红色、绿色、黄色、蓝色、洋红色、青色和白色），并在 `curses` 模块中初始化两个全局变量 `COLORS` 和 `COLOR_PAIRS`，用于存储终端可支持的最大颜色数及颜色对数量。此外，它还会将终端上的颜色恢复至终端刚开启时的原始值。

### curses.wrapper()

```py
curses.wrapper(func, /, *args, **kwargs)
```

初始化 `curses` 并调用另一个可调用对象 `func`，该对象应当为你的使用 `curses` 的应用程序的其余部分。 如果应用程序引发了异常，此函数将在重新引发异常并生成回溯信息之前将终端恢复到正常状态。 随后可调用对象 `func` 会被传入主窗口 `stdscr` 作为其第一个参数，再带上其他所有传给 `wrapper()` 的参数。

### curses.assume_default_colors()

```py
curses.assume_default_colors(fg, bg, /)
```

允许在支持此特性的终端上使用颜色的默认值。使用此功能可在您的应用程序中支持透明度。

### curses.use_default_colors()

相当于 `assume_default_colors(-1, -1)`。

```py
# 使用默认颜色，创建颜色列表
curses.use_default_colors()  
color_list = [curses.COLOR_RED, curses.COLOR_GREEN,  
            curses.COLOR_YELLOW, curses.COLOR_BLUE,  
            curses.COLOR_MAGENTA, curses.COLOR_CYAN]  

# 设置颜色对，设置一批前景色，背景为默认
for i, fg in enumerate(color_list, start=1):  
    curses.init_pair(i, fg, -1)  
```

### curses.color_pair() —— 返回颜色对属性值

```py
curses.color_pair(pair_number)
```

返回用于以指定颜色对显示文本的属性值。 仅支持前 256 个颜色对。 该属性值可与 `A_STANDOUT`, `A_REVERSE` 以及其他 `A_*` 属性组合使用。 `pair_number()` 是此函数的对应操作。

### curses.pair_number() —— 返回颜色对编号

```py
curses.pair_number(attr)
```

返回通过属性值 `attr` 所设置的颜色对的编号。 `color_pair()` 是此函数的对应操作。

### curses.update_lines_cols()

```py
curses.update_lines_cols()
```

更新 `LINES` 和 `COLS` 模块变量。 适用于检测手动调整屏幕大小。

## 窗口对象

### class curses.window

```py
class curses.window
```

Window 对象会由上面的 `initscr()` 和 `newwin()` 返回，它具有以下方法和属性

#### window.erase() —— 清空窗口

> 通常仅需清空

#### window.clear()

类似于 `erase()`，但还会导致在下次调用 `refresh()` 时整个窗口被重新绘制。
> 开销更大

#### window.getch()

```py
window.getch([y, x])
```

在将光标移动到 `y, x` （如果已指定）后读取按键，并将其作为整数返回。 如果窗口不是面板并且自上次刷新以来已被修改，则窗口会首先刷新。 等待直到按下按键，或者如果读取是非阻塞的或超时，则返回 -1。

```py
while True:
    # 若收到键盘 `q` 则退出
    if stdscr.getch() == ord('q'):
        break
```

#### window.nodelay()

```py
window.nodelay(flag)
```

- `flag` 
    - `True`  
        `getch()` 非阻塞


#### window.refresh() —— 立即更新显示

```py
window.refresh([pminrow, pmincol, sminrow, smincol, smaxrow, smaxcol])
```

立即更新显示（将实际屏幕与之前的绘制/删除方法进行同步）。

`pminrow` 和 `pmincol` 指定要在面板中显示的矩形的左上角。 

`sminrow`, `smincol`, `smaxrow` 和 `smaxcol` 指定要在屏幕上显示的矩形的边缘。 要在面板中显示的矩形的右下角是根据屏幕坐标计算的，因为这两个矩形的大小必须相同。 两个矩形都必须完全包含在其各自的结构内。 

`pminrow`, `pmincol`, `sminrow` 或 `smincol` 的负值将被视为零。

#### window.addch()

```py
window.addch(ch[, attr])
window.addch(y, x, ch[, attr])
```

将带有属性 `attr` 的字符 `ch` 绘制到 `(y, x)`，覆盖之前在该位置上绘制的任何字符。 默认情况下，字符的位置和属性均为窗口对象的当前设置。

> 在窗口、子窗口或面板之外写入会引发 `curses.error`。 尝试在窗口、子窗口或面板的右下角写入将在字符被打印之后引发异常。 

#### window.addstr()

```py
window.addstr(str[, attr])
window.addstr(y, x, str[, attr])
```

将带有属性 `attr` 的字符串 `str` 绘制到 `(y, x)`，覆盖之前在屏幕上的任何内容。



## 常量

- `curses.COLORS`  
    终端可支持的最大颜色数。 它只有在调用 `start_color()` 之后才会被定义。

- `curses.COLOR_PAIRS`  
    终端可支持的最大颜色对数。 它只有在调用 `start_color()` 之后才会被定义。

- `curses.COLS`  
    屏幕的宽度，即列数。 它只有在调用 `initscr()` 之后才会被定义。 由 `update_lines_cols()`、 `resizeterm()` 和 `resize_term()` 更新。

- `curses.LINES`  
    屏幕的高度，即行数。 它只有在调用 `initscr()` 之后才会被定义。 由 `update_lines_cols()`、 `resizeterm()` 和 `resize_term()` 更新。


有些常量可用于指定字符单元属性。 实际可用的常量取决于具体的系统。

- `curses.A_BOLD`  
    粗体模式

- `curses.A_INVIS`  
    不可见或空白模式

键由名称以 `KEY_` 开头的整数常量引用。确切的可用键取决于系统。

- `curses.KEY_RESIZE`  
    终端大小改变事件