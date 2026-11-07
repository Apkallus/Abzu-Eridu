https://man7.org/linux/man-pages/man1/cat.1.html

# `cat` - 连接文件并打印到标准输出

## 概要

```sh
cat [OPTION]... [FILE]...
```

## 描述

将 FILE 连接到标准输出。

当没有 FILE，或 FILE 为 `-` 时，读取标准输入。

- `-A, --show-all`  
    等价于 `-vET`

- `-b, --number-nonblank`  
    对非空输出行编号，覆盖 `-n`

- `-e`  
    等价于 `-vE`

- `-E, --show-ends`  
    在每行末尾显示 `$` 或 `^M$`

- `-n, --number`  
    对所有输出行编号

- `-s, --squeeze-blank`  
    抑制重复的空输出行

- `-t`  
    等价于 `-vT`

- `-T, --show-tabs`  
    将 `TAB` 字符显示为 `^I`

- `-u`  
    （忽略）

- `-v, --show-nonprinting`  
    使用 `^` 和 `M-` 表示法，`LFD` 和 `TAB` 除外

- `--help`  
    显示此帮助信息并退出

- `--version`  
    输出版本信息并退出

## 示例

- 
    ```sh
    cat f - g
    ```
    输出 f 的内容，然后标准输入，然后 g 的内容。

- 
    ```sh
    cat
    ```
    将标准输入复制到标准输出。

## 作者

由 Torbjorn Granlund 和 Richard M. Stallman 编写。

## 报告错误

将错误报告发送至：bug-coreutils@gnu.org
GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
使用 GNU 软件的通用帮助：<https://www.gnu.org/gethelp/>
将任何翻译错误报告至
<https://translationproject.org/team/>

## 版权

Copyright © 2026 Free Software Foundation, Inc. 许可证 GPLv3+：
GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。
这是自由软件：你可以自由地修改和再分发它。
在法律允许的范围内，不提供任何担保。

## 另请参阅

"tac(1)"

完整文档 <https://www.gnu.org/software/coreutils/cat>
或通过以下方式在本地获取：`info '(coreutils) cat invocation'`

## 版本说明

本页面是 *coreutils*（基本文件、shell 和文本操作实用程序）项目的一部分。有关该项目的信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果你对本手册页有错误报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页面取自 2026-08-03 从 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩ 获取的 coreutils-9.11.tar.xz 压缩包。如果你发现此 HTML 版本页面存在任何渲染问题，或者你认为有更好或更新的页面来源，或者你对本版本说明中的信息（该信息*不*属于原始手册页的一部分）有更正或改进，请发送邮件至 man-pages@man7.org

```
GNU coreutils 9.11              April 2026                         CAT(1)
```