https://www.man7.org/linux/man-pages/man1/ln.1.html

# `ln` - 在文件之间创建链接

## SYNOPSIS

```sh
ln [OPTION]... [-T] TARGET LINK_NAME
ln [OPTION]... TARGET
ln [OPTION]... TARGET... DIRECTORY
ln [OPTION]... -t DIRECTORY TARGET...
```

## DESCRIPTION

第 1 种形式中，创建指向 `TARGET` 的链接，名称为 `LINK_NAME`。第 2 种形式中，在当前目录中创建指向 `TARGET` 的链接。第 3 和第 4 种形式中，在 `DIRECTORY` 中为每个 `TARGET` 创建链接。默认创建硬链接；使用 `--symbolic` 创建符号链接。默认情况下，每个目标（新链接的名称）不应已存在。创建硬链接时，每个 `TARGET` 都必须存在。符号链接可以保存任意文本；如果之后被解析，相对链接将相对于其父目录解释。

长选项的必需参数对短选项也同样必需。

- `--backup[=CONTROL]`  
    为每个已存在的目标文件创建备份

- `-b`  
    类似 `--backup`，但不接受参数

- `-d, -F, --directory`  
    允许超级用户尝试为目录创建硬链接（如果系统支持）

- `-f, --force`  
    删除已存在的目标文件

- `-i, --interactive`  
    提示是否删除目标

- `-L, --logical`  
    解引用作为符号链接的 `TARGET`

- `-n, --no-dereference`  
    如果 `LINK_NAME` 是指向目录的符号链接，则将其视为普通文件

- `-P, --physical`  
    直接为符号链接创建硬链接

- `-r, --relative`  
    与 `-s` 一起使用时，创建相对于链接位置的链接

- `-s, --symbolic`  
    创建符号链接而不是硬链接

- `-S, --suffix=SUFFIX`  
    覆盖通常的备份后缀

- `-t, --target-directory=DIRECTORY`  
    指定在其中创建链接的 `DIRECTORY`

- `-T, --no-target-directory`  
    始终将 `LINK_NAME` 视为普通文件

- `-v, --verbose`  
    打印每个已链接文件的名称

- `--help`  
    显示此帮助并退出

- `--version`  
    输出版本信息并退出

备份后缀为 `~`，除非通过 `--suffix` 或 `SIMPLE_BACKUP_SUFFIX` 设置。版本控制方法可以通过 `--backup` 选项或 `VERSION_CONTROL` 环境变量选择。可用的值如下：

- `none, off`  
    从不创建备份（即使给出了 `--backup`）

- `numbered, t`  
    创建编号备份

- `existing, nil`  
    如果存在编号备份则使用编号备份，否则使用简单备份

- `simple, never`  
    始终创建简单备份

使用 `-s` 会忽略 `-L` 和 `-P`。否则，当 `TARGET` 是符号链接时，最后指定的选项控制行为，默认为 `-P`。

## AUTHOR

由 Mike Parker 和 David MacKenzie 编写。

## REPORTING BUGS

报告缺陷至：bug-coreutils@gnu.org  
GNU coreutils 主页：<https://www.gnu.org/software/coreutils/>  
使用 GNU 软件的一般帮助：<https://www.gnu.org/gethelp/>  
报告任何翻译缺陷至 <https://translationproject.org/team/>

## COPYRIGHT

版权所有 © 2026 Free Software Foundation, Inc. 许可证 GPLv3+：GNU GPL 版本 3 或更高版本 <https://gnu.org/licenses/gpl.html>。这是自由软件：你可以自由更改和重新分发它。在法律允许的范围内，不提供任何担保。

## SEE ALSO

`link(2)`、`symlink(2)`

完整文档：<https://www.gnu.org/software/coreutils/ln>，或在本地通过以下方式获取：`info '(coreutils) ln invocation'`

## COLOPHON

本页是 `coreutils`（基本文件、shell 和文本操作实用工具）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/coreutils/>⟩ 找到。如果你对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/coreutils/>⟩。本页取自 2026-08-03 获取的 tarball `coreutils-9.11.tar.xz`，来源为 ⟨<http://ftp.gnu.org/gnu/coreutils/>⟩。如果你发现本页 HTML 版本存在渲染问题，或认为有更好或更新版本的页面来源，或对本 COLOPHON 中的信息（该部分不属于原始手册页）有更正或改进，请发送邮件至 man-pages@man7.org

```text
GNU coreutils 9.11              April 2026                          LN(1)
```