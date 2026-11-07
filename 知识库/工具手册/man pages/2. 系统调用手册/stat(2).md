# `stat`、`fstat`、`lstat`、`fstatat` — 获取文件状态

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#include <sys/stat.h>

int stat(const char *restrict path,
         struct stat *restrict statbuf);
int fstat(int fd, struct stat *statbuf);
int lstat(const char *restrict path,
         struct stat *restrict statbuf);

#include <fcntl.h>           /* Definition of AT_* constants */
#include <sys/stat.h>

int fstatat(int dirfd, const char *restrict path,
         struct stat *restrict statbuf, int flags);
```

glibc 的特性测试宏要求（见 `[feature_test_macros(7)]`）：

```c
lstat():
    /* Since glibc 2.20 */ _DEFAULT_SOURCE
        || _XOPEN_SOURCE >= 500
        || /* Since glibc 2.10: */ _POSIX_C_SOURCE >= 200112L
        || /* glibc 2.19 and earlier */ _BSD_SOURCE

fstatat():
    Since glibc 2.10:
        _POSIX_C_SOURCE >= 200809L
    Before glibc 2.10:
        _ATFILE_SOURCE
```

## 描述

这些函数在 `statbuf` 指向的缓冲区中返回关于文件的信息。对文件本身不需要任何权限，但——对于 `stat()`、`fstatat()` 和 `lstat()`——需要对 `path` 中通往该文件的所有目录具有执行（搜索）权限。

`stat()` 和 `fstatat()` 获取 `path` 所指向文件的信息；`fstatat()` 的差异如下所述。

`lstat()` 与 `stat()` 相同，区别在于如果 `path` 是符号链接，则它返回关于链接本身的信息，而不是链接所指向的文件。

`fstat()` 与 `stat()` 相同，区别在于要获取信息的文件由文件描述符 `fd` 指定。

### stat 结构

所有这些系统调用都返回一个 `stat` 结构（见 `[stat(3type)]`）。

*注意*：出于性能和简单性的考虑，`stat` 结构中的不同字段可能包含系统调用执行期间不同时刻的状态信息。例如，如果另一个进程通过调用 `[chmod(2)]` 或 `[chown(2)]` 更改了 `st_mode` 或 `st_uid`，`stat()` 可能返回旧的 `st_mode` 和新的 `st_uid`，或者旧的 `st_uid` 和新的 `st_mode`。

### fstatat()

`fstatat()` 系统调用是访问文件信息的更通用接口，它仍然可以提供 `stat()`、`lstat()` 和 `fstat()` 各自的确切行为。

如果 `path` 是相对路径，则它相对于文件描述符 `dirfd` 所引用的目录解释（而不是像 `stat()` 和 `lstat()` 对相对路径名那样相对于调用进程的当前工作目录）。

如果 `path` 是相对路径且 `dirfd` 是特殊值 `AT_FDCWD`，则 `path` 相对于调用进程的当前工作目录解释（像 `stat()` 和 `lstat()` 那样）。

如果 `path` 是绝对路径，则忽略 `dirfd`。

`flags` 可以是 0，或者包含以下一个或多个标志的按位 OR：

- `AT_EMPTY_PATH`（自 Linux 2.6.39）  
  如果 `path` 是空字符串（或自 Linux 6.11 起为 NULL），则操作 `dirfd` 所引用的文件（该文件可能通过 `[open(2)]` 的 `O_PATH` 标志获得）。在这种情况下，`dirfd` 可以引用任何类型的文件，而不仅仅是目录，`fstatat()` 的行为类似于 `fstat()`。如果 `dirfd` 是 `AT_FDCWD`，则调用操作当前工作目录。此标志是 Linux 特有的；定义 `_GNU_SOURCE` 以获取其定义。

- `AT_NO_AUTOMOUNT`（自 Linux 2.6.38）  
  不自动挂载 `path` 的终端（“基名”）组件。自 Linux 3.1 起此标志被忽略。自 Linux 4.11 起此标志为隐含。

- `AT_SYMLINK_NOFOLLOW`  
  如果 `path` 是符号链接，不解引用它：而是返回关于链接本身的信息，像 `lstat()` 那样。（默认情况下，`fstatat()` 解引用符号链接，像 `stat()` 那样。）

关于 `fstatat()` 必要性的解释，参见 `[openat(2)]`。

## 返回值

成功时返回 0。出错时返回 -1，并将 `errno` 设置为指示错误。

## 错误

- `EACCES`  
  对 `path` 路径前缀中的某个目录拒绝搜索权限。（另见 `[path_resolution(7)]`。）

- `EBADF`  
  `fd` 不是有效的打开文件描述符。

- `EBADF`（`fstatat()`）  
  `path` 是相对路径，但 `dirfd` 既不是 `AT_FDCWD` 也不是有效文件描述符。

- `EFAULT`  
  地址错误。

- `EINVAL`（`fstatat()`）  
  `flags` 中指定了无效标志。

- `ELOOP`  
  遍历路径时遇到太多符号链接。

- `ENAMETOOLONG`  
  `path` 太长。

- `ENOENT`  
  `path` 的某个组件不存在或是悬空符号链接。

- `ENOENT`  
  `path` 是空字符串且 `flags` 中未指定 `AT_EMPTY_PATH`。

- `ENOMEM`  
  内存不足（即内核内存）。

- `ENOTDIR`  
  `path` 路径前缀的某个组件不是目录。

- `ENOTDIR`（`fstatat()`）  
  `path` 是相对路径，且 `dirfd` 是指向非目录文件的文件描述符。

- `EOVERFLOW`  
  `path` 或 `fd` 引用的文件的大小、inode 编号或块数无法分别用 `off_t`、`ino_t` 或 `blkcnt_t` 类型表示。例如，当在 32 位平台上未使用 `-D_FILE_OFFSET_BITS=64` 编译的应用程序对大小超过 `(1<<31)-1` 字节的文件调用 `stat()` 时，可能发生此错误。

## 标准

POSIX.1-2024。

## 历史

- `stat`、`fstat`、`lstat`  
  SVr4、4.3BSD、POSIX.1-2001。

- `fstatat`  
  POSIX.1-2008。Linux 2.6.16，glibc 2.4。

根据 POSIX.1-2001，对符号链接调用 `lstat()` 只需在 `st_size` 字段和 `stat` 结构的 `st_mode` 字段的文件类型中返回有效信息。POSIX.1-2008 收紧了规范，要求 `lstat()` 在除 `st_mode` 中的模式位之外的所有字段中返回有效信息。

`st_blocks` 和 `st_blksize` 字段的使用可能可移植性较差。（它们是在 BSD 中引入的。不同系统之间的解释不同，涉及 NFS 挂载时甚至可能在单个系统上不同。）

### C 库/内核差异

随着时间的推移，`stat` 结构大小的增加导致在 i386 等 32 位平台上出现了三个相继的 `stat()` 版本：`sys_stat()`（槽位 `__NR_oldstat`）、`sys_newstat()`（槽位 `__NR_stat`）和 `sys_stat64()`（槽位 `__NR_stat64`）。前两个版本在 Linux 1.0 中就已存在（尽管名称不同）；最后一个在 Linux 2.4 中添加。类似的说明适用于 `fstat()` 和 `lstat()`。

不同版本处理的内核内部 `stat` 结构分别如下：

- `__old_kernel_stat`  
  原始结构，字段较窄，无填充。

- `stat`  
  更大的 `st_ino` 字段，并在结构各部分添加填充以允许未来扩展。

- `stat64`  
  更大的 `st_ino` 字段，更大的 `st_uid` 和 `st_gid` 字段以容纳 Linux-2.4 将 UID 和 GID 扩展到 32 位，以及各种其他扩大的字段和结构中进一步的填充。（各种填充字节最终在 Linux 2.6 中被消耗，随着 32 位设备 ID 和时间戳字段的纳秒组件的出现。）

glibc 的 `stat()` 包装函数向应用程序隐藏这些细节，调用内核提供的最新版本系统调用，并在旧二进制文件需要时重新打包返回的信息。

在现代 64 位系统上，情况更简单：只有一个 `stat()` 系统调用，内核处理包含足够大小字段的 `stat` 结构。

glibc 的 `fstatat()` 包装函数所使用的底层系统调用实际上名为 `fstatat64()`，或者在某些架构上名为 `newfstatat()`。

## 示例

以下程序调用 `lstat()` 并显示返回的 `stat` 结构中的选定字段。

```c
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/sysmacros.h>
#include <time.h>

