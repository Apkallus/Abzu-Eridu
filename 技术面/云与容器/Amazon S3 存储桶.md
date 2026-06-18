
S3 代表简单存储服务，是亚马逊的在线存储产品。

如果 S3 存储桶配置不正确，可能会向攻击者泄露信息。S3 存储桶可能包含隐藏的端点、日志、凭证、用户信息、源代码和其他可能对你有用的信息。

大多数存储桶使用 URL 格式 `BUCKET.s3.amazonaws.com` 或 `s3.amazonaws.com/BUCKET`，因此以下搜索词很可能找到结果：

```
site:s3.amazonaws.com COMPANY_NAME
site:amazonaws.com COMPANY_NAME
```

如果公司为其 S3 存储桶使用自定义 URL，则尝试更灵活的搜索词。公司通常仍会在其自定义存储桶 URL 中放置像 `aws` 和 `s3` 这样的关键词，因此尝试这些搜索：

```
amazonaws s3 COMPANY_NAME
amazonaws bucket COMPANY_NAME
amazonaws COMPANY_NAME
s3 COMPANY_NAME
```


另一种找到存储桶的方法是搜索公司的公共 GitHub 仓库中的 S3 URL。尝试在这些仓库中搜索 `s3` 一词


工具：
- [S3Scanner](https://github.com/sa7mon/S3Scanner)
- [GrayhatWarfare](https://buckets.grayhatwarfare.com/) 在线搜索引擎
- [Lazys3](https://github.com/nahamsec/lazys3/) 爆破
- [Bucket Stream](https://github.com/eth0izzle/bucket-stream/) 解析属于组织的证书，并根据证书上找到的域名排列来查找 S3 存储桶。Bucket Stream 还会自动检查存储桶是否可访问

靶机：
Scott Piper 创建的 http://flaws.cloud 站点。这个故意易受攻击的站点及其姊妹站点 http://flaws2.cloud 是练习云渗透测试技能的绝佳资源。


一旦你找到几个属于目标组织的存储桶，使用 AWS 命令行工具查看你是否可以访问一个。使用以下命令安装该工具：

```bash
pip install awscli
```

然后按照 Amazon 的文档 <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html> 配置它以与 AWS 一起工作。

现在你应该能够直接从终端通过 `aws s3` 命令访问存储桶。尝试列出你找到的存储桶的内容：

```bash
aws s3 ls s3://BUCKET_NAME/
```

如果有效，看看你是否可以通过将文件复制到本地机器来读取任何有趣文件的内容：

```bash
aws s3 cp s3://BUCKET_NAME/FILE_NAME /path/to/local/directory
```

收集通过存储桶泄露的任何有用信息，并将其用于未来的利用。可能泄露诸如活动 API 密钥或个人信息等信息。仅暴露的 S3 存储桶本身就常被视为一个漏洞。还可尝试将自己的测试文件上传到存储桶或从存储桶中删除此测试文件。例如，此命令将把本地名为 `TEST_FILE` 的文件复制到目标的 S3 存储桶中：

```bash
aws s3 cp TEST_FILE s3://BUCKET_NAME/
```

此命令将删除你刚刚上传的 `TEST_FILE`：

```bash
aws s3 rm s3://BUCKET_NAME/TEST_FILE
```

这些命令是在不实际篡改目标公司文件的情况下证明你对存储桶具有写访问权限的无害方式。始终上传和删除你自己的测试文件。