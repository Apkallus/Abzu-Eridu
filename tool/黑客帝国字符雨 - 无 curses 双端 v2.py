#!/usr/bin/python3

from dataclasses import dataclass, field
from random import random as _random, choices as _choices, seed as _seed
from functools import cache  
from typing import NamedTuple  
from unicodedata import east_asian_width  
from shutil import get_terminal_size
from time import monotonic, sleep
from datetime import timedelta
import os
import sys
import subprocess
import signal
import gc

def info():
    """
黑客帝国绿色日文字符雨

- 新字符与突变  
    - 头部字符下落时，在下方创建新字符；头部不应为空格
    - 除空格外的字符，概率突变为新字符；空格保持到结束

- 列速度
    - 每列速度随机
    - 若同列拥有任何字符，则新头部使用相同速度
    - 当本列无任何字符时，列状态重置为随机

- 颜色与可见次数  
    - 字符原地绿色渐变，从亮到暗
        - 头部为白绿色的高亮
        - 中间渐变
        - 末尾设置隐藏字符，仅可被头部照亮
        - 高亮字符同时设置粗体
    - 颜色可见次数为普通颜色索引的显示次数
        - 正比于速度，速度快则颜色可见次数多
        - 高亮使用特殊设置
        
- 照亮辐射
    - 头部可照亮除本列外的其他字符
    - 被照亮字符使用：较亮（辐射亮度，自身颜色）
    - 多级辐射区域，范围、亮度中越近越亮
    - 辐射亮度上限为次高亮颜色索引

移除 curses 库时的参考
- https://github.com/python/cpython/tree/main/Lib/_pyrepl

性能
- profiling
    ```sh
    python3 -m profiling.sampling run --mode=cpu -r 20khz -d 60
    ```
    - curses
        ```log
        666129 function calls (126326 primitive calls) in 6.316 seconds

        nsamples  tottime persample cumtime persample filename:lineno(function)
            95464    4.773    0.000    4.773    0.000 testc.py:580(main)
            4073    0.204    0.000    0.204    0.000 testc.py:447(update_glow_coverage)
            3017    0.151    0.000    0.151    0.000 testc.py:231(do_render)
            2582    0.129    0.000    0.129    0.000 testc.py:275(do_render)
        5096/2467    0.123    0.000    0.255    0.000 testc.py:445(update_glow_coverage)
        1755/1754    0.088    0.000    0.088    0.000 testc.py:221(do_render)
        ```

    - nocurses_v1
        ```log
        258099 function calls (50955 primitive calls) in 2.548 seconds

        nsamples  tottime persample cumtime persample filename:lineno(function)
            7026    0.351    0.000    0.351    0.000 testa.py:712(refresh)
            4928    0.246    0.000    0.246    0.000 testa.py:618(update_glow_coverage)
        3810/3808    0.190    0.000    0.191    0.000 testa.py:404(do_render)
            3522    0.176    0.000    0.176    0.000 testa.py:684(refresh)
        2993/2992    0.150    0.000    0.150    0.000 testa.py:695(refresh)
        4887/2883    0.144    0.000    0.244    0.000 testa.py:616(update_glow_coverage)
        ```

    - nocurses_v2
        ```log
        193143 function calls (37861 primitive calls) in 1.893 seconds

        nsamples  tottime persample cumtime persample filename:lineno(function)
            5680    0.284    0.000    0.284    0.000 testb.py:697(refresh)
        10236/4811    0.241    0.000    0.512    0.000 testb.py:445(do_render)
        2634/2633    0.132    0.000    0.132    0.000 testb.py:680(refresh)
            1899    0.095    0.000    0.095    0.000 testb.py:656(napms)
            1822    0.091    0.000    0.091    0.000 testb.py:390(apply_glow)
            1306    0.065    0.000    0.065    0.000 testb.py:403(apply_glow)
        ```

- strace
    ```sh
    timeout 30 strace -c
    ```

    - curses
        ```log
        % time     seconds  usecs/call     calls    errors syscall
        ------ ----------- ----------- --------- --------- ------------------
        92.72    1.488015          17     87145           write
        4.65    0.074677          14      4980           poll
        0.93    0.014863          31       472         1 clock_nanosleep
        0.92    0.014761          14      1019           rt_sigaction
        0.14    0.002178           9       219        36 newfstatat
        0.11    0.001711          14       116           brk
        0.10    0.001570          14       107           read
        0.07    0.001185          16        74           mmap
        ------ ----------- ----------- --------- --------- ------------------
        100.00    1.604788          16     94535        52 total
        ```

    - nocurses_v1
        ```log
        % time     seconds  usecs/call     calls    errors syscall
        ------ ----------- ----------- --------- --------- ------------------
        17.70    0.008437           9       927           write
        15.31    0.007295           7       926         1 clock_nanosleep
        15.03    0.007163           7       940         1 ioctl
        13.93    0.006636           7       926           pselect6
        8.84    0.004213          13       315        42 newfstatat
        5.15    0.002454          16       145           read
        3.48    0.001656          17        97         5 openat
        3.24    0.001544          16        95           mmap
        2.95    0.001408          14        94           close
        2.95    0.001405          12       117           brk
        2.80    0.001334          13        98           fstat
        2.14    0.001021          12        79         3 lseek
        ------ ----------- ----------- --------- --------- ------------------
        100.00    0.047654           9      4911        56 total
        ```

    - nocurses_v2
        ```log
        % time     seconds  usecs/call     calls    errors syscall
        ------ ----------- ----------- --------- --------- ------------------
        15.87    0.009718          10       935           write
        14.16    0.008670           9       927           clock_nanosleep
        13.68    0.008378           9       928           pselect6
        13.02    0.007976           9       820       115 newfstatat
        11.96    0.007322           7       952         1 ioctl
        8.67    0.005309          13       408           read
        4.94    0.003028          12       245         7 openat
        4.24    0.002598          10       240           close
        3.54    0.002167          16       131           mmap
        3.32    0.002035           9       223           fstat
        2.51    0.001540           8       184         3 lseek
        ------ ----------- ----------- --------- --------- ------------------
        100.00    0.061240           9      6269       130 total
        ```

"""


