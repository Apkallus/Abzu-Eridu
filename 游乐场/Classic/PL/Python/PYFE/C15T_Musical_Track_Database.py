# This application will read an iTunes export file in CSV format and produce a properly normalized database with this structure:
# 该应用程序将读取 CSV 格式的 iTunes 导出文件，并生成一个结构正确的规范化数据库：

# CREATE TABLE Artist (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name    TEXT UNIQUE
# );

# CREATE TABLE Genre (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name    TEXT UNIQUE
# );

# CREATE TABLE Album (
#     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     artist_id  INTEGER,
#     title   TEXT UNIQUE
# );

# CREATE TABLE Track (
#     id  INTEGER NOT NULL PRIMARY KEY 
#         AUTOINCREMENT UNIQUE,
#     title TEXT  UNIQUE,
#     album_id  INTEGER,
#     genre_id  INTEGER,
#     len INTEGER, rating INTEGER, count INTEGER
# );
# If you run the program multiple times in testing or with different files, make sure to empty out the data before each run.
# 如果你在测试或使用不同文件时多次运行程序，请确保在每次运行前清空数据。

# You can use this code as a starting point for your application: http://www.py4e.com/code3/tracks.zip. The ZIP file contains the tracks.csv file to be used for this assignment. You can export your own tracks from iTunes and create a database, but for the database that you turn in for this assignment, only use the tracks.csv data that is provided. You can adapt the tracks_csv.py application in the zip file to complete the assignment.
# 您可以使用此代码作为应用程序的起点：http://www.py4e.com/code3/tracks.zip。
# ZIP 文件包含用于本次作业的 tracks.csv 文件。
# 您可以从 iTunes 导出自己的曲目并创建数据库，但对于您提交的作业数据库，仅使用提供的 tracks.csv 数据。
# 您可以修改 zip 文件中的 tracks_csv.py 应用程序来完成作业。

# To grade this assignment, the program will run a query like this on your uploaded database and look for the data it expects to see:
# 为了评分这个作业，程序将在你上传的数据库上运行类似以下的查询，并查找它期望看到的数据：

# SELECT Track.title, Artist.name, Album.title, Genre.name 
#     FROM Track JOIN Genre JOIN Album JOIN Artist 
#     ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
#         AND Album.artist_id = Artist.id
#     ORDER BY Artist.name LIMIT 3
# The expected result of the modified query on your database is: (shown here as a simple HTML table with titles)
# 你数据库中修改后的查询的预期结果是：（这里以简单的 HTML 表格形式显示标题）

# Track	                                    Artist	Album	        Genre
# Chase the Ace	                            AC/DC	Who Made Who	Rock
# D.T.	                                    AC/DC	Who Made Who	Rock
# For Those About To Rock (We Salute You)	AC/DC	Who Made Who	Rock

import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# execute() 执行单条语句
# executescript() 执行多条语句
# Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Genre;
                  
CREATE TABLE Artist (
    id  INTEGER PRIMARY KEY,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER PRIMARY KEY,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER PRIMARY KEY,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
                  
CREATE TABLE Genre (
    id  INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);
''')
# 新增 Genre 表， 使用 name 作为列

handle = open('code3/tracks/tracks.csv')


# Another One Bites The Dust,Queen,Greatest Hits,55,100,217103
#   0                          1      2           3  4   5

# Asche Zu Asche,Rammstein,Herzeleid,79,100,231810,Industrial

for line in handle:
    line = line.strip()
    pieces = line.split(',')
    if len(pieces) < 6 : continue

    name = pieces[0]
    artist = pieces[1]
    album = pieces[2]
    count = pieces[3]
    rating = pieces[4]
    length = pieces[5]
    # 新增流派
    genre = pieces[6]

    # print(name, artist, album, count, rating, length, genre)
    # fetchone() 读取一行 
    
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count, genre_id) 
        VALUES ( ?, ?, ?, ?, ?, ? )''', 
        ( name, album_id, length, rating, count, genre_id ) )
    


    conn.commit()

check = ("""SELECT Track.title, Artist.name, Album.title, Genre.name 
    FROM Track JOIN Genre JOIN Album JOIN Artist 
    ON Track.genre_id = Genre.ID and Track.album_id = Album.id 
        AND Album.artist_id = Artist.id
    ORDER BY Artist.name LIMIT 3""")
for row in cur.execute(check):
    print(row)