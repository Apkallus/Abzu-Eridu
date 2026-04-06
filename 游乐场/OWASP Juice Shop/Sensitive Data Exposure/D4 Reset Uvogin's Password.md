---
title: Reset Uvogin's Password
description: 使用社交媒体搜索软件尝试收集目标用户信息，并且根据用户的语言风格推测可能的化名。除当前帖子外，还使用历史档案网站搜索以前的帖子
---
:x: 未完成
- 描述：通过忘记密码机制，使用他安全问题的原始答案来重置Uvogin的密码。
- 已知信息 
    ```"email": "uvogin@juice-sh.op"```
    ```"question":"Your favorite movie?"```
- 应用程序内信息搜集
    - 使用数据导出功能得到评论
        ```json
        {
            "username": "",
            "email": "uvogin@juice-sh.op",
            "orders": [],
            "reviews": [{
                "message": "y0ur f1r3wall needs m0r3 musc13",
                "author": "uvogin@juice-sh.op",
                "productId": 2,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "0 st4rs f0r 7h3 h0rr1bl3 s3cur17y",
                "author": "uvogin@juice-sh.op",
                "productId": 30,
                "likesCount": 0,
                "likedBy": []
            }, {
                "message": "K33p5 y0ur ju1cy 5plu773r 70 y0ur53lf!",
                "author": "uvogin@juice-sh.op",
                "productId": 38,
                "likesCount": 0,
                "likedBy": []
            }],
            "memories": []
        }
        ```
- 提示：人们经常在网上重复使用别名。你可以尝试通过搜索 Uvogin 的名字或根据他独特的写作习惯稍作变体来在线查找相关信息。
- 搜索评论信息为 ```用数字和符号替代外形相似的字母属于 Leet语```

- 查看示例解决方案
    > 人们常常在不同网站上重复使用别名。Sherlock https://github.com/sherlock-project/sherlock 是一个用于查找已知别名/化名的社交媒体账号的绝佳工具。
    尝试几种 ```uvogin``` 的别名变体，```uv0gin``` 带我们来到一个同样写有推文的推特账号，该推文提到了一家易受攻击的饮料店。但关于他最喜欢的电影什么都没有

- 按照 Sherlock 在 Github 的项目页面说明，
    - > 使用 Docker 命令安装容器
    ```docker run -it --rm sherlock/sherlock```
    - > 要搜索单个用户：
    sherlock user123
    - > 找到的账户将被保存在一个单独的文本文件中，并带有相应的用户名（例如 user123.txt ）。
    - :x: 网络连接错误，暂且跳过

- 访问 https://x.com/uv0gin 或许由于未登录，显示此用户未发帖
    > WayBack https://archive.org/web/ 可以用来检查他们的个人资料页面的旧版本，以寻找已删除的推文。确实，WayBack 上可用的快照之一包含一条引用 Silence of the Lambs 的已删除推文，而这条推文实际上是他们安全问题的正确答案。
    - https://archive.org/web/ 网络连接异常