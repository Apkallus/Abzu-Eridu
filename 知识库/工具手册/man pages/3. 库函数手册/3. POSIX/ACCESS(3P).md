# `access`、`faccessat` — 确定文件描述符的可访问性

https://man7.org/linux/man-pages/man3/access.3p.html

## 概要

```c
#include <unistd.h>

int access(const char *path, int amode);

#include <fcntl.h>

int faccessat(int fd, const char *path, int amode, int flag);
```

## 描述

`access()` 函数应检查由 `path` 参数指向的路径名所命名的文件，根据 `amode` 中包含的位模式检查其可访问性。可访问性检查（包括路径名解析期间检查的目录权限）应使用真实用户 ID 代替有效用户 ID，并使用真实组 ID 代替有效组 ID 执行。

`amode` 的值要么是要检查的访问权限（`R_OK`、`W_OK`、`X_OK`）的按位包含 OR，要么是存在性测试（`F_OK`）。

如果检查任何访问权限，应按照 POSIX.1‐2017 基础定义卷 *第 4.5 节*，*文件访问权限* 中所述分别检查每一项，但该描述中针对具有适当特权的进程引用执行权限的情况除外：即使未向任何用户授予执行权限，实现也可以为 `X_OK` 指示成功。

`faccessat()` 函数在 `flag` 值为零时调用，应等效于 `access()` 函数，但 `path` 指定相对路径的情况除外。在这种情况下，要确定可访问性的文件应相对于与文件描述符 `fd` 关联的目录定位，而不是相对于当前工作目录。如果与文件描述符关联的打开文件描述的访问模式不是 `O_SEARCH`，函数应使用文件描述符底层目录的当前权限检查是否允许目录搜索。如果访问模式是 `O_SEARCH`，函数不应执行该检查。

如果将特殊值 `AT_FDCWD` 传递给 `faccessat()` 的 `fd` 参数，应使用当前工作目录，并且如果 `flag` 为零，行为应与调用 `access()` 完全相同。

`flag` 的值由以下列表中的标志按位包含 OR 构造，这些标志定义在 `<fcntl.h>` 中：

- `AT_EACCESS`：可访问性检查（包括路径名解析期间检查的目录权限）应使用有效用户 ID 和组 ID 执行，而不是像调用 `access()` 所要求的那样使用真实用户 ID 和组 ID。

## 返回值

成功完成后，这些函数应返回 0。否则，这些函数应返回 -1 并将 `errno` 设置为指示错误。

## 错误

这些函数在以下情况下应失败：

- `EACCES`：文件模式的权限位不允许请求的访问，或路径前缀的某个组件拒绝搜索权限。
- `ELOOP`：解析 `path` 参数期间遇到符号链接中存在循环。
- `ENAMETOOLONG`：路径名某个组件的长度超过 `{NAME_MAX}`。
- `ENOENT`：`path` 的某个组件未命名现有文件，或 `path` 是空字符串。
- `ENOTDIR`：路径前缀的某个组件命名了一个现有文件，该文件既不是目录也不是指向目录的符号链接；或者 `path` 参数至少包含一个非斜杠字符并以一个或多个尾随斜杠字符结尾，且最后一个路径名组件命名了一个现有文件，该文件既不是目录也不是指向目录的符号链接。
- `EROFS`：请求对只读文件系统上的文件进行写访问。

`faccessat()` 函数在以下情况下应失败：

- `EACCES`：与 `fd` 关联的打开文件描述的访问模式不是 `O_SEARCH`，且 `fd` 底层目录的权限不允许目录搜索。
- `EBADF`：`path` 参数未指定绝对路径，且 `fd` 参数既不是 `AT_FDCWD`，也不是为读取或搜索而打开的有效文件描述符。
- `ENOTDIR`：`path` 参数不是绝对路径，且 `fd` 是与非目录文件关联的文件描述符。

这些函数在以下情况下可能失败：

- `EINVAL`：`amode` 参数的值无效。
- `ELOOP`：解析 `path` 参数期间遇到超过 `{SYMLOOP_MAX}` 个符号链接。
- `ENAMETOOLONG`：路径名长度超过 `{PATH_MAX}`，或者符号链接的路径名解析产生的中间结果长度超过 `{PATH_MAX}`。
- `ETXTBSY`：请求对正在执行的纯过程（共享文本）文件进行写访问。

`faccessat()` 函数在以下情况下可能失败：

- `EINVAL`：`flag` 参数的值无效。

*以下各节为资料性内容。*

## 示例

### 测试文件是否存在

以下示例测试 `/tmp` 目录中是否存在名为 `myfile` 的文件。

```c
#include <unistd.h>
...
int result;
const char *pathname = "/tmp/myfile";

result = access (pathname, F_OK);
```

## 应用用法

