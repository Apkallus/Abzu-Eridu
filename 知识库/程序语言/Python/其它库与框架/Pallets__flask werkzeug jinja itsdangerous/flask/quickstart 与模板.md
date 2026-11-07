# flask 

## 快速应用

[快速应用](https://flask.palletsprojects.com/zh-cn/stable/quickstart/#a-minimal-application)

### 会话

除了请求对象之外，还有第二个对象叫做 [session]，它允许你跨请求存储特定于某个用户的信息。这是基于 cookie 为你实现的，并对 cookie 进行加密签名。这意味着用户可以看到 cookie 的内容，但无法修改它，除非他们知道用于签名的密钥。

为了使用会话，你必须设置一个密钥。会话的工作方式如下：

```python
from flask import session

# 将密钥设置为一些随机字节。务必严格保密！
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # 如果 session 中存在 username，则将其移除
    session.pop('username', None)
    return redirect(url_for('index'))
```

> 如何生成良好的密钥
> 
> 密钥应尽可能随机。你的操作系统可以通过加密随机生成器生成相当随机的数据。使用以下命令可快速为 `Flask.secret_key`（或 [SECRET_KEY]）生成一个值：
> 
> ```console
> $ python -c 'import secrets; print(secrets.token_hex())'
> '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
> ```

关于基于 cookie 的会话的说明：Flask 会把你放入 `session` 对象的值序列化到一个 cookie 中。如果你发现某些值无法跨请求持久化，而 cookie 确实已启用，并且你没有收到明确的错误消息，请检查页面响应中 cookie 的大小与 Web 浏览器支持的大小相比如何。

除了默认的基于客户端的会话之外，如果你希望改为在服务器端处理会话，有若干 Flask 扩展支持这一点。

## 模板

https://flask.palletsprojects.com/zh-cn/stable/templating/

Flask 使用 `Jinja2` 作为默认的模板渲染引擎。