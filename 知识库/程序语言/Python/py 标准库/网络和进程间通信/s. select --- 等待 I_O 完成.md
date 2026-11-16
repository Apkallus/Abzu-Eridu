https://docs.python.org/zh-cn/3/library/select.html

# select --- 等待 I/O 完成

该模块提供了对 `select()` 和 `poll()` 函数的访问，这在大多数操作系统上都是可用的。

```py
# 读取标准输入，直到输入退出键 `q` 
while True:
    if select.select([0], [], [], 0)[0]:
        key = os.read(0, 64)
        if b'q' in key:
            break
```

## select.select()

```py
select.select(rlist, wlist, xlist, timeout=None)
```

Unix `select()` 系统调用接口。输入文件描述符列表

- `rlist`   
    等待，直到可以开始读取

- `wlist`  
    等待，直到可以开始写入

- `xlist`  
    等待“异常情况”（请参阅当前系统的手册，以获取哪些情况称为异常情况）

- `timeout`  
    默认阻塞轮询，为零则永不阻塞

返回值是三个列表，包含已就绪对象，返回的三个列表是前三个参数的子集。当超时时间已到且没有文件描述符就绪时，返回三个空列表。