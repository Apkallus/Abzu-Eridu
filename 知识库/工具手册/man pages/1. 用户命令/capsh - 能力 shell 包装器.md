https://www.man7.org/linux/man-pages/man1/capsh.1.html

# `capsh` - 能力 shell 包装器

## 概要

```sh
capsh [OPTION]...
```

## 描述

可以使用此工具探索和约束 Linux 能力支持与使用。此工具为某些类型的能力测试和环境创建提供了方便的包装器。它还提供了一些调试功能，可用于汇总能力状态。

## 选项

`capsh` 接受若干可选参数，并按提供顺序作用于它们。如下：

- `--help`  
  显示 `capsh` 支持的命令列表。

- `--print`  
  显示当前能力及相关状态。

- `--current`  
  显示当前能力状态、1e 能力和 `IAB` 向量。

- `-- [args]`  
  使用尾部参数执行 `/bin/bash`。注意，可以使用 `-c 'command to execute'` 执行特定命令。

- `-+ [args]`  
  使用 [cap_launch(3)] fork 一个子进程来执行 shell。当子进程退出时，`capsh` 以子进程的状态退出；若子进程被信号终止，则以 `1` 退出。

- `== [args]`  
  使用剩余参数再次执行 `capsh`。可用于测试 `exec()` 行为。注意，当正在运行的 `capsh` 是通过 shell 的 `PATH` 搜索找到时，会搜索 `PATH`。如果 `exec` 发生在 `--chroot=/some/path` 参数之后，`PATH` 定位到的二进制文件可能不会解析为最初运行的同一个二进制文件。此行为是有意设计的，因为它可以完成 chroot 过渡。

- `=+ [args]`  
  使用 [cap_launch(3)] fork 一个子进程来重新执行 `capsh`。当此子进程退出时，`capsh` 以子进程的状态退出；若子进程被信号终止，则以 `1` 退出。

- `--caps=cap-set`  
  将当前进程能力设置为 `cap-set` 指定的能力。其中 `cap-set` 是按 [cap_text_formats(7)] 表示的能力 `Set` 的文本表示。

- `--drop=cap-list`  
  从当前边界集中移除列出的能力。能力是由 [cap_from_name(3)] 函数识别的逗号分隔能力列表。使用此功能要求 `capsh` 在其有效集中具有 `CAP_SETPCAP`。

- `--inh=cap-list`  
  将当前进程的可继承能力集设置为逗号分隔列表中提供的能力。要使此操作成功，当前进程应已在当前可继承和许可能力集的并集中具有这些能力中的每一个，或者 `capsh` 应在其有效集中具有 `CAP_SETPCAP`。

- `--user=username`  
  假定命名用户的身份。也就是说，使用 [getpwuid(3)] 查找用户的 UID 和 GID，使用 [getgrouplist(3)] 查找其组成员关系，并使用 [cap_setuid(3)] 和 [cap_setgroups(3)] 设置它们。执行此命令后，有效能力将被清除，但许可集不会被清除，因此正在运行的程序仍具有特权。

- `--mode`  
  显示由 [cap_get_mode(3)] 函数猜测的当前 libcap 模式。

- `--mode=<mode>`  
  强制程序进入 [cap_set_mode(3)] 安全模式。这是一组安全位和当前能力安排，因其预定的安全姿态而被推荐。

- `--modes`  
  列出 `--mode=<mode>` 支持的所有 libcap 模式。

- `--inmode=<mode>`  
  确认当前模式为 `<mode>` 中指定的模式，否则以状态 `1` 退出。

- `--uid=id`  
  使用 [setuid(2)] 系统调用强制所有 UID 值等于 `id`。此参数可能需要显式准备有效集。

- `--cap-uid=<uid>`  
  使用 [cap_setuid(3)] 函数设置当前进程的 UID。这会完成设置 UID 的所有准备工作，而不会在进程中丢弃能力。执行此命令后，当前有效能力将被降低。

- `--is-uid=<id>`  
  除非当前 UID 等于 `<id>`，否则以状态 `1` 退出。

- `--gid=<id>`  
  使用 [setgid(2)] 系统调用强制所有 GID 值等于 `<id>`。

- `--is-gid=<id>`  
  除非当前 GID 等于 `<id>`，否则以状态 `1` 退出。

- `--groups=<gid-list>`  
  将补充组设置为提供的数字列表。这些组使用 [setgroups(2)] 系统调用设置。有关更方便的方法，请参见 `--user`。

- `--keep=<0|1>`  
  在非纯能力模式下，内核向超级用户提供宽松特权。然而，通常当超级用户将 UID 更改为某个较低权限用户时，能力会被丢弃。对于这些情况，内核可以允许进程在 [setuid(2)] 系统调用后保留其能力。此功能称为 `keep-caps` 支持。使用此程序激活它的方式就是此参数。将值设置为 `1` 将使 `keep-caps` 生效。将其设置为 `0` 将使当前进程的 `keep-caps` 停用。在所有情况下，执行 `exec()` 时 `keep-caps` 都会停用。有关禁用此功能的方法，请参见 `--secbits` 和 `--mode`。

- `--secbits=N`  
  设置程序的安全位。这是通过 [prctl(2)] 的 `PR_SET_SECUREBITS` 操作完成的。支持位及其含义列表可在 `<sys/secbits.h>` 头文件中找到。程序将通过 `--print` 命令列出这些位。参数表示为数字位掩码，格式为 [strtoul(3)] 允许的任何格式。这种位操作的替代方案内置于 `--mode*` 命令行参数中。

