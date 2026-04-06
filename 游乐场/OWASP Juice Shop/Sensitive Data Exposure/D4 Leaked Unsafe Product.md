---
title: Leaked Unsafe Product
description: SQL 注入得到下架的产品信息，搜索引擎检索关键词获得此产品的更多内容，如产品名与描述或成分
---

- 描述：识别出从商店中撤下的不安全产品，并告知 http://127.0.0.1:3000/#/contact 商店哪些成分是危险的。
- 由之前挑战的 SQL 注入查询得到的产品表检索到对应产品信息
    ```json
    {
        "id": 11,
        "name": "Rippertuer Special Juice",
        "description": "Contains a magical collection of the rarest fruits gathered from all around the world, like Cherymoya Annona cherimola, Jabuticaba Myrciaria cauliflora, Bael Aegle marmelos... and others, at an unbelievable price! <br/><span style=\"color:red;\">This item has been made unavailable because of lack of safety standards.</span> (This product is unsafe! We plan to remove it from the stock!)",
        "price": 16.99,
        "deluxePrice": 16.99,
        "image": "undefined.jpg",
        "createdAt": "2025-12-14 04:39:27.597 +00:00",
        "updatedAt": "2025-12-14 04:39:27.597 +00:00",
        "deletedAt": "2025-12-14 04:39:27.769 +00:00"
    }
    ```
- 轮流提交列出的三种成分仍无法通过挑战
    - 搜索 ```Rippertuer Special Juice``` 
    得到对此商品成分的详细描述 https://pastebin.com/90dUgd7s
    其中 
        ```
        Hueteroneel
        请注意，这种水果与 Eurogium Edule 一起食用有时会导致致命，尽管相关报告很少。
        ```
- 提交 ```Hueteroneel Eurogium Edule``` 通过挑战