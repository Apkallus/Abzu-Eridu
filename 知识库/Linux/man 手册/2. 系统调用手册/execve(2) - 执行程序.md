https://www.man7.org/linux/man-pages/man2/execve.2.html

# execve - 执行程序

### 库

标准 C 库（`libc`，`-lc`）

### 概要

```c
#include <unistd.h>

int execve(const char *path, char *const _Nullable argv[],
           char *const _Nullable envp[]);
```

### 描述

`execve()` 执行 `path` 所引用的程序。这会导致调用进程当前正在运行的程序被新程序替换，并使用新初始化的栈、堆以及（已初始化和未初始化的）数据段。

`path` 必须是二进制可执行文件，或以如下形式的一行开头的脚本：

```sh
#!interpreter [optional-arg]
```

后一种情况的细节参见下面的“解释器脚本”。

`argv` 是指向字符串的指针数组，作为新程序的命令行参数传递。按照惯例，其中第一个字符串（即 `argv[0]`）应包含与被执行文件相关联的文件名。`argv` 数组必须由空指针终止。（因此，在新程序中，`argv[argc]` 将是空指针。）

`envp` 是指向字符串的指针数组，按惯例形式为 `key=value`，作为新程序的环境传递。`envp` 数组必须由空指针终止。

本手册页详细描述 Linux 系统调用；有关 libc 提供的该函数命名法以及许多通常更可取的标准变体（包括搜索 `PATH` 环境变量的变体）的概述，参见 [`exec(3)`]。

新程序的 `main` 函数在定义为以下形式时，可以访问参数向量和环境：

```c
int main(int argc, char *argv[], char *envp[])
```

但请注意，POSIX.1 未规定 `main` 函数使用第三个参数；根据 POSIX.1，应通过外部变量 `environ`（[environ(7)]）访问环境。

`execve()` 成功时不返回，并且调用进程的文本、已初始化数据、未初始化数据（bss）和栈会根据新加载程序的内容被覆盖。

如果当前程序正在被 ptrace，则在 `execve()` 成功后，会向其发送 `SIGTRAP` 信号。

如果 `path` 引用的程序文件上设置了设置用户 ID 位，则调用进程的有效用户 ID 会改为该程序文件所有者的用户 ID。类似地，如果程序文件上设置了设置组 ID 位，则调用进程的有效组 ID 会设置为该程序文件的组。

如果以下任一条件为真，则不执行上述有效 ID 转换（即忽略设置用户 ID 和设置组 ID 位）：

- 调用线程设置了 `no_new_privs` 属性（参见 [`prctl(2)`]）；

- 底层文件系统以 `nosuid` 挂载（[`mount(2)`] 的 `MS_NOSUID` 标志）；或

- 调用进程正在被 ptrace。

如果上述任一条件为真，程序文件的能力（参见 [`capabilities(7)`]）也会被忽略。

进程的有效用户 ID 会复制到保存的设置用户 ID；类似地，有效组 ID 会复制到保存的设置组 ID。此复制发生在因设置用户 ID 和设置组 ID 模式位而发生的任何有效 ID 更改之后。

进程的实际 UID 和实际 GID，以及其补充组 ID，不会因调用 `execve()` 而改变。

如果可执行文件是包含共享库桩的 a.out 动态链接二进制可执行文件，则在执行开始时调用 Linux 动态链接器 [`ld.so(8)`]，以将所需的共享对象载入内存并将可执行文件与它们链接。

如果可执行文件是动态链接的 ELF 可执行文件，则使用 `PT_INTERP` 段中命名的解释器来加载所需的共享对象。对于与 glibc 链接的二进制文件，该解释器通常是 `/lib/ld-linux.so.2`（参见 [`ld-linux.so(8)`]）。

#### 对进程属性的影响

在 `execve()` 期间，所有进程属性都会保留，但以下属性除外：

- 正在被捕获的任何信号的处置会重置为默认（[signal(7)]）。

- 任何备用信号栈都不会保留（[`sigaltstack(2)`]）。

