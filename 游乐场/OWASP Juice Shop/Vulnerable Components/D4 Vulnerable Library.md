---
title: Vulnerable Library
descriptions: 使用双重空字节文件绕过文件类型防护后读取依赖项包数据。在 LLM、在线漏洞数据库、CLI工具中识别库及其版本的漏洞
---

- 描述：通知商店 http://127.0.0.1:3000/#/contact 它正在使用的易受攻击的库。（在您的评论中提及确切的库名称和版本）
- 关联挑战 D4 Legacy Typosquatting
    Library
- 在 ```/ftp``` 路径中下载包的备份
    http://127.0.0.1:3000/ftp/package.json.bak%2500.md

- 复制依赖项列表到 LLM 中搜索，出现多个易受攻击的库
    ```
    express-jwt: 0.1.3
    sanitize-html: 1.4.2
    sequelize: ~4
    ...
    ```
- 提交第一项 ```"express-jwt": "0.1.3"``` 到客户反馈功能后通过挑战
- 示例解决方案
    > 使用像 Retire.js https://retirejs.github.io/ 这样的在线漏洞数据库或 npm-audit https://docs.npmjs.com/cli/audit/ 这样的 CLI 工具（随 Node.js 提供），可以相对容易地识别它。