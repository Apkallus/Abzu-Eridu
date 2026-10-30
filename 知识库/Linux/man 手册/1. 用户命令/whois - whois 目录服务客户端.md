https://manpages.debian.org/trixie/whois/whois.1.en.html

# `whois` - whois 目录服务客户端

## 概要

```sh
whois [ { -h | --host } HOST ] [ { -p | --port } PORT ] [ -abBcdGHIKlLmMrRx ] [ -g SOURCE:FIRST-LAST ] [ -i ATTR[,ATTR]... ] [ -s SOURCE[,SOURCE]... ] [ -T TYPE[,TYPE]... ] [ --verbose ] [ --no-recursion ] OBJECT
whois -q KEYWORD
whois -t TYPE
whois -v TYPE
whois --help
whois --version
```

## 描述

`whois` 在 `RFC 3912` 数据库中搜索对象。

此版本的 whois 客户端会尝试猜测用于查询指定对象的正确服务器。如果无法猜测，则对于 NIC 句柄将连接到 `whois.networksolutions.com`，对于 IPv4 地址和网络名称将连接到 `whois.arin.net`。

## 选项

- `-h` `HOST`, `--host=HOST`  
  连接到 `HOST`。

- `-H`  
  不显示某些注册管理机构喜欢向你展示的法律免责声明。

- `-p` `PORT`, `--port=PORT`  
  连接到 `PORT`。

- `-I`  
  首先查询 `whois.iana.org`，然后遵循其引用到对该请求具有权威性的 whois 服务器。这适用于 IP 地址、AS 号和域名。**注意**：这意味着 IANA 服务器将收到你的完整查询。

- `--no-recursion`  
  禁用从注册管理机构到注册商服务器的递归。

- `--verbose`  
  输出详细信息。

- `--help`  
  显示在线帮助。

- `--version`  
  显示程序版本。

其他选项是 `whois.ripe.net` 及一些类似 RIPE 的服务器理解的标志：

- `-a`  
  还搜索所有镜像数据库。

- `-b`  
  返回带有滥用联系人的简短 IP 地址范围。

- `-B`  
  禁用对象过滤。（显示电子邮件地址。）

- `-c`  
  返回带 `irt` 对象引用的最小 IP 地址范围。

- `-d`  
  还返回反向 DNS 委派对象。

- `-g` `SOURCE:FIRST-LAST`  
  在 `SOURCE` 数据库中搜索更新序列号介于 `FIRST` 和 `LAST` 之间的更新。它可用于获取近实时镜像流。

- `-G`  
  禁用关联对象的分组。

- `-i` `ATTR[,ATTR]...`  
  反向搜索具有关联属性的对象。`ATTR` 是属性名，而位置参数 `OBJECT` 是属性值。

- `-K`  
  仅返回主键属性。例外是 `set` 对象的 `members` 属性，它始终返回。另一个例外是 `organisation`、`person` 和 `role` 对象的所有属性，它们从不返回。

- `-l`  
  返回具体程度低一级的对象。

- `-L`  
  返回所有具体程度较低的对象。

- `-m`  
  返回具体程度高一级的对象。

- `-M`  
  返回所有具体程度较高的对象。

- `-q` `KEYWORD`  
  返回服务器信息。`KEYWORD` 可以是 `version`（服务器版本）、`sources`（数据库源列表）或 `types`（支持的对象类型列表）。

- `-r`  
  禁用联系信息的递归查找。

- `-R`  
  禁止跟随引用，并强制显示服务器本地副本中的对象。

- `-s` `SOURCE[,SOURCE]...`  
  请求服务器搜索从 `SOURCE` 镜像的对象。源用逗号分隔，顺序有意义。使用 `-q sources` 参数获取有效源列表。

- `-t` `TYPE`  
  返回 `TYPE` 对象的模板。

- `-T` `TYPE[,TYPE]...`  
  将搜索限制为 `TYPE` 的对象。多个类型用逗号分隔。

- `-v` `TYPE`  
  返回 `TYPE` 对象的详细模板。

- `-x`  
  仅搜索网络地址前缀的精确匹配。

## 注意事项

当向 Verisign gTLD（例如 `.com`、`.net`……）的 thin registry 服务器查询某个域时，程序会自动在前面加上 `domain` 关键字，以仅显示域记录。必须使用 `nameserver` 或 `registrar` 关键字来显示其他类型的记录。

当向 `whois.arin.net` 查询 IPv4 或 IPv6 网络时，CIDR 网络掩码长度将自动从查询字符串中移除。

当向 `whois.nic.ad.jp` 查询 AS 号时，程序会自动将请求转换为适当格式，在字符串 `AS` 后插入一个空格。

当向 `whois.denic.de` 查询域名且未指定其他标志时，程序会自动添加标志 `-T dn`。

当向 `whois.dk-hostmaster.dk` 查询域名且未指定其他标志时，程序会自动添加标志 `--show-handles`。

查询非 RIPE 服务器时，RIPE 特定的命令行选项会被忽略。这是否符合用户意图可能因情况而异。使用非标准查询参数时，不应由客户端解释的命令行选项必须放在 `--` 分隔符之后（该分隔符标记查询字符串的开始）。

如果 `/etc/whois.conf` 配置文件存在，则在应用常规规则之前，会查询该文件以查找服务器。该文件的每一行应包含一个要与查询文本匹配的正则表达式，以及要使用的 whois 服务器，二者用空白分隔。IDN 域必须使用 ACE 格式。

whois 协议没有规定无法由 ASCII 表示的字符的编码，而且各实现差异很大。如果程序知道特定服务器使用某种编码，则在需要时会将服务器输出转码为当前系统区域设置指定的编码。

命令行参数将始终根据当前系统区域设置进行解释，并转换为 IDN ASCII 兼容编码。

## 文件

`/etc/whois.conf`

## 环境

- `LANG`  
  当查询 `whois.nic.ad.jp` 和 `whois.jprs.jp` 时，除非 `LANG` 或 `LC_MESSAGES` 环境变量指定日语区域设置，否则请求英文文本。

- `WHOIS_OPTIONS`  
  将在命令行指定选项之前评估的选项列表。

- `WHOIS_SERVER`  
  如果程序无法猜测某些类型对象的位置，将查询此服务器。如果该变量不存在，则查询 `whois.arin.net`。

## 另请参阅

[whois.conf(5)]。

`RFC 3912`：WHOIS 协议规范。

*RIPE 数据库查询参考手册*：<https://www.ripe.net/data-tools/support/documentation/ripe-database-query-reference-manual>

## 缺陷

程序在命令行解析器中可能存在缓冲区溢出：确保不要向它传递不可信数据。应将其重写为使用动态字符串库。

## 历史

此程序紧密跟踪 RIPE 的 Ambrose Magee 等人基于原始 BSD 客户端开发的 whois 客户端用户界面。

## 作者

**Whois** 和本手册页由 Marco d'Itri `md@linux.it` 编写，并根据 GNU 通用公共许可证第 2 版或更高版本的条款授权。

2019-12-30 · Marco d'Itri