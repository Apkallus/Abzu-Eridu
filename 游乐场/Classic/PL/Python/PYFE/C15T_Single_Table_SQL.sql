-- 如果您还没有安装，请安装 SQLite 浏览器 http://sqlitebrowser.org/.

-- 然后，创建一个 SQLITE 数据库或使用现有的数据库，并在数据库中创建一个名为"Ages"的表：

CREATE TABLE Ages ( 
  name VARCHAR(128), 
  age INTEGER
)
-- 确保表为空，方法是删除之前插入的任何行，并使用以下命令插入这些行且仅插入这些行：

DELETE FROM Ages;
INSERT INTO Ages (name, age) VALUES ('Lucie', 13);
INSERT INTO Ages (name, age) VALUES ('Luci', 34);
INSERT INTO Ages (name, age) VALUES ('Piotr', 18);
INSERT INTO Ages (name, age) VALUES ('Damien', 32);
INSERT INTO Ages (name, age) VALUES ('Rajan', 15);

-- 插入完成后，运行以下 SQL 命令： 
-- 字符串拼接后转十六进制，再排序
SELECT hex(name || age) AS X FROM Ages ORDER BY X

-- 找到结果记录集中的第一行，并输入看起来像 53656C696E613333 的長字符串。

-- 注意： 这个作业必须使用 SQLite - 特别是上面提到的 SELECT 查询在其他任何数据库中都不会工作。
-- 所以你不能用 MySQL 或 Oracle 来完成这个作业。