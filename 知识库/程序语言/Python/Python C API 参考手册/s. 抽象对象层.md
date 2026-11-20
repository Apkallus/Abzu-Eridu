https://docs.python.org/zh-cn/3/c-api/sequence.html

# 序列协议

## PyObject *PySequence_Fast()

```py
PyObject *PySequence_Fast(PyObject *o, const char *m)
```

作为 CPython 的实现细节，如果 `o` 已经是一个序列或列表，它将被直接返回。