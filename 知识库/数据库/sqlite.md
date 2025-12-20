- 模式，https://sqlite.org/schematab.html
    > 每个 SQLite 数据库都包含一个"模式表"，用于存储该数据库的模式。数据库的模式是对数据库中包含的所有其他表、索引、触发器和视图的描述。模式表如下所示：
    ```sql
    CREATE TABLE sqlite_schema(
        type text,
        name text,
        tbl_name text,
        rootpage integer,
        sql text
    );
    ```