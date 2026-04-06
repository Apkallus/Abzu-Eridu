---
title: Legacy Typosquatting
description: 使用双重空字节文件绕过文件类型防护后读取依赖项包数据，在nmp网站查看依赖项包名定位可能的钓鱼包
---

- 描述：通知商店 http://127.0.0.1:3000/#/contact ，它至少在v6.2.0-SNAPSHOT版本中已成为钓鱼网站的受害者。（提及罪魁祸首的确切名称）
- 提示：
    1. Investigating the forgotten developer’s backup file might bring some insight.
    调查被遗忘的开发者备份文件可能会带来一些见解。

    2. "Malicious packages in npm" is a worthwhile read on Ivan Akulov’s blog.
    "Ivan Akulov 博客中的 'npm 中的恶意包'" 值得一看。
- 提示对应 URL
    https://iamakulov.com/notes/npm-malicious-packages/
    这是关于使用 npm 安装包时，存在拼写错误时被安装的名称近似的钓鱼伪造包
    > 始终检查你正在安装的包的名称。你可以查看下载数量：如果一个包很受欢迎但下载数量很低，那就有问题。
- 在 ```/ftp``` 路径中下载包的备份
    http://127.0.0.1:3000/ftp/package.json.bak%2500.md
- 在 npm 网站中搜索包文件中的依赖项包名
    https://www.npmjs.com/search?q=
    最终搜索到拥有很少下载数量的 
    ```epilogue-js```
    输入此包名到反馈表单完成挑战