https://man7.org/linux/man-pages/man2/rename.2.html

# `rename`、`renameat`、`renameat2` - 更改文件的名称或位置

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#include <stdio.h>

int rename(const char *oldpath, const char *newpath);

#include <fcntl.h>           /* AT_* 常量的定义 */
#include <stdio.h>

int renameat(int olddirfd, const char *oldpath,
             int newdirfd, const char *newpath);
int renameat2(int olddirfd, const char *oldpath,
              int newdirfd, const char *newpath, unsigned int flags);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）：

```c
renameat():
    自 glibc 2.10 起：
        _POSIX_C_SOURCE >= 200809L
    在 glibc 2.10 之前：
        _ATFILE_SOURCE

renameat2():
    _GNU_SOURCE
```

## 描述

`rename()` 重命名文件，必要时在目录之间移动它。对该文件的任何其他硬链接（由 [link(2)] 创建）不受影响。`oldpath` 的打开文件描述符也不受影响。

各种限制决定重命名操作是否成功：参见下面的“错误”。

如果 `newpath` 已存在，它将被原子替换，因此不存在某个时刻另一个进程尝试访问 `newpath` 时会发现它缺失。然而，可能会有一个窗口期，其中 `oldpath` 和 `newpath` 都引用正在被重命名的文件。

如果 `oldpath` 和 `newpath` 是引用同一文件的现有硬链接，则 `rename()` 不做任何事，并返回成功状态。

如果 `newpath` 存在但操作因某种原因失败，`rename()` 保证在适当位置保留 `newpath` 的一个实例。

`oldpath` 可以指定目录。在这种情况下，`newpath` 要么必须不存在，要么必须指定空目录。

如果 `oldpath` 引用符号链接，则重命名该链接；如果 `newpath` 引用符号链接，则该链接将被覆盖。

### `renameat()`

`renameat()` 系统调用的操作方式与 `rename()` 完全相同，除了这里描述的差异。

如果 `oldpath` 中给出的路径名是相对路径，则它相对于文件描述符 `olddirfd` 引用的目录来解释（而不是像 `rename()` 对相对路径名那样相对于调用进程的当前工作目录）。

如果 `oldpath` 是相对路径，且 `olddirfd` 是特殊值 `AT_FDCWD`，则 `oldpath` 相对于调用进程的当前工作目录来解释（类似 `rename()`）。

如果 `oldpath` 是绝对路径，则忽略 `olddirfd`。

`newpath` 的解释与 `oldpath` 相同，只是相对路径名相对于文件描述符 `newdirfd` 引用的目录来解释。

关于 `renameat()` 必要性的说明，参见 [openat(2)]。

### `renameat2()`

`renameat2()` 有一个额外的 `flags` 参数。`flags` 参数为零的 `renameat2()` 调用等价于 `renameat()`。

`flags` 参数是由以下零个或多个标志组成的位掩码：

- `RENAME_EXCHANGE`  
  原子交换 `oldpath` 和 `newpath`。两个路径名都必须存在，但类型可以不同（例如，一个可以是非空目录，另一个是符号链接）。

- `RENAME_NOREPLACE`  
  不覆盖重命名的 `newpath`。如果 `newpath` 已存在则返回错误。  
  
  `RENAME_NOREPLACE` 不能与 `RENAME_EXCHANGE` 一起使用。  
  
  `RENAME_NOREPLACE` 需要底层文件系统支持。对各种文件系统的支持添加如下：  
  - ext4（Linux 3.15）；  
  - btrfs、tmpfs 和 cifs（Linux 3.17）；  
  - xfs（Linux 4.0）；  
  - Linux 4.9 中添加了对许多其他文件系统的支持，包括 ext2、minix、reiserfs、jfs、vfat 和 bpf。

