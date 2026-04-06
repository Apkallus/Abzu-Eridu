# This application will read roster data in JSON format, parse the file, 
# and then produce an SQLite database that contains a User, Course, 
# and Member table and populate the tables from the data file.
# 该应用程序将读取 JSON 格式的花名册数据，解析文件，然后生成包含用户、课程和成员表的 SQLite 数据库，并从数据文件中填充表。

# You can base your solution on this code: http://www.py4e.com/code3/roster/roster.py - this code is incomplete as you need to modify the program to store the role column in the Member table to complete the assignment.
# 您可以根据以下代码找到解决方案： http://www.py4e.com/code3/roster/roster.py - 
# 此代码不完整，因为您需要修改程序以将角色列存储在成员表中以完成分配。

# Each student gets their own file for the assignment. Download this file:
# 每位学生都会获得一份自己的作业文件。下载此文件：


# Dowload your roster.json data
# 下载你的 roster.json 数据
# And save it as roster_data.json. Move the downloaded file into the same folder as your roster.py program.
# 并将其保存为 roster_data.json 。将下载的文件移动到同一个 文件夹作为您的 roster.py 程序。
# Once you have made the necessary changes to the program 
# and it has been run successfully reading the above JSON data, run the following SQL command:
# 对程序进行必要的更改并且程序成功读取上述 JSON 数据后，请运行以下 SQL 命令：

# SELECT User.name,Course.title, Member.role FROM 
#     User JOIN Member JOIN Course 
#     ON User.id = Member.user_id AND Member.course_id = Course.id
#     ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;
# The output should look as follows:
# Zuzanna|si334|0
# Zoubaeir|si422|0
# Once that query gives the correct data, run this query:
# SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
#     User JOIN Member JOIN Course 
#     ON User.id = Member.user_id AND Member.course_id = Course.id
#     ORDER BY X LIMIT 1;
# You should get one row with a string that looks like XYZZY53656C696E613333.
# 输出应如下所示： 一旦该查询提供正确的数据，请运行此查询： 您应该得到一行类似 XYZZY53656C696E613333 的字符串。




import json
import sqlite3

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER PRIMARY KEY,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER PRIMARY KEY,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')


fname = 'roster_data.json'

# [
#   [
#     "Izaak",
#     "si110",
#     1
#   ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0]
    title = entry[1]
    role = entry[2]


    # print((name, title, role))

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()

cmd = """SELECT User.name, Course.title, Member.role FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2;"""
for row in cur.execute(cmd):
    print(row)

cmd = """SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;"""
for row in cur.execute(cmd):
    print(row)