https://github.com/expressjs/cookie-session/

# cookie-session

简单基于 cookie 的会话中间件。

用户会话可以通过 cookie 以两种主要方式存储：在服务器端或客户端。本模块将会话数据存储在客户端的 cookie 中，而像 [express-session](https://www.npmjs.com/package/express-session) 这样的模块仅在客户端的 cookie 中存储会话标识符，并将会话数据存储在服务器端，通常是在数据库中。

以下几点可以帮助你选择使用哪种：

- `cookie-session` 不需要服务器端的任何数据库/资源，但总会话数据不能超过浏览器的最大 cookie 大小。
- `cookie-session` 可以简化某些负载均衡场景。
- `cookie-session` 可用于存储“轻量”会话，并包含一个标识符，用于查找数据库支持的二级存储，以减少数据库查询。

**注意** 本模块不会加密 cookie 中的会话内容，仅提供签名以防止篡改。客户端可以通过检查 cookie 的值来读取会话数据。不应在 `req.session` 中设置秘密数据而不加密，或改用服务器端会话。

**注意** 本模块不会阻止会话重放，因为设置的过期时间仅是 cookie 的过期时间；如果这是你的应用关注的问题，你可以在 `req.session` 对象中存储过期日期并在服务器端验证，并根据应用需要实现任何其他逻辑来延长会话。

## 安装

这是一个通过 [npm registry](https://www.npmjs.com/) 提供的 [Node.js](https://nodejs.org/en/) 模块。使用 [`npm install` 命令](https://docs.npmjs.com/getting-started/installing-npm-packages-locally) 进行安装：

```sh
$ npm install cookie-session
```

## API

```js
var cookieSession = require('cookie-session')
var express = require('express')

var app = express()

app.use(cookieSession({
  name: 'session',
  keys: [/* secret keys */],

  // Cookie 选项
  maxAge: 24 * 60 * 60 * 1000 // 24 小时
}))
```

### cookieSession(options)

使用提供的选项创建一个新的 cookie 会话中间件。该中间件会将 `session` 属性附加到 `req`，该属性提供一个表示已加载会话的对象。如果在请求中没有提供有效会话，则这是一个新会话，或者是从请求中加载的会话。

如果 `req.session` 的内容被修改，中间件会自动向响应添加 `Set-Cookie` 头。_注意_，除非会话中有内容，否则响应中不会有 `Set-Cookie` 头（因此不会为特定用户创建会话），所以一旦你有要存储的标识信息，请务必向 `req.session` 添加一些内容。

#### 选项

Cookie 会话接受选项对象中的以下属性。

##### name

要设置的 cookie 的名称，默认为 `session`。

##### keys

用于签名和验证 cookie 值的密钥列表，或一个配置好的 [`Keygrip`](https://www.npmjs.com/package/keygrip) 实例。设置的 cookie 始终使用 `keys[0]` 签名，而其他密钥可用于验证，从而允许密钥轮换。如果提供了 `Keygrip` 实例，它可以用于更改签名参数，如签名算法。

##### secret

如果未提供 `keys`，将用作单个密钥的字符串。

##### Cookie 选项

其他选项传递给 `cookies.get()` 和 `cookies.set()`，允许你控制安全性、域、路径和签名等设置。

这些选项还可以包含以下任何一项（完整列表请参见 [cookies 模块文档](https://www.npmjs.org/package/cookies#readme)）：

- `maxAge`：一个数字，表示从 `Date.now()` 到过期时间的毫秒数
- `expires`：一个 `Date` 对象，指示 cookie 的过期日期（默认在会话结束时过期）。
- `path`：一个字符串，指示 cookie 的路径（默认为 `/`）。
- `domain`：一个字符串，指示 cookie 的域（无默认值）。
- `partitioned`：一个布尔值，指示是否在 Chrome 中为 [CHIPS 更新](https://developers.google.com/privacy-sandbox/3pcd/chips) 对 cookie 进行分区（默认为 `false`）。如果为 true，来自嵌入站点的 Cookie 将被分区，并且只能从创建它的同一顶级站点读取。
- `priority`：一个字符串，指示 cookie 优先级。可以设置为 `'low'`、`'medium'` 或 `'high'`。
- `sameSite`：一个布尔值或字符串，指示 cookie 是否为“同站点”cookie（默认为 `false`）。可以设置为 `'strict'`、`'lax'`、`'none'` 或 `true`（映射为 `'strict'`）。
- `secure`：一个布尔值，指示 cookie 是否仅通过 HTTPS 发送（HTTP 默认为 `false`，HTTPS 默认为 `true`）。如果将其设置为 `true` 且 Node.js 不直接通过 TLS 连接，请务必阅读如何[在代理后设置 Express](https://expressjs.com/en/guide/behind-proxies/)，否则 cookie 可能永远无法正确设置。
- `httpOnly`：一个布尔值，指示 cookie 是否仅通过 HTTP(S) 发送，而不提供给客户端 JavaScript（默认为 `true`）。
- `signed`：一个布尔值，指示是否对 cookie 进行签名（默认为 `true`）。
- `overwrite`：一个布尔值，指示是否覆盖先前设置的具有相同名称的 cookie（默认为 `true`）。

### req.session

表示给定请求的会话。

#### .isChanged

如果会话在请求期间已被更改，则为 `true`。

#### .isNew

如果会话是新的，则为 `true`。

#### .isPopulated

确定会话是否已填充数据或为空。

### req.sessionOptions

表示当前请求的会话选项。这些选项是中间件构造时提供的选项的浅克隆，可以修改以基于每个请求更改 cookie 设置行为。

### 销毁会话

要销毁会话，只需将其设置为 `null`：

```js
req.session = null
```

### 保存会话

由于会话的全部内容都保存在客户端 cookie 中，因此会话是通过在 `Set-Cookie` 响应头中写出 cookie 来“保存”的。当 Node.js 响应头写入客户端时，如果会话发生了更改且会话未被销毁，则会自动完成此操作。

## 示例

### 简单的查看计数器示例

```js
var cookieSession = require('cookie-session')
var express = require('express')

var app = express()

app.set('trust proxy', 1) // 信任第一个代理

app.use(cookieSession({
  name: 'session',
  keys: ['key1', 'key2']
}))

app.get('/', function (req, res, next) {
  // 更新查看次数
  req.session.views = (req.session.views || 0) + 1

  // 写入响应
  res.end(req.session.views + ' views')
})

app.listen(3000)
```

### 每用户粘性最大年龄

```js
var cookieSession = require('cookie-session')
var express = require('express')

var app = express()

app.set('trust proxy', 1) // 信任第一个代理

app.use(cookieSession({
  name: 'session',
  keys: ['key1', 'key2']
}))

// 这允许你设置 req.session.maxAge，让某些会话
// 具有与默认值不同的值。
app.use(function (req, res, next) {
  req.sessionOptions.maxAge = req.session.maxAge || req.sessionOptions.maxAge
  next()
})

// ... 你的逻辑在这里 ...
```

### 延长会话过期时间

如果会话内容没有更改，本模块不会发送 `Set-Cookie` 头。这意味着，为了在用户浏览器中延长会话的过期时间（例如响应用户活动），需要对会话进行某种修改。

```js
var cookieSession = require('cookie-session')
var express = require('express')

var app = express()

app.use(cookieSession({
  name: 'session',
  keys: ['key1', 'key2']
}))

// 更新 cookie 中的值，以便发送 set-cookie。
// 仅每分钟更改一次，以免每个请求都发送。
app.use(function (req, res, next) {
  req.session.nowInMinutes = Math.floor(Date.now() / 60e3)
  next()
})

// ... 你的逻辑在这里 ...
```

### 使用自定义签名算法

此示例展示如何创建一个自定义 `Keygrip` 实例作为 `keys` 选项，以提供密钥和额外的签名配置。

```js
var cookieSession = require('cookie-session')
var express = require('express')
var Keygrip = require('keygrip')

var app = express()

app.use(cookieSession({
  name: 'session',
  keys: new Keygrip(['key1', 'key2'], 'SHA384', 'base64')
}))

// ... 你的逻辑在这里 ...
```

## 使用限制

### 最大 Cookie 大小

由于整个会话对象都被编码并存储在 cookie 中，因此可能会超过不同浏览器上的最大 cookie 大小限制。[RFC6265 规范](https://tools.ietf.org/html/rfc6265#section-6.1) 建议浏览器 **应该** 允许

> 每个 cookie 至少 4096 字节（按 cookie 名称、值和属性的长度之和计算）

实际上，这个限制在不同浏览器中略有不同。请参阅[浏览器限制列表](http://browsercookielimits.iain.guru)。根据经验法则，**每个域不要超过 4093 字节**。

如果你的会话对象在编码后大到超过浏览器限制，在大多数情况下浏览器将拒绝存储该 cookie。这将导致来自浏览器的后续请求要么 a) 没有任何会话信息，要么 b) 使用足够小、未超过 cookie 限制的旧会话信息。

如果你发现会话对象达到了这些限制，最好考虑是否应该从服务器上的数据库加载会话中的数据，而不是在每个请求中与浏览器之间传输。或者转向[替代会话策略](https://github.com/expressjs/session#compatible-session-stores)。