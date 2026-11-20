#!/usr/bin/python3

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
    - vscode 控制台无法区分侧边高亮与全高亮，此处仅使用全高亮

移除 curses 库时的参考
- https://github.com/python/cpython/tree/main/Lib/_pyrepl

已使用预构建列表替换 `from functools import cache` 的 @cache 装饰器
"""

from dataclasses import dataclass, field
from random import random as _random, choices as _choices, seed as _seed
from typing import NamedTuple  
from unicodedata import east_asian_width  
from shutil import get_terminal_size
from time import monotonic
from datetime import timedelta
from collections.abc import Sequence, Iterable
import os
import sys
import signal
import gc

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
    bold_code: int = 1 # 设置粗体 
    bold: bytes = b'\x1b[1m' # 设置粗体 
    normal_code: int = 22 # 设置正常体
    normal: bytes = b'\x1b[22m' # 设置正常体
    sgr_cube6_template: bytes = b'\x1b[38;5;%sm' # 颜色序列
    style_dict: dict[int, bytes] = field(default_factory=dict[int, bytes]) # style code 与字节的字典
    
    # 位置序列
    sgr_pos_template: bytes = b'\x1b[%d;%dH'
    sgr_pos_1: bytes = b'\x1b[H'
 
    # 组合，不进行 init，使用 __post_init__ 构建
    init_screen_seq: bytes = field(init=False) 
    clear_screen_seq: bytes = field(init=False) 
    clean_up_seq: bytes = field(init=False) 

    def __post_init__(self) -> None:
        """
        __post_init__ 使用已有常量字段构建组合字段
        """
        self.style_dict = {
            self.bold_code: self.bold,
            self.normal_code: self.normal
        }

        self.init_screen_seq = b''.join([
            self.bk_screen_enter, # 进入备用屏幕
            self.reset_attr, # 重置 attr
            self.civis, # 隐藏指针
            self.sgr_pos_1, # 移动指针
        ])

        self.clear_screen_seq = b''.join([
            self.reset_attr, # 重置 attr
            self.civis, # 隐藏指针
            self.sgr_pos_1, # 移动指针
            self.clean_and_rollback, # 清空屏幕与回滚区
            self.clean, # 清空屏幕与回滚区
        ])

        self.clean_up_seq = b''.join([
            self.reset_attr, # 重置 attr
            self.sgr_pos_1, # 移动指针
            self.cnorm, # 显示指针
            self.clean_and_rollback, # 清空屏幕与回滚区
            self.clean, # 清空屏幕与回滚区
            self.bk_screen_quit, # 从备用屏幕恢复
        ])

CHAR_W = 2 # 全角字符宽度2

WIDE_SET = ('W', 'F')
def is_wide_char(ch: str|bytes):
    """
    是否为全角字符
    """
    # 广义上，宽字符包括 W、F 和 A（在东亚语境下），而窄字符则包括 N、Na、H 和 A（不在东亚语境下）。
    if isinstance(ch, bytes):
        ch = ch.decode()
    return east_asian_width(ch) in WIDE_SET

def build_char_list(*args):
    """
    从 unicode 范围提取字符，输入十六进制字符串
    """
    res_char_list = []
    for arg in args:
        int_list = arg
        # 若为元组，则转为迭代型。与列表类型归一
        if isinstance(arg, tuple):
            start, end = arg
            int_list = range(start, end + 1)

        # 十六进制转字符，设置字符与字符宽度
        for i in int_list:
            cur_char = chr(i)
            res_char_list.append((cur_char.encode(), CHAR_W if is_wide_char(cur_char) else 1))
                              
    return res_char_list


def random_choice_chunk(*args, **kwargs):
    """
    随机可迭代容器 choice 的批量模式
    ```
    for i in _choices(*args, **kwargs):
        yield i
    ```
    """
    while True:
        yield from _choices(*args, **kwargs)


# 序列对象
CONSOLE_CODE = codes_obj()

# unicode 范围
# 作为头部的字符集
CHAR_STR_LIST = [
    # 全角片假名
    (0x30A1, 0x30FA), 
    # 全角字母
    (0xFF21, 0xFF3A), 
    # 全角数字
    (0xFF10, 0xFF19),
    # 全角非连续符号集合
    [0xFF02, 0xFF0A, 0xFF0B, 0xFF0D, 0xFF0E, 0xFF1A, 0xFF1C, 0xFF1D, 0xFF1E, 0xFF3F, 0xFF5C],
    # 半角非连续特殊字符集合
    [0x1A15, 0x2D47, 0x10501], 
]
# 构建 bytes 列表，与随机迭代器
CHAR_LIST = build_char_list(*CHAR_STR_LIST)
CHAR_LIST_IT = random_choice_chunk(CHAR_LIST, k=256)

# 作为体的字符集，空格不应位于头部
SPACE = "\u3000".encode() # 全角空格
SPACE_H = "\u0020".encode() # 半角空格
FULL_CHAR_LIST = CHAR_LIST + [(SPACE, CHAR_W)]
FULL_CHAR_LIST_IT = random_choice_chunk(FULL_CHAR_LIST, k=256)

# 调试时的固定 random 种子
# _seed('caffee')
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

INVIS_NUM = 3 # 不可见颜色数量，位于尾部，仅被头部照亮。同样基于速度缩放
GLOW_RING_COUNT = 3 # 衰减半径，头部照亮范围
MAX_BRIGHT = 1 # 最大辐射亮度，nocurses 1为次高光头部。
HEADER_DIST = 5 # 头部之间最小距离

INCREMENTAL = True # 增量更新开关。但 ascii 序列写入中使用相同移动与更新逻辑，当前全量也很接近增量

STDOUT_FD = sys.stdout.fileno()
STDIN_FD = sys.stdin.fileno()

QUIT_KEY = b'q' # 退出键

COL_ATTR_SHIFT = 8 # 颜色与属性组合 key 的位移

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

def platform_sign_signal():
    pass

# 按键事件读取大小
READ_LEN = 32

# 窗口变化事件 flag
WIN_SIZE_CHANGE_FLAG = False

def terminal_size_change(*args, **kwargs):
    """
    窗口变化事件时，设置全局变量
    - linux 注册信号
    - windows 使用事件
    """
    global WIN_SIZE_CHANGE_FLAG
    WIN_SIZE_CHANGE_FLAG = True

if platform_type == 'linux':
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

    def platform_sign_signal():
        """
        窗口变化
        """
        signal.signal(signal.SIGWINCH, terminal_size_change)

elif platform_type == 'win32':
    import ctypes
    import ctypes.wintypes as wintypes
    import _winapi

    # 库函数设置
    KERNEL32 = ctypes.WinDLL("kernel32", use_last_error=True)

    def platform_init_screen():
        """
        设置控制台页编号到 UTF-8
        """
        # subprocess.getstatusoutput('chcp 65001')
        KERNEL32.SetConsoleOutputCP(wintypes.UINT(65001))
        
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

    # 事件常量
    KEY_EVENT = 0x0001
    WINDOW_BUFFER_SIZE_EVENT = 0x0004  
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

    WIN_STDIN_HANDLE = _winapi.GetStdHandle(_winapi.STD_INPUT_HANDLE)

    def platform_event_poll_read(time_sleep_s):
        """
        实际暂停时长 = 预期暂停时长 - 计算与渲染延迟
        - 事件
            - 按键
            - 窗口大小调整
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
                raise RuntimeError()
        
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
                # 按键事件
                if rec.EventType == KEY_EVENT:

                    # 若按键事件非按下，跳过
                    key_event = rec.Event.KeyEvent
                    if not key_event.bKeyDown:
                        continue

                    # 添加结构中的字符
                    ch = key_event.uChar.UnicodeChar
                    char_list.append(ch)

                # 窗口大小变化事件
                elif rec.EventType == WINDOW_BUFFER_SIZE_EVENT:
                    terminal_size_change()

            key = None
            if char_list:
                key = ''.join(char_list).encode()

        return key

