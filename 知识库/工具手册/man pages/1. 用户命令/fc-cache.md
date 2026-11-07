https://man.openbsd.org/fc-cache.1

# fc-cache

## 名称

`fc-cache` — 构建字体信息缓存文件

## 概要

```sh
fc-cache [ -cEfrsvVh ] [ --chroot root ] [ --error-on-no-fonts ] [ --force ] [ --really-force ] [ -y dir | --sysroot dir ] [ --system-only ] [ --verbose ] [ --version ] [ --help ] [ dir ... ]
```

## 描述

`fc-cache` 扫描系统上的字体目录，并为使用 fontconfig 处理字体的应用程序构建字体信息缓存文件。

如果未给定目录参数，`fc-cache` 会使用当前字体配置中的每个目录。每个目录都会被扫描，以查找 FreeType 可读取的字体文件。随后会创建一个缓存，其中包含每个字体的属性及关联的文件名。此缓存用于在使用 fontconfig 库时加快应用程序启动速度。

请注意，`fc-cache` 必须针对每种架构执行一次，以生成为该架构定制的字体信息。

## 选项

本程序遵循通常的 GNU 命令行语法，长选项以两个短横线（`--`）开头。下面包含选项摘要。

- `-E --error-on-no-fonts`  
    如果 `dir` 中没有字体，或者未给定配置中的目录中没有字体，则引发错误。

- `-c root --chroot root`  
    启动前将根目录切换到 `root`。

- `-f --force`  
    强制重新生成看似最新的缓存文件，覆盖时间戳检查。

- `-r --really-force`  
    删除所有现有缓存文件并重新扫描。

- `-s --system-only`  
    仅扫描系统级目录，省略用户主目录中的位置。

- `-v --verbose`  
    忙碌时显示状态信息。

- `-y -sysroot dir`  
    将所有扫描路径前加上 `dir`。

- `-h --help`  
    显示选项摘要。

- `-V --version`  
    显示程序版本并退出。

- `dir`  
    要扫描字体的目录。

## 返回码

如果缓存成功生成，`fc-cache` 返回零；否则返回非零。

## 文件

- `%cachedir%/*-%arch%.cache-%version%`  
    这些文件由 `fc-cache` 生成，包含从文件名到字体属性的映射。fontconfig 库会在应用程序启动时读取它们，以定位合适的字体。

## 另请参阅

`fc-cat(1)`、`fc-list(1)`、`fc-match(1)`、`fc-pattern(1)`、`fc-query(1)`、`fc-scan(1)`

fontconfig 用户指南 <https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html>

## 作者

本手册页由 Keith Packard `<keithp@keithp.com>` 和 Josselin Mouette `<joss@debian.org>` 编写。