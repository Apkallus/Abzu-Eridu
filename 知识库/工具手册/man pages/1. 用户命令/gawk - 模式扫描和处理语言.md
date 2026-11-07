https://www.man7.org/linux/man-pages/man1/gawk.1.html

# `gawk` - 模式扫描和处理语言

## 概要

```sh
gawk [ POSIX or GNU style options ] -f program-file [ -- ] file ...
gawk [ POSIX or GNU style options ] [ -- ] program-text file ...
```

## 首先阅读

本手册页是*礼节性*提供的。请注意，`gawk` 的唯一权威来源是 Texinfo 手册 *GAWK: Effective AWK Programming*，可在以下链接以多种格式在线获取：<https://www.gnu.org/software/gawk/manual>。应始终将 Texinfo 手册视为权威版本。

本手册页有意尽可能简洁。完整细节在手册中提供，对于任何特定功能的完整说明，您应查阅该手册。在可能的情况下，提供了指向手册在线版本的链接。

此外，`gawk` 维护者保留在未来从发行版中移除此手册页的权利，以减轻其维护负担。

## 描述

`gawk` 是 GNU 项目对 AWK 编程语言的实现。它符合 POSIX 1003.1 标准中的语言定义。此版本又基于 Aho、Kernighan 和 Weinberger 所著 *The AWK Programming Language* 第一版（1987 年）中的描述。`gawk` 提供了 Brian Kernighan 当前版本 `awk` 中的附加功能以及大量 GNU 特有扩展。

命令行由以下部分组成：`gawk` 本身的选项、AWK 程序文本（如果不是通过 `-f` 或 `--include` 选项提供），以及要在预定义 AWK 变量 `ARGC` 和 `ARGV` 中使用的值。

## 选项格式

`gawk` 选项可以是传统的 POSIX 风格单字母选项，也可以是 GNU 风格长选项。POSIX 选项以单个“-”开头，而长选项以“--”开头。

## 选项

`gawk` 接受以下选项。标准选项列在前面，随后是按短选项字母顺序排列的 `gawk` 扩展选项。选项的完整说明见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Options>。

- 
    ```
    -f program-file
    --file program-file
    ```
    从文件 `program-file` 读取 AWK 程序源代码，而不是从第一个命令行参数读取。可以多次使用 `-f` 选项。

- 
    ```
    -F fs
    --field-separator fs
    ```
    使用 `fs` 作为输入字段分隔符（预定义变量 `FS` 的值）。

- 
    ```
    -v var=val
    --assign var=val
    ```
    在程序开始执行之前，将值 `val` 赋给变量 `var`。

- 
    ```
    -b
    --characters-as-bytes
    ```
    将所有输入数据视为单字节字符。`--posix` 选项会覆盖此选项。

- 
    ```
    -c
    --traditional
    ```
    以*兼容*模式运行。

- 
    ```
    -C
    --copyright
    ```
    在标准输出上打印 GNU 版权信息的简短版本，并成功退出。

- 
    ```
    -d[file]
    --dump-variables[=file]
    ```
    将全局变量及其类型和最终值的排序列表打印到 `file`。默认文件是当前目录中的 `awkvars.out`。

- 
    ```
    -D[file]
    --debug[=file]
    ```
    启用 AWK 程序调试。有关调试器的详细信息，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Debugger>。

- 
    ```
    -e program-text
    --source program-text
    ```
    使用 `program-text` 作为 AWK 程序源代码。

- 
    ```
    -E file
    --exec file
    ```
    类似于 `-f`，但此选项是最后处理的选项。它应与 `#!` 脚本一起使用，特别是用于 CGI 应用程序，以避免从 URL 在命令行中传入选项或源代码（！）。此选项禁用命令行变量赋值。

- 
    ```
    -g
    --gen-pot
    ```
    扫描并解析 AWK 程序，并在标准输出上生成 GNU `.pot`（Portable Object Template，可移植对象模板）格式文件，其中包含程序中所有可本地化字符串的条目。程序本身不会运行。

- 
    ```
    -h
    --help
    ```
    在标准输出上打印可用选项的简短摘要。根据 *GNU 编码标准*，这些选项会导致立即成功退出。

- 
    ```
    -i include-file
    --include include-file
    ```
    加载 awk 源代码库。更多信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/AWKPATH-Variable>。

- 
    ```
    -I
    --trace
    ```
    在程序运行时，将执行的内部字节码名称打印到标准错误。

- 
    ```
    -k
    --csv
    ```
    启用 CSV 特殊处理。更多信息请参见下文“逗号分隔值”。

- 
    ```
    -l lib
    --load lib
    ```
    从共享库 `lib` 加载 `gawk` 扩展。更多信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/AWKLIBPATH-Variable>。

- 
    ```
    -L [value]
    --lint[=value]
    ```
    对可疑的或不可移植到其他 AWK 实现的结构提供警告。有关 `value` 可能取值的列表，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Options>。

- 
    ```
    -M
    --bignum
    ```
    强制对数字进行任意精度算术运算。如果 `gawk` 未编译为使用 GNU MPFR 和 GMP 库，则此选项无效。（在这种情况下，`gawk` 会发出警告。）

