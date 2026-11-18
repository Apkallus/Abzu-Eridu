https://learn.microsoft.com/zh-cn/windows/console/console-functions

# 控制台 API 函数

## ReadConsoleInput 函数

https://learn.microsoft.com/zh-cn/windows/console/readconsoleinput

从控制台输入缓冲区读取数据，并将其从缓冲区删除。

```C
BOOL WINAPI ReadConsoleInput(
  _In_  HANDLE        hConsoleInput,
  _Out_ PINPUT_RECORD lpBuffer,
  _In_  DWORD         nLength,
  _Out_ LPDWORD       lpNumberOfEventsRead
);
```

### 参数

`hConsoleInput` [in] 
    控制台输入缓冲区的句柄。 该句柄必须具有 `GENERIC_READ` 访问权限。 有关详细信息，请参阅"控制台缓冲区安全性和访问权限"

`lpBuffer` [out]  
    指针 – 指向接收输入缓冲区数据的 `INPUT_RECORD` 结构数组。

`nLength` [in] 
    *lpBuffer* 参数指向的数组大小（以数组元素表示）。

`lpNumberOfEventsRead` [out]  
    指针 – 指向接收所读取输入记录数量的变量。

### 返回值

如果该函数成功，则返回值为非零值。

如果函数失败，则返回值为零。 要获得更多的“错误信息”

### 注解

如果 `nLength` 参数中请求的记录数超过缓冲区中可用的记录数，则读取可用的记录数。 在读取至少一条输入记录之前，该函数不会返回值。

进程可以在其中一个“等待函数”中指定控制台输入缓冲区句柄，以确定何时存在未读控制台输入。 当输入缓冲区不为空时，将发出控制台输入缓冲区句柄的状态信号。



## GetStdHandle 函数 

检索指定标准设备（标准输入、标准输出或标准错误）的句柄。

### 语法

```C
HANDLE WINAPI GetStdHandle(
  _In_ DWORD nStdHandle
);
```

### 参数

`nStdHandle` [in]  
标准设备。此参数可以是以下值之一。

- `STD_INPUT_HANDLE`（`((DWORD)-10)`） 
    标准输入设备。初始情况下，这是控制台输入缓冲区 `CONIN$`。 
- `STD_OUTPUT_HANDLE`（`((DWORD)-11)`）  
    标准输出设备。初始情况下，这是活动控制台屏幕缓冲区 `CONOUT$`。 
- `STD_ERROR_HANDLE`（`((DWORD)-12)`）  
    标准错误设备。初始情况下，这是活动控制台屏幕缓冲区 `CONOUT$`。 

> **注意**
>
> 这些常量的值是无符号数，但在头文件中被定义为有符号数的强制转换，并利用 C 编译器将其回绕到略低于 32 位最大值的值。在不会解析头文件并重新定义这些常量的语言中与这些句柄交互时，请注意这一约束。例如，`((DWORD)-10)` 实际上是无符号数 `4294967286`。

### 返回值

如果函数成功，返回值是指定设备的句柄，或由先前调用 `SetStdHandle` 设置的重定向句柄。除非应用程序已使用 `SetStdHandle` 设置了访问权限更小的标准句柄，否则该句柄具有 `GENERIC_READ` 和 `GENERIC_WRITE` 访问权限。

> **提示**
>
> 使用完此句柄后，不需要用 `CloseHandle` 释放它。有关详细信息，请参阅“备注”。

如果函数失败，返回值为 `INVALID_HANDLE_VALUE`。要获取扩展错误信息，请调用 `GetLastError`。

如果应用程序没有关联的标准句柄（例如在交互式桌面上运行的服务），并且未重定向这些句柄，则返回值为 `NULL`。