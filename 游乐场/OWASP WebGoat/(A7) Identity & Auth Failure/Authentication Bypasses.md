---
id: CWE-233
title: Authentication Bypasses
---
<!-- muse start -->
Web Goat 对验证绕过的简单示例。
此处并非移除名值对或值，而是根据字段的命名格式修改名。
<!-- muse end -->

## 1. 认证绕过

认证绕过有多种实现方式，但通常利用配置或逻辑中的某些缺陷。通过篡改创造合适条件。

### 隐藏输入

最简单的情形是依赖网页/DOM中的隐藏输入。

### 移除参数

有时，若攻击者不知道参数的正确值，可能会直接从提交内容中移除该参数以观察结果。

### 强制浏览

若网站的某个区域未通过配置得到适当保护，该区域可能通过猜测/暴力破解方式被访问。

## 2. 双因素认证密码重置

认证绕过的典型案例是2016年发生的PayPal双因素认证绕过事件（https://henryhoggard.co.uk/blog/Paypal-2FA-Bypass）。用户因无法接收短信验证码而选择备用验证方式（安全问题验证）。攻击者通过代理工具完全移除参数并成功绕过认证。

![PayPal双因素认证绕过场景](./images/paypal-2fa-bypass.png)
*WSTG: PayPal双因素认证绕过*

### 场景描述

当您从服务商无法识别的设备或位置重置密码时，系统要求回答预设的安全问题。但这些问题答案存储在另一台设备中（未随身携带），且用户已遗忘答案。

### 验证流程

用户已提供用户名/邮箱信息，并选择备用验证方式。

```
Verify Your Account by answering the questions below:

What is the name of your favorite teacher?
foooooo

What is the name of the street you grew up on?
foooooo
```

探测提交
```http
POST /WebGoat/auth-bypass/verify-account HTTP/1.1
Host: localhost:3000

secQuestion0=fooo&secQuestion1=barr&jsEnabled=1&verifyMethod=SEC_QUESTIONS&userId=12309746
```

尝试按照示例文章彻底移除安全问题的名值对但无法通过，仅移除值也无法通过。
当前字段名为：
`secQuestion0`
`secQuestion1`

不是尝试移除而是根据字段名格式进行修改
在两个字段字段名 `secQuestion[x]` 后添加任意字符，通过挑战