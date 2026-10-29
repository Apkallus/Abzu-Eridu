# acl — 访问控制列表

https://man7.org/linux/man-pages/man5/acl.5.html

## 描述

本手册页描述 POSIX 访问控制列表，用于为文件和目录定义更细粒度的自主访问权限。

## ACL 类型

每个对象都可以被认为关联有一个 ACL，用于管理对该对象的自主访问；此 ACL 称为访问 ACL。此外，目录可以关联一个 ACL，用于管理在该目录内创建对象的初始访问 ACL；此 ACL 称为默认 ACL。

## ACL 条目

ACL 由一组 ACL 条目组成。ACL 条目以读、写和搜索/执行权限的组合形式，为单个用户或一组用户指定对关联对象的访问权限。

ACL 条目包含条目标签类型、可选的条目标签限定符以及一组权限。我们使用术语“限定符”表示 ACL 条目的条目标签限定符。

对于标签类型为 `ACL_USER` 或 `ACL_GROUP` 的条目，限定符分别表示用户或组的标识符。标签类型不是 `ACL_USER` 或 `ACL_GROUP` 的条目没有定义的限定符。

定义了以下条目标签类型：

- `ACL_USER_OBJ`：`ACL_USER_OBJ` 条目表示文件所有者的访问权限。
- `ACL_USER`：`ACL_USER` 条目表示由该条目的限定符标识的用户的访问权限。
- `ACL_GROUP_OBJ`：`ACL_GROUP_OBJ` 条目表示文件组的访问权限。
- `ACL_GROUP`：`ACL_GROUP` 条目表示由该条目的限定符标识的组的访问权限。
- `ACL_MASK`：`ACL_MASK` 条目表示类型为 `ACL_USER`、`ACL_GROUP_OBJ` 或 `ACL_GROUP` 的条目可以授予的最大访问权限。
- `ACL_OTHER`：`ACL_OTHER` 条目表示不匹配 ACL 中任何其他条目的进程的访问权限。

执行访问检查时，`ACL_USER_OBJ` 和 `ACL_USER` 条目与有效用户 ID 进行测试。有效组 ID 以及所有补充组 ID 与 `ACL_GROUP_OBJ` 和 `ACL_GROUP` 条目进行测试。

## 有效 ACL

有效的 ACL 对于 `ACL_USER_OBJ`、`ACL_GROUP_OBJ` 和 `ACL_OTHER` 标签类型中的每一种都恰好包含一个条目。标签类型为 `ACL_USER` 和 `ACL_GROUP` 的条目可以在 ACL 中出现零次或多次。包含 `ACL_USER` 或 `ACL_GROUP` 标签类型条目的 ACL 必须恰好包含一个 `ACL_MASK` 标签类型的条目。如果 ACL 不包含 `ACL_USER` 或 `ACL_GROUP` 标签类型的条目，则 `ACL_MASK` 条目是可选的。

所有用户 ID 限定符在 `ACL_USER` 标签类型的所有条目中必须唯一，所有组 ID 在 `ACL_GROUP` 标签类型的所有条目中必须唯一。

如果目录未关联默认 ACL，`acl_get_file()` 函数返回一个包含零个 ACL 条目的 ACL 作为该目录的默认 ACL。`acl_set_file()` 函数也接受包含零个 ACL 条目的 ACL 作为目录的有效默认 ACL，表示该目录不应关联默认 ACL。这等效于使用 `acl_delete_def_file()` 函数。

## ACL 条目与文件权限位的对应关系

ACL 定义的权限是文件权限位所指定权限的超集。

文件所有者、组和其他权限与特定 ACL 条目之间存在对应关系：所有者权限对应于 `ACL_USER_OBJ` 条目的权限。如果 ACL 有 `ACL_MASK` 条目，则组权限对应于 `ACL_MASK` 条目的权限。否则，如果 ACL 没有 `ACL_MASK` 条目，则组权限对应于 `ACL_GROUP_OBJ` 条目的权限。其他权限对应于 `ACL_OTHER` 条目的权限。

