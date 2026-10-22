# os.path --- 常用的路径操作

https://docs.python.org/zh-cn/3.15/library/os.path.html

此模块实现了一些有用的路径名称相关函数。传给 path 形参的可以是字符串、字节串或者任何实现了 [`os.PathLike`] 协议的对象。

与 Unix 不同，Python 不会执行任何 *自动* 路径扩展。 

## 🎯 `os.path.join()` —— 合并路径片段

```py
os.path.join(path, /, *paths)
```

智能地合并一个或多个路径片段。

如果一个片段为绝对路径（在 Windows 需要有驱动器号和根目录），则之前的所有片段都会被忽略并且合并将在该绝对路径上继续进行。 

```py
os.path.join('/home/foo', 'bar')
# '/home/foo/bar'

os.path.join('/home/foo', '/bar')
# '/bar'
```

> 最后一个参数设置绝对路径以消除前缀