- 
    ```
    -n
    --non-decimal-data
    ```
    识别输入数据中的八进制和十六进制值。*请非常谨慎地使用此选项！*

- 
    ```
    -N
    --use-lc-numeric
    ```
    强制 `gawk` 在解析输入数据时使用区域设置的小数点字符。

- 
    ```
    -o[file]
    --pretty-print[=file]
    ```
    将程序的漂亮打印版本输出到 `file`。默认文件是当前目录中的 `awkprof.out`。此选项隐含 `--no-optimize`。

- 
    ```
    -O
    --optimize
    ```
    对程序的内部表示应用 `gawk` 的默认优化。这是默认行为。

- 
    ```
    -p[prof-file]
    --profile[=prof-file]
    ```
    启动性能分析会话，并将分析数据发送到 `prof-file`。默认是当前目录中的 `awkprof.out`。此选项隐含 `--no-optimize`。

- 
    ```
    -P
    --posix
    ```
    开启*兼容*模式，并禁用许多常见扩展。

- 
    ```
    -s
    --no-optimize
    ```
    禁用 `gawk` 对程序内部表示的默认优化。

- 
    ```
    -S
    --sandbox
    ```
    以沙箱模式运行 `gawk`。

- 
    ```
    -V
    --version
    ```
    在标准输出上打印此 `gawk` 副本的版本信息。这在报告缺陷时很有用。根据 *GNU 编码标准*，这些选项会导致立即成功退出。

- `--`  
    表示选项结束。这很有用，可以允许 AWK 程序本身的后续参数以“-”开头。

在兼容模式下，任何其他选项都会被标记为无效，但除此之外会被忽略。在正常操作中，只要已提供程序文本，未知选项就会通过 `ARGV` 数组传递给 AWK 程序进行处理。

为了 POSIX 兼容性，可以使用 `-W` 选项，后跟长选项的名称。

## AWK 程序执行

AWK 程序由一系列可选指令、模式-动作语句和可选函数定义组成。

```awk
@include "filename"
@nsinclude "filename"
@load "filename"
@namespace "name"
pattern   { action statements }
function name(parameter list) { statements }
```

`gawk` 首先从 `program-file`（如果指定）、`--source` 的参数或命令行上第一个非选项参数读取程序源代码。`gawk` 读取程序文本时，就好像所有 `program-file` 和命令行源文本都已连接在一起。

此外，以 `@include` 开头的行可用于将其他源文件包含到程序中。这等效于使用 `--include` 选项。以 `@nsinclude` 开头的行也会包含文件，但有两个区别。首先，被包含文件中的命名空间*不会*重置为默认的 `awk`，并且此类文件可以被多次包含。

以 `@load` 开头的行可用于将扩展函数加载到程序中。这等效于使用 `--load` 选项。

环境变量 `AWKPATH` 指定在使用 `-f` 和 `--include` 选项查找源文件时使用的搜索路径。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/AWKPATH-Variable>。

环境变量 `AWKLIBPATH` 指定在使用 `--load` 选项查找源文件时使用的搜索路径。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/AWKLIBPATH-Variable>。

`gawk` 按如下方式执行 AWK 程序：首先，执行通过 `-v` 选项指定的所有变量赋值。接下来，`gawk` 将程序编译为内部形式。然后，`gawk` 执行 `BEGIN` 规则（如果有）中的代码，接着读取 `ARGV` 数组中命名的每个文件（直到 `ARGV[ARGC-1]`）。如果命令行上没有指定文件，`gawk` 读取标准输入。

命令行上形式为 `var=val` 的文件名被视为变量赋值。变量 `var` 被赋值为 `val`。（这发生在任何 `BEGIN` 规则运行之后。）

如果 `ARGV` 的某个特定元素的值为空（`""`），`gawk` 会跳过它。

对于每个输入文件，如果存在 `BEGINFILE` 规则，`gawk` 在处理文件内容之前执行关联的代码。类似地，`gawk` 在处理文件之后执行与 `ENDFILE` 规则关联的代码。

对于输入中的每条记录，`gawk` 测试它是否匹配 AWK 程序中的任何*模式*。对于记录匹配的每个模式，`gawk` 执行关联的*动作*。模式按照它们在程序中出现的顺序进行测试。

最后，在所有输入耗尽后，`gawk` 执行 `END` 规则（如果有）中的代码。

## 变量、记录和字段

AWK 变量是动态的；它们在首次使用时出现。它们的值是浮点数或字符串，或两者兼有，取决于它们的使用方式。此外，`gawk` 允许变量具有正则表达式类型。AWK 也有一维数组；多维数组可以被模拟。然而，`gawk` 提供真正的数组的数组。程序运行时会设置若干预定义变量；这些变量按需描述并在下面总结。

### 记录

通过给内置变量 `RS` 赋值，您可以控制记录的分隔方式。详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Records>。通常，记录由换行符分隔。

### 字段

