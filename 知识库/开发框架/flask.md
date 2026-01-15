### flask

<https://flask.palletsprojects.com/zh-cn/stable/quickstart/#a-minimal-application>

```python
import flask

app = flask.Flask(__name__)

@app.before_request
def debug():
    print("request path:", flask.request.path)

@app.route("/", methods=["GET", "POST"])
def index():
    return flask.redirect('http://challenge.localhost:80/gate', 302)

app.secret_key = os.urandom(8)
app.run("localhost", 1337)
```

- 当使用 `app = flask.Flask(__name__)` 初始化时，`root_path` 会自动设置为当前 Python 模块所在的目录
- `@app.before_request`
    每一次请求进入此app的路由函数之前自动执行
- `@app.route("/", methods=["GET", "POST"])`  
    设置路由：路径与请求方法
- `flask.redirect(URL, 状态码)`
    设置重定向的位置与状态码
- `flask.request.path`
    获取请求路径
- `flask.request.args.get(key, default=None, type=None)`  
    key：要获取的参数名
    default：参数不存在时的默认值。注，是“参数”不存在而不是“参数值”不存在。
- `flask.request.get_data(as_text=True)`
    读取原始请求体
- `app.secret_key`  
    会话密钥
- 默认的响应头部为 HTML，可直接返回包含HTML内容的字符串