[社区 0.5 旧版文档](http://mitsuhiko.pocoo.org/werkzeug-docs/index.html)


## 旧版

### ⚔️ Secure Cookie

http://mitsuhiko.pocoo.org/werkzeug-docs/contrib/securecookie.html

该模块实现了一种客户端无法篡改的 Cookie，因为它会添加一个由服务端校验的校验和。如果你只需要保存用户 ID，或用于标识已登录用户的少量信息，可以将它作为会话（session）的替代方案。

需要注意的是，与普通 Cookie 一样，这些数据仍然可以被客户端读取。不过，你无需在服务端存储和清理会话数据。

示例用法：

```python
>>> from werkzeug.contrib.securecookie import SecureCookie
>>> x = SecureCookie({"foo": 42, "baz": (1, 2, 3)}, "deadbeef")
```

将其序列化为字符串，以便存入 Cookie：

```python
>>> value = x.serialize()
```

再从该字符串中反序列化：

```python
>>> x = SecureCookie.unserialize(value, "deadbeef")
>>> x["baz"]
(1, 2, 3)
```

如果有人修改了 Cookie，导致校验和错误，`unserialize` 方法会静默失败，并返回一个新的空 `SecureCookie` 对象。

请注意，Cookie 中的值对客户端可见，因此不要把不希望用户看到的数据存入 Cookie。