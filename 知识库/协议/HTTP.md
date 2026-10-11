[MDN 文档](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)

[hacktricks wiki](https://hacktricks.wiki/en/network-services-pentesting/pentesting-web/special-http-headers.html)

## 常用头部

IP
```
X-Forwarded-For
X-Originating-IP
X-Remote-IP
X-Remote-Addr
X-Client-IP
```

HOST/IP
```
X-Forwarded-Host
X-Host
X-Forwarded-Server
X-HTTP-Host-Override
Forwarded
```

URI
```
X-Forwarded-Uri
X-Original-URI
```

URL
```
X-Original-URL
X-Rewrite-URL
```

## 指南

### HTTP 身份验证

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/Authentication

[RFC 7235](https://datatracker.ietf.org/doc/html/rfc7235) 定义了一个 HTTP 身份验证框架，服务器可以用来质询（challenge）客户端的请求，客户端则可以提供身份验证凭据。

质询与响应的工作流程如下：

1. 服务器端向客户端返回 `401`（Unauthorized，未被授权的）响应状态码，并在 `WWW-Authenticate` 响应标头提供如何进行验证的信息，其中至少包含有一种质询方式。

2. 之后，想要使用服务器对自己身份进行验证的客户端，可以通过包含凭据的 `Authorization` 请求标头进行验证。

3. 通常，客户端会向用户显示密码提示，然后发送包含正确的 `Authorization` 标头的请求。


#### Basic 验证方案

“Basic”HTTP 验证方案是在 [RFC 7617](https://datatracker.ietf.org/doc/html/rfc7617) 中规定的，在该方案中，使用用户的 `ID:密码` 作为凭据信息，并且使用 base64 算法进行编码。

服务器响应头
```http
WWW-Authenticate: Basic realm="Restricted access"
```

客户端请求头
```http
Authorization: Basic d2llbmVyOnBldGVy
```
- 其中，认证头部的 base64 解码后
    ```log
    wiener:peter
    ```

## 参考

### HTTP 标头

#### ⚔️ Max-Forwards

`Max-Forwards` 请求标头被用于限制 [`TRACE`] 方法可经过的服务器（通常指代理服务器）数目。它的值是一个整数，指定可经过的服务器最大数目。服务器在转发 `TRACE` 请求之前，将递减 `Max-Forwards` 的值，直到到达目标服务器，或服务器接收到 `Max-Forwards` 的值为 0 的请求。而后直接返回一个 `200 OK` 的响应（可以包含一些标头）。

如果 `TRACE` 请求中没有 `Max-Forwards` 标头，就可以认为，不限制可经过的服务器最大数目。

```http
Max-Forwards: <integer>
```

#### Link

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Link

HTTP 实体报头 `Link` 提供了序列化 HTTP 头部链接的方法。它在语义上与 HTML 元素 `<link> `相等。


```http
Link: < uri-reference >; param1=value1; param2="value2"
```

- `<uri-reference>`
    URI reference 必须要用 `<` 和 `>` 来关闭。

参数
- `link` 头部包含以 `;` 分隔的参数，这些参数与 HTML 元素 `<link>` 的属性一致。

#### X-Frame-Options 点击劫持防护

用来给浏览器指示允许一个页面可否在 `<frame>`、`<iframe>`、`<embed>` 或者 `<object>` 中展现的标记。


#### Content-Security-Policy (CSP) 内容安全策略

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Content-Security-Policy

导航指令
- `frame-ancestors` 点击劫持防护
    指定可能嵌入页面的有效父项 `<frame>`、`<iframe>`、`<object>` 或 `<embed>`。

    - `frame-ancestors 'none'` 指令的行为类似于 X-Frame-Options 的 `deny` 指令。
    - `frame-ancestors 'self'` 指令大致等同于 X-Frame-Options 的 `sameorigin` 指令。

##### CSP: connect-src

限制通过使用脚本接口加载的 URL。其中受限制的 API 如下：

- `<a>` `ping`
- `fetch()`
- `XMLHttpRequest`
- `WebSocket`
- `EventSource`
- `Navigator.sendBeacon()`

#### Set-Cookie —— 将 cookie 由服务器发送到用户代理

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/Set-Cookie

#### WWW-Authenticate

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Headers/WWW-Authenticate

HTTP `WWW-Authenticate` 响应标头定义了 HTTP 身份验证的方法（“质询”），它用于获取特定资源的访问权限。

指令
- `<auth-scheme>`
    身份验证方案。

- `realm=<realm>` 可选
    描述受保护区域的字符串。
    
### HTTP 请求方法
#### ⚔️ TRACE

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Methods/TRACE

HTTP 方法 `TRACE` 沿着通往目标资源的路径进行信息回环测试。

请求的最终接收者应将收到的信息（不包括可能包括敏感数据的字段）作为 [`200 OK`] 响应的信息主体反映给客户端，其 [`Content-Type`] 为 `message/http`。最终接收者是源服务器或第一个在请求中收到 [`Max-Forwards`] 值为 `0` 的服务器。