https://werkzeug.palletsprojects.com/en/stable/datastructures/#http-related

## HTTP 相关

### Headers

```py
class werkzeug.datastructures.Headers([defaults])
```

存储一些标头的对象。它具有类似字典的接口，但有序，可以多次存储相同的键，并且迭代产生 `(key, value)` 对而不是仅产生键。

如果你想更优雅地处理以元组列表形式存储的 WSGI 标头，此数据结构很有用。

从 Werkzeug 0.3 起，此类引发的 `KeyError` 同时也是 `BadRequest` HTTP 异常的子类，如果在 HTTP 异常的通配捕获中被捕获，将渲染 `400 BAD REQUEST` 页面。

Headers 与 Python 的 `wsgiref.headers.Headers` 类基本兼容，但 `__getitem__` 除外。`wsgiref` 对 `headers['missing']` 返回 `None`，而 `Headers` 会引发 `KeyError`。

要创建新的 `Headers` 对象，请向它传递一个包含默认值的列表、字典或其他 `Headers` 对象。这些值的验证方式与稍后添加的值相同。

标头键被假定为可信且有效的，它们不得来自不受信任的用户输入。标头值中不允许换行，否则会引发 `ValueError`。

参数：

- `defaults`（`Headers | MultiDict[str, t.Any] | cabc.Mapping[str, t.Any | list[t.Any] | tuple[t.Any, ...] | set[t.Any]] | cabc.Iterable[tuple[str, t.Any]] | None`）  
    用于 `Headers` 的默认值列表。

> **变更日志**
>
> 在 3.1 版本中更改：实现 `|` 和 `|=` 运算符。
>
> 在 2.1.0 版本中更改：默认值的验证方式与稍后添加的值相同。
>
> 在 0.9 版本中更改：此数据结构现在存储 unicode 值，类似于 multi dict 的方式。主要区别在于也可以设置字节，这些字节会自动按 latin1 解码。
>
> 在 0.9 版本中更改：`linked()` 函数已被移除且没有替代品，因为它是一个不支持编码模型更改的 API。

#### `get()`

```py
get(key: str) -> str | None
get(key: str, default: str) -> str
get(key: str, default: T) -> str | T
get(key: str, type: Callable[[str], T]) -> T | None
get(key: str, default: T, type: Callable[[str], T]) -> T
```

如果请求的数据不存在，则返回默认值。如果提供了 `type` 且它是可调用对象，则应转换值、返回该值，或者如果无法转换则引发 `ValueError`。在这种情况下，函数将返回默认值，就像未找到值一样：

```pycon
>>> d = Headers([('Content-Length', '42')])
>>> d.get('Content-Length', type=int)
42
```

参数：

- `key`（`str`）  
    要查找的键。
- `default`（`str | T | None`）  
    如果无法查找键则返回的默认值。如果未进一步指定，则返回 `None`。
- `type`（`Callable[[str], T] | None`）  
    用于在 `Headers` 中转换值的可调用对象。如果此可调用对象引发 `ValueError`，则返回默认值。

返回类型：`str | T | None`

> **变更日志**
>
> 在 3.0 版本中更改：移除 `as_bytes` 参数。
>
> 在 0.9 版本中更改：新增 `as_bytes` 参数。

#### `getlist()`

```py
getlist(key: str) -> list[str]
getlist(key: str, type: Callable[[str], T]) -> list[T]
```

返回给定键的项目列表。如果该键不在 `Headers` 中，返回值将为空列表。与 `get()` 一样，`getlist()` 接受 `type` 参数。所有项目都将使用其中定义的可调用对象进行转换。

参数：

- `key`（`str`）  
    要查找的键。
- `type`（`Callable[[str], T] | None`）  
    用于在 `Headers` 中转换值的可调用对象。如果此可调用对象引发 `ValueError`，该值将从列表中移除。

返回：该键所有值的 `list`。

返回类型：`list[str] | list[T]`

> **变更日志**
>
> 在 3.0 版本中更改：移除 `as_bytes` 参数。
>
> 在 0.9 版本中更改：新增 `as_bytes` 参数。

#### `get_all()`

```py
get_all(name) → list[str]
```

返回指定字段所有值的列表。

此方法与 `wsgiref` 的 `get_all()` 方法兼容。

参数：

- `name`（`str`）

返回类型：`list[str]`

#### `extend()`

```py
extend(arg=None, /, **kwargs) → None
```

使用另一个包含标头项的对象以及关键字参数扩展此对象中的标头。

要替换现有键而不是扩展，请使用 `update()`。

如果提供，第一个参数可以是另一个 `Headers` 对象、`MultiDict`、`dict` 或对的迭代器。

