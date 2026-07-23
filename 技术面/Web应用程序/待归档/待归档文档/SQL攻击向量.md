- SQL 注入速查表
    - [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection/cheat-sheet)

- 将输入拼接到 SQL 而不是预处理时出现 SQL 注入
- 探查
    - 对于文本，输入```'```查看是否出现错误
    - 对于数字，输入运算符查看是否计算。
        - 例，输入 ```1+1``` 查看是否为 ```2```
- 注释 ```--```
    - 在登录页面的账户名或邮箱后尝试注释掉后续内容，如密码匹配
        - 靶场 OWASP Juice Shop - Injection - Login Admin 使用管理员账户登录，在获得管理员邮箱后
            - 在用户邮箱处设置攻击向量 ```admin@juice-sh.op'==``` 注释后续密码匹配
            - 漏洞代码的 SQL
                ```typescript
                SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL
                ```
            - 或者，在用户邮箱处设置攻击向量 ```' or 1=1==``` SQL 查询整个列表，应用程序读取第一条，而第一个用户或许为管理员账户
            -  或者，```' or 1=1 ORDER BY 1 LIMIT 1 OFFSET 0 --``` 修改 ```OFFSET``` 的值按顺序登录账户，直到登录管理员账户
            
- OWASP Juice Shop - Injection - Database Schema
    - 根据错误信息设计基准向量
    - 使用 ```ORDER BY``` 测试原查询列数
    - 搜索数据库模式表信息
    - 构建联合查询获取模式表信息