@dataclass(slots=True)
class codes_obj:
    """
    terminfo 常量
    - 转义序列头  
        ESC（`0x1B`，`^[`）

    - DEC 私有模式序列  
        `ESC [ ? 25 h`  
    
    - ECMA-48 CSI 序列  
        `CSI`（或 `ESC [`）后跟一串参数
        - `H`（`CUP`）  
            将光标移到指定行、列（原点为 `1,1`）

        - `J`（`ED`）  
            擦除显示（默认：从光标到显示末尾）。
            - `ESC [ 2 J`：擦除整个显示。

    - ECMA-48 选择图形再现（SGR）  
        `ESC [ parameters m` 设置显示属性。  
    """
    cnorm: bytes = b'\x1b[?25h' # 光标可见
    civis: bytes  = b'\x1b[?25l' # 光标隐藏
    bk_screen_enter: bytes  = b'\x1b[?1049h' # 使用备用屏幕
    bk_screen_quit: bytes  = b'\x1b[?1049l' # 从备用屏幕恢复
    
    clean: bytes = b'\x1b[2J' # 全屏擦除
    clean_and_rollback: bytes = b'\x1b[3J' # 清除回滚区

    reset_attr: bytes = b'\x1b[0m' # 重置所有属性
    bold_code: bytes = b'1' # 设置粗体 
    bold: bytes = b'\x1b[1m' # 设置粗体 
    normel_code: bytes = b'22' # 设置正常体
    normel: bytes = b'\x1b[22m' # 设置正常体
    sgr_cube6_template: bytes = b'\x1b[38;5;%sm' # 颜色序列
    

    # 位置序列
    sgr_pos_template: bytes = b'\x1b[%d;%dH'
    sgr_pos_1: bytes = b'\x1b[H'

    # 组合
    init_screen_seq: bytes = b''.join([
        bk_screen_enter, # 进入备用屏幕
        reset_attr, # 重置 attr
        civis, # 隐藏指针
        sgr_pos_1, # 移动指针
    ])

    clear_screen_seq: bytes = b''.join([
        reset_attr, # 重置 attr
        civis, # 隐藏指针
        sgr_pos_1, # 移动指针
        clean_and_rollback, # 清空屏幕与回滚区
        clean, # 清空屏幕与回滚区
    ])

    clean_up_seq: bytes = b''.join([
        reset_attr, # 重置 attr
        sgr_pos_1, # 移动指针
        cnorm, # 显示指针
        clean_and_rollback, # 清空屏幕与回滚区
        clean, # 清空屏幕与回滚区
        bk_screen_quit, # 从备用屏幕恢复
    ])

def build_char_list(*args):
    """
    从 unicode 范围提取字符，输入十六进制字符串
    """
    res_char_list = []
    for arg in args:
        # 若为元组，则使用范围提取
        if isinstance(arg, tuple):
            start, end = arg
            res_char_list += [chr(i).encode() for i in range(int(start, 16), int(end, 16) + 1)]
        # 若为列表，则提取其中的单字符
        elif isinstance(arg, list):
            res_char_list += [chr(int(c, 16)).encode() for c in arg]
    return res_char_list


def random_choice_chunk(*args, **kwargs):
    """
    随机可迭代容器 choice 的批量模式
    ```
    yield from random.choices(...)
    ```
    """
    while True:
        yield from _choices(*args, **kwargs)
        # for i in _choices(*args, **kwargs):
        #     yield i

# 序列对象
CONSOLE_CODE = codes_obj()

# unicode 范围
# 作为头部的字符集
CHAR_LIST = build_char_list(
    # 全角片假名
    ("0x30A1", "0x30FA"), 
    # 全角字母
    ("FF21", "FF3A"), 
    # 全角数字
    ("FF10", "FF19"),
    # 全角非连续符号集合
    ["FF02", "FF0A", "FF0B", "FF0D", "FF0E", "FF1A", "FF1C", "FF1D", "FF1E", "FF3F", "FF5C"],
    # 半角非连续特殊字符集合
    ["1A15", "2D47", "10501"],
)

CHAR_LIST_IT = random_choice_chunk(CHAR_LIST, k=256)

# 作为体的字符集，空格不应位于头部
SPACE = "\u3000".encode() # 全角空格
SPACE_H = "\u0020".encode() # 半角空格
FULL_CHAR_LIST = CHAR_LIST + [SPACE]
FULL_CHAR_LIST_IT = random_choice_chunk(FULL_CHAR_LIST, k=256)

