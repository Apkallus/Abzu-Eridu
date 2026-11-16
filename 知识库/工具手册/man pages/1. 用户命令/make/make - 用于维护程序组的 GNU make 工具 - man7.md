https://www.man7.org/linux/man-pages/man1/make.1.html

# `make` - 用于维护程序组的 GNU make 工具

## 概要

```sh
make [OPTION]... [TARGET]...
```

## 描述

`make` 实用程序将自动确定大型程序中哪些部分需要重新编译，并发出重新编译它们的命令。本手册描述了 `make` 的 GNU 实现，它由 Richard Stallman 和 Roland McGrath 编写，目前由 Paul Smith 维护。我们的示例展示 C 程序，因为它们非常常见，但你可以将 `make` 与任何编译器可通过 shell 命令运行的编程语言一起使用。事实上，`make` 不仅限于程序。你可以用它来描述任何任务：某些文件必须在其他文件更改时自动更新。

要准备使用 `make`，你必须编写一个名为 makefile 的文件，描述程序中文件之间的关系，并提供更新每个文件的命令。在程序中，通常可执行文件从目标文件更新，而目标文件又通过编译源文件生成。

一旦存在合适的 makefile，每次你更改某些源文件时，这个简单的 shell 命令：

```sh
make
```

就足以执行所有必要的重新编译。`make` 程序使用 makefile 描述和文件的最后修改时间来决定哪些文件需要更新。对于每个这样的文件，它发出记录在 makefile 中的命令。

`make` 执行 makefile 中的命令来更新一个或多个目标，其中目标通常是程序。如果没有 `-f` 选项，`make` 将按顺序查找 makefile：`GNUmakefile`、`makefile` 和 `Makefile`。

通常你应该将 makefile 命名为 `makefile` 或 `Makefile`。（我们推荐 `Makefile`，因为它会在目录列表开头附近显眼地出现，紧邻其他重要文件如 `README`。）首先检查的名称 `GNUmakefile` 不推荐用于大多数 makefile。如果你有一个特定于 GNU `make` 的 makefile，并且其他版本的 `make` 无法理解，则应使用此名称。如果 `makefile` 为 `-`，则读取标准输入。

`make` 更新目标的条件是：它依赖于自上次修改目标以来已被修改的先决文件，或者目标不存在。

## 选项

- `-b`、`-m`  
    这些选项被忽略，以兼容其他版本的 `make`。

- `-B`、`--always-make`  
    无条件地 make 所有目标。

- `-C` `dir`、`--directory=dir`  
    在读取 makefile 或执行任何其他操作之前，切换到目录 `dir`。如果指定了多个 `-C` 选项，每个都相对于前一个解释：`-C / -C etc` 等价于 `-C /etc`。这通常用于 `make` 的递归调用。

- `-d`  
    除正常处理外，还打印调试信息。调试信息说明正在考虑重新生成哪些文件、正在比较哪些文件时间以及结果如何、哪些文件实际需要重新生成、考虑了哪些隐式规则以及应用了哪些——关于 `make` 如何决定要做什么的所有有趣内容。

- `--debug[=FLAGS]`  
    除正常处理外，还打印调试信息。如果省略 `FLAGS`，则行为与指定 `-d` 相同。`FLAGS` 可以是以下名称中的任意或全部，用逗号或空格分隔。只有第一个字符有意义，其余可以省略：`all` 表示所有调试输出（与使用 `-d` 相同），`basic` 表示基本调试，`verbose` 表示更详细的基本调试，`implicit` 表示显示隐式规则搜索操作，`jobs` 表示命令调用的详细信息，`makefile` 表示在重新生成 makefile 时进行调试，`print` 显示运行的所有配方（即使它们是静默的），`why` 显示 `make` 决定重建每个目标的原因。使用 `none` 禁用所有先前的调试标志。

- `-e`、`--environment-overrides`  
    使从环境获取的变量优先于 makefile 中的变量。

- `-E` `string`、`--eval` `string`  
    在解析任何 makefile 之前，使用 `eval` 函数解释 `string`。

- `-f` `file`、`--file=file`、`--makefile=FILE`  
    使用 `file` 作为 makefile。

- `-i`、`--ignore-errors`  
    忽略为重新生成文件而执行的命令中的所有错误。

- `-I` `dir`、`--include-dir=dir`  
    指定要在其中搜索包含的 makefile 的目录 `dir`。如果使用多个 `-I` 选项指定多个目录，则按指定顺序搜索这些目录。与 `make` 的其他标志参数不同，使用 `-I` 标志给出的目录可以直接跟在标志之后：允许 `-Idir`，也允许 `-I dir`。允许此语法是为了兼容 C 预处理器的 `-I` 标志。

- `-j` [`jobs`]、`--jobs[=jobs]`  
    指定同时运行的 `jobs`（命令）数量。如果有多个 `-j` 选项，则最后一个有效。如果给出 `-j` 选项而没有参数，`make` 将不限制可以同时运行的作业数量。

- `--jobserver-style=style`  
    要使用的 jobserver 风格。`style` 可以是 `fifo`、`pipe` 或 `sem`（仅限 Windows）之一。

- `-k`、`--keep-going`  
    出错后尽可能继续。虽然失败的目标以及依赖于它的目标无法重新生成，但这些目标的其他依赖项仍可以照常处理。

- `-l` [`load`]、`--load-average[=load]`  
    指定如果还有其他作业正在运行且负载平均值至少为 `load`（浮点数），则不应启动新作业（命令）。没有参数时，移除先前的负载限制。

