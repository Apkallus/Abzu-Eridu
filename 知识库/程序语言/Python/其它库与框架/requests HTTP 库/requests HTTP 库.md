https://requests.readthedocs.io/en/latest/

# Requests: HTTP for Humans™

**`Requests`** 是一个优雅而简单的 `Python` `HTTP` 库，为人类而构建。

---

**见证 `Requests` 的力量**：

```pycon
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"type":"User"...'
>>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```

参见[类似代码，不使用 `Requests`](https://gist.github.com/973705)。

`Requests` 让你极其轻松地发送 `HTTP/1.1` 请求。无需手动向 `URL` 添加查询字符串，也无需对 `POST` 数据进行表单编码。得益于 [`urllib3`](https://github.com/urllib3/urllib3)，`Keep-Alive` 和 `HTTP` 连接池是 100% 自动的。

## 备受喜爱的特性

`Requests` 已为当今的 `Web` 做好准备。

- `Keep-Alive` 与连接池
- 国际化域名和 `URL`
- 带 `Cookie` 持久化的会话
- 浏览器风格的 `SSL` 验证
- 自动内容解码
- `Basic/Digest` 身份验证
- 优雅的键/值 `Cookie`
- 自动解压缩
- `Unicode` 响应体
- `HTTP(S)` 代理支持
- 多部分文件上传
- 流式下载
- 连接超时
- 分块请求
- `.netrc` 支持

`Requests` 官方支持 `Python 3.10+`，并且在 `PyPy` 上运行良好。