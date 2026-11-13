https://docs.python.org/zh-cn/3.15/library/pstats.html

# pstats --- 性能分析器的统计信息¶

`pstats` 模块提供了用于读取、操纵和显示由 Python 的性能分析器生成的性能分析统计信息。 它能够读取来自 `profiling.tracing` (确定型性能分析器) 和 `profiling.sampling` (统计型性能分析器) 的输出。

## 命令行接口

pstats 模块可作为脚本调用，以交互式方式浏览配置文件数据:

```sh
python -m pstats profile.bin
```

这将打开一个以行为导向的界面（基于 `cmd` 构建），用于查看统计信息。在提示符处输入 `help`，以查看可用命令。

```log
profile.bin% help

Documented commands (type help <topic>):
========================================
EOF  add  callees  callers  help  quit  read  reverse  sort  stats  strip
```

```log
profile.bin% help sort
Sort profile data according to specified keys.
(Typing `sort' without arguments lists valid keys.)

profile.bin% sort
Valid sort keys (unique prefixes are accepted):
calls -- call count
ncalls -- call count
cumtime -- cumulative time
cumulative -- cumulative time
filename -- file name
line -- line number
module -- file name
name -- function name
nfl -- name/file/line
pcalls -- primitive call count
stdname -- standard name
time -- internal time
tottime -- internal time


```log
profile.bin% help stats
Print statistics from the current stat object.
Arguments may be:
* An integer maximum number of entries to print.
* A decimal fractional number between 0 and 1, controlling
  what fraction of selected entries to print.
* A regular expression; only entries with function names
  that match it are printed.
```


```console
$ python -m pstats profile.bin
profile.bin% sort tottime
profile.bin% stats 20
```