标头键被假定为可信且有效的，它们不得来自不受信任的用户输入。标头值中不允许换行，否则会引发 `ValueError`。

> **变更日志**
>
> 在 1.0 版本中更改：支持 `MultiDict`。允许传递 `kwargs`。

参数：

- `arg`（`Headers | MultiDict[str, Any] | Mapping[str, Any | list[Any] | tuple[Any, ...] | set[Any]] | Iterable[tuple[str, Any]] | None`）
- `kwargs`（`str`）

返回类型：`None`

#### `remove()`

```py
remove(key) → None
```

移除一个键。

参数：

- `key`（`str`）  
    要移除的键。

返回类型：`None`

#### `pop()`

```py
pop() → tuple[str, str]
pop(key: str) -> str
pop(key: int | None = None) -> tuple[str, str]
pop(key: str, default: str) -> str
pop(key: str, default: T) -> str | T
```

移除并返回一个键或索引。

参数：

- `key`（`str | int | None`）  
    要弹出的键。如果它是整数，则移除该位置的项目；如果是字符串，则移除该键的值。如果省略键或为 `None`，则移除最后一项。
- `default`（`str | T`）

返回：一个项目。

返回类型：`str | tuple[str, str] | T`

#### `popitem()`

```py
popitem() → tuple[str, str]
```

移除一个键或索引并返回一个 (key, value) 项目。

返回类型：`tuple[str, str]`

#### `add()`

```py
add(key, value, /, **kwargs) → None
```

向列表添加新的标头元组。

关键字参数可以为标头值指定附加参数，下划线会转换为短横线：

```pycon
>>> d = Headers()
>>> d.add('Content-Type', 'text/plain')
>>> d.add('Content-Disposition', 'attachment', filename='foo.png')
```

关键字参数转储在后台使用 `dump_options_header()`。

参数：

- `key`（`str`）  
    标头键。这被假定为可信且有效的，它不得来自不受信任的用户输入。
- `value`（`Any`）  
    标头值。不允许换行，否则会引发 `ValueError`。
- `kwargs`（`Any`）

返回类型：`None`

> **变更日志**
>
> 在 0.4.1 版本中更改：为 `wsgiref` 兼容性新增关键字参数。

#### `add_header()`

```py
add_header(key, value, /, **kwargs) → None
```

向列表添加新的标头元组。

`add()` 的别名，用于与 `wsgiref` 的 `add_header()` 方法兼容。

参数：

- `key`（`str`）
- `value`（`Any`）
- `kwargs`（`Any`）

返回类型：`None`

#### `clear()`

```py
clear() → None
```

清除所有标头。

返回类型：`None`

#### `set()`

```py
set(key, value, /, **kwargs) → None
```

移除 `key` 的所有标头元组并添加一个新的。如果之前没有条目，新添加的键将出现在列表末尾；否则替换第一个条目。

关键字参数可以为标头值指定附加参数，下划线会转换为短横线。更多信息请参见 `add()`。

> **变更日志**
>
> 在 0.6.1 版本中更改：`set()` 现在接受与 `add()` 相同的参数。

参数：

- `key`（`str`）  
    标头键。这被假定为可信且有效的，它不得来自不受信任的用户输入。
- `value`（`Any`）  
    标头值。不允许换行，否则会引发 `ValueError`。
- `kwargs`（`Any`）

返回类型：`None`

#### `setlist()`

```py
setlist(key, values) → None
```

移除标头的任何现有值并添加新值。

参数：

- `key`（`str`）  
    标头键。这被假定为可信且有效的，它不得来自不受信任的用户输入。
- `value`  
    标头值的可迭代对象。不允许换行，否则会引发 `ValueError`。
- `values`（`Iterable[Any]`）

返回类型：`None`

> **变更日志**
>
> 在 1.0 版本中新增。

#### `setdefault()`

```py
setdefault(key, default) → str
```

如果键在标头中，则返回该键的第一个值；否则将标头设置为 `default` 给定的值并返回该值。

参数：

- `key`（`str`）  
    标头键。这被假定为可信且有效的，它不得来自不受信任的用户输入。
- `default`（`Any`）  
    如果键不存在时要设置的标头值。不允许换行，否则会引发 `ValueError`。

返回类型：`str`

#### `setlistdefault()`

```py
setlistdefault(key, default) → list[str]
```

如果键在标头中，则返回该键的值列表；否则将标头设置为 `default` 给定的值列表并返回该值。

与 `MultiDict.setlistdefault()` 不同，修改返回的列表不会影响标头。

参数：

- `key`（`str`）  
    标头键。这被假定为可信且有效的，它不得来自不受信任的用户输入。
