---
title: Poison Null Byte
description: 尝试绕过文件类型的文件名空字节攻击时，也尝试使用多层 URL 编码推迟被解析为空字节的位置。
---
- 描述：Bypass a security control with a Poison Null Byte to access a file not meant for your eyes.
    https://hakipedia.com/index.php/Poison_Null_Byte
- 由已探测的 ```/ftp``` 路径，使用双重 URL 编码的空字节攻击访问对应受限文件 ```GET /ftp/xxx%2500.md HTTP/1.1```