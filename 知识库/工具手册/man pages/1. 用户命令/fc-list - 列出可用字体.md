https://man.archlinux.org/man/fc-list.1.en

# fc-list

## 名称

`fc-list` — 列出可用字体

## 概要

```sh
fc-list [ -vVh ] [ --verbose ] [ -f format | --format format ] [ -q | --quiet ] [ --version ] [ --help ]
[ pattern [ element ... ] ]
```

## 描述

`fc-list` 列出系统中可供使用 fontconfig 的应用程序使用的字体和样式。如果指定了任何元素，则只打印这些元素。否则，除非请求详细输出，否则打印字体族和样式。

## 选项

本程序遵循通常的 GNU 命令行语法，长选项以两个短横线（`--`）开头。下面包含选项摘要。

- `-v --verbose`  
    为每个匹配打印整个字体模式的详细输出；如果提供了任何 `element`，则打印这些元素。

- `-f --format format`  
    根据格式说明符 `format` 格式化输出。

- `-q --quiet`  
    抑制所有正常输出。如果没有字体匹配，则返回 1 作为错误码。

- `-V --version`  
    显示程序版本并退出。

- `-h --help`  
    显示选项摘要。

- `pattern`  
    如果设置了此参数，则仅显示匹配 `pattern` 的字体。

- `element`  
    如果设置，则显示匹配字体的 `element` 属性。

## 示例

- `fc-list`  
    列出所有字体面。

- `fc-list :lang=hi`  
    列出覆盖印地语的字体面。

- `fc-list : family style file spacing`  
    列出每个字体面的文件名和 `spacing` 值。`:` 是匹配所有字体的空模式。

## 另请参阅

“fc-match(1)”、“FcFontList(3)”、“FcPatternFormat(3)”、“fc-cat(1)”、“fc-cache(1)”、“fc-pattern(1)”、“fc-query(1)”、“fc-scan(1)”

fontconfig 用户指南 <https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html>

## 作者

本手册页由 Keith Packard `<keithp@keithp.com>` 和 Josselin Mouette `<joss@debian.org>` 编写。

2008 年 8 月 13 日