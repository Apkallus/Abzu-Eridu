https://flask.palletsprojects.com/en/stable/config/

# 配置处理

`Flask` 对象的 `config` 属性保存各来源的已加载配置值。

## 配置基础

`config` 是字典的子类：

```py
app = Flask(__name__)
app.config['TESTING'] = True
```

某些配置值也会转发到 `Flask` 对象，因此可从那里读取和写入它们：

```py
app.testing = True
```

要一次更新多个键，使用 `dict.update()` 方法：

```py
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
```

## 内置配置值

以下配置值由 Flask 内部使用：

- `DEBUG`  
    是否启用调试模式。使用 `flask run` 启动开发服务器时，未处理异常会显示交互式调试器，代码更改时服务器会重新加载。`debug` 属性映射到此配置键。该值由 `FLASK_DEBUG` 环境变量设置。
    > 调试时开启，简化过程
    
    默认：`False`

- `SERVER_NAME`  
    告知应用它绑定到的主机和端口。
        
    默认：`None`
    
- `SECRET_KEY`  
    用于安全签名会话 cookie 的密钥，也可供扩展或应用用于任何其他安全相关需求。它应是较长的随机 `bytes` 或 `str`。
    
    默认：`None`