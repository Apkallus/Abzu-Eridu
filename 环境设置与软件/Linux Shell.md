## bash 语法


### 变量

bash中无数据类型的概念、无需声明变量。

使用变量 `VAL=VALUE`
引用变量 `$VAL`

关键字**local**创建局部变量

变量名仅限字母数字下划线，于是`$VAL`将读取直到有效变量名外的字符。如：
`export PATH=$PATH:/usr/sbin`
变量在`:`符号终止，即使没有使用显式的分隔`${}`也可被shell识别。

`HISTSIZE` 设置历史记录长度

#### 环境变量 PATH

它在纯文本文件中存储了一系列绝对目录路径，由一系列用冒号分隔的绝对路径组成，shell 会在此目录列表中搜索与命令对应的程序。 

通过向此列表添加或替换目录，可让这些程序支持裸命令名启动
要永久添加用户的 PATH 变量，将其添加到该用户的`.bash_profile` 文件中。

### 命令链 & 控制

- `;`  
	命令链式组合的最简单方式是使用 `;`。在大多数上下文中，`;` 分隔命令的方式类似于用 Enter 键分隔行。

- `&&`  
	`&&` 运算符允许您仅在第一个命令成功时（遵循Linux惯例，即退出码为0）才运行第二个命令。这被称为"AND"运算符，因为需要同时满足两个条件：第一个命令必须成功*且*第二个命令才会运行。这对于需要特定操作依赖于其他操作成功执行的复杂命令行工作流非常有用。

- `||`  
	`||`运算符允许您在第一个命令失败（以非零代码退出）时才运行第二个命令。这被称为*OR*运算符，因为要么第一个命令成功*要么*第二个命令将运行。`||`运算符对于提供回退命令或错误处理非常有用！

- `bash [options] [file]`  
	Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。

### 重定向 & 管道符

<https://www.gnu.org/software/bash/manual/html_node/Redirections.html>

重定向 使用 shell 解释的特殊符号。 重定向允许复制、打开、关闭命令的文件句柄，使其指向不同的文件，并可以更改命令读取和写入的文件。
与 exec 内置命令一起使用时，重定向会修改当前 shell 执行环境中的文件句柄。
以下重定向运算符可以出现在简单命令的任何位置，也可以出现在命令之后。重定向按其出现的顺序（从左到右）进行处理。

每个可以以文件描述符编号开头的重定向，也可以改为以 `{varname}` 形式的单词开头。
- `exec {d}</` 重定向根目录，将自动分配的 fd 保存到变量 `$d`

重定向到文件：
`命令 > 文件`
- `>`将重定向的数据覆盖写入文件。如果指定的文件不存在，则创建。  
	权限为 `rw-rw-rw-` (`0666`)

	`>` 默认会重定向标准输出，但你可以通过在重定向符号前放置适当的标准文件描述符来指定是重定向标准输出还是标准错误：
	- `1>` stdout（默认）
	- `2>` stderr

重定向到文件并追加数据:
`命令 >> 文件`
- `>>` 被重定向的输出追加到文件中。同样，可以使用文件描述符来指定是将标准输出还是标准错误写入指定的文件。

从文件重定向输入：
`命令 < 文件` 或 `< 文件 命令`
- `<`也可以用来将文件重定向到程序的标准输入。

将一个程序的输出管道传输到另一个程序:
`命令 | 命令`
- `|` （管道符）用于将一个命令的标准输出重定向到另一个命令的标准输入。管道符`|`不被视为重定向操作符，而是一个控制操作符。


将标准错误重定向到标准输出:
- `2>&1` 在使用重定向时，你可以使用`&N`（其中 N=文件描述符）将两种输出方式重定向到同一个路径。这也可以与`|`控制运算符一起使用。


模式与技巧：
- `2>/dev/null`  
	丢弃错误信息
- `if ! 命令 >/dev/null 2>&1; then`  
	将命令的标准输出重定向到黑洞丢弃，将标准错误重定向到标准输出（当前为黑洞丢弃）。
	使用命令的返回状态码进行判断


### 展开与替换机制

当 shell 遇到空格时，它会结束变量赋值

默认情况下，在 Shell 会话中设置的变量仅在该 Shell 进程内局部有效。  
使用`export VAR`导出到子进程的环境变量后可被使用。

`env` 命令打印出 Shell 中设置的每一个*导出的*变量

#### `()` 子shell

圆括号 `(...)` 会启动一个 subshell（子进程的 bash） 来执行里面的命令。

子 shell 里对变量的修改一般也不会带回父 shell（除非 export 并且父 shell再读取环境等），这也是它“隔离”的一部分。

用于：
- 命令替换：`$(cmd)`
- 圆括号命令组：`( list )`

#### 展开

