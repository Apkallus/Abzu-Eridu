---
title: Premium Paywall
description: 查看 HTML 注释获取隐藏信息，分析字符串加密/混淆类型，分析从路径爆破探测到的文件的与此的关联与类型。使用文件内容对加密字符串进行解密
---

- 描述：Unlock Premium Challenge https://blockchain.info/address/1AbKfgvw9psQ41NbLi8kufDQTezwG8DRZm to access exclusive content.

- 查看此挑战在计分板的 HTML 代码
    得到一个特殊的注释内容
    ```IvLuRfBJYlmStf9XfL6ckJFngyd9LfV1JaaN/KRTPQPidTuJ7FR+D/nkWJUF+0xUF07CeCeqYfxq+OJVVa0gNbqgYkUNvn//UbE7e95C+6e+7GtdpqJ8mqm4WcPvUGIUxmGLTTAC2+G9UuFCD1DUjg==```
    - 在 LLM 进行模式分析为 AES加密（CBC模式）
        - 初始化向量 开头 
        ```IvLuRfBJYlmStf9XfL6ckJ```
        - 密文主体 其余部分 
        ```Fngyd9LfV1JaaN/KRTPQPidTuJ7FR+D/nkWJUF+0xUF07CeCeqYfxq+OJVVa0gNbqgYkUNvn//UbE7e95C+6e+7GtdpqJ8mqm4WcPvUGIUxmGLTTAC2+G9UuFCD1DUjg==```

- 之前的挑战中在尝试得到 JWT 公钥时，其目录
    http://localhost:3000/encryptionkeys
    还包括文件 ```premium.key```
    内容为
    ```1337133713371337.EA99A61D92D2955B1E9285B55BF2AD42```

- 查看示例解决方案
    > 为了解密密文，最好使用 openssl 。
    ```bash
    echo "IvLuRfBJYlmStf9XfL6ckJFngyd9LfV1JaaN/KRTPQPidTuJ7FR+D/nkWJUF+0xUF07CeCeqYfxq+OJVVa0gNbqgYkUNvn//UbE7e95C+6e+7GtdpqJ8mqm4WcPvUGIUxmGLTTAC2+G9UuFCD1DUjg==" | openssl enc -d -aes-256-cbc -K EA99A61D92D2955B1E9285B55BF2AD42 -iv 1337133713371337 -a -A
    ```

    > "-d": "解密模式",
   "-aes-256-cbc": "使用AES-256-CBC加密算法",
   "-K": "指定密钥（16进制格式）",
   "-iv": "指定初始化向量（IV，16进制格式）",
   "-a": "Base64解码输入",
   "-A": "逐行Base64解码"
   "-K"/"-iv" 自动将输入的字符串转换为16进制格式，不足则补0