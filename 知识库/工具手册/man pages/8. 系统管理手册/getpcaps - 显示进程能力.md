https://www.man7.org/linux/man-pages/man8/getpcaps.8.html

# `getpcaps` - 显示进程能力

## 概要

```sh
getpcaps [optional args] pid...
```

## 描述

`getpcaps` 显示命令行上给出的 `pid` 值所指示的进程的能力。`pid` 为 `0` 时显示正在运行 `getpcaps` 本身的进程的能力。

进程的能力 `Set` 以 [cap_text_formats(7)] 中描述的文本表示显示。

可选参数：

- `--help` 或 `--usage`  
  显示用法信息并退出。

- `--ugly` 或 `--legacy`  
  以略显丑陋的旧版格式显示输出。

- `--verbose`  
  以类似旧版但使用现代默认终端字体时不那么丑陋的格式显示用法。

- `--iab`  
  显示进程的 `IAB` 元组能力。此处的输出格式也在 [cap_text_formats(7)] 中描述。双引号括住常规进程能力，方括号括住 `IAB` 元组。此格式也由 [captree(8)] 使用。

## 报告缺陷

请通过以下地址引用的缺陷跟踪器报告缺陷：

<https://sites.google.com/site/fullycapable>

## 另请参阅

[capsh(1)]、[cap_from_text(3)]、[cap_iab(3)]、`cap_text_format(7)`、[capabilities(7)]、[captree(8)]、[getcap(8)] 和 [setcap(8)]。

## 作者

本手册页最初由 Robert Bihlmeyer <`robbe@debian.org`> 为 Debian GNU/Linux 系统编写（但可供他人使用）。

## 版本说明

本页是 *libcap*（能力命令和库）项目的一部分。项目信息可在 <https://sites.google.com/site/fullycapable/> 找到。若对本手册页有缺陷报告，请发送至 `morgan@kernel.org`（请在主题行中注明“libcap”）。本页取自该项目上游 Git 仓库 <https://git.kernel.org/pub/scm/libs/libcap/libcap.git/>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-07-30。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`2026-04-07` · `GETPCAPS(8)`