[文档](https://playwright.dev/python/docs/)
- [中文版](https://playwright.net.cn/python/docs/intro) JS 功能异常

# API 参考

## Playwright

```py
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("http://example.com")
    # other actions...
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

## Classes

### Browser

浏览器通过 `browser_type.launch()` 创建。使用 `Browser` 创建 `Page` 的示例

```py
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
```

#### 方法

##### new_context

创建一个新的浏览器上下文。它不会与其他浏览器上下文共享 cookie/缓存。

```py
browser = playwright.firefox.launch() # or "chromium" or "webkit".
# create a new incognito browser context.
context = browser.new_context()
# create a new page in a pristine context.
page = context.new_page()
page.goto("https://example.com")

# gracefully close up everything
context.close()
browser.close()
```

##### new_page

在新的浏览器上下文中创建一个新页面。关闭此页面也会关闭上下文。

这是一个便捷 API，仅应用于单页场景和简短的代码片段。生产代码和测试框架应显式调用 `browser.new_context()`，然后调用` browser_context.new_page()` 来精确控制它们的生命周期。

```py
browser.new_page()
browser.new_page(**kwargs)
```


#### 事件

##### `on("context")`

当创建新的浏览器上下文时触发。

```py
browser.on("context", handler)
```

### BrowserContext

https://playwright.dev/python/docs/api/class-browsercontext

浏览器上下文 (BrowserContexts) 提供了一种操作多个独立浏览器会话的方式。

如果一个页面打开另一个页面，例如通过 `window.open` 调用，则弹出的页面将属于父页面的浏览器上下文。

Playwright 允许使用 `browser.new_context()` 方法创建隔离的非持久浏览器上下文。非持久浏览器上下文不会将任何浏览数据写入磁盘。

```py
# create a new incognito browser context
context = browser.new_context()
# create a new page inside context.
page = context.new_page()
page.goto("https://example.com")
# dispose context once it is no longer needed.
context.close()
```

#### 事件

##### `on("console")`

当页面中的 JavaScript 调用其中一个 console API 方法（例如 `console.log` 或 `console.dir`）时触发。

传递给 `console.log` 和页面的参数可在 `ConsoleMessage` 事件处理程序参数上获取。

事件数据
- `ConsoleMessage`


##### `on("request")`

当页面发出请求时触发。`request` 对象是只读的。要拦截并修改请求，请参阅 `page.route()` 或 `browser_context.route()`。

```py
page.on("request", handler)
```

事件数据
- `Request`

##### `on("pageerror")`

当页面内发生未捕获异常时发出。

```py
# Log all uncaught errors to the terminal
page.on("pageerror", lambda exc: print(f"uncaught exception: {exc}"))

# Navigate to a page with an exception.
page.goto("data:text/html,<script>throw new Error('test')</script>")
```

```py
page.on("pageerror", handler)
```

事件数据
- `Error`

##### `on("response")`

当接收到请求的 response 状态和标头时触发。对于成功的响应，事件顺序依次为 request、response 和 requestfinished。

```py
page.on("response", handler)
```

事件数据
- `Response`

### ConsoleMessage

https://playwright.net.cn/python/docs/api/class-consolemessage

`ConsoleMessage` 对象由页面通过 `page.on("console")` 事件分发。页面中记录的每个控制台消息在 Playwright 上下文中都有一个对应的事件。

```py
# Listen for all console logs
page.on("console", lambda msg: print(msg.text))

# Listen for all console events and handle errors
page.on("console", lambda msg: print(f"error: {msg.text}") if msg.type == "error" else None)

# Get the next console log
with page.expect_console_message() as msg_info:
    # Issue console.log inside the page
    page.evaluate("console.log('hello', 42, { foo: 'bar' })")
msg = msg_info.value

# Deconstruct print arguments
msg.args[0].json_value() # hello
msg.args[1].json_value() # 42
```

### Request

每当页面发送网络资源请求时，Page 会触发以下事件序列：

- 当页面发出请求时触发 `page.on("request")`。
- 当收到请求的响应状态和响应头时触发 `page.on("response")`。
- 当响应体下载完成且请求完成时触发 `page.on("requestfinished")`。

如果请求在某些时候失败，则会触发 `page.on("requestfailed")` 事件，而不是 `'requestfinished'` 事件（并且可能不会触发 `'response'` 事件）。

HTTP 错误响应，例如 404 或 503，从 HTTP 角度来看仍然是成功响应，因此请求将以`'requestfinished'`事件完成。

如果请求收到“重定向”响应，则该请求将成功地以`requestfinished`事件完成，并且会向重定向的 URL 发出新请求。

#### 属性

##### method

请求方法（GET、POST 等）

```py
request.method
```

返回
- `str`


##### url

请求的 URL。

```py
request.url
```

返回
- `str`


### Response

https://playwright.net.cn/python/docs/api/class-response

Response 类表示页面接收到的响应。

#### 属性

##### status

包含响应的状态码（例如，成功时为 200）。

```py
response.status
```

返回
- `int`

##### url

包含响应的 URL。

```py
response.url
```

返回
- `str`


### error

https://playwright.net.cn/python/docs/api/class-error


继承自：`Exception`

当某些操作异常终止时，就会引发 Error，例如在 `page.evaluate()` 运行期间浏览器关闭。所有 Playwright 异常都继承自此类。

#### 属性

##### message

错误消息。

```py
error.message
```

类型
- `str`
