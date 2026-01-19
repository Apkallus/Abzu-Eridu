# name: "Dealing with Data"
# auxiliary:
#   pwnshop:
#     build_image: pwncollege/challenge-simple:latest
#     verify_image: pwncollege/challenge-simple:latest
#     binary_name: runme
#     variants: 16
#     challenge: PasswordCheckerBase
# resources:
# - name: Tip - Debugging Your Assembly
#   type: markdown
#   content: |
#       These challenges are written in Python and run your assembly code in an emulator.
#       This means you cannot use the normal debugging tools such as `gdb` to debug the challenge. However, we have added a special debug functionality to these challenges.
#       If an `int3` instruction is executed by the challenge in your assembly code, the emulator will print out the current state of the registers and memory.
#       This can be extremely useful to reason about your code!
# challenges:
# - id: password-simple-2
#   name: "... and again!"
#   description: |
#     Once more into the breach, dear hacker!
#     Just to make sure you get the idea.
#   auxiliary:
#     pwnshop:
#       attributes:
#         seed: 133738000
#         strip: True

from mylib import *
import yaml
import sys
import urllib.request
import re

# yaml 库将 yam 文件yaml_data解析为字典
# 转换字典为md文件，之后使用已存在的md占位符转换程序

yaml_to_md_path = ".tool\\yaml_to_md.md"

argv_num = len(sys.argv)
print("参数个数为:", argv_num)
print("参数列表:", sys.argv)

if argv_num > 1:
    print("从程序参数读取 url 文件内容到 yaml_to_md.md 文件")
    # 获取编辑链接转换为文件链接
    replace_list = []
    replace_list.append(("//github.com/", "//raw.githubusercontent.com/"))
    replace_list.append(("/edit/", "/refs/heads/"))
    url = url_trans(sys.argv[1], replace_list)
    print(url)
    
    response = urllib.request.urlopen(url)
    yaml_str = response.read().decode("utf-8")

else:
    print("直接从输入文件读取内容")
    yaml_str = read_or_creat_file(yaml_to_md_path)

# print(yaml_str)

yaml_data = yaml.safe_load(yaml_str)  # 避免执行恶意代码

# print(yaml_data)

# 分为资源与挑战两部分
# 资源内容为description，挑战内容为content
# 添加条件检测确保存在，或使用异常
md_list = []
part_list = ["resources", "challenges"]
text_list = ["description", "content"]

module_name_str = yaml_data["name"]

md_list.append(f"# {module_name_str}")

for part in part_list:
    if part not in yaml_data:
        continue

    md_list.append(f"## {part}")

    data_list = yaml_data[part]
    for challenge in data_list:
        md_list.append(f"### {challenge["name"]}")

        for text in text_list:
            if text in challenge:
                md_list.append(challenge[text])

md_str = "\n\n".join(md_list)
write_to_file(yaml_to_md_path, md_str, "w")