不建议使用这些函数，因为到返回的信息被处理时，它已经过时。（也就是说，处理该信息总是会导致检查时间到使用时间（time-of-check-to-time-of-use）的竞态条件。）应用程序应改为尝试执行该操作本身，并处理文件不可访问时发生的 `[EACCES]` 错误（在需要使用 `access()` 或未使用 `AT_EACCES` 的 `faccessat()` 的情况下，事先更改有效用户和组 ID，之后也许再改回。）

历史上，`access()` 的用途之一是在设置用户 ID 为 root 的程序中检查运行程序的用户是否有权访问文件。这依赖于“超级用户”特权，该特权基于有效用户 ID 为零而授予，因此当 `access()` 使用真实用户 ID 检查可访问性时，这些特权不会被考虑在内。在较新的系统上，可以分配与用户或组 ID 无关联的特权；如果具有此类特权的程序调用 `access()`，ID 的更改对这些特权没有影响，因此它们会在可访问性检查中被考虑在内。因此，在此类程序中，`access()`（以及 `flag` 为零的 `faccessat()`）不能用于这一历史目的。同样，如果系统提供任何不基于用户 ID 的附加或替代文件访问控制机制，它们仍会被考虑在内。

如果使用相对路径名，则不考虑当前目录（或与文件描述符 `fd` 关联的目录）是否可通过任何绝对路径名访问。因此，使用 `access()` 或未使用 `AT_EACCES` 的 `faccessat()` 的应用程序可能会表现得好像文件对具有进程真实用户 ID 和组 ID 的用户可访问，而实际上该用户无法访问该文件，因为在文件层次结构中当前目录（或与文件描述符 `fd` 关联的目录）之上的某个位置访问会被拒绝。

如果将 `access()` 或 `faccessat()` 与 `W_OK` 一起使用来检查对设置了 `S_ISVTX` 位的目录的写访问，返回指示目录可写的值可能会产生误导，因为基于目录中文件的所有权，某些对目录中文件的操作将不被允许（见 POSIX.1‐2017 基础定义卷 *第 4.3 节*，*目录保护*）。

除描述中定义的集合之外，`amode` 的其他值可能有效；例如，如果系统具有扩展访问控制。

将 `AT_EACCESS` 值用于 `flag` 可启用 `access()` 中不可用的功能。

## 基本原理

在早期提案中，`access()` 函数的一些不足导致了 `eaccess()` 函数的创建，因为：

1. `access()` 的历史实现在进程真实用户 ID 为超级用户时不能正确测试文件访问。特别是，它们在测试执行权限时总是返回零，而不考虑文件是否可执行。
2. 超级用户对系统上的所有文件具有完全访问权限。因此，由超级用户启动并切换到权限较低的有效用户 ID 的程序不能使用 `access()` 来测试其文件访问权限。

然而，`eaccess()` 的历史模型并未解决问题 (1)，因此本卷 POSIX.1‐2017 现在允许 `access()` 以期望的方式行为，因为若干实现已经纠正了该问题。还有人认为，问题 (2) 更容易通过适当使用 `open()`、`chdir()` 或某个 `exec` 函数并响应错误来解决，而不是创建一个不那么可靠的新函数。因此，`eaccess()` 未包含在本卷 POSIX.1‐2017 中。

关于适当特权和执行权限位的句子反映了历史实现在检查超级用户对 `X_OK` 的访问时实现的两种可能性。

不鼓励新实现返回 `X_OK`，除非至少设置了一个执行权限位。

`faccessat()` 函数的目的是能够检查当前工作目录以外的目录中文件的可访问性，而不会暴露于竞态条件。文件路径的任何部分都可能在调用 `access()` 的同时被更改，从而导致未指定行为。通过为目标目录打开文件描述符并使用 `faccessat()` 函数，可以保证测试可访问性的文件相对于所需目录定位。

## 未来方向

这些函数可能会在本标准的未来版本中被正式弃用（例如，通过将其遮蔽为 `OB`）。

## 另请参见

`[chmod(3p)]`、`[fstatat(3p)]`

POSIX.1‐2017 基础定义卷，*第 4.5 节*，*文件访问权限*，`[fcntl.h(0p)]`，`[unistd.h(0p)]`

## 版权

本文本的部分内容以电子形式重印和复制自 IEEE Std 1003.1-2017，Standard for Information Technology -- Portable Operating System Interface (POSIX), The Open Group Base Specifications Issue 7, 2018 Edition，Copyright (C) 2018 by the Institute of Electrical and Electronics Engineers, Inc and The Open Group。如果本版本与原始 IEEE 和 The Open Group 标准之间存在任何差异，以原始 IEEE 和 The Open Group 标准为准。原始标准可在线获取：<http://www.opengroup.org/unix/online.html>。

本页面中出现的任何排版或格式错误很可能是在源文件转换为 man page 格式期间引入的。要报告此类错误，请参见 <https://www.kernel.org/doc/man-pages/reporting_bugs.html>。

IEEE/The Open Group 2017 `ACCESS`(3P)

---

引用此页面的页面：`[unistd.h(0p)]`、`[ex(1p)]`、`[chmod(3p)]`、`[faccessat(3p)]`、`[fstatat(3p)]`