读取每条输入记录时，`gawk` 使用 `FS` 变量的值作为字段分隔符，将记录拆分为*字段*。此外，`FIELDWIDTHS` 和 `FPAT` 可用于控制输入字段拆分。详细信息请从以下链接开始阅读：<https://www.gnu.org/software/gawk/manual/html_node/Fields>。

输入记录中的每个字段可以通过其位置引用：`$1`、`$2` 等。`$0` 是整条记录，包括前导和尾随空白。

变量 `NF` 被设置为输入记录中的字段总数。

给现有字段赋值会导致在引用 `$0` 时重建整条记录。类似地，给 `$0` 赋值会导致记录被重新拆分，从而为字段创建新值。

### 逗号分隔值

使用 `-k` 或 `--csv` 选项调用时，`gawk` 的记录确定和字段拆分方式不同：记录由不带引号的换行符终止，字段由逗号分隔。双引号可用于括住包含逗号、换行符或双写双引号的字段。更多详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Comma-Separated-Fields>。

### 内置变量

`gawk` 的内置变量列在下面。此列表有意简洁。详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Built_002din-Variables>。

- `ARGC`  
    命令行参数的数量。

- `ARGIND`  
    当前正在处理的文件在 `ARGV` 中的索引。

- `ARGV`  
    命令行参数数组。该数组的索引从 0 到 `ARGC` - 1。

- `BINMODE`  
    在非 POSIX 系统上，指定所有文件 I/O 使用“二进制”模式。详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/PC-Using>。

- `CONVFMT`  
    数字的转换格式，默认为 `"%.6g"`。

- `ENVIRON`  
    一个数组，包含当前环境的值。

- `ERRNO`  
    如果在为 `getline` 执行重定向、在 `getline` 读取期间或在 `close()` 期间发生系统错误，则为一个描述问题的字符串。

- `FIELDWIDTHS`  
    以空白分隔的字段宽度列表。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Constant-Size>。

- `FILENAME`  
    当前输入文件的名称。如果命令行上没有指定文件，则 `FILENAME` 的值为“-”。然而，在 `BEGIN` 规则内部，`FILENAME` 是未定义的（除非由 `getline` 设置）。

- `FNR`  
    当前输入文件中的输入记录号。

- `FPAT`  
    描述记录中字段内容的正则表达式。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Splitting-By-Content>。

- `FS`  
    输入字段分隔符，默认为空格。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Field-Separators>。

- `FUNCTAB`  
    一个数组，其索引和对应值是程序中所有用户定义函数或扩展函数的名称。

- `IGNORECASE`  
    控制所有正则表达式和字符串操作的大小写敏感性。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Case_002dsensitivity>。

- `LINT`  
    提供从 AWK 程序内部对 `--lint` 选项的动态控制。

- `NF`  
    当前输入记录中的字段数。

- `NR`  
    到目前为止看到的输入记录总数。

- `OFMT`  
    数字的输出格式，默认为 `"%.6g"`。

- `OFS`  
    输出字段分隔符，默认为空格。

- `ORS`  
    输出记录分隔符，默认为换行符。

- `PREC`  
    任意精度浮点数的工作精度，默认为 53。

- `PROCINFO`  
    此数组的元素提供对正在运行的 AWK 程序相关信息的访问。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Auto_002dset>。

- `ROUNDMODE`  
    用于数字任意精度算术的舍入模式，默认为 `"N"`（IEEE-754 roundTiesToEven 模式）。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Setting-the-rounding-mode>。

- `RS`  
    输入记录分隔符，默认为换行符。

- `RT`  
    记录终止符。`gawk` 将 `RT` 设置为与 `RS` 指定的字符或正则表达式匹配的输入文本。

- `RSTART`  
    由 `match()` 匹配的第一个字符的索引；如果没有匹配，则为 0。

- `RLENGTH`  
    由 `match()` 匹配的字符串长度；如果没有匹配，则为 -1。

- `SUBSEP`  
    用于分隔数组元素中多个下标的字符串，默认为 `"\034"`。

- `SYMTAB`  
    一个数组，其索引是程序中当前定义的所有全局变量和数组的名称。

- `TEXTDOMAIN`  
    AWK 程序的文本域；用于查找程序字符串的本地化翻译。

### 数组

数组使用方括号（`[` 和 `]`）之间的表达式进行下标访问。如果表达式是表达式列表（`expr`、`expr` ...），则数组下标是由每个表达式的（字符串）值连接而成的字符串，并以 `SUBSEP` 变量的值分隔。此机制模拟多维数组。例如：

```awk
i = "A"; j = "B"; k = "C"
x[i, j, k] = "hello, world\n"
```

将字符串 `"hello, world\n"` 赋给数组 `x` 中由字符串 `"A\034B\034C"` 索引的元素。AWK 中的所有数组都是关联数组，即按字符串值索引。

特殊运算符 `in` 可用于测试数组是否具有由特定值组成的索引：

```awk
if (val in array)
     print array[val]
```

如果数组有多个下标，请使用 `(i, j) in array`。

`in` 结构也可用于 `for` 循环中，以遍历数组的所有元素。然而，`(i, j) in array` 结构仅在测试中有效，在 `for` 循环中无效。

