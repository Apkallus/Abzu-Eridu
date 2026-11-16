https://man7.org/linux/man-pages/man8/setarch.8.html

# `setarch` - 在新程序环境中更改报告的体系结构，和/或设置 personality 标志

## 概要

```sh
setarch [arch] [options] [program [argument...]]

arch [options] [program [argument...]]
```

## 描述

`setarch` 修改执行域和进程 personality 标志。

执行域目前仅影响 `uname -m` 的输出。例如，在 AMD64 系统上运行 `setarch i386 program` 将使 `program` 看到 `i686` 而不是 `x86_64` 作为机器类型。默认 `program` 是 `/bin/sh`。

自版本 2.33 起，`arch` 命令行参数是可选的，`setarch` 可用于更改 personality 标志（`ADDR_LIMIT_3GB`、`SHORT_INODE` 等）而不修改执行域。

## 选项

- `--list`  
    列出 `setarch` 已知的体系结构。`setarch` 是否能够实际设置每种体系结构取决于正在运行的内核。

- `--show[=personality]`  
    显示当前活动的 personality 和标志。如果提供了 `personality` 参数，则显示该 personality 而不是当前的。`personality` 是一个十六进制数字，其可能值在 `sys/personality.h` 中描述。

- `-p`, `--pid=pid`  
    与 `--show` 一起使用时，显示指定进程的 personality 和标志。

- `--uname-2.6`  
    使指定的 `program` 看到以 2.6 开头的内核版本号。打开 `UNAME26`。

- `-v`, `--verbose`  
    详细模式。

- `-3`, `--3gb`  
    指定的 `program` 应使用最多 3GB 的地址空间。在 x86 上受支持。打开 `ADDR_LIMIT_3GB`。

- `--4gb`  
    此选项没有效果。仅为向后兼容而保留，可能会在未来的版本中移除。

- `-B`, `--32bit`  
    将地址空间限制为 32 位以模拟硬件。在 ARM 和 Alpha 上受支持。打开 `ADDR_LIMIT_32BIT`。

- `-F`, `--fdpic-funcptrs`  
    将用户空间信号处理函数指针视为地址描述符指针。此选项对不支持 `FDPIC` ELF 二进制文件的体系结构没有效果。在内核 v4.14 中，支持仅限于 ARM、Blackfin、Fujitsu FR-V 和 SuperH CPU 体系结构。

- `-I`, `--short-inode`  
    过时的错误模拟标志。打开 `SHORT_INODE`。

- `-L`, `--addr-compat-layout`  
    提供传统的虚拟地址空间布局。当 `program` 二进制文件没有 `PT_GNU_STACK` ELF 头时使用。打开 `ADDR_COMPAT_LAYOUT`。

- `-R`, `--addr-no-randomize`  
    禁用虚拟地址空间的随机化。打开 `ADDR_NO_RANDOMIZE`。

- `-S`, `--whole-seconds`  
    过时的错误模拟标志。打开 `WHOLE_SECONDS`。

- `-T`, `--sticky-timeouts`  
    使 `select(2)`、`pselect(2)` 和 `ppoll(2)` 系统调用保留超时值，而不是在被信号处理函数中断时将其修改为反映未睡眠的时间。当 `program` 依赖此行为时使用。更多详情请参见 `select(2)` 手册页中的超时描述。打开 `STICKY_TIMEOUTS`。

- `-X`, `--read-implies-exec`  
    如果设置了此项，则 `mmap(2)` 的 `PROT_READ` 也将添加 `PROT_EXEC` 位——如传统 x86 二进制文件所预期。请注意，ELF 加载器在遇到传统二进制文件时会自动设置此位。打开 `READ_IMPLIES_EXEC`。

- `-Z`, `--mmap-page-zero`  
    SVr4 错误模拟，将 `mmap(2)` 的零页设置为只读。当 `program` 依赖此行为且源代码不可用于修复时使用。打开 `MMAP_PAGE_ZERO`。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-V`, `--version`  
    显示版本并退出。

## 示例

```sh
setarch --addr-no-randomize mytestprog
setarch ppc32 rpmbuild --target=ppc --rebuild foo.src.rpm
setarch ppc32 -vL3 rpmbuild --target=ppc --rebuild bar.src.rpm
setarch ppc32 --32bit rpmbuild --target=ppc --rebuild foo.src.rpm
setarch --show
setarch --show=$(cat /proc/9284/personality)
setarch --show --pid 9284
```

## 作者

Elliot Lee <sopwith@redhat.com>，Jindrich Novy <jnovy@redhat.com>，Karel Zak <kzak@redhat.com>

## 另请参见

“personality(2)”、“select(2)”、“proc_pid_personality(5)”

## 报告缺陷

关于缺陷报告，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`setarch` 命令是 util-linux 包的一部分，可从 Linux 内核存档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 `util-linux`（一个 Linux 实用程序的随机集合）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页获取自项目上游 Git 仓库 ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
util-linux 2.43.devel-739-eee2e 2026-05-24                     SETARCH(8)
```