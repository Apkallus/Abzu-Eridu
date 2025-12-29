# 设置目录字符串
pwd_str = """4.10.0 业务逻辑简介
4.10.1 测试业务逻辑数据验证
4.10.2 测试伪造请求的能力
4.10.3 测试完整性检查
4.10.4 测试处理时序
4.10.5 测试功能使用次数限制
4.10.6 测试工作流绕过
4.10.7 测试针对应用程序误用的防御措施
4.10.8 测试意外文件类型上传
4.10.9 测试恶意文件上传
4.10.10 测试支付功能"""

# 设置目录路径
filepath = '渗透架构\\Web 应用程序渗透\\10. 业务逻辑测试'

file_list = pwd_str.split('\n')
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