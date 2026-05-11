- Exposed credentials
    - 描述：一位开发者在客户端硬编码了未使用但仍然有效的测试账户凭证，这是疏忽的。
    - 在 ```main.js``` 中搜索关键词 ```test```，找到
        ```javascript                
        testingUsername = "testing@juice-sh.op";
        testingPassword = "IamUsedForTesting";
        ```
        使用此凭证登录后通过挑战