# 调试时的固定 random 种子
_seed('caffee')
# 若提高帧间隔，应当降低跳帧值（低渲染速度下，高跳帧值导致下落缓慢）
# 帧间隔
DELTA_TIME_S = timedelta(milliseconds=32).total_seconds()
# 设置跳帧值（每 N 帧更新一次），越小更新越频繁（快）
# 此处使用跳帧值的反比设置最大颜色显示次数，更快的头拥有更长的轨迹
FRAME_SKIPPING_RANGE = range(1, 4) 
FRAME_SKIPPING_IT = random_choice_chunk(FRAME_SKIPPING_RANGE, k=128)
FRAME_COUNTER_INIT = 1 # 初始帧数
HIGHLIGHT_SHOW_LIMIT = 1 # 高亮颜色的最大显示次数
MUT_CHAR = 0.1 # 字符突变几率，转为其他字符
MAX_HEAD = 2 # 每列最大头部数量
LAUNCH_RAT = 0.006 # 每列发动几率
CHAR_W = 2 # 全角字符宽度2
INVIS_NUM = 3 # 不可见颜色数量，位于尾部，仅被头部照亮               
GLOW_RING_COUNT = 3 # 衰减半径，头部照亮范围
MAX_BRIGHT = 1 # 最大辐射亮度，nocurses 1为次高光头部。
HEADER_DIST = 5 # 头部之间最小距离

INCREMENTAL = True # 增量更新开关。但 ascii 序列写入中使用相同移动与更新逻辑，当前全量也很接近增量

STDOUT_FD = sys.stdout.fileno()
STDIN_FD = sys.stdin.fileno()

QUIT_KEY = b'q'

"""
双平台设置
"""
# 双平台读取按键，懒加载库
platform_type = sys.platform

def platform_clean_up():
    pass

def platform_init_screen():
    pass

def platform_event_poll_read():
    pass

READ_LEN = 32

if platform_type.startswith('linux'):
    import select
    import tty
    import termios

    # 进入时，若当前 fd 连接到终端，则保存当前终端状态，禁用缓冲、用户输入立即生效
    SAVED_TERMIOS_ATTR = None
    if os.isatty(STDIN_FD):
        SAVED_TERMIOS_ATTR = tty.setcbreak(STDIN_FD)


    def platform_clean_up():
        """
        退出时，若 fd 连接到 tty，则恢复终端状态
        """
        if platform_type.startswith('linux') and SAVED_TERMIOS_ATTR:
            termios.tcsetattr(STDIN_FD, termios.TCSANOW, SAVED_TERMIOS_ATTR)

    # 注册轮询对象，等待数据读取
    POLL_OBJ = select.poll()
    POLL_OBJ.register(STDIN_FD, select.POLLIN)

    def platform_event_poll_read(time_sleep_s):
        """
        实际暂停时长 = 预期暂停时长 - 计算与渲染延迟
        - 输入即为事件，等待事件与休眠合并
        """
        key = None
        
        # s -> ms
        # 根据返回列表是否为空得到事件 flag
        key_flag = bool(POLL_OBJ.poll(time_sleep_s * 1000))

        # 若存在数据读取事件，则读取
        if key_flag:
            key = os.read(STDIN_FD, READ_LEN)

        return key
    
