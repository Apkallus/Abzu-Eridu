https://man7.org/linux/man-pages/man2/setresuid.2.html

# `setresuid`、`setresgid` - 设置实际、有效和保存的用户或组 ID

## 库

标准 C 库（`libc`，`-lc`）

## 概要

```c
#define _GNU_SOURCE         /* 参见 feature_test_macros(7) */
#include <unistd.h>

int setresuid(uid_t ruid, uid_t euid, uid_t suid);
int setresgid(gid_t rgid, gid_t egid, gid_t sgid);
```

## 描述

`setresuid()` 设置调用进程的实际用户 ID、有效用户 ID 和保存的 set-user-ID。

非特权进程可以将其实际 UID、有效 UID 和保存的 set-user-ID 分别更改为以下之一：当前实际 UID、当前有效 UID 或当前保存的 set-user-ID。

特权进程（在 Linux 上，具有 `CAP_SETUID` 能力的进程）可以将其实际 UID、有效 UID 和保存的 set-user-ID 设置为任意值。

如果其中一个参数等于 `-1`，则相应的值不会更改。

无论对实际 UID、有效 UID 和保存的 set-user-ID 做出什么更改，文件系统 UID 始终设置为与（可能新的）有效 UID 相同的值。

完全类似地，`setresgid()` 设置调用进程的实际 GID、有效 GID 和保存的 set-group-ID（并且始终将文件系统 GID 修改为与有效 GID 相同），对非特权进程具有相同的限制。

## 返回值

成功时返回零。出错时返回 `-1`，并设置 `errno` 以指示错误。

*注意*：在某些情况下，即使调用者是 UID 0，`setresuid()` 也可能失败；忽略检查 `setresuid()` 的失败返回是严重的安全错误。

## 错误

- `EAGAIN`  
    该调用会更改调用者的实际 UID（即 `ruid` 与调用者的实际 UID 不匹配），但在分配必要的内核数据结构时发生了临时失败。

- `EAGAIN`  
    `ruid` 与调用者的实际 UID 不匹配，并且此调用会使属于实际用户 ID `ruid` 的进程数超过调用者的 `RLIMIT_NPROC` 资源限制。自 Linux 3.1 起，此错误情况不再发生（但健壮的应用程序应检查此错误）；参见 `execve(2)` 中 `EAGAIN` 的描述。

- `EINVAL`  
    一个或多个目标用户或组 ID 在此用户命名空间中无效。

- `EPERM`  
    调用进程没有特权（在其用户命名空间中没有必要的能力），并尝试将 ID 更改为不允许的值。对于 `setresuid()`，必要的能力是 `CAP_SETUID`；对于 `setresgid()`，是 `CAP_SETGID`。

## 版本

### C 库/内核差异

在内核层面，用户 ID 和组 ID 是每线程属性。然而，POSIX 要求进程中的所有线程共享相同的凭据。NPTL 线程实现通过为各种更改进程 UID 和 GID 的系统调用提供包装函数来满足 POSIX 要求。这些包装函数（包括 `setresuid()` 和 `setresgid()` 的包装函数）采用基于信号的技术，以确保当一个线程更改凭据时，进程中的所有其他线程也会更改其凭据。详情请参见 `nptl(7)`。

## 标准

POSIX.1-2024。

## 历史

POSIX.1-2024。Linux 2.1.44，glibc 2.3.2。HP-UX、FreeBSD。

最初的 Linux `setresuid()` 和 `setresgid()` 系统调用仅支持 16 位用户和组 ID。随后，Linux 2.4 添加了 `setresuid32()` 和 `setresgid32()`，支持 32 位 ID。glibc 的 `setresuid()` 和 `setresgid()` 包装函数透明地处理内核版本之间的差异。

## 另请参见

“getresuid(2)”、“getuid(2)”、“setfsgid(2)”、“setfsuid(2)”、“setreuid(2)”、“setuid(2)”、“capabilities(7)”、“credentials(7)”、“user_namespaces(7)”

## 版本说明

本页是 `man-pages`（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/doc/man-pages/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>⟩。本页获取自 2026-09-09 从 ⟨<https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/>⟩ 下载的 tarball `man-pages-6.19.tar.gz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
Linux man-pages 6.19            2026-02-08                   setresuid(2)
```