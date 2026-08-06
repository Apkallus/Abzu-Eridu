
## Referer 的验证可以被绕过

某些应用程序以简陋的方式验证 `Referer` 头，可以被绕过。例如，如果应用程序验证 `Referer` 中的域以预期值开头，则攻击者可以将此值作为自己域的子域放置：

```
http://vulnerable-website.com.attacker-website.com/csrf-attack
```

同样，如果应用程序仅验证 `Referer` 包含其自身的域名，则攻击者可以将所需值放在 URL 的其他位置：

```
http://attacker-website.com/csrf-attack?vulnerable-website.com
```

> **注意：** 尽管你可能能够使用 Burp 识别此行为，但当你去浏览器中测试概念验证时，通常会发现在这种情况下这种方法不再有效。为了降低以这种方式泄露敏感数据的风险，许多浏览器现在默认从 `Referer` 头中剥离查询字符串。
>
> 你可以通过确保包含你攻击的响应设置了 `Referrer-Policy: unsafe-url` 头来覆盖此行为（请注意此处 `Referrer` 拼写正确，只是为了确保你注意到这一点！）。这确保将发送完整的 URL，包括查询字符串。

> **LAB** | **PRACTITIONER** | 未解决  
> [CSRF with broken Referer validation](/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-broken)