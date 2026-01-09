# 设置目录字符串
file_str = """4.12.0 API测试概述
4.12.1 API侦察
4.12.2 API失效的对象级授权
4.12.99 GraphQL测试"""

# 设置目录路径
filepath = '渗透架构\\Web 应用程序渗透\\12. API 测试'

file_list = file_str.split('\n')
# 去掉 "4." 部分
file_clear_list = [e.strip()[2:] for e in file_list]
print(file_clear_list)

try:
    for new_file in file_clear_list:
        with open(f'{filepath}\\{new_file}.md', 'x', encoding='utf-8') as f:
            # 只需 split 分割一次即可达到保留文件名中的空格的效果
            title = new_file.split(' ', 1)[1]
            print(title)
            f.write(f'# {title}\n\n')
except FileExistsError:
    print('目录字符串中的文件已存在')
    raise

# 将目录字符串拆分为字符串列表，遍历列表创建对应文件并写入文件名为一级标题