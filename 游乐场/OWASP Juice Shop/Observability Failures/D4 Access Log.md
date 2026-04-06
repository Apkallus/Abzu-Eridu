---
title: Access Log
description: 对目录进行探测时根据风格对目录或文件名进行转换，对多层目录进行探测，此处为根目录后两层目录
---
- 描述：Gain access to any access log file of the server.
- 访问已知的 ```/ftp``` 文件端点
    - 即使访问大多数文件时响应为
    ```403 Error: Only .md and .pdf files are allowed!```
    然而 ```incident-support.kdbx``` 仍可访问下载
    - 搜索 ```incident-support.kdbx```
        > KeePass数据库文件：
        用于存储加密密码库，通常包含敏感凭证（如系统登录密码、API密钥、数据库连接串等）。
        若未设置强主密码或加密密钥泄露，攻击者可完全获取内部系统权限。
- 查看示例解决方案
- 使用 burp 的攻击器对根目录使用“感兴趣的文件及目录”列表进行爆破
    - ```/api-docs/```
        ```NextGen B2B API
        New & secure JSON-based API for our enterprise customers.
        (Deprecates previously offered XML-based endpoints)
        ```
- 使用 burp 的攻击器对设置集束炸弹攻击 ```/目录列表/目录列表```，设置为小写字母 
    按照返回字符数进行排序，得到 ```support/logs```

- 代码挑战
    - 漏洞在于对 ```/support/logs``` 的路由
    - 修复方法：全部移除
        > 通常情况下，没有必要通过服务器自身的网络URL暴露服务器日志，尤其是在服务器面向互联网时。