---
title: Misplaced Signature File
description: 尝试绕过文件类型的文件名空字节攻击时，也尝试使用多层 URL 编码推迟被解析为空字节的位置。
---
- 描述：访问一个放置错误的 SIEM signature https://github.com/Neo23x0/sigma 文件。
- 在 ```/ftp``` 目录下尝试绕过限制读取文件，使用文件名空字节截断攻击
    - 若访问不存在的路径 
        ```Error: ENOENT: no such file or directory```
    - 使用 ```%00``` 
        ```BadRequestError: Bad Request```
- 查看示例解决方案
- 在之前的攻击向量中 ```%00``` 并未被解析为普通路径，而是有效的作为空字节但导致错误
    - 使用多重 URL 编码 ```%2500```尝试推迟被解析为空字节的位置
- 访问对应安全信息管理的可能的文件名“可疑的错误” ```http://127.0.0.1:3000/ftp/suspicious_errors.yml%2500.md```
    ```md
    title: Suspicious error messages specific to the application
    description: Detects error messages that only occur from tampering with or attacking the application
    author: Bjoern Kimminich
    logsource:
        category: application
        product: nodejs
        service: errorhandler
    detection:
        keywords:
            - 'Blocked illegal activity'
            - '* with id=* does not exist'
            - 'Only * files are allowed'
            - 'File names cannot contain forward slashes'
            - 'Unrecognized target URL for redirect: *'
            - 'B2B customer complaints via file upload have been deprecated for security reasons'
            - 'Infinite loop detected'
            - 'Detected an entity reference loop'
        condition: keywords
    level: low
    ```