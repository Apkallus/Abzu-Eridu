# `chown` — 更改文件所有者和组

https://man7.org/linux/man-pages/man1/chown.1.html

## 概要

```sh
chown [OPTION]... [OWNER][:[GROUP]] FILE...
chown [OPTION]... --reference=RFILE FILE...
```

## 描述

本手册页记录 GNU 版本的 `chown`。`chown` 更改每个给定文件的用户和/或组所有权。
- 如果只给出所有者（用户名或数字用户 ID），则该用户成为每个给定文件的所有者，文件的组不变。
- 如果所有者后跟冒号和组名（或数字组 ID），且两者之间没有空格，则文件的所有权也会更改。
- 如果用户名后跟冒号但没有组名，则该用户成为文件的所有者，文件的组更改为该用户的登录组。
- 如果给出了冒号和组，但省略了所有者，则只更改文件的组；在这种情况下，`chown` 执行与 `chgrp` 相同的功能。
- 如果只给出冒号，或者整个操作数为空，则所有者和组都不更改。

## 选项

将每个 `FILE` 的所有者和/或组更改为 `OWNER` 和/或 `GROUP`。使用 `--reference` 时，将每个 `FILE` 的所有者和组更改为 `RFILE` 的所有者和组。

- `-c`, `--changes`：类似详细输出，但仅在发生更改时报告
- `-f`, `--silent`, `--quiet`：抑制大多数错误消息
- `-v`, `--verbose`：对处理的每个文件输出诊断信息
- `--dereference`：影响每个符号链接的引用对象（这是默认行为），而不是符号链接本身
- `-h`, `--no-dereference`：影响符号链接，而不是任何引用文件；仅在可以更改符号链接所有权的系统上有用
- `--from=CURRENT_OWNER:CURRENT_GROUP`：仅当每个文件的当前所有者和/或组与此处指定的值匹配时，才更改其所有权。两者均可省略，此时省略的属性不要求匹配
- `--no-preserve-root`：不特殊对待 `/`（默认）
- `--preserve-root`：拒绝对 `/` 进行递归操作
- `--reference=RFILE`：使用 `RFILE` 的所有权而不是指定值。如果 `RFILE` 是符号链接，总是解引用
- `-R`, `--recursive`：递归操作文件和目录

以下选项修改在还指定了 `-R` 选项时遍历层次结构的方式。如果指定了多个，只有最后一个生效。`-P` 是默认值。

- `-H`：如果命令行参数是指向目录的符号链接，则遍历它
- `-L`：遍历遇到的每个指向目录的符号链接
- `-P`：不遍历任何符号链接
- `--help`：显示此帮助并退出
- `--version`：输出版本信息并退出

如果缺少所有者，则所有者不变。如果缺少组，则组不变；但如果符号 `OWNER` 后跟 `:` 暗示了登录组，则组会改为该用户的登录组。`OWNER` 和 `GROUP` 可以是数字，也可以是符号名称。

## 示例

```sh
chown root /u
```

将 `/u` 的所有者更改为 `root`。

```sh
chown root:staff /u
```

同样，但将其组也更改为 `staff`。

```sh
chown -hR root /u
```

将 `/u` 及其子文件的所有者更改为 `root`。

## 作者

由 David MacKenzie 和 Jim Meyering 编写。

## 报告错误

报告错误至：`bug-coreutils@gnu.org`  
GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>  
使用 GNU 软件的一般帮助：<https://www.gnu.org/gethelp/>  
报告任何翻译错误至 <https://translationproject.org/team/>

## 版权

Copyright © 2026 Free Software Foundation, Inc. 许可证 GPLv3+：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参见

`[chown(2)]`

完整文档 <https://www.gnu.org/software/coreutils/chown> 或通过以下方式本地获取：`info '(coreutils) chown invocation'`

## 版权说明

本页面是 *coreutils*（基本文件、shell 和文本操作实用程序）项目的一部分。有关该项目的信息可在 <http://www.gnu.org/software/coreutils/> 找到。如果您对本手册页有错误报告，请参见 <http://www.gnu.org/software/coreutils/>。本页面取自 2026-08-03 从 <http://ftp.gnu.org/gnu/coreutils/> 获取的 coreutils-9.11.tar.xz 压缩包。如果您发现此 HTML 版本页面存在渲染问题，或者您认为有更好或更新的页面来源，或者您对本版权说明（*不*属于原始手册页的一部分）中的信息有更正或改进，请发送邮件至 `man-pages@man7.org`。

GNU coreutils 9.11 April 2026 `CHOWN`(1)