可以使用 `delete` 语句从数组中删除元素。`delete` 语句也可用于删除数组的全部内容，只需指定数组名而不带下标。

`gawk` 支持真正的多维数组。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Arrays>。

### 命名空间

`gawk` 提供简单的*命名空间*机制，以帮助解决 AWK 中所有变量都是全局变量的问题。更多详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Namespaces>。

### 变量类型与转换

变量和字段可以是（浮点）数字、字符串或两者兼有。它们也可以是正则表达式。变量值的解释方式取决于其上下文。如果在数值表达式中使用，它将被视为数字；如果作为字符串使用，它将被视为字符串。

要强制将变量视为数字，请给它加零；要强制将其视为字符串，请将其与空字符串连接。

未初始化变量的数值为零，字符串值为 `""`（空字符串）。

更多（重要！）细节可在手册中找到。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Typing-and-Comparison>。

### 八进制和十六进制常量

您可以在 AWK 程序源代码中使用 C 风格的八进制和十六进制常量。

### 字符串常量

AWK 中的字符串常量是用双引号括起来的字符序列（如 `"value"`）。在字符串内部，可识别某些*转义序列*，与 C 中相同。详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Escape-Sequences>。

### 正则表达式常量

正则表达式常量是用正斜杠括起来的字符序列（如 `/value/`）。手册中描述的转义序列也可用于常量正则表达式内部。

`gawk` 提供*强类型*正则表达式常量。它们以前导 `@` 符号书写，如下所示：`@/value/`。此类常量可以赋给标量（变量、数组元素）并传递给用户定义函数。以这种方式赋值的变量具有正则表达式类型。

## 模式和动作

AWK 是一种面向行的语言。模式在前，动作在后。动作语句括在 `{` 和 `}` 中。模式可以缺失，动作也可以缺失，但当然不能两者都缺失。如果模式缺失，则动作对每条输入记录执行。缺失动作等效于 `{ print }`，它会打印整条记录。

注释以 `#` 字符开始，并持续到行尾。空行可用于分隔语句。有关语句何时跨行继续的规则，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Statements_002fLines>。

### 模式

AWK 模式可以是以下之一：

```awk
BEGIN
END
BEGINFILE
ENDFILE
/regular expression/
relational expression
pattern && pattern
pattern || pattern
pattern ? pattern : pattern
(pattern)
! pattern
pattern1, pattern2
```

`BEGIN` 和 `END` 是两种特殊模式，不会对输入进行测试。所有 `BEGIN` 模式的动作部分按顺序执行，就像所有语句都写在一个 `BEGIN` 规则中一样。它们在读取任何输入之前执行。类似地，所有 `END` 规则语句在所有输入耗尽时（或执行 `exit` 语句时）执行。`BEGIN` 和 `END` 模式不能与模式表达式中的其他模式组合，也不能有缺失的动作部分。

`BEGINFILE` 和 `ENDFILE` 是附加的特殊模式，其动作分别在读取每个命令行输入文件的第一条记录之前和读取每个文件的最后一条记录之后执行。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/BEGINFILE_002fENDFILE>。

有关模式及其组成元素的更多信息，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Pattern-Overview>。

### 动作

动作语句括在花括号 `{` 和 `}` 中。动作语句由大多数语言中常见的赋值、条件和循环语句组成。可用的运算符、控制语句和输入/输出语句仿照 C 中的相应内容。

### 运算符

AWK 中的运算符按优先级递减顺序如下：

- `(...)`  
    分组。

- `$`  
    字段引用。

- `++ --`  
    自增和自减，包括前缀和后缀。

- `^`  
    指数运算。

- `+ - !`  
    一元加、一元减和逻辑非。

- `* / %`  
    乘法、除法和取模。

- `+ -`  
    加法和减法。

- `space`  
    字符串连接。

- `| |&`  
    用于 `getline`、`print` 和 `printf` 的管道 I/O。

- `< > <= >= == !=`  
    常规关系运算符。

- `~ !~`  
    正则表达式匹配、否定匹配。

- `in`  
    数组成员资格。

- `&&`  
    逻辑 AND。

- `||`  
    逻辑 OR。

- `?:`  
    C 条件表达式，形式为 `expr1 ? expr2 : expr3`。如果 `expr1` 为真，则表达式的值为 `expr2`，否则为 `expr3`。只计算 `expr2` 和 `expr3` 中的一个。

- `= += -= *= /= %= ^=`  
    赋值。支持绝对赋值（`var = value`）和运算符赋值（其他形式）。

### 控制语句

控制语句如下：

```awk
if (condition) statement [ else statement ]
while (condition) statement
do statement while (condition)
for (expr1; expr2; expr3) statement
for (var in array) statement
break
continue
delete array[index]
delete array
exit [ expression ]
{ statements }
switch (expression) {
case value|regex : statement
...
[ default: statement ]
}
```

### I/O 语句

输入/输出语句如下：

- 
    ```awk
    close(file [, how])
    ```
    关闭打开的文件、管道或协进程。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/I_002fO-Functions>。

