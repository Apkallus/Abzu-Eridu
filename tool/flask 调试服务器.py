import flask, os

app = flask.Flask(__name__)

@app.before_request
def print_request():
    print("\n====== print request ======")
    print(f"url: {flask.request.url}")
    print(f"client_addr: {flask.request.environ['REMOTE_ADDR']}:{flask.request.environ['REMOTE_PORT']}")
    print(f"server_addr: {flask.request.server}")
    print("=== print headers ===")
    print(f"{flask.request.method} {flask.request.path} {flask.request.environ["SERVER_PROTOCOL"]}")
    print(f"{flask.request.headers}")
    print("=== print row body ===")
    print(f"{flask.request.get_data()}")
    print("=== print pretty body ===")
    print(f"{flask.request.get_data(as_text=True)}")
    # 打印环境信息
    # print(f"{flask.request.environ}")

@app.after_request
def print_response(response: flask.Response):
    print("\n====== print response ======")
    print("=== print headers ===")
    print(f"{response.status} {flask.request.environ["SERVER_PROTOCOL"]}")
    print(f"{response.headers}")
    print("=== print row body ===")
    print(f"{response.get_data()}")
    return response

@app.after_request
def set_headers(response: flask.Response):
    # 设置跨域头部
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return "foo"

# 启用 deubg 模式：代码变动时热重载，立即生效
app.debug = True
app.secret_key = os.urandom(8)
app.run("localhost", 1337)