- `default`（`Iterable[Any]`）  
    如果键不存在时要设置的标头值可迭代对象。不允许换行，否则会引发 `ValueError`。

返回类型：`list[str]`

> **变更日志**
>
> 在 1.0 版本中新增。

#### `update()`

```py
update(arg=None, /, **kwargs) → None
```

使用另一个标头对象和关键字参数中的项替换此对象中的标头。

要扩展现有键而不是替换，请使用 `extend()`。

如果提供，第一个参数可以是另一个 `Headers` 对象、`MultiDict`、`dict` 或对的迭代器。

标头键被假定为可信且有效的，它们不得来自不受信任的用户输入。标头值中不允许换行，否则会引发 `ValueError`。

> **变更日志**
>
> 在 1.0 版本中新增。

参数：

- `arg`（`Headers | MultiDict[str, Any] | Mapping[str, Any | list[Any] | tuple[Any, ...] | Set[Any]] | Iterable[tuple[str, Any]] | None`）
- `kwargs`（`Any | list[Any] | tuple[Any, ...] | Set[Any]`）

返回类型：`None`

#### `to_wsgi_list()`

```py
to_wsgi_list() → list[tuple[str, str]]
```

将标头转换为适合 WSGI 的列表。

返回：列表

返回类型：`list[tuple[str, str]]`

### EnvironHeaders

```py
class werkzeug.datastructures.EnvironHeaders(environ)
```

来自 WSGI 环境的标头只读版本。它提供与 `Headers` 相同的接口，并从 WSGI 环境构造。从 Werkzeug 0.3 起，此类引发的 `KeyError` 同时也是 `BadRequest` HTTP 异常的子类，如果在 HTTP 异常的通配捕获中被捕获，将渲染 `400 BAD REQUEST` 页面。

参数：

- `environ`（`WSGIEnvironment`）

### HeaderSet

```py
class werkzeug.datastructures.HeaderSet(headers=None, on_update=None)
```

类似于 `ETags` 类，这实现了一个类似集合的结构。与 `ETags` 不同，它大小写不敏感，用于 vary、allow 和 content-language 标头。

如果未使用 `parse_set_header()` 函数构造，实例化方式如下：

```pycon
>>> hs = HeaderSet(['foo', 'bar', 'baz'])
>>> hs
HeaderSet(['foo', 'bar', 'baz'])
```

参数：

- `headers`（`cabc.Iterable[str] | None`）
- `on_update`（`cabc.Callable[[te.Self], None] | None`）

#### `add()`

```py
add(header) → None
```

向集合中添加新标头。

参数：

- `header`（`str`）

返回类型：`None`

#### `remove()`

```py
remove(header) → None
```

从集合中移除标头。如果标头不在集合中，则引发 `KeyError`。

> **变更日志**
>
> 在 0.5 版本中更改：在旧版本中，如果对象缺失，会引发 `IndexError` 而不是 `KeyError`。

参数：

- `header`（`str`）  
    要移除的标头。
- `self`（`te.Self`）

返回类型：`None`

#### `update()`

```py
update(iterable) → None
```

将可迭代对象中的所有标头添加到集合中。

参数：

- `iterable`（`cabc.Iterable[str]`）  
    用可迭代对象中的项更新集合。
- `self`（`te.Self`）

返回类型：`None`

#### `discard()`

```py
discard(header) → None
```

类似于 `remove()` 但忽略错误。

参数：

- `header`（`str`）  
    要丢弃的标头。

返回类型：`None`

#### `find()`

```py
find(header) → int
```

返回标头在集合中的索引，如果未找到则返回 -1。

参数：

- `header`（`str`）  
    要查找的标头。

返回类型：`int`

#### `index()`

```py
index(header) → int
```

返回标头在集合中的索引，或引发 `IndexError`。

参数：

- `header`（`str`）  
    要查找的标头。

返回类型：`int`

#### `clear()`

```py
clear() → None
```

清除集合。

参数：

- `self`（`te.Self`）

返回类型：`None`

#### `as_set()`

```py
as_set(preserve_casing=False) → set[str]
```

将集合作为真正的 Python `set` 类型返回。调用此方法时，所有项都转换为小写，顺序丢失。

参数：

- `preserve_casing`（`bool`）  
    如果设置为 `True`，返回集合中的项将保留 `HeaderSet` 中的原始大小写；否则将为小写。

返回类型：`set[str]`

#### `to_header()`

```py
to_header() → str
```

将标头集合转换为 HTTP 标头字符串。

返回类型：`str`

### Accept

```py
class werkzeug.datastructures.Accept(values=())
```

`Accept` 对象只是用于 `(value, quality)` 元组列表的 `list` 子类。它会自动按特异性和质量排序。

