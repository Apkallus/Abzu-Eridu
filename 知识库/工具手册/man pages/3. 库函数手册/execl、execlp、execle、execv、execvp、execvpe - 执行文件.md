https://www.man7.org/linux/man-pages/man3/exec.3.html

# `execl`、`execlp`、`execle`、`execv`、`execvp`、`execvpe` - 执行文件

## 库

标准 C 库（`libc`，`-lc`）

## 概要

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

glibc 的特性测试宏要求（参见 `feature_test_macros(7)`）：

```c
execvpe():
    _GNU_SOURCE
```

## 描述

`exec()` 函数族用新的进程映像替换当前进程映像。本手册页描述的函数构建在 `execve(2)` 之上。（关于替换当前进程映像的更多细节，参见 `execve(2)` 手册页。）

这些函数的第一个参数是要执行的文件的名称。

这些函数可以根据 `exec` 前缀后的字母进行分组。

### l - `execl()`、`execlp()`、`execle()`

`const char *arg` 及其后的省略号可以看作 `arg0`、`arg1`、...、`argn`。它们一起描述一个指针列表，指向一个或多个以 null 结尾的字符串，表示可供被执行的程序使用的参数列表。按照惯例，第一个参数应指向与被执行文件关联的文件名。参数列表*必须*以 null 指针终止，并且由于这些是可变参数函数，此指针必须强制转换为 `(char *) NULL`。

与 `l` 函数相反，`v` 函数（见下文）将被执行程序的命令行参数指定为向量。

### v - `execv()`、`execvp()`、`execvpe()`

`char *const argv[]` 参数是一个指针数组，指向以 null 结尾的字符串，表示可供新程序使用的参数列表。按照惯例，第一个参数应指向与被执行文件关联的文件名。指针数组*必须*以 null 指针终止。

### e - `execle()`、`execvpe()`

新进程映像的环境通过 `envp` 参数指定。`envp` 参数是一个指针数组，指向以 null 结尾的字符串，并且*必须*以 null 指针终止。

所有其他 `exec()` 函数（后缀中不包含 `e` 的函数）从调用进程中的外部变量 `environ` 获取新进程映像的环境。

### p - `execlp()`、`execvp()`、`execvpe()`

如果指定的文件名不包含斜杠（`/`）字符，这些函数会复制 shell 搜索可执行文件的操作。文件在 `PATH` 环境变量指定的、以冒号分隔的目录路径名列表中搜索。如果未定义此变量，则路径列表默认为包含 `confstr(_CS_PATH)` 返回的目录（通常返回 `"/bin:/usr/bin"`）的列表，并且可能还包括当前工作目录；更多细节参见“版本”。

`execvpe()` 使用调用者环境中的 `PATH` 值搜索程序，而不是使用 `envp` 参数中的值。

如果指定的文件名包含斜杠字符，则忽略 `PATH`，并执行指定路径名处的文件。

此外，某些错误会被特殊处理。

如果对某个文件的权限被拒绝（尝试的 `execve(2)` 失败，错误为 `EACCES`），这些函数将继续搜索搜索路径的其余部分。但是，如果未找到其他文件，它们将返回，并将 `errno` 设置为 `EACCES`。

如果无法识别文件头（尝试的 `execve(2)` 失败，错误为 `ENOEXEC`），这些函数将以该文件的路径作为第一个参数执行 shell（`/bin/sh`）。（如果此尝试失败，则不再进行进一步搜索。）

所有其他 `exec()` 函数（后缀中不包含 `p` 的函数）将标识要执行的程序的（相对或绝对）路径名作为其第一个参数。

## 返回值

`exec()` 函数仅在发生错误时返回。返回值是 `-1`，并设置 `errno` 以指示错误。

## 错误

所有这些函数都可能失败，并为 `execve(2)` 指定的任何错误设置 `errno`。

## 属性

关于本节中使用的术语的解释，参见 `attributes(7)`。

| 接口 | 属性 | 值 |
| --- | --- | --- |
| `execl()`、`execle()`、`execv()` | 线程安全 | `MT-Safe` |
| `execlp()`、`execvp()`、`execvpe()` | 线程安全 | `MT-Safe env` |

## 版本

当环境不包含变量 `PATH` 时使用的默认搜索路径在不同系统之间有所差异。它通常包括 `/bin` 和 `/usr/bin`（按此顺序），并且可能还包括当前工作目录。在其他一些系统上，当前工作目录被包含在 `/bin` 和 `/usr/bin` 之后，作为防木马措施。glibc 实现长期遵循传统默认值，即将当前工作目录包含在搜索路径的开头。然而，在 glibc 2.24 开发期间的一些代码重构导致当前工作目录完全从默认搜索路径中删除。这一意外行为变化被认为稍有裨益，并且不会被还原。

`execlp()` 和 `execvp()` 在尝试执行文件时发生错误时的行为是历史惯例，但传统上未被记录，也不是 POSIX 标准规定的。BSD（可能还有其他系统）在遇到 `ETXTBSY` 时会自动睡眠并重试。Linux 将其视为硬错误并立即返回。

传统上，`execlp()` 和 `execvp()` 函数忽略上述错误以外的所有错误，以及 `ENOMEM` 和 `E2BIG`，在这些错误发生时返回。现在，如果发生上述错误以外的任何错误，它们都会返回。

## 标准

`environ`、`execl()`、`execlp()`、`execle()`、`execv()`、`execvp()` 符合 POSIX.1-2008。

`execvpe()` 是 GNU 扩展。

## 历史

`environ`、`execl()`、`execlp()`、`execle()`、`execv()`、`execvp()` 符合 POSIX.1-2001。

`execvpe()` 出现于 glibc 2.11。

## 缺陷

在 glibc 2.24 之前，`execl()` 和 `execle()` 内部使用 `realloc(3)`，因此不是异步信号安全的，违反了 POSIX.1 的要求。这在 glibc 2.24 中已修复。

### 体系结构特定细节

在 sparc 和 sparc64 上，`execv()` 由内核作为系统调用提供（原型如上所示），以兼容 SunOS。在这些体系结构上，`execv()` 包装函数不使用此函数。

## 另请参见

`sh(1)`、`execve(2)`、`execveat(2)`、`fork(2)`、`ptrace(2)`、`fexecve(3)`、`system(3)`、`environ(7)`

## 版本说明

本页是 `man-pages`（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/doc/man-pages/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>⟩。本页获取自 2026-09-09 从 ⟨<https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/>⟩ 下载的 tarball `man-pages-6.19.tar.gz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
Linux man-pages 6.19            2025-05-17                        exec(3)
```