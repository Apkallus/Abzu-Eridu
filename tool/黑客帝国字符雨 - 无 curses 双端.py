#!/usr/bin/python3

from dataclasses import dataclass, field
from random import random as _random, choices as _choices  
from functools import cache  
from typing import NamedTuple  
from unicodedata import east_asian_width  
import shutil
from time import monotonic, sleep
from datetime import timedelta
import os
import sys
import subprocess

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

未优化时的性能
- profiling
    ```sh
    python3 -m profiling.sampling run --mode=cpu -r 20khz -d 60
    ```
    - nocurses
        ```log
        686498 function calls (130430 primitive calls) in 6.521 seconds
        nsamples  tottime persample cumtime persample filename:lineno(function)
            5656    0.283    0.000    0.283    0.000 os.write(STDOUT_FD, ''.join(write_list).encode()) # testa.py:663(refresh)
            4840    0.242    0.000    0.242    0.000 glow_conf.coverage_set.update(cur_coverage_set) # testa.py:569(update_glow_coverage)
            3868    0.193    0.000    0.193    0.000 sorted_buff = sorted(color_and_buff.buff.items()) # testa.py:635(refresh)
        ```

    - curses
        ```log
        255170 function calls (50366 primitive calls) in 2.518 seconds

        nsamples  tottime persample cumtime persample filename:lineno(function)
            99541    4.977    0.000    4.977    0.000 stdscr.refresh() # testb.py:580(main)
             4172    0.209    0.000    0.209    0.000 glow_conf.coverage_set.update(cur_coverage_set) # testb.py:447(update_glow_coverage)
             3056    0.153    0.000    0.153    0.000 if e.y_x in glow_config.coverage_set and glow_config.bright < cur_render_color: # testb.py:231(do_render)
        ```

