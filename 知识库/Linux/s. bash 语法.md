## 3. 基本 Shell 特性

### 3.4 Shell 参数

#### 3.4.2 特殊参数

- `-`  
    （`$-`，连字符。）展开为当前选项标志，这些标志在调用时指定、由 `set` 内建命令指定，或由 shell 自身设置（例如 `-i` 选项）。

    ```console
    $ echo $-
    himBHs
    $ bash -c 'echo $-'
    hBc
    ```

## 4. 内建命令

### alias —— 打印或设置命令别名

```bash
alias [-p] [name[=value] ...]
```

不带参数或带 `-p` 选项时，`alias` 会以可重新作为输入使用的形式，将别名列表打印到标准输出。如果提供了参数，则为每个给出了 `value` 的 `name` 定义别名。

```sh
# 设置 ls 开启终端输出高亮
alias ls='ls --color=auto'
```

### command —— 执行或显示命令

```sh
command [-pVv] command [arguments ...]
```

`command` 内建命令运行 `command` 及 `arguments`，并忽略任何名为 `command` 的 shell 函数。只会执行 shell 内建命令或通过搜索 `PATH` 找到的命令。

如果提供了 `-V` 或 `-v` 选项，`command` 会打印 `command` 的描述。`-v` 选项显示一个单词，指示用于调用 `command` 的命令或文件名；`-V` 选项产生更详细的描述。在这种情况下，如果找到 `command`，返回状态为零；否则为非零。

示例
```console
$ command id
uid=1000(hacker) gid=1000(hacker) groups=1000(hacker)

$ command -v id
/run/dojo/bin/id

$ command -V id
id is /run/dojo/bin/id
```
- `-v` 可用来寻找命令路径

### read —— 读取到变量

```sh
read [-Eers] [-a aname] [-d delim] [-i text] [-n nchars]
    [-N nchars] [-p prompt] [-t timeout] [-u fd] [name ...]
```

从标准输入读取一行，或者从作为 `-u` 选项参数提供的文件描述符 `fd` 读取一行，按照上文 [Word Splitting] 中所述将其拆分为单词，并将第一个单词赋给第一个 `name`，第二个单词赋给第二个 `name`，依此类推。

示例

```sh
read FLAG </flag
```


### mapfile —— 设置索引数组变量

```sh
mapfile [-d delim] [-n count] [-O origin] [-s count]
    [-t] [-u fd] [-C callback] [-c quantum] [array]
```

从标准输入读取行，或者如果提供了 `-u` 选项，则从文件描述符 `fd` 读取行，并将其放入索引数组变量 `array`。变量 `MAPFILE` 是默认的 `array`。如果提供了选项，其含义如下：

- `-d`  
    使用 `delim` 的第一个字符而不是换行符来终止每个输入行。如果 `delim` 是空字符串，`mapfile` 将在读到 NUL 字符时终止一行。

- `-n`  
    最多复制 `count` 行。如果 `count` 为 0，则复制所有行。

- `-t`  
    从读取的每一行中移除末尾的 `delim`（默认换行符）。

- `-u`  
    从文件描述符 `fd` 而不是标准输入读取行。

- `-C`  
    每读取 `quantum` 行就求值一次 `callback`。`-c` 选项指定 `quantum`。

- `-c`  
    指定每次调用 `callback` 之间读取的行数。

如果指定了 `-C` 而未指定 `-c`，默认 `quantum` 为 5000。当求值 `callback` 时，会将下一个要赋值的数组元素索引和要赋给该元素的行作为附加参数提供给它。`callback` 在读取行之后、赋值数组元素之前求值。

如果未提供显式起始索引，`mapfile` 会在赋值前清除 `array`。

```sh
# find 得到按行分隔的路径，mapfile 去除换行符存入数组，遍历使用 basename 得到文件名
mapfile -t file_list < <(find /challenge | awk -F ':' '{print $1}')   
for file_path in "${file_list[@]}"; do

    # 从路径提取文件名
    name="$(basename "$file_path")"
    # 对二进制文件进行base64编码后重命名
    base64 "$file_path" > "$MY_COPY_DIR/$name.base64"

    set -x
    # 查看二进制文件的安全信息
    checksec "$file_path"

    set +x 2>/dev/null
done
```

### 6.1 调用 Bash

与 `set` 内建命令一起使用的所有单字符选项（参见“Set 内建命令”）都可以在调用 shell 时作为选项使用。

还有一些单字符选项可以在调用时提供，但 `set` 内建命令不支持这些选项。

- `-i`  
    强制 shell 以交互方式运行。交互式 shell 在“交互式 Shell”中描述。

### 6.3 交互式 Shell

#### 6.3.2 此 Shell 是交互式的吗？

要在启动脚本中判断 Bash 是否以交互方式运行，请测试特殊参数 `-` 的值。当 shell 为交互式时，它包含 `i`。例如：

```sh
case "$-" in
    *i*)	echo This shell is interactive ;;
    *)	echo This shell is not interactive ;;
esac
```