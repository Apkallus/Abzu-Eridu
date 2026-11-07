https://www.man7.org/linux/man-pages/man8/setcap.8.html

# `setcap` - 设置文件能力

## 概要

```sh
setcap [-q] [-n <rootuid>] [-v] {capabilities|-|-r} filename [ ... capabilitiesN fileN ]
```

## 描述

在未提供 `-v`（验证）选项时，`setcap` 将每个指定 `filename` 的能力设置为指定的 `capabilities`。可选的 `-n <rootuid>` 参数可用于设置文件能力，使其仅在以此 root 用户 ID 为所有者的用户命名空间中使用。`-v` 选项用于验证指定的能力当前是否与文件关联。如果同时提供 `-v` 和 `-n`，还会验证 `-n <rootuid>` 参数。

`capabilities` 集按照 [cap_text_formats(7)] 中描述的格式指定。

特殊能力字符串 `'-'` 可用于指示从标准输入读取能力。在这种情况下，能力集以空行终止。

特殊能力字符串 `'-r'` 用于从文件中移除能力集。注意，设置空能力集与移除它**并不相同**。空集可用于保证文件不会以特权执行，尽管当前生效的 `ambient+inheritable` 集原本会为执行的二进制文件授予能力。

`-f` 用于强制完成，即使该操作在某种程度上被视为无效操作。这可能会影响 `-r`，以及设置内核无法理解的文件能力。

`-q` 标志用于减少程序输出中的冗余信息。

## 退出码

`setcap` 程序成功时退出码为 `0`。失败时退出码为 `1`。

## 报告缺陷

请通过以下地址引用的缺陷跟踪器报告缺陷：

<https://sites.google.com/site/fullycapable>

## 另请参阅

[capsh(1)]、[cap_from_text(3)]、[cap_get_file(3)]、[cap_text_formats(7)]、[capabilities(7)]、[user_namespaces(7)]、[captree(8)]、[getcap(8)] 和 [getpcaps(8)]。

## 版本说明

本页是 *libcap*（能力命令和库）项目的一部分。项目信息可在 <https://sites.google.com/site/fullycapable/> 找到。若对本手册页有缺陷报告，请发送至 `morgan@kernel.org`（请在主题行中注明“libcap”）。本页取自该项目上游 Git 仓库 <https://git.kernel.org/pub/scm/libs/libcap/libcap.git/>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-07-30。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`2026-04-07` · `SETCAP(8)`