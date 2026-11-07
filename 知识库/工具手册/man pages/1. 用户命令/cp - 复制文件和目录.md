https://www.man7.org/linux/man-pages/man1/cp.1.html

# `cp` - 复制文件和目录

## 概要

```sh
cp [OPTION]... [-T] SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
cp [OPTION]... -t DIRECTORY SOURCE...
```

## 描述

将 `SOURCE` 复制到 `DEST`，或将多个 `SOURCE` 复制到 `DIRECTORY`。

长选项的必需参数对短选项也是必需的。

- `-a, --archive`  
  与 `-dR --preserve=all` 相同

- `--attributes-only`  
  不复制文件数据，仅复制属性

- `--backup[=CONTROL]`  
  为每个现有目标文件创建备份

- `-b`  
  类似 `--backup`，但不接受参数

- `--copy-contents`  
  递归时复制特殊文件的内容

- `-d`  
  与 `--no-dereference --preserve=links` 相同

- `--debug`  
  解释文件如何被复制。隐含 `-v`

- `-f, --force`  
  若现有目标文件无法打开，则移除它并重试（当同时使用 `-n` 选项时忽略此选项）

- `-i, --interactive`  
  覆盖前提示（覆盖先前的 `-n` 选项）

- `-H`  
  跟随 `SOURCE` 中的命令行符号链接

- `-L, --dereference`  
  始终跟随 `SOURCE` 中的符号链接

- `-P, --no-dereference`  
  从不跟随 `SOURCE` 中的符号链接

- `--keep-directory-symlink`  
  跟随指向目录的现有符号链接

- `-l, --link`  
  硬链接文件而不是复制

- `-n, --no-clobber`  
  （已弃用）静默跳过现有文件。另请参见 `--update`

- `-p`  
  与 `--preserve=mode,ownership,timestamps` 相同

- `--preserve[=ATTR_LIST]`  
  保留指定属性

- `--no-preserve=ATTR_LIST`  
  不保留指定属性

- `--parents`  
  在 `DIRECTORY` 下使用完整源文件名

- `-R, -r, --recursive`  
  递归复制目录

- `--reflink[=WHEN]`  
  控制克隆/`CoW` 复制。见下文

- `--remove-destination`  
  在尝试打开每个现有目标文件之前先移除它（与 `--force` 对比）

- `--sparse=WHEN`  
  控制稀疏文件的创建。见下文

- `--strip-trailing-slashes`  
  从每个 `SOURCE` 参数中移除末尾斜杠

- `-s, --symbolic-link`  
  创建符号链接而不是复制

- `-S, --suffix=SUFFIX`  
  覆盖通常的备份后缀

- `-t, --target-directory=DIRECTORY`  
  将所有 `SOURCE` 参数复制到 `DIRECTORY`

- `-T, --no-target-directory`  
  将 `DEST` 视为普通文件

- `--update[=UPDATE]`  
  控制更新哪些现有文件；`UPDATE={all,none,none-fail,older(default)}`

- `-u`  
  等价于 `--update[=older]`。见下文

- `-v, --verbose`  
  解释正在执行的操作

- `-x, --one-file-system`  
  停留在当前文件系统

- `-Z`  
  将目标文件的 SELinux 安全上下文设置为默认类型

- `--context[=CTX]`  
  类似 `-Z`，或若指定 `CTX`，则将 SELinux 或 SMACK 安全上下文设置为 `CTX`

- `--help`  
  显示此帮助并退出

- `--version`  
  输出版本信息并退出

`ATTR_LIST` 是逗号分隔的属性列表。属性包括：`mode` 表示权限（包括任何 `ACL` 和 `xattr` 权限），`ownership` 表示用户和组，`timestamps` 表示文件时间戳，`links` 表示硬链接，`context` 表示安全上下文，`xattr` 表示扩展属性，`all` 表示所有属性。

默认情况下，稀疏 `SOURCE` 文件通过粗略启发式检测，相应的 `DEST` 文件也会被设为稀疏。这是 `--sparse=auto` 选择的行为。指定 `--sparse=always`，只要 `SOURCE` 文件包含足够长的零字节序列，就创建稀疏 `DEST` 文件。使用 `--sparse=never` 阻止创建稀疏文件。

`UPDATE` 控制目标中哪些现有文件被替换。未指定 `--update` 选项时，`all` 是默认操作，结果为替换目标中的所有现有文件。`none` 类似 `--no-clobber` 选项，不替换目标中的任何文件，且跳过的文件不会导致失败。`none-fail` 也确保不替换目标中的任何文件，但任何被跳过的文件都会被诊断并导致失败。指定 `--update` 时，`older` 是默认操作，结果为如果文件比相应源文件旧，则替换该文件。

默认或使用 `--reflink=auto` 时，`cp` 会尝试轻量复制，仅在修改时复制数据块，如果不可能则回退到标准复制。使用 `--reflink[=always]` 时，若不支持 `CoW`，`cp` 将失败，而 `--reflink=never` 确保执行标准复制。

备份后缀为 `~`，除非通过 `--suffix` 或 `SIMPLE_BACKUP_SUFFIX` 设置。版本控制方法可通过 `--backup` 选项或 `VERSION_CONTROL` 环境变量选择。值如下：

- `none, off`  
  从不进行备份（即使给出 `--backup`）

- `numbered, t`  
  进行编号备份

- `existing, nil`  
  若存在编号备份则编号，否则简单备份

- `simple, never`  
  始终进行简单备份

作为特殊情况，当给出 `force` 和 `backup` 选项，且对于现有常规文件，`SOURCE` 与 `DEST` 同名时，`cp` 会备份 `SOURCE`。

## 作者

由 Torbjorn Granlund、David MacKenzie 和 Jim Meyering 编写。

## 报告缺陷

- 报告缺陷至：`bug-coreutils@gnu.org`
- GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>
- 使用 GNU 软件的通用帮助：<https://www.gnu.org/gethelp/>
- 报告任何翻译缺陷至 <https://translationproject.org/team/>

## 版权

版权所有 © 2026 Free Software Foundation, Inc. 许可证 `GPLv3+`：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## 另请参阅

[install(1)]

完整文档 <https://www.gnu.org/software/coreutils/cp>，或通过以下方式在本地获取：`info '(coreutils) cp invocation'`

## 版本说明

本页是 *coreutils*（基本文件、Shell 和文本操作工具）项目的一部分。项目信息可在 <http://www.gnu.org/software/coreutils/> 找到。若对本手册页有缺陷报告，请参见 <http://www.gnu.org/software/coreutils/>。本页取自 2026-08-03 从 <http://ftp.gnu.org/gnu/coreutils/> 获取的 `coreutils-9.11.tar.xz` 压缩包。如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`GNU coreutils 9.11` · 2026 年 4 月 · `CP(1)`