- 
    ```awk
    getline
    ```
    从下一条输入记录设置 `$0`；设置 `NF`、`NR`、`FNR`、`RT`。

- 
    ```awk
    getline <file
    ```
    从 `file` 的下一条记录设置 `$0`；设置 `NF`、`RT`。

- 
    ```awk
    getline var
    ```
    从下一条输入记录设置 `var`；设置 `NR`、`FNR`、`RT`。

- 
    ```awk
    getline var <file
    ```
    从 `file` 的下一条记录设置 `var`；设置 `RT`。

- 
    ```awk
    command | getline [var]
    ```
    运行 `command`，将输出通过管道送入 `$0` 或 `var`（如上所述），并设置 `RT`。

- 
    ```awk
    command |& getline [var]
    ```
    将 `command` 作为协进程运行，将输出通过管道送入 `$0` 或 `var`（如上所述），并设置 `RT`。（`command` 也可以是套接字。请参见下文“特殊文件名”小节。）

- 
    ```awk
    fflush([file])
    ```
    刷新与打开的输出文件或管道 `file` 关联的任何缓冲区。如果省略 `file` 或它是空字符串，则刷新所有打开的输出文件和管道。

- 
    ```awk
    next
    ```
    停止处理当前输入记录。读取下一条输入记录，并从 AWK 程序中的第一个模式重新开始处理。到达输入数据末尾时，执行任何 `END` 规则。

- 
    ```awk
    nextfile
    ```
    停止处理当前输入文件。下一条读取的输入记录来自下一个输入文件。更新 `FILENAME` 和 `ARGIND`，将 `FNR` 重置为 1，并从 AWK 程序中的第一个模式重新开始处理。到达输入数据末尾时，执行任何 `ENDFILE` 和 `END` 规则。

- 
    ```awk
    print
    ```
    打印当前记录。输出记录以 `ORS` 的值终止。

- 
    ```awk
    print expr-list
    ```
    打印表达式。每个表达式由 `OFS` 的值分隔。输出记录以 `ORS` 的值终止。

- 
    ```awk
    print expr-list >file
    ```
    将表达式打印到 `file`。

- 
    ```awk
    printf fmt, expr-list
    ```
    格式化并打印。

- 
    ```awk
    printf fmt, expr-list >file
    ```
    格式化并打印到 `file`。

- 
    ```awk
    system(cmd-line)
    ```
    执行命令 `cmd-line`，并返回退出状态。更多详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/I_002fO-Functions>。

`print` 和 `printf` 还允许附加的输出重定向：

- 
    ```awk
    print ... >> file
    ```
    将输出追加到 `file`。

- 
    ```awk
    print ... | command
    ```
    写入管道。

- 
    ```awk
    print ... |& command
    ```
    将数据发送到协进程或套接字。（另请参见下文“特殊文件名”小节。）

`getline` 函数成功时返回 1，文件结束时返回 0，出错时返回 -1。出错时，`ERRNO` 描述问题。可能可以重试失败的 I/O；请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Retrying-Input>。

> **注意**：打开双向套接字失败会导致向调用函数返回非致命错误。如果在循环中使用管道、协进程或套接字进行 `getline`，或在 `print` 或 `printf` 中使用它们，则*必须*使用 `close()` 来创建命令或套接字的新实例。当管道、套接字或协进程返回 EOF 时，AWK 不会自动关闭它们。

AWK 版本的 `printf` 语句和 `sprintf()` 函数与 C 中的类似。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Printf>。

### 特殊文件名

当通过 `print` 或 `printf` 将 I/O 重定向到文件，或通过 `getline` 从文件读取时，`gawk` 在内部识别某些特殊文件名。这些文件名允许访问从 `gawk` 的父进程（通常是 shell）继承的打开文件描述符。这些文件名也可在命令行上用于命名数据文件。文件名包括：

- `-`  
    标准输入。

- `/dev/stdin`  
    标准输入。

- `/dev/stdout`  
    标准输出。

- `/dev/stderr`  
    标准错误输出。

- `/dev/fd/n`  
    与打开的文件描述符 `n` 关联的文件。

以下特殊文件名可与 `|&` 协进程运算符一起使用，以创建 TCP/IP 网络连接：

- 
    ```text
    /inet/tcp/lport/rhost/rport
    /inet4/tcp/lport/rhost/rport
    /inet6/tcp/lport/rhost/rport
    ```
    用于在本地端口 `lport` 上连接到远程主机 `rhost` 的远程端口 `rport` 的 TCP/IP 连接。使用端口 `0` 让系统选择端口。使用 `/inet4` 强制 IPv4 连接，使用 `/inet6` 强制 IPv6 连接。普通 `/inet` 使用系统默认值（很可能是 IPv4）。仅可与 `|&` 双向 I/O 运算符一起使用。

### 数值函数

AWK 具有以下内置算术函数：

- 
    ```awk
    atan2(y, x)
    ```
    返回 `y/x` 的反正切值，以弧度为单位。

- 
    ```awk
    cos(expr)
    ```
    返回 `expr` 的余弦值，`expr` 以弧度为单位。

- 
    ```awk
    exp(expr)
    ```
    指数函数。