文件所有者、组和其他权限始终与对应 ACL 条目的权限匹配。修改文件权限位会导致关联 ACL 条目的修改，修改这些 ACL 条目也会导致文件权限位的修改。

## 对象创建与默认 ACL

当使用 `creat()`、`mkdir()`、`mknod()`、`mkfifo()` 或 `open()` 函数中的任何一个创建文件对象时，会初始化该文件的访问 ACL。如果目录关联有默认 ACL，则创建文件对象的函数的 `mode` 参数和该目录的默认 ACL 用于确定新对象的 ACL：

1. 新对象继承所在目录的默认 ACL 作为其访问 ACL。
2. 对应于文件权限位的访问 ACL 条目会被修改，使其不包含 `mode` 参数所指定权限中不包含的权限。

如果目录未关联默认 ACL，则创建文件对象的函数的 `mode` 参数和文件创建掩码（见 `[umask(2)]`）用于确定新对象的 ACL：

1. 为新对象分配一个访问 ACL，其中包含标签类型为 `ACL_USER_OBJ`、`ACL_GROUP_OBJ` 和 `ACL_OTHER` 的条目。这些条目的权限设置为文件创建掩码指定的权限。
2. 对应于文件权限位的访问 ACL 条目会被修改，使其不包含 `mode` 参数所指定权限中不包含的权限。

## 访问检查算法

进程可以请求对受 ACL 保护的文件对象进行读、写或执行/搜索访问。访问检查算法确定是否授予对该对象的访问。

```text
1. If the effective user ID of the process matches the user ID
   of the file object owner, then

         if the ACL_USER_OBJ entry contains the requested
         permissions, access is granted,

         else access is denied.

2. else if the effective user ID of the process matches the
   qualifier of any entry of type ACL_USER, then

         if the matching ACL_USER entry and the ACL_MASK entry
         contain the requested permissions, access is granted,

         else access is denied.

3. else if the effective group ID or any of the supplementary
   group IDs of the process match the file group or the
   qualifier of any entry of type ACL_GROUP, then

         if the ACL contains an ACL_MASK entry, then

               if the ACL_MASK entry and any of the matching
               ACL_GROUP_OBJ or ACL_GROUP entries contain the
               requested permissions, access is granted,

               else access is denied.

         else (note that there can be no ACL_GROUP entries
         without an ACL_MASK entry)

               if the ACL_GROUP_OBJ entry contains the requested
               permissions, access is granted,

               else access is denied.

4. else if the ACL_OTHER entry contains the requested
   permissions, access is granted.

5. else access is denied.
```

## ACL 文本形式

定义了用于表示 ACL 的长文本形式和短文本形式。在两种形式中，ACL 条目都表示为三个以冒号分隔的字段：ACL 条目标签类型、ACL 条目限定符和自主访问权限。第一个字段包含以下条目标签类型关键字之一：

- `user`：`user` ACL 条目指定授予文件所有者（条目标签类型 `ACL_USER_OBJ`）或指定用户（条目标签类型 `ACL_USER`）的访问权限。
- `group`：`group` ACL 条目指定授予文件组（条目标签类型 `ACL_GROUP_OBJ`）或指定组（条目标签类型 `ACL_GROUP`）的访问权限。
- `mask`：`mask` ACL 条目指定除文件所有者的 `user` 条目和 `other` 条目外，任何 ACL 条目可以授予的最大访问权限（条目标签类型 `ACL_MASK`）。
- `other`：`other` ACL 条目指定授予不匹配任何 `user` 或 `group` ACL 条目的任何进程的访问权限（条目标签类型 `ACL_OTHER`）。

第二个字段包含与条目标签类型 `ACL_USER` 或 `ACL_GROUP` 的 ACL 条目关联的用户或组的用户或组标识符，对于所有其他条目为空。用户标识符可以是用户名或十进制形式的用户 ID 编号。组标识符可以是组名或十进制形式的组 ID 编号。

第三个字段包含自主访问权限。读、写和搜索/执行权限按此顺序由 `r`、`w` 和 `x` 字符表示。这些字符中的每一个都被 `-` 字符替换，以表示 ACL 条目中不存在该权限。从文本形式转换为内部表示时，不存在的权限无需指定。

