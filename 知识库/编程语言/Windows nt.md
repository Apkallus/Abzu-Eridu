# ntdll

## 迁移

路径：
- C 文件 `C:\Users\hacker\saved_data`
- nt 文件 `\??\C:\Users\hacker\saved_data`
- C 管道 `\.\pipe\LOCAL\FlagPipe`
- nt 管道 `\Device\NamedPipe\LOCAL\FlagPipe`

## InitializeObjectAttributes 宏 （ntdef.h）- InitializeObjectAttributes 宏初始化不透明OBJECT_ATTRIBUTES结构

https://learn.microsoft.com/zh-cn/windows/win32/api/ntdef/nf-ntdef-initializeobjectattributes

## RtlInitUnicodeString 函数 (wdm.h) - 设置字符串到 unicode 结构

```c++
NTSYSAPI VOID RtlInitUnicodeString(
  [out]          PUNICODE_STRING         DestinationString,
  [in, optional] __drv_aliasesMem PCWSTR SourceString
);
```

## NtCreateFile 函数 （winternl.h） - 创建新文件或目录，或打开现有文件、设备、目录或卷

https://learn.microsoft.com/zh-cn/windows/win32/api/winternl/nf-winternl-ntcreatefile

```c++
__kernel_entry NTSTATUS NtCreateFile(
  [out]          PHANDLE            FileHandle,
  [in]           ACCESS_MASK        DesiredAccess,
  [in]           POBJECT_ATTRIBUTES ObjectAttributes,
  [out]          PIO_STATUS_BLOCK   IoStatusBlock,
  [in, optional] PLARGE_INTEGER     AllocationSize,
  [in]           ULONG              FileAttributes,
  [in]           ULONG              ShareAccess,
  [in]           ULONG              CreateDisposition,
  [in]           ULONG              CreateOptions,
  [in]           PVOID              EaBuffer,
  [in]           ULONG              EaLength
);
```

tips:
- `ObjectAttributes` 对象属性字段中包含文件路径
    - 调用 `InitializeObjectAttributes` 初始化对象结构宏设置 `_OBJECT_ATTRIBUTES` 对象结构
        - 其中字符串指针类型为 unicode
            - 调用内核函数 `RtlInitUnicodeString` 设置路径字符串到 unicode 结构
- `CreateOptions` 打开文件选项字段需设置同步 flag 以读写

```c++
// 获取文件句柄：nt CreateFile 定义，之后获取地址
typedef NTSTATUS (NTAPI* CreateFile_NT_func)(PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, PLARGE_INTEGER, ULONG, ULONG, ULONG, ULONG, PVOID,ULONG);
CreateFile_NT_func CreateFile_NT;

// 设置 unicode 结构：nt RtlInitUnicodeString 定义，之后获取地址
typedef  VOID (NTAPI* RtlInitUnicodeString_NT_func)(PUNICODE_STRING, PCWSTR);
RtlInitUnicodeString_NT_func RtlInitUnicodeString_NT;

// CreateFile 包装函数，返回句柄
HANDLE CreateFile_wrap(const wchar_t* file_str, ULONG CreateDisposition){
    // 设置字符串路径到 unicode 结构
    UNICODE_STRING file_path = {0};
    RtlInitUnicodeString_NT(&file_path, file_str);
    // 使用字符串 unicode 结构，设置对象属性
    _OBJECT_ATTRIBUTES ObjectAttributes;
    InitializeObjectAttributes(
        &ObjectAttributes, 
        &file_path,
        OBJ_CASE_INSENSITIVE,
        NULL,
        NULL
    );
    
    // 调用 nt CreateFile 函数，注意读写必有同步 flag
    IO_STATUS_BLOCK IoStatusBlock;
    HANDLE FileHandle;
    CreateFile_NT(
            &FileHandle,   // out 文件句柄指针
            FILE_GENERIC_READ | FILE_GENERIC_WRITE | SYNCHRONIZE, // 访问 mask，读写与同步
            &ObjectAttributes, // 文件结构，包含文件路径字符串
            &IoStatusBlock, // out 完成状态
            NULL,   // 文件初始大小
            FILE_ATTRIBUTE_NORMAL, // 文件属性
            FILE_SHARE_READ | FILE_SHARE_WRITE, // 共享模式
            CreateDisposition, // 打开模式，参数传入
            FILE_NON_DIRECTORY_FILE | FILE_SYNCHRONOUS_IO_NONALERT, // 打开文件选项，非目录与同步
            NULL, // 扩展属性缓冲区
            0 // 扩展缓冲区长度
    );
    return FileHandle;
}

// 设置全局变量 nt 函数地址
CreateFile_NT = (CreateFile_NT_func)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtCreateFile");
RtlInitUnicodeString_NT = (RtlInitUnicodeString_NT_func)GetProcAddress(GetModuleHandleA("ntdll.dll"), "RtlInitUnicodeString");

// 打开管道句柄
HANDLE flag_handle = CreateFile_wrap(L"\\Device\\NamedPipe\\LOCAL\\FlagPipe", FILE_OPEN);

// 打开文件句柄
HANDLE copy_handle = CreateFile_wrap(L"\\??\\C:\\Users\\hacker\\saved_data", FILE_OVERWRITE_IF);
```