所有 `Accept` 对象的工作方式类似于列表，但提供处理数据的额外功能。包含检查被规范化为此标头的规则：

```pycon
>>> a = CharsetAccept([('ISO-8859-1', 1), ('utf-8', 0.7)])
>>> a.best
'ISO-8859-1'
>>> 'iso-8859-1' in a
True
>>> 'UTF8' in a
True
>>> 'utf7' in a
False
```

要获取项目的质量，可以使用普通的项目查找：

```pycon
>>> print a['utf-8']
0.7
>>> a['utf7']
0
```

> **变更日志**
>
> 在 1.0.0 版本中更改：对于相同质量的标签，`Accept` 内部值不再按字母顺序排列。而是保留初始顺序。
>
> 在 0.5 版本中更改：`Accept` 对象现在被强制为不可变。

参数：

- `values`（`Accept | cabc.Iterable[tuple[str, float]] | None`）

#### `quality()`

```py
quality(key) → float
```

返回键的质量。

> **变更日志**
>
> 在 0.6 版本中新增：在以前的版本中，你必须使用项目查找语法（例如 `obj[key]` 而不是 `obj.quality(key)`）。

参数：

- `key`（`str`）

返回类型：`float`

#### `index()`

```py
index(key) → int
```

获取条目的位置或引发 `ValueError`。

参数：

- `key`（`str | tuple[str, float]`）  
    要查找的键。

返回类型：`int`

> **变更日志**
>
> 在 0.5 版本中更改：以前会引发 `IndexError`，这与列表 API 不一致。

#### `find()`

```py
find(key) → int
```

获取条目的位置或返回 -1。

参数：

- `key`（`str | tuple[str, float]`）  
    要查找的键。

返回类型：`int`

#### `values()`

```py
values() → Iterator[str]
```

遍历所有值。

返回类型：`Iterator[str]`

#### `to_header()`

```py
to_header() → str
```

将标头集合转换为 HTTP 标头字符串。

返回类型：`str`

#### `best_match()`

```py
best_match(matches: Iterable[str]) -> str | None
best_match(matches: Iterable[str], default: str = None) -> str
```

根据客户端的特异性和质量从可能匹配项列表中返回最佳匹配。如果两个项目具有相同的质量和特异性，则返回先出现的那个。

参数：

- `matches`（`Iterable[str]`）  
    要检查的匹配项列表。
- `default`（`str | None`）  
    如果没有匹配项则返回的值。

返回类型：`str | None`

#### `best`

```py
property best: str | None
```

最佳匹配作为值。

### MIMEAccept

```py
class werkzeug.datastructures.MIMEAccept(values=())
```

类似于 `Accept`，但具有针对 mimetype 的特殊方法和行为。

参数：

- `values`（`Accept | cabc.Iterable[tuple[str, float]] | None`）

#### `accept_html`

```py
property accept_html: bool
```

如果此对象接受 HTML，则为 `True`。

#### `accept_xhtml`

```py
property accept_xhtml: bool
```

如果此对象接受 XHTML，则为 `True`。

#### `accept_json`

```py
property accept_json: bool
```

如果此对象接受 JSON，则为 `True`。

### CharsetAccept

```py
class werkzeug.datastructures.CharsetAccept(values=())
```

类似于 `Accept`，但针对字符集进行了规范化。

参数：

- `values`（`Accept | cabc.Iterable[tuple[str, float]] | None`）

### LanguageAccept

```py
class werkzeug.datastructures.LanguageAccept(values=())
```

类似于 `Accept`，但针对语言标签进行了规范化。

参数：

- `values`（`Accept | cabc.Iterable[tuple[str, float]] | None`）

### RequestCacheControl

```py
class werkzeug.datastructures.RequestCacheControl(values=(), on_update=None)
```

请求的缓存控制。这是不可变的，并提供对所有与请求相关的缓存控制标头的访问。

要再次获取 `RequestCacheControl` 对象的标头，可以将对象转换为字符串或调用 `to_header()` 方法。如果你计划子类化它并添加自己的项，请查看该类的源代码。

> **变更日志**
>
> 在 3.1 版本中更改：字典值始终为 `str | None`。设置属性会将值转换为字符串。将非布尔属性设置为 `False` 等同于将其设置为 `None`。获取类型化属性时，如果转换引发 `ValueError`，将返回 `None` 而不是字符串。
>
> 在 3.1 版本中更改：如果 `max_age` 存在但没有值，则为 `None`，而不是 `-1`。
>
> 在 3.1 版本中更改：`no_cache` 是布尔值，存在时为 `True`，而不是 `"*"`。
>
> 在 3.1 版本中更改：如果 `max_stale` 存在但没有值，则为 `True`，而不是 `"*"`。
>
> 在 3.1 版本中更改：`no_transform` 是布尔值。以前它被错误地始终设置为 `None`。
>
> 在 3.1 版本中更改：如果 `min_fresh` 存在但没有值，则为 `None`，而不是 `"*"`。
>
> 在 2.1 版本中更改：设置 `max_age` 等整数属性会将值转换为整数。
>
> 在 0.5 版本中新增：此请求类上不存在仅响应属性。

