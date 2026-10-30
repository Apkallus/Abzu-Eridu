https://man7.org/linux/man-pages/man3/unlink.3p.html

# `unlink`、`unlinkat` — 删除目录项

## 概要

```c
#include <unistd.h>

int unlink(const char *path);

#include <fcntl.h>

int unlinkat(int fd, const char *path, int flag);
```

## 描述

`unlink()` 函数应删除一个文件链接。如果 `path` 命名的是符号链接，`unlink()` 应删除 `path` 命名的符号链接，并且不应影响该符号链接内容所命名的任何文件或目录。否则，`unlink()` 应删除 `path` 所指向的路径名命名的链接，并递减该链接所引用文件的链接计数。

当文件的链接计数变为 0 且没有进程打开该文件时，该文件占用的空间应被释放，并且该文件应不再可访问。如果在删除最后一个链接时有一个或多个进程已打开该文件，则链接应在 `unlink()` 返回之前被删除，但文件内容的删除应推迟到对该文件的所有引用都关闭之后。

除非进程具有适当特权且实现支持对目录使用 `unlink()`，否则 `path` 参数不应命名目录。

成功完成后，`unlink()` 应将父目录的最后数据修改时间戳和最后文件状态更改时间戳标记为更新。此外，如果文件的链接计数不为 0，则应将该文件的最后文件状态更改时间戳标记为更新。

`unlinkat()` 函数应等价于 `unlink()` 或 `rmdir()` 函数，除非 `path` 指定相对路径。在这种情况下，要删除的目录项是相对于与文件描述符 `fd` 关联的目录确定的，而不是相对于当前工作目录。如果与文件描述符关联的打开文件描述的访问模式不是 `O_SEARCH`，则该函数应使用文件描述符底层目录的当前权限检查是否允许目录搜索。如果访问模式是 `O_SEARCH`，则该函数不应执行该检查。

`flag` 的值由 `<fcntl.h>` 中定义的以下列表中的标志按位包含或构造：

- `AT_REMOVEDIR`  
  将 `fd` 和 `path` 指定的目录项作为目录删除，而不是作为普通文件删除。

如果将特殊值 `AT_FDCWD` 传递给 `unlinkat()` 的 `fd` 参数，则应使用当前工作目录，并且行为应与调用 `unlink()` 或 `rmdir()`（分别取决于 `flag` 中是否设置了 `AT_REMOVEDIR` 位）完全相同。

## 返回值

成功完成后，这些函数应返回 `0`。否则，这些函数应返回 `-1` 并设置 `errno` 以指示错误。如果返回 `-1`，则命名的文件不应被更改。

## 错误

这些函数在以下情况下应失败且不应删除文件：

- `EACCES`  
  对路径前缀的某个组件拒绝搜索权限，或者对包含要删除目录项的目录拒绝写权限。

- `EBUSY`  
  `path` 参数命名的文件无法被删除，因为它正被系统或另一个进程使用，并且实现认为这是错误。

- `ELOOP`  
  在解析 `path` 参数期间遇到符号链接循环。

- `ENAMETOOLONG`  
  路径名某个组件的长度超过 `{NAME_MAX}`。

- `ENOENT`  
  `path` 的某个组件未命名现有文件，或 `path` 是空字符串。

- `ENOTDIR`  
  路径前缀的某个组件命名的是现有文件，而该文件既不是目录也不是指向目录的符号链接；或者 `path` 参数包含至少一个非斜杠字符并以一个或多个尾随斜杠字符结尾，且最后一个路径名组件命名的是现有文件，而该文件既不是目录也不是指向目录的符号链接。

- `EPERM`  
  `path` 命名的文件是目录，并且调用进程没有适当特权，或者实现禁止对目录使用 `unlink()`。

- `EPERM` 或 `EACCES`  
  包含 `path` 参数所引用文件的目录上设置了 `S_ISVTX` 标志，并且进程不满足 POSIX.1-2017 基础定义卷 *第 4.3 节*“目录保护”中指定的条件。

- `EROFS`  
  要删除的目录项是只读文件系统的一部分。

`unlinkat()` 函数在以下情况下应失败：

- `EACCES`  
  与 `fd` 关联的打开文件描述的访问模式不是 `O_SEARCH`，且 `fd` 底层目录的权限不允许目录搜索。

- `EBADF`  
  `path` 参数未指定绝对路径，且 `fd` 参数既不是 `AT_FDCWD` 也不是为读取或搜索而打开的有效文件描述符。

- `ENOTDIR`  
  `path` 参数不是绝对路径，且 `fd` 是与非目录文件关联的文件描述符。

- `EEXIST` 或 `ENOTEMPTY`  
  `flag` 参数设置了 `AT_REMOVEDIR` 位，且 `path` 参数命名的是非空目录，或者存在除点或点-点中单个条目之外的指向该目录的硬链接。

- `ENOTDIR`  
  `flag` 参数设置了 `AT_REMOVEDIR` 位，且 `path` 未命名目录。

这些函数在以下情况下可能失败且不删除文件：

- `EBUSY`  
  `path` 命名的文件是命名 `STREAM`。

- `ELOOP`  
  在解析 `path` 参数期间遇到超过 `{SYMLOOP_MAX}` 个符号链接。

- `ENAMETOOLONG`  
  路径名长度超过 `{PATH_MAX}`，或者符号链接的路径名解析产生了长度超过 `{PATH_MAX}` 的中间结果。

- `ETXTBSY`  
  要删除的条目是正在执行的纯过程（共享文本）文件的最后一个目录项。