- 
    ```awk
    int(expr)
    ```
    截断为整数。

- 
    ```awk
    log(expr)
    ```
    自然对数函数。

- 
    ```awk
    rand()
    ```
    返回一个介于零和一之间的随机数 `N`，满足 0 ≤ `N` < 1。

- 
    ```awk
    sin(expr)
    ```
    返回 `expr` 的正弦值，`expr` 以弧度为单位。

- 
    ```awk
    sqrt(expr)
    ```
    返回 `expr` 的平方根。

- 
    ```awk
    srand([expr])
    ```
    使用 `expr` 作为随机数生成器的新种子。如果未提供 `expr`，则使用当前时间。返回随机数生成器的前一个种子。

### 字符串函数

`gawk` 具有以下内置字符串函数；详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/String-Functions>。

- 
    ```awk
    asort(s [, d [, how] ])
    ```
    返回源数组 `s` 中的元素数量。对 `s` 的内容进行排序，将排序值的索引替换为从 1 开始的整数。如果给定目标数组 `d`，将 `s` 复制到 `d`，然后对 `d` 排序，保持 `s` 的索引不变。可选字符串 `how` 控制方向和比较模式。有关 `how` 的有效值，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/String-Functions>。`s` 和 `d` 可以是同一个数组；只有在同时提供第三个参数时才有意义。

- 
    ```awk
    asorti(s [, d [, how] ])
    ```
    返回源数组 `s` 中的元素数量。类似于 `asort()`，但使用数组*索引*进行排序。

- 
    ```awk
    gensub(r, s, h [, t])
    ```
    在目标字符串 `t` 中搜索正则表达式 `r` 的匹配项。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/String-Functions>。

- 
    ```awk
    gsub(r, s [, t])
    ```
    对于字符串 `t` 中与正则表达式 `r` 匹配的每个子字符串，替换为字符串 `s`，并返回替换次数。如果未提供 `t`，则使用 `$0`。替换文本中的 `&` 会被实际匹配的文本替换。使用 `\&` 获得字面量 `&`。

- 
    ```awk
    index(s, t)
    ```
    返回字符串 `t` 在字符串 `s` 中的索引；如果 `t` 不存在，则返回零。

- 
    ```awk
    length([s])
    ```
    返回字符串 `s` 的长度；如果未提供 `s`，则返回 `$0` 的长度。当参数为数组时，`length()` 返回数组中的元素数量。

- 
    ```awk
    match(s, r [, a])
    ```
    返回正则表达式 `r` 在 `s` 中出现的位置；如果 `r` 不存在，则返回零，并设置 `RSTART` 和 `RLENGTH` 的值。

- 
    ```awk
    patsplit(s, a [, r [, seps] ])
    ```
    根据正则表达式 `r` 将字符串 `s` 拆分为数组 `a` 和分隔符数组 `seps`，并返回字段数。拆分行为与使用 `FPAT` 进行字段拆分相同。

- 
    ```awk
    split(s, a [, r [, seps] ])
    ```
    根据正则表达式 `r` 将字符串 `s` 拆分为数组 `a` 和分隔符数组 `seps`，并返回字段数。如果省略 `r`，则改用 `FS`。数组 `a` 和 `seps` 会先被清空。拆分行为与字段拆分相同。

- 
    ```awk
    sprintf(fmt, expr-list)
    ```
    根据 `fmt` 打印 `expr-list`，并返回结果字符串。

- 
    ```awk
    strtonum(str)
    ```
    检查 `str`，并返回其数值。详细信息请参见手册。

- 
    ```awk
    sub(r, s [, t])
    ```
    类似于 `gsub()`，但只替换第一个匹配的子字符串。返回零或一。

- 
    ```awk
    substr(s, i [, n])
    ```
    返回 `s` 中从 `i` 开始的最多 `n` 个字符的子字符串。如果省略 `n`，则使用 `s` 的剩余部分。

- 
    ```awk
    tolower(str)
    ```
    返回字符串 `str` 的副本，其中 `str` 中的所有大写字符已转换为对应的小写字符。非字母字符保持不变。

- 
    ```awk
    toupper(str)
    ```
    返回字符串 `str` 的副本，其中 `str` 中的所有小写字符已转换为对应的大写字符。非字母字符保持不变。

`gawk` 具备多字节感知能力。这意味着 `index()`、`length()`、`substr()` 和 `match()` 都按字符而非字节工作。`toupper()` 和 `tolower()` 具备区域设置感知能力。

### 时间函数

`gawk` 提供以下函数来获取时间戳并格式化它们。详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Time-Functions>。

- 
    ```awk
    mktime(datespec [, utc-flag])
    ```
    将 `datespec` 转换为与 `systime()` 返回形式相同的时间戳，并返回结果。

- 
    ```awk
    strftime([format [, timestamp[, utc-flag]]])
    ```
    根据 `format` 中的规范格式化 `timestamp`。

- 
    ```awk
    systime()
    ```
    返回当前时间，以自 Epoch（POSIX 系统上为 1970-01-01 00:00:00 UTC）以来的秒数表示。

