- Deluxe Fraud
    - 描述：免费获得高级会员资格。
    - 访问高级会员页面
        ```http://127.0.0.1:3000/#/deluxe-membership```
        对应请求
        ```GET /rest/deluxe-membership HTTP/1.1```
        - 此时使用管理员账户，尝试使用 ```POST``` 方法，得到错误响应
            ```json
            {
                "status": "error",
                "error": "Something went wrong. Please try again!"
            }
            ```
    - 使用管理员账户时显示
        ```You are not eligible for deluxe membership!```
    - 使用新账户显示“成为会员”按钮，点击后进入
        ```http://127.0.0.1:3000/#/payment/deluxe```
        - 支付请求
            ```POST /rest/deluxe-membership HTTP/1.1```
            ```json
            {
                "paymentMode": "card",
                "paymentId": 7
            }
            ```
        - 响应的 JWT 中的变化
            ```json
            "role":"deluxe","deluxeToken":"05d0fbd5c74a6aecf73819d9559e8766e84b731670274e588b4e8d9ff1237e0e"
            ```
            - 尝试使用注册管理员账户时修改表单 JSON 的漏洞，虽然可设置字段，但无法未成为高级会员
    - 创建新账户，使用 POST 方法，请求体为空，通过挑战，JWT 未变化
    - 示例解决方案：
        >  将 paymentMode 参数更改为空字符串并发送，Juice Shop 不再知道从哪里扣除款项
    - 修改或移除参数进入预期外行为，此处为扣款方式