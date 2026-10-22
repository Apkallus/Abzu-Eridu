[expressjs 官网](https://expressjs.com/en/5x/api/)

[github](https://github.com/expressjs/expressjs.com/tree/main/src/content/api)

## api

```js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('hello world');
});

app.listen(3000);
```

### Express

https://expressjs.com/en/5x/api/express/

创建一个 Express 应用。`express()` 函数是由 `express` 模块导出的顶层函数。

```js
const express = require('express');
const app = express();
```

Express 对象具有以下方法，可用于创建中间件函数、路由器，并提供一些内置中间件：
...

---

#### 方法

##### express.static()

Arguments
- root Type:String
  The root directory from which to serve static assets.

### Application Object

https://expressjs.com/en/5x/api/application

`app` 对象通常表示 Express 应用程序。通过调用 Express 模块导出的顶层 `express()` 函数来创建它：

```js
var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('hello world');
});

app.listen(3000);
```

`app` 对象具有用于以下用途的方法：

- 路由 HTTP 请求；例如，参见 [app.METHOD] 和 [app.param]。
- 配置中间件；参见 [app.route]。
- 渲染 HTML 视图；参见 [app.render]。
- 注册模板引擎；参见 [app.engine]。

它还具有影响应用程序行为的设置（属性）；有关更多信息，请参见 [应用程序设置]。

> **注意**
>
> Express 应用程序对象可以分别通过[请求对象](https://expressjs.com/en/5x/api/request/)和[响应对象](https://expressjs.com/en/5x/api/response/)的 `req.app` 和 `res.app` 来引用。

#### 方法

##### app.all()

**参数**

- `path`
  类型：`String | RegExp | Array`
  调用中间件函数的路径；可以是以下任意一种：表示路径的字符串、路径模式、用于匹配路径的正则表达式模式，或上述任意组合的数组。有关示例，请参见 [路径示例]。

- `callback`
  类型：`Function | Function[]`
  回调函数；可以是：一个中间件函数、一系列中间件函数（用逗号分隔）、一个中间件函数数组，或上述所有内容的组合。你可以提供多个行为与中间件完全相同的回调函数，不同之处在于这些回调可以调用 `next('route')` 以跳过剩余的路径回调。你可以使用此机制对路由施加前置条件，然后如果没有理由继续当前路由，则将控制权传递给后续路由。由于 [router](https://expressjs.com/en/5x/api/router/) 和 [app](https://expressjs.com/en/5x/api/application/) 实现了中间件接口，你可以像使用任何其他中间件函数一样使用它们。有关示例，请参见 [中间件回调函数示例]。

此方法类似于标准的 [app.METHOD()] 方法，但它匹配所有 HTTP 动词。

**示例**

对于 `/secret` 的请求，无论使用 GET、POST、PUT、DELETE 还是任何其他 HTTP 请求方法，都会执行以下回调：

**JavaScript**

```js
app.all('/secret', (req, res, next) => {
  console.log('Accessing the secret section ...');
  next(); // pass control to the next handler
});
```

`app.all()` 方法对于为特定路径前缀或任意匹配映射“全局”逻辑很有用。例如，如果你将以下内容放在所有其他路由定义的最前面，它要求从该点开始的所有路由都需要身份验证，并自动加载用户。请记住，这些回调不必充当端点：`loadUser` 可以执行一项任务，然后调用 `next()` 以继续匹配后续路由。

##### app.listen()

**参数**

- `port`
  类型：`Number | undefined`
  要监听的 TCP 端口。如果省略或为 `0`，操作系统将分配一个任意未使用的端口。

- `host`
  类型：`String | undefined`
  接受连接的主机。

- `backlog`
  类型：`Number | undefined`
  待处理连接队列的最大长度。

- `path`
  类型：`String | undefined`
  要监听的 UNIX 套接字路径，作为主机和端口的替代方案。

- `callback`
  类型：`Function | undefined`
  服务器开始监听后调用的函数。如果服务器发出 `error` 事件（例如 `EADDRINUSE`），错误将作为参数传递给此回调。

**返回值：** `http.Server`

在指定的主机和端口上绑定并监听连接，或启动 UNIX 套接字并在给定路径上监听连接。此方法与 Node 的 [http.Server.listen()](https://nodejs.org/api/http.html#serverlisten) 相同。

如果省略 port 或为 0，操作系统将分配一个任意未使用的端口，这对于自动化任务（测试等）等情况很有用。

**CommonJS**

```js
const express = require('express');
const app = express();

app.listen(3000); // bind and listen on a TCP port
app.listen('/tmp/sock'); // or listen on a UNIX socket
```

> **注意**
>
> 当服务器发出 `error` 事件（如 `EADDRINUSE`）时，错误会传递给提供的 `callback`。在回调内部处理它：

```js
const server = app.listen(8080, '0.0.0.0', (error) => {
  if (error) {
    throw error; // e.g. EADDRINUSE
  }
  console.log(`Listening on ${JSON.stringify(server.address())}`);
});
```

`express()` 返回的 `app` 实际上是一个 JavaScript `Function`，设计用于作为回调传递给 Node 的 HTTP 服务器以处理请求。这使得可以轻松地用同一代码库提供应用的 HTTP 和 HTTPS 版本，因为 app 并不继承自这些（它只是一个回调）：

**CommonJS**

```js
const express = require('express');
const https = require('https');
const http = require('http');
const app = express();

http.createServer(app).listen(80);
https.createServer(options, app).listen(443);
```

`app.listen()` 方法返回一个 [http.Server](https://nodejs.org/api/http.html#class-httpserver) 对象，并且（对于 HTTP）是以下内容的便捷方法：

```js
app.listen = function () {
  const server = http.createServer(this);
  return server.listen.apply(server, arguments);
};
```

> **注意**
>
> Node 的 [http.Server.listen()](https://nodejs.org/api/http.html#serverlisten) 方法的所有形式实际上都受支持。

##### app.use()

**参数**

- `path`
  类型：`String | RegExp | Array | undefined`
  调用中间件函数的路径；可以是以下任意一种：表示路径的字符串、路径模式、用于匹配路径的正则表达式模式，或上述任意组合的数组。有关示例，请参见 [路径示例]。

- `callback`
  类型：`Function | Function[]`
  回调函数；可以是：一个中间件函数、一系列中间件函数（用逗号分隔）、一个中间件函数数组，或上述所有内容的组合。你可以提供多个行为与中间件完全相同的回调函数，不同之处在于这些回调可以调用 `next('route')` 以跳过剩余的路径回调。你可以使用此机制对路由施加前置条件，然后如果没有理由继续当前路由，则将控制权传递给后续路由。由于 [router](https://expressjs.com/en/5x/api/router/) 和 [app](https://expressjs.com/en/5x/api/application/) 实现了中间件接口，你可以像使用任何其他中间件函数一样使用它们。有关示例，请参见 [中间件回调函数示例]。

将指定的[中间件](https://expressjs.com/en/5x/guide/using-middleware/)函数挂载到指定路径：当请求路径的基础部分匹配 `path` 时，该中间件函数会被执行。

**描述**

路由将匹配其路径后紧跟“`/`”的任何路径。例如：`app.use('/apple', ...)` 将匹配“/apple”、“/apple/images”、“/apple/images/news”等。

由于 `path` 默认为“/”，未挂载路径的中间件将对应用的每个请求执行。例如，以下中间件函数将对应用的*每个*请求执行：

**JavaScript**

```js
app.use((req, res, next) => {
  console.log('Time: %d', Date.now());
  next();
});
```

> **注意**
>
> 子应用将：
>
> - 不继承具有默认值的设置的值。你必须在子应用中设置该值。
> - 继承没有默认值的设置的值。
>
> 有关详细信息，请参见 [应用程序设置]。

中间件函数按顺序执行，因此中间件的包含顺序很重要。

**JavaScript**

```js
// this middleware will not allow the request to go beyond it
app.use((req, res, next) => {
  res.send('Hello World');
});

// requests will never reach this route
app.get('/', (req, res) => {
  res.send('Welcome');
});
```

**错误处理中间件**

错误处理中间件始终接受*四个*参数。你必须提供四个参数才能将其标识为错误处理中间件函数。即使你不需要使用 `next` 对象，也必须指定它以保持签名。否则，`next` 对象将被解释为常规中间件，并且无法处理错误。有关错误处理中间件的详细信息，请参见：[错误处理](https://expressjs.com/en/5x/guide/error-handling/)。

以与其他中间件函数相同的方式定义错误处理中间件函数，不同之处在于使用四个参数而不是三个，具体签名为 `(err, req, res, next)`：

**JavaScript**

```js
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});
```

### response

[expressjs 官网](https://expressjs.com/en/5x/api/response/)

#### Methods

##### res.set()

**签名** 返回 `Response`

- `field`（`String | Object`）：头名称，或用于一次设置多个头的头名称/值对对象。
- `value`（`String | String[]`，可选）：头值（当 `field` 为字符串时）。

将响应的 HTTP 头 `field` 设置为 `value`。要一次设置多个字段，请传入一个对象作为参数。

```js
res.set('Content-Type', 'text/plain');

res.set({
  'Content-Type': 'text/plain',
  'Content-Length': '123',
  ETag: '12345',
});
```

别名为 `res.header(field [, value])`。


##### res.sendFile()

**签名**

- `path`（`String`）：要传输的文件的路径。除非设置了 `root` 选项，否则必须是绝对路径。
- `options`（`Object`，可选）：提供文件的选项。
  - `maxAge`（`Number | String`，默认 `0`）：以毫秒为单位设置 `Cache-Control` 头的 max-age 属性，或使用 [ms 格式](https://www.npmjs.com/package/ms) 的字符串。
  - `root`（`String`）：相对文件名的根目录。
  - `lastModified`（`Boolean`，默认 `true`）：将 `Last-Modified` 头设置为操作系统上文件的最后修改日期。设置为 `false` 以禁用。
  - `headers`（`Object`）：包含要随文件提供的 HTTP 头的对象。
  - `dotfiles`（`String`，默认 `"ignore"`）：提供点文件的选项。可能的值有 `"allow"`、`"deny"` 和 `"ignore"`。
  - `acceptRanges`（`Boolean`，默认 `true`）：启用或禁用接受范围请求。
  - `cacheControl`（`Boolean`，默认 `true`）：启用或禁用设置 `Cache-Control` 响应头。
  - `immutable`（`Boolean`，默认 `false`）：启用或禁用 `Cache-Control` 响应头中的 `immutable` 指令。如果启用，还应指定 `maxAge` 选项以启用缓存。
- `fn`（`Function`，可选）：传输完成或发生错误时调用的回调 `fn(err)`。

传输给定 `path` 处的文件。根据文件名的扩展名设置 `Content-Type` 响应 HTTP 头字段。除非在选项对象中设置了 `root` 选项，否则 `path` 必须是文件的绝对路径。

> **警告**
>
> 此 API 提供对运行中文件系统上的数据的访问。确保以下任一条件成立：(a) 如果 `path` 参数包含用户输入，则将其构造为绝对路径的方式是安全的；或 (b) 将 `root` 选项设置为某个目录的绝对路径，以限制访问范围。
>
> 当提供 `root` 选项时，`path` 参数允许是相对路径，包括包含 `..`。Express 将验证作为 `path` 提供的相对路径是否会在给定的 `root` 选项内解析。

当传输完成或发生错误时，该方法会调用回调函数 `fn(err)`。如果指定了回调函数并且发生错误，则回调函数必须显式处理响应过程，要么结束请求-响应周期，要么将控制权传递给下一个路由。

以下是使用 `res.sendFile` 及其所有参数的示例。

```js
app.get('/file/:name', (req, res, next) => {
  const options = {
    root: path.join(__dirname, 'public'),
    dotfiles: 'deny',
    headers: {
      'x-timestamp': Date.now(),
      'x-sent': true,
    },
  };

  const fileName = req.params.name;
  res.sendFile(fileName, options, (err) => {
    if (err) {
      next(err);
    } else {
      console.log('Sent:', fileName);
    }
  });
});
```

```ts
import { type Request, type Response, type NextFunction } from 'express';

app.get('/file/:name', (req: Request, res: Response, next: NextFunction) => {
  const options = {
    root: path.join(__dirname, 'public'),
    dotfiles: 'deny',
    headers: {
      'x-timestamp': Date.now(),
      'x-sent': true,
    },
  };

  const fileName = req.params.name;
  res.sendFile(fileName, options, (err) => {
    if (err) {
      next(err);
    } else {
      console.log('Sent:', fileName);
    }
  });
});
```

以下示例展示了使用 `res.sendFile` 为提供文件提供细粒度支持：

```js
app.get('/user/:uid/photos/:file', (req, res) => {
  const uid = req.params.uid;
  const file = req.params.file;

  req.user.mayViewFilesFrom(uid, (yes) => {
    if (yes) {
      res.sendFile(`/uploads/${uid}/${file}`);
    } else {
      res.status(403).send("Sorry! You can't see that.");
    }
  });
});
```

```ts
import { type Request, type Response } from 'express';

app.get('/user/:uid/photos/:file', (req: Request, res: Response) => {
  const uid = req.params.uid;
  const file = req.params.file;

  req.user.mayViewFilesFrom(uid, (yes) => {
    if (yes) {
      res.sendFile(`/uploads/${uid}/${file}`);
    } else {
      res.status(403).send("Sorry! You can't see that.");
    }
  });
});
```

更多信息，或如果你有问题或疑虑，请参阅 [send](https://github.com/pillarjs/send)。