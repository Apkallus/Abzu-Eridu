# pathlib --- 面向对象的文件系统路径

https://docs.python.org/zh-cn/3.15/library/pathlib.html

该模块提供表示文件系统路径的类，其语义适用于不同的操作系统。路径类被分为提供纯计算操作而没有 I/O 的 [纯路径]，以及从纯路径继承而来但提供 I/O 操作的 [具体路径]。


## 纯路径

纯路径对象提供了不实际访问文件系统的路径处理操作。有三种方式来访问这些类，也是不同的风格：

#### 🎯 class pathlib.PurePath()

```py
class pathlib.PurePath(*pathsegments)
```

一个通用的类，代表当前系统的路径风格 (实例化为 [PurePosixPath] 或者 [PureWindowsPath]):

> 如果某个段为绝对路径，则其前面的所有段都会被忽略 (类似 `os.path.join()`):

```py
PurePath('/etc', '/usr', 'lib64')
# PurePosixPath('/usr/lib64')
PureWindowsPath('c:/Windows', 'd:bar')
# PureWindowsPath('d:bar')
```

### 方法和特征属性

#### 🎯 `PurePath.joinpath()`

```py
PurePath.joinpath(*pathsegments)
```

调用此方法等同于依次将路径与给定的每个 `pathsegments` 组合到一起

> 与 `PurePath` 拥有相同行为：最后一个参数设置绝对路径以消除前缀