参数：

- `values`（`cabc.Mapping[str, t.Any] | cabc.Iterable[tuple[str, t.Any]] | None`）
- `on_update`（`cabc.Callable[[_CacheControl], None] | None`）

#### `cache_property()`

```py
static cache_property(key, empty, type, *, doc=None) → Any
```

返回缓存标头的新属性对象。如果要在子类中添加对缓存扩展的支持，则很有用。

参数：

- `key`（`str`）  
    解析后的 cache-control 标头字典中存在的属性名称。
- `empty`（`Any`）  
    如果键存在但没有值时使用的值。
- `type`（`type[Any] | None`）  
    将字符串值转换成的类型，而不是字符串。如果转换引发 `ValueError`，返回值为 `None`。
- `doc`（`str | None`）  
    属性的文档字符串。如果未给出，则根据其他参数生成。

返回类型：`Any`

> **变更日志**
>
> 在 3.1 版本中更改：新增 `doc` 参数。
>
> 在 2.0 版本中更改：从 `cache_property` 重命名。

#### `copy()`

```py
copy()
```

返回字典的浅拷贝。

#### `get()`

```py
get(key, default=None, /)
```

如果键在字典中，则返回键的值，否则返回默认值。

#### `items()`

```py
items()
```

返回提供字典项视图的类集合对象。

#### `keys()`

```py
keys()
```

返回提供字典键视图的类集合对象。

#### `to_header()`

```py
to_header() → str
```

将存储的值转换为缓存控制标头。

返回类型：`str`

#### `values()`

```py
values()
```

返回提供字典值视图的对象。

#### `max_age`

```py
property max_age
```

`max-age` 属性。一个 `int`，如果不存在则为 `None`。

#### `max_stale`

```py
property max_stale
```

`max-stale` 属性。一个 `int`，如果存在但没有值则为 `True`，如果不存在则为 `None`。

#### `min_fresh`

```py
property min_fresh
```

`min-fresh` 属性。一个 `int`，如果不存在则为 `None`。

#### `no_cache`

```py
property no_cache
```

`no-cache` 属性。一个 `bool`，存在或不存在。

#### `no_store`

```py
property no_store
```

`no-store` 属性。一个 `bool`，存在或不存在。

#### `no_transform`

```py
property no_transform
```

`no-transform` 属性。一个 `bool`，存在或不存在。

#### `only_if_cached`

```py
property only_if_cached
```

`only-if-cached` 属性。一个 `bool`，存在或不存在。

#### `stale_if_error`

```py
property stale_if_error
```

`stale-if-error` 属性。一个 `int`，如果不存在则为 `None`。

### ResponseCacheControl

```py
class werkzeug.datastructures.ResponseCacheControl(values=(), on_update=None)
```

响应的缓存控制。与 `RequestCacheControl` 不同，这是可变的，并提供对所有与响应相关的缓存控制标头的访问。

要再次获取 `ResponseCacheControl` 对象的标头，可以将对象转换为字符串或调用 `to_header()` 方法。如果你计划子类化它并添加自己的项，请查看该类的源代码。

> **变更日志**
>
> 在 3.1 版本中更改：字典值始终为 `str | None`。设置属性会将值转换为字符串。将非布尔属性设置为 `False` 等同于将其设置为 `None`。获取类型化属性时，如果转换引发 `ValueError`，将返回 `None` 而不是字符串。
>
> 在 3.1 版本中更改：如果 `no_cache` 存在但没有值，则为 `True`，而不是 `"*"`。
>
> 在 3.1 版本中更改：如果 `private` 存在但没有值，则为 `True`，而不是 `"*"`。
>
> 在 3.1 版本中更改：`no_transform` 是布尔值。以前它被错误地始终设置为 `None`。
>
> 在 3.1 版本中更改：新增 `must_understand`、`stale_while_revalidate` 和 `stale_if_error` 属性。
>
> 在 2.1.1 版本中更改：`s_maxage` 将值转换为整数。
>
> 在 2.1 版本中更改：设置 `max_age` 等整数属性会将值转换为整数。
>
> 在 0.5 版本中新增：此响应类上不存在仅请求属性。

参数：

- `values`（`cabc.Mapping[str, t.Any] | cabc.Iterable[tuple[str, t.Any]] | None`）
- `on_update`（`cabc.Callable[[_CacheControl], None] | None`）