### 位操作函数

`gawk` 提供以下位操作函数。将负操作数传递给这些函数中的任何一个都会导致致命错误。这些函数是：

- 
    ```awk
    and(v1, v2 [, ...])
    ```
    返回参数列表中提供的值的按位 AND。至少必须有两个值。

- 
    ```awk
    compl(val)
    ```
    返回 `val` 的按位补码。

- 
    ```awk
    lshift(val, count)
    ```
    返回 `val` 左移 `count` 位后的值。

- 
    ```awk
    or(v1, v2 [, ...])
    ```
    返回参数列表中提供的值的按位 OR。至少必须有两个值。

- 
    ```awk
    rshift(val, count)
    ```
    返回 `val` 右移 `count` 位后的值。

- 
    ```awk
    xor(v1, v2 [, ...])
    ```
    返回参数列表中提供的值的按位 XOR。至少必须有两个值。

### 类型函数

以下函数提供有关其参数的类型相关信息。

- 
    ```awk
    isarray(x)
    ```
    如果 `x` 是数组，则返回真，否则返回假。

- 
    ```awk
    typeof(x)
    ```
    返回一个指示 `x` 类型的字符串。该字符串将是 `"array"`、`"number"`、`"number|bool"`、`"regexp"`、`"string"`、`"strnum"`、`"unassigned"` 或 `"untyped"` 之一。

### 国际化函数

以下函数可在 AWK 程序内部用于在运行时翻译字符串。完整详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/I18N-Functions>。

- 
    ```awk
    bindtextdomain(directory [, domain])
    ```
    指定 `gawk` 查找 `.gmo` 文件的目录，以防这些文件不会或无法放在“标准”位置。它返回 `domain` 被“绑定”到的目录。

- 
    ```awk
    dcgettext(string [, domain [, category]])
    ```
    返回 `string` 在文本域 `domain` 中针对区域设置类别 `category` 的翻译。

- 
    ```awk
    dcngettext(string1, string2, number [, domain [, category]])
    ```
    返回 `string1` 和 `string2` 在文本域 `domain` 中针对区域设置类别 `category` 的翻译中用于 `number` 的复数形式。

### 布尔值函数

您可以创建特殊的布尔类型值；有关它们如何工作以及为何存在，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Boolean-Functions>。

- 
    ```awk
    mkbool(expression)
    ```
    根据 `expression` 的布尔值，返回真值或假值。真值的数值为一。假值的数值为零。

## 用户自定义函数

AWK 中的函数定义如下：

```awk
function name(parameter list) { statements }
```

函数在从模式或动作中的表达式内部被调用时执行。函数调用中提供的实际参数用于实例化函数中声明的形式参数。数组按引用传递，其他变量按值传递。局部变量在参数列表中声明为额外参数。函数可以被间接调用；详细信息请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Indirect-Calls>。

函数调用中的左括号必须紧跟在函数名之后，中间不能有任何空白。

使用 `return expr` 从函数返回值。如果未提供值，或函数通过“自然结束”返回，则返回值未定义。

## 动态加载新函数

您可以使用 `@load` 语句将用 C 或 C++ 编写的新函数动态添加到正在运行的 `gawk` 解释器中。完整细节超出本手册页的范围；请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Dynamic-Extensions>。

## 信号

`gawk` 性能分析器接受两个信号。`SIGUSR1` 使其将性能分析文件和函数调用栈转储到性能分析文件，该文件是 `awkprof.out`，或使用 `--profile` 选项指定的任何文件。然后它继续运行。`SIGHUP` 使 `gawk` 转储性能分析文件和函数调用栈，然后退出。

## 国际化

字符串常量是用双引号括起来的字符序列。在非英语环境中，可以将 AWK 程序中的字符串标记为需要翻译为本地自然语言。此类字符串在 AWK 程序中使用前导下划线（`_`）标记。有关生成和运行可本地化 AWK 程序所涉及的步骤，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Internationalization>。

## GNU 扩展

`gawk` 对 POSIX `awk` 有大量扩展。它们在以下链接中描述：<https://www.gnu.org/software/gawk/manual/html_node/POSIX_002fGNU>。通过使用 `--traditional` 或 `--posix` 选项调用 `gawk`，可以禁用所有扩展。

## 环境变量

`AWKPATH` 提供一个目录列表，`gawk` 在查找通过 `-f`、`--file`、`-i` 和 `--include` 选项以及 `@include` 和 `@nsinclude` 指令命名的文件时会搜索这些目录。如果初始搜索失败，则在给文件名追加 `.awk` 后再次搜索路径。

`AWKLIBPATH` 提供一个目录列表，`gawk` 在查找通过 `-l` 和 `--load` 选项以及 `@load` 指令命名的文件时会搜索这些目录。

`GAWK_PERSIST_FILE`（如果存在）指定一个文件，用作持久内存的后备存储。请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Persistent-Memory>。

`GAWK_READ_TIMEOUT` 指定从终端、管道或双向通信（包括套接字）读取输入的超时时间，以毫秒为单位。

