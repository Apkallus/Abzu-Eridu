---
title: Reset Morty's Password
description: 得到可能的密码问题答案后，创建针对性变体单词表。使用 X 头部绕过速率限制
---

- 描述：通过忘记密码机制，使用 Morty 的加密答案来重置他的密码。
- 由 SQL 注入的用户表或 SQL 注入登录后得到的 JWT 可得到
    - 邮件 
    ```morty@juice-sh.op```
    - 密码问题
    ```Name of your favorite pet?```

- SQL 注入登录后使用数据导出功能得到
    ```json
    {
        "username": "",
        "email": "morty@juice-sh.op",
        "orders": [],
        "reviews": [{
            "message": "Even more interesting than watching Interdimensional Cable!",
            "author": "morty@juice-sh.op",
            "productId": 32,
            "likesCount": 0,
            "likedBy": []
        }],
        "memories": []
    }
    ```

- 搜索引擎查询 ```Interdimensional Cable morty pet name```
    得到动画角色 ```morty``` 与对应宠物 ```Snuffles```
    https://rickandmorty.fandom.com/wiki/Morty_Smith#Snuffles
    https://rickandmorty.fandom.com/wiki/Snuffles
    > Snuffles, (who changed his name to Snowball and back again) was Morty's pet dog
    - 尝试名称 ```Snuffles``` 与 ```Snowball``` 的大小写均错误
:x: 未完成，之后尝试创建自己的单词表
- 查看示例解决方案
    - 创建包含这两个名称的字母数字单词表以及 leet 风格的变体，尝试进行爆破
    - 使用 ```X-Forwarded-For``` 头部绕过速率限制

- 代码挑战
    ```typescript
	/* Rate limiting */
	app.enable('trust proxy')
	app.use('/rest/user/reset-password', rateLimit({
	    windowMs: 5 * 60 * 1000,
	    max: 100,
	    keyGenerator({
	        headers,
	        ip
	    }: {
	        headers: any,
	        ip: any
	    }) {
	        return headers['X-Forwarded-For'] ?? ip
	    }
	}))
    ```
    - 漏洞在于使用 X 头部作为密钥生成内容，而 X 头部可被随意修改
    - 修复：移除将 X 头部作为密钥生成的代码

    > 移除允许任意 HTTP 头部优先于客户端 IP 的自定义密钥生成器，是这里的最佳选择。现在攻击者至少需要伪造他们的实际 IP 来绕过速率限制，因为这是这里使用的速率限制模块的默认密钥。不过，存在一个功能上的缺点，因为现在例如企业代理后面的用户可能会作为一个群体被速率限制，而不是单独地。但是，在 5 分钟内允许 100 次密码重置，这种情况不太可能频繁发生。