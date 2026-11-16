https://www.man7.org/linux/man-pages/man1/setsid.1.html

# `setsid` - 在新会话中运行程序

## 概要

```sh
setsid [options] program [arguments]
```

## 描述

`setsid` 在新会话中运行程序。如果已经是进程组领导者，该命令会调用 `fork(2)`。否则，它在当前进程中执行程序。此默认行为可以通过 `--fork` 选项覆盖。

## 选项

- `-c`, `--ctty`  
    将控制终端设置为当前终端。

- `-f`, `--fork`  
    始终创建新进程。

- `-w`, `--wait`  
    等待程序执行结束，并将该程序的退出状态作为 `setsid` 的退出状态返回。

- `-h`, `--help`  
    显示帮助文本并退出。

- `-V`, `--version`  
    显示版本并退出。

## 作者

Rick Sladkey <jrs@world.std.com>

## 另请参见

“setsid(2)”

## 报告缺陷

关于缺陷报告，请使用问题跟踪器 <https://github.com/util-linux/util-linux/issues>。

## 可用性

`setsid` 命令是 util-linux 包的一部分，可从 Linux 内核存档 <https://www.kernel.org/pub/linux/utils/util-linux/> 下载。本页是 `util-linux`（一个 Linux 实用程序的随机集合）项目的一部分。项目信息可在 ⟨<https://www.kernel.org/pub/linux/utils/util-linux/>⟩ 找到。如果对本手册页有缺陷报告，请发送至 `util-linux@vger.kernel.org`。本页获取自项目上游 Git 仓库 ⟨git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git⟩，日期为 2026-08-04。（当时在仓库中找到的最近提交日期为 2026-08-03。）如果你发现此 HTML 版本页面中的任何渲染问题，或者你认为该页面有更好或更最新的来源，或者你对此 `COLOPHON` 中的信息有更正或改进（该 `COLOPHON` *不*属于原始手册页），请发送邮件至 `man-pages@man7.org`。

```text
util-linux 2.43.devel-739-eee2e 2026-05-24                      SETSID(1)
```