## NtCreateNamedPipeFile 函数 - 创建并打开特定命名管道的第一个实例或现有命名管道的另一个实例的服务器端句柄

https://learn.microsoft.com/zh-cn/windows/win32/devnotes/nt-create-named-pipe-file

```c++
NTSTATUS NtCreateNamedPipeFile(
  [out]          PHANDLE            FileHandle,
  [in]           ULONG              DesiredAccess,
  [in]           POBJECT_ATTRIBUTES ObjectAttributes,
  [out]          PIO_STATUS_BLOCK   IoStatusBlock,
  [in]           ULONG              ShareAccess,
  [in]           ULONG              CreateDisposition,
  [in]           ULONG              CreateOptions,
  [in]           ULONG              NamedPipeType,
  [in]           ULONG              ReadMode,
  [in]           ULONG              CompletionMode,
  [in]           ULONG              MaximumInstances,
  [in]           ULONG              InboundQuota,
  [in]           ULONG              OutboundQuota,
  [in, optional] PLARGE_INTEGER     DefaultTimeout
);
```




## NtOpenFile 函数 （ntifs.h）- NtOpenFile 例程将打开现有文件、目录、设备或卷

https://learn.microsoft.com/zh-cn/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntopenfile

```c++
__kernel_entry NTSYSCALLAPI NTSTATUS NtOpenFile(
  [out] PHANDLE            FileHandle,
  [in]  ACCESS_MASK        DesiredAccess,
  [in]  POBJECT_ATTRIBUTES ObjectAttributes,
  [out] PIO_STATUS_BLOCK   IoStatusBlock,
  [in]  ULONG              ShareAccess,
  [in]  ULONG              OpenOptions
);
```

```c++
// NtOpenFile 包装函数，返回句柄
HANDLE NtOpenFile_wrap(const wchar_t* file_str){
    // 设置字符串路径到 unicode 结构
    UNICODE_STRING file_path = {0};
    RtlInitUnicodeString_NT(&file_path, file_str);
    // 使用字符串 unicode 结构，设置对象属性
    _OBJECT_ATTRIBUTES ObjectAttributes;
    InitializeObjectAttributes(
        &ObjectAttributes, 
        &file_path,
        OBJ_CASE_INSENSITIVE,
        NULL,
        NULL
    );
    
    // 调用 nt CreateFile 函数，注意读写必有同步 flag
    IO_STATUS_BLOCK IoStatusBlock;
    HANDLE FileHandle;
    NtOpenFile_NT(
            &FileHandle,   // out 文件句柄指针
            FILE_GENERIC_READ | FILE_GENERIC_WRITE | SYNCHRONIZE, // 访问 mask，读写与同步
            &ObjectAttributes, // 文件结构，包含文件路径字符串
            &IoStatusBlock, // out 完成状态
            FILE_SHARE_READ | FILE_SHARE_WRITE, // 共享模式
            FILE_NON_DIRECTORY_FILE | FILE_SYNCHRONOUS_IO_NONALERT // 打开文件选项，非目录与同步
    );
    return FileHandle;
}

NtOpenFile_NT =  (NtOpenFile_func)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtOpenFile");
```

