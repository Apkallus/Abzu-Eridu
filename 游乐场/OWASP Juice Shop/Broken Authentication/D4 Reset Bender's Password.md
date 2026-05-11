---
title: Reset Jim's Password
description: pass
---

- 描述：通过忘记密码机制，使用他安全问题的原始答案来重置Bender的密码。
- 已知信息 
    ```"email": "bender@juice-sh.op"```
    ```"question":"Company you first work for as an adult?"```
- 应用程序内信息搜集
    - 使用数据导出功能查看评论
        ```http://127.0.0.1:3000/#/privacy-security/data-export```
        ```json
        {
            "username": "",
            "email": "bender@juice-sh.op",
            "orders": [],
            "reviews": [{
                "message": "Fry liked it too.",
                "author": "bender@juice-sh.op",
                "productId": 6,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Will put one on the Planet Express ship's bumper!",
                "author": "bender@juice-sh.op",
                "productId": 37,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Puny mask for puny human weaklings!",
                "author": "bender@juice-sh.op",
                "productId": 38,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Ooooh, puny human playing Mau Mau, now?",
                "author": "bender@juice-sh.op",
                "productId": 39,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Mau Mau with bling-bling? Humans are so pathetic!",
                "author": "bender@juice-sh.op",
                "productId": 40,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "Just when my opinion of humans couldn't get any lower, along comes Stan...",
                "author": "bender@juice-sh.op",
                "productId": 42,
                "likesCount": 0,
                "likedBy": []
            }],
            "memories": []
        }
        ```
    - 查看保存的地址
        ```http://127.0.0.1:3000/#/address/saved```
        ```
        Bender
        Robot Arms Apts 42, New New York, New New York, 10001
        Planet Earth 
        ```
- 分析应用程序内搜集到的信息
    - 搜索 ```Planet Express ship's```
        > 《星际快递飞船》由教授命名为老贝西，是一艘明亮的绿色（实际名称为电性粘液）的送货飞船，属于 Planet Express。It is used by Bender, Fry, and Leela
        - 对应 ```飞出个未来 Futurama``` 
        - 角色名匹配 ```Fry liked it too.```
    - 搜索 ```Futurama bender```
        > Bender Bending Rodríguez, (born September 4, 2996), designated Bending Unit 22, and commonly known as Bender, is a bending unit created by a division of MomCorp in Tijuana, Mexico, and his serial number is 2716057.
        > 作为一个弯曲单元，在他遇到弗雷之前，他的一生都在弯曲横梁，用于建造 Suicide booths。
        > Suicide booth 是在 2006 年至 2008 年间发明的。自 2008 年以来，美国最重要的 Suicide booth 品牌是 Stop'n'Drop
- 使用问题答案 ```Stop'n'Drop``` 修改密码

- 代码修复：彻底移除修改代码的安全问题