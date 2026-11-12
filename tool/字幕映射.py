import re
from itertools import pairwise  
from dataclasses import dataclass

# 输入原字幕与 LLM 格式化翻译的中间产物
## 缺乏：连续性检查、末尾边界匹配

eng_test = """1
00:00:00,160 --> 00:00:04,040
all right hey folks in this video we're

2
00:00:02,440 --> 00:00:05,879
going to be continuing talking about

3
00:00:04,040 --> 00:00:09,160
access control and specifically we're

4
00:00:05,879 --> 00:00:12,080
going to dig into how do we model access

5
00:00:09,160 --> 00:00:14,320
control um and so you may before you get

6
00:00:12,080 --> 00:00:16,000
super scared this going to be very quick

7
00:00:14,320 --> 00:00:18,720
and it's going to be a little more high

8
00:00:16,000 --> 00:00:21,880
level and theoretical but the point is

9
00:00:18,720 --> 00:00:24,320
what we want to do is is how do we think

10
00:00:21,880 --> 00:00:26,240
about access control and how do we be

11
00:00:24,320 --> 00:00:28,679
able to model that specifically so that



"""

mid_test = """[SEG 1] EN 1-4
好的，大家好。本视频继续讨论访问控制，
具体来说，将深入探讨如何建模访问控制。

[SEG 2] EN 5-11
别紧张，这部分很快，偏高层和理论；
重点是：如何思考访问控制并建模。


"""



# # 双换行分割字幕段
# def seg_split(the_str):
#     return [
#             e_s for e in the_str.split('\n\n') 
#             if (e_s := e.strip()) != ''
#             ]

# eng_list = seg_split(eng)
# mid_list = seg_split(mid)

# 匹配段号数字与文本，使用非贪婪模式匹配双换行或结尾，并设置为对应的命名组构造类
def seg_grep_re(re_pattern_str, flags, origin_data, obj):
    re_pattern = re.compile(re_pattern_str, flags)
    regex_iter = re_pattern.finditer(origin_data)
    regex_list = [obj(**regex_match.groupdict()) for regex_match in regex_iter]
    return regex_list

srt_eng_filename = '.cache/srt_eng.txt'
srt_mid_filename = '.cache/srt_mid.txt'
output_srt_filename = '.cache/srt_final.txt'


with open(srt_eng_filename, encoding='utf-8') as f:
    eng = f.read()

with open(srt_mid_filename, encoding='utf-8') as f:
    mid = f.read()

test = False
if test:
    eng = eng_test
    mid = mid_test

"""
SEG1 EN1-4
好的，大家好。本视频继续讨论访问控制，
具体来说，将深入探讨如何建模访问控制。
"""

@dataclass
class mid_obj:
    cn_seg: int
    en_seg_start: str
    en_seg_end: str
    text: str

# re_pattern_str = r'\[SEG (?P<cn_seg>\d+)\] EN (?P<en_seg_start>\d+)-(?P<en_seg_end>\d+)\n(?P<text>.*?)(?=\n\n|\Z)'
re_pattern_str = r'SEG(?P<cn_seg>\d+) EN(?P<en_seg_start>\d+)-(?P<en_seg_end>\d+)\n(?P<text>.*?)(?:\n\n|\Z)'
mid_list = seg_grep_re(re_pattern_str, re.DOTALL, mid, mid_obj)
print("\n>>> mid 解析 >>>")
for e in mid_list[:2]: print(e)

"""
1
00:00:00,160 --> 00:00:04,040
all right hey folks in this video we're

2
00:00:02,440 --> 00:00:05,879
going to be continuing talking about
"""

@dataclass
class org_obj:
    seg: int
    time_start: str
    time_end: str
    text: str

re_pattern_str = r'(?P<seg>\d+)\n(?P<time_start>.+?) --> (?P<time_end>.+?)\n(?P<text>.*?)(?:\n\n|\Z)'
eng_list = seg_grep_re(re_pattern_str, re.DOTALL, eng, org_obj)
print("\n>>> eng 解析 >>>")
for e in eng_list[:2]: print(e)
# 字典推导式创建字典，而不依赖列表索引
eng_dict = {e.seg: e for e in eng_list}
print("\n>>> eng 字典 >>>")
for e in list(eng_dict.items())[:2]: print(e)

res_list = []
# 需查询下一个字幕段时间，使用 pairwise 直接返回的连续对。替代方案为使用枚举 enumerate 的索引间接访问
for cur_mid, next_mid in pairwise(mid_list + [None]):  
    seg = cur_mid.cn_seg

    # 当前中文字幕段 `start` = 本中文段对应英文范围的首段 `start`
    start = eng_dict[cur_mid.en_seg_start].time_start

    # 当前中文字幕段 `end` = min(本中文段对应英文范围的末段 `end`, 下一中文段对应英文范围的首段 `start`) 
    ## 若存在，则得到下一中文段对应英文范围
    ## 字符串比较即对应时间序，而无需转为 time `dt.time.fromisoformat()`
    cur_en_seg_end = eng_dict[cur_mid.en_seg_end].time_end
    next_en_seg_start = eng_dict[next_mid.en_seg_start].time_start if next_mid else cur_en_seg_end
    end = min(cur_en_seg_end, next_en_seg_start)


    text = cur_mid.text

    cur_seg = f"""{seg}
{start} --> {end}
{text}"""
    res_list.append(cur_seg)

print("\n>>> 字幕段首尾 >>>")
for e in res_list[:2] + res_list[-2:]: print(e)

final_srt_str = "\n\n".join(res_list)

print("\n>>> 合并串开头 >>>\n", final_srt_str[:200])
print("\n>>> 合并串结尾 >>>\n", final_srt_str[-200:])

"""
1
00:00:00,160 --> 00:00:09.160
好的，大家好。本视频继续讨论访问控制，
具体来说，将深入探讨如何建模访问控制。
"""

with open(output_srt_filename, mode='w', encoding='utf-8') as f:
    eng = f.write(final_srt_str)