#### `fromkeys()`

```py
classmethod fromkeys(iterable, value=None, /)
```

创建一个新字典，键来自 iterable，值设置为 value。

#### `cache_property()`

```py
static cache_property(key, empty, type, *, doc=None) → Any
```

返回缓存标头的新属性对象。如果要在子类中添加对缓存扩展的支持，则很有用。

参数：

- `key`（`str`）  
    解析后的 cache-control 标头字典中存在的属性名称。
- `empty`（`Any`）  
    如果键存在但没有值时使用的值。
- `type`（`type[Any] | None`）  
    将字符串值转换成的类型，而不是字符串。如果转换引发 `ValueError`，返回值为 `None`。
- `doc`（`str | None`）  
    属性的文档字符串。如果未给出，则根据其他参数生成。

返回类型：`Any`

> **变更日志**
>
> 在 3.1 版本中更改：新增 `doc` 参数。
>
> 在 2.0 版本中更改：从 `cache_property` 重命名。

#### `clear()`

```py
clear() → None
```

从字典中移除所有项。

返回类型：`None`

#### `copy()`

```py
copy()
```

返回字典的浅拷贝。

#### `get()`

```py
get(key, default=None, /)
```

如果键在字典中，则返回键的值，否则返回默认值。

#### `items()`

```py
items()
```

返回提供字典项视图的类集合对象。

#### `keys()`

```py
keys()
```

返回提供字典键视图的类集合对象。

#### `pop()`

```py
pop(k[, d]) → v, remove specified key and return the corresponding value.
```

如果未找到键，则返回给定的默认值；否则引发 KeyError。

参数：

- `self`（`te.Self`）
- `key`（`K`）
- `default`（`V | T`）

返回类型：`V | T`

#### `popitem()`

```py
popitem() → tuple[K, V]
```

移除并返回一个 (key, value) 对作为 2 元组。

对按 LIFO（后进先出）顺序返回。如果字典为空，则引发 KeyError。

返回类型：`tuple[K, V]`

#### `setdefault()`

```py
setdefault(key, default=None) → V
```

如果键不在字典中，则插入键，值为 default。

如果键在字典中，则返回键的值，否则返回默认值。

参数：

- `self`（`te.Self`）
- `key`（`K`）
- `default`（`V | None`）

返回类型：`V`

#### `to_header()`

```py
to_header() → str
```

将存储的值转换为缓存控制标头。

返回类型：`str`

#### `update()`

```py
update([E, ]**F) → None.  Update D from mapping/iterable E and F.
```

如果 E 存在且有 .keys() 方法，则执行： for k in E.keys(): D[k] = E[k]
如果 E 存在且缺少 .keys() 方法，则执行： for k, v in E: D[k] = v
在任一情况下，随后执行： for k in F:  D[k] = F[k]

参数：

- `arg`（`Mapping[K, V] | Iterable[tuple[K, V]] | None`）
- `kwargs`（`V`）

返回类型：`None`

#### `values()`

```py
values()
```

返回提供字典值视图的对象。

#### `immutable`

```py
property immutable
```

`immutable` 属性。一个 `bool`，存在或不存在。

#### `max_age`

```py
property max_age
```

`max-age` 属性。一个 `int`，如果不存在则为 `None`。

#### `must_revalidate`

```py
property must_revalidate
```

`must-revalidate` 属性。一个 `bool`，存在或不存在。

#### `must_understand`

```py
property must_understand
```

`must-understand` 属性。一个 `bool`，存在或不存在。

#### `no_cache`

```py
property no_cache
```

`no-cache` 属性。一个 `str`，如果存在但没有值则为 `True`，如果不存在则为 `None`。

#### `no_store`

```py
property no_store
```

`no-store` 属性。一个 `bool`，存在或不存在。

#### `no_transform`

```py
property no_transform
```

`no-transform` 属性。一个 `bool`，存在或不存在。

#### `private`

```py
property private
```

`private` 属性。一个 `str`，如果存在但没有值则为 `True`，如果不存在则为 `None`。

#### `proxy_revalidate`

```py
property proxy_revalidate
```

`proxy-revalidate` 属性。一个 `bool`，存在或不存在。

#### `public`

```py
property public
```

`public` 属性。一个 `bool`，存在或不存在。

#### `s_maxage`

```py
property s_maxage
```

`s-maxage` 属性。一个 `int`，如果不存在则为 `None`。

#### `stale_if_error`

```py
property stale_if_error
```

`stale-if-error` 属性。一个 `int`，如果不存在则为 `None`。

#### `stale_while_revalidate`

```py
property stale_while_revalidate
```

