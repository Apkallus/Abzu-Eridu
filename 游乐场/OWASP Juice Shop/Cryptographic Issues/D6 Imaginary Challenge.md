---
title: Imaginary Challenge
description: 获取多个混淆序列样本进行分析，根据字符串类型与模式在依赖项列表中查找对应库。检索库的文档获取使用信息，根据样本分析模式推测对应参数，在其他不确定参数中使用默认或示例的参数进行测试。或许还要查看版本的功能区别，使用旧版本并查看过时的文档
---

- 描述：```Solve challenge #999. Unfortunately, this challenge does not exist.```

- 提示：
    > 了解后台如何保存和恢复进度。
    根据所有可用信息（例如 package.json.bak），推断应用程序如何加密和解密你的黑客进度。

- 保存进度的请求
    ```GET /rest/continue-code HTTP/1.1```
    响应
    ```json
    {
        "continueCode": "pkHMulhrtbclI5CMiQfRSPU6H7u8hPtkclIkT6CwsVF9iQf7SKUYH3uQh4tecrI9TBCPsBFLiBSeURHWpuoohyetx4cX6IEOTa6C5Ds8bFlNibEfkaSgjUMEHkgunQhp2tROI8XTYvC6QsEXFYOiyPfVXSYoULwHw2tqmc4rI7nTxYC5xsj7FkYiBefmqSg7UaQH2BuzPh2yt61cQQIPBTLZC7YsRXFNOiLvfYZSbjUDPHbPuRvhXxtL2cgXIM1TNzC9ZsRp"
    }
    ```
- 恢复进度的请求
    ```PUT /rest/continue-code/apply/pkHMulhrtbclI5CMiQfRSPU6H7u8hPtkclIkT6CwsVF9iQf7SKUYH3uQh4tecrI9TBCPsBFLiBSeURHWpuoohyetx4cX6IEOTa6C5Ds8bFlNibEfkaSgjUMEHkgunQhp2tROI8XTYvC6QsEXFYOiyPfVXSYoULwHw2tqmc4rI7nTxYC5xsj7FkYiBefmqSg7UaQH2BuzPh2yt61cQQIPBTLZC7YsRXFNOiLvfYZSbjUDPHbPuRvhXxtL2cgXIM1TNzC9ZsRp HTTP/1.1```
    清除数据后对初始状态的进度字符串为
    ```PUT /rest/continue-code/apply/Wb351y8noRVw6yLkJ5Yxv7MObe2EAVqg0zKQljaNWpmXBZD4qP3gr91X6OkJ HTTP/1.1```

- 进度字符串长度随进度增加
- 将依赖项与两个进度字符串放到 LLM 分析后最可能的库是 hashids

- 示例解决方案：
    > 1. 点击标有查看演示的链接（ http://codepen.io/ivanakimov/pen/bNmExm）
    2. Juice Shop 仅使用了示例盐（ this is my salt ）和该演示页面的默认字符范围（ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ）。它只是将结果哈希的最小长度设置为 60 而不是 8
    3. 使用示例（见下方代码）对值 999 进行编码，可得到哈希结果 69OxrZ8aJEgxONZyWoz1Dw4BvXmRGkM6Ae9M7k2rK63YpqQLPjnlb5V5LvDj
    - 演示链接已失效，官网文档仅包含打乱字母表以及设置长度，未提及加盐
    - 官网的默认字符范围与示例解决方案相同
    - 由初始状态的字符串长度 60 的确可知设置的最小字符串长度值为 60
    - 唯一无法直接得到的内容，是加盐这个功能的存在以及默认或示例的盐
        - 过时文档提到加盐这个功能且能够看到 this is my salt 作为示例出现。能够回推

    - 然而进一步查看 FQA 时发现此库已经移除了加盐的功能
        > 为什么移除了盐参数？
        盐参数用于打乱字母顺序，它从未打算与安全性或安全性相关联。Hashids 和 Sqids 的工作方式与十进制到十六进制的转换类似，但有一些调整。没有任何加密，为了避免混淆，该参数已被完全移除。
    - 需使用旧版或不一定存在的兼容模式进行加盐