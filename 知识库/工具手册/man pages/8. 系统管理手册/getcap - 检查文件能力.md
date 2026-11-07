https://www.man7.org/linux/man-pages/man8/getcap.8.html

# `getcap` - 检查文件能力

## 概要

```sh
getcap [-v] [-n] [-r] [-h] filename [ ... ]
```

## 描述

`getcap` 显示每个指定文件的名称和能力。

## 选项

- `-h`  
  打印快速用法。

- `-n`  
  打印与文件能力关联的任何非零用户命名空间 root 用户 ID 值。

- `-r`  
  启用递归搜索。

- `-v`  
  显示所有搜索到的条目，即使它们没有文件能力。

- `filename`  
  每行一个文件。

**注意：** `=` 的空值不等价于文件上省略（或移除）的能力。这对 Ambient 能力向量最为重要，因为具有 Ambient 能力的进程在执行具有 `=` 能力的文件时会丢失它们，但在执行省略文件能力的文件时会保留 Ambient 特权继承。这个特殊的空设置可用于阻止二进制文件以特权执行。有一段时间，内核尊重这种对 root 执行该文件的抑制，但内核开发者在数年后认为这种行为对超级用户来说出乎意料，并仅针对该用户身份撤销了它。对于进程树，可以使用 [capsh(1)] 的 `--mode` 选项来抑制 root 特权。

## 报告缺陷

请通过以下地址引用的缺陷跟踪器报告缺陷：

<https://sites.google.com/site/fullycapable>

## 另请参阅

[capsh(1)]、[cap_get_file(3)]、[cap_to_text(3)]、[capabilities(7)]、[user_namespaces(7)]、[captree(8)]、[getpcaps(8)] 和 [setcap(8)]。

## 版本说明

本页是 *libcap*（能力命令和库）项目的一部分。项目信息可在 <https://sites.google.com/site/fullycapable/> 找到。若对本手册页有缺陷报告，请发送至 `morgan@kernel.org`（请在主题行中注明“libcap”）。本页取自该项目上游 Git 仓库 <https://git.kernel.org/pub/scm/libs/libcap/libcap.git/>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-07-30。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`2026-04-07` · `GETCAP(8)`