elif platform_type.startswith('win'):
    import msvcrt
    import ctypes
    import ctypes.wintypes as wintypes
    import _winapi

    def platform_init_screen():
        """
        设置控制台页编号到 UTF-8
        """
        subprocess.getstatusoutput('chcp 65001')

    # 库函数设置
    KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)

    class uChar_union(ctypes.Union):
        _fields_ = [
            ("UnicodeChar", wintypes.WCHAR),
            ("AsciiChar", wintypes.CHAR)
        ]

    class KEY_EVENT_RECORD(ctypes.Structure):
        """
        typedef struct _KEY_EVENT_RECORD {
            BOOL  bKeyDown;
            WORD  wRepeatCount;
            WORD  wVirtualKeyCode;
            WORD  wVirtualScanCode;
            union {
                WCHAR UnicodeChar;
                CHAR  AsciiChar;
            } uChar;
            DWORD dwControlKeyState;
        } KEY_EVENT_RECORD;
        """
        _fields_ = [
            ("bKeyDown", wintypes.BOOL),
            ("wRepeatCount", wintypes.WORD),
            ("wVirtualKeyCode", wintypes.WORD),
            ("wVirtualScanCode", wintypes.WORD),
            ("uChar", uChar_union),
            ("dwControlKeyState", wintypes.DWORD)
        ]

    class WINDOW_BUFFER_SIZE_RECORD(ctypes.Structure):
        """
        typedef struct _WINDOW_BUFFER_SIZE_RECORD {
            COORD dwSize;
        } WINDOW_BUFFER_SIZE_RECORD;
        """
        _fields_ = [("dwSize", wintypes._COORD)]

    class Event_union(ctypes.Union):
        _fields_ = [
            ("KeyEvent", KEY_EVENT_RECORD),
            ("WindowBufferSizeEvent", WINDOW_BUFFER_SIZE_RECORD)
        ]    

    KEY_EVENT = 0x0001
    class INPUT_RECORD(ctypes.Structure):
        """
        typedef struct _INPUT_RECORD {
            WORD  EventType;
            union {
                KEY_EVENT_RECORD          KeyEvent;
                MOUSE_EVENT_RECORD        MouseEvent;
                WINDOW_BUFFER_SIZE_RECORD WindowBufferSizeEvent;
                MENU_EVENT_RECORD         MenuEvent;
                FOCUS_EVENT_RECORD        FocusEvent;
            } Event;
        } INPUT_RECORD;
        """
        _fields_ = [
            ("EventType", wintypes.WORD),
            ("Event", Event_union)                
        ]

    """ 
    BOOL WINAPI ReadConsoleInput(
        _In_  HANDLE        hConsoleInput,
        _Out_ PINPUT_RECORD lpBuffer,
        _In_  DWORD         nLength,
        _Out_ LPDWORD       lpNumberOfEventsRead
    );
    """

    # 从控制台输入缓冲区读取数据，并将其从缓冲区删除。
    ReadConsoleInput = KERNEL32.ReadConsoleInputW

    ReadConsoleInput.restype = wintypes.BOOL
    ReadConsoleInput.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(INPUT_RECORD),
        wintypes.DWORD,
        wintypes.LPDWORD
    ]

    def getch():
        key = None
        if msvcrt.kbhit():
            # 平台统一为 bytes
            key = msvcrt.getwch().encode()
        return key

    WIN_STDIN_HANDLE = _winapi.GetStdHandle(_winapi.STD_INPUT_HANDLE)

    def platform_event_poll_read(time_sleep_s):
        """
        实际暂停时长 = 预期暂停时长 - 计算与渲染延迟
        """

        key = None
    
        # 等待信号或超时
        key_flag = _winapi.WaitForSingleObject(WIN_STDIN_HANDLE, int(time_sleep_s * 1000))

        if key_flag == _winapi.WAIT_OBJECT_0:
            rec_buff = (INPUT_RECORD * READ_LEN)()
            read_count = wintypes.DWORD()
            if not ReadConsoleInput(
                WIN_STDIN_HANDLE,
                rec_buff,
                READ_LEN,
                read_count
            ):
                raise WindowsError()
        
            """
            for (i = 0; i < cNumRead; i++)
            {
                switch(irInBuf[i].EventType)
                {
                    case KEY_EVENT: // keyboard input
                        KeyEventProc(irInBuf[i].Event.KeyEvent);
                        break;

                    case MOUSE_EVENT: // mouse input
                        MouseEventProc(irInBuf[i].Event.MouseEvent);
                        break;

                    case WINDOW_BUFFER_SIZE_EVENT: // scrn buf. resizing
                        ResizeEventProc( irInBuf[i].Event.WindowBufferSizeEvent );
                        break;

                    case FOCUS_EVENT:  // disregard focus events

                    case MENU_EVENT:   // disregard menu events
                        break;

                    default:
                        ErrorExit("Unknown event type");
                        break;
                }
            }
            """    
            char_list = []
            for i in range(read_count.value):
                rec = rec_buff[i]
                # 若事件非按键，跳过
                if rec.EventType != KEY_EVENT:
                    continue

                key_event = rec.Event.KeyEvent
                # 若按键事件非按下，跳过
                if not key_event.bKeyDown:
                    continue

                # 添加结构中的字符
                ch = key_event.uChar.UnicodeChar
                char_list.append(ch)

            key = ''.join(char_list).encode() or None

        return key

class Pos(NamedTuple):
    y: int
    x: int


def rgb_cube6(r, g, b):  
    """
    256 色：值 `0..15` 为 IBGR（黑、红、绿、……、白），`16..231` 为 6*6*6 色立方，`232..255` 为灰度渐变。
    - r 6**2
    - g 6**1
    - b 6**0
    """
    return str(16 + 36*r + 6*g + b).encode()

@dataclass(slots=True)
class color_and_buff_obj:
    # 预构建颜色序列
    color_256_list: list[bytes|None] = field(default_factory=list) 
    # 预构建属性+颜色组合序列
    # {属性{颜色}}
    attr_color_dict: dict = field(default_factory=dict) 
    max_visible_color_index: int = 0
    max_pair_index: int = 0
    highlight_index: int = 0
    # 行级列表，索引为行号，当前列遍历时从左向右，逐列添加时自然有序
    # 行索引[列索引，字符，颜色，属性]，此处使用固定长度的连续元素到行级列表内，按照步进读取。而非作为元组或列表嵌套
    buff: list = field(default_factory=list) 

@dataclass(slots=True)
class element_obj:
    """
    每个字符元素
    - color_show_count  
        每个颜色出现的次数
    """
    pos: Pos
    char: bytes
    color_index: int = 0 # 颜色序列索引，nocurses 初始化为0
    color_show_count: int = 0 # 每个颜色的显示次数

    # 增量更新字段，可设置为继承并同名覆盖的子类，但仅简单设置为单类的字段。当前全量也使用这些字段
    last_render_char: str | None = None # 之前渲染字符
    last_render_color: int | None = None # 之前渲染颜色
    last_render_attr: int | None = None # 之前渲染属性

@dataclass(slots=True)
class col_obj:
    """
    列状态，保存本列的元素列表
    """
    col_index: int # 列索引
    col_x: int # 列位置
    char_dict: dict[Pos, element_obj] = field(default_factory=dict) # 追踪所有字符位置，颜色遍历完成后移除
    header_dict: dict[int, Pos] = field(default_factory=dict) # 追踪新生头所在行，到底部时移除
    _next_head_id: int = 0 # 下个 head 的序号
    frame_skip: int = 0 # 跳帧数（速度）
    cur_frame: int = 0 # 当前帧数（达到跳帧数时更新）
    color_show_limit: int = 0 # 每个颜色序列的最大显示次数
    rm_char_list: list[element_obj] = field(default_factory=list) # 被移除字符的列表
    