对于通过套接字连接到远程主机，`GAWK_SOCK_RETRIES` 控制重试次数，`GAWK_MSEC_SLEEP` 控制重试之间的间隔。该间隔以毫秒为单位。在不支持 `[usleep(3)]` 的系统上，该值会向上舍入为整数秒。

如果环境中存在 `POSIXLY_CORRECT`，`gawk` 的行为与在命令行上指定了 `--posix` 完全相同。使用 `--lint` 时，`gawk` 会就此发出警告消息。

## 退出状态

如果 `exit` 语句带有值，则 `gawk` 以提供给它的数值退出。否则，如果执行期间没有问题，`gawk` 以 C 常量 `EXIT_SUCCESS` 的值退出。该值通常为零。

如果发生错误，`gawk` 以 C 常量 `EXIT_FAILURE` 的值退出。该值通常为一。如果 `gawk` 因致命错误退出，则退出状态为 2。在非 POSIX 系统上，此值可能映射为 `EXIT_FAILURE`。

## 版本信息

本手册页记录的是 `gawk` 版本 5.4。

## 作者

UNIX `awk` 的原始版本由 Bell 实验室的 Alfred Aho、Peter Weinberger 和 Brian Kernighan 设计并实现。Ozan Yigit 是当前维护者。Brian Kernighan 偶尔参与其开发。

Free Software Foundation 的 Paul Rubin 和 Jay Fenlason 编写了 `gawk`，以兼容第七版 UNIX 中分发的原始版本 `awk`。John Woods 贡献了许多缺陷修复。David Trueman 在 Arnold Robbins 的贡献下，使 `gawk` 兼容新版本的 UNIX `awk`。Arnold Robbins 是当前维护者。

有关 `gawk` 及其文档贡献者的完整列表，请参见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Contributors>。

有关维护者以及当前支持哪些移植版本的最新信息，请参见 `gawk` 发行版中的 `README` 文件。

## 缺陷报告和问题

如果您发现 `gawk` 中的缺陷，请使用 `gawkbug(1)` 程序报告。

报告缺陷的完整说明见以下链接：<https://www.gnu.org/software/gawk/manual/html_node/Bugs>。*请*仔细阅读并遵循其中给出的说明。这将使所有相关人员的缺陷报告和解决过程更加容易。真的。

另一方面，如果您有关于如何使用 `awk` 或 `gawk` 完成特定任务的问题，请将求助请求发送电子邮件至 `help-gawk@gnu.org`。

## 缺陷

鉴于命令行变量赋值功能，`-F` 选项并非必需；它仅为向后兼容而保留。

本手册页太长；`gawk` 功能太多。

## 另请参见

`egrep(1)`、`[sed(1)]`、`gawkbug(1)`、`[printf(3)]` 和 `[strftime(3)]`。

*The AWK Programming Language*，第二版，Alfred V. Aho、Brian W. Kernighan、Peter J. Weinberger，Addison-Wesley，2023 年。ISBN 9-780138-269722。

*GAWK: Effective AWK Programming*，5.4 版，随 `gawk` 源代码提供。本文档的当前版本可在以下链接在线获取：<https://www.gnu.org/software/gawk/manual>。

GNU `gettext` 文档，可在以下链接在线获取：<https://www.gnu.org/software/gettext>。

## 示例

打印并排序所有用户的登录名：

```awk
BEGIN     { FS = ":" }
     { print $1 | "sort" }
```

统计文件中的行数：

```awk
     { nlines++ }
END  { print nlines }
```

在每一行前加上其在文件中的行号：

```awk
{ print FNR, $0 }
```

连接并加行号（同一主题的变体）：

```awk
{ print NR, $0 }
```

对特定数据行运行外部命令：

```sh
tail -f access_log |
awk '/myhome.html/ { system("nmap " $1 ">> logdir/myhome.html") }'
```

## 复制许可

Copyright © 1989, 1991–1999, 2001–2005, 2007, 2009–2026, Free Software Foundation, Inc.

允许制作和分发本手册页的逐字副本，前提是所有副本上保留版权声明和本许可声明。

允许在逐字复制的条件下复制和分发本手册页的修改版本，前提是产生的全部衍生作品按照与本许可声明相同的许可声明条款分发。

允许在其他语言的上述修改版本条件下复制和分发本手册页的翻译版本，但本许可声明可以在经基金会批准的翻译中陈述。

## 版权页

本页是 `gawk`（GNU awk）项目的一部分。项目信息可在 <http://www.gnu.org/software/gawk/> 找到。如果您对本手册页有缺陷报告，请参见 <http://pkg-shadow.alioth.debian.org/getinvolved.php>。本页于 2026-08-03 从项目的上游 Git 仓库 <git://git.savannah.gnu.org/gawk.git> 获取。（当时，在仓库中找到的最近提交日期为 2026-08-01。）如果您发现本页的 HTML 版本存在渲染问题，或认为有更好或更及时的页面来源，或对 COLOPHON 中的信息（该部分*不是*原始手册页的一部分）有更正或改进，请发送邮件至 `man-pages@man7.org`。

Free Software Foundation       June 25 2026                       *GAWK*(1)