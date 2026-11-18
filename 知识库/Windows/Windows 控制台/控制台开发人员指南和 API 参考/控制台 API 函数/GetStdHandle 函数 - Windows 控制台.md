https://learn.microsoft.com/en-us/windows/console/getstdhandle

# GetStdHandle 函数 - Windows 控制台 | Microsoft Learn

检索指定标准设备（标准输入、标准输出或标准错误）的句柄。

## 语法

```C
HANDLE WINAPI GetStdHandle(
  _In_ DWORD nStdHandle
);
```

## 参数

*nStdHandle* [in]  
标准设备。此参数可以是以下值之一。

| 值 | 含义 |
| --- | --- |
| `STD_INPUT_HANDLE`（`((DWORD)-10)`） | 标准输入设备。初始情况下，这是控制台输入缓冲区 `CONIN$`。 |
| `STD_OUTPUT_HANDLE`（`((DWORD)-11)`） | 标准输出设备。初始情况下，这是活动控制台屏幕缓冲区 `CONOUT$`。 |
| `STD_ERROR_HANDLE`（`((DWORD)-12)`） | 标准错误设备。初始情况下，这是活动控制台屏幕缓冲区 `CONOUT$`。 |

> **注意**
>
> 这些常量的值是无符号数，但在头文件中被定义为有符号数的强制转换，并利用 C 编译器将其回绕到略低于 32 位最大值的值。在不会解析头文件并重新定义这些常量的语言中与这些句柄交互时，请注意这一约束。例如，`((DWORD)-10)` 实际上是无符号数 `4294967286`。

## 返回值

如果函数成功，返回值是指定设备的句柄，或由先前调用 `SetStdHandle` 设置的重定向句柄。除非应用程序已使用 `SetStdHandle` 设置了访问权限更小的标准句柄，否则该句柄具有 `GENERIC_READ` 和 `GENERIC_WRITE` 访问权限。

> **提示**
>
> 使用完此句柄后，不需要用 `CloseHandle` 释放它。有关详细信息，请参阅“备注”。

如果函数失败，返回值为 `INVALID_HANDLE_VALUE`。要获取扩展错误信息，请调用 `GetLastError`。

如果应用程序没有关联的标准句柄（例如在交互式桌面上运行的服务），并且未重定向这些句柄，则返回值为 `NULL`。

## 备注

需要从控制台读取或向控制台写入的应用程序可以使用 `GetStdHandle` 返回的句柄。创建控制台时，标准输入句柄是控制台输入缓冲区的句柄，标准输出和标准错误句柄是控制台活动屏幕缓冲区的句柄。这些句柄可由 `ReadFile` 和 `WriteFile` 函数使用，也可由任何访问控制台输入缓冲区或屏幕缓冲区的控制台函数使用（例如 `ReadConsoleInput`、`WriteConsole` 或 `GetConsoleScreenBufferInfo` 函数）。

进程的标准句柄可以通过调用 `SetStdHandle` 重定向，此时 `GetStdHandle` 返回重定向后的句柄。如果标准句柄已被重定向，可以在调用 `CreateFile` 函数时指定 `CONIN$` 值，以获取控制台输入缓冲区的句柄。类似地，可以指定 `CONOUT$` 值，以获取控制台活动屏幕缓冲区的句柄。

进程在进入 `main` 方法时的标准句柄，由构建应用程序时传递给链接器的 `/SUBSYSTEM` 标志配置决定。指定 `/SUBSYSTEM:CONSOLE` 会请求操作系统在启动时用控制台会话填充这些句柄，前提是父进程尚未通过继承填充标准句柄表。相反，`/SUBSYSTEM:WINDOWS` 意味着应用程序不需要控制台，并且很可能不会使用标准句柄。有关句柄继承的详细信息，请参阅 `STARTF_USESTDHANDLES` 的文档。

某些应用程序会在其声明子系统的边界之外运行；例如，`/SUBSYSTEM:WINDOWS` 应用程序可能会为了日志记录或调试目的检查/使用标准句柄，但正常以图形用户界面运行。这些应用程序需要在启动时仔细探查标准句柄的状态，并在需要时使用 `AttachConsole`、`AllocConsole` 和 `FreeConsole` 来添加/移除控制台。

某些应用程序还可能根据继承句柄的类型改变其行为。可以使用 `GetFileType` 区分控制台、管道、文件及其他类型。

### 句柄释放

使用 `GetStdHandle` 检索到的句柄后，不需要调用 `CloseHandle`。返回值只是进程表中存储的值的副本。进程本身通常被视为这些句柄及其生命周期的所有者。每个句柄在创建时根据 `CreateProcess` 调用的继承和启动具体情况放入表中，并在进程销毁时释放。

如果应用程序有意替换这些句柄或阻止进程的其他部分使用它们，则可能需要手动操作这些句柄的生命周期。由于运行中的代码可能会缓存 `HANDLE`，因此该代码不一定会拾取通过 `SetStdHandle` 所做的更改。通过 `CloseHandle` 显式关闭句柄会在整个进程范围内关闭它，任何缓存引用的下一次使用都会遇到错误。

替换进程表中标准句柄的指导原则是：使用 `GetStdHandle` 从表中获取现有 `HANDLE`，使用 `SetStdHandle` 放入一个通过 `CreateFile`（或类似函数）打开的新 `HANDLE`，然后关闭检索到的句柄。

`GetStdHandle` 或 `SetStdHandle` 函数都不会验证进程表中存储为句柄的值。验证会在实际读/写操作（例如 `ReadFile` 或 `WriteFile`）时执行。

### 附加/分离行为

附加到新控制台时，标准句柄始终会被替换为控制台句柄，除非在进程创建期间指定了 `STARTF_USESTDHANDLES`。

如果标准句柄的现有值为 `NULL`，或现有值看起来像控制台伪句柄，则该句柄会被替换为控制台句柄。

当父进程同时使用 `CREATE_NEW_CONSOLE` 和 `STARTF_USESTDHANDLES` 创建控制台进程时，除非标准句柄的现有值为 `NULL` 或控制台伪句柄，否则标准句柄不会被替换。

> **注意**
>
> 控制台进程*必须*在启动时填充标准句柄，否则系统会自动用新控制台的适当句柄填充它们。图形用户界面（GUI）应用程序可以在没有标准句柄的情况下启动，并且不会自动填充。

## 示例

有关示例，请参阅 Reading Input Buffer Events。

## 要求

| - | - |
| --- | --- |
| 最低支持的客户端 | Windows 2000 Professional [仅桌面应用] |
| 最低支持的服务器 | Windows 2000 Server [仅桌面应用] |
| 头文件 | ProcessEnv.h（通过 Winbase.h，包含 Windows.h） |
| 库 | Kernel32.lib |
| DLL | Kernel32.dll |