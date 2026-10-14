# Win32

<https://learn.microsoft.com/zh-cn/windows/win32/api>

[数据类型](https://learn.microsoft.com/en-us/windows/win32/winprog/windows-data-types)
- `LPCSTR` 指向 C 字符串(CSTR)的长指针(LP)
- `HANDLE` 引用内核资源

[各版本系统调用编号](https://github.com/j00ru/windows-syscalls)

[句柄与对象](https://learn.microsoft.com/en-us/windows/win32/sysinfo/handles-and-objects)

[x64 调用约定](https://learn.microsoft.com/zh-cn/cpp/build/x64-calling-convention?view=msvc-180)
- 整数参数在寄存器 RCX、RDX、R8 和 R9 中传递，第 5 个和更高位置的参数在堆栈上传递。
- 影子参数栈空间约定：调用者将参数5保存在 ret+0x20 处，而 +0x0~+0x20 的4个槽位由被调用者放入参数1~4
    - 即使参数不满5个仍使用一致的约定
- 64 位的标量返回值通过 RAX 返回，非标量类型在XMM0中返回
- 使用者保存：寄存器 RBX、RBP、RDI、RSI、RSP、R12、R13、R14、R15 和 XMM6-XMM15 视为非易失性。

## CreateFileA 函数 （fileapi.h） - 创建或打开文件或 I/O 设备

```c++
HANDLE CreateFileA(
  [in]           LPCSTR                lpFileName,
  [in]           DWORD                 dwDesiredAccess,
  [in]           DWORD                 dwShareMode,
  [in, optional] LPSECURITY_ATTRIBUTES lpSecurityAttributes,
  [in]           DWORD                 dwCreationDisposition,
  [in]           DWORD                 dwFlagsAndAttributes,
  [in, optional] HANDLE                hTemplateFile
);
```

- `[in] lpFileName`
    要创建或打开的文件或设备的名称。 可以在此名称中使用正斜杠 （/） 或反斜杠 （\）。

- `[in] dwDesiredAccess`
    请求对文件或设备的访问权限，可以汇总为读取、写入或 0，以指示两者均未提供）。

- `[in] dwShareMode`
    请求的文件或设备的共享模式，可以读取、写入、删除、所有这些或无（请参阅下表）。 

- `[in, optional] lpSecurityAttributes`
    指向包含两个独立但相关数据成员的 SECURITY_ATTRIBUTES 结构的指针：可选的安全描述符，以及一个布尔值，该值确定是否可由子进程继承返回的句柄。

    此参数可以 NULL。

- `[in] dwCreationDisposition`
    对存在或不存在的文件或设备执行的操作。

    对于文件以外的设备，此参数通常设置为 OPEN_EXISTING 3 仅当文件或设备存在时才打开该文件或设备。

    - CREATE_NEW 1
        仅当该文件尚不存在时，才会创建一个新文件。
    - CREATE_ALWAYS 2
        总是创建新文件。

- `[in] dwFlagsAndAttributes`
    文件或设备属性和标志，FILE_ATTRIBUTE_NORMAL 是文件最常见的默认值。

- `[in, optional] hTemplateFile`
    具有 GENERIC_READ 访问权限的模板文件的有效句柄。 模板文件为正在创建的文件提供文件属性和扩展属性。

    此参数可以 NULL。

    打开现有文件时，CreateFile 忽略此参数。

```asm
; CreateFileA("\\.\pipe\LOCAL\FlagPipe", 0x10000000, 0, nullptr,      OPEN_EXISTING, SECURITY_ANONYMOUS, nullptr)
; rcx 文件路径
; rdx 权限，所有权限 0x10000000
; r8 共享模型，0x0
; r9 安全指针，NULL
; rsp+0x20 操作，OPEN_EXISTING 存在时打开 
; rsp+0x28 属性，SECURITY_ANONYMOUS 在匿名模拟级别模拟客户端
; rsp+0x30 扩展，NULL

f"""
_start:
    lea rcx, [rip+file_path]
    mov edx, 0x10000000
    xor r8, r8
    xor r9, r9
    sub rsp, 0x38
    mov qword ptr [rsp+0x20], 3
    mov qword ptr [rsp+0x28], 0x80
    mov qword ptr [rsp+0x30], 0
    call [rip + CreateFileA_addr]
    add rsp, 0x38

file_path:
    .asciz "\\\\\\\\.\\\\pipe\\\\LOCAL\\\\FlagPipe"

CreateFileA_addr:
    .quad {CreateFileA_addr:#x}
"""
```

## ReadFile 函数 （fileapi.h）- 从指定的文件或输入/输出（I/O）设备读取数据

```c++
BOOL ReadFile(
  [in]                HANDLE       handle_value,
  [out]               LPVOID       lpBuffer,
  [in]                DWORD        nNumberOfBytesToRead,
  [out, optional]     LPDWORD      lpNumberOfBytesRead,
  [in, out, optional] LPOVERLAPPED lpOverlapped
);
```

- `[in] handle_value`
    设备的句柄。

    必须使用读取访问权限创建 handle_value 参数。 

- `[out] lpBuffer`
    指向接收从文件或设备读取的数据的缓冲区的指针。

- `[in] nNumberOfBytesToRead`
    要读取的最大字节数。

- `[out, optional] lpNumberOfBytesRead`
    指向使用同步 handle_value 参数时接收读取的字节数的变量的指针。 ReadFile 在执行任何工作或错误检查之前将此值设置为零。 如果这是一个异步操作，请对此参数使用 NULL 以避免潜在的错误结果。

    仅当 lpOverlapped 参数不 NULL时，此参数才能 NULL。

- `[in, out, optional] lpOverlapped`
    如果使用 FILE_FLAG_OVERLAPPED打开 handle_value 参数，则需要指向 OVERLAPPED 结构的指针，否则它可以 NULL。

```asm
; ReadFile(handle_value, buf_addr, 0x40, &numberOfBytesRead, nullptr)
; RCX 句柄，此处使用 rax 传递
; RDX 缓冲区指针 
; R8 读取字节数
; R9 out 字节
; rsp+0x20 同步 NULL

f"""
_start:
    mov rcx, rax
    mov rdx, [rip + buf_addr]
    mov r8, 0x40
    lea r9, [rip + lpNumberOfBytesRead]
    sub rsp, 0x28
    mov qword ptr [rsp+0x20], 0
    call [rip + ReadFile_addr]
    add rsp, 0x28


buf_addr:
    .quad {buf_addr:#x}
lpNumberOfBytesRead:
    .quad 0
ReadFile_addr:
    .quad {ReadFile_addr:#x}
"""
```

## VirtualProtect 函数 (memoryapi.h) - 更改调用进程的虚拟地址空间中已提交页面区域的保护

<https://learn.microsoft.com/zh-cn/windows/win32/api/memoryapi/nf-memoryapi-virtualprotect>

若要更改任何进程的访问保护，请使用 VirtualProtectEx 函数。

```c++
BOOL VirtualProtect(
  [in]  LPVOID lpAddress,
  [in]  SIZE_T dwSize,
  [in]  DWORD  flNewProtect,
  [out] PDWORD lpflOldProtect
);
```

[内存保护常量](https://learn.microsoft.com/zh-cn/windows/win32/Memory/memory-protection-constants)

## WriteFile 函数 （fileapi.h）- 将数据写入指定的文件或输入/输出（I/O）设备

此函数适用于同步和异步操作。 有关专为异步操作设计的类似函数，请参阅 WriteFileEx。

```c++
BOOL WriteFile(
  [in]                HANDLE       handle_value,
  [in]                LPCVOID      lpBuffer,
  [in]                DWORD        nNumberOfBytesToWrite,
  [out, optional]     LPDWORD      lpNumberOfBytesWritten,
  [in, out, optional] LPOVERLAPPED lpOverlapped
);
```

参数：
- `[in] handle_value`
    文件或 I/O 设备的句柄。

    必须使用写入访问权限创建 handle_value 参数。 

- `[in] lpBuffer`
    指向包含要写入文件或设备的数据的缓冲区的指针。
    
- `[in] nNumberOfBytesToWrite`
    要写入文件或设备的字节数。

    值为零指定 null 写入操作。 

- `[out, optional] lpNumberOfBytesWritten`
    指向使用同步 handle_value 参数时写入的字节数的变量的指针。 WriteFile 在执行任何工作或错误检查之前将此值设置为零。 如果这是一个异步操作，请对此参数使用 NULL 以避免潜在的错误结果。

    仅当 lpOverlapped 参数不 NULL时，此参数才能 NULL。

- `[in, out, optional] lpOverlapped`
    如果使用 FILE_FLAG_OVERLAPPED打开 handle_value 参数，则需要指向 OVERLAPPED 结构的指针，否则此参数可以 NULL。

    对于支持字节偏移的 handle_value，如果使用此参数，则必须指定开始写入文件或设备的字节偏移量。 通过设置 Offset 和 OffsetHighOVERLAPPED 结构的成员来指定此偏移量。 对于不支持字节偏移的 handle_value，将忽略 Offset 和 OffsetHigh。

    若要写入文件末尾，请将 Offset 和 OffsetHighOVERLAPPED 结构的成员指定为 0xFFFFFFFF。 这在功能上等效于以前调用 CreateFile 函数，以使用 FILE_APPEND_DATA 访问打开 handle_value。

```asm
; WriteFile(handle_value, buf_addr, 0x40, lpNumberOfBytesWritten, NULL)
; RCX 句柄，此处使用 rax 传递
; RDX 缓冲区指针 
; R8 写入字节
; R9 out 字节
; rsp+0x20 同步 NULL

f"""
_start:
    mov rcx, rax
    mov rdx, [rip + lpBuffer]
    mov r8, 0x40
    lea r9, [rip + lpNumberOfBytesWritten]
    sub rsp, 0x28
    mov qword ptr [rsp+0x20], 0
    call [rip + WriteFile_addr]
    add rsp, 0x28

lpBuffer:
    .quad {buf_addr:#x}
lpNumberOfBytesWritten:
    .quad 0
WriteFile_addr:
    .quad {WriteFile_addr:#x}
"""
```

## GetStdHandle 函数 - 检索指定标准设备的句柄（标准输入、标准输出或标准错误）

```c++
HANDLE WINAPI GetStdHandle(
  _In_ DWORD nStdHandle
);
```

- `nStdHandle [in]`
    标准设备。 此参数的取值可为下列值之一。

    - STD_INPUT_HANDLE ((DWORD)-10)	标准输入设备。 最初，这是输入缓冲区 CONIN$ 的控制台。
    - STD_OUTPUT_HANDLE ((DWORD)-11)	标准输出设备。 最初，这是活动控制台屏幕缓冲区 CONOUT$。
    - STD_ERROR_HANDLE ((DWORD)-12)	标准错误设备。 最初，这是活动控制台屏幕缓冲区 CONOUT$。

```asm
; GetStdHandle(STD_OUTPUT_HANDLE)
; rcx 常量

f"""
_start:
    mov ecx, -11
    sub rsp, 0x28
    call [rip + GetStdHandle_addr]
    add rsp, 0x28
    
GetStdHandle_addr:
    .quad {GetStdHandle_addr:#x}
"""
```

## WinExec 函数 (winbase.h) - 运行指定的应用程序

```c++
UINT WinExec(
  [in] LPCSTR lpCmdLine,
  [in] UINT   uCmdShow
);
```

```asm
; WinExec("cmd /c type C:\\flag")
; rcx 命令行字符串
; rdx 终端显示方式

f"""
_start:
    lea rcx, [rip+cmd_str]
    xor edx, edx
    sub rsp, 0x28
    call [rip + WinExec_addr]
    add rsp, 0x28

cmd_str:
    .asciz "cmd /c type C:\\\\flag"

WinExec_addr:
    .quad {WinExec_addr:#x}
"""
```

## DuplicateToken 函数 (securitybaseapi.h) - 复制一个已经存在的令牌

```c++
BOOL DuplicateToken(
  [in]  HANDLE                       ExistingTokenHandle,
  [in]  SECURITY_IMPERSONATION_LEVEL ImpersonationLevel,
  [out] PHANDLE                      DuplicateTokenHandle
);
```

## OpenProcess 函数 (processthreadsapi.h) - 打开现有的本地进程对象

```cpp
HANDLE OpenProcess(
  [in] DWORD dwDesiredAccess,
  [in] BOOL  bInheritHandle,
  [in] DWORD dwProcessId
);
```

**参数**
- `[in] dwDesiredAccess`
    对进程对象的访问。 针对进程的安全描述符检查此访问权限。 此参数可以是一个或多个进程访问权限。

    如果调用方已启用 SeDebugPrivilege 特权，则会授予请求的访问权限，而不考虑安全描述符的内容。

- `[in] bInheritHandle`
    如果此值为 TRUE，则此进程创建的进程将继承句柄。 否则，进程不会继承此句柄。

- `[in] dwProcessId`
    要打开的本地进程的标识符。


**返回值**

如果函数成功，则返回值是指定进程的打开句柄。
如果函数失败，则返回值为 NULL。

## CreateRemoteThread 函数 （processthreadsapi.h）- 创建在另一个进程的虚拟地址空间中运行的线程

```c++
HANDLE CreateRemoteThread(
  [in]  HANDLE                 hProcess,
  [in]  LPSECURITY_ATTRIBUTES  lpThreadAttributes,
  [in]  SIZE_T                 dwStackSize,
  [in]  LPTHREAD_START_ROUTINE lpStartAddress,
  [in]  LPVOID                 lpParameter,
  [in]  DWORD                  dwCreationFlags,
  [out] LPDWORD                lpThreadId
);
```

lpStartAddress 线程 rip 起始地址

- `[in] hProcess`
    要在其中创建线程的进程句柄。 

- `[in] lpThreadAttributes`
    指向 SECURITY_ATTRIBUTES 结构的指针，该结构指定新线程的安全描述符，并确定子进程是否可以继承返回的句柄。 如果 lpThreadAttributes 为 NULL，则线程将获取默认的安全描述符，并且无法继承句柄。 

- `[in] dwStackSize`
    堆栈的初始大小（以字节为单位）。 系统将此值舍入到最近的页面。 如果此参数为 0（零），则新线程使用可执行文件的默认大小。 

- `[in] lpStartAddress`
    指向由线程执行的 LPTHREAD_START_ROUTINE 类型的应用程序定义的函数的指针，表示远程进程中线程的起始地址。

- `[in] lpParameter`
    指向要传递给线程函数的变量的指针。

- `[in] dwCreationFlags`
    控制线程创建的标志。

- `[out] lpThreadId`
    指向接收线程标识符的变量的指针。

    如果此参数 NULL，则不返回线程标识符。

**返回值**
如果函数成功，则返回值是新线程的句柄。
如果函数失败，则返回值 NULL。 

## VirtualAllocEx 函数 （memoryapi.h）- 保留、提交或更改指定进程的虚拟地址空间中内存区域的状态

该函数初始化它分配给零的内存。

```c++
LPVOID VirtualAllocEx(
  [in]           HANDLE hProcess,
  [in, optional] LPVOID lpAddress,
  [in]           SIZE_T dwSize,
  [in]           DWORD  flAllocationType,
  [in]           DWORD  flProtect
);
```

- `[in] hProcess`
    进程的句柄。

- `[in, optional] lpAddress`
    为要分配的页面区域指定所需起始地址的指针。

- `[in] dwSize`
    要分配的内存区域的大小（以字节为单位）。

- `[in] flAllocationType`
    内存分配的类型。

- `[in] flProtect`
    要分配的页面区域的内存保护。

**返回值**
如果函数成功，则返回值是页面分配区域的基址。
如果函数失败，则返回值 NULL。

## WriteProcessMemory 函数 (memoryapi.h) - 将数据写入到指定进程中的内存区域。 

```c++
BOOL WriteProcessMemory(
  [in]  HANDLE  hProcess,
  [in]  LPVOID  lpBaseAddress,
  [in]  LPCVOID lpBuffer,
  [in]  SIZE_T  nSize,
  [out] SIZE_T  *lpNumberOfBytesWritten
);
```

- `[in] hProcess`
    要修改的进程内存的句柄。 句柄必须具有对进程的PROCESS_VM_WRITE和PROCESS_VM_OPERATION访问权限。

- `[in] lpBaseAddress`
    可供写入访问，如果无法访问，则函数将失败。

- `[in] lpBuffer`
    指向缓冲区的指针，该缓冲区包含要写入指定进程的地址空间中的数据。

- `[in] nSize`
    要写入指定进程的字节数。

- `[out] lpNumberOfBytesWritten`
    指向变量的指针，该变量接收传输到指定进程的字节数。 此参数是可选的。 如果 lpNumberOfBytesWritten 为 NULL，则忽略参数。

**返回值**
如果该函数成功，则返回值为非零值。
如果函数失败，则返回值为 0（零）。 

## ReadProcessMemory 函数 (memoryapi.h)

```c++
BOOL ReadProcessMemory(
  [in]  HANDLE  hProcess,
  [in]  LPCVOID lpBaseAddress,
  [out] LPVOID  lpBuffer,
  [in]  SIZE_T  nSize,
  [out] SIZE_T  *lpNumberOfBytesRead
);
```

**参数**
- `[in] hProcess`
    包含正在读取的内存的进程句柄。 句柄必须具有对进程的PROCESS_VM_READ访问权限。

- `[in] lpBaseAddress`
    指向从中读取的指定进程中基址的指针。 在进行任何数据传输之前，系统会验证指定大小的基址和内存中的所有数据是否可供读取访问，如果无法访问，则函数将失败。

- `[out] lpBuffer`
    指向从指定进程的地址空间接收内容的缓冲区的指针。

- `[in] nSize`
    要从指定进程读取的字节数。

- `[out] lpNumberOfBytesRead`
    指向变量的指针，该变量接收传输到指定缓冲区的字节数。 如果 lpNumberOfBytesRead 为 NULL，则忽略 参数。

**返回值**
如果该函数成功，则返回值为非零值。
如果函数失败，则返回值为 0（零）。 

## GetModuleHandleA 函数 （libloaderapi.h）- 检索指定模块的模块句柄

```c++
HMODULE GetModuleHandleA(
  [in, optional] LPCSTR lpModuleName
);
```

- `[in, optional] lpModuleName`
    加载的模块的名称（.dll 或 .exe 文件）。 如果省略文件扩展名，则会追加默认库扩展名 .dll


**返回值**
如果函数成功，则返回值是指定模块的句柄。
如果函数失败，则返回值为 NULL。

## GetProcAddress 函数 (libloaderapi.h) - 从指定的动态链接库 (DLL) 检索导出函数 (也称为过程) 或变量的地址

```c++
FARPROC GetProcAddress(
  [in] HMODULE hModule,
  [in] LPCSTR  lpProcName
);
```

**参数**
- `[in] hModule`
    包含函数或变量的 DLL 模块的句柄。 LoadLibrary、LoadLibraryEx、LoadPackagedLibrary 或 GetModuleHandle 函数返回此句柄。

- `[in] lpProcName`
    函数或变量名称，或函数的序号值。

**返回值**
如果函数成功，则返回值是导出的函数或变量的地址。
如果函数失败，则返回值为 NULL

## DllMain 入口点

```c++
BOOL WINAPI DllMain(
  _In_ HINSTANCE hinstDLL,
  _In_ DWORD     fdwReason,
  _In_ LPVOID    lpvReserved
);
```

```c++
BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // DLL 模块句柄
    DWORD fdwReason,     // 调用本函数的原因
    LPVOID lpvReserved ) // 保留参数
{
    // 根据调用原因执行相应操作
    switch( fdwReason ) 
    { 
        case DLL_PROCESS_ATTACH:
         // 每个新进程初始化一次
         // 若返回 FALSE，DLL 加载失败
            break;

        case DLL_THREAD_ATTACH:
         // 执行线程相关的初始化
            break;

        case DLL_THREAD_DETACH:
         // 执行线程相关的清理
            break;

        case DLL_PROCESS_DETACH:
        
            if (lpvReserved != nullptr)
            {
                break; // 若为进程终止，不执行清理
            }
            
         // 执行必要的清理工作
            break;
    }
    return TRUE;  // DLL_PROCESS_ATTACH 成功
}
```

## CreateProcessA 函数 （processthreadsapi.h）- 创建一个新进程及其主线程

```c++
BOOL CreateProcessA(
  [in, optional]      LPCSTR                lpApplicationName,
  [in, out, optional] LPSTR                 lpCommandLine,
  [in, optional]      LPSECURITY_ATTRIBUTES lpProcessAttributes,
  [in, optional]      LPSECURITY_ATTRIBUTES lpThreadAttributes,
  [in]                BOOL                  bInheritHandles,
  [in]                DWORD                 dwCreationFlags,
  [in, optional]      LPVOID                lpEnvironment,
  [in, optional]      LPCSTR                lpCurrentDirectory,
  [in]                LPSTARTUPINFOA        lpStartupInfo,
  [out]               LPPROCESS_INFORMATION lpProcessInformation
);
```

- `[in, optional] lpApplicationName`
    要执行的模块的名称。 

- `[in, out, optional] lpCommandLine`
    要执行的命令行。

- `[in, optional] lpProcessAttributes`
    指向 SECURITY_ATTRIBUTES 结构的指针，该结构确定新进程对象的返回句柄是否可以由子进程继承。 如果 NULL，则无法继承句柄。

- `[in, optional] lpThreadAttributes`
    指向 SECURITY_ATTRIBUTES 结构的指针，该结构确定新线程对象的返回句柄是否可以由子进程继承。 如果 NULL，则无法继承句柄。

- `[in] bInheritHandles`
    如果此参数为 TRUE，则调用进程中的每个可继承句柄都由新进程继承。 如果参数为 FALSE，则不会继承句柄。 

- `[in] dwCreationFlags`
    控制优先级类和创建进程的标志。

    - CREATE_SUSPENDED 挂起创建

- `[in, optional] lpEnvironment`
    指向新进程的 环境块 的指针。 如果此参数 NULL，则新进程使用调用进程的环境。

- `[in, optional] lpCurrentDirectory`
    进程的当前目录的完整路径。 
    如果此参数 NULL，则新进程将具有与调用进程相同的当前驱动器和目录。

- `[in] lpStartupInfo`
    指向 STARTUPINFO 或 STARTUPINFOEX 结构的指针。

- `[out] lpProcessInformation`
    指向接收有关新进程的标识信息的 PROCESS_INFORMATION 结构的指针。


**返回值**
如果函数成功，则返回值为非零。
如果函数失败，则返回值为零。

## WaitForSingleObject 函数 （synchapi.h）- 等待指定的对象处于信号状态或超时间隔过

```c++
DWORD WaitForSingleObject(
  [in] HANDLE hHandle,
  [in] DWORD  dwMilliseconds
);
```

- `[in] hHandle`
    对象的句柄。 

- `[in] dwMilliseconds`
    超时间隔（以毫秒为单位）。 
    如果 INFINITE，则仅当发出对象信号时，函数才会返回。


**返回值**
如果函数成功，则返回值指示导致函数返回的事件。

## getExitCodeThread 函数 (processthreadsapi.h) - 检索指定线程的终止状态

```c++
BOOL GetExitCodeThread(
  [in]  HANDLE  hThread,
  [out] LPDWORD lpExitCode
);
```

- `[in] hThread`
    线程的句柄。

- `[out] lpExitCode`
    指向用于接收线程终止状态的变量的指针。 

## CloseHandle 函数 (handleapi.h) - 关闭打开的对象句柄

```c++
BOOL CloseHandle(
  [in] HANDLE hObject
);
```

- `[in] hObject`
    打开对象的有效句柄。

**返回值**
如果该函数成功，则返回值为非零值。
如果函数失败，则返回值为零。

## LoadLibraryA 函数 （libloaderapi.h）- 将指定的模块加载到调用进程的地址空间中

```c++
HMODULE LoadLibraryA(
  [in] LPCSTR lpLibFileName
);
```

- `[in] lpLibFileName`
    模块的名称。

**返回值**
如果函数成功，则返回值是模块的句柄。
如果函数失败，则返回值为 NULL。

## CreateToolhelp32Snapshot 函数 (tlhelp32.h) - 获取指定进程以及这些进程使用的堆、模块和线程的快照

```c++
HANDLE CreateToolhelp32Snapshot(
  [in] DWORD dwFlags,
  [in] DWORD th32ProcessID
);
```

**参数**
- `[in] dwFlags`
    要包含在快照中的系统部分

    - TH32CS_SNAPMODULE 0x00000008
        包括快照 th32ProcessID 中指定的进程的所有模块。 若要枚举模块，请参阅 Module32First。

    - TH32CS_SNAPMODULE32 0x00000010
        从 64 位进程调用时，包括快照中 th32ProcessID 中指定的进程的所有 32 位模块。 此标志可以与 TH32CS_SNAPMODULE 或 TH32CS_SNAPALL结合使用。

- `[in] th32ProcessID`
    要包含在快照中的进程的进程标识符。 此参数可以为零以指示当前进程。 

**返回值**
如果函数成功，它将返回指定快照的打开句柄。
如果函数失败，它将返回 INVALID_HANDLE_VALUE。

## Module32First 函数 (tlhelp32.h) - 检索与进程关联的第一个模块的相关信息

```c++
BOOL Module32First(
  [in]      HANDLE          hSnapshot,
  [in, out] LPMODULEENTRY32 lpme
);
```

**参数**
- `[in] hSnapshot`
    快照的句柄，该句柄是从上次调用 CreateToolhelp32Snapshot 函数返回的。

- `[in, out] lpme`
    指向 MODULEENTRY32 结构的指针。

**返回值**
如果模块列表的第一个条目已复制到缓冲区，则返回 TRUE ，否则返回 FALSE 。

**注解**
调用应用程序必须将 MODULEENTRY32 的 dwSize 成员设置为 结构的大小（以字节为单位）。

若要检索与指定进程关联的其他模块的相关信息，请使用 Module32Next 函数。

## Module32Next 函数 (tlhelp32.h) - 检索与进程或线程关联的下一个模块的相关信息

```c++
BOOL Module32Next(
  [in]  HANDLE          hSnapshot,
  [out] LPMODULEENTRY32 lpme
);
```

**参数**
- `[in] hSnapshot`
    快照的句柄，该句柄是从上次调用 CreateToolhelp32Snapshot 函数返回的。

- `[out] lpme`
    指向 MODULEENTRY32 结构的指针。

**返回值**
如果模块列表的下一个条目已复制到缓冲区，则返回 TRUE ，否则返回 FALSE 。

**注解**
若要检索与进程关联的第一个模块的相关信息，请使用 Module32First 函数。

## GetLastError 函数 (errhandlingapi.h) - 检索调用线程的最后错误代码值。

```c++
_Post_equals_last_error_ DWORD GetLastError();
```

**返回值**
返回值是调用线程的最后错误代码。

## CallNamedPipeA 函数 (winbase.h) - 连接到消息类型管道 (，并等待管道实例不可用) ，写入管道并从管道读取，然后关闭管道

https://learn.microsoft.com/zh-cn/windows/win32/api/winbase/nf-winbase-callnamedpipea

## DefineDosDeviceA 函数 (winbase.h) - 定义、重新定义或删除 MS-DOS 设备名称

https://learn.microsoft.com/zh-cn/windows/win32/api/winbase/nf-winbase-definedosdevicea

```c++
BOOL DefineDosDeviceA(
  [in]           DWORD  dwFlags,
  [in]           LPCSTR lpDeviceName,
  [in, optional] LPCSTR lpTargetPath
);
```

- `[in] dwFlags`
    DefineDosDevice 函数的可控制方面

    - DDD_RAW_TARGET_PATH 0x00000001
        按原样使用 lpTargetPath 字符串。即完全路径

- `[in] lpDeviceName`
    指向 MS-DOS 设备名称字符串的指针，指定函数正在定义、重新定义或删除的设备。

- `[in, optional] lpTargetPath`
    指向将实现此设备的路径字符串的指针

**返回值**
如果该函数成功，则返回值为非零值。
如果函数失败，则返回值为零。 

## 模板

获取文件句柄、读取到 buf，获取标准输出句柄，从 buf 打印到标准输出
```asm
; CreateFileA("\\.\pipe\LOCAL\FlagPipe", 0x10000000, 0, nullptr,  OPEN_EXISTING, SECURITY_ANONYMOUS, nullptr)

; ReadFile(handle_value, the_buf, 0x40, &numberOfBytesRead, nullptr)

; GetStdHandle(STD_OUTPUT_HANDLE)

; WriteFile(handle_value, buf_addr, 0x40, lpNumberOfBytesWritten, NULL)

f"""
_start:
    lea rcx, [rip+file_path]
    mov edx, 0x10000000
    xor r8, r8
    xor r9, r9
    sub rsp, 0x38
    mov qword ptr [rsp+0x20], 3
    mov qword ptr [rsp+0x28], 0x80
    mov qword ptr [rsp+0x30], 0
    call [rip + CreateFileA_addr]
    add rsp, 0x38

    mov rcx, rax
    lea rdx, [rip + the_buf]
    mov r8, 0x40
    lea r9, [rip + lpNumberOfBytesRead]
    sub rsp, 0x28
    mov qword ptr [rsp+0x20], 0
    call [rip + ReadFile_addr]
    add rsp, 0x28


    mov ecx, -11
    sub rsp, 0x28
    call [rip + GetStdHandle_addr]
    add rsp, 0x28

    mov rcx, rax
    lea rdx, [rip + the_buf]
    mov r8, 0x40
    lea r9, [rip + lpNumberOfBytesWritten]
    sub rsp, 0x28
    mov qword ptr [rsp+0x20], 0
    call [rip + WriteFile_addr]
    add rsp, 0x28
    ret

file_path:
    .asciz "\\\\\\\\.\\\\pipe\\\\LOCAL\\\\FlagPipe"
CreateFileA_addr:
    .quad {CreateFileA_addr:#x}


lpNumberOfBytesRead:
    .quad 0
ReadFile_addr:
    .quad {ReadFile_addr:#x}

the_buf:
    .zero 0x40
the_buf_end:


GetStdHandle_addr:
    .quad {GetStdHandle_addr:#x}


lpNumberOfBytesWritten:
    .quad 0
WriteFile_addr:
    .quad {WriteFile_addr:#x}
"""
```
- `.zero` 创建一块0初始化的缓冲区
