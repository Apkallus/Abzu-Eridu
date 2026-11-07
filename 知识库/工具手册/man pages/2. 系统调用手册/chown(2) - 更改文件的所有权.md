# `chown`, `fchown`, `lchown`, `fchownat` - 更改文件的所有权

https://man7.org/linux/man-pages/man2/chown.2.html

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#include <unistd.h>

int chown(const char *path, uid_t owner, gid_t group);
int fchown(int fd, uid_t owner, gid_t group);
int lchown(const char *path, uid_t owner, gid_t group);

#include <fcntl.h>           /* AT_* 常量的定义 */
#include <unistd.h>

int fchownat(int dirfd, const char *path,
             uid_t owner, gid_t group, int flags);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）：

```c
fchown(), lchown():
    /* 自 glibc 2.12 起： */ _POSIX_C_SOURCE >= 200809L
        || _XOPEN_SOURCE >= 500
        || /* glibc <= 2.19： */ _BSD_SOURCE

fchownat():
    自 glibc 2.10 起：
        _POSIX_C_SOURCE >= 200809L
    glibc 2.10 之前：
        _ATFILE_SOURCE
```

## 描述

这些系统调用更改文件的所有者和组。`chown()`、`fchown()` 和 `lchown()` 系统调用之间的区别仅在于如何指定文件：

- `chown()` 更改由 `path` 指定的文件的所有权；如果该文件是符号链接，则对其进行解引用。
- `fchown()` 更改由打开的文件描述符 `fd` 引用的文件的所有权。
- `lchown()` 与 `chown()` 类似，但不会解引用符号链接。

只有特权进程（Linux：具有 `CAP_CHOWN` 能力的进程）才能更改文件的所有者。文件的所有者可以将文件的组更改为该所有者所属的任意组。特权进程（Linux：具有 `CAP_CHOWN` 的进程）可以任意更改组。

如果 `owner` 或 `group` 指定为 `-1`，则不更改该 ID。

当非特权用户更改可执行文件的所有者或组时，`S_ISUID` 和 `S_ISGID` 模式位会被清除。POSIX 未规定 root 执行 `chown()` 时是否也应如此；Linux 行为取决于内核版本，并且自 Linux 2.2.13 起，root 与其他用户同等对待。对于非组可执行文件（即未设置 `S_IXGRP` 位的文件），`S_ISGID` 位表示强制锁定，并且不会因 `chown()` 而被清除。

当可执行文件的所有者或组被更改（由任何用户）时，该文件的所有能力集都会被清除。

### `fchownat()`

`fchownat()` 系统调用的操作方式与 `chown()` 完全相同，只是存在这里描述的差异。

如果 `path` 是相对路径，则它相对于文件描述符 `dirfd` 所引用的目录进行解释（而不是像 `chown()` 对相对路径名那样相对于调用进程的当前工作目录）。

如果 `path` 是相对路径且 `dirfd` 是特殊值 `AT_FDCWD`，则 `path` 相对于调用进程的当前工作目录进行解释（类似 `chown()`）。

如果 `path` 是绝对路径，则忽略 `dirfd`。

`flags` 参数是通过对以下零个或多个值进行 OR 运算创建的位掩码：

- `AT_EMPTY_PATH`（自 Linux 2.6.39 起）：如果 `path` 是空字符串，则对 `dirfd` 引用的文件进行操作（该文件可能已通过 [open(2)] 的 `O_PATH` 标志获得）。在这种情况下，`dirfd` 可以引用任何类型的文件，而不仅是目录。如果 `dirfd` 是 `AT_FDCWD`，则调用对当前工作目录进行操作。此标志是 Linux 特有的；定义 `_GNU_SOURCE` 以获取其定义。
- `AT_SYMLINK_NOFOLLOW`：如果 `path` 是符号链接，则不要解引用它：而是像 `lchown()` 一样对链接本身进行操作。（默认情况下，`fchownat()` 会像 `chown()` 一样解引用符号链接。）

参见 [openat(2)] 了解为什么需要 `fchownat()`。

## 返回值

成功时返回零。出错时返回 `-1`，并设置 [errno] 以指示错误。

## 错误

取决于文件系统，可能返回下面未列出的其他错误。

下面列出 `chown()` 的更通用错误。

- `EACCES`：路径前缀的某个组件上搜索权限被拒绝。（另见 [path_resolution(7)]。）
- `EBADF`（`fchown()`）：`fd` 不是有效的打开文件描述符。
- `EBADF`（`fchownat()`）：`path` 是相对路径，但 `dirfd` 既不是 `AT_FDCWD` 也不是有效的文件描述符。
- `EFAULT`：`path` 指向可访问地址空间之外。
- `EINVAL`（`fchownat()`）：`flags` 中指定了无效标志。
- `EIO`（`fchown()`）：修改 inode 时发生低级 I/O 错误。
- `ELOOP`：解析 `path` 时遇到过多符号链接。
- `ENAMETOOLONG`：`path` 太长。
- `ENOENT`：文件不存在。
- `ENOMEM`：可用内核内存不足。
- `ENOTDIR`：路径前缀的某个组件不是目录。
- `ENOTDIR`（`fchownat()`）：`path` 是相对路径，且 `dirfd` 是指向非目录文件的文件描述符。
- `EPERM`：调用进程没有更改所有者和/或组所需的权限（见上文）。
- `EPERM`：文件被标记为不可变或仅追加。（参见 [FS_IOC_SETFLAGS(2const)]。）
- `EROFS`：命名文件位于只读文件系统上。