## NtCreateSymbolicLinkObject - 创建符号链接

https://ntdoc.m417z.com/ntcreatesymboliclinkobject

## NtOpenSymbolicLinkObject 函数 - 打开现有符号链接

此函数将来可能会更改或不可用。

```c++
NTSTATUS WINAPI NtOpenSymbolicLinkObject(
  _Out_ PHANDLE            LinkHandle,
  _In_  ACCESS_MASK        DesiredAccess,
  _In_  POBJECT_ATTRIBUTES ObjectAttributes
);
```


参数
- `LinkHandle [out]`
    新打开的符号链接对象的句柄。

- `DesiredAccess [in]`
    一个 ACCESS_MASK ，指定对目录对象的请求访问权限。 通常使用 GENERIC_READ以便可以将句柄传递给 NtQueryDirectoryObject 函数。

- `ObjectAttributes [in]`
    目录对象的属性。 若要初始化 OBJECT_ATTRIBUTES 结构，请使用 InitializeObjectAttributes 宏。


## NtCreateThreadEx - 创建远程线程

https://ntdoc.m417z.com/ntcreatethreadex

```asm
NtCreateThreadEx_syscall:
    mov     r10,rcx
    mov     eax,0C4h
    syscall
    ret
```

参数
- ThreadHandle - 指向一个变量的指针，该变量接收新线程的句柄。
- DesiredAccess - 返回句柄上的线程访问掩码。此值通常为 THREAD_ALL_ACCESS。
- ObjectAttributes - 一个可选的指针，指向 OBJECT_ATTRIBUTES 结构，用于指定新对象/句柄的属性，例如安全描述符和句柄继承。
- ProcessHandle - 应创建线程的进程句柄。可以是 NtCurrentProcess 伪句柄，也可以是具有 PROCESS_CREATE_THREAD 访问权限的句柄。
- StartRoutine - 在新线程上执行的函数。
- Argument - 用户提供的、传递给线程启动例程的参数。
- CreateFlags - 一个位掩码，控制新线程的属性或其创建方式。见下文。
    - THREAD_CREATE_FLAGS_CREATE_SUSPENDED
        创建处于挂起状态的线程，而不是立即允许其执行。
    - THREAD_CREATE_FLAGS_BYPASS_PROCESS_FREEZE
        当系统挂起或冻结进程时，线程不应被挂起。
- ZeroBits - 线程栈基地址中必须为零的高位地址位数。注意，当该值大于 32 时，它将成为一个位掩码。
- StackSize - 栈的初始大小，以字节为单位。系统会将此值向上舍入到最近的页面大小。如果此参数为零，新线程将使用可执行文件的默认大小。
- MaximumStackSize - 栈的最大大小，以字节为单位。系统会将此值向上舍入到最近的页面大小。如果此参数为零，新线程将使用可执行文件的默认大小。
- AttributeList - 一个可选的指针，指向一个缓冲区，该缓冲区定义了一个 PS_ATTRIBUTE 结构列表，这些结构控制线程创建的各个方面，并允许检索有关新线程的信息。

