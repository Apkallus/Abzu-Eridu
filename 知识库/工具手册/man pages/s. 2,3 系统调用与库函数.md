
## `rename`、`renameat`、`renameat2` - 更改文件的名称或位置

### 库

标准 C 库（`libc`，`-lc`）

### 概要

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

`rename()` 重命名文件，必要时在目录之间移动它。

> 仅检查目录权限，而非文件权限

https://man7.org/linux/man-pages/man2/unlink.2.html

## `unlink`、`unlinkat` - 删除一个名称，可能还会删除该名称所引用的文件

### 库

标准 C 库（`libc`，`-lc`）

### 概要

```c
#include <unistd.h>

int unlink(const char *path);

#include <fcntl.h>           /* AT_* 常量的定义 */
#include <unistd.h>

int unlinkat(int dirfd, const char *path, int flags);
```

> 仅检查目录权限，而非文件权限



## `cbreak`、`echo`、`halfdelay`、`intrflush`、`is_cbreak`、`is_echo`、`is_nl`、`is_raw`、`keypad`、`meta`、`nl`、`nocbreak`、`nodelay`、`noecho`、`nonl`、`noqiflush`、`noraw`、`notimeout`、`qiflush`、`raw`、`timeout`、`wtimeout`、`typeahead` — 获取和设置 `curses` 终端输入选项


### cbreak, nocbreak

```c
int cbreak(void);
int nocbreak(void);
```

通常，终端驱动程序会缓冲输入的字符，直到输入换行或回车才将其传递给应用程序。这种规范（“cooked”）线路规程还支持软件流控制、简单的行编辑功能（字符和单词擦除，以及整行擦除或“kill”）和作业控制。

`cbreak` 将终端配置为 `cbreak mode`，该模式禁用行缓冲以及擦除和 kill 字符处理——中断、退出、挂起和流控制字符不受影响——并使用户输入的字符立即可供程序使用。

`nocbreak` 恢复规范（“cooked”）模式。

