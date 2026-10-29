https://www.man7.org/linux/man-pages/man1/chgrp.1.html

# `chgrp` - 更改组所有权

## 概要

```sh
chgrp [OPTION]... GROUP FILE...
chgrp [OPTION]... --reference=RFILE FILE...
```

## 描述

将每个 `FILE` 的组更改为 `GROUP`。使用 `--reference` 时，将每个 `FILE` 的组更改为 `RFILE` 的组。

- `-c`, `--changes`  
  类似 `verbose`，但仅在发生更改时报告

- `-f`, `--silent`, `--quiet`  
  抑制大多数错误消息

- `-v`, `--verbose`  
  为处理的每个文件输出诊断信息

- `--dereference`  
  作用于每个符号链接的目标（这是默认行为），而不是符号链接本身

- `-h`, `--no-dereference`  
  作用于符号链接，而不是其引用的任何文件；仅在能够更改符号链接所有权的系统上有用

- `--from=CURRENT_OWNER:CURRENT_GROUP`  
  仅当每个文件的当前所有者和/或组与此处指定的值匹配时，才更改其所有权。两者均可省略；省略的属性不要求匹配

- `--no-preserve-root`  
  不特殊对待 `/`（默认）

- `--preserve-root`  
  拒绝对 `/` 进行递归操作

- `--reference=RFILE`  
  使用 `RFILE` 的所有权，而不是指定值。若 `RFILE` 是符号链接，则始终解引用

- `-R`, `--recursive`  
  递归操作文件和目录

以下选项修改在同时指定 `-R` 选项时遍历层次结构的方式。若指定多个，仅最后一个生效。`-P` 是默认值。

- `-H`  
  若命令行参数是指向目录的符号链接，则遍历它

- `-L`  
  遍历遇到的每个指向目录的符号链接

- `-P`  
  不遍历任何符号链接

- `--help`  
  显示此帮助并退出

- `--version`  
  输出版本信息并退出

## 示例

- 
    ```sh
    chgrp staff /u
    ```
    将 `/u` 的组更改为 `staff`。

- 
    ```sh
    chgrp -hR staff /u
    ```
    将 `/u` 及其子文件的组更改为 `staff`。

## 作者

由 David MacKenzie 和 Jim Meyering 编写。

## 报告缺陷

- 报告缺陷至：`bug-coreutils@gnu.org`
- GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
- 使用 GNU 软件的通用帮助：<https://www.gnu.org/gethelp/>
- 报告任何翻译缺陷至 <https://translationproject.org/team/>

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 `GPLv3+`：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参阅

[chown(1)]、[chown(2)]

完整文档 <https://www.gnu.org/software/coreutils/chgrp>，或通过以下方式在本地获取：`info '(coreutils) chgrp invocation'`

## 版本说明

本页是 *coreutils*（基本文件、Shell 和文本操作工具）项目的一部分。项目信息可在 <http://www.gnu.org/software/coreutils/> 找到。若对本手册页有缺陷报告，请参见 <http://www.gnu.org/software/coreutils/>。本页取自 2026-08-03 从 <http://ftp.gnu.org/gnu/coreutils/> 获取的 `coreutils-9.11.tar.xz` 压缩包。如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`GNU coreutils 9.11` · 2026 年 4 月 · `CHGRP(1)`