## 版本

4.4BSD 版本只能由超级用户使用（也就是说，普通用户不能放弃文件）。

## 标准

POSIX.1-2024。

## 历史

- `chown()`：SVr4、POSIX.1-1988、4.4BSD。
- `fchown()`：SVr4、4.4BSD、SUSv1、POSIX.1-2001。
- `lchown()`：SVr4、4.4BSD、SUSv1、POSIX.1-2001 XSI、POSIX.1-2008。
- `fchownat()`：POSIX.1-2008。Linux 2.6.16，glibc 2.4。

## 注释

### 新文件的所有权

创建新文件时（例如通过 [open(2)] 或 [mkdir(2)]），其所有者被设置为创建进程的文件系统用户 ID。文件的组取决于一系列因素，包括文件系统类型、用于挂载文件系统的选项，以及父目录上是否启用了 set-group-ID 模式位。如果文件系统支持 `-o grpid`（或同义地 `-o bsdgroups`）和 `-o nogrpid`（或同义地 `-o sysvgroups`）[mount(8)] 选项，则规则如下：

- 如果文件系统以 `-o grpid` 挂载，则新文件的组与父目录的组相同。
- 如果文件系统以 `-o nogrpid` 挂载且父目录上禁用了 set-group-ID 位，则新文件的组与进程的文件系统 GID 相同。
- 如果文件系统以 `-o nogrpid` 挂载且父目录上启用了 set-group-ID 位，则新文件的组与父目录的组相同。

截至 Linux 4.12，`-o grpid` 和 `-o nogrpid` 挂载选项由 ext2、ext3、ext4 和 XFS 支持。不支持这些挂载选项的文件系统遵循 `-o nogrpid` 规则。

### glibc 注释

在 `fchownat()` 不可用的较旧内核上，glibc 包装函数会回退到使用 `chown()` 和 `lchown()`。当 `path` 是相对路径时，glibc 会基于 `/proc/self/fd` 中与 `dirfd` 参数对应的符号链接构造路径名。

### NFS

在启用了 UID 映射的 NFS 文件系统上，`chown()` 的语义被有意违反。此外，所有访问文件内容的系统调用的语义也被违反，因为 `chown()` 可能导致对已打开文件的立即访问撤销。客户端缓存可能导致从所有权已更改以允许某用户访问，到该用户能在其他客户端上实际访问该文件之间存在延迟。

### 历史细节

最初的 Linux `chown()`、`fchown()` 和 `lchown()` 系统调用仅支持 16 位用户和组 ID。随后，Linux 2.4 添加了 `chown32()`、`fchown32()` 和 `lchown32()`，支持 32 位 ID。glibc 的 `chown()`、`fchown()` 和 `lchown()` 包装函数会透明地处理不同内核版本之间的差异。

在 Linux 2.1.81 之前（2.1.46 除外），`chown()` 不会跟随符号链接。自 Linux 2.1.81 起，`chown()` 会跟随符号链接，并且新增了一个不跟随符号链接的系统调用 `lchown()`。自 Linux 2.1.86 起，这个新调用（其语义与旧 `chown()` 相同）获得了相同的系统调用号，而 `chown()` 获得了新引入的编号。

## 示例

以下程序将其第二个命令行参数中指定的文件的所有权更改为其第一个命令行参数中指定的值。新所有者可以指定为数字用户 ID，也可以指定为用户名（通过使用 [getpwnam(3)] 在系统密码文件中执行查找，将其转换为用户 ID）。

### 程序源码

```c
#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int
main(int argc, char *argv[])
{
    char           *endptr;
    uid_t          uid;
    struct passwd  *pwd;

    if (argc != 3 || argv[1][0] == '\0') {
        fprintf(stderr, "%s <owner> <file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    uid = strtol(argv[1], &endptr, 10);  /* 允许数字字符串 */

    if (*endptr != '\0') {         /* 不是纯数字字符串 */
        pwd = getpwnam(argv[1]);   /* 尝试获取用户名的 UID */
        if (pwd == NULL) {
            perror("getpwnam");
            exit(EXIT_FAILURE);
        }

        uid = pwd->pw_uid;
    }

    if (chown(argv[2], uid, -1) == -1) {
        perror("chown");
        exit(EXIT_FAILURE);
    }

    exit(EXIT_SUCCESS);
}
```

## 另见

[chgrp(1)]、[chown(1)]、[chmod(2)]、[flock(2)]、[path_resolution(7)]、[symlink(7)]

## 版权页

本页是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 <https://www.kernel.org/doc/man-pages/> 找到。若对本手册页有错误报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页获取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的压缩包 `man-pages-6.19.tar.gz`。如果你发现此 HTML 版本的页面有渲染问题，或认为有更好或更新的来源，或对 COLOPHON 中的信息有更正或改进（这些信息*不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

Linux man-pages 6.19            2026-02-08                       `chown`(2)