---
title: Frontend Typosquatting
description: 查询依赖项包时，除了依赖项 package.json 外，还存在自动生成的许可证汇总文件。
---

- 描述：通知商店 http://127.0.0.1:3000/#/contact 有关一个深度渗透到前端领域的拼写错误钓鱼包 typosquatting （提及罪魁祸首的确切名称）

- 查看示例解决方案
    > 请求访问 http://localhost:3000/3rdpartylicenses.txt 以获取 Angular CLI 默认生成的第三方许可证列表

> 3rdpartylicenses.txt 是专为 前端第三方库 生成的许可证汇总文件。Angular 生产环境构建（ng build --prod）时，自动收集所有前端依赖（如 @angular/*、rxjs 等）的许可证信息并生成此文件。
文件存放路径:
构建完成后，该文件位于项目输出目录（如 dist/）的 根目录 下，与 index.html 及编译后的 JS 文件同级。
文本格式:
文件为纯文本格式，内容按 “第三方库名称 + 许可证类型 + 许可证全文” 分段排列。
- 使用与挑战 Legacy Typosquatting 相同方法，在
    https://www.npmjs.com/search?q=
    中搜索包名，根据流行度猜测可能的伪造钓鱼包
    - https://www.npmjs.com/package/ngy-cookie
        同样由 juice shop 开发者上传