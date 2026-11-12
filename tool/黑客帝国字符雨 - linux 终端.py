#!/usr/bin/python3

import curses
from dataclasses import dataclass, field
from random import random as _random, choice as _choice  
from functools import cache  
from typing import NamedTuple  

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
        
- 照亮余烬
    - 头部可照亮除本列外的其他字符
    - 被照亮字符使用：较亮（余烬亮度，自身颜色）
    - 多级余烬，范围、亮度中越近越亮
    - 余烬亮度上限为次高亮颜色索引
"""

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

# 作为体的字符集，空格不应位于头部
SPACE = "\u3000" # 空格
FULL_CHAR_LIST = CHAR_LIST + [SPACE]

FRAME_MS = 30  # 帧间隔
SPEED_RANGE = range(1, 5) # 设置更新频率
FRAME_INIT = 1 # 初始帧数
BRIGHT_MAX = 1 # 高亮颜色的最大显示次数
MUT_CHAR = 0.1 # 字符突变几率
MAX_HEAD = 2 # 每列的最大新生字符数，存在之前的残余。并非序列数量
LAUNCH_RAT = 0.007 # 每列发动几率
CHAR_W = 2 # 全角字符宽度2
INVIS_NUM = 3 # 不可见颜色数量，仅被头部照亮               
EMBER_LAYER = 3 # 余烬层数
MAX_EMBER_LV = 2 # 最大余烬亮度，1为最亮高光头部
HEADER_DIST = 5 # 头部之间最小距离

def rgb_cube6(r, g, b):  
    """
    在8个基础色（0-7）与变体外（8-15），rgb 的拥有分量 0-5 
    - r 6**2
    - g 6**1
    - b 6**0
    """
    return 16 + 36*r + 6*g + b  

def init_colors():  
    """
    设置颜色对：创建一批绿色渐变前景色，背景色为默认，从亮到暗。  
    g=0 时几乎为灰色，选取 5-1  
    rgb(4,5,4) 几乎为白色，选取 (3,5,3) 白绿色头部  
    添加 (1,5,1) 作为次高光，余烬最大等级可为次高光
    """
    highlight_green = [(3,5,3), (1,5,1)]
    linear_green = [(0, green, 0) for green in range(5, 0, -1)]
    color_rgb_list = highlight_green + linear_green

    pair_number = 1
    for rgb in color_rgb_list:  
        curses.init_pair(pair_number, rgb_cube6(*rgb), -1)  
        pair_number += 1

    # 更新颜色计数
    max_color_index = pair_number - 1

    for _ in range(INVIS_NUM):
        # 设置之后被隐藏的额外色
        curses.init_pair(pair_number, -1, -1)  
        pair_number += 1

    # max_pair_index 包含不可见
    max_pair_index = pair_number - 1    
    # 最大高光索引
    highlight_index = len(highlight_green)
    return max_pair_index, max_color_index, highlight_index

class Pos(NamedTuple):
    y: int
    x: int

@dataclass(slots=True)
class element_obj:
    """
    每个字符元素
    - cur_show_count  
        每个颜色出现的次数
    """
    y_x: Pos
    char: str
    color_index: int = 1 # 颜色序列索引
    cur_show_count: int = 0 # 每个颜色的显示次数

@dataclass(slots=True)
class col_obj:
    """
    列状态，保存本列的元素列表
    """
    col_x: int # 列
    char_dict: dict[Pos, element_obj] = field(default_factory=dict) # 追踪所有字符位置，颜色遍历完成后移除
    head_dict: dict[int, Pos] = field(default_factory=dict) # 追踪新生头所在行，到底部时移除
    _next_head_id: int = 0 # 下个 head 的序号
    max_frame: int = 0 # 最大更新帧数
    cur_frame: int = 0 # 当前更新帧数
    max_show_count: int = 0 # 每个颜色序列的最大显示次数

@dataclass(slots=True)
class ember_obj:
    """
    保存余烬信息：缩放、集合、亮度
    """
    scale: int = 0 # 方圈距离
    ember_set: set[Pos] = field(default_factory=set) # 照亮余烬集合
    ember_lv: int = 0 # 照亮余烬亮度


@cache
def _color_pair(pair_number):
    """
    缓存重复计数的颜色对编号，尝试使用花哨的功能。  
    虽然可预构建列表，但缓存装饰器的包装函数可保持原代码结构
    """
    return curses.color_pair(pair_number)

def render_char(stdscr: curses.window, col: col_obj, max_color_index, ember_conf_list: list[ember_obj], highlight_index):
    """
    渲染字符
    - 若字符作为头部，设置粗体
    - 若字符作为余烬被头部照亮，当前亮度为自身亮度 ~ 余烬亮度的最亮值
    - 若字符未被照亮，仅设置当前状态
        - 若字符作为末尾隐藏颜色序列，则隐藏
    """

    for e in col.char_dict.values():
        # 记录字符当前颜色索引
        cur_color_index = e.color_index
        
        # 若字符作为非高亮索引的余烬
        if cur_color_index > highlight_index:

            # 若被头部照亮，当前亮度为自身亮度 ~ 余烬亮度的最亮值
            for ember_config in ember_conf_list:
                if e.y_x in ember_config.ember_set:
                    cur_color_index = min(cur_color_index, ember_config.ember_lv)
                    break

        # 得到字符当前颜色索引对应属性，之后调整格式
        attr = _color_pair(cur_color_index)

        # 若字符为高亮索引，设置粗体
        if cur_color_index <= highlight_index:
            attr |= curses.A_BOLD

        # 若字符为隐藏颜色序列，设置隐藏
        elif cur_color_index > max_color_index:
            attr |= curses.A_INVIS

        stdscr.addch(*e.y_x, e.char, attr)

def update_char(col: col_obj, max_pair_index, highlight_index):
    """
    直到元素颜色渐变完成前，持续更新颜色序列、显示次数、字符突变
    """
    # 重置列帧数
    col.cur_frame = FRAME_INIT

    # 更新元素
    # 遍历字典 key 快照，更新字典本身
    for pos in list(col.char_dict):
        e = col.char_dict[pos]
        # 设置随机字符突变。空格不参与突变，一旦突变为空格则持续到消亡
        if e.char != SPACE and _random() < MUT_CHAR:
            e.char = _choice(FULL_CHAR_LIST)

        # 更新元素颜色次数
        e.cur_show_count += 1
        # 若颜色次数达到上限（普通颜色或高亮颜色）：更新颜色索引，并设置颜色次数为0
        # 预期多种构造：预构建颜色列表，移除显示次数；转移显示次数而设置到颜色对象中的状态
        if e.cur_show_count >= col.max_show_count or (e.color_index <= highlight_index and e.cur_show_count >= BRIGHT_MAX):
            # 若颜色列表尚未完成，则继续更新索引
            if e.color_index < max_pair_index:
                e.color_index += 1
                e.cur_show_count = 0
            # 若当前元素消亡，移除
            else:
                del col.char_dict[pos]

def set_header(col: col_obj):
    """
    新生字符
    - 无任何字符时，初始化列
    - 否则创建一个新生字符
    """
    # 设置初始下落字符位置，y 固定为最上方，也可修改为随机行
    header_pos = Pos(0, col.col_x)
    # 初始化列
    if len(col.char_dict) == 0:
        # 添加到头部字典
        col.head_dict[col._next_head_id] = header_pos
        col._next_head_id += 1
        # 设置列速度，初始化帧数
        col.max_frame = _choice(SPEED_RANGE)
        # 速度越快，拖尾越长
        col.max_show_count = len(SPEED_RANGE) - col.max_frame + 1 
        # 初始化帧
        col.cur_frame = FRAME_INIT

    # 创建一个新生字符，添加到头部字典
    else:
        col.head_dict[col._next_head_id] = header_pos
        col._next_head_id += 1

    # 加载新下落字符（位置、字符、属性）到元素字典
    col.char_dict[header_pos] = element_obj(header_pos, _choice(CHAR_LIST))

def update_header(col: col_obj, max_y):
    """
    更新列的头部，创建新头
    """
    for key in list(col.head_dict):
        nexrow_y = col.head_dict[key].y + 1

        # 若头未到达底部，则继续下落
        if nexrow_y <= max_y:
            new_pos = Pos(y=nexrow_y, x=col.col_x)
            col.head_dict[key] = new_pos
            col.char_dict[new_pos] = element_obj(new_pos, _choice(CHAR_LIST))
            
        # 否则移除
        else:
            del col.head_dict[key]



# 直接设置缓存，而非手动构造预计算容器
@cache 
def get_ember_set(row_y, col_x, scale):
    """
    计算头部周围一圈的集合。
    """
    row_dist = scale * 1
    col_dist = scale * CHAR_W

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



def linear_gradient(layer, color_list):
    """
    在颜色范围，基于端点数量设置接近等距的颜色渐变
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