- 内存映射不会保留（[`mmap(2)`]）。

- 已附加的 System V 共享内存段会被分离（[`shmat(2)`]）。

- POSIX 共享内存区域会被取消映射（[`shm_open(3)`]）。

- 打开的 POSIX 消息队列描述符会被关闭（[mq_overview(7)]）。

- 任何打开的 POSIX 命名信号量会被关闭（[sem_overview(7)]）。

- POSIX 定时器不会保留（[`timer_create(2)`]）。

- 任何打开的目录流会被关闭（[`opendir(3)`]）。

- 内存锁不会保留（[`mlock(2)`]、[`mlockall(2)`]）。

- 退出处理程序不会保留（[`atexit(3)`]、[`on_exit(3)`]）。

- 浮点环境会重置为默认（参见 [`fenv(3)`]）。

前一个列表中的进程属性均在 POSIX.1 中规定。以下 Linux 特有的进程属性在 `execve()` 期间也不会保留：

- 进程的 "dumpable" 属性设置为值 1，除非正在执行设置用户 ID 程序、设置组 ID 程序或具有能力的程序；在后一种情况下，dumpable 标志可能会改为重置为 `/proc/sys/fs/suid_dumpable` 中的值，具体情形见 [`prctl(2)`] 中 `PR_SET_DUMPABLE` 下的描述。请注意，对 "dumpable" 属性的更改可能导致进程的 `/proc/`pid 目录中文件的所有权变为 `root:root`，如 [proc(5)] 所述。

- [`prctl(2)`] 的 `PR_SET_KEEPCAPS` 标志会被清除。

- （自 Linux 2.4.36 / 2.6.23 起）如果正在执行设置用户 ID 或设置组 ID 程序，则由 [`prctl(2)`] 的 `PR_SET_PDEATHSIG` 标志设置的父进程死亡信号会被清除。

- 进程名称（由 [`prctl(2)`] 的 `PR_SET_NAME` 设置，并由 `ps -o comm` 显示）会重置为新可执行文件的名称。

- `SECBIT_KEEP_CAPS` *securebits* 标志会被清除。参见 [`capabilities(7)`]。

- 终止信号会重置为 `SIGCHLD`（参见 [`clone(2)`]）。

- 文件描述符表会被取消共享，撤销 [`clone(2)`] 的 `CLONE_FILES` 标志的效果。

另请注意以下几点：

- 在 `execve()` 期间，除调用线程外的所有线程都会被销毁。互斥锁、条件变量和其他 pthreads 对象不会保留。

- 程序启动时会执行相当于 `setlocale(LC_ALL, "C")` 的操作。

- POSIX.1 规定，任何被忽略或设置为默认的信号，其处置保持不变。POSIX.1 规定了一个例外：如果 `SIGCHLD` 正在被忽略，则实现可以保持处置不变或将其重置为默认；Linux 执行前者。

- 任何未完成的异步 I/O 操作都会被取消（[`aio_read(3)`]、[`aio_write(3)`]）。

- 有关 `execve()` 期间能力的处理，参见 [`capabilities(7)`]。

- 默认情况下，文件描述符在 `execve()` 期间保持打开。标记为 close-on-exec 的文件描述符会被关闭；参见 [`fcntl(2)`] 中 `FD_CLOEXEC` 的描述。（如果文件描述符被关闭，这将导致释放此进程在底层文件上获得的所有记录锁。详情参见 [`fcntl(2)`]。）POSIX.1 规定，如果在成功的 `execve()` 之后，文件描述符 0、1 和 2 原本会被关闭，并且由于被执行文件上设置了设置用户 ID 或设置组 ID 模式位，进程将获得特权，则系统可以为这些文件描述符中的每一个打开一个未指定的文件。作为一般原则，任何可移植程序，无论是否特权，都不能假定这三个文件描述符在 `execve()` 期间保持关闭。

#### 解释器脚本

解释器脚本是一个启用了执行权限的文本文件，其第一行为以下形式：