@dataclass(slots=True)
class glow_obj:
    """
    保存辐射环信息：环、亮度
    - 覆盖范围的构建 set + in set -> 每列临近头部列表 + 普通运算
    """
    ring: int = 0 # 辐射环到头部的距离
    bright: int = 0 # 辐射亮度

def init_colors():  
    """
    设置颜色对：创建一批绿色渐变前景色，背景色为默认，从亮到暗。  
    g=0 时几乎为灰色，选取 5-1  
    rgb(4,5,4) 几乎为白色，选取 (3,5,3) 白绿色头部  
    添加 (1,5,1) 作为次高光，余烬最大等级可为次高光
    """
    style_bold = CONSOLE_CODE.bold
    style_normel = CONSOLE_CODE.normel
    style_bold_code = CONSOLE_CODE.bold_code
    style_normel_code = CONSOLE_CODE.normel_code
    color_temp = CONSOLE_CODE.sgr_cube6_template

    color_and_buff = color_and_buff_obj()
    highlight_green = [(3,5,3), (1,5,1)]
    linear_green = [(0, green, 0) for green in range(5, 0, -1)]
    color_rgb_list = highlight_green + linear_green

    for idx, rgb in enumerate(color_rgb_list):  
        # 普颜色序列
        color_seq = color_temp % rgb_cube6(*rgb)
        color_and_buff.color_256_list.append(color_seq)
        # 预构建属性+颜色组合序列
        color_and_buff.attr_color_dict[(color_seq, style_bold)] = color_temp % (rgb_cube6(*rgb) + b';' + style_bold_code)
        color_and_buff.attr_color_dict[(color_seq, style_normel)] = color_temp % (rgb_cube6(*rgb) + b';' + style_normel_code)

    # 更新颜色计数
    color_and_buff.max_visible_color_index = len(color_and_buff.color_256_list) - 1

    for _ in range(INVIS_NUM):
        # 设置之后被隐藏的额外色
        color_and_buff.color_256_list.append(None)

    # max_pair_index 包含不可见
    color_and_buff.max_pair_index = len(color_and_buff.color_256_list) - 1
    # 最大高光索引
    color_and_buff.highlight_index = len(highlight_green) - 1

    return color_and_buff



WIDE_SET = ('W', 'F')
@cache
def as_wide_char(ch: bytes):
    # 广义上，宽字符包括 W、F 和 A（在东亚语境下），而窄字符则包括 N、Na、H 和 A（不在东亚语境下）。
    return True if east_asian_width(ch.decode()) in WIDE_SET else False


def apply_glow(near_headers: list[tuple], linear_bright_list, y, cur_render_color_idx):
    # 遍历附近头部
    for header_y, e_delta_x in near_headers:

        # 对于本列，元素仅被下方头部照亮。
        if e_delta_x == 0:
            e_delta_y = header_y - y
            # 若位于下方、被照亮
            if 0 < e_delta_y <= GLOW_RING_COUNT:
                # 若更亮，则更新当前颜色索引
                glow_color_idx = linear_bright_list[e_delta_y - 1]
                if glow_color_idx < cur_render_color_idx:
                    cur_render_color_idx = glow_color_idx

        # 对于附近列
        else:
            e_delta_y = abs(header_y - y) 
            # 若距离过远，则跳过
            if e_delta_y > GLOW_RING_COUNT:
                continue

            # 若更亮，则更新当前颜色索引
            e_r = max(e_delta_y, e_delta_x)
            glow_color_idx = linear_bright_list[e_r - 1]
            if glow_color_idx < cur_render_color_idx:
                cur_render_color_idx = glow_color_idx
                
    return cur_render_color_idx