- strace
    ```sh
    timeout 30 strace -c
    ```
    - nocurses
        ```log
        % time     seconds  usecs/call     calls    errors syscall
        ------ ----------- ----------- --------- --------- ------------------
         21.21    0.009750          10       927           write
         17.38    0.007988           8       926         1 clock_nanosleep
         15.87    0.007297           7       940         1 ioctl
        100.00    0.045974           9      4911        56 total
        ```

    - curses
        ```log
        % time     seconds  usecs/call     calls    errors syscall
        ------ ----------- ----------- --------- --------- ------------------
         92.53    1.466099          17     85167           write
          4.81    0.076201          15      5013           poll
          0.93    0.014738          31       473           clock_nanosleep
        100.00    1.584409          17     92585        51 total
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
    bk_screen_enter = b'\x1b[?1049h' # 使用备用屏幕
    bk_screen_quit = b'\x1b[?1049l' # 从备用屏幕恢复
    
    clean: bytes = b'\x1b[2J' # 全屏擦除
    clean_and_rollback: bytes = b'\x1b[3J' # 全屏擦除

    reset_attr: bytes = b'\x1b[0m' # 重置所有属性
    bold: str = '\x1b[1m' # 设置粗体 
    normel: str = '\x1b[22m' # 设置正常体
    sgr_rgb_template: str = '\x1b[38;5;%dm' # 显示序列
    

    # 位置序列
    sgr_pos_template: str = '\x1b[%d;%dH'
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
            res_char_list += [chr(i) for i in range(int(start, 16), int(end, 16) + 1)]
        # 若为列表，则提取其中的单字符
        elif isinstance(arg, list):
            res_char_list += [chr(int(c, 16)) for c in arg]
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
    # 非连续特殊字符集合
    ["1A15", "2D47", "10501"],
    # 非连续符号集合
    ["FF02", "FF0A", "FF0B", "FF0D", "FF0E", "FF1A", "FF1C", "FF1D", "FF1E", "FF3F", "FF5C"],
)

CHAR_LIST_IT = random_choice_chunk(CHAR_LIST, k=256)

# 作为体的字符集，空格不应位于头部
SPACE = "\u3000" # 全角空格
SPACE_H = '\u0020' # 半角空格
FULL_CHAR_LIST = CHAR_LIST + [SPACE]
FULL_CHAR_LIST_IT = random_choice_chunk(FULL_CHAR_LIST, k=256)

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
MAX_BRIGHT = 2 # 最大辐射亮度，2为次高光头部
HEADER_DIST = 5 # 头部之间最小距离

INCREMENTAL = True # 增量更新开关

STDOUT_FD = sys.stdout.fileno()
STDIN_FD = sys.stdin.fileno()

QUIT_KEY = b'q'

# 双平台读取按键，懒加载库
platform_name = sys.platform

def platform_clean_up():
    pass

def platform_init_screen():
    pass

if platform_name.startswith('linux'):
    import select
    import tty
    import termios

    # 进入时，保存当前终端状态，终端禁用缓冲，用户输入立即生效
    SAVED_TERMIOS_ATTR = tty.setcbreak(STDIN_FD)
    def getch():
        key = None
        if select.select([STDIN_FD], [], [], 0)[0]:
            # 得到 bytes
            key = os.read(STDIN_FD, 32)
        return key

    # 退出时，恢复终端状态
    def platform_clean_up():
        if platform_name.startswith('linux'):
            termios.tcsetattr(STDIN_FD, termios.TCSANOW, SAVED_TERMIOS_ATTR)



elif platform_name.startswith('win'):
    import msvcrt
    def getch():
        key = None
        if msvcrt.kbhit():
            # 平台统一为 bytes
            key = msvcrt.getwch().encode()
        return key

    # 设置控制台输出 UTF-8
    def platform_init_screen():
        subprocess.getstatusoutput('chcp 65001')


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
    return 16 + 36*r + 6*g + b  

@dataclass(slots=True)
class color_and_buff_obj:
    color_256_list: list[bytes|None|int] = field(default_factory=list) 
    max_visible_color_index: int = 0
    max_pair_index: int = 0
    highlight_index: int = 0
    # 使用 (y,x) 排序
    # 位置: [字符，颜色，属性]
    buff: dict[Pos, list] = field(default_factory=dict) 

def init_colors():  
    """
    设置颜色对：创建一批绿色渐变前景色，背景色为默认，从亮到暗。  
    g=0 时几乎为灰色，选取 5-1  
    rgb(4,5,4) 几乎为白色，选取 (3,5,3) 白绿色头部  
    添加 (1,5,1) 作为次高光，余烬最大等级可为次高光
    """
    color_and_buff = color_and_buff_obj([None])
    highlight_green = [(3,5,3), (1,5,1)]
    linear_green = [(0, green, 0) for green in range(5, 0, -1)]
    color_rgb_list = highlight_green + linear_green

    for rgb in color_rgb_list:  
        color_and_buff.color_256_list.append(CONSOLE_CODE.sgr_rgb_template % rgb_cube6(*rgb))

    # 更新颜色计数
    color_and_buff.max_visible_color_index = len(color_and_buff.color_256_list) - 1

    for _ in range(INVIS_NUM):
        # 设置之后被隐藏的额外色
        color_and_buff.color_256_list.append(None)

    # max_pair_index 包含不可见
    color_and_buff.max_pair_index = len(color_and_buff.color_256_list) - 1
    # 最大高光索引
    color_and_buff.highlight_index = len(highlight_green)
    return color_and_buff

@dataclass(slots=True)
class element_obj:
    """
    每个字符元素
    - color_show_count  
        每个颜色出现的次数
    """
    y_x: Pos
    char: str
    color_index: int = 1 # 颜色序列索引
    color_show_count: int = 0 # 每个颜色的显示次数
    # 增量更新字段，可设置为继承并同名覆盖的子类，但仅简单设置为单类的字段
    last_render_char: str | None = None # 增量更新使用的之前渲染字符
    last_render_color: int | None = None # 增量更新使用的之前渲染颜色

@dataclass(slots=True)
class col_obj:
    """
    列状态，保存本列的元素列表
    """
    col_x: int # 列
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
    保存辐射环信息：环、覆盖范围坐标、亮度
    """
    ring: int = 0 # 辐射环到头部的距离
    coverage_set: set[Pos] = field(default_factory=set) # 覆盖范围
    bright: int = 0 # 辐射亮度

WIDE_SET = ('W', 'F')
@cache
def as_wide_char(ch):
    # 广义上，宽字符包括 W、F 和 A（在东亚语境下），而窄字符则包括 N、Na、H 和 A（不在东亚语境下）。
    return True if east_asian_width(ch) in WIDE_SET else False

def do_render(color_and_buff: color_and_buff_obj, col: col_obj, glow_conf_list: list[glow_obj]):
    """
    渲染字符
    - 若字符作为头部，设置粗体
    - 若字符作为余烬被头部照亮，当前亮度为自身亮度 ~ 辐射亮度的最亮值
    - 若字符未被照亮，仅设置当前状态
        - 若字符作为末尾隐藏颜色序列，则隐藏
    
    性能优化
    - 迭代元素视图取字段 -> 对元素视图进行分类集合运算，更多开销
        - 迭代元素直接访问数据类字段
        - 分类集合运算创建多个中间视图，再迭代多个分类视图本身，开销仍超过判断分支减少的收益
    - 结构清晰度 > 性能调整
    """

    for e in col.char_dict.values(): 
        # 记录字符与当前颜色索引
        cur_render_char = e.char
        cur_render_color_idx = e.color_index
        
        # 若字符作为非高亮索引的余烬
        if cur_render_color_idx > color_and_buff.highlight_index:

            # 若被头部照亮，且辐射亮度相对更亮，则设置为辐射亮度
            for glow_config in glow_conf_list:
                if e.y_x in glow_config.coverage_set and glow_config.bright < cur_render_color_idx:
                    cur_render_color_idx = glow_config.bright
                    break

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
            if cur_render_color_idx > color_and_buff.max_visible_color_index:

                # 增量更新时，若上一帧渲染为隐藏，跳过。实际字符变化时，由于隐藏颜色索引仍跳过
                if e.last_render_char == SPACE:
                    continue

                # 增量更新时，第一次则设置隐藏属性或空格
                cur_render_char = SPACE
            
            # 若字符为高亮索引，设置粗体
            elif cur_render_color_idx <= color_and_buff.highlight_index:
                attr = CONSOLE_CODE.bold

            # 此处汇集增量无法跳过隐藏、高亮、余烬
            
            # 保存元素最终渲染的字符、颜色，到增量专用的陈旧状态字段
            e.last_render_char, e.last_render_color = cur_render_char, cur_render_color_idx

            # 增量需额外添加全角/半角的转换（全量直接擦除所有）：
            # 若当前字符为半角，则添加半角空格，并且作为字符串写入
            if not as_wide_char(cur_render_char):
                color_and_buff.buff[Pos(e.y_x.y, e.y_x.x + 1)] = [SPACE_H, color_and_buff.color_256_list[cur_render_color_idx], attr]    

            color_and_buff.buff[e.y_x] = [cur_render_char, color_and_buff.color_256_list[cur_render_color_idx], attr]          

        # # 全量渲染
        # else:

        #     # 若字符为隐藏颜色序列
        #     # 全量重绘时，仅绘制显示的字符：不设置隐藏字符，以减少 addch 调用
        #     if cur_render_color_idx > color_and_buff.max_visible_color_index:
        #         continue 
            
        #     # 若字符为高亮索引，设置粗体
        #     elif cur_render_color_idx <= color_and_buff.highlight_index:
        #         attr |= .A_BOLD

        #     # 此处汇集被渲染的高亮、余烬
        #     attr |= _color_pair(cur_render_color_idx)
        #     .addch(*e.y_x, cur_render_char, attr)

def render_rm_patch(color_and_buff: color_and_buff_obj, col: col_obj): 
    # 若移除字符位置并非新头部，则设置空格补丁
    header_pos_view = col.header_dict.values()
    for rm_element in col.rm_char_list:
        if rm_element.y_x not in header_pos_view:
            space_patch = SPACE if as_wide_char(rm_element.char) else SPACE_H
            color = color_and_buff.color_256_list[rm_element.color_index]
            color_and_buff.buff[rm_element.y_x] = [space_patch, color, None] 

    # 补丁完成后，清空移除字符列表
    col.rm_char_list.clear()

def update_char(col: col_obj, max_pair_index, highlight_index): 
    """
    直到元素颜色渐变完成前，持续更新颜色序列、显示次数、字符突变
    """
    # 重置列帧数
    col.cur_frame = FRAME_COUNTER_INIT

    # 若增量更新，重置列移除元素列表
    if INCREMENTAL:
        col.rm_char_list.clear()

    # 更新元素
    # 遍历字典 key 快照，更新字典本身
    for pos, e in list(col.char_dict.items()):

        # 设置随机字符突变。空格不参与突变，一旦突变为空格则持续到消亡
        if e.char != SPACE and _random() < MUT_CHAR:
            e.char = next(FULL_CHAR_LIST_IT)

        # 更新元素颜色次数
        e.color_show_count += 1
        # 若颜色次数达到上限（普通颜色或高亮颜色）：更新颜色索引，并设置颜色次数为0
        # 预期多种构造：预构建颜色列表，移除显示次数；转移显示次数而设置到颜色对象中的状态
        if e.color_show_count >= col.color_show_limit or (e.color_index <= highlight_index and e.color_show_count >= HIGHLIGHT_SHOW_LIMIT):
            # 若颜色列表尚未完成，则继续更新索引
            if e.color_index < max_pair_index:
                e.color_index += 1
                e.color_show_count = 0
            # 若当前元素消亡，移除
            else:

                # 若增量更新，移除字典元素，并添加消亡元素到保存列表
                if INCREMENTAL:
                    col.rm_char_list.append(col.char_dict.pop(pos))
                # 若全量更新，直接删除
                else:
                    del col.char_dict[pos]

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
    if len(col.char_dict) == 0:

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

# 直接设置缓存，而非手动构造预计算容器
@cache 
def build_ring_coverage_set(row_y, col_x, ring):
    """
    计算头部周围一圈的集合。
    """
    row_dist = ring * 1
    col_dist = ring * CHAR_W

    # 正方形4个点
    left_col, right_col = col_x - col_dist, col_x + col_dist
    up_row, down_row = row_y - row_dist, row_y + row_dist

    def get_line_set(y_start, y_end, x_start, x_end):
        line_set = {
            Pos(y, x) 
            for y in range(y_start, y_end + 1, 1)
            for x in range(x_start, x_end + CHAR_W, CHAR_W)
        }
        return line_set

    # 添加：正方形4条边
    up_line = get_line_set(up_row, up_row, left_col, right_col)
    down_line = get_line_set(down_row, down_row, left_col, right_col)
    left_line = get_line_set(up_row, down_row, left_col, left_col)
    right_line = get_line_set(up_row, down_row, right_col, right_col)

    # 排除：正方形顶边 - 头部中心。下落的头部并不照亮本头部的轨迹
    center_top = get_line_set(up_row, row_y, col_x, col_x)

    # 计算集合，头部照亮除正上方外的一圈
    # 注意，集合运算符应用普通运算优先级，`-` 拥有相对高优先级。使用括号，或仅对 up_line 执行集合移除
    res_set = (up_line | down_line | left_line | right_line) - center_top

    return res_set

def update_glow_coverage(col_list: list[col_obj], glow_conf_list: list[glow_obj]):
    """
    遍历头部，设置辐射环范围到覆盖集合。之后渲染时使用覆盖集合立即得到是否被照亮以及亮度
    - 性能优化：从集合 -> 字典，并不能实际带来提升
        - 调用侧：迭代 set 查询 break -> 单次 dict hash 查询  
            提升很小
        - 构建侧：set 集合批量添加 -> 每个位置均在 dict 中比较/构建 
            增加开销
    """
    # 刷新辐射环配置内的覆盖集合
    for glow_conf in glow_conf_list:
        glow_conf.coverage_set = set()

    # 搜索所有列的头部
    for col in col_list:
        if len(col.header_dict) > 0:
            for header_pos in col.header_dict.values():
                # 按照配置范围，设置多级辐射环覆盖集合
                for glow_conf in glow_conf_list:
                    # 传入当前坐标以及缩放范围
                    cur_coverage_set = build_ring_coverage_set(*header_pos, glow_conf.ring)
                    # 更新覆盖集合
                    glow_conf.coverage_set.update(cur_coverage_set)

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

def build_glow_list(max_visible_color_index):
    # 可用辐射亮度列表 -> 渐变辐射亮度列表
    available_bright_range = range(MAX_BRIGHT, max_visible_color_index + 1)
    linear_bright_list = linear_gradient(GLOW_RING_COUNT, available_bright_range)

    # 使用渐变集合预设置辐射环对象
    glow_conf_list = [ glow_obj(ring=ring, bright=bright) 
                    for ring, bright in enumerate(linear_bright_list, start=1) ]

    return glow_conf_list

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

def napms(frame_begin_time_s):
    """
    实际暂停时长 = 预期暂停时长 - 计算与渲染延迟
    """
    time_delay_s = monotonic() - frame_begin_time_s
    time_sleep_s = DELTA_TIME_S - time_delay_s

    # 休眠剩余时间，若渲染超出设置的帧间隔，则立即渲染
    if time_sleep_s > 0:
        sleep(time_sleep_s)

@cache
def build_pos_seq(pos: Pos):
    # 写入时向右下 ↘ 偏移
    y, x = pos
    return CONSOLE_CODE.sgr_pos_template % (y+1, x+1)

def refresh(color_and_buff: color_and_buff_obj):
    sorted_buff = sorted(color_and_buff.buff.items())
    write_list = []

    cur_y, cur_x = None, None
    # 字符总是发送，不参与比较
    cur_color, cur_attr = None, None
    for pos, render_data in sorted_buff:
        y, x = pos
        char, color, attr = render_data
        # 当光标位置不连续时发送位置序列
        if cur_y is None or cur_y != y or cur_x != x:
            pos_seq = build_pos_seq(pos)
            write_list.append(pos_seq)
            cur_y, cur_x = y, x+1

        # 当颜色不连续时发送颜色序列
        if color and color != cur_color:
            write_list.append(color)

        # 当状态不连续时发送状态序列
        if attr and attr != cur_attr:
            write_list.append(attr)

        # 总是发送字符。上述条件可减少同状态的序列数
        write_list.append(char)

        _, cur_color, cur_attr = render_data
            
    os.write(STDOUT_FD, ''.join(write_list).encode())

    color_and_buff.buff.clear()

def init_screen():
    os.write(STDOUT_FD, CONSOLE_CODE.init_screen_seq)

    platform_init_screen()

def clear_screen():
    os.write(STDOUT_FD, CONSOLE_CODE.clear_screen_seq)

def clean_up():
    """
    退出或异常
    """
    os.write(STDOUT_FD, CONSOLE_CODE.clean_up_seq)

    platform_clean_up()

def main():

    # 初始化屏幕
    init_screen()

    # 初始化颜色对
    color_and_buff = init_colors()

    # 初始化辐射环配置
    glow_conf_list = build_glow_list(color_and_buff.max_visible_color_index)

    # 初始化终端大小
    terminal_size = shutil.get_terminal_size()

    # 列状态，全角字符宽度为2
    # 初始化行、列为 max - 1
    def init_col(terminal_size):
        col_list = [col_obj(x) for x in range(0, terminal_size.columns - CHAR_W + 1, CHAR_W)]
        return col_list
    
    col_list = init_col(terminal_size)
    max_y = terminal_size.lines - 1

    while True:

        # 计时
        frame_begin_time_s = monotonic()

        key = getch()
        # 若收到键盘 `q` 则退出
        if key and QUIT_KEY in key:
            break

        # 若终端大小改变
        test_terminal_size = shutil.get_terminal_size()
        if terminal_size != test_terminal_size:
            # 清空屏幕
            clear_screen()

            # 更新行列大小
            terminal_size = test_terminal_size

            # 重置，或修改为继承之前列再添加/移除
            col_list = init_col(terminal_size)
            max_y = terminal_size.lines - 1

        # 全量重绘时每帧清空屏幕
        if not INCREMENTAL:
            clear_screen()

        # 遍历列，应用每列的元素到画布
        # 分离渲染与更新，实现变速效果

        # 更新与创建新头
        for col in col_list:

            # 若列存在任何字符，则更新
            if len(col.char_dict) > 0:
                # 每 N 帧更新
                if col.cur_frame >= col.frame_skip:
                    update_char(col, color_and_buff.max_pair_index, color_and_buff.highlight_index)
                    # 若未到达底部，则继续下落
                    update_header(col, max_y)

                # 递增帧计数
                else:
                    col.cur_frame += 1

            # 若列头部数量未达上限，且之前的头不在初始位置附近，则随机创建新头
            if len(col.header_dict) < MAX_HEAD and has_header_dist(col) and _random() < LAUNCH_RAT:
                set_header(col)

        # 列遍历完成后
        # 获取当前新生字符位置设置辐射覆盖范围
        update_glow_coverage(col_list, glow_conf_list)      

        # 列与辐射范围更新后，每轮渲染
        for col in col_list:

            # 若列存在任何字符，则渲染
            if len(col.char_dict) > 0: 
                do_render(color_and_buff, col, glow_conf_list)

            # 对于增量模式，若存在任何移除字符，则补丁移除。每次清空移除列表，省略模式判断
            if len(col.rm_char_list) > 0:
                render_rm_patch(color_and_buff, col)

        # 刷新
        refresh(color_and_buff)
        # 休眠
        napms(frame_begin_time_s) 

try:
    main()

# 捕获 `Ctrl + c`
except KeyboardInterrupt:
    pass

# 最终清理状态
finally:
    clean_up()