- [参数展开](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
	`$var` 和 `${var}`   
	变量名前加 `$` 符号，触发变量展开来引用变量。  
	用变量的值替换变量名，后面紧跟其他字符时，使用 `${}` 才能区分变量名边界。

    - `"${BIN_FILES[@]}"` 
        以数组元素为单位展开
    - `"${parameter:offset:length}"` 
        数组切片

- 命令替换  
	`$(command)` 或（已弃用）  `command`.  
	命令替换允许命令的输出替换命令本身，同时删除任何尾随的换行符。  
	命令替换 `$(cat file)` 可以被替换为等效但更快的 `$(< file)`  
	- 技巧：将命令作为字符串保存到变量中，然后使用命令替换执行变量的命令字符串
        - 如`TODAY=$(date)`设置运行日期
- 算术展开  
	`$(( expression ))`   
	在 shell 中做整数运算。

- 花括号展开  
	`{a,b,c}`，`{1..5}` 等  
	生成一组字符串，例如：

	```sh
	echo {1..3}
	1 2 3
	```

- 路径名展开 / 通配符  
	`*`、`?`、`[abc]`、`[a-z]` 等  
	把模式匹配到的文件名列出来。

- 波浪线展开  
	`~`  
	展开为用户的 home 目录。

- 历史展开  
	`!`   
	用历史命令或历史参数替换。

- 单双引号  
	在 Shell 中，所有引号都必须*成对匹配*，否则命令无效。
	- 单引号 `'...'` 几乎禁止一切展开
	- 双引号 `"..."` 保留大部分展开，但不解析为转义序列（`\n`）

- C 语言风格的转义  
	`$'...'`  
	得到真实字节，潜在用法：`VAL=$''`得到转义序列后使用 `echo "$VAL"`打印出回车换行

#### 进程替换

连接到一个命令输出创建的临时文件

- `命令B <(命令A)`  
	将命令A的输出连接到命令B的*参数*，即命令A的输出作为命令B的参数  
	当写入 `<(command)` 时，bash 将运行该命令并将其输出连接到一个它将创建的临时文件，它被称为*命名管道*
- `命令B >(命令A)`
	将命令B的输出连接到命令A的标准输入  
	当写入一个 `>(command)` 参数，bash 将运行 `command` 命令，但将其输入连接到一个临时命名管道文件。当命令B写入此文件时，数据会传送到命令A的标准输入



### bash 脚本

`bash [options] [file]`
Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。

按照惯例，Shell脚本通常以 `sh` 作为后缀命名
然后通过将其作为参数传递给新的Shell实例（`bash`）来执行！
当以这种方式调用Shell时，它不会从用户处获取命令，而是从文件中读取命令。

```sh
hacker@dojo:~$ bash pwn.sh
```

如果您的Shell脚本文件是*可执行的*（请回顾 linux-文件权限），您可以直接通过其相对路径或绝对路径调用它

### `#!` - Shebang

```bash
#!/bin/bash

echo "Hello Hackers!"
```

如果程序文件以字符`#!`开头（通常称为"Shebang"），Linux会将文件视为*解释型程序*，并将该行剩余内容视为*解释器*的路径。然后，内核会调用该解释器，并将程序文件的路径作为其唯一参数。

请注意，Shebang行必须位于文件的*第一行*——其前面不能有空行或空格！

常见Shebang：
- `#!/bin/bash` 用于bash脚本
- `#!/usr/bin/python3` 用于Python脚本
- `#!/bin/sh` 用于POSIX shell脚本——这是`bash`的一个功能较少但更兼容非Linux系统的原始前身！


### 参数

用户向 bash 脚本提供输入参数：
    在 bash 语法中，`$1` 代表传入的第一个参数，`$2` 是第二个参数，依此类推。此外
    `@`位置参数集合
    `$@` 所有传入的参数
    `$#` 参数的总数
    `$?` 最近终止命令的退出码，成功执行为0
    `$$` 得到当前 shell 的 pid

以下是一个简单示例：

```bash
hacker@dojo:~$ cat myscript.sh
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
hacker@dojo:~$ bash myscript.sh hello world
First argument: hello
Second argument: world
hacker@dojo:~$
```

切片示例：
```sh
for i in "${@:$OPTIND:$#}" 
```

### 条件

#### if else

```bash
if [ "$1" == "one" ]
then
    echo "1"
elif [ "$1" == "two" ]
then
    echo "2"
else
    echo "unknown"
fi
```

语法规则较为严格，主要有以下原因：
首先，*必须*在`if`后、`[`后以及`]`前保留空格；
其次，`if`、`then`和`fi`必须位于不同行（或用分号分隔），不能将它们合并到同一语句中。
另一个特殊之处是：`if`语句的结束标记是`fi`（即*if*的倒写），而非`endif`或`end`等常见形式。


与`if`类似，*必须*在`elif`后使用`then`

`else`没有条件——它会捕获所有之前未匹配的情况。它也不需要`then`语句。最后，`fi`需放置在`else`代码块之后，表示整个复合语句的结束

`if [ 条件 ]; then` 这里的 `[` 实际上是一个命令，等价于：
`test 条件`

#### case

 `case` 语句，它允许你针对一个变量匹配多个值，而无需通过一长串 `if-else` 语句。`case` 语句的语法如下所示。该语句以 `esac` 结束，即 `case` 的倒写

```sh
case 表达式 in
  Pattern_Case_1)
   STATEMENTS
   ;;
 Pattern_Case_1)
   STATEMENTS
   ;;
 Pattern_Case_N)
   STATEMENTS
   ;;
 *)
   STATEMENTS
   ;;
esac
```

### 循环

```bash
# 从1开始，间隔5，直到100
for i in $(seq 1 5 100); do
    echo "select substr(datum, $i, 5) from dataset;" \
    | /challenge/sql \
    | grep "substr(datum" \
    | sed -e "s/.*, 5)': '//" -e "s/'}.*//"
    
done | tr -d '\n'
```

```bash
# 循环输出 0x01 与 0xff 两个字节（竞争条件）
while true; do
echo -ne "\x01\xff";
done | hd
```

### 函数

```sh
# 函数定义
function_name(){
    commands
    ...
}

# 函数调用
function_name
```

### 操作符

```sh
[ -n "$var" ]   # var 非空？
[ -z "$var" ]   # var 为空？（-z 是 is zero-length）
```

`-n`、`-z` 是 字符串测试 的一元（单目）操作符

判断文件是否存在:
`-e path`：存在（不管是文件还是目录）
`-f path`：存在且是普通文件
`-d path`：存在且是目录

### 正则表达式

https://www.rexegg.com/regex-quickstart.html

正则表达式由两部分组成：常量和运算符。常量是字符串集，而运算符是表示对这些字符串进行操作的符号。这两个元素共同使正则表达式成为强大的模式匹配工具。以下是表示字符的正则表达式运算符的快速概述：

- `\d` 匹配任何数字。
- `\w` 匹配任何字符。
- `\s` 匹配任何空白字符，`\S` 匹配任何非空白字符。
- `.` 匹配任何单个字符。
- `\` 转义一个特殊字符。
- `^` 匹配字符串或行的开头。
- `$` 匹配字符串或行的结尾。

还有几个运算符指定要匹配的字符数：

- `*` 匹配前一个字符零次或多次。
- `+` 匹配前一个字符一次或多次。
- `{3}` 匹配前一个字符三次。
- `{1,3}` 匹配前一个字符一至三次。
- `{1,}` 匹配前一个字符一次或多次。
- `[abc]` 匹配括号内的一个字符。
- `[a-z]` 匹配 a 到 z 范围内的一个字符。
- `(a|b|c)` 匹配 a 或 b 或 c。

## Shell 启动文件

### .bashrc

当你的 shell 启动时，它会在你的主目录中寻找 `.bashrc` 文件并将其作为*启动脚本*执行。

你可以通过设置环境变量、调整 shell 配置等方式，自定义 `/home/用户名/.bashrc` 以添加实用功能。

恶意软件常以 `.bashrc` 等启动脚本为目标，以实现持久化驻留！

获取二进制文件路径数组，对所有 elf 文件使用base64编码后保存到home目录
```sh
#!/bin/bash

export PS4='${BASH_SOURCE} >>> '

set -x
# 显示挑战目录内容
ls -al /challenge/
set +x 2>/dev/null

MY_COPY_DIR=~/challenge-copy/

# 清空当前复制目录并新建
rm -rf "$MY_COPY_DIR"
mkdir -p "$MY_COPY_DIR"

# 复制挑战目录内容到复制目录
cp -r /challenge/* "$MY_COPY_DIR"

# 获取二进制文件路径数组
mapfile -t BIN_FILES < <(file /challenge/* | grep ELF | sed 's/: \{1,\}.*$//')

# 遍历二进制文件路径数组
for file_path in "${BIN_FILES[@]}"; do

    # 从路径提取文件名
    name="$(basename "$file_path")"
    # 对二进制文件进行base64编码后重命名
    base64 "$file_path" > "$MY_COPY_DIR/$name.base64"

    set -x
    # 查看二进制文件的安全信息
    checksec "$file_path"

    set +x 2>/dev/null
done

# 打印找到的工具到文件
# ropper --file  "$BIN_FILE_PATH" --nocolor > log_rop.log

# 打印 ret2cus 地址
# objdump -d -M intel "$BIN_FILE_PATH" | grep -n "__libc_csu_init" -A80 | grep -n "4c 89 f2" -A14

# 查看 cpu 对 shstk/ibt 的支持
# grep -m1 -oE 'shstk|ibt' /proc/cpuinfo

# /challenge/run
```

### .bash_profile

.bash_profile 是每个用户主目录中的一个隐藏文件，用于定义该用户特定的环境变量和启动程序。

例如：添加程序目录到 `PATH` 环境变量，而无需指定其绝对路径


## 功能

### alias - 别名

`alias 别名=指令名称` 

在 .bashrc 将常用长串指令设置为别名

### read

`read` 从标准输入*读取*到变量中  `read 变量`  
注，仅读一行。
- `-p` 参数的示例，该参数允许您指定提示信息  
    `read -p "输入提示" 变量`  

### echo

`echo` 打印到标准输出  
- `echo $VAR` 做单词分割：把换行当空格处理
- `echo "$VAR"` 使用双引号展开变量到一个字符串中

### test

`test` 命令评估条件并输出 `true` 或 `false`

常见形式：`[ 条件标志 表达式 ]`

- `-f` 标志测试文件是否存在。
- `-eq` 和 `-ne` 标志分别测试相等和不相等
- `-gt`、`-ge`、`-lt` 和 `-le` 标志分别测试大于、大于或等于、小于、小于或等于
- `-z` 和 `-n` 标志测试字符串是否为空
- `-d`、`-f` 标志检查目录和文件是否存在
- `-r`、`-w` `-x` 标志检查目录和文件权限

使用 `&&` `||` `!` 来组合测试表达式

### source - 在当前 shell 环境中执行存储在文件中的命令

`source 文件名`

### trap '...' DEBUG

在每一命令执行前触发一次

例：
- `trap 'echo ">>> 执行命令: $BASH_COMMAND"' DEBUG`

### getopts - 解析选项

https://www.geeksforgeeks.org/linux-unix/getopts-command-in-linux-with-examples/

`getopts optstring name [arg]`

### set -x/set +x（xtrace）

- `set -x` 
	- 会让 Bash 在执行每条命令之前，把“即将执行的命令（展开后的结果）”打印到标准错误（stderr）。常用于调试脚本：看变量展开成了什么、走了哪个分支、实际运行了哪些子命令。
	- 每行前面默认是 `+`

- `set +x`
	关闭

- `PS4`
	环境变量，控制 xtrace 的前缀

例：
	```sh
	export PS4='${BASH_SOURCE} >>> '

	set -x
	ls -al /challenge/
	set +x 2>/dev/null
	```

### exec

- `exec /程序` 替换当前进程到对应程序
- `exec 3</` 将根目录重定向到 fd 3
    - `exec {fdn}</; echo $fdn` 将根目录重定向到自动分配的空闲 fd，并使用 `echo` 查看对应 fd，`fdn` 为普通变量名


### mapfile & readarray

```
mapfile [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]
readarray [-n count] [-O origin] [-s count] [-t] [-u fd] [-C callback] [-c quantum] [array]
```

从标准输入读取行到索引数组变量array中，如果提供-u选项，则从文件描述符fd读取。变量MAPFILE是默认的数组。如果提供选项，则具有以下含义：
- `-t`
    删除每行读取后的换行符。

示例：
- `mapfile -t BIN_FILES  < <(file /challenge/* | grep ELF)`

### whiptail - 从 shell 脚本中显示对话框

```
whiptail [ --title title ] [ --backtitle backtitle ] [ --clear ] [ --default-item string ] [ --defaultno ] [ --fb ] [ --nocancel ] [ --yes-button text ] [ --no-button text ] [ --ok-button text ] [ --cancel-button text ] [ --noitem [ ] --output-fd fd ] [ --separate-output ] [ --scrolltext ] [ --topleft ] box-options
```

whiptail 是一个程序，它允许你使用从 shell 脚本中的对话框来提出各种问题或显示消息。目前，这些类型的对话框已经实现：
是/否框、菜单框、输入框、消息框、文本框、信息框、复选框、单选框、进度条框和密码框。

- `--textbox file height width`
	文本框允许你在对话框中显示文本文件的内容，类似于一个简单的文本文件查看器。
	- `whiptail --textbox /flag 10 70`

### awk - 模式扫描和处理语言

`gawk [ POSIX or GNU style options ] -f program-file [ -- ] file ...`

`awk 'pattern { action }' input_file`
- 模式:
	可以是正则表达式（如 /error/）、条件表达式（如 $3 > 100）或特殊模式 BEGIN / END。
	- `BEGIN{ }`：在处理任何输入行之前执行一次。常用于初始化变量。
	- `END{ }`：在处理完所有输入行之后执行一次。常用于汇总输出。

示例：
- `awk '{print}' /flag`