注意，此处替换以简化为:
- `PUSER_THREAD_START_ROUTINE` 到 `LPTHREAD_START_ROUTINE`
- `PPS_ATTRIBUTE_LIST` 到 `PVOID` 由于暂时不设置线程信息结构
```c++
#define THREAD_CREATE_FLAGS_BYPASS_PROCESS_FREEZE 0x00000040 // NtCreateThreadEx only // since 19H1
// 设置系统调用
extern "C" NTSTATUS NtCreateThreadEx_syscall(
    PHANDLE,
    ACCESS_MASK,
    PCOBJECT_ATTRIBUTES,
    HANDLE,
    LPTHREAD_START_ROUTINE,
    PVOID,
    ULONG,
    SIZE_T,
    SIZE_T,
    SIZE_T,
    PVOID
);

// NtCreateThreadEx 包装函数
HANDLE NtCreateThreadEx_wrap(HANDLE ProcessHandle, LPTHREAD_START_ROUTINE StartRoutine, PVOID Argument){


    HANDLE ThreadHandle;
    NtCreateThreadEx_syscall( // dll stub
        &ThreadHandle, // 新线程句柄指针
        THREAD_ALL_ACCESS, // 线程访问掩码
        NULL, // 指定属性
        ProcessHandle, // 进程句柄，参数传递
        StartRoutine, // 在新线程上执行的函数，参数传递
        Argument, // 线程启动例程的参数，参数传递
        THREAD_CREATE_FLAGS_BYPASS_PROCESS_FREEZE, // 控制新线程的属性
        0, // 为零的高位地址位数
        0, // 栈的初始大小
        0, // 栈的最大大小
        (PVOID)NULL // 线程信息结构指针
    );
    return ThreadHandle;
}
```

## NtAllocateVirtualMemory 函数 （ntifs.h） - 设置虚拟内存

https://learn.microsoft.com/zh-cn/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntallocatevirtualmemory

```asm
NtAllocateVirtualMemory_syscall:
    mov     r10,rcx
    mov     eax,18h
    syscall
    ret
```

```c++
__kernel_entry NTSYSCALLAPI NTSTATUS NtAllocateVirtualMemory(
  [in]      HANDLE    ProcessHandle,
  [in, out] PVOID     *BaseAddress,
  [in]      ULONG_PTR ZeroBits,
  [in, out] PSIZE_T   RegionSize,
  [in]      ULONG     AllocationType,
  [in]      ULONG     Protect
);
```

```c++
extern "C" NTSTATUS NtAllocateVirtualMemory_syscall(
    HANDLE   ,
    PVOID    ,
    ULONG_PTR,
    PSIZE_T  ,
    ULONG    ,
    ULONG    
);

LPVOID NtAllocateVirtualMemory_wrap(HANDLE ProcessHandle, PVOID BaseAddress_arg, SIZE_T RegionSize_arg, ULONG AllocationType, ULONG Protect){

    SIZE_T RegionSize = RegionSize_arg;
    PVOID BaseAddress = BaseAddress_arg;
    NtAllocateVirtualMemory_syscall( // dll stub
        ProcessHandle   , // 进程句柄，参数传递
        &BaseAddress    , // 分配区域的基址，参数传递 in 后，返回 out
        (ULONG_PTR)NULL, // 基址中必须为零的高序地址位数
        &RegionSize  , // 分配区域的实际大小的变量的指针，参数传递 in
        AllocationType    , // 分配类型位掩码，参数传递
        Protect   // 保护标志的位掩码，参数传递
    );
    return (LPVOID)BaseAddress;
}
```

## NtAllocateVirtualMemory 函数 （ntifs.h） - 写入虚拟内存

https://ntdoc.m417z.com/ntwritevirtualmemory

```asm
NtWriteVirtualMemory_syscall:
    mov     r10,rcx
    mov     eax,3Ah
    syscall
    ret
```

```c++
_Kernel_entry_
NTSYSCALLAPI
NTSTATUS
NTAPI
NtWriteVirtualMemory(
    _In_ HANDLE ProcessHandle,
    _In_opt_ PVOID BaseAddress,
    _In_reads_bytes_(NumberOfBytesToWrite) PVOID Buffer,
    _In_ SIZE_T NumberOfBytesToWrite,
    _Out_opt_ PSIZE_T NumberOfBytesWritten
    );
```

```c++
extern "C" NTSTATUS NtWriteVirtualMemory_syscall(HANDLE, LPVOID, LPCVOID, SIZE_T , SIZE_T*);

NTSTATUS NtWriteVirtualMemory_wrap(HANDLE hProcess, LPVOID lpBaseAddress, LPCVOID lpBuffer, SIZE_T nSize, SIZE_T* PnSize){
    return NtWriteVirtualMemory_syscall(hProcess, lpBaseAddress, lpBuffer, nSize, PnSize);
}
```