- `--chroot=/some/path`  
  使用新根目录（`/`）等于 `path` 执行 [chroot(2)] 系统调用。此操作要求 `CAP_SYS_CHROOT` 生效。

- `--forkfor=sec`  
  此命令使程序 fork 一个子进程，持续 `sec` 秒。子进程将睡眠那么长时间，然后以状态 `0` 退出。此命令的目的是支持探索在能力变化情况下进程可被杀死的方式。参见 `--killit` 命令。一次只能有一个 fork 处于活动状态。

- `--killit=sig`  
  此命令使 `--forkfor` 子进程被 [kill(2)] 以指定信号杀死。然后命令等待子进程退出。如果退出状态与用于杀死它的信号不匹配，`capsh` 程序以状态 `1` 退出。

- `--explain=cap_xxx`  
  简要文本描述指定能力为正在运行的程序提供哪些特权。注意，可以不用 `cap_xxx`，而是提供十进制数字，`capsh` 将查找相应能力的描述。

- `--shell=/full/path`  
  此选项更改遇到参数 `==` 时调用的 shell。

- `--strict`  
  此选项切换对后续修复 `--caps=` 和 `--inh=` 参数的抑制。也就是说，当当前 `Effective` 标志不包含 `CAP_SETPCAP` 时，待提升的 `Inheritable` 标志值（在严格模式下）仅限于 `Permitted` 集合中的值。严格模式默认关闭。提供此参数偶数次会恢复此默认行为。

- `--suggest=phrase`  
  扫描 `capsh` 已知的每个能力文本描述，并显示所有包含 `phrase` 的描述。

- `--decode=N`  
  这是一个便利功能。如果查看 `/proc/1/status`，其中有一些与能力相关的字段，形式如下：

    ```log
    CapInh:   0000000000000000
    CapPrm:   0000003fffffffff
    CapEff:   0000003fffffffff
    CapBnd:   0000003fffffffff
    CapAmb:   0000000000000000
    ```

  此选项提供一种快速解码以这种十六进制形式表示的能力向量的方法。下面是一个解码最低两个能力位的示例：

    ```console
    $ capsh --decode=3
    ```
    ```log
    0x0000000000000003=cap_chown,cap_dac_override
    ```

- `--supports=xxx`  
  随着内核演进，会添加更多能力。此选项可用于验证系统上是否存在某个能力。例如，在内核 2.6.27 上运行时，`--supports=cap_syslog` 会使 `capsh` 立即以状态 `1` 退出。然而，在内核 2.6.38 上运行时，它会静默成功。

- `--has-p=xxx`  
  除非 `permitted` 向量中提升了能力 `xxx`，否则以状态 `1` 退出。

- `--has-ambient`  
  执行检查以查看正在运行的内核是否支持 `ambient` 能力。如果不支持，`capsh` 以状态 `1` 退出。

- `--has-a=xxx`  
  除非 `ambient` 向量中提升了能力 `xxx`，否则以状态 `1` 退出。

- `--has-b=xxx`  
  除非 `bounding` 向量中能力 `xxx` 处于（默认）非阻塞状态，否则以状态 `1` 退出。

- `--iab=xxx`  
  尝试设置可继承能力向量的 `IAB` 元组。用于 `xxx` 的文本约定是 [cap_iab_from_text(3)] 的约定，并在 [cap_text_formats(7)] 中描述。

- `--addamb=xxx`  
  将指定的 `ambient` 能力添加到正在运行的进程。

- `--delamb=xxx`  
  从正在运行的进程中移除指定的 `ambient` 能力。

- `--noamb`  
  从正在运行的进程中丢弃所有 `ambient` 能力。

- `--noenv`  
  当处理后续 `--user` 参数时，抑制对 `HOME` 和 `USER` 环境变量的覆盖。

- `--quiet`  
  除非它是第一个参数，否则忽略此参数。如果存在，它会抑制 `capsh` 运行时检查，以确认正在运行的 `libcap` 足够新，能够命名内核支持的所有能力值。

## 退出状态

成功执行后，`capsh` 以状态 `0` 退出。发生错误后，`capsh` 立即以状态 `1` 退出。

## 作者

由 Andrew G. Morgan <`morgan@kernel.org`> 编写。

## 报告缺陷

请通过以下地址引用的缺陷跟踪器报告缺陷：

<https://sites.google.com/site/fullycapable>

## 另请参阅

[libcap(3)]、[cap_from_text(3)]、[cap_iab(3)]、[cap_text_formats(7)]、[capabilities(7)]、[captree(8)]、[getcap(8)]、[getpcaps(8)] 和 [setcap(8)]。

## 版本说明

本页是 *libcap*（能力命令和库）项目的一部分。项目信息可在 <https://sites.google.com/site/fullycapable/> 找到。若对本手册页有缺陷报告，请发送至 `morgan@kernel.org`（请在主题行中注明“libcap”）。本页取自该项目上游 Git 仓库 <https://git.kernel.org/pub/scm/libs/libcap/libcap.git/>，获取日期为 2026-08-04。（当时仓库中找到的最近提交日期为 2026-07-30。）如果你发现本页 HTML 版本的任何渲染问题，或认为本页有更好或更新的来源，或对本版本说明中的信息（该信息*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

`libcap` · 2026-04-07 · `CAPSH(1)`