https://docs.python.org/zh-cn/3/library/msvcrt.html

# msvcrt --- 来自 MS VC++ 运行时的有用例程

这些函数提供了对 Windows 平台上某些有用功能的访问。

该模块实现了控制台 I/O API 的普通和宽字符变体。


```py
# kbhit 非阻塞等待读取按键，getwch 在按键事件发生时读取按键
QUIT_KEY = b'q'

def getch():
    key = None
    if msvcrt.kbhit():
        key = msvcrt.getwch().encode()
    return key

while True:
    key = getch() 
    # 若收到键盘 `q` 则退出
    if key and QUIT_KEY in key:
        break
```

## 控制台 I/O

### msvcrt.kbhit()

```py
msvcrt.kbhit()
```

如果正在等待读取一个按键则返回一个非零值。 在其他情况下，将返回 0。

### msvcrt.getch()

```py
msvcrt.getch()
```

读取一个按键并将结果字符以字节串形式返回。 不会回显到控制台。 

### msvcrt.getwch()

```py
msvcrt.getwch()
```

`getch()` 的宽字符版本，返回一个 Unicode 值。