- `RENAME_WHITEOUT`（自 Linux 3.18 起）  
  此操作仅对 overlay/union 文件系统实现有意义。  
  
  指定 `RENAME_WHITEOUT` 会在执行重命名的同时，在重命名的源位置创建一个“whiteout”对象。整个操作是原子的，因此如果重命名成功，则 whiteout 也已被创建。  
  
  “whiteout”是在 union/overlay 文件系统构造中具有特殊含义的对象。在这些构造中，存在多个层，只有最顶层会被修改。上层上的 whiteout 会有效隐藏下层中匹配的文件，使其看起来好像该文件不存在。  
  
  当位于下层的文件被重命名时，该文件首先被复制到上层（如果尚未在上层），然后在上层读写层上重命名。同时，源文件需要被“whiteout”（以便下层中的源文件版本不可见）。整个操作需要原子完成。  
  
  当不属于 union/overlay 时，whiteout 显示为设备号为 `{0,0}` 的字符设备。（注意，其他 union/overlay 实现可能采用不同方法存储 whiteout 条目；具体来说，BSD union mount 使用单独的 inode 类型 `DT_WHT`，虽然 Linux 中可用的某些文件系统（如 CODA 和 XFS）支持它，但至少截至 Linux 4.19，内核的 whiteout 支持代码会忽略它。）  
  
  `RENAME_WHITEOUT` 需要与创建设备节点相同的特权（即 `CAP_MKNOD` 能力）。  
  
  `RENAME_WHITEOUT` 不能与 `RENAME_EXCHANGE` 一起使用。  
  
  `RENAME_WHITEOUT` 需要底层文件系统支持。支持它的文件系统包括 tmpfs（自 Linux 3.18 起）、ext4（自 Linux 3.18 起）、XFS（自 Linux 4.1 起）、f2fs（自 Linux 4.2 起）、btrfs（自 Linux 4.7 起）和 ubifs（自 Linux 4.9 起）。

## 返回值

成功时返回零。出错时返回 `-1`，并设置 `errno` 以指示错误。

## 错误

- `EACCES`  
  对包含 `oldpath` 或 `newpath` 的目录拒绝写权限，或者对 `oldpath` 或 `newpath` 路径前缀中的某个目录拒绝搜索权限，或者 `oldpath` 是目录且不允许写权限（需要更新 `..` 条目）。（另见 [path_resolution(7)]。）

- `EBUSY`  
  重命名失败，因为 `oldpath` 或 `newpath` 是某个进程正在使用的目录（可能作为当前工作目录、根目录，或因为已打开供读取），或正被系统使用（例如作为挂载点），而系统认为这是错误。（注意，在这种情况下没有要求返回 `EBUSY`——无论如何执行重命名都没有问题——但如果系统无法以其他方式处理这种情况，允许返回 `EBUSY`。）

- `EDQUOT`  
  用户在文件系统上的磁盘块配额已耗尽。

- `EFAULT`  
  `oldpath` 或 `newpath` 指向你的可访问地址空间之外。

- `EINVAL`  
  新路径名包含旧路径名的路径前缀，或者更一般地，试图使目录成为其自身的子目录。

- `EISDIR`  
  `newpath` 是现有目录，但 `oldpath` 不是目录。

- `ELOOP`  
  在解析 `oldpath` 或 `newpath` 时遇到太多符号链接。

- `EMLINK`  
  `oldpath` 已达到其最大链接数，或者它是一个目录，并且包含 `newpath` 的目录已达到最大链接数。

- `ENAMETOOLONG`  
  `oldpath` 或 `newpath` 太长。

- `ENOENT`  
  `oldpath` 命名的链接不存在；或者 `newpath` 中的某个目录组件不存在；或者 `oldpath` 或 `newpath` 是空字符串。

- `ENOMEM`  
  可用内核内存不足。

- `ENOSPC`  
  包含该文件的设备没有空间容纳新的目录项。

- `ENOTDIR`  
  `oldpath` 或 `newpath` 中用作目录的组件实际上不是目录。或者 `oldpath` 是目录，而 `newpath` 存在但不是目录。