def init_ember_set(col_list: list[col_obj], ember_conf_list: list[ember_obj]):
    """
    遍历头部，设置余烬范围到集合。之后渲染时使用集合立即得到是否被照亮以及亮度
    """
    # 初始化余烬配置内的集合
    for ember_conf in ember_conf_list:
        ember_conf.ember_set = set()

    # 搜索所有列的头部
    for col in col_list:
        if len(col.head_dict) > 0:
            for header_pos in col.head_dict.values():
                # 按照配置范围，设置多级余烬集合
                for ember_conf in ember_conf_list:
                    # 传入当前坐标以及缩放范围
                    cur_ember_set = get_ember_set(*header_pos, ember_conf.scale)
                    # 更新余烬字典的集合
                    ember_conf.ember_set.update(cur_ember_set)

    # # 多级余烬集合消除重叠。去重后
    # t_e = set()
    # for e in ember_conf_list:
    #     e.ember_set -= t_e
    #     t_e.update(e.ember_set)

def build_ember_list(max_color_index):
    # 计算当前余烬范围参数对应的可用近似等距渐变集合，即余烬范围参数 >= 实际余烬集合数
    color_range = range(MAX_EMBER_LV, max_color_index + 1)
    ember_lv_list = linear_gradient(EMBER_LAYER, color_range)

    # 使用渐变集合预设置余烬对象
    ember_conf_list = [ ember_obj(scale=scale, ember_lv=ember_lv) 
                    for scale, ember_lv in enumerate(ember_lv_list, start=1) ]

    return ember_conf_list

