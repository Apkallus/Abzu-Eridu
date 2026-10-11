https://httpd.apache.org/docs/2.4/en/mod/

# mod

## mod_md

- 描述
  跨虚拟主机管理域、通过 ACME 协议进行证书签发
- 状态
  实验性
- 模块标识符
  `md_module`
- 源文件
  `mod_md.c`
- 兼容性
  在 2.4.30 及更高版本中可用

### 摘要

本模块为一个或多个虚拟主机管理域的通用属性。它有两个主要用途：其一，通过 ACME 协议（[RFC 8555](https://www.rfc-editor.org/rfc/rfc8555)）监督/续订 TLS 证书。模块会在证书过期之前进行续订，以应对互联网服务中断。有多种方式可以监控所有以这种方式管理的证书的状态，并可通过配置在续订、过期和出错时运行您自己的通知命令。

其二，mod_md 提供了另一种 OCSP Stapling 实现。它既适用于受管证书，也适用于您自行配置的证书。OCSP Stapling 是任何 https: 站点的必要组件，会影响页面加载时间，并且取决于其他设置，还会影响页面可用性。更多内容参见下文 stapling 部分。

用于管理证书的默认 ACME 颁发机构是 [Let's Encrypt](https://letsencrypt.org/)，但也可以配置其他支持该协议的 CA。

简单配置示例：

#### 虚拟主机上下文中的 TLS

```apache
MDomain example.org

<VirtualHost *:443>
    ServerName example.org
    DocumentRoot htdocs/a

    SSLEngine on
    # 未指定证书
</VirtualHost>
```

此设置在服务器启动时会联系 [Let's Encrypt](https://letsencrypt.org/) 为域请求证书。如果 Let's Encrypt 能够验证域的所有权，模块将获取证书及其链，存储在本地文件系统中（参见 `MDStoreDir`），并在下次重启时提供给 `mod_ssl`。

这发生在服务器已经运行期间。所有其他主机将继续照常工作。当证书尚不可用时，对受管域的请求将以 '503 Service Unavailable' 应答。

#### 先决条件

本模块还需要加载 `mod_watchdog`。

使用 Let's Encrypt 进行证书注册和续订，要求您的服务器可从公共互联网通过端口 80 (http:) 和/或端口 443 (https:) 访问。（除非您的服务器配置为使用 DNS 进行质询——更多内容见下文"通配符证书"。）

模块将从 Let's Encrypt 提供的方法中进行选择。通常 LE 在两个端口和 DNS 上都提供质询，Apache 会选择一种可用的方法。

为了确定哪种方法可用，模块会检查 Apache httpd 监听的端口。如果包含端口 80，则假定 http: 质询（名为 http-01）可用。如果服务器监听端口 443，则 https: 质询（名为 tls-alpn-01）也会被加入列表。（如果配置了 `MDChallengeDns01`，质询 dns-01 也会被加入。）

如果您的设置不那么直接，有两种方法可以影响这一点。首先，如果服务器位于端口映射器（如防火墙）之后，请查看 `MDPortMap`。其次，您可以通过直接配置 `MDCAChallenges` 完全覆盖模块的推测。

#### https: 质询

对于通过 TLS 协议进行的域验证，`tls-alpn-01` 是质询类型的名称。它要求 Apache 服务器监听端口 443（如果您将该端口映射到其他端口，请参见 `MDPortMap`）。

Let's Encrypt 将使用特殊指示符 `acme-tls/1` 打开到 Apache 的 TLS 连接（TLS 的这个指示部分称为 ALPN，因此是质询的名称。浏览器也使用 ALPN 来请求 HTTP/2 连接）。

与 HTTP/2 协议一样，要允许这一点，您需要配置：

```apache
Protocols h2 http/1.1 acme-tls/1
```

然后 `tls-alpn-01` 质询类型就可用。

#### 通配符证书

通配符证书是可能的，但开箱即用并不直接。Let's Encrypt 要求对它们使用 `dns-01` 质询验证。其他方式都被认为不够好。

这里的困难在于 Apache 无法自行完成。顾名思义，`dns-01` 要求您为域展示一些包含质询数据的特定 DNS 记录。因此您需要*写入*域的 DNS 记录。

如果您知道如何做，可以将其与 mod_md 集成。假设您在 `/usr/bin/acme-setup-dns` 中有一个脚本，可以这样配置 Apache：

```apache
MDChallengeDns01 /usr/bin/acme-setup-dns
```

当需要为域设置/拆除 DNS 质询记录时，Apache 将调用此脚本。

假设您想要一个 `*.mydomain.com` 的证书，mod_md 将调用：

```bash
/usr/bin/acme-setup-dns setup mydomain.com challenge-data
# 这需要移除 _acme-challenge.mydomain.com 的所有现有 DNS TXT 记录
# 并创建一条内容为 "challenge-data" 的新记录
```

之后它将调用：

```bash
/usr/bin/acme-setup-dns teardown mydomain.com
# 这需要移除 _acme-challenge.mydomain.com 的所有现有 DNS TXT 记录
```

#### 监控

Apache 有一个用于监控的标准模块：`mod_status`。mod_md 贡献了一个部分，使监控您的域变得容易。

您会看到所有 MD 按字母顺序列出、它们包含的域名、整体状态、过期时间和特定设置。设置显示您选择的续订时间（或默认值）、使用的 CA 等。

'Renewal' 列将显示证书续订的活动和错误描述。这应该能让人们更容易地找出是否一切正常或出了什么问题。

如果某个 MD 出错，也会在此处显示。这让您无需翻阅服务器日志即可评估问题。

还有一个新的 '`md-status`' 处理程序可用，以 JSON 格式提供来自 '`server-status`' 的 MD 信息。您可以这样配置：

```apache
<Location "/md-status">
  SetHandler md-status
  Require host example.com
</Location>
```

在您的服务器上。与 '`server-status`' 一样，您**必须**使用授权限制（例如 `mod_authz_host`）保护 `md-status` 输出不被公开查看。

如果您只想检查特定域的 JSON 状态，只需将其附加到您的状态 URL：

```console
> curl https://<yourhost>/md-status/another-domain.org
{
  "name": "another-domain.org",
  "domains": [
    "another-domain.org",
    "www.another-domain.org"
  ],
  ...
```

此 JSON 状态还会在域续订时显示活动日志：

```json
{
"when": "Wed, 19 Jun 2019 14:45:58 GMT",
"type": "progress", "detail": "The certificate for the managed domain has been renewed successfully and can be used. A graceful server restart now is recommended."
},{
"when": "Wed, 19 Jun 2019 14:45:58 GMT",
"type": "progress", "detail": "Retrieving certificate chain for test-901-003-1560955549.org"
},{
"when": "Wed, 19 Jun 2019 14:45:58 GMT",
"type": "progress", "detail": "Waiting for finalized order to become valid"
},{
"when": "Wed, 19 Jun 2019 14:45:50 GMT",
"type": "progress", "detail": "Submitting CSR to CA for test-901-003-1560955549.org"
},
...
```

您还可以在暂存目录以及（启用后的）域目录中的 `job.json` 文件中找到这些信息。这允许您在任何更晚的时间点检查它们。

此外，还有 `MDCertificateStatus`，它以 JSON 格式提供对相关证书信息的访问。

#### Stapling

如果您想先在一个 Managed Domain 中尝试 stapling，请配置：

```apache
<MDomain mydomain.net>
  MDStapling on
</MDomain>
```

并使用 '`server-status`' 和/或 `MDMessageCmd` 来观察其运作方式。您将看到 Stapling 信息是否存在、有效期多长、来自哪里以及何时刷新。

如果这一切都令您满意，您可以将其打开用于所有证书，或仅用于受管证书。

mod_ssl 现有的 stapling 实现已被许多站点使用了多年。mod_ssl 和 mod_md 的实现之间有两个主要区别：

1. 按需 vs. 计划：mod_ssl 在被请求时（例如在新连接上）检索 stapling 信息。mod_md 在服务器启动时以及其生命周期达到 2/3 后立即检索它。
2. 内存 vs. 持久化：mod_ssl *可以*持久化此信息，但大多数示例配置使用内存缓存。mod_md 始终存储在文件系统中。

如果您不巧在 CA 的 OCSP 服务中断期间重启服务器，您的用户可能无法再访问您的站点。没有持久化，您的服务器无法向客户端提供数据，客户端浏览器也无法获取，因为 OCSP 服务没有响应。

mod_md 中的实现会将其持久化，在重启后再次加载，并使其可用于传入连接。在此信息过期前一两天，它会进行续订，从而能够应对较长的 OCSP 服务停机。

出于向后兼容性考虑，mod_ssl 中的现有实现无法大幅更改。例如，mod_ssl 无法在不破坏许多现有安装（这些安装未加载它）的情况下添加对 mod_watchdog 的依赖。


### MDServerStatus 指令

- 描述
  控制是否将受管域信息添加到 `server-status`。
- 语法
  `MDServerStatus on|off`
- 默认
  `MDServerStatus off`
- 上下文
  服务器配置
- 状态
  实验性
- 模块
  mod_md
- 兼容性
  默认值在 2.4.69 中更改为 'off'

如果启用，将向 `mod_status` 的 `server-status` 处理程序输出添加一个部分，其中列出所有受管域及其 DNS 名称、续订状态、生命周期和主要属性。

与 `md-status` 一样，`server-status` 输出**必须**使用适当的授权限制保护，以防止公开查看。

> CTF apache 端点 `/server-status`

## Apache Core Features

### 🎯 TraceEnable 指令 —— 决定服务器对 `TRACE` 请求的处理行为

- 语法
    `TraceEnable [on|off|extended]`

- 默认值
    `TraceEnable on`

- 上下文
    服务器配置、虚拟主机

- 状态
    核心（Core）

- 模块
    core

该指令用于覆盖核心服务器与 [`mod_proxy`] 对 `TRACE` 请求的默认处理行为。默认的 `TraceEnable on` 允许符合 RFC 2616 规范的 `TRACE` 请求，该规范禁止请求携带消息体。若设置为 `TraceEnable off`，核心服务器和 [`mod_proxy`] 将向客户端返回 `405`（Method Not Allowed）错误。

最后，仅出于测试和诊断目的，可以使用非标准兼容的 `TraceEnable extended` 指令来允许请求携带消息体。作为源服务器时，核心模块会将请求体大小限制为 64KB（若使用 `Transfer-Encoding: chunked`，则额外增加 8KB 用于分块头）。核心模块会在响应体中回显完整的请求头及所有分块头。作为代理服务器时，请求体不受 64KB 的限制。

无法使用 `<Limit>` 或 `<LimitExcept>` 来限制 `TRACE` 方法，请改用 `TraceEnable` 指令。

> **注意**
> 尽管存在相反的说法，但在 Apache httpd 中启用 `TRACE` 方法并不会暴露任何安全漏洞。`TRACE` 方法由 HTTP/1.1 规范定义，相关实现理应支持该方法。

> `TRACE` 方法在 CTF 中用来泄露敏感头部