else:
    raise NotImplementedError()

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
    return str(16 + 36*r + 6*g + b)

@dataclass(slots=True)
class color_obj:
    # 预构建颜色序列
    color_256_list: list[bytes|None] = field(default_factory=list) 
    # 预构建属性+颜色组合序列
    # {属性{颜色}}
    attr_color_dict: dict = field(default_factory=dict) 
    max_visible_color_index: int = 0
    max_pair_index: int = 0
    highlight_index: int = 0
    # 渐变颜色
    linear_bright_list: list = field(default_factory=list) 

@dataclass(slots=True)
class element_obj:
    """
    每个字符元素
    - color_show_count  
        每个颜色出现的次数
    """
    pos: Pos
    char: bytes
    char_len: int
    color_index: int = 0 # 颜色序列索引，nocurses 初始化为0
    color_show_count: int = 0 # 每个颜色的显示次数

    # 增量更新字段，可设置为继承并同名覆盖的子类，但仅简单设置为单类的字段。当前全量也使用这些字段
    last_render_char: bytes | None = None # 之前渲染字符
    last_render_color_idx: int | None = None # 之前渲染颜色
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
    
def init_colors():  
    """
    设置颜色对：创建一批绿色渐变前景色，背景色为默认，从亮到暗。  
    vscode 的默认调色下 g=0 时几乎为灰色，选取 5-1。但 windows 终端仍可显示为暗绿色
    rgb(4,5,4) 几乎为白色，选取 (3,5,3) 白绿色头部  
    添加 (1,5,1) 作为次高光，余烬最大等级可为次高光
    """
    style_bold_code = CONSOLE_CODE.bold_code
    style_normal_code = CONSOLE_CODE.normal_code
    color_temp = CONSOLE_CODE.sgr_cube6_template

    color_conf = color_obj()
    highlight_green = [(3,5,3), (1,5,1)]
    linear_green = [(0, green, 0) for green in range(5, 0, -1)]
    color_rgb_list = highlight_green + linear_green

    for color_idx, rgb in enumerate(color_rgb_list):  
        # 普通颜色序列
        rgb_256_str = rgb_cube6(*rgb)
        color_conf.color_256_list.append(color_temp % rgb_256_str.encode())
        
        # 预构建属性+颜色组合序列,位移拼接作为 key
        color_conf.attr_color_dict[(color_idx << COL_ATTR_SHIFT) | style_bold_code] = color_temp % (f'{rgb_256_str};{style_bold_code}'.encode())
        color_conf.attr_color_dict[(color_idx << COL_ATTR_SHIFT) | style_normal_code] = color_temp % (f'{rgb_256_str};{style_normal_code}'.encode())

    # 更新颜色计数
    color_conf.max_visible_color_index = len(color_conf.color_256_list) - 1

    for _ in range(INVIS_NUM):
        # 设置之后被隐藏的额外色
        color_conf.color_256_list.append(None)

    # max_pair_index 包含不可见
    color_conf.max_pair_index = len(color_conf.color_256_list) - 1
    # 最大高光索引
    color_conf.highlight_index = len(highlight_green) - 1

    # 初始化辐射环渐变颜色
    color_conf.linear_bright_list = build_linear_bright_list(color_conf.max_visible_color_index)

    return color_conf



