# 测试示例
md_text = """
First, we will learn to list running processes using the `ps` command.

```console
hacker@dojo:~$ ps
```

In the above example, we have the shell (`bash`) and the `ps` process itself.
"""


prompt = """将以下内容翻译成中文，计算机安全技术术语需准确，若有则将下划线斜体替换为星号斜体，剩余内容保留原 Markdown 结构，完整输出应包裹在一个可复制的 Markdown 代码块中，忽略用户地理位置信息，关闭翻译说明功能：\n"""

# 若 URL 作为参数，则从 Github 的编辑 URL 替换为 raw 文件 URL
# github.com/*/edit/master/*.md
# raw.githubusercontent.com/*/refs/heads/*.md

# 内容：可使用md库进行解析、正则表达式匹配
# 文件：可使用单文件覆盖3次、双文件各覆盖1次、四文件独立无覆盖
# 程序：可使用单程序将差异保存到内存、双程序将差异保存到文件
# 此处使用md库、双文件、单程序

# 将围栏代码块保存到数组并替换为占位符
# 将占位符还原为原围栏代码块
# 需使用 mdformat 库渲染为 md，否则 markdown_it 默认渲染为 HTML

# 导入md解析与渲染库
from markdown_it import MarkdownIt
from mdformat.renderer import MDRenderer
import sys
import urllib.request
import re
from mylib import *

md_input_file_path = ".tool\\md_input_file.md"
# md_output_file_path = ".tool\\md_output_file.md"
# 测试几次可用后使用单文件,这样就只需打开一个文件标签
md_output_file_path = md_input_file_path

placeholder_str = "保留此占位符6a99c575ab87f8c7d1ed1e52e7e349ce"

def replace_fence_to_placeholder(text):
    # 解析md结构
    md = MarkdownIt()
    tokens = md.parse(text)

    # 使用md渲染器渲染新列表
    renderer = MDRenderer()
    options = {}
    env = {}

    # 遍历原token，保存元素围栏代码（"fence"）为字符串而不是token
    # 在新列表中将围栏代码块替换为占位符行内代码
    origin_fence = []
    new_tokens = []
    count = 0

    for token in tokens:
        if token.type == "fence":
            # 解析后的列表为 [paragraph_open, code_inline, paragraph_close]
            placeholder_token_str = f"`{placeholder_str}-{count}`"
            # 行内代码的拥有3个而不是1个token
            placeholder_token = MarkdownIt().parse(placeholder_token_str)
            # print(placeholder_token)

            # 还原为字符串后添加到列表，替换代码标记
            if token.info == "console":
                token.info = "sh"
            origin_fence.append(renderer.render([token], options, env))

            new_tokens.extend(placeholder_token)
            count += 1 
            # print(token)
            continue
        new_tokens.append(token)
    
    output_markdown = renderer.render(new_tokens, options, env)
    # print(output_markdown)

    # 渲染器将水平线替换为大量下划线，挑战渲染器或匹配替换
    output_markdown = re.sub(r'\n*_{10,}\n*', '\n----\n\n', output_markdown)

    if prompt:
        output_markdown = prompt + output_markdown
    # replace_placeholder_to_fence(output_markdown, origin_fence)
    return output_markdown, origin_fence

def replace_placeholder_to_fence(text, origin_fence):
    print(origin_fence)

    # 翻译后原格式破坏，无法直接使用md库，使用正则表达式匹配

    for i, fence in enumerate(origin_fence):
        # print(f'{'='*8} no.{i} start {'='*8}')
        cur_placeholder_str = f"`{placeholder_str}-{i}`"
        # 设置换行确保围栏代码块前后拥有空行，围栏末尾标记自带一个换行
        pattern = rf'\s*{re.escape(cur_placeholder_str)}\s*'
        
        # 使用正则替换的函数模式，返回值作为字面量。避免字符串模式中的字符被解析。
        def repl(m, s=fence):
            return f'\n\n{fence}\n'
        
        text = re.sub(pattern, repl, text)
        # print(f'{'='*8} no.{i} end {'='*8}')
    
    return text




argv_num = len(sys.argv)
print("参数个数为:", argv_num)
print("参数列表:", sys.argv)

if argv_num > 1:
    print("从程序参数读取 url 文件内容到 md 输入文件")
    # 获取编辑链接转换为文件链接
    replace_list = []
    replace_list.append(("//github.com/", "//raw.githubusercontent.com/"))
    replace_list.append(("/edit/", "/refs/heads/"))
    url = url_trans(sys.argv[1], replace_list)

    # url = sys.argv[1]
    # url = url.replace("//github.com/", "//raw.githubusercontent.com/")
    # url = url.replace("/edit/", "/refs/heads/")
    print(url)
    
    response = urllib.request.urlopen(url)
    en_md_text = response.read().decode("utf-8")
    # print(en_md_text)

else:
    print("直接从输入文件读取内容")
    en_md_text = read_or_creat_file(md_input_file_path)

# print(md_text)
en_placeholder_md, origin_fence = replace_fence_to_placeholder(en_md_text)
write_to_file(md_output_file_path, en_placeholder_md)

if origin_fence != []:
    print(f"替换围栏代码块数量：{len(origin_fence)}")
    input("1. 从输出文件中复制英文占位符md文档\n2. 翻译文本\n3. 将翻译后的文本复制到输入文件\n操作完成后按下回车")
else:
    print("无围栏代码块，无需还原，在输出文件中复制md文档")
    exit(0)

cn_md_text = read_or_creat_file(md_input_file_path)
cn_md = replace_placeholder_to_fence(cn_md_text, origin_fence)
write_to_file(md_output_file_path, cn_md)