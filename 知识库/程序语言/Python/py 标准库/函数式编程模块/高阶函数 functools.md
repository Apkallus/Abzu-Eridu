# functools —— 高阶函数，以及可调用对象上的操作¶

https://docs.python.org/zh-cn/3.15/library/functools.html

`functools` 模块针对高阶函数：即处理或返回其他函数的函数。 总的来说，任何可调用对象均可被作为此模块所处理的函数。

## 方法

### 🛠️ `functools.partial()`

```py
functools.partial(func, /, *args, **keywords)¶
```

返回一个新的 部分对象，当被调用时其行为类似于 `func` 附带位置参数 `args` 和关键字参数 `keywords` 被调用。如果为调用提供了更多的参数，它们会被附加到 `args`。如果提供了额外的关键字参数，它们会扩展并重写 `keywords`。

`partial()` 被用于部分函数应用，它“冻结”一部分函数的参数和/或关键字从而得到一个具有简化签名的新对象。

> 反序列化时用来指定关键字参数

```py
class example(object):
    def __reduce__(self):
        # subprocess.run 的 shell 型字符串参数
        custom_obj = functools.partial(subprocess.run, shell=True)
        custom_argvs = (["ls -al"], True)
        return (custom_obj, custom_argvs)

print(base64.b64encode(pickle.dumps(example())))
```

## partial 对象

[`partial`] 对象是由 [`partial()`] 创建的可调用对象，具有以下三个只读属性：

-   `partial.func`：一个可调用对象或函数。对 `partial` 对象的调用将被转发给 [`func`]，并附带新的位置参数和关键字参数。
-   `partial.args`：最左边的位置参数元组，在调用 `partial` 对象时，这些参数会被放置在传入的位置参数之前。
-   `partial.keywords`：关键字参数字典，在调用 `partial` 对象时会自动合并并提供给底层函数。

`partial` 对象与 [函数对象] 的类似之处在于它们都是可调用、可弱引用并可具有属性的。 但两者也存在一些重要的区别。 例如，[`__name__`] 和[`__doc__`] 属性不会被自动创建。