```text
#!interpreter [optional-arg]
```

`interpreter` 必须是可执行文件的有效路径名。

`interpreter` 将使用以下参数调用：

```text
interpreter [optional-arg] path arg...
```

其中 `arg...` 是 `execve()` 的 `argv` 参数所指向的一系列单词，从 `argv[1]` 开始。请注意，无法获得传递给 `execve()` 调用的 `argv[0]`。

为了可移植使用，`optional-arg` 应不存在，或指定为单个单词（即不应包含空白字符）；参见下面的“版本”。

自 Linux 2.6.28 起，内核允许脚本的解释器本身也是脚本。此许可递归适用，最多递归四次，因此解释器可以是由脚本解释的脚本，依此类推。

#### 参数和环境大小的限制

大多数 UNIX 实现会对可传递给新程序的命令行参数（`argv`）和环境（`envp`）字符串的总大小施加某种限制。POSIX.1 允许实现使用 `ARG_MAX` 常量（定义在 `<limits.h>` 中，或通过调用 `sysconf(_SC_ARG_MAX)` 在运行时获得）公布此限制。

在 Linux 2.6.23 之前，用于存储环境和参数字符串的内存限制为 32 页（由内核常量 `MAX_ARG_PAGES` 定义）。在页大小为 4 kB 的架构上，这产生 128 kB 的最大大小。

在 Linux 2.6.23 及更高版本上，大多数架构支持从 `execve()` 调用时生效的软 `RLIMIT_STACK` 资源限制（参见 [`getrlimit(2)`]）派生的尺寸限制。（没有内存管理单元的架构除外：它们维持 Linux 2.6.23 之前生效的限制。）此更改允许程序拥有大得多的参数和/或环境列表。对于这些架构，总大小限制为允许栈大小的 1/4。（施加 1/4 限制确保新程序始终有一些栈空间。）此外，总大小限制为内核常量 `_STK_LIM`（8 MiB）值的 3/4。自 Linux 2.6.25 起，内核还对此大小限制设置 32 页的下限，因此即使 `RLIMIT_STACK` 设置得很低，应用程序也保证至少拥有与 Linux 2.6.22 及更早版本所提供的同样多的参数和环境空间。（Linux 2.6.23 和 2.6.24 未提供此保证。）此外，每个字符串的限制为 32 页（内核常量 `MAX_ARG_STRLEN`），字符串最大数量为 0x7FFFFFFF。

### 返回值

成功时，`execve()` 不返回；出错时返回 `-1`，并设置 `errno` 以指示错误。

### 错误

- `E2BIG`：环境（`envp`）和参数列表（`argv`）中的总字节数过大，某个参数或环境字符串过长，或可执行文件的完整 `path` 过长。终止空字节计入字符串长度。

- `EACCES`：拒绝了对 `path` 路径前缀的某个组件或脚本解释器名称的搜索权限。（另见 [path_resolution(7)]。）

- `EACCES`：文件或脚本解释器不是常规文件。

- `EACCES`：文件、脚本或 ELF 解释器的执行权限被拒绝。

- `EACCES`：文件系统以 `noexec` 挂载。

- `EAGAIN`：（自 Linux 3.1 起）调用者使用某个 `set*uid()` 调用更改了其实际 UID 后，曾超过并且现在仍然超过其 `RLIMIT_NPROC` 资源限制（参见 [`setrlimit(2)`]）。有关此错误的更详细解释，参见“注释”。

- `EFAULT`：`path` 或向量 `argv` 或 `envp` 中的某个指针指向你可访问地址空间之外。

- `EINVAL`：ELF 可执行文件有多个 `PT_INTERP` 段（即试图指定多个解释器）。

- `EIO`：发生 I/O 错误。

- `EISDIR`：ELF 解释器是一个目录。

- `ELIBBAD`：ELF 解释器不是可识别的格式。

- `ELOOP`：在解析 `path` 或脚本或 ELF 解释器名称时遇到太多符号链接。

