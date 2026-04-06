---
id: CWE-261
title: Spoofing an Authentication Cookie
---
<!-- muse start -->
会话ID（cookie）使用多层简单编码而不是加密或加盐散列。
此处在Base64解码-HEX解码-字符串翻转后得到Cookie的构造格式，从而创造Cookie
<!-- muse end -->

## 概念  

认证系统的安全性关键在于Cookie生成算法必须安全且不易被猜测。若攻击者能预测或确定该算法，则可能为其他用户生成有效的认证Cookie，从而绕过认证机制并冒充用户。  

为降低此风险，必须采用强健且加密安全的算法生成认证Cookie。这些算法应使用强随机化和哈希技术，确保生成Cookie的唯一性和不可预测性。此外，实施会话过期和定期轮换认证Cookie等措施可进一步提升安全性。通过频繁更改Cookie值并强制会话超时，可显著减少攻击者利用潜在漏洞的机会窗口。  

## 通过伪造认证Cookie尝试绕过认证机制

### 登录系统说明

当收到有效的认证Cookie时，系统将自动为用户登录。
若未发送Cookie但提供的凭据正确，系统将生成认证Cookie。
其他任何情况下登录尝试均将被拒绝。
请密切关注攻击过程中收到的反馈信息。

已知凭据:

| 用户名 | 密码    |
|--------|---------|
| webgoat | webgoat |
| admin  | admin   |

### 目标

分析认证Cookie生成原理，尝试伪造Cookie并以Tom身份登录。

webgoat:
spoof_auth=NmY2ODVhNDY1MjQ4NmY2YjczNDM3NDYxNmY2NzYyNjU3Nw==

admin:
spoof_auth=NmY2ODVhNDY1MjQ4NmY2YjczNDM2ZTY5NmQ2NDYx

对 `NmY2ODVhNDY1MjQ4NmY2YjczNDM3NDYxNmY2NzYyNjU3Nw==`
进行 Base 64 解码，得到
`6f685a4652486f6b734374616f67626577`
继续进行 Hex 解码，得到
`ohZFRHoksCtaogbew`
翻转，得到
`webgoatCskoHRFZho`

对 `NmY2ODVhNDY1MjQ4NmY2YjczNDM2ZTY5NmQ2NDYx`
进行上述多步后，得到
`ohZFRHoksCnimda`
`adminCskoHRFZho`

分析得出Cookie的格式为
前半部分为 `用户名`
后半部分为 `CskoHRFZho`

目标 `Tom`，反向步骤。
字符串为
`TomCskoHRFZho`
反转，得到
`ohZFRHoksCmoT`
Hex编码，得到
`6F685A4652486F6B73436D6F54`
Base 64 编码，得到
`NkY2ODVBNDY1MjQ4NkY2QjczNDM2RDZGNTQ=`

编辑头部，添加设计的 Cookie `spoof_auth=NkY2ODVBNDY1MjQ4NkY2QjczNDM2RDZGNTQ=` 通过挑战