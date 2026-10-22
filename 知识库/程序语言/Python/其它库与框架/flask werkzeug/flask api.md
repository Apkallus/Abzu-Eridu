# API

https://flask.palletsprojects.com/zh-cn/stable/api
[社区旧版文档 0.3 - 1.0 更新日志](https://flaskr.readthedocs.io/ko/flas_kr/en/upgrading.html)


## 待归档

```python
import flask

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


## Application Object

### Flask

#### 🎯 `secret_key`

如果设置了密钥，加密组件便可使用它对 cookie 及其他内容进行签名。例如，当你希望使用安全 cookie 时，请将其设置为复杂的随机值。

此属性也可通过配置中的 [`SECRET_KEY`] 配置键进行配置。默认值为 `None`。

## Template Rendering

### flask.render_template_string —— 从字符串渲染模板

```py
flask.render_template_string(source, **context)
```