- `-L`、`--check-symlink-times`  
    使用符号链接和目标之间最新的 mtime。

- `-n`、`--just-print`、`--dry-run`、`--recon`  
    打印将要执行的命令，但不执行它们（除非在某些情况下）。

- `-o` `file`、`--old-file=file`、`--assume-old=file`  
    即使 `file` 比其依赖项旧，也不要重新生成 `file`，也不要因 `file` 的更改而重新生成任何内容。本质上，该文件被视为非常旧，其规则被忽略。

- `-O`[`type`]、`--output-sync[=type]`  
    当使用 `-j` 并行运行多个作业时，确保每个作业的输出收集在一起，而不是与其他作业的输出交错。如果未指定 `type` 或为 `target`，则每个目标的整个配方的输出被分组在一起。如果 `type` 为 `line`，则配方中每个命令行的输出被分组在一起。如果 `type` 为 `recurse`，则整个递归 make 的输出被分组在一起。如果 `type` 为 `none`，则禁用输出同步。

- `-p`、`--print-data-base`  
    打印读取 makefile 后产生的数据库（规则和变量值）；然后照常执行或按其他指定执行。这也会打印 `-v` 开关提供的版本信息（见下文）。要打印数据库而不尝试重新生成任何文件，请使用 `make -p -f/dev/null`。

- `-q`、`--question`  
    “问题模式”。不运行任何命令，也不打印任何内容；只返回退出状态，如果指定目标已经是最新的，则为零，否则为非零。

- `-r`、`--no-builtin-rules`  
    消除内置隐式规则的使用。同时清除后缀规则的默认后缀列表。

- `-R`、`--no-builtin-variables`  
    不定义任何内置变量。

- `-s`、`--silent`、`--quiet`  
    静默操作；不打印正在执行的命令。

- `--no-silent`  
    取消 `-s` 选项的效果。

- `-S`、`--no-keep-going`、`--stop`  
    取消 `-k` 选项的效果。

- `-t`、`--touch`  
    触摸文件（将它们标记为最新而不真正更改它们）而不是运行其命令。这用于假装命令已完成，以欺骗未来的 `make` 调用。

- `--trace`  
    打印关于每个目标处置的信息（为什么重建目标以及运行什么命令来重建它）。

- `-v`、`--version`  
    打印 `make` 程序的版本以及版权、作者列表和无担保声明。

- `-w`、`--print-directory`  
    在其他处理之前和之后打印包含工作目录的消息。这对于追踪复杂的递归 `make` 命令嵌套中的错误可能很有用。

- `--no-print-directory`  
    关闭 `-w`，即使它是隐式打开的。

- `--shuffle[=MODE]`  
    启用目标和先决条件排序的随机化。`MODE` 是以下之一：`none` 禁用随机模式，`random` 以随机顺序随机化先决条件，`reverse` 以相反顺序考虑先决条件，或整数 `<seed>` 启用具有特定 `seed` 值的 `random` 模式。如果省略 `MODE`，默认为 `random`。

- `-W` `file`、`--what-if=file`、`--new-file=file`、`--assume-new=file`  
    假装目标 `file` 刚刚被修改。与 `-n` 标志一起使用时，这会显示如果你修改该文件会发生什么。没有 `-n` 时，这几乎等同于在运行 `make` 之前对给定文件运行 `touch` 命令，不同之处在于修改时间只在 `make` 的想象中改变。

- `--warn-undefined-variables`  
    当引用未定义变量时发出警告。

## 退出状态

如果所有 makefile 都成功解析且没有构建的目标失败，GNU `make` 以零状态退出。如果使用了 `-q` 标志并且 `make` 确定目标需要重建，将返回状态 1。如果遇到任何错误，将返回状态 2。

## 另请参见

`make` 的完整文档以 Texinfo 手册形式维护。如果 `info` 和 `make` 程序在你的站点正确安装，命令

```sh
info make
```

应该可以让你访问完整手册。

## 缺陷

参见 *The GNU Make Manual* 中的“Problems and Bugs”一章。

## 作者

本手册页由斯坦福大学的 Dennis Morse 贡献。Mike Frysinger 贡献了进一步的更新。它由 Roland McGrath 重新编写。由 Paul Smith 维护。

## 版权

版权所有 © 1992-1993, 1996-2022 Free Software Foundation, Inc. 本文件是 *GNU make* 的一部分。

GNU Make 是自由软件；你可以根据自由软件基金会发布的 GNU 通用公共许可证条款（许可证版本 3 或（由你选择）任何更新版本）重新分发和/或修改它。

GNU Make 分发时希望它有用，但不提供任何担保；甚至不提供适销性或特定用途适用性的暗示担保。更多详情请参见 GNU 通用公共许可证。

你应该已随此程序收到 GNU 通用公共许可证的副本。如果没有，请参见 <https://www.gnu.org/licenses/>。

## 版本说明

本页是 *make*（GNU make）项目的一部分。项目信息可在 ⟨<http://www.gnu.org/software/make/>⟩ 找到。如果对本手册页有缺陷报告，请参见 ⟨<http://www.gnu.org/software/make/>⟩。本页获取自 2026-08-04 从 ⟨<http://ftp.gnu.org/gnu/make/>⟩ 下载的 tarball `make-4.4.tar.gz`。如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
GNU                            31 May 2022                        MAKE(1)
```