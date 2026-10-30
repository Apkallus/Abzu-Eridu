https://man7.org/linux/man-pages/man2/unlink.2.html

# `unlink`、`unlinkat` - 删除一个名称，可能还会删除该名称所引用的文件

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#include <unistd.h>

int unlink(const char *path);

#include <fcntl.h>           /* AT_* 常量的定义 */
#include <unistd.h>

int unlinkat(int dirfd, const char *path, int flags);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）：

```c
unlinkat():
    自 glibc 2.10 起：
        _POSIX_C_SOURCE >= 200809L
    在 glibc 2.10 之前：
        _ATFILE_SOURCE
```

## 描述

`unlink()` 从文件系统中删除一个名称。如果该名称是某个文件的最后一个链接，并且没有进程打开该文件，则该文件被删除，其占用的空间可被重新使用。

如果该名称是某个文件的最后一个链接，但仍有进程打开该文件，则该文件将继续存在，直到引用它的最后一个文件描述符被关闭。

如果该名称引用符号链接，则删除该链接。

如果该名称引用套接字、FIFO 或设备，则删除其名称，但已打开该对象的进程可以继续使用它。

### `unlinkat()`

`unlinkat()` 系统调用的操作方式与 `unlink()` 或 [rmdir(2)] 完全相同（取决于 `flags` 是否包含 `AT_REMOVEDIR` 标志），除了这里描述的差异。

如果 `path` 是相对路径，则它相对于文件描述符 `dirfd` 引用的目录来解释（而不是像 `unlink()` 和 [rmdir(2)] 对相对路径名那样相对于调用进程的当前工作目录）。

如果 `path` 是相对路径，且 `dirfd` 是特殊值 `AT_FDCWD`，则 `path` 相对于调用进程的当前工作目录来解释（类似 `unlink()` 和 [rmdir(2)]）。

如果 `path` 是绝对路径，则忽略 `dirfd`。

`flags` 是一个位掩码，可以指定为 `0`，或者通过按位或组合控制 `unlinkat()` 操作的标志值来指定。目前仅定义了一个这样的标志：

- `AT_REMOVEDIR`  
  默认情况下，`unlinkat()` 对 `path` 执行等同于 `unlink()` 的操作。如果指定 `AT_REMOVEDIR` 标志，则对 `path` 执行等同于 [rmdir(2)] 的操作。

关于 `unlinkat()` 必要性的说明，参见 [openat(2)]。

## 返回值

成功时返回零。出错时返回 `-1`，并设置 `errno` 以指示错误。

## 错误

- `EACCES`  
  进程的有效 UID 不允许对包含 `path` 的目录进行写访问，或者 `path` 中的某个目录不允许搜索权限。（另见 [path_resolution(7)]。）

- `EBUSY`  
  `path` 无法被删除，因为它正被系统或另一个进程使用；例如，它是一个挂载点，或者 NFS 客户端软件创建它来表示一个活动但无名的 inode（“NFS silly renamed”）。

- `EFAULT`  
  `path` 指向你的可访问地址空间之外。

- `EIO`  
  发生了 I/O 错误。

- `EISDIR`  
  `path` 引用目录。（这是自 Linux 2.1.132 起返回的非 POSIX 值。）

- `ELOOP`  
  在转换 `path` 时遇到太多符号链接。

- `ENAMETOOLONG`  
  `path` 太长。

- `ENOENT`  
  `path` 中的某个组件不存在或是悬空符号链接，或者 `path` 为空。

- `ENOMEM`  
  可用内核内存不足。

- `ENOTDIR`  
  `path` 中用作目录的组件实际上不是目录。

- `EPERM`  
  系统不允许删除目录，或者删除目录需要调用进程没有的特权。（这是 POSIX 规定的错误返回；如上所述，Linux 在这种情况下返回 `EISDIR`。）

- `EPERM`（仅 Linux）  
  文件系统不允许删除文件。

- `EPERM` 或 `EACCES`  
  包含 `path` 的目录设置了 sticky 位（`S_ISVTX`），并且进程的有效 UID 既不是要删除文件的 UID，也不是包含它的目录的 UID，并且进程没有特权（Linux：没有 `CAP_FOWNER` 能力）。

- `EPERM`  
  要删除的文件被标记为不可变或仅追加。（参见 [FS_IOC_SETFLAGS(2const)]。）

- `EROFS`  
  `path` 引用只读文件系统上的文件。

`unlink()` 和 [rmdir(2)] 发生的相同错误也可能发生在 `unlinkat()` 中。以下额外错误可能发生在 `unlinkat()` 中：

- `EBADF`  
  `path` 是相对路径，但 `dirfd` 既不是 `AT_FDCWD` 也不是有效文件描述符。

- `EINVAL`  
  `flags` 中指定了无效标志值。

- `EISDIR`  
  `path` 引用目录，且 `flags` 中未指定 `AT_REMOVEDIR`。

- `ENOTDIR`  
  `path` 是相对路径，而 `dirfd` 是引用非目录文件的文件描述符。

## 标准

POSIX.1-2024。

## 历史

- `unlink()`  
  SVr4、4.3BSD、POSIX.1-2001。

- `unlinkat()`  
  POSIX.1-2008。Linux 2.6.16，glibc 2.4。

### glibc

在 `unlinkat()` 不可用的较旧内核上，glibc 包装函数回退到使用 `unlink()` 或 [rmdir(2)]。当 `path` 是相对路径时，glibc 基于 `/proc/self/fd` 中对应于 `dirfd` 参数的符号链接构造路径名。

## 缺陷

NFS 底层协议中的不完善之处可能导致仍在使用的文件意外消失。

## 另请参阅

[rm(1)]、[unlink(1)]、[chmod(2)]、[link(2)]、[mknod(2)]、[open(2)]、[rename(2)]、[rmdir(2)]、[mkfifo(3)]、[remove(3)]、[path_resolution(7)]、[symlink(7)]

## 版本说明

本页是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 <https://www.kernel.org/doc/man-pages/> 找到。若对本手册页有缺陷报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 `man-pages-6.19.tar.gz` 压缩包。如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`Linux man-pages 6.19` · 2026-02-08 · `unlink(2)`