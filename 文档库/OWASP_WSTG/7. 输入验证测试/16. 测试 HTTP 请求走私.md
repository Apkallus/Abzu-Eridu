# 测试 HTTP 请求走私

|ID          |
|------------|
|WSTG-INPV-16|

## 概述

HTTP 请求走私是一类由前端和后端组件解析 HTTP 请求方式不一致所导致的漏洞。当反向代理、负载均衡器或 API 网关等中间件与后端服务器对请求边界的解释存在差异时，攻击者可以注入或“走私”隐藏的请求，这些请求会被无序处理。

现代基础设施通过引入 HTTP/2、协议降级（HTTP/2 → HTTP/1.1）和明文升级（H2C）显著扩大了攻击面，其中请求规范化和转换逻辑经常偏离 RFC 预期。

当两个或多个 HTTP 解析器对请求的起止位置存在分歧时，就会产生请求走私漏洞。历史上，这种差异最常见于对 `Content-Length`（CL）和 `Transfer-Encoding`（TE）头部的冲突解释。

在现代架构中，额外的不同步向量源于：

- HTTP/2 到 HTTP/1.1 的转换层
- 明文 HTTP/2（H2C）升级机制
- 头部规范化不匹配
- 协议降级期间重新引入被禁止的头部
- 跨协议边界的连接复用

这些行为可能导致持久性的不同步、缓存投毒、凭据劫持和访问控制绕过。

## 测试目标

- 识别前端和后端组件之间的请求边界不一致
- 检测经典的 CL/TE 不同步漏洞
- 评估协议转换逻辑（HTTP/2 → HTTP/1.1）
- 评估 H2C 升级处理及降级安全性
- 确认后端请求队列投毒

## 如何测试

### 黑盒测试

#### 测试 CL.TE 不同步

在 CL.TE 场景中，前端使用 `Content-Length` 确定请求大小，而后端遵循 `Transfer-Encoding`。

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
Foo: x
```

预期结果：

- 后端在 `0` 块处停止解析
- 走私的请求保留在缓冲区中
- 后续合法请求被破坏或返回意外响应（例如 404）

#### 测试 TE.CL 不同步

在 TE.CL 场景中，前端正确处理分块编码，但后端依赖 `Content-Length`。

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 4
Transfer-Encoding: chunked

5c
GET /admin HTTP/1.1
Content-Length: 0

0
```

预期结果：

- 后端提前停止
- 剩余负载被解释为新请求
- 可能发生未授权端点访问或请求投毒

#### 测试 TE.TE（混淆的 Transfer-Encoding）

如果两台服务器都支持 `Transfer-Encoding`，头部混淆可能导致其中一个解析器忽略它。

常见技术包括：

- 空白字符操纵
- 头部重复
- 非标准分隔符

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 44
Transfer-Encoding:\tchunked
Transfer-Encoding: identity

0

GET /404 HTTP/1.1
Foo: bar
```

### 现代攻击向量

#### HTTP/2 到 HTTP/1.1 的不同步

在许多部署中，客户端使用 HTTP/2 与边缘服务器通信，而后端服务仍通过 HTTP/1.1 运行。在协议转换期间，中间件必须从 HTTP/2 帧重建 HTTP/1.1 请求。

常见的故障点包括：

- 不正确重建 `Content-Length`
- 重新引入逐跳头部
- 多个逻辑请求被折叠为单个后端请求

> 注意：HTTP/2 降级本身并不固有漏洞。
> 当协议转换重建的 HTTP/1.1 请求违反后端解析假设时，利用成为可能，从而导致请求边界不同步。

测试方法：

- 发送多个具有冲突长度语义的 HTTP/2 DATA 帧
- 通过时间差异或响应拆分观察后端行为
- 监视请求队列投毒

##### 示例：通过请求重建的 HTTP/2 降级走私

在此场景中，客户端通过 HTTP/2 与前端通信，而后端仅支持 HTTP/1.1。中间件从多个 HTTP/2 DATA 帧重建 HTTP/1.1 请求。

**HTTP/2（概念表示）：**

- DATA 帧 1：

```http
0\r\n\r\n
```

- DATA 帧 2：

```http
GET /admin HTTP/1.1
Host: internal
```

**重建的 HTTP/1.1 请求（后端视角）：**

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 0

GET /admin HTTP/1.1
Host: internal
```

如果前端将请求视为已完成，而后端继续解析缓冲数据，则第二个请求可能被无序处理，导致请求走私。

> 隐式降级：
> 即使没有显式的 `Upgrade: h2c` 机制，许多 CDN 和反向代理在将请求转发到后端服务时，也会静默地将 HTTP/2 客户端连接降级为 HTTP/1.1。
> 这些隐式降级扩大了走私攻击面，特别是当与连接复用和请求规范化不足结合时。

#### H2C 走私（明文 HTTP/2 升级）

H2C 允许使用 `Upgrade: h2c` 机制将 HTTP/1.1 连接升级到 HTTP/2。
与协议降级不同，H2C 走私发生在就地协议转换期间，此时前端和后端组件可能暂时对同一连接的活跃解析状态存在分歧，可能在后端缓冲区中留下残留字节。

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
HTTP2-Settings: AAMAAABkAARAAAAAAAIAAAAA

0

GET /admin HTTP/1.1
Host: internal
```

风险因素：

- 部分升级接受
- 后端继续按 HTTP/1.1 解析
- 升级后处理走私请求

#### 通过协议降级的请求队列投毒

某些代理将 HTTP/2 请求降级为 HTTP/1.1，但未能完全清理：

- `Content-Length`
- 重复头部
- 无效的伪头部顺序

攻击者可以利用这一点投毒持久后端连接，影响多个用户。

### 漏洞指标

- 相同请求的响应不一致
- 意外的 404 或 400 响应
- 延迟或不匹配的响应
- 跨用户响应泄露

## 修复

- 强制执行严格的 RFC 合规解析
- 规范化所有中间件的请求处理
- 在不需要时禁用 H2C
- 避免在不受信任的连接上进行协议降级
- 在解析错误时终止并重新验证后端连接

## 工具

- [HTTP Request Smuggler（Burp Suite 扩展）](https://portswigger.net/bappstore/aaaa60ef945341e8a450217a54a11646)
- [Smuggler（Python），作者 defparam](https://github.com/defparam/smuggler)
- [h2csmuggler，作者 Bishop Fox](https://github.com/BishopFox/h2csmuggler)

## 参考资料

- [James Kettle，“HTTP 不同步攻击：请求走私重生”（PortSwigger 研究）](https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn)
- [James Kettle，“HTTP/2：续集总是更糟”（PortSwigger 研究）](https://portswigger.net/research/http2)
- [Jake Miller，“h2c 走私：通过 HTTP/2 明文的请求走私”（Bishop Fox）](https://bishopfox.com/blog/h2c-smuggling-request)
- [Amit Klein, Chaim Linhart, Ronen Heled, Steve Orrin：“HTTP 请求走私”（2005）](https://web.archive.org/web/20210816212852/https://www.cgisecurity.com/lib/http-request-smuggling.pdf)
- [RFC 7230，第 3.3.3 节：消息体长度](https://datatracker.ietf.org/doc/html/rfc7230#section-3.3.3)
- [RFC 7540：超文本传输协议版本 2（HTTP/2）](https://datatracker.ietf.org/doc/html/rfc7540)