int
main(int argc, char *argv[])
{
    struct stat sb;

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    if (lstat(argv[1], &sb) == -1) {
        perror("lstat");
        exit(EXIT_FAILURE);
    }

    printf("ID of containing device:  [%x,%x]\n",
           major(sb.st_dev),
           minor(sb.st_dev));

    printf("File type:                ");

    switch (sb.st_mode & S_IFMT) {
    case S_IFBLK:  printf("block device\n");            break;
    case S_IFCHR:  printf("character device\n");        break;
    case S_IFDIR:  printf("directory\n");               break;
    case S_IFIFO:  printf("FIFO/pipe\n");               break;
    case S_IFLNK:  printf("symlink\n");                 break;
    case S_IFREG:  printf("regular file\n");            break;
    case S_IFSOCK: printf("socket\n");                  break;
    default:       printf("unknown?\n");                break;
    }

    printf("I-node number:            %ju\n", (uintmax_t) sb.st_ino);

    printf("Mode:                     %jo (octal)\n",
           (uintmax_t) sb.st_mode);

    printf("Link count:               %ju\n", (uintmax_t) sb.st_nlink);
    printf("Ownership:                UID=%ju   GID=%ju\n",
           (uintmax_t) sb.st_uid, (uintmax_t) sb.st_gid);

    printf("Preferred I/O block size: %jd bytes\n",
           (intmax_t) sb.st_blksize);
    printf("File size:                %jd bytes\n",
           (intmax_t) sb.st_size);
    printf("Blocks allocated:         %jd\n",
           (intmax_t) sb.st_blocks);

    printf("Last status change:       %s", ctime(&sb.st_ctime));
    printf("Last file access:         %s", ctime(&sb.st_atime));
    printf("Last file modification:   %s", ctime(&sb.st_mtime));

    exit(EXIT_SUCCESS);
}
```

## 另请参见

`[ls(1)]`、`[stat(1)]`、`[access(2)]`、`[chmod(2)]`、`[chown(2)]`、`[readlink(2)]`、`[statx(2)]`、`[utime(2)]`、`[stat(3type)]`、`[capabilities(7)]`、`[inode(7)]`、`[symlink(7)]`

## 版权说明

本页面是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。有关该项目的信息可在 <https://www.kernel.org/doc/man-pages/> 找到。如果您对本手册页有错误报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页面取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 man-pages-6.19.tar.gz 压缩包。如果您发现此 HTML 版本页面存在渲染问题，或者您认为有更好或更新的页面来源，或者您对本版权说明（*不*属于原始手册页的一部分）中的信息有更正或改进，请发送邮件至 man-pages@man7.org。

Linux man-pages 6.19 2026-02-08 `stat`(2)