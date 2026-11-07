https://www.man7.org/linux/man-pages/man1/getfacl.1.html

# `getfacl` - 获取文件访问控制列表

## 概要

```sh
getfacl [-aceEsRLPtpndvh] file ...
getfacl [-aceEsRLPtpndvh] -
```

## 描述

对于每个文件，`getfacl` 显示文件名、所有者、所属组以及访问控制列表（`ACL`）。如果目录具有默认 `ACL`，`getfacl` 还会显示默认 `ACL`。非目录不能具有默认 `ACL`。

如果 `getfacl` 用于不支持 `ACL` 的文件系统，`getfacl` 显示由传统文件模式权限位定义的访问权限。

`getfacl` 的输出格式如下：

```log
1:  # file: somedir/
2:  # owner: lisa
3:  # group: staff
4:  # flags: -s-
5:  user::rwx
6:  user:joe:rwx               #effective:r-x
7:  group::rwx                 #effective:r-x
8:  group:cool:r-x
9:  mask::r-x
10:  other::r-x
11:  default:user::rwx
12:  default:user:joe:rwx       #effective:r-x
13:  default:group::r-x
14:  default:mask::r-x
15:  default:other::---
```

第 1--3 行指示文件名、所有者和所属组。

第 4 行指示 `setuid`（`s`）、`setgid`（`s`）和 `sticky`（`t`）位：要么是表示该位的字母，要么是短横线（`-`）。如果设置了这些位中的任何一位，则包含此行；否则省略，因此大多数文件不会显示此行。（参见下文“符合 POSIX 1003.1e 草案标准 17”。）

第 5、7 和 10 行对应文件模式权限位的 `user`、`group` 和 `other` 字段。这三者称为基本 `ACL` 条目。第 6 行和第 8 行是命名用户和命名组条目。第 9 行是有效权限掩码。此条目限制授予所有组和命名用户的有效权限。（文件所有者和其他人的权限不受有效权限掩码影响；所有其他条目都受影响。）第 11--15 行显示与此目录关联的默认 `ACL`。目录可以具有默认 `ACL`。常规文件永远不具有默认 `ACL`。

`getfacl` 的默认行为是同时显示 `ACL` 和默认 `ACL`，并在条目的权限与有效权限不同的行中包含有效权限注释。

如果输出到终端，有效权限注释对齐到第 40 列。否则，单个制表符分隔 `ACL` 条目和有效权限注释。

多个文件的 `ACL` 列表由空行分隔。`getfacl` 的输出也可用作 `setfacl` 的输入。

### 权限

对文件具有搜索访问权限的进程（即，对文件所在目录具有读访问权限的进程）也被授予对该文件 `ACL` 的读访问权限。这类似于访问文件模式所需的权限。

## 选项

- `-a, --access`  
  显示文件访问控制列表。

- `-d, --default`  
  显示默认访问控制列表。

- `-c, --omit-header`  
  不显示注释头（每个文件输出的前三行）。

- `-e, --all-effective`  
  打印所有有效权限注释，即使与 `ACL` 条目定义的权限相同。

- `-E, --no-effective`  
  不打印有效权限注释。

- `-s, --skip-base`  
  跳过仅具有基本 `ACL` 条目（所有者、组、其他人）的文件。

- `-R, --recursive`  
  递归列出所有文件和目录的 `ACL`。

- `-L, --logical`  
  逻辑遍历，跟随符号链接。默认行为是跟随命令行上给出的符号链接，并跳过子目录中遇到的符号链接。

- `-P, --physical`  
  物理遍历，不跟随符号链接。命令行上给出的符号链接会被拒绝。（对于命令行上给出的路径名，此选项仅适用于最终组件；前面的路径组件仍可能是符号链接。）

- `-t, --tabular`  
  使用替代的表格输出格式。`ACL` 和默认 `ACL` 并排显示。由于 `ACL` 掩码条目而无效的权限以大写显示。`ACL_USER_OBJ` 和 `ACL_GROUP_OBJ` 条目的条目标签名称也以大写字母显示，有助于发现这些条目。

- `-p, --absolute-names`  
  不剥离前导斜杠字符（`/`）。默认行为是剥离前导斜杠字符。

- `-n, --numeric`  
  列出数字用户 ID 和组 ID

- `-v, --version`  
  打印 `getfacl` 的版本并退出。

- `-h, --help`  
  打印解释命令行选项的帮助。

- `--`  
  命令行选项结束。所有剩余参数都被解释为文件名，即使它们以短横线字符开头。

- `-`  
  如果文件名参数是单个短横线字符，`getfacl` 从标准输入读取文件列表。

## 符合 POSIX 1003.1e 草案标准 17

如果定义了环境变量 `POSIXLY_CORRECT`，`getfacl` 的默认行为按以下方式改变：除非另有指定，仅打印 `ACL`。仅当给出 `-d` 选项时才打印默认 `ACL`。如果未给出命令行参数，`getfacl` 的行为如同以 `getfacl -` 调用。不生成指示 `setuid`、`setgid` 和 `sticky` 位的标志注释。

## 作者

Andreas Gruenbacher，<andreas.gruenbacher@gmail.com>。

请将缺陷报告和评论发送至上述地址。

## 另请参阅

[setfacl(1)]、[acl(5)]

## 版本说明

本页是 *acl*（操作访问控制列表）项目的一部分。项目信息可在 <http://savannah.nongnu.org/projects/acl> 找到。若对本手册页有缺陷报告，请参见 <http://savannah.nongnu.org/bugs/?group=acl>。本页取自该项目上游 Git 仓库 ⟨git://git.savannah.nongnu.org/acl.git⟩，获取日期为 2026-08-03。（当时仓库中找到的最近提交日期为 2026-06-29。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`2000 年 5 月` · ACL 文件工具 · `GETFACL(1)`