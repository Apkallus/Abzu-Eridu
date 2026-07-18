
## 2.11 子域名接管

子域名接管漏洞发生在子域名指向已移除或不再活跃的服务（如 Web 主机或云服务）时。这可能是由于各种原因，例如外部服务已停用但 DNS 记录未更新或删除，或者组织忘记续订特定服务的订阅，导致子域名指向非活动服务。这些子域名有时可以在相应服务上声明或注册。

为了说明，让我们以 `redseclabs.com` 为例。在枚举过程中，我们发现子域 `redseclabsssto.redseclabs.com`。该域返回 “404 Not Found” 错误，并提示指定的存储桶不存在。

为进一步调查，我们将使用 “dig” 命令来了解此子域的 DNS 配置。

**命令**
```bash
dig redseclabsto.redseclabs.com
```

命令输出表明规范名称（CNAME）指向一个 S3 存储桶记录，`redseclabsssto.redseclabs.com.s3.us-west-2.amazonaws.com`，托管在 Amazon Web Services（AWS）上。由于存储桶不存在，可以尝试使用 AWS 控制台注册同名的新存储桶并夺取控制权。

### 2.11.1 使用 Subjack 自动化子域名接管

Subjack （[https://github.com/haccer/subjack](https://github.com/haccer/subjack)） 是一个自动化子域名接管工具，可以扫描子域名列表并并发指出那些易受劫持的子域名。然而，它可能产生误报，因此手动验证其发现的准确性很重要。

以下命令以子域名列表作为输入，并返回可能易受子域名劫持的子域结果。

**命令**
```bash
subjack -w subdomains.txt -t 100 -timeout 30 -o results.txt
```