每个 ACL 条目的开头和结尾，以及字段分隔符（冒号字符）前后允许有空白。

### 长文本形式

长文本形式每行包含一个 ACL 条目。此外，数字符号（`#`）可以开始一个注释，该注释延伸到行尾。如果 `ACL_USER`、`ACL_GROUP_OBJ` 或 `ACL_GROUP` ACL 条目包含的权限不也包含在 `ACL_MASK` 条目中，则该条目后跟数字符号、字符串 `effective:` 以及该条目定义的有效访问权限。以下是长文本形式的示例：

```text
user::rw-
user:lisa:rw-         #effective:r--
group::r--
group:toolies:rw-     #effective:r--
mask::r--
other::r--
```

### 短文本形式

短文本形式是以逗号分隔的 ACL 条目序列，用于输入。不支持注释。条目标签类型关键字可以以其完整未缩写形式出现，也可以以其单字母缩写形式出现。`user` 的缩写是 `u`，`group` 的缩写是 `g`，`mask` 的缩写是 `m`，`other` 的缩写是 `o`。权限可以按任意顺序最多包含以下字符中的每一个：`r`、`w`、`x`。以下是短文本形式的示例：

```text
u::rw-,u:lisa:rw-,g::r--,g:toolies:rw-,m::r--,o::r--
g:toolies:rw,u:lisa:rw,u::wr,g::r,o::r,m::r
```

## 基本原理

IEEE 1003.1e 草案 17 定义了访问控制列表，其中包括标签类型为 `ACL_MASK` 的条目，并定义了文件权限位之间的映射，该映射不是恒定的。标准工作组定义这个相对复杂的接口，是为了确保符合 IEEE 1003.1（“POSIX.1”）的应用程序在具有 ACL 的系统上仍能按预期工作。IEEE 1003.1e 草案 17 在 B.23 节中包含了选择此接口的基本原理。

## 文件实用程序的变化

在支持 ACL 的系统上，文件实用程序 `[ls(1)]`、`[cp(1)]` 和 `[mv(1)]` 会以以下方式改变其行为：

- 对于具有默认 ACL 或访问 ACL 包含超过三个必需 ACL 条目的文件，`[ls(1)]` 实用程序在 `ls -l` 产生的长格式中会在权限字符串后显示加号（`+`）。
- 如果指定了 `-p` 标志，`[cp(1)]` 实用程序也会保留 ACL。如果无法做到，则产生警告。
- `[mv(1)]` 实用程序始终保留 ACL。如果无法做到，则产生警告。

`[chmod(1)]` 实用程序和 `[chmod(2)]` 系统调用对访问 ACL 的影响在“ACL 条目与文件权限位的对应关系”中描述。

## 标准

IEEE 1003.1e 草案 17（“POSIX.1e”）文档描述了 IEEE 1003.1 标准的若干安全扩展。虽然 1003.1e 的工作已被放弃，但许多 UNIX 风格系统实现了 POSIX.1e 草案 17 或更早草案的部分内容。

Linux 访问控制列表实现了 POSIX.1e 中为访问控制列表定义的完整函数和实用程序集，以及若干扩展。该实现完全符合 POSIX.1e 草案 17；扩展按此标记。访问控制列表操作函数定义在 ACL 库（`libacl`，`-lacl`）中。符合 POSIX 的接口声明在 `<sys/acl.h>` 头文件中。这些函数的 Linux 特定扩展声明在 `<acl/libacl.h>` 头文件中。

## 注释

### 拒绝权限与 Linux 用户命名空间

虽然 ACL 可用于根据进程所属的组拒绝进程权限，但这被认为是不良实践。像 `[newuidmap(1)]` 这样的特权辅助程序可以授予非特权进程访问 `[setgroups(2)]` 系统调用的能力，这允许它们放弃补充组成员关系，并使基于该成员关系的限制失效。更多详情见 `[user_namespaces(7)]`。

## 另请参见