def is_header_dist(col: col_obj):
    """
    - True
        - 当不存在任何头部时
        - 当存在头部，且在距离外
    - False
        - 当存在头部，且在距离内
    """
    res = True
    # 无头部时头部列表为空，返回 True
    for header_pos in col.head_dict.values():
        if header_pos.y < HEADER_DIST:
            res = False
            break
    return res

def main(stdscr: curses.window):

    # 隐藏光标
    curses.curs_set(0) 
    # 使用默认颜色
    curses.use_default_colors() 

    # 读取按键时设置为非阻塞
    stdscr.nodelay(True) 

    # 初始化颜色对
    max_pair_index, max_color_index, highlight_index = init_colors()

    # 初始化余烬配置
    ember_conf_list = build_ember_list(max_color_index)

    # 列状态，全角字符宽度为2
    def init_col():
        col_list = [col_obj(x) for x in range(0, curses.COLS - CHAR_W, CHAR_W)]
        return col_list
    
    col_list = init_col()

    max_y = curses.LINES - 1

    while True:

        key = stdscr.getch()
        # 若收到键盘 `q` 则退出
        if key == ord('q'):
            break

        # 若终端大小改变
        if key == curses.KEY_RESIZE:
            # 更新变量
            curses.update_lines_cols()

            # 重置，或修改为继承之前列再添加/移除
            col_list = init_col()
            
            max_y = curses.LINES - 1

        # 清空屏幕
        stdscr.erase() 

        # 遍历列，应用每列的元素到画布
        # 分离渲染与更新，实现变速效果
        for col in col_list:

            # 若列头部数量未达上限，且之前的头不在初始位置附近，则随机创建新头
            if len(col.head_dict) < MAX_HEAD and is_header_dist(col) and _random() < LAUNCH_RAT:
                set_header(col)

            # 若列存在任何字符，则渲染、更新
            if len(col.char_dict) > 0:
                # 每轮渲染
                render_char(stdscr, col, max_color_index, ember_conf_list, highlight_index)

                # 每 N 帧更新
                if col.cur_frame >= col.max_frame:
                    update_char(col, max_pair_index, highlight_index)
                    # 若未到达底部，则继续下落
                    update_header(col, max_y)

                # 递增帧计数
                else:
                    col.cur_frame += 1

        # 列遍历完成后
        # 获取当前新生字符位置设置余烬范围集合
        init_ember_set(col_list, ember_conf_list)    

        # 刷新
        stdscr.refresh()
        # 休眠
        curses.napms(FRAME_MS) 

# 使用包装函数，自动初始化
curses.wrapper(main)

