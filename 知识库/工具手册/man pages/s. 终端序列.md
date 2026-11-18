## terminfo(5) - 终端能力数据库

https://github.com/ThomasDickey/ncurses-snapshots/

- `clear`  
    清除屏幕并将光标移到起始位置（P*）

- `civis`  
    使光标不可见

- `cup` 
    移到第 #1 行第 #2 列

- `sgr0`  
    关闭所有属性

- `rmso`  
    退出突出显示模式

- `setaf`  
    将前景色设为 #1，使用 ANSI 转义

- `setab`  
    将背景色设为 #1，使用 ANSI 转义

- `colornm`  
    给出颜色 #1 的名称

- `colors`  
    屏幕上的最大颜色数

- `pairs`  
    屏幕上的最大颜色对数

## console_codes(4) - Linux 控制台转义与控制序列

### Linux 控制台控制

#### 控制字符

- ESC（`0x1B`，`^[`）  
    开始一个转义序列；

#### DEC 私有模式序列

将末尾的 `h` 替换为 `l` 即可得到重置模式序列。

- `ESC [ ? 25 h`  
    `DECTECM`（默认开启）：使光标可见。

#### ECMA-48 CSI 序列

`CSI`（或 `ESC [`）后跟一串参数，最多 `NPAR`（`16`）个，这些参数是用分号分隔的十进制数。空参数或缺失参数取为 `0`。

> 原点为 1,1 而非 0,0 

CSI 序列的动作由其最终字符决定。

- `H`（`CUP`）  
    将光标移到指定行、列（原点为 `1,1`）。

- `J`（`ED`）  
    擦除显示（默认：从光标到显示末尾）。

    - `ESC [ 1 J`：从开头擦除到光标。
    - `ESC [ 2 J`：擦除整个显示。
    - `ESC [ 3 J`：擦除包含在回滚缓冲区内的整个显示（自 Linux 3.0 起）。
    > 注意，`[3J` 仅擦除回滚缓冲区

#### ECMA-48 选择图形再现（SGR）

`ESC [ parameters m` 设置显示属性。  
可以在同一序列中设置多个属性，用分号分隔。空参数（位于分号之间、字符串起始符或终止符处）被解释为零。

- `0`  
    将所有属性重置为默认值。
    > 所有属性：粗细体、颜色

- `1`  
    设置粗体。

- `22`  
    设置正常强度。
    > 重置粗体与变暗

- `38`  
    后续为 256/24 位前景色，被塞入 16 种基本颜色（Linux 3.16 之前：开启下划线并设置默认前景色）。

命令 `38` 和 `48` 需要进一步参数：

- `;5;x`  
    256 色：值 `0..15` 为 IBGR（黑、红、绿、……、白），`16..231` 为 6×6×6 色立方，`232..255` 为灰度渐变。

- `;2;r;g;b`  
    24 位色，`r`/`g`/`b` 分量范围为 `0..255`。

## tput - 初始化终端、使用其能力或查询 terminfo 数据库


```sh
# 闪烁的光标

# 隐藏光标
tput civis
# 收到退出信号信号前恢复光标
trap "tput cnorm" EXIT

# 循环交替：显示与隐藏光标
while true; do
    tput cnorm
    sleep 0.6
    tput civis
    sleep 0.6
done
```

## 待使用

[python 标准库私有模块的无 curses 实现](https://github.com/python/cpython/tree/main/Lib/_pyrepl) 

https://invisible-island.net/xterm/ctlseqs/ctlseqs.html