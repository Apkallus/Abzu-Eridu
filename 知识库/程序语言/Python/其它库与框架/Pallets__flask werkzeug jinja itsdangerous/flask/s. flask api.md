# API

[官网文档](https://flask.palletsprojects.com/en/stable/api/)

[社区旧版文档 0.3 - 1.0 更新日志](https://flaskr.readthedocs.io/ko/flas_kr/en/upgrading.html)


## 待归档

```python
import flask, os

app = flask.Flask(__name__)

@app.before_request
def debug():
    print("request path:", flask.request.path)

@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.route("/", methods=["GET", "POST"])
def index():
    return flask.redirect('http://challenge.localhost:80/gate', 302)


app.secret_key = os.urandom(8)
app.run("localhost", 1337)
```

- 当使用 `app = flask.Flask(__name__)` 初始化时，`root_path` 会自动设置为当前 Python 模块所在的目录
- `app.run(..., threaded=True)`：
    并发处理
- `@app.before_request`
    每一次请求进入此app的路由函数之前自动执行
- `@app.after_request`
    可统一加响应头
- `@app.route(path, methods=[...])`
    设置路由：路径与请求方法
    例：`@app.route("/", methods=["GET", "POST"])`  
    
- `flask.redirect(URL, 状态码)`
    设置重定向的位置与状态码

- `flask.request`
    - `flask.request.path`
        获取请求路径

    - `flask.request.args`
        URL query 参数
        - `flask.request.args.get(key, default=None, type=None)`  
            - key：要获取的参数名
            - default：参数不存在时的默认值。注，是“参数”不存在而不是“参数值”不存在。
            - type: 参数类型

    - `flask.request.get_data(as_text=True)`
        读取原始请求体
    - `flask.request.get_json()`
        JSON body
    - `flask.request.form`
        表单
- `app.secret_key`  
    会话密钥

返回值形式:
- 字符串：作为响应 body（响应头部为 `text/html`)
- `(body, status_code)`：带状态码
- `jsonify(dict)`：返回 JSON，自动 `Content-Type: application/json`


## 应用程序对象

https://flask.palletsprojects.com/en/stable/api/#application-object

### flask.Flask()

```py
class flask.Flask(
    import_name,
    static_url_path=None,
    static_folder='static',
    static_host=None,
    host_matching=False,
    subdomain_matching=False,
    template_folder='templates',
    instance_path=None,
    instance_relative_config=False,
    root_path=None,
)
```

Flask 对象实现一个 WSGI 应用，并作为中心对象。它接收应用程序的模块或包名称。创建后，它作为视图函数、URL 规则、模板配置等的中心注册表。

包名用于解析包内资源或模块所在文件夹，具体取决于包参数解析为实际 Python 包（包含 `__init__.py` 的文件夹）还是标准模块（仅 `.py` 文件）。

有关资源加载的更多信息，请参阅 `open_resource()`。

通常在主模块或包的 `__init__.py` 文件中创建 `Flask` 实例，如下所示：

```py
from flask import Flask
app = Flask(__name__)
```

> **关于第一个参数**
>
> 第一个参数用于让 Flask 知道什么属于你的应用。此名称用于在文件系统上查找资源，可被扩展用于改进调试信息等。
>
> 因此提供什么很重要。如果使用单个模块，`__name__` 始终是正确值。如果使用包，通常建议硬编码包名。
>
> 例如应用程序定义在 `yourapplication/app.py`，应使用以下两个版本之一创建：
>
> ```py
> app = Flask('yourapplication')
> app = Flask(__name__.split('.')[0])
> ```
>
> 为什么？即使使用 `__name__`，应用也能工作，得益于资源查找方式。但这会使调试更痛苦。某些扩展会根据应用的导入名称做出假设。例如 Flask-SQLAlchemy 扩展在调试模式下会查找触发 SQL 查询的代码。如果导入名称设置不正确，调试信息会丢失。（例如它只会拾取 `yourapplication.app` 中的 SQL 查询，而不是 `yourapplication.views.frontend`）

#### config

作为 `Config` 的配置字典。行为与普通字典完全相同，但支持从文件加载配置的额外方法。
> 字典项见 `配置处理` 小节


#### run()

```py
run(host=None, port=None, debug=None, load_dotenv=True, **options)
```

在本地开发服务器上运行应用程序，它不旨在满足生产服务器的安全和性能要求。

如果设置了 `debug` 标志，服务器会在代码更改时自动重新加载，并在发生异常时显示调试器。

> 除非处于调试模式，否则 Flask 会用通用错误页面抑制任何服务器错误。因此，要仅启用交互式调试器而不启用代码重载，必须使用 `debug=True` 和 `use_reloader=False` 调用 `run()`。在非调试模式下设置 `use_debugger` 为 `True` 不会捕获任何异常，因为不会有异常可捕获。

**参数**

- `host` (`str | None`)  
    要监听的主机名。设置为 `'0.0.0.0'` 可使服务器也可从外部访问。默认为 `'127.0.0.1'`，如果存在 `SERVER_NAME` 配置变量则使用其中的主机。

- `port` (`int | None`)  
    Web 服务器端口。默认为 `5000`，如果存在 `SERVER_NAME` 配置变量则使用其中定义的端口。

- `debug` (`bool | None`)  
    如果给出，启用或禁用调试模式。参见 `debug`。`FLASK_DEBUG` 环境变量将覆盖 `debug`。

- `load_dotenv` (`bool`)  
    加载最近的 `.env` 和 `.flaskenv` 文件以设置环境变量。还会将工作目录更改为找到的第一个文件所在目录。

- `options` (`Any`)  
    转发给底层 Werkzeug 服务器的选项。更多信息请参阅 `werkzeug.serving.run_simple()`。

#### debug

```py
debug: bool
```

是否启用调试模式。使用 `flask run` 启动开发服务器时，未处理异常将显示交互式调试器，代码更改时服务器将重新加载。这映射到 `DEBUG` 配置键。如果设置较晚，行为可能不符合预期。

默认：`False`


#### route()

```py
route(rule, **options)
```

视图函数装饰器，使用给定 URL 规则和选项注册。调用 `add_url_rule()`，其实现有更多细节。

```py
@app.route("/")
def index():
    return "Hello, World!"
```

参见“URL 路由注册”。

如果未传入 `endpoint` 参数，路由的端点名称默认为视图函数名称。

`methods` 参数默认为 `["GET"]`。`HEAD` 和 `OPTIONS` 会自动添加。

**参数**

- `rule` (`str`)  
    URL 规则字符串。

- `options` (`Any`)  
    传递给 `Rule` 对象的额外选项。

#### 🎯 secret_key

如果设置了密钥，加密组件可以使用它来签名 cookie 和其他内容。例如，当你想使用安全 cookie 时，将其设置为复杂的随机值。

此属性也可以通过配置键 `SECRET_KEY` 配置。默认为 `None`。

#### before_request()

```py
before_request(f)
```

修饰器，注册一个在每个请求之前运行的函数。

函数将不带任何参数调用。如果它返回非 `None` 值，该值将像视图返回值一样处理，并停止进一步的请求处理。

#### after_request()

```py
after_request(f)
```

注册一个在此对象上每个请求之后运行的函数。

函数以响应对象调用，并且必须返回响应对象。这允许函数在发送之前修改或替换响应。

如果函数引发异常，任何剩余的 `after_request` 函数将不会被调用。

#### redirect() —— 创建重定向响应对象

```py
redirect(location, code=302)
```

由 `flask.redirect()` 调用，也可以直接调用。

**参数**

- `location` (`str`)  
    要重定向到的 URL。

- `code` (`int`)  
    重定向的状态码。

**返回类型**

`BaseResponse`

示例

```py
flask.redirect('http://example.net/', 302)
```

## 传入请求数据

### class flask.Request()

```py
class flask.Request(environ, populate_request=True, shallow=False)
```

Flask 默认使用的请求对象。会记住匹配的端点与视图参数。它就是最终作为 `request` 的对象。

#### environ

```py
environ: WSGIEnvironment
```

包含 HTTP 头和来自 WSGI 服务器信息的 WSGI 环境。
> 打印时以字典的形式，包括非当前对象的键值对

#### url

```py
property url: str
```

完整请求 URL，包括方案、主机、根路径、路径和查询字符串。

#### server

服务器地址。`(host, port)`，对于 Unix 套接字为 `(path, None)`，如果未知则为 `None`。

#### remote_addr

发送请求的客户端地址。

#### method

发出请求所用的方法，例如 `GET`。

#### path

`root_path` 之后的 URL 路径部分。这是应用中用于路由的路径。

#### scheme

请求所用协议的 URL 方案，例如 `https` 或 `wss`。

#### headers

随请求接收的头。

#### data

```py
property data: bytes
```

从 `stream` 读取的原始数据。如果请求表示表单数据，则为空。

即使表示表单数据也要获取原始数据，请使用 `get_data()`。


#### get_data()

```py
get_data(cache=True, as_text=False, parse_form_data=False) -> bytes | str
```

将客户端传入的缓冲数据读入一个 bytes 对象。默认缓存，但可通过将 `cache` 设置为 `False` 更改。

通常不建议在不先检查内容长度的情况下调用此方法，因为客户端可能发送数十兆字节或更多，导致服务器内存问题。

注意，如果表单数据已经解析，此方法将不返回任何内容，因为表单数据解析不会像此方法那样缓存数据。要隐式调用表单数据解析函数，请将 `parse_form_data` 设置为 `True`。这样做时，如果表单解析器处理了数据，此方法的返回值将为空字符串。通常不需要这样做，因为如果整个数据已缓存（默认），表单解析器将使用缓存数据解析表单数据。请在任何情况下都注意先检查内容长度，再调用此方法，以避免耗尽服务器内存。

如果 `as_text` 设置为 `True`，返回值将是解码后的字符串。

## 响应对象

### `flask.Response(...)`

```py
class flask.Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False)
```

Flask 默认使用的响应对象。其行为类似 Werkzeug 的响应对象，但默认 mimetype 为 HTML。

#### `status`

```py
status: str
```

HTTP 状态码作为字符串。

#### `status_code`

```py
status_code: int
```

HTTP 状态码作为数字。

#### get_data()

```py
get_data(as_text=False) → bytes | str
```

响应正文的字符串表示。每当调用此属性时，响应可迭代对象会被编码并展平。如果流式传输大数据，可能导致不希望的行为。

可以通过将 `implicit_sequence_conversion` 设置为 `False` 来禁用此行为。

如果 `as_text` 设置为 `True`，返回值将是解码后的字符串。

## 模板渲染

### flask.render_template_string —— 从字符串渲染模板

```py
flask.render_template_string(source, **context)
```

## 有用的函数和类

```py
# SSTI 视图函数内，非顶层
from flask import current_app, after_this_request
@after_this_request
def hook(response): # 回调函数接收 response
    from flask import make_response
    return make_response('foo') # 回调函数返回 response，新或旧
```

### `flask.current_app` —— 访问当前应用

当前正在处理请求的应用的代理。这对于无需导入应用即可访问应用很有用，或者在无法导入应用时（例如使用应用工厂模式、蓝图和扩展中）很有用。

> 代码注入时，直接访问当前应用

### `flask.after_this_request()` —— 装饰器：在当前请求后执行函数

```python
flask.after_this_request(f)
```

在此请求后执行函数。这可用于修改响应对象。函数接收响应对象，必须返回相同或新的响应对象。

> 代码注入时，返回载荷请求的执行结果

示例：

```python
@app.route('/')
def index():
    @after_this_request
    def add_header(response):
        response.headers['X-Foo'] = 'Parachute'
        return response
    return 'Hello World!'
```

### `flask.make_response()` —— 创建响应对象

```python
flask.make_response(*args)
```

调用此函数而不是使用 `return`，将获得一个可用于附加头的响应对象。