`unlinkat()` 函数在以下情况下可能失败：

- `EINVAL`  
  `flag` 参数的值无效。

*以下各节仅供参考。*

## 示例

### 删除文件的链接

以下示例展示如何通过删除名为 `/modules/pass1` 的条目来删除指向名为 `/home/cnd/mod1` 的文件的链接。

```c
#include <unistd.h>

char *path = "/modules/pass1";
int   status;
...
status = unlink(path);
```

### 检查错误

以下示例片段创建一个名为 `LOCKFILE`（定义为 `/etc/ptmp`）的临时密码锁文件，并获取其文件描述符。如果无法以写方式打开该文件，则使用 `unlink()` 删除文件描述符与 `LOCKFILE` 之间的链接。

```c
#include <sys/types.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/stat.h>

#define LOCKFILE "/etc/ptmp"

int pfd;  /* 由 open 调用返回的文件描述符整数。 */
FILE *fpfd;  /* 用于 putpwent() 的文件指针。 */
...
/* 打开密码锁文件。如果它存在，这是错误。 */
if ((pfd = open(LOCKFILE, O_WRONLY| O_CREAT | O_EXCL, S_IRUSR
    | S_IWUSR | S_IRGRP | S_IROTH)) == -1)  {
    fprintf(stderr, "Cannot open /etc/ptmp. Try again later.\n");
    exit(1);
}

/* 锁文件已创建；继续对锁文件进行 fdopen，以便
   可以使用 putpwent()。
 */
if ((fpfd = fdopen(pfd, "w")) == NULL) {
    close(pfd);
    unlink(LOCKFILE);
    exit(1);
}
```

### 替换文件

以下示例片段使用 `unlink()` 丢弃文件的链接，以便可以用文件的新版本替换它们。如果发生错误，第一次调用删除指向 `LOCKFILE` 的链接。后续调用删除指向 `SAVEFILE` 和 `PASSWDFILE` 的链接，以便可以创建新链接，然后当不再需要时删除指向 `LOCKFILE` 的链接。

```c
#include <sys/types.h>
#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <sys/stat.h>

#define LOCKFILE "/etc/ptmp"
#define PASSWDFILE "/etc/passwd"
#define SAVEFILE "/etc/opasswd"
...
/* 如果未做任何更改，则假定出错并保持 passwd 不变。 */
if (!valid_change) {
    fprintf(stderr, "Could not change password for user %s\n", user);
    unlink(LOCKFILE);
    exit(1);
}

/* 更改新密码文件的权限。 */
chmod(LOCKFILE, S_IRUSR | S_IRGRP | S_IROTH);

/* 删除保存的密码文件。 */
unlink(SAVEFILE);

/* 保存当前密码文件。 */
link(PASSWDFILE, SAVEFILE);

/* 删除当前密码文件。 */
unlink(PASSWDFILE);

/* 将新密码文件保存为当前密码文件。 */
link(LOCKFILE,PASSWDFILE);

/* 删除锁文件。 */
unlink(LOCKFILE);

exit(0);
```

## 应用用法

应用程序应使用 `rmdir()` 删除目录。

## 原理

在许多历史实现中，删除目录仅限于超级用户，原因见 `link()`（另见 `rename()`）。

历史实现中 `[EBUSY]` 的含义是“挂载点忙”。由于 POSIX.1-2017 本卷不涉及挂载和卸载的系统管理概念，错误的描述改为“资源忙”。（当第二个进程尝试打开独占使用的设备时，某些设备驱动程序使用此含义。）该措辞还旨在允许实现在目录是任何进程的根目录或当前工作目录时拒绝删除该目录。

标准开发者审查了 TR 24715-2006，并注意到符合 LSB 的实现可能在删除目录时返回 `[EISDIR]` 而不是 `[EPERM]`。曾考虑通过将 `[EPERM]` 的要求改为 `[EPERM]` 或 `[EISDIR]` 来允许这种行为，但决定反对，因为这会破坏现有严格符合和符合标准的应用程序。为可移植到 POSIX.1-2008 和 LSB 而编写的应用程序应准备好处理任一错误码。

`unlinkat()` 函数的目的是删除当前工作目录之外目录中的目录项，而不暴露于竞态条件。文件的路径的任何部分都可能在与 `unlink()` 调用并行时被更改，导致未指定行为。通过为目标目录打开文件描述符并使用 `unlinkat()` 函数，可以保证被删除的目录项位于所需目录的相对位置。

## 未来方向

无。

## 另请参阅

[close(3p)]、[link(3p)]、[remove(3p)]、[rename(3p)]、[rmdir(3p)]、[symlink(3p)]

POSIX.1-2017 基础定义卷 *第 4.3 节*“目录保护”、[fcntl.h(0p)]、[unistd.h(0p)]

## 版权

本文部分内容从 IEEE Std 1003.1-2017《信息技术标准——可移植操作系统接口（POSIX），The Open Group 基础规范第 7 期，2018 年版》以电子形式重印和复制，版权 (C) 2018 归电气和电子工程师协会公司和 The Open Group 所有。如果本版本与原始 IEEE 和 The Open Group 标准之间存在任何差异，以原始 IEEE 和 The Open Group 标准为准。原始标准可在 <http://www.opengroup.org/unix/online.html> 在线获取。

本页中出现的任何排版或格式错误很可能是在将源文件转换为手册页格式期间引入的。要报告此类错误，请参见 <https://www.kernel.org/doc/man-pages/reporting_bugs.html>。

`IEEE/The Open Group` · 2017 · `UNLINK(3P)`