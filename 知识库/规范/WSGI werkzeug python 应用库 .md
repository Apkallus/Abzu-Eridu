https://werkzeug.palletsprojects.com/en/stable/

## Reference

### URL Routing

https://werkzeug.palletsprojects.com/en/stable/routing/

#### Maps, Rules and Adapters —— 映射、规则和适配器

https://werkzeug.palletsprojects.com/en/stable/routing/#maps-rules-and-adapters

```py
class werkzeug.routing.Map(rules=None, default_subdomain='', strict_slashes=True, merge_slashes=True, redirect_defaults=True, converters=None, sort_parameters=False, sort_key=None, host_matching=False)
```

map 类存储所有 URL 规则和一些配置参数。某些配置值仅存储在 `Map` 实例上，因为它们影响所有规则；其他配置值只是默认值，可以针对每条规则覆盖。请注意，除 `rules` 之外的所有参数都必须作为关键字参数指定！

**参数：**

- `rules`（*t.Iterable*[*RuleFactory*] | *None*）—— 此 map 的 url 规则序列。
- `default_subdomain`（*str*）—— 未定义子域的规则的默认子域。
- `strict_slashes`（*bool*）—— 如果规则以斜杠结尾但匹配的 URL 没有，则重定向到带尾部斜杠的 URL。
    > 作用于对应根目录的空串，空串将被重定向到 `/`
- `merge_slashes`（*bool*）—— 在匹配或构建 URL 时合并连续的斜杠。匹配将重定向到规范化后的 URL。变量部分中的斜杠不会被合并。
- `redirect_defaults`（*bool*）—— 如果未以该方式访问，则重定向到默认规则。这有助于创建唯一的 URL。
- `converters`（*t.Mapping*[*str*, *type*[*BaseConverter*]] | *None*）—— 一个转换器字典，向转换器列表添加额外的转换器。如果你重新定义一个转换器，它将覆盖原来的转换器。
- `sort_parameters`（*bool*）—— 如果设置为 `True`，则对 url 参数进行排序。有关更多详细信息，请参见 `url_encode`。
- `sort_key`（*t.Callable*[[*t.Any*], *t.Any*] | *None*）—— `url_encode` 的排序键函数。
- `host_matching`（*bool*）—— 如果设置为 `True`，则启用主机匹配功能并禁用子域匹配功能。如果启用，则使用规则的 `host` 参数而非 `subdomain` 参数。

**变更日志**

- 在 3.0 版本中更改：`charset` 和 `encoding_errors` 参数已被移除。
- 在 1.0 版本中更改：如果 `url_scheme` 为 `ws` 或 `wss`，则仅 WebSocket 规则会匹配。
- 在 1.0 版本中更改：添加了 `merge_slashes` 参数。
- 在 0.7 版本中更改：添加了 `encoding_errors` 和 `host_matching` 参数。
- 在 0.5 版本中更改：添加了 `sort_parameters` 和 `sort_key` 参数。


## 代码库

### routing

#### exceptions.py

```py
class RequestRedirect(HTTPException, RoutingException):
    """Raise if the map requests a redirect. This is for example the case if
    `strict_slashes` are activated and an url that requires a trailing slash.

    The attribute `new_url` contains the absolute destination url.
    """

    code = 308
    ...
```

定义 `strict_slashes` 重定向 code

## HTTP Utilities

https://werkzeug.palletsprojects.com/en/stable/http/

### Form Data Parsing

#### FormDataParser

https://werkzeug.palletsprojects.com/en/stable/http/#werkzeug.formparser.FormDataParser

```py
class werkzeug.formparser.FormDataParser(stream_factory=None, max_form_memory_size=None, max_content_length=None, cls=None, silent=True, *, max_form_parts=None)
```

此类为 Werkzeug 实现表单数据的解析。它本身可以解析 multipart 和 URL 编码的表单数据。它可以被继承和扩展，但对于大多数 MIME 类型，更好的做法是使用未经修改的流，并将其作为请求对象上的单独属性暴露出来。

> 即，自动解析 URL 编码