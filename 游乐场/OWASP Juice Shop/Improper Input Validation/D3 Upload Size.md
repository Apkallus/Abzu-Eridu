---
title: Upload Size
description: pass
---

- 描述：Upload a file larger than 100 kB.
- 上传端点 ```http://127.0.0.1:3000/#/complain```
    - 直接选择大文件时提示 ```File too large. Maximum 100 KB allowed. ``` 
    并禁用提交按钮
    - 提交一个限制内的 PDF 文件
        - 第一个请求 
            ```POST /file-upload HTTP/1.1```
            响应
            ```HTTP/1.1 204 No Content```
        - 第二个请求
            ```POST /api/Complaints/ HTTP/1.1```
            响应
            ```HTTP/1.1 201 Created```
            ```json
            {
                "status": "success",
                "data": {
                    "id": 10,
                    "UserId": 2,
                    "message": "a",
                    "updatedAt": "2025-12-14T02:39:57.652Z",
                    "createdAt": "2025-12-14T02:39:57.652Z",
                    "file": null
                }
            }
            ```
    - 修改HTML界面，则仅包含投诉端点的请求，未发出上传文件请求
    - 仅在 ```POST /file-upload HTTP/1.1```的请求体中填充字符无法通过实验
    - 查看示例解决方案
    - 缺乏编辑 POST 请求体内容中选择文件的工具，构建 HTML 页面
        ```html
        <html>
        <body>
            <form action="http://localhost:3000/file-upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file"/>
            <input type="submit" value="Submit request" />
            </form>
        </body>
        </html>
        ```
        - 上传小文件得到 ```HTTP/1.1 201 Created``` 
        - 上传 400KB 大文件得到 ```HTTP/1.1 500 Internal Server Error```
            ```MulterError: File too large```
        - 上传一个略大于限制的文件得到 ```HTTP/1.1 201 Created``` 后通过挑战