`chmod(1)`、`creat(2)`、`getfacl(1)`、`ls(1)`、`mkdir(2)`、`mkfifo(2)`、`mknod(2)`、`mount(8)`、`open(2)`、`setfacl(1)`、`stat(2)`、`umask(1)`

### POSIX 1003.1e 草案 17

<https://wt.tuxomania.net/publications/posix.1e/download.html>

### 按类别划分的 POSIX 1003.1e 函数

**ACL 存储管理**  
`acl_dup(3)`、`acl_free(3)`、`acl_init(3)`

**ACL 条目操作**  
`acl_copy_entry(3)`、`acl_create_entry(3)`、`acl_delete_entry(3)`、`acl_get_entry(3)`、`acl_valid(3)`  
`acl_add_perm(3)`、`acl_calc_mask(3)`、`acl_clear_perms(3)`、`acl_delete_perm(3)`、`acl_get_permset(3)`、`acl_set_permset(3)`  
`acl_get_qualifier(3)`、`acl_get_tag_type(3)`、`acl_set_qualifier(3)`、`acl_set_tag_type(3)`

**对象上的 ACL 操作**  
`acl_delete_def_file(3)`、`acl_get_fd(3)`、`acl_get_file(3)`、`acl_set_fd(3)`、`acl_set_file(3)`

**ACL 格式转换**  
`acl_copy_entry(3)`、`acl_copy_ext(3)`、`acl_from_text(3)`、`acl_to_text(3)`、`acl_size(3)`

### 按可用性划分的 POSIX 1003.1e 函数

第一组函数在大多数具有类 POSIX 访问控制列表的系统上受支持，而第二组函数受支持的系统较少。对于将要移植的应用程序，最好避免使用第二组。

`acl_delete_def_file(3)`、`acl_dup(3)`、`acl_free(3)`、`acl_from_text(3)`、`acl_get_fd(3)`、`acl_get_file(3)`、`acl_init(3)`、`acl_set_fd(3)`、`acl_set_file(3)`、`acl_to_text(3)`、`acl_valid(3)`

`acl_add_perm(3)`、`acl_calc_mask(3)`、`acl_clear_perms(3)`、`acl_copy_entry(3)`、`acl_copy_ext(3)`、`acl_copy_int(3)`、`acl_create_entry(3)`、`acl_delete_entry(3)`、`acl_delete_perm(3)`、`acl_get_entry(3)`、`acl_get_permset(3)`、`acl_get_qualifier(3)`、`acl_get_tag_type(3)`、`acl_set_permset(3)`、`acl_set_qualifier(3)`、`acl_set_tag_type(3)`、`acl_size(3)`

### Linux 扩展

这些不可移植的扩展在 Linux 系统上可用。

`acl_check(3)`、`acl_cmp(3)`、`acl_delete_def_file_at(3)`、`acl_entries(3)`、`acl_equiv_mode(3)`、`acl_error(3)`、`acl_extended_fd(3)`、`acl_extended_file(3)`、`acl_extended_file_at(3)`、`acl_extended_file_nofollow(3)`、`acl_from_mode(3)`、`acl_get_file_at(3)`、`acl_get_perm(3)`、`acl_set_file_at(3)`、`acl_to_any_text(3)`

## 作者

Andreas Gruenbacher, <andreas.gruenbacher@gmail.com>

## 版权说明

本页面是 *acl*（操作访问控制列表）项目的一部分。有关该项目的信息可在 <http://savannah.nongnu.org/projects/acl> 找到。如果您对本手册页有错误报告，请参见 <http://savannah.nongnu.org/bugs/?group=acl>。本页面取自该项目上游 Git 仓库 ⟨git://git.savannah.nongnu.org/acl.git⟩，获取日期为 2026-08-03。（当时在仓库中找到的最近提交日期为 2026-06-29。）如果您发现此 HTML 版本页面存在渲染问题，或者您认为有更好或更新的页面来源，或者您对本版权说明（*不*属于原始手册页的一部分）中的信息有更正或改进，请发送邮件至 `man-pages@man7.org`。

Linux ACL June 5, 2026 `ACL`(5)