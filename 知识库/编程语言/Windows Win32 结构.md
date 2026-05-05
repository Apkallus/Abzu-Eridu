
## LARGE_INTEGER union (winnt.h)- 表示 64 位带符号整数值

```c++
typedef union _LARGE_INTEGER {
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } DUMMYSTRUCTNAME;
  struct {
    DWORD LowPart;
    LONG  HighPart;
  } u;
  LONGLONG QuadPart;
} LARGE_INTEGER;
```

**注解**
LARGE_INTEGER结构实际上是一个联合。 如果编译器具有对 64 位整数的内置支持，请使用 QuadPart 成员来存储 64 位整数。 否则，请使用 LowPart 和 HighPart 成员来存储 64 位整数。

## UNICODE_STRING 结构 (ntdef.h) - UNICODE_STRING 结构用于定义 Unicode 字符串

https://learn.microsoft.com/zh-cn/windows/win32/api/ntdef/ns-ntdef-_unicode_string

```c++
typedef struct _UNICODE_STRING {
  USHORT Length;
  USHORT MaximumLength;
  PWSTR  Buffer;
} UNICODE_STRING, *PUNICODE_STRING;
```

tips:
- 使用 `RtlInitUnicodeString` 或 `RtlInitUnicodeStringEx` 进行初始化