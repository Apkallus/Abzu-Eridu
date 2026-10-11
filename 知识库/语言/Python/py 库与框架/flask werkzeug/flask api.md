# API

https://flask.palletsprojects.com/zh-cn/stable/api
[社区旧版文档 0.3 - 1.0 更新日志](https://flaskr.readthedocs.io/ko/flas_kr/en/upgrading.html)


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