- `ELOOP`：在递归脚本解释期间达到最大递归限制（参见上面的“解释器脚本”）。在 Linux 3.8 之前，这种情况产生的错误是 `ENOEXEC`。

- `EMFILE`：已达到每进程打开文件描述符数量限制。

- `ENAMETOOLONG`：`path` 过长。

- `ENFILE`：已达到系统范围内打开文件总数限制。

- `ENOENT`：`path` 或脚本或 ELF 解释器不存在。

- `ENOEXEC`：可执行文件不是可识别的格式、架构错误，或有其他格式错误导致无法执行。

- `ENOMEM`：可用内核内存不足。

- `ENOTDIR`：`path` 路径前缀的某个组件或脚本或 ELF 解释器不是目录。

- `EPERM`：文件系统以 `nosuid` 挂载，用户不是超级用户，并且文件设置了设置用户 ID 或设置组 ID 位。

- `EPERM`：进程正在被跟踪，用户不是超级用户，并且文件设置了设置用户 ID 或设置组 ID 位。

- `EPERM`："capability-dumb" 应用程序不会获得可执行文件授予的完整允许能力集。参见 [`capabilities(7)`]。

- `ETXTBSY`：指定的可执行文件正被一个或多个进程以写入方式打开。

### 版本

POSIX 未记录 `#!` 行为，但它在其他 UNIX 系统上存在（有一些差异）。

在 Linux 上，`argv` 和 `envp` 可以指定为 `NULL`。在这两种情况下，这与将参数指定为指向包含单个空指针的列表的指针具有相同效果。**不要利用这个非标准且不可移植的缺陷！** 在许多其他 UNIX 系统上，将 `argv` 指定为 `NULL` 会导致错误（`EFAULT`）。*一些*其他 UNIX 系统对 `envp==NULL` 情况的处理与 Linux 相同。

POSIX.1 规定 [`sysconf(3)`] 返回的值在进程生命周期内应保持不变。然而，自 Linux 2.6.23 起，如果 `RLIMIT_STACK` 资源限制发生变化，则 `_SC_ARG_MAX` 报告的值也会变化，以反映用于保存命令行参数和环境变量的空间限制已改变。

#### 解释器脚本

内核对脚本开头 `#!` 字符之后的文本施加最大长度；超出限制的字符会被忽略。在 Linux 5.1 之前，限制为 127 个字符。自 Linux 5.1 起，限制为 255 个字符。

解释器脚本的 `optional-arg` 参数的语义因实现而异。在 Linux 上，解释器名称之后的整个字符串作为单个参数传递给解释器，并且该字符串可以包含空白字符。然而，在某些其他系统上行为不同。一些系统使用第一个空白字符来终止 `optional-arg`。在某些系统上，解释器脚本可以有多个参数，并且 `optional-arg` 中的空白字符用于分隔参数。

Linux（与大多数其他现代 UNIX 系统一样）忽略脚本上的设置用户 ID 和设置组 ID 位。

### 标准

POSIX.1-2024。

### 历史

4.3BSD、SVr4、POSIX.1-1988。

在 UNIX V6 中，`exec()` 调用的参数列表以 0 结束，而 `main` 的参数列表以 -1 结束。因此，该参数列表不能直接用于进一步的 `exec()` 调用。自 UNIX V7 起，两者都是 `NULL`。

### 注释

有时会看到将 `execve()`（以及 [`exec(3)`] 中描述的相关函数）描述为“执行一个*新*进程”（或类似说法）。这是一种极具误导性的描述：并没有新进程；调用进程的许多属性保持不变（特别是其 PID）。`execve()` 所做的只是安排一个现有进程（调用进程）执行新程序。

设置用户 ID 和设置组 ID 进程不能被 [`ptrace(2)`] 跟踪。

以 `nosuid` 挂载文件系统的结果因 Linux 内核版本而异：一些版本会在这会给予用户其原本没有的权限时拒绝执行设置用户 ID 和设置组 ID 可执行文件（并返回 `EPERM`），一些版本则只是忽略设置用户 ID 和设置组 ID 位并成功 `exec()`。

