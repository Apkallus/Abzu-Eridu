### `execl`、`execlp`、`execle`、`execv`、`execvp`、`execvpe` - 执行一个文件

https://www.man7.org/linux/man-pages/man3/exec.3.html

#### 库

标准 C 库（`libc`，`-lc`）

#### 概要

```c
#include <unistd.h>

extern char **environ;

int execl(const char *path, const char *arg, ...
                /*, (char *) NULL */);
int execlp(const char *file, const char *arg, ...
                /*, (char *) NULL */);
int execle(const char *path, const char *arg, ...
                /*, (char *) NULL, char *const envp[] */);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execvpe(const char *file, char *const argv[], char *const envp[]);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）：

```c
execvpe():
    _GNU_SOURCE
```

#### 描述

`exec()` 函数族用新的进程映像替换当前进程映像。本手册页描述的函数构建在 [`execve(2)`] 之上。（有关替换当前进程映像的更多细节，参见 [`execve(2)`] 手册页。）

这些函数的第一个参数是要执行的文件的名称。

可以根据 `exec` 前缀后面的字母对这些函数进行分组。

##### `l` - `execl()`、`execlp()`、`execle()`

`const char *arg` 及后续省略号可视为 `arg0`、`arg1`、……、`argn`。它们共同描述一个由一个或多个指向以 null 结尾的字符串的指针组成的列表，该列表表示被执行程序可用的参数列表。按照惯例，第一个参数应指向与正在执行的文件相关联的文件名。参数列表必须由空指针终止；并且，由于这些是可变参数函数，该指针必须强制转换为 `(char *) NULL`。

与 `l` 系列函数不同，下面的 `v` 系列函数以向量形式指定被执行程序的命令行参数。

##### `v` - `execv()`、`execvp()`、`execvpe()`

`char *const argv[]` 参数是一个指针数组，其中的指针指向以 null 结尾的字符串，这些字符串表示新程序可用的参数列表。按照惯例，第一个参数应指向与正在执行的文件相关联的文件名。指针数组必须由空指针终止。

##### `e` - `execle()`、`execvpe()`

新进程映像的环境通过 `envp` 参数指定。`envp` 参数是一个指针数组，其中的指针指向以 null 结尾的字符串，并且必须由空指针终止。

所有其他 `exec()` 函数（后缀中不含 `e`）从调用进程中的外部变量 `environ` 获取新进程映像的环境。

##### `p` - `execlp()`、`execvp()`、`execvpe()`

如果指定的文件名不包含斜杠（`/`）字符，这些函数会复制 shell 在搜索可执行文件时的行为。将在 `PATH` 环境变量指定的、以冒号分隔的目录路径名列表中查找该文件。如果未定义此变量，则路径列表默认为一个列表，其中包含 `confstr(_CS_PATH)` 返回的目录（通常返回值为 `"/bin:/usr/bin"`），并且可能还包含当前工作目录；更多细节参见“版本”部分。

`execvpe()` 使用调用者环境中的 `PATH` 值搜索程序，而不是使用 `envp` 参数。

如果指定的文件名包含斜杠字符，则忽略 `PATH`，并执行指定路径名处的文件。

此外，某些错误会被特殊处理。

如果某个文件的权限被拒绝（尝试的 [`execve(2)`] 失败，错误为 `EACCES`），这些函数将继续搜索搜索路径的其余部分。然而，如果未找到其他文件，它们将返回，并将 `errno` 设置为 `EACCES`。

如果无法识别文件头（尝试的 [`execve(2)`] 失败，错误为 `ENOEXEC`），这些函数将执行 shell（`/bin/sh`），并将该文件的路径作为其第一个参数。（如果此尝试失败，则不再进行进一步搜索。）

所有其他 `exec()` 函数（后缀中不含 `p`）将标识要执行程序的（相对或绝对）路径名作为其第一个参数。

#### 返回值

`exec()` 函数仅在发生错误时返回。返回值为 `-1`，并设置 `errno` 以指示错误。

#### 错误

所有这些函数都可能失败，并针对 [`execve(2)`] 指定的任何错误设置 `errno`。

#### 属性

有关本节所用术语的解释，参见 [attributes(7)]。

| 接口 | 属性 | 值 |
| --- | --- | --- |
| `execl()`、`execle()`、`execv()` | 线程安全 | `MT-Safe` |
| `execlp()`、`execvp()`、`execvpe()` | 线程安全 | `MT-Safe env` |

#### 版本

默认搜索路径（当环境中不包含变量 `PATH` 时使用）在不同系统之间有所差异。它通常包含 `/bin` 和 `/usr/bin`（按此顺序），也可能包含当前工作目录。在其他一些系统上，当前工作目录被包含在 `/bin` 和 `/usr/bin` 之后，作为一项防木马措施。glibc 的实现长期遵循传统默认值，即当前工作目录包含在搜索路径的开头。然而，在 glibc 2.24 开发期间的一些代码重构导致当前工作目录被完全从默认搜索路径中移除。这一意外行为变更被认为略有裨益，并且不会被回退。

当尝试执行文件期间发生错误时，`execlp()` 和 `execvp()` 的行为是历史惯例，但传统上并未被记录，也未由 POSIX 标准规定。BSD（可能还有其他系统）在遇到 `ETXTBSY` 时会自动休眠并重试。Linux 将其视为硬错误并立即返回。

传统上，函数 `execlp()` 和 `execvp()` 会忽略除上述错误以及 `ENOMEM` 和 `E2BIG` 之外的所有错误，遇到这些错误时则返回。现在，如果发生上述错误以外的任何错误，它们都会返回。

#### 标准

- `environ`、`execl()`、`execlp()`、`execle()`、`execv()`、`execvp()`

  POSIX.1-2008。

- `execvpe()`

  GNU。

#### 历史

- `environ`、`execl()`、`execlp()`、`execle()`、`execv()`、`execvp()`

  POSIX.1-2001。

- `execvpe()`

  glibc 2.11。

#### 缺陷

在 glibc 2.24 之前，`execl()` 和 `execle()` 在内部使用 [`realloc(3)`]，因此不是异步信号安全的，违反了 POSIX.1 的要求。此问题已在 glibc 2.24 中修复。

##### 架构特定细节

在 `sparc` 和 `sparc64` 上，为了与 `SunOS` 兼容，内核将 `execv()` 作为系统调用提供（原型如上所示）。在这些架构上，`execv()` 包装函数并不使用该系统调用。

