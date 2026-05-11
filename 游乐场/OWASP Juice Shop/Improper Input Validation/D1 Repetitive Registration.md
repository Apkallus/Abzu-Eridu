- Repetitive Registration
    - 描述：在注册用户时遵循DRY原则。
    - 提示：绕过重复输入密码
    - 在拦截代理服务器中查看注册账户的请求
        ```POST /api/Users/ HTTP/1.1```
        ```json
        {
            "email": "test@a",
            "password": "12345",
            "passwordRepeat": "12345",
            "securityQuestion": {
                "id": 7,
                "question": "Name of your favorite pet?",
                "createdAt": "2025-12-10T10:55:05.438Z",
                "updatedAt": "2025-12-10T10:55:05.438Z"
            },
            "securityAnswer": "none"
        }
        ```
        - 删除 ```passwordRepeat``` 名值对后发送请求通过挑战
    - 示例解决方案：
    在输入密码与密码重复后，返回密码栏修改后仍可注册。
    - 修改时，仅对密码栏检查一次，持续对重复密码栏检查
    - 后端未对注册的数据进行检查