def do_render(color_and_buff: color_and_buff_obj, col: col_obj, linear_bright_list: list[int],
             near_header_list: list[list]):
    """
    渲染字符
    - 若字符作为头部，设置粗体
    - 若字符作为余烬被头部照亮，当前亮度为自身亮度 ~ 辐射亮度的最亮值
    - 若字符未被照亮，仅设置当前状态
        - 若字符作为末尾隐藏颜色序列，则隐藏
    
    性能优化，结构清晰度 > 性能调整
    - 迭代元素视图取字段 -> 对元素视图进行分类集合运算，更多开销
        - 迭代元素直接访问数据类字段
        - 分类集合运算创建多个中间视图，再迭代多个分类视图本身，开销仍超过判断分支减少的收益
    - 构建 GLOW_RING_COUNT 个大 set + set 成员查询 -> 每列构建临近头部指针列表 + 每个元素遍历
        - 构建 set  -> 构建 指针list  
            开销减小，仅添加到列表
        - hash 成员查询 -> 普通运算
            开销减小
    """
    near_headers = near_header_list[col.col_index]
    hl_idx = color_and_buff.highlight_index
    vc_idx = color_and_buff.max_visible_color_index
    render_buff = color_and_buff.buff
    color_list = color_and_buff.color_256_list


    for e in col.char_dict.values(): 
        # 记录字符与当前颜色索引
        cur_render_char = e.char
        cur_render_color_idx = e.color_index
        y, x = e.pos

        # 若字符作为非高亮索引的余烬
        if cur_render_color_idx > hl_idx:

            cur_render_color_idx = apply_glow(near_headers, linear_bright_list, y, cur_render_color_idx)

        # 设置默认 style 为普通体
        attr = CONSOLE_CODE.normel

        # 增量更新与全量渲染差异
        if INCREMENTAL:

            # 增量更新时，若字符与可见颜色未变化，则跳过。此处由颜色隐含基于其设置的属性
            # 若字符、颜色在上一帧存在且未变化，跳过
            if e.last_render_color is not None and cur_render_char == e.last_render_char and e.last_render_color == cur_render_color_idx:
                continue

            # 若字符为隐藏颜色序列
            # 增量更新时，设置一次补丁空格：不对上一帧的隐藏状态设置字符，以减少 addch/addstr 调用
            if cur_render_color_idx > vc_idx:

                # 增量更新时，若上一帧渲染为隐藏，跳过。实际字符变化时，由于隐藏颜色索引仍跳过
                if e.last_render_char == SPACE:
                    continue

                # 增量更新时，第一次则设置隐藏属性或空格
                cur_render_char = SPACE
            
            # 若字符为高亮索引，设置粗体
            elif cur_render_color_idx <= hl_idx:
                attr = CONSOLE_CODE.bold

            # 此处汇集增量无法跳过隐藏、高亮、余烬
            
            # 保存元素最终渲染的字符、颜色，到增量陈旧状态字段
            e.last_render_char, e.last_render_color, e.last_render_attr = cur_render_char, cur_render_color_idx, attr

            # 增量需额外添加全角/半角的转换（全量直接擦除所有）：
            # 若当前字符为半角，则添加半角空格，并且作为字符串写入
            if not as_wide_char(cur_render_char):
                # 半角空格位于实际字符 x+1 处，删除时仅需设置一个全角空格，而无需再次区分（当前字符在左，空格在右）
                render_buff[y].extend((x + 1, SPACE_H, color_list[cur_render_color_idx], attr))

            render_buff[y].extend((x, cur_render_char, color_list[cur_render_color_idx], attr))

        # # 全量渲染
        else:

            # 若字符为隐藏颜色序列
            # 全量重绘时，仅绘制显示的字符：不设置隐藏字符，以减少 addch 调用
            if cur_render_color_idx > vc_idx:
                continue 
            
            # 若字符为高亮索引，设置粗体
            elif cur_render_color_idx <= hl_idx:
                attr = CONSOLE_CODE.bold

            # 保存元素最终渲染的字符、颜色，到陈旧状态字段
            e.last_render_char, e.last_render_color, e.last_render_attr = cur_render_char, cur_render_color_idx, attr

            # 此处汇集被渲染的高亮、余烬
            render_buff[y].extend((x, cur_render_char, color_list[cur_render_color_idx], attr))       

def render_rm_patch(color_and_buff: color_and_buff_obj, col: col_obj, header_list: list[Pos]): 
    render_buff = color_and_buff.buff
    color_list = color_and_buff.color_256_list
    header_pos = header_list[col.col_index]

    # 若移除字符位置并非新创头部，则设置空格补丁覆盖
    for rm_element in col.rm_char_list:
        if rm_element.pos not in header_pos:
            color = color_list[rm_element.last_render_color]
            y, x = rm_element.pos
            render_buff[y].extend((x, SPACE, color, rm_element.last_render_attr))

    # 补丁完成后，清空移除字符列表
    col.rm_char_list.clear()

def update_char(col: col_obj, color_and_buff: color_and_buff_obj): 
    """
    直到元素颜色渐变完成前，持续更新颜色序列、显示次数、字符突变
    """
    # 性能：重复被引用的字段绑定到本地
    max_pair_index = color_and_buff.max_pair_index
    highlight_index = color_and_buff.highlight_index
    rm_char_list = col.rm_char_list
    char_dict = col.char_dict
    color_show_limit = col.color_show_limit
    # 重置列帧数
    col.cur_frame = FRAME_COUNTER_INIT

    # 若增量更新，重置列移除元素列表。从字典快照修改为末尾移除后，全量更新也使用此容器
    rm_char_list.clear()

    # 更新元素
    # 遍历字典，收集待删除 key。之后连续移除。而非建立 list 快照后移除
    for pos, e in char_dict.items():
        
        # 设置随机字符突变。空格不参与突变，一旦突变为空格则持续到消亡
        if e.char != SPACE and _random() < MUT_CHAR:
            e.char = next(FULL_CHAR_LIST_IT)

        # 更新元素颜色次数
        e.color_show_count += 1
        # 若颜色次数达到上限（普通颜色或高亮颜色）：更新颜色索引，并设置颜色次数为0
        # 预期多种构造：预构建颜色列表，移除显示次数；转移显示次数而设置到颜色对象中的状态
        if e.color_show_count >= color_show_limit \
            or (e.color_index <= highlight_index and e.color_show_count >= HIGHLIGHT_SHOW_LIMIT):

            # 若颜色列表尚未完成，则继续更新索引
            if e.color_index < max_pair_index:
                e.color_index += 1
                e.color_show_count = 0
            # 若当前元素消亡，移除
            else:
                # 添加消亡元素到保存列表
                # 增量/全量更新，均在之后移除字典元素
                rm_char_list.append(char_dict[pos])

    # 连续移除待删除元素
    for rm_pos in rm_char_list:
        del char_dict[rm_pos.pos]

