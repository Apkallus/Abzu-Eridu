pwd_str = """4.7.1 反射型跨站脚本测试
4.7.2 存储型跨站脚本测试
4.7.3 HTTP方法篡改测试
4.7.4 HTTP参数污染测试
4.7.5 SQL注入测试
 4.7.5.1 Oracle数据库测试
 4.7.5.2 MySQL数据库测试
 4.7.5.3 SQL Server数据库测试
 4.7.5.4 PostgreSQL数据库测试
 4.7.5.5 MS Access数据库测试
 4.7.5.6 NoSQL注入测试
 4.7.5.7 ORM注入测试
 4.7.5.8 客户端注入测试
4.7.6 LDAP注入测试
4.7.7 XML注入测试
4.7.8 SSI注入测试
4.7.9 XPath注入测试
4.7.10 IMAP与SMTP注入测试
4.7.11 代码注入测试
 4.7.11.1 文件包含测试
4.7.12 命令注入测试
4.7.13 格式化字符串注入测试
4.7.14 潜伏性漏洞测试
4.7.15 HTTP拆分与走私测试
4.7.16 HTTP传入请求测试
4.7.17 Host头注入测试
4.7.18 服务端模板注入测试
4.7.19 服务端请求伪造测试
4.7.20 批量赋值测试"""

filepath = '渗透架构\\Web 应用程序渗透\\7. 输入验证测试'

file_list = pwd_str.split('\n')
# 去掉 "4." 部分
file_clear_list = [e.strip()[2:] for e in file_list]
print(file_clear_list)

try:
    for new_file in file_clear_list:
        with open(f'{filepath}\\{new_file}.md', 'x', encoding='utf-8') as f:
            # 提取文件名
            f.write(f'# {new_file.split()[1]}\n\n')
except FileExistsError:
    print('目录字符串中的文件已存在')
    raise

# 将目录字符串拆分为字符串列表，遍历列表创建对应文件并写入文件名为一级标题