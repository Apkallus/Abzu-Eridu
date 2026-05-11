- Error Handling
    - 描述：引发一个既不优雅也不一致处理的错误。
    - 只是访问账户页面时
    ```http://127.0.0.1:3000/profile```
    意外得到错误响应后完成挑战
    ```HTTP/1.1 500 Internal Server Error```
        ```html
        <div id="wrapper">
        <h1>OWASP Juice Shop (Express ^4.21.0)</h1>
        <h2><em>500</em> Error: Blocked illegal activity by ::ffff:172.17.0.1</h2>
        <ul id="stacktrace"><li> &nbsp; &nbsp;at /juice-shop/build/routes/userProfile.js:72:18</li></ul>
        </div>
        ```
        的确故障，账号与挑战进度消失，重新开始挑战，之后应当经常使用进度备份功能
    - 提示：
        > 尝试向表单提交不良输入。或者篡改 URL 路径或参数。
    - 示例解决方案：
        - 访问不存在的 URL 路径参数
        ```http://localhost:3000/rest/qwertz```
        - 登录时使用 SQL 注入的冗余单引号 ```'```
