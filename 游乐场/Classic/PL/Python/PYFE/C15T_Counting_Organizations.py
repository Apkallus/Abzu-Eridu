# -- This application will read the mailbox data (mbox.txt) and count the number of email messages per organization (i.e. domain name of the email address) using a database with the following schema to maintain the counts.
# -- 这个应用程序将读取邮箱数据（mbox.txt），
# -- 并使用一个具有以下架构的数据库来维护每个组织的电子邮件消息数量（即电子邮件地址的域名）。

# -- CREATE TABLE Counts (org TEXT, count INTEGER)
# -- When you have run the program on mbox.txt upload the resulting database file above for grading.
# -- 运行程序处理 mbox.txt 后，将生成的数据库文件上传至此处进行评分。
# -- If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.
# -- 如果你在测试或使用不同文件时多次运行程序，请确保在每次运行前清空数据。

# -- You can use this code as a starting point for your application: http://www.py4e.com/code3/emaildb.py.
# -- 你可以使用这段代码作为你的应用程序的起点：http://www.py4e.com/code3/emaildb.py。

# -- The data file for this application is the same as in previous assignments: http://www.py4e.com/code3/mbox.txt.
# -- 这个应用程序的数据文件与之前的作业相同：http://www.py4e.com/code3/mbox.txt。

# -- Because the sample code is using an UPDATE statement and committing the results to the database as each record is read in the loop, it might take as long as a few minutes to process all the data. The commit insists on completely writing all the data to disk every time it is called.
# -- 因为示例代码使用 UPDATE 语句，并在循环中每次读取记录时将结果提交到数据库，
# -- 所以处理所有数据可能需要几分钟的时间。提交操作坚持每次调用时将所有数据完全写入磁盘。

# -- The program can be speeded up greatly by moving the commit operation outside of the loop. In any database program, there is a balance between the number of operations you execute between commits and the importance of not losing the results of operations that have not yet been committed.
# -- 通过将提交操作移出循环，可以大大提高程序的运行速度。在任何数据库程序中，
# -- 执行提交操作之间的操作次数与不丢失尚未提交操作结果的重要性之间需要保持平衡。

import sqlite3
import re

# 连接并打开数据库文件
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

# 对数据文件进行处理
fname = 'code3/mbox.txt'
fh = open(fname)
## 读取数据文件并更新数据库
# for line in fh:
#     # 使用正则表达式提取域名
#     org_list = re.findall(r'^From \w+@(\w+)', line)
#     for org in org_list:   
#         # 查看org是否存在于数据库中，若无则初始化为1,否则+1
#         cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
#         row = cur.fetchone()
#         if row is None:
#             cur.execute('''INSERT INTO Counts (org, count)
#                     VALUES (?, 1)''', (org,))
#         else:
#             cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
#                         (org,))
#         conn.commit()

## 读取数据文件，将内容保存在内存中，之后一次性录入到数据库
org_dict = {}
for line in fh:
    # 使用正则表达式提取域名，并录入到字典
    org_list = re.findall(r'^From \S+@(\S+)', line)
    for org in org_list:   
        org_dict[org] = org_dict.get(org, 0) + 1

# 使用字典的key,value录入到数据库
for org, count in list(org_dict.items()):
    cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, ?)''', (org, count))
conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(row[0], row[1])

cur.close()