`stale-while-revalidate` 属性。一个 `int`，如果不存在则为 `None`。

### ETags

```py
class werkzeug.datastructures.ETags(strong_etags=None, weak_etags=None, star_tag=False)
```

一个集合，可用于检查一个 etag 是否存在于 etag 集合中。

参数：

- `strong_etags`（`cabc.Iterable[str] | None`）
- `weak_etags`（`cabc.Iterable[str] | None`）
- `star_tag`（`bool`）

#### `as_set()`

```py
as_set(include_weak=False) → set[str]
```

将 `ETags` 对象转换为 Python 集合。默认情况下，所有弱 etag 都不在此集合中。

参数：

- `include_weak`（`bool`）

返回类型：`set[str]`

#### `is_weak()`

```py
is_weak(etag) → bool
```

检查 etag 是否为弱。

参数：

- `etag`（`str`）

返回类型：`bool`

#### `is_strong()`

```py
is_strong(etag) → bool
```

检查 etag 是否为强。

参数：

- `etag`（`str`）

返回类型：`bool`

#### `contains_weak()`

```py
contains_weak(etag) → bool
```

检查 etag 是否属于包含弱和强标签的集合。

参数：

- `etag`（`str`）

返回类型：`bool`

#### `contains()`

```py
contains(etag) → bool
```

检查 etag 是否属于忽略弱标签的集合。也可以使用 `in` 运算符。

参数：

- `etag`（`str`）

返回类型：`bool`

#### `contains_raw()`

```py
contains_raw(etag) → bool
```

当传入带引号的标签时，它将检查此标签是否属于集合。如果标签是弱标签，则对照弱和强标签进行检查；否则仅对照强标签。

参数：

- `etag`（`str`）

返回类型：`bool`

#### `to_header()`

```py
to_header() → str
```

将 etags 集合转换为 HTTP 标头字符串。

返回类型：`str`

### Authorization

```py
class werkzeug.datastructures.Authorization(auth_type, data=None, token=None)
```

表示 `Authorization` 请求标头的各部分。

如果设置了标头，`Request.authorization` 返回一个实例。

实例可用于测试 `Client` 请求方法的 `auth` 参数，以在测试请求中发送标头。

根据认证方案，将设置 `parameters` 或 `token` 之一。`Basic` 方案的令牌会解码为 `username` 和 `password` 参数。

为方便起见，`auth["key"]` 和 `auth.key` 都访问 `parameters` 字典中的键，还有 `auth.get("key")` 和 `"key" in auth`。

> **变更日志**
>
> 在 2.3 版本中更改：新增 `token` 参数和属性，以支持使用令牌而不是参数的认证方案，例如 `Bearer`。
>
> 在 2.3 版本中更改：对象不再是 `dict`。
>
> 在 0.5 版本中更改：对象是不可变字典。

参数：

- `auth_type`（`str`）
- `data`（`dict[str, str | None] | None`）
- `token`（`str | None`）

#### `type`

```py
type
```

授权方案，如 `basic`、`digest` 或 `bearer`。

#### `parameters`

```py
parameters
```

从标头解析的参数字典。对于给定方案，此属性或 `token` 之一将有一个值。

#### `token`

```py
token
```

从标头解析的令牌。对于给定方案，此属性或 `parameters` 之一将有一个值。

> **变更日志**
>
> 在 2.3 版本中新增。

#### `from_header()`

```py
classmethod from_header(value) → te.Self | None
```

解析 `Authorization` 标头值并返回一个实例，如果值为空则返回 `None`。

参数：

- `value`（`str | None`）  
    要解析的标头值。

返回类型：`te.Self | None`

> **变更日志**
>
> 在 2.3 版本中新增。

#### `to_header()`

```py
to_header() → str
```

生成表示此数据的 `Authorization` 标头值。

> **变更日志**
>
> 在 2.0 版本中新增。

返回类型：`str`

### WWWAuthenticate

```py
class werkzeug.datastructures.WWWAuthenticate(auth_type, values=None, token=None)
```

表示 `WWW-Authenticate` 响应标头的各部分。

将 `Response.www_authenticate` 设置为实例或实例列表，以在响应中为此标头设置值。修改此实例将修改标头值。

根据认证方案，应设置 `parameters` 或 `token` 之一。`Basic` 方案会将 `username` 和 `password` 参数编码为令牌。

为方便起见，`auth["key"]` 和 `auth.key` 都作用于 `parameters` 字典，可用于获取、设置或删除参数。还提供了 `auth.get("key")` 和 `"key" in auth`。

