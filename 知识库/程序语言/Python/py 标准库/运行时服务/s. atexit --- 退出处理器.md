https://docs.python.org/zh-cn/3/library/atexit.html

# atexit --- 退出处理器

`atexit` 模块定义了用于注册和取消注册 “退出处理器” 的函数

## atexit.register(func, *args, **kwargs)

```py
atexit.register(func, *args, **kwargs)
```

将函数注册为退出处理器

这个函数返回 `func` 对象，可以把它当作装饰器使用。

参数型：

```py
def goodbye(name, adjective):
    print('Goodbye %s, it was %s to meet you.' % (name, adjective))

import atexit

atexit.register(goodbye, 'Donny', 'nice')
# 或者：
atexit.register(goodbye, adjective='nice', name='Donny')
```

装饰器型：

```py
import atexit

@atexit.register
def goodbye():
    print('You are now leaving the Python sector.')
```