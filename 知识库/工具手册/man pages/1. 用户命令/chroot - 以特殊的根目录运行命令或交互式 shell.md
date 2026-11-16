https://www.man7.org/linux/man-pages/man1/chroot.1.html

# `chroot` - 以特殊的根目录运行命令或交互式 shell

## 概要

```sh
chroot [OPTION]... NEWROOT [COMMAND [ARG]...]
```

## 描述

以根目录设置为 `NEWROOT` 运行 `COMMAND`。

- `--groups=G_LIST`  
    以 `g1,g2,..,gN` 指定补充组

- `--userspec=USER:GROUP`  
    指定要使用的用户和组（ID 或名称）

- `--skip-chdir`  
    不将工作目录更改为 `/`

- `--help`  
    显示此帮助并退出

- `--version`  
    输出版本信息并退出

如果未给出命令，则运行 `"$SHELL" -i`（默认：`/bin/sh -i`）。

**退出状态：**

- `125`  
    如果 `chroot` 命令本身失败

- `126`  
    如果找到 `COMMAND` 但无法调用

- `127`  
    如果无法找到 `COMMAND`

- `-`  
    否则为 `COMMAND` 的退出状态

## 作者

由 Roland McGrath 编写。

## 报告缺陷

- 将缺陷报告发送至：`bug-coreutils@gnu.org`
- GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
- 使用 GNU 软件的一般帮助：<https://www.gnu.org/gethelp/>
- 将任何翻译缺陷报告至：<https://translationproject.org/team/>

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 `GPLv3+`：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参见

“chroot(2)”

完整文档：<https://www.gnu.org/software/coreutils/chroot>，或通过以下命令在本地获取：`info '(coreutils) chroot invocation'`

## 版本说明

本页是 `coreutils`（基本文件、shell 和文本操作实用程序）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页获取自 2026-08-03 从 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩ 下载的 tarball `coreutils-9.11.tar.xz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
GNU coreutils 9.11              April 2026                      CHROOT(1)
```