def help_build_header(pos: Pos, col: col_obj, next_head_id: int):
    # 加载头部字符（位置、字符、属性）到元素字典
    col.char_dict[pos] = element_obj(pos, next(CHAR_LIST_IT))
    # 加载头部字符，到头部字典
    col.header_dict[next_head_id] = pos

def set_header(col: col_obj):
    """
    新生字符
    - 若无任何字符时，初始化列
    - 初始化或继续下落，均创建一个新生字符
    """

    # 若初始化列
    if not col.char_dict: # if len(col.char_dict) == 0:

        # 设置列速度，初始化帧数
        col.frame_skip = next(FRAME_SKIPPING_IT)
        # 速度越快，拖尾越长
        col.color_show_limit = len(FRAME_SKIPPING_RANGE) - col.frame_skip + 1 
        # 初始化帧
        col.cur_frame = FRAME_COUNTER_INIT


    # 设置初始下落字符位置，y 固定为最上方，也可修改为随机行
    header_pos = Pos(0, col.col_x)

    # 加载头部字符（位置、字符、属性）到元素与头部字典
    help_build_header(header_pos, col, col._next_head_id)

    col._next_head_id += 1

def update_header(col: col_obj, max_y):
    """
    更新列的头部，创建新头
    """
    for key in list(col.header_dict):
        nexrow_y = col.header_dict[key].y + 1

        # 若头未到达底部，则继续下落
        if nexrow_y <= max_y:
            new_pos = Pos(y=nexrow_y, x=col.col_x)
            help_build_header(new_pos, col, key)
            
        # 否则移除
        else:
            del col.header_dict[key]

def linear_gradient(layer, color_list):
    """
    在颜色范围的颜色渐变，等距采样
    至少为最亮的1个颜色  
    2个时，额外包含最暗的1个颜色  
    更多时，取中间  
    """
    # 最大索引 max_e
    max_e = len(color_list) - 1
    # 切割分母 max_i
    max_i = layer - 1
    # 若不切割，直接返回首个元素
    if max_i == 0:  
        return [color_list[0]]     
    # 模型1：i/max_i * max_e 分数切割比例递增，固定长度
    # 模型2: i*max_e / max_i 整数长度倍增，切割比例固定
    return [color_list[round((i / max_i * max_e))] 
            for i in range(layer)]

def build_linear_bright_list(max_visible_color_index):
    # 可用辐射亮度列表 -> 渐变辐射亮度列表
    available_bright_range = range(MAX_BRIGHT, max_visible_color_index + 1)
    linear_bright_list = linear_gradient(GLOW_RING_COUNT, available_bright_range)

    return linear_bright_list

def has_header_dist(col: col_obj):
    """
    - True
        - 当不存在任何头部时
        - 当存在头部，且在距离外
    - False
        - 当存在头部，且在距离内
    """
    res = True
    # 无头部时头部列表为空，返回 True
    for header_pos in col.header_dict.values():
        if header_pos.y < HEADER_DIST:
            res = False
            break
    return res


@cache
def build_pos_seq(y, x):
    # 写入时向右下 ↘ 偏移
    return CONSOLE_CODE.sgr_pos_template % (y+1, x+1)

def refresh(color_and_buff: color_and_buff_obj):
    """
    性能
    - write 容器
        - bytearray > list + join  
            虽然 list 已为指针复制，最后合并。但字节组性能略高
    - 分支
        - if...else > match...case   
            简单的 if 性能略高于需构建元组的 match
    """
    write_list = bytearray()
    render_buff = color_and_buff.buff
    
    cur_y, cur_x = None, None
    # 字符总是发送，不参与比较
    cur_color, cur_attr = None, None
    for y, line in enumerate(render_buff):
        # 跳过空行
        if not line: # len(line) == 0:
            continue

        # 4元素固定步长读取，可包装为类 batched 的迭代器
        for i in range(0, len(line), 4):
            x, char, color, attr = line[i],line[i+1],line[i+2],line[i+3] # line[i:i+4]
            # 当光标位置不连续时发送位置序列
            if cur_y is None or cur_y != y or cur_x != x:
                pos_seq = build_pos_seq(y, x) 
                write_list += pos_seq
                cur_y, cur_x = y, x+2

            attr_flag = attr and attr != cur_attr
            color_flag = color and color != cur_color

            # 当状态与颜色都不连续时发送合并序列
            if attr_flag and color_flag:
                write_list += color_and_buff.attr_color_dict[(color, attr)]

            # 当状态不连续时发送状态序列
            elif attr_flag:
                write_list += attr

            # 当颜色不连续时发送颜色序列
            elif color_flag:
                write_list += color

            # 总是发送字符。上述条件可减少同状态的序列数
            write_list += char

            cur_color, cur_attr = color, attr
                
    os.write(STDOUT_FD, write_list)

    # 清空 buff
    for line in render_buff:
        line.clear()

def init_screen():
    os.write(STDOUT_FD, CONSOLE_CODE.init_screen_seq)

    platform_init_screen()

def clear_screen():
    os.write(STDOUT_FD, CONSOLE_CODE.clear_screen_seq)

def clean_up():
    """
    注册为普通与异常处理器
    """
    os.write(STDOUT_FD, CONSOLE_CODE.clean_up_seq)

    platform_clean_up()

signal_stop = False
def signal_handler(*args):
    global signal_stop
    signal_stop = True