> **变更日志**
>
> 在 2.3 版本中更改：新增 `token` 参数和属性，以支持使用令牌而不是参数的认证方案，例如 `Bearer`。
>
> 在 2.3 版本中更改：对象不再是 `dict`。
>
> 在 2.3 版本中更改：移除 `on_update` 参数。

参数：

- `auth_type`（`str`）
- `values`（`dict[str, str | None] | None`）
- `token`（`str | None`）

#### `type`

```py
property type: str
```

授权方案，如 `basic`、`digest` 或 `bearer`。

#### `parameters`

```py
property parameters: dict[str, str | None]
```

标头的参数字典。对于给定方案，此属性或 `token` 之一应有一个值。

#### `token`

```py
property token: str | None
```

标头的参数字典。对于给定方案，此属性或 `token` 之一应有一个值。

#### `from_header()`

```py
classmethod from_header(value) → te.Self | None
```

解析 `WWW-Authenticate` 标头值并返回一个实例，如果值为空则返回 `None`。

参数：

- `value`（`str | None`）  
    要解析的标头值。

返回类型：`te.Self | None`

> **变更日志**
>
> 在 2.3 版本中新增。

#### `to_header()`

```py
to_header() → str
```

生成表示此数据的 `WWW-Authenticate` 标头值。

返回类型：`str`

### IfRange

```py
class werkzeug.datastructures.IfRange(etag=None, date=None)
```

表示解析形式的 `If-Range` 标头的非常简单的对象。它将要么没有 etag 或日期，要么有其中之一但绝不会同时有两个。

> **变更日志**
>
> 在 0.7 版本中新增。

参数：

- `etag`（`str | None`）
- `date`（`datetime | None`）

#### `etag`

```py
etag
```

解析并去掉引号的 etag。范围始终基于强 etag，因此不需要弱信息。

#### `date`

```py
date
```

解析格式的日期或 `None`。

#### `to_header()`

```py
to_header() → str
```

将对象转换回 HTTP 标头。

返回类型：`str`

### Range

```py
class werkzeug.datastructures.Range(units, ranges)
```

表示 `Range` 标头。所有方法仅支持 `bytes` 作为单位。如果给定，存储范围列表，但仅在只提供一个范围时方法才有效。

引发：`ValueError` – 如果提供的范围无效。

参数：

- `units`（`str`）
- `ranges`（`cabc.Sequence[tuple[int, int | None]]`）

> **变更日志**
>
> 在 0.15 版本中更改：验证传入的范围。
>
> 在 0.7 版本中新增。

#### `units`

```py
units
```

此范围的单位。通常是 `"bytes"`。

#### `ranges`

```py
ranges
```

提供的范围标头的 `(begin, end)` 元组列表。范围是非包含的。

#### `range_for_length()`

```py
range_for_length(length) → tuple[int, int] | None
```

如果范围是针对字节的，长度不为 None，并且恰好有一个范围且可满足，则返回一个 `(start, stop)` 元组，否则返回 `None`。

参数：

- `length`（`int | None`）

返回类型：`tuple[int, int] | None`

#### `make_content_range()`

```py
make_content_range(length) → ContentRange | None
```

从当前范围和给定内容长度创建 `ContentRange` 对象。

参数：

- `length`（`int | None`）

返回类型：`ContentRange | None`

#### `to_header()`

```py
to_header() → str
```

将对象转换回 HTTP 标头。

返回类型：`str`

#### `to_content_range_header()`

```py
to_content_range_header(length) → str | None
```

基于给定长度将对象转换为 `Content-Range` HTTP 标头。

参数：

- `length`（`int | None`）

返回类型：`str | None`

### ContentRange

```py
class werkzeug.datastructures.ContentRange(units, start, stop, length=None, on_update=None)
```

表示内容范围标头。

> **变更日志**
>
> 在 0.7 版本中新增。

参数：

- `units`（`str | None`）
- `start`（`int | None`）
- `stop`（`int | None`）
- `length`（`int | None`）
- `on_update`（`cabc.Callable[[ContentRange], None] | None`）

#### `units`

```py
units: str | None
```

要使用的单位，通常是 `"bytes"`。

#### `start`

```py
start: int | None
```

范围的起点或 `None`。

#### `stop`

```py
stop: int | None
```

范围的终点（非包含）或 `None`。仅当 start 也为 `None` 时才可为 `None`。

#### `length`

```py
length: int | None
```

范围的长度或 `None`。

#### `set()`

```py
set(start, stop, length=None, units='bytes') → None
```

更新范围的简单方法。

参数：

- `start`（`int | None`）
- `stop`（`int | None`）
- `length`（`int | None`）
- `units`（`str | None`）

返回类型：`None`

#### `unset()`

```py
unset() → None
```

将单位设置为 `None`，表示不再使用该标头。

返回类型：`None`