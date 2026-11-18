https://learn.microsoft.com/zh-cn/windows/win32/api/synchapi/

## WaitForSingleObject 函数 （synchapi.h）

https://learn.microsoft.com/zh-cn/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject

等待指定的对象处于信号状态或超时。

若要进入可警报的等待状态，请使用 [WaitForSingleObjectEx] 函数。 若要等待多个对象，请使用 [WaitForMultipleObjects]。

### 语法

```cpp
DWORD WaitForSingleObject(
  [in] HANDLE hHandle,
  [in] DWORD  dwMilliseconds
);
```

### 参数

`[in] hHandle`

对象的句柄。 有关可以指定句柄的对象类型的列表，请参阅以下“备注”部分。

如果在等待仍在挂起时关闭此句柄，则函数的行为是未定义的。

句柄必须具有 **SYNCHRONIZE** 访问权限。 有关详细信息，请参阅 [标准访问权限]。

`[in] dwMilliseconds`

超时间隔（以毫秒为单位）。 如果指定了非零值，函数将等待对象发出信号或间隔。 如果 *dwMilliseconds* 为零，则函数不会在对象未发出信号时进入等待状态;它始终会立即返回。 如果 *dwMilliseconds***INFINITE**，则仅当发出对象信号时，函数才会返回。

**Windows XP、Windows Server 2003、Windows Vista、Windows 7、Windows Server 2008 和 Windows Server 2008 R2：***dwMilliseconds* 值确实包括用于低功率状态的时间。 例如，当计算机处于睡眠状态时，超时确实会不断倒计时。

**Windows 8 及更新版本、Windows Server 2012 及更新版本：***dwMilliseconds* 值不包括在低功率状态下花费的时间。 例如，当计算机处于睡眠状态时，超时不会不断倒计时。

### 返回值

如果函数成功，则返回值指示导致函数返回的事件。 它可以是以下值之一。


- `WAIT_OBJECT_0` `0x00000000L`  
	指定对象的状态已发出信号。 

- `WAIT_TIMEOUT` `0x00000102L`  
    超时，并且对象的状态不对齐。 