- `ENOTEMPTY` 或 `EEXIST`  
  `newpath` 是非空目录，即包含除 `.` 和 `..` 之外的条目。

- `EPERM` 或 `EACCES`  
  包含 `oldpath` 的目录设置了 sticky 位（`S_ISVTX`），并且进程的有效用户 ID 既不是要删除文件的用户 ID，也不是包含它的目录的用户 ID，并且进程没有特权（Linux：没有 `CAP_FOWNER` 能力）；或者 `newpath` 是现有文件，并且包含它的目录设置了 sticky 位，并且进程的有效用户 ID 既不是被替换文件的用户 ID，也不是包含它的目录的用户 ID，并且进程没有特权（Linux：没有 `CAP_FOWNER` 能力）；或者包含 `oldpath` 的文件系统不支持所请求类型的重命名。

- `EROFS`  
  文件位于只读文件系统上。

- `EXDEV`  
  `oldpath` 和 `newpath` 不在同一已挂载文件系统上。（Linux 允许文件系统挂载在多个点，但 `rename()` 不能跨不同挂载点工作，即使同一文件系统挂载在两者上。）

以下额外错误可能发生在 `renameat()` 和 `renameat2()` 中：

- `EBADF`  
  `oldpath`（`newpath`）是相对路径，但 `olddirfd`（`newdirfd`）不是有效文件描述符。

- `ENOTDIR`  
  `oldpath` 是相对路径，而 `olddirfd` 是引用非目录文件的文件描述符；`newpath` 和 `newdirfd` 类似。

以下额外错误可能发生在 `renameat2()` 中：

- `EEXIST`  
  `flags` 包含 `RENAME_NOREPLACE` 且 `newpath` 已存在。

- `EINVAL`  
  `flags` 中指定了无效标志。

- `EINVAL`  
  `flags` 中同时指定了 `RENAME_NOREPLACE` 和 `RENAME_EXCHANGE`。

- `EINVAL`  
  `flags` 中同时指定了 `RENAME_WHITEOUT` 和 `RENAME_EXCHANGE`。

- `EINVAL`  
  文件系统不支持 `flags` 中的某个标志。

- `ENOENT`  
  `flags` 包含 `RENAME_EXCHANGE` 且 `newpath` 不存在。

- `EPERM`  
  `flags` 中指定了 `RENAME_WHITEOUT`，但调用者没有 `CAP_MKNOD` 能力。

## 标准

- `rename()`  
  C11、POSIX.1-2024。

- `renameat()`  
  POSIX.1-2024。

- `renameat2()`  
  Linux。

## 历史

- `rename()`  
  C89、POSIX.1-2001、4.3BSD。

- `renameat()`  
  POSIX.1-2008。Linux 2.6.16，glibc 2.4。

- `renameat2()`  
  Linux 3.15，glibc 2.28。

### glibc 说明

在 `renameat()` 不可用的较旧内核上，glibc 包装函数回退到使用 `rename()`。当 `oldpath` 和 `newpath` 是相对路径名时，glibc 基于 `/proc/self/fd` 中对应于 `olddirfd` 和 `newdirfd` 参数的符号链接构造路径名。

## 缺陷

在 NFS 文件系统上，不能假定如果操作失败，文件就没有被重命名。如果服务器执行了重命名操作然后崩溃，重新传输的 RPC 将在服务器恢复后处理时导致失败。应用程序应处理这种情况。类似问题参见 [link(2)]。

## 另请参阅

[mv(1)]、[rename(1)]、[chmod(2)]、[link(2)]、[symlink(2)]、[unlink(2)]、[path_resolution(7)]、[symlink(7)]

## 版本说明

本页是 *man-pages*（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 <https://www.kernel.org/doc/man-pages/> 找到。若对本手册页有缺陷报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 `man-pages-6.19.tar.gz` 压缩包。如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`Linux man-pages 6.19` · 2026-02-08 · `rename(2)`