def apply_glow(near_headers: list[tuple], linear_bright_list: list, y, cur_render_color_idx):
    # 遍历附近头部
    for header_y, e_delta_col in near_headers:

        # 对于本列，元素仅被下方头部照亮。
        if e_delta_col == 0:
            e_delta_row = header_y - y
            # 若位于下方、被照亮
            if 0 < e_delta_row <= GLOW_RING_COUNT:
                # 若更亮，则更新当前颜色索引
                glow_color_idx = linear_bright_list[e_delta_row - 1]
                if glow_color_idx < cur_render_color_idx:
                    cur_render_color_idx = glow_color_idx

        # 对于附近列
        else:
            e_delta_row = abs(header_y - y) 
            # 若距离过远，则跳过
            if e_delta_row > GLOW_RING_COUNT:
                continue

            # 若更亮，则更新当前颜色索引
            e_r = max(e_delta_row, e_delta_col)
            glow_color_idx = linear_bright_list[e_r - 1]
            if glow_color_idx < cur_render_color_idx:
                cur_render_color_idx = glow_color_idx
                
    return cur_render_color_idx

def do_render(color_conf: color_obj, render_buff: list[list], col: col_obj,
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
    - 从元素引用修改为索引引用
    """
    near_headers = near_header_list[col.col_index]
    highlight_idx = color_conf.highlight_index
    visible_color_idx = color_conf.max_visible_color_index
    linear_bright_list = color_conf.linear_bright_list
    style_normal_code = CONSOLE_CODE.normal_code
    style_bold_code = CONSOLE_CODE.bold_code

    for e in col.char_dict.values(): 
        # 记录字符与当前颜色索引
        cur_render_char = e.char
        cur_render_color_idx = e.color_index
        y, x = e.pos

        # 若列周围存在高亮头部，且字符作为非高亮索引的余烬
        if near_headers and cur_render_color_idx > highlight_idx:

            cur_render_color_idx = apply_glow(near_headers, linear_bright_list, y, cur_render_color_idx)

        # 设置默认 style 为普通体
        attr = style_normal_code

        # 增量更新与全量渲染差异
        if INCREMENTAL:

            # 增量更新时，若字符与可见颜色未变化，则跳过。此处由颜色隐含基于其设置的属性
            # 若字符、颜色在上一帧存在且未变化，跳过
            if e.last_render_color_idx is not None and cur_render_char == e.last_render_char and e.last_render_color_idx == cur_render_color_idx:
                continue

            # 若字符为隐藏颜色序列
            # 增量更新时，设置一次补丁空格：不对上一帧的隐藏状态设置字符，以减少 addch/addstr 调用
            if cur_render_color_idx > visible_color_idx:

                # 增量更新时，若上一帧渲染为隐藏，跳过。实际字符变化时，由于隐藏颜色索引仍跳过
                if e.last_render_char == SPACE:
                    continue

                # 增量更新时，第一次则设置隐藏属性或空格
                cur_render_char = SPACE
            
            # 若字符为高亮索引，设置粗体
            elif cur_render_color_idx <= highlight_idx:
                attr = style_bold_code

            # 此处汇集增量无法跳过隐藏、高亮、余烬
            
            # 保存元素最终渲染的字符、颜色，到增量陈旧状态字段
            e.last_render_char, e.last_render_color_idx, e.last_render_attr = cur_render_char, cur_render_color_idx, attr
            
            # 增量需额外添加全角/半角的转换（全量直接擦除所有）：
            # 若当前字符为半角，则添加半角空格，并且作为字符串写入
            # 方法1：构建为字符集合，查询成员；设置为元素
            # 方法2：设置为字符或元素的属性
            char_len = e.char_len
            if e.char_len == 1:
                # 半角空格位于实际字符 x+1 处，删除时仅需设置一个全角空格，而无需再次区分（当前字符在左，空格在右）
                render_buff[y].append((x + 1, SPACE_H, char_len, cur_render_color_idx, attr))

            render_buff[y].append((x, cur_render_char, char_len, cur_render_color_idx, attr))

        # # 全量渲染
        else:

            # 若字符为隐藏颜色序列
            # 全量重绘时，仅绘制显示的字符：不设置隐藏字符，以减少 addch 调用
            if cur_render_color_idx > visible_color_idx:
                continue 
            
            # 若字符为高亮索引，设置粗体
            elif cur_render_color_idx <= highlight_idx:
                attr = style_bold_code

            # 保存元素最终渲染的字符、颜色，到陈旧状态字段
            e.last_render_char, e.last_render_color_idx, e.last_render_attr = cur_render_char, cur_render_color_idx, attr
            
            # 此处汇集被渲染的高亮、余烬
            render_buff[y].append((x, cur_render_char, e.char_len, cur_render_color_idx, attr))       

def render_rm_patch(render_buff, col: col_obj, header_list: Sequence[Iterable[Pos]]): 
    header_pos = header_list[col.col_index]

    # 若移除字符位置并非新创头部，则设置空格补丁覆盖
    for rm_element in col.rm_char_list:
        if rm_element.pos not in header_pos:
            y, x = rm_element.pos
            render_buff[y].append((x, SPACE, rm_element.char_len, rm_element.last_render_color_idx, rm_element.last_render_attr))

    # 补丁完成后，清空移除字符列表
    col.rm_char_list.clear()

def refresh(color_conf: color_obj, render_buff, pos_seq: list[list[bytes]]):
    """
    性能
    - write 容器
        - bytearray < list + join  
            list 已为指针复制，最后合并。字节组每次分配复制
    - 分支
        - if...else > match...case   
            简单的 if 性能略高于需构建元组的 match
    - 解包
        - list extend 为扁平序列，4元素固定步长读取。且使用索引而避免 batched 的中间元组
            - extend 对元组内每个元素执行一次指针复制
        - list append 为一组元素，遍历解包
    """
    write_list = []
    attr_color_dict = color_conf.attr_color_dict
    color_list = color_conf.color_256_list
    max_visible_color_idx = color_conf.max_visible_color_index
    style_dict = CONSOLE_CODE.style_dict

    cur_y, cur_x = None, None
    # 字符总是发送，不参与比较
    cur_color, cur_attr = None, None
    for y, line in enumerate(render_buff):
        # 跳过空行
        if not line: # len(line) == 0:
            continue

        # 解包元素
        for x, char, char_len, color, attr in line:
            # 当光标位置不连续时发送位置序列
            if cur_y is None or cur_y != y or cur_x != x:
                write_list.append(pos_seq[y][x])
                cur_y = y
                cur_x = x + char_len

            attr_flag = attr != cur_attr
            color_flag = color != cur_color and color <= max_visible_color_idx

            # 当状态与颜色都不连续时发送合并序列
            if attr_flag and color_flag:
                write_list.append(attr_color_dict[(color << COL_ATTR_SHIFT) | attr])

            # 当状态不连续时发送状态序列
            elif attr_flag:
                # write_list += attr
                write_list.append(style_dict[attr])

            # 当颜色不连续时发送颜色序列
            elif color_flag:
                # write_list += color
                write_list.append(color_list[color])

            # 总是发送字符。上述条件可减少同状态的序列数
            write_list.append(char)

            cur_color, cur_attr = color, attr

    # 循环写入，确保短写时完全写入
    # 创建内存视图，多次写入时移动。而非创建容器
    mem_view = memoryview(b''.join(write_list))
    while mem_view:
        write_len = os.write(STDOUT_FD, mem_view)
        mem_view = mem_view[write_len:]

    # 清空 buff
    for line in render_buff:
        line.clear()


def update_char(col: col_obj, color_conf): 
    """
    直到元素颜色渐变完成前，持续更新颜色序列、显示次数、字符突变
    """
    # 性能：重复被引用的字段绑定到本地
    max_pair_index = color_conf.max_pair_index
    highlight_index = color_conf.highlight_index
    rm_char_list = col.rm_char_list
    char_dict = col.char_dict
    color_show_limit = col.color_show_limit
    # 重置列帧数
    col.cur_frame = FRAME_COUNTER_INIT

    # 若增量更新，重置列移除元素列表。从字典快照修改为末尾移除后，全量更新也使用此容器
    rm_char_list.clear()

    # 更新元素
    # 遍历字典，收集待删除 key。之后连续移除。而非建立 list 快照后移除
    for e in char_dict.values():
        
        # 设置随机字符突变。空格不参与突变，一旦突变为空格则持续到消亡
        if e.char != SPACE and _random() < MUT_CHAR:
            e.char, e.char_len = next(FULL_CHAR_LIST_IT)

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
                rm_char_list.append(e)

    # 连续移除待删除元素
    for rm_pos in rm_char_list:
        del char_dict[rm_pos.pos]

def build_header(pos: Pos, col: col_obj, next_head_id: int):
    # 加载头部字符（位置、字符、属性）到元素字典
    col.char_dict[pos] = element_obj(pos, *next(CHAR_LIST_IT))
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
    build_header(header_pos, col, col._next_head_id)

    col._next_head_id += 1

def update_header(col: col_obj, max_y):
    """
    更新列的头部，创建新头
    """
    header_dict = col.header_dict

    for key, pos in list(header_dict.items()):
        nexrow_y = pos.y + 1

        # 若头未到达底部，则继续下落
        if nexrow_y <= max_y:
            new_pos = Pos(y=nexrow_y, x=pos.x)
            build_header(new_pos, col, key)
            
        # 否则移除
        else:
            del header_dict[key]

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

    platform_sign_signal()

def update_near_header_list(col_list: list[col_obj], header_list: Sequence[Iterable[Pos]], 
                            near_header_list: list[list[tuple]]):
    """
    每列构建临近头部列表，替代原版的一个大集合
    - 收集：逐列 +-3 扫描
    - 分发：头写入 +-3 列
    """
    col_list_len = len(col_list)
    for near_header in near_header_list:
        near_header.clear()

    for col in col_list:
        col_index = col.col_index
        # 排除无头部列
        headers = header_list[col_index]
        if not headers:
            continue

        # 获取当前列附近的范围，不超过边界。注意坐标与列位置的转换
        near_cols_start = max(col_index - GLOW_RING_COUNT, 0)
        near_cols_end = min(col_index + GLOW_RING_COUNT, col_list_len - 1)
        near_range = range(near_cols_start, near_cols_end + 1)

        # 遍历当前列头部，临近头部列表中添加到 +-3 范围
        for header in headers:
            for near_idx in near_range:

                # 添加到临近头部列表，[y, e_delta_col] 
                e_delta_col = abs(col_index - near_idx)
                e_delta_row = header.y
                near_header_list[near_idx].append((e_delta_row, e_delta_col))


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

# 初始化行级 buff
def init_buff(terminal_size):
    """
    行级列表，索引为行号，当前列遍历时从左向右，逐列添加时自然有序
    行索引[列索引，字符，颜色，属性]，此处使用固定长度的连续元素到行级列表内，按照步进读取。而非作为元组或列表嵌套
    """
    buff = [[] for _ in range(0, terminal_size.lines)]
    return buff


def init_col(terminal_size):
    """
    # 列状态，全角字符宽度为2
    # 初始化行、列为 max - 1
    """
    col_list = [col_obj(i, x) for i, x in enumerate(range(0, terminal_size.columns - 1, CHAR_W))]
    return col_list

def init_near_header_list(col_list_len):
    near_header_list = [[] for _ in range(col_list_len)]
    return near_header_list

def init_pos_seq(terminal_size):
    """
    初始化位置序列
    """
    sgr_pos_template = CONSOLE_CODE.sgr_pos_template
    y_range = range(terminal_size.lines)
    x_range = range(terminal_size.columns)

    pos_seq = [[] for y in y_range]
    for y in range(terminal_size.lines):
        for x in x_range:
            cur_seq = sgr_pos_template % (y+1, x+1)
            pos_seq[y].append(cur_seq)
    return pos_seq

@dataclass(slots=True)
class terminal_size_related_obj:

    terminal_size: os.terminal_size
    render_buff: list[list] 
    pos_seq: list[list] 
    col_list: list[col_obj]
    near_header_list: list[list] 

    @classmethod
    def build(cls):
        """
        classmethod 线性构建所有字段值，最后 cls 初始化
        """
        # 初始化终端大小
        terminal_size = get_terminal_size()
        
        # 初始化输出 buff
        render_buff = init_buff(terminal_size)

        # 初始化位置序列
        pos_seq = init_pos_seq(terminal_size)

        # 初始化列
        col_list = init_col(terminal_size)

        # glow 使用的临近头部列表
        near_header_list = init_near_header_list(len(col_list))

        return cls(
            terminal_size,
            render_buff,
            pos_seq,
            col_list,
            near_header_list
        )

    @property
    def max_y(self):
        return self.terminal_size.lines - 1

def main():
    global WIN_SIZE_CHANGE_FLAG

    # 注册信号
    sign_signal()

    # 初始化屏幕
    init_screen()

    # 初始化颜色
    color_conf = init_colors()

    # 初始化终端大小相关容器
    terminal_conf = terminal_size_related_obj.build()

    # 停止跟踪，调高回收阈值
    gc.freeze()
    _, threshold1, threshold2 = gc.get_threshold()
    gc.set_threshold(50_000, threshold1, threshold2)

    # 直到终止信号
    while not signal_stop:

        # 计时
        frame_begin_time_s = monotonic()

        # 若终端大小改变事件发生
        if WIN_SIZE_CHANGE_FLAG:

            # 若事件发生后仍保持改变状态
            test_terminal_size = get_terminal_size()
            if terminal_conf.terminal_size != test_terminal_size:
                # 清空屏幕
                clear_screen()

                # 初始化终端大小相关容器
                terminal_conf = terminal_size_related_obj.build()

            # 重置窗口改变事件 flag
            WIN_SIZE_CHANGE_FLAG = False

        # 全量重绘时每帧清空屏幕
        if not INCREMENTAL:
            clear_screen()

        # 遍历列，应用每列的元素到画布
        # 分离渲染与更新，实现变速效果

        # 更新与创建新头
        for col in terminal_conf.col_list:

            # 若列存在任何字符，则更新
            if col.char_dict: # len(col.char_dict) > 0:
                # 每 N 帧更新
                if col.cur_frame >= col.frame_skip:
                    update_char(col, color_conf)
                    # 若未到达底部，则继续下落
                    update_header(col, terminal_conf.max_y)

                # 递增帧计数
                else:
                    col.cur_frame += 1

            # 若列头部数量未达上限，且之前的头不在初始位置附近，则随机创建新头
            if len(col.header_dict) < MAX_HEAD and has_header_dist(col) and _random() < LAUNCH_RAT:
                set_header(col)

        # 多处被使用的头部列表
        header_list = [col.header_dict.values() for col in terminal_conf.col_list]
        update_near_header_list(terminal_conf.col_list, header_list, terminal_conf.near_header_list)
   
        # 列与辐射范围更新后，每轮渲染
        for col in terminal_conf.col_list:

            # 若列存在任何字符，则渲染
            if col.char_dict:  # len(col.char_dict) > 0: 
                do_render(color_conf, terminal_conf.render_buff, col, terminal_conf.near_header_list)

            # 对于增量模式，若存在任何移除字符，则补丁移除。每次清空移除列表，省略模式判断
            if col.rm_char_list: # len(col.rm_char_list) > 0:
                render_rm_patch(terminal_conf.render_buff, col, header_list)

        # 刷新
        refresh(color_conf, terminal_conf.render_buff, terminal_conf.pos_seq)
        
        # 等待事件并休眠
        key = event_sleep_ms(frame_begin_time_s) 
        # 若收到键盘 `q` 则退出
        if key and QUIT_KEY in key:
            break
try:
    main()
    
except:
    pass

finally:
    clean_up()
