# urllib.parse --- 将 URL 解析为组件

https://docs.python.org/zh-cn/3.15/library/urllib.parse.html

该模块定义了一个标准接口，用于将统一资源定位符（URL）字符串拆分为不同部分（协议、网络位置、路径等），或将各个部分组合回 URL 字符串，并将“相对 URL”转换为基于给定的“基准 URL”的绝对 URL。

## URL 解析

### 🎯 urllib.parse.urljoin()

```py
urllib.parse.urljoin(base, url, allow_fragments=True)
```

通过合并一个 "基准 URL" (base) 和另一个 URL (url) 来构造一个完整 ("absolute") URL。



> 备注：如果 url 为绝对 URL (即以 `//` 或 `scheme://` 打头)，则 url 的主机名和/或协议将出现在结果中。 例如: 
> ```py
> urljoin("http://base.com", "http://url.net")
> # http://url.net
> ```