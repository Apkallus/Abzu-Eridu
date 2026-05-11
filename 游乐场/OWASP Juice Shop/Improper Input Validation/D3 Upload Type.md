---
title: Upload Type
description: pass
---

- 描述：Upload a file that has no .pdf or .zip extension.
- 上传端点 ```http://127.0.0.1:3000/#/complain```
- 在拦截代理服务器中删除上传 POST 请求体中的文件扩展名，通过挑战