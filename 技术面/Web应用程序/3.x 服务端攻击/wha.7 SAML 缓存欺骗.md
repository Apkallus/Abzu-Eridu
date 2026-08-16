



















## 7.12 攻击 SAML

SAML 是一种基于 XML 的标准，用于在不同实体之间提供身份验证和授权。在 SAML 上下文中，这些实体称为身份提供者（IdP）和服务提供者（SP）。SAML 通过一组凭据简化用户对多个服务的访问，此功能称为单点登录（SSO）。

### SAML 关键组件

- **用户代理（User Agent）**：通常指用户的 Web 浏览器。
- **身份提供者（Identity Provider，IdP）**：IdP 充当负责认证用户的中央权威机构，安全存储和管理用户凭据及相关认证信息。
- **服务提供者（Service Provider，SP）**：SP 指用户想要访问的应用程序或服务。
- **SAML 断言（SAML Assertion）**：SAML 的关键元素，这是一个包含必要用户信息、时间戳和认证上下文的 XML 文档。它由 IdP 数字签名以确保完整性和真实性。

在实践中，配置 SAML 时，SP 和 IdP 之间建立信任关系。这意味着用户必须先通过 IdP 认证，然后才能访问 SP 提供的服务。一旦用户被 IdP 认证，它会生成 SAML 断言，发送给应用程序。由于 SP 信任 IdP，它允许用户访问应用程序，无需再次登录。这种便利性称为单点登录（SSO），用户在 IdP 初次认证后可无缝访问各种应用程序。

### 7.12.1 SAML 工作流程

下图（图 7.50）概述了 SSO 过程的工作流程，涉及 SP、用户代理和 IdP。

**图 7.49 SAML 工作流程（来源：www.miniorange.com/images/sso-protocol/saml-sso.png）**

了解了关键概念，让我们看看在现实测试中可能遇到的一些值得注意的 SAML 攻击。

### 7.12.2 SAML 场景 1：响应篡改

在图 7.50 所示的工作流程中，当攻击者试图篡改发送给 SP 的 SAML 响应（步骤 5）时，可能出现潜在漏洞。这意味着断言的值（可能包含用户名、角色等详细信息）可以被篡改并发送回服务提供者。如果服务提供者未验证来自 IdP 的 SAML 断言，它可能基于篡改的断言授予访问权限，导致权限提升和其他意外后果。

**图 7.50 演示工作流程中的缺陷**

让我们使用“VulnerableSAMLApp”[https://github.com/yogisec/VulnerableSAMLApp] 来复现此行为。该应用程序专为演示 SAML 漏洞而构建。为重现此问题，我们将按以下顺序操作：

**步骤 1**：以用户“yogi”身份登录。该用户属于 `users` 组。

**图 7.51 用户“Yogi”已登录，属于 users 组**

**步骤 2**：接下来，我们将使用 BurpSuite 中的扩展 SAMLRaider 拦截 SAML 响应。

**SAML 响应（部分）**
```xml
<saml:AuthnStatement AuthnInstant="2023-10-27T20:10:55Z" SessionNotOnOrAfter="2023-10-28T04:10:55Z" SessionIndex="_638cb38901eb86f5304170d06aaf73e0e59a6c345f">
    <saml:AuthnContext><saml:AuthnContextClassRef>urn:oasis:names:tc:SAML:2.0:ac:classes:Password</saml:AuthnContextClassRef></saml:AuthnContext>
</saml:AuthnStatement>
<saml:AttributeStatement>
    <saml:Attribute Name="memberOf" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:uri">
        <saml:AttributeValue xsi:type="xs:string">users</saml:AttributeValue>
    </saml:Attribute>
    <!-- 其他属性 -->
</saml:AttributeStatement>
```

**图 7.52 拦截 SAML 响应**

**步骤 3**：接下来，为提升权限，我们将用户组更改为 `administrators` 并提交请求给 SP。

**图 7.53 篡改 SAML 响应**

由于 SP 忽略验证 SAML 断言是否由 IdP 签名，它将执行请求，导致“yogi”被授予 `administrators` 组成员资格。

**图 7.54 篡改 SAML 断言导致权限提升**

### 7.12.3 SAML 场景 2：签名排除攻击

考虑 SP 主动验证 SAML 断言并确保其由 IdP 数字签名的场景。在这种情况下，对 SAML 响应的任何更改都将导致拒绝。例如，如果我们修改用户组，消息将因与签名不一致而被拒绝。

然而，如果 SP 仅在签名时验证断言的有效性，则可能出现潜在漏洞。换言之，应用程序不严格要求所有事务都使用签名消息。这意味着如果 SAML 响应中缺少签名元素，签名验证步骤可能会被完全绕过。此漏洞称为“签名排除攻击”。

为重现此漏洞，只需在 SAMLRaider 中拦截 SAML 响应，并点击“Remove Signatures”。这样，所有签名元素将被移除，结果用户将作为管理员被认证。

**图 7.55 尝试篡改 SAML 响应时返回的错误**

**图 7.56 从 SAML 响应中删除消息签名**

## 7.13 攻击多因素认证

## 7.14 Web 缓存欺骗

Web 服务器通常使用 URL 模式或正则表达式来决定应缓存哪些页面。因此，它们可能难以区分表现出不同行为但共享相同根路径的 URL。同时，负载均衡器和 Web 应用防火墙（WAF）有时会缓存不应缓存的内容。这种结合可能为攻击者提供欺骗 Web 服务器缓存敏感数据的机会。后续访问者可能无意中访问此缓存数据。由于此类攻击源自客户端，因此需要用户交互才能执行。

为了说明，考虑一个银行应用程序，其中 `tmgm` 代表攻击者账户，`admin` 是潜在受害者账户。

**步骤 1**：攻击者使用 `tmgm` 账户登录银行仪表板。

**图 7.60 攻击者以 `tmgm` 用户身份登录**

**步骤 2**：攻击者构造以下 URL，附加一个不存在的 `random.css` 文件，然后将此恶意链接发送给受害者。

**有效载荷**
```
http://tmgm-portal.local:5000/dashboard/random.css
```

**步骤 3**：受害者以 `admin` 身份登录，点击收到的链接。由于 `random.css` 文件不存在，Web 服务器显示仪表板页面。结果，该页面的内容被缓存在 `random.css` URL 下。

**步骤 4**：随后，当攻击者访问先前构造的 URL `http://tmgm-portal.local:5000/dashboard/random.css` 时，显示缓存的 admin 仪表板页面。

**图 7.61 受害者以 `admin` 用户身份登录并点击恶意链接**

**图 7.62 攻击者通过引用 `random.css` URL 检索 admin 仪表板**

## 7.15 额外进阶

- **Sentry MBA CAPTCHA 绕过**：探索 Sentry MBA 内置的 OCR 功能。研究它如何利用先进技术通过图像处理方法解码和绕过 CAPTCHA。
- **人工 CAPTCHA 解决 API**：研究旨在雇用人类解决 CAPTCHA 的 API。选择并使用此类 API 来评估其在解决各种 CAPTCHA 类型时的有效性。
- **二阶 IDOR**：深入研究二阶 IDOR，检查其机制及相关风险。
- **批量赋值漏洞**：研究批量赋值漏洞背后的原理。分析其与 Web 参数篡改的关系，并确定是否可以归为一类还是应单独处理。
- **OAuth2 redirect_uri 绕过**：研究绕过 redirect_uri 和白名单的各种方法。
