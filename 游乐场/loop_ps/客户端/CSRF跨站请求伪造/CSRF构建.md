## 如何构建 CSRF 攻击
实验：无防御的 CSRF 漏洞
https://portswigger.net/web-security/csrf/lab-no-defenses

登录的响应为
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=9I4afsu4lMGC3sgHCQa7kmFLgV6uzsU5; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 0

此处对会话cookie关闭了SameSite的防护

修改邮件的功能仅使用会话cookie验证
POST /my-account/change-email HTTP/2

对修改邮件post使用burp概念验证功能，生成html表单
