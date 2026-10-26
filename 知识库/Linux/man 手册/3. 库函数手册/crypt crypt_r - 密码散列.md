# crypt(3)

https://www.man7.org/linux/man-pages/man3/crypt.3.html

## 名称

`crypt`、`crypt_r` - 密码散列

## 库

密码散列库（`libcrypt`，`-lcrypt`）

## 概要

```c
#include <unistd.h>

char *crypt(const char *key, const char *salt);

#include <crypt.h>

char *crypt_r(const char *key, const char *salt,
              struct crypt_data *restrict data);
```

glibc 的特性测试宏要求（参见 [feature_test_macros(7)]）

- `crypt()`：
  - 自 glibc 2.28 起：`_DEFAULT_SOURCE`
  - glibc 2.27 及更早版本：`_XOPEN_SOURCE`

- `crypt_r()`：`_GNU_SOURCE`

## 描述

### `crypt()`

```c
char *crypt(const char *key, const char *salt);
```

`crypt()` 是密码散列函数。它基于数据加密标准（DES）算法，并带有一些变体，目的之一是阻止使用硬件实现进行密钥搜索。

- `key` 是用户输入的密码。
- `salt` 是从集合 `[a-zA-Z0-9./]` 中选择的两个字符组成的字符串。该字符串用于以 4096 种不同方式之一扰动算法。

通过取 `key` 前八个字符中每个字符的最低 7 位，可得到一个 56 位密钥。该 56 位密钥用于重复加密一个常量字符串（通常为全零字符串）。返回值指向散列后的密码，即一系列 13 个可打印 ASCII 字符（前两个字符表示盐值本身）。返回值指向静态数据，其内容会被每次调用覆盖。

> **警告：** 密钥空间包含 `2**56` 个可能值，等于 `7.2e16`。使用大规模并行计算机可以穷举搜索该密钥空间。已有软件（例如 `crack(1)`）可搜索人类通常用于密码的这部分密钥空间。因此，密码选择至少应避免常见单词和姓名。建议使用在选择过程中检查可破解密码的 [passwd(1)] 程序。

DES 算法本身有一些怪癖，使得 `crypt()` 接口除了密码认证之外不适合用于任何其他用途。如果你计划将 `crypt()` 接口用于密码学项目，不要这样做：找一本好的加密书籍，并使用一个广泛可用的 DES 库。

### `crypt_r()`

```c
char *crypt_r(const char *key, const char *salt,
              struct crypt_data *restrict data);
```

`crypt_r()` 是 `crypt()` 的可重入版本。`data` 指向的结构用于存储结果数据和簿记信息。除了分配该结构之外，调用者唯一应对该结构做的事情是在第一次调用 `crypt_r()` 之前将 `data->initialized` 设置为零。

## 返回值

成功时，返回指向散列后密码的指针。出错时，返回 `NULL`。

## 错误

- `EINVAL`：`salt` 格式错误。
- `ENOSYS`：`crypt()` 函数未实现，可能是因为美国出口限制。
- `EPERM`：`/proc/sys/crypto/fips_enabled` 具有非零值，并且尝试使用弱散列类型，例如 `DES`。

## 属性

有关本节所用术语的解释，参见 [attributes(7)]。

| 接口 | 属性 | 值 |
| --- | --- | --- |
| `crypt()` | 线程安全 | `MT-Unsafe race:crypt` |
| `crypt_r()` | 线程安全 | `MT-Safe` |

## 标准

- `crypt()`：POSIX.1-2008。
- `crypt_r()`：GNU。

## 历史

- `crypt()`：POSIX.1-2001、SVr4、4.3BSD。

### 在 glibc 中的可用性

`crypt()`、[encrypt(3)] 和 [setkey(3)] 函数是 POSIX.1-2008 XSI 加密选项组的一部分，并且是可选的。如果这些接口不可用，则符号常量 `_XOPEN_CRYPT` 要么未定义，要么定义为 -1，并且可以在运行时用 [sysconf(3)] 检查可用性。如果下游发行版已从 glibc crypt 切换到 `libxcrypt`，就可能是这种情况。在此类发行版中重新编译应用程序时，程序员必须检测 `_XOPEN_CRYPT` 是否不可用，并包含 `<crypt.h>` 以获取函数原型；否则，`libxcrypt` 是 ABI 兼容的直接替换。

## 备注

### glibc 中的特性

此函数的 glibc 版本支持额外的散列算法。

如果 `salt` 是以字符 `$id$` 开头的字符串，后跟一个可选以 `$` 结尾的字符串，则结果形式为：

```text
$id$salt$hashed
```

`id` 标识所使用的散列方法（而不是 DES），然后决定如何解释密码字符串的其余部分。支持以下 `id` 值：

- `1`：`MD5`
- `2a`：`Blowfish`（不在主线 glibc 中；在某些 Linux 发行版中添加）
- `5`：`SHA-256`（自 glibc 2.7 起）
- `6`：`SHA-512`（自 glibc 2.7 起）

因此，`$5$salt$hashed` 和 `$6$salt$hashed` 分别包含使用基于 `SHA-256` 和 `SHA-512` 的函数散列后的密码。

“`salt`”表示盐值中 `$id$` 之后最多 16 个字符。密码字符串的“`hashed`”部分是实际计算出的密码。该字符串的大小固定：

- `MD5`：22 个字符
- `SHA-256`：43 个字符
- `SHA-512`：86 个字符

“`salt`”和“`hashed`”中的字符取自集合 `[a-zA-Z0-9./]`。在 `MD5` 和 `SHA` 实现中，整个 `key` 都是重要的（而不是像 `DES` 中那样仅前 8 个字节）。

自 glibc 2.7 起，`SHA-256` 和 `SHA-512` 实现支持用户指定的散列轮数，默认值为 5000。如果盐中的 `$id$` 字符后跟 `rounds=xxx$`，其中 `xxx` 是整数，则结果形式为：

```text
$id$rounds=yyy$salt$hashed
```

其中 `yyy` 是实际使用的散列轮数。如果 `xxx` 小于 1000，则实际使用的轮数为 1000；如果 `xxx` 大于 999999999，则为 999999999；否则等于 `xxx`。

## 参见

[login(1)]、[passwd(1)]、[encrypt(3)]、[getpass(3)]、[passwd(5)]

## 版权页

本页是 `man-pages`（Linux 内核和 C 库用户空间接口文档）项目的一部分。项目信息可在 <https://www.kernel.org/doc/man-pages/> 找到。如果你对本手册页有错误报告，请参见 <https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/tree/CONTRIBUTING>。本页取自 2026-09-09 从 <https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/> 获取的 tarball `man-pages-6.19.tar.gz`。如果你发现本页 HTML 版本存在渲染问题，或者你认为有更好或更新的页面来源，或者对本 COLOPHON 中的信息（该信息不是原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

```text
Linux man-pages 6.19            2025-09-21                       crypt(3)
```