def sign_signal():
    """
    注册各种中断信号到信号处理器，仅设置循环开关
    - 设置 sys.exit 将导致 profiling.sampling 导出性能数据时被中断
    - 退出循环后，由 finally 清理
    """
    sig_list = [
        signal.SIGTERM, # 终止
        signal.SIGINT, # 中断 Ctrl + C
    ]

    for sig in sig_list:
        signal.signal(sig, signal_handler)

def update_near_header_list(col_list: list[col_obj], header_list: list[Pos], col_list_len, near_header_list: list[list[tuple]]):
    """
    每列构建临近头部列表，替代原版的一个大集合
    """
    for near_header in near_header_list:
        near_header.clear()

    for col in col_list:
        near_cols_start = max(col.col_index - GLOW_RING_COUNT, 0)
        near_cols_end = min(col.col_index + GLOW_RING_COUNT, col_list_len - 1)
        
        # 获取当前列附近的范围，不超过边界。注意坐标与列位置的转换           
        for i in range(near_cols_start, near_cols_end + 1):
            # 排除无头部列
            headers = header_list[i]
            if not headers:
                continue

            for header in headers:
                # 添加到临近头部列表，[y, e_delta_x] 
                e_delta_x = abs(col.col_index - i)
                near_header_list[col.col_index].append((header.y, e_delta_x))

def event_sleep_ms(frame_begin_time_s):
    """
    实际暂停时长 = 预期暂停时长 - 计算与渲染延迟
    - 输入即为事件，等待事件与休眠合并
    """
    key = None
    
    time_delay_s = monotonic() - frame_begin_time_s
    time_sleep_s = DELTA_TIME_S - time_delay_s

    # 休眠剩余时间，若渲染超出设置的帧间隔，则立即渲染。
    # 同时等待数据读取
    if time_sleep_s > 0:
        # s -> ms
        key = platform_event_poll_read(time_sleep_s)

    return key
    
def main():

    # 注册信号
    sign_signal()

    # 初始化屏幕
    init_screen()

    # 初始化颜色对
    color_and_buff = init_colors()

    # 初始化辐射环配置
    linear_bright_list = build_linear_bright_list(color_and_buff.max_visible_color_index)

    # 初始化终端大小
    terminal_size = get_terminal_size()

    # 列状态，全角字符宽度为2
    # 初始化行、列为 max - 1
    def init_col(terminal_size):
        col_list = [col_obj(i, x) for i, x in enumerate(range(0, terminal_size.columns - 1, CHAR_W))]
        return col_list
    
    col_list = init_col(terminal_size)
    col_list_len = len(col_list)
    max_y = terminal_size.lines - 1

    # 初始化行级 buff
    def init_buff(terminal_size):
        color_and_buff.buff = [[] for _ in range(0, terminal_size.lines)]
    
    init_buff(terminal_size)

    def init_near_header_list():
        near_header_list = [[] for _ in range(col_list_len)]
        return near_header_list

    near_header_list = init_near_header_list()

    # 停止跟踪，调高回收阈值
    gc.freeze()
    _, threshold1, threshold2 = gc.get_threshold()
    gc.set_threshold(50_000, threshold1, threshold2)

    while not signal_stop:

        # 计时
        frame_begin_time_s = monotonic()

        # 若终端大小改变
        test_terminal_size = get_terminal_size()
        if terminal_size != test_terminal_size:
            # 清空屏幕
            clear_screen()

            # 更新行列大小
            terminal_size = test_terminal_size

            # 重置，或修改为继承之前列再添加/移除
            col_list = init_col(terminal_size)
            max_y = terminal_size.lines - 1
            col_list_len = len(col_list)

            init_buff(terminal_size)

            near_header_list = init_near_header_list()

        # 全量重绘时每帧清空屏幕
        if not INCREMENTAL:
            clear_screen()

        # 遍历列，应用每列的元素到画布
        # 分离渲染与更新，实现变速效果

        # 更新与创建新头
        for col in col_list:

            # 若列存在任何字符，则更新
            if col.char_dict: # len(col.char_dict) > 0:
                # 每 N 帧更新
                if col.cur_frame >= col.frame_skip:
                    update_char(col, color_and_buff)
                    # 若未到达底部，则继续下落
                    update_header(col, max_y)

                # 递增帧计数
                else:
                    col.cur_frame += 1

            # 若列头部数量未达上限，且之前的头不在初始位置附近，则随机创建新头
            if len(col.header_dict) < MAX_HEAD and has_header_dist(col) and _random() < LAUNCH_RAT:
                set_header(col)

        # 多处被使用的头部列表
        header_list: list = [col.header_dict.values() for col in col_list]
        update_near_header_list(col_list, header_list, col_list_len, near_header_list)
   
        # 列与辐射范围更新后，每轮渲染
        for col in col_list:

            # 若列存在任何字符，则渲染
            if col.char_dict:  # len(col.char_dict) > 0: 
                do_render(color_and_buff, col, linear_bright_list, near_header_list)

            # 对于增量模式，若存在任何移除字符，则补丁移除。每次清空移除列表，省略模式判断
            if col.rm_char_list: # len(col.rm_char_list) > 0:
                render_rm_patch(color_and_buff, col, header_list)

        # 刷新
        refresh(color_and_buff)
        
        # 等待事件并休眠
        key = event_sleep_ms(frame_begin_time_s) 
        # 若收到键盘 `q` 则退出
        if key and QUIT_KEY in key:
            break
try:
    main()
    
# except:
#     pass

finally:
    clean_up()
