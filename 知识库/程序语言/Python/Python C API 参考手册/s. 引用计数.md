https://docs.python.org/zh-cn/3.15/c-api/refcounting.html

# 引用计数

本节介绍的函数和宏被用于管理 Python 对象的引用计数。

## PyObject *Py_NewRef()

```py
PyObject *Py_NewRef(PyObject *o)
```

为对象创建一个新的 `strong reference`: 在 `o` 上调用 `Py_INCREF()` 并返回对象 `o`。

当不再需要这个 `strong reference` 时，应当在其上调用 `Py_DECREF()` 来释放引用。