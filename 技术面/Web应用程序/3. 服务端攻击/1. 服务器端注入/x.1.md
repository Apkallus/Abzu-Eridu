
## 如何防止 OS 命令注入攻击

防止 OS 命令注入漏洞最有效的方法是永远不要从应用程序层代码调用 OS 命令。在几乎所有情况下，都可以使用更安全的平台 API 以不同方式实现所需功能。

如果必须使用用户提供的输入调用 OS 命令，则必须执行严格的输入验证。一些有效验证的示例包括：

- 针对允许值的白名单进行验证。
- 验证输入是否为数字。
- 验证输入仅包含字母数字字符，不包含其他语法或空格。

永远不要尝试通过转义 Shell 元字符来清理输入。在实践中，这太容易出错，并且容易被熟练的攻击者绕过。

> #### 阅读更多
>
> - [使用 Burp Suite 的 Web 漏洞扫描器查找 OS 命令注入漏洞](/burp/vulnerability-scanner)
> - [阅读 PortSwigger Research 关于 44Con 和 BSides Manchester 上《狩猎异步漏洞》演讲的总结](https://portswigger.net/research/hunting-asynchronous-vulnerabilities)