在大多数 `execve()` 失败的情况下，控制权返回到原始可执行映像，`execve()` 的调用者随后可以处理该错误。然而，在（罕见的）情况下（通常由资源耗尽引起），失败可能发生在不可返回点之后：原始可执行映像已被拆除，但新映像无法完全构建。在这种情况下，内核会用 `SIGSEGV`（Linux 3.17 之前为 `SIGKILL`）信号杀死进程。

#### `execve()` 与 `EAGAIN`

对调用 `execve()` 时可能发生（自 Linux 3.1 起）的 `EAGAIN` 错误的更详细解释如下。

当先前的 [`setuid(2)`]、[`setreuid(2)`] 或 [`setresuid(2)`] 调用导致进程的实际用户 ID 发生变化，并且该变化导致进程超过其 `RLIMIT_NPROC` 资源限制（即属于新实际 UID 的进程数超过资源限制）时，可能发生 `EAGAIN` 错误。从 Linux 2.6.0 到 Linux 3.0，这会导致 `set*uid()` 调用失败。（在 Linux 2.6 之前，未对更改用户 ID 的进程施加该资源限制。）

自 Linux 3.1 起，刚才描述的场景不再导致 `set*uid()` 调用失败，因为它太常导致安全漏洞：有缺陷的应用程序不检查返回状态，并假定——如果调用者具有 root 特权——该调用总是会成功。相反，`set*uid()` 调用现在会成功更改实际 UID，但内核会设置一个名为 `PF_NPROC_EXCEEDED` 的内部标志，以记录已超过 `RLIMIT_NPROC` 资源限制。如果 `PF_NPROC_EXCEEDED` 标志已设置，并且在后续 `execve()` 调用时资源限制仍被超过，则该调用会失败，错误为 `EAGAIN`。此内核逻辑确保 `RLIMIT_NPROC` 资源限制对于常见的特权守护进程工作流——即 [`fork(2)`] + `set*uid()` + `execve()`——仍然得到执行。

如果在 `execve()` 调用时资源限制不再被超过（因为在 `set*uid()` 调用和 `execve()` 调用之间，属于此实际 UID 的其他进程已终止），则 `execve()` 调用成功，内核清除 `PF_NPROC_EXCEEDED` 进程标志。如果此进程后续调用 [`fork(2)`] 成功，该标志也会被清除。

### 示例

以下程序旨在由下面的第二个程序 exec。它只是回显其命令行参数，每行一个。

```c
/* myecho.c */

#include <stdio.h>
#include <stdlib.h>

int
main(int argc, char *argv[])
{
    for (size_t j = 0; j < argc; j++)
        printf("argv[%zu]: %s\n", j, argv[j]);

    exit(EXIT_SUCCESS);
}
```

此程序可用于 exec 其命令行参数中指定的程序：

```c
/* execve.c */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
    static char *newargv[] = { NULL, "hello", "world", NULL };
    static char *newenviron[] = { NULL };

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <file-to-exec>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    newargv[0] = argv[1];

    execve(argv[1], newargv, newenviron);
    perror("execve");   /* execve() 仅在出错时返回 */
    exit(EXIT_FAILURE);
}
```

我们可以使用第二个程序如下 exec 第一个程序：

```console
$ cc myecho.c -o myecho
$ cc execve.c -o execve
$ ./execve ./myecho
argv[0]: ./myecho
argv[1]: hello
argv[2]: world
```

我们还可以使用这些程序演示脚本解释器的使用。为此，我们创建一个“解释器”为 `myecho` 程序的脚本：

```console
$ cat > script
#!./myecho script-arg
^D
$ chmod +x script
```

然后我们可以使用我们的程序 exec 该脚本：

```console
$ ./execve ./script
argv[0]: ./myecho
argv[1]: script-arg
argv[2]: ./script
argv[3]: hello
argv[4]: world
```
