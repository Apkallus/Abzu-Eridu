---
title: Nested Easter Egg
description: 根据字符串特征判断加密方式
---

- 描述：应用一些高级密码分析来找到真正的复活节彩蛋。
- 关联挑战 Easter Egg 中在 ```ftp``` 路径读取的文件内容
    ```L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==```
    - Base64 解码为
        ```/gur/qrif/ner/fb/shaal/gurl/uvq/na/rnfgre/rtt/jvguva/gur/rnfgre/rtt```

- 查看示例解决方案
    > 注意上述字符串中重复的模式（ rtt 、 gur 等）
    将此 ROT13 解码为 /the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg
- 字母全小写、特殊符号不变、字符串长度不定、模式重复出现