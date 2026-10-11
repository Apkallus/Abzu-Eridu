https://docs.python.org/zh-cn/3.14/library/hashlib.html

# hashlib --- 安全哈希与消息摘要

## 哈希算法

每种类型的 `hash` 都有一个构造器方法。它们都返回一个具有相同简单接口的哈希对象。例如，使用 `sha256()` 创建一个 SHA-256 哈希对象。你可以使用 `update` 方法向这个对象输入 字节类对象 (通常是 `bytes`)。在任何时候你都可以使用 `digest()` 或 `hexdigest()` 方法获得到目前为止输入这个对象的拼接数据的 `digest`。

为了允许多线程，当在其构造器或 `.update` 方法中计算一次性提供超过 2047 字节数据的哈希时将会释放 Python `GIL`.


## 哈希对象

下列值会以构造器所返回的哈希对象的常量属性的形式被提供：

- `hash.digest_size`：以字节表示的结果哈希对象的大小。
- `hash.block_size`：以字节表示的哈希算法的内部块大小。

`hash` 对象具有以下属性：

- `hash.name`：此哈希对象的规范名称，总是为小写形式并且总是可以作为 `[new()]` 的形参用来创建另一个此类型的哈希对象。

    在 3.4 版本发生变更: `name` 属性自被引入起即存在于 CPython 中，但在 Python 3.4 之前并未正式指明，因此可能不存在于某些平台上。

`hash` 对象具有下列方法：

### hash.update(data)

```python
hash.update(data)
```
用 `[bytes-like object]` 来更新哈希对象。 重复调用相当于单次调用并传入所有参数的拼接结果: `m.update(a); m.update(b)` 等价于 `m.update(a+b)`。

### hash.digest()

```python
hash.digest()
```
返回当前已传给 `[update()]` 方法的数据摘要。这是一个大小为 `[digest_size]` 的字节串对象，字节串中可包含 0 至 255 的完整取值范围。

### hash.hexdigest()

```python
hash.hexdigest()
```
类似于 `[digest()]` 但摘要会以两倍长度字符串对象的形式返回，其中仅包含十六进制数码。 这可以被用于在电子邮件或其他非二进制环境中安全地交换数据值。

### hash.copy()

```python
hash.copy()
```
返回哈希对象的副本（“克隆”）。这可被用来高效地计算共享相同初始子串的数据的摘要。