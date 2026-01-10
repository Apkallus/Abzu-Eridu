bash中无数据类型的概念、无需声明变量。

变量名前加 `$` 符号，触发变量展开来引用变量。
`echo $VAR`

关键字**local**创建局部变量

当 shell 遇到空格时，它会结束变量赋值

默认情况下，在 Shell 会话中设置的变量仅在该 Shell 进程内局部有效。  
使用`export VAR`导出到子进程的环境变量后可被使用。

`env` 命令打印出 Shell 中设置的每一个*导出的*变量

命令替换允许命令的输出替换命令本身，同时删除任何尾随的换行符。标准的命令替换形式是在命令被如下方式括起来时发生：  
`$(command)`  
或（已弃用）  
`command`.  
命令替换 `$(cat file)` 可以被替换为等效但更快的 `$(< file)` 。

`read` 内置命令，从标准输入*读取*到变量中  
- `-p` 参数的示例，该参数允许您指定提示信息  
    `read -p "输入提示" VAR`  

在交互式 bash 中，字符 `!` 会被当成“上一条命令”等历史引用来解析；
- 双引号 `"..."`，里面的 `!` 会被 bash 继续做历史扩展；
- 单引号 `'...'` 包住整体，`!` 就不会被历史扩展；
- 或者将`!`转义

在 Bash 里，单引号 `'` 和 双引号 `"` 的区别：

- 单引号：几乎什么都不展开，按字面原样保留。
    即，不触发 `!` 历史扩展
- 双引号：会做变量、命令替换、历史扩展等部分展开。

## bash 脚本

`bash [options] [file]`
Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。

按照惯例，Shell脚本通常以 `sh` 作为后缀命名
然后通过将其作为参数传递给新的Shell实例（`bash`）来执行！
当以这种方式调用Shell时，它不会从用户处获取命令，而是从文件中读取命令。

```sh
hacker@dojo:~$ bash pwn.sh
```

如果您的Shell脚本文件是*可执行的*（请回顾 linux-文件权限），您可以直接通过其相对路径或绝对路径调用它

```sh
echo 'hack the planet' > solve.sh && chmod u+x solve.sh
```
### 参数

```sh
hacker@dojo:~$ bash myscript.sh hello world
```

脚本可以通过特殊变量访问这些参数：
- `$1` 包含第一个参数（"hello"）
- `$2` 包含第二个参数（"world"）
- `$3` 将包含第三个参数（如果存在）
- ...以此类推

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

### 条件

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
首先，*必须*在`if`后、`[`后以及`]`前保留空格（如果您熟悉C等语言，这点有所不同）；
其次，`if`、`then`和`fi`必须位于不同行（或用分号分隔），不能将它们合并到同一语句中。
另一个特殊之处是：`if`语句的结束标记是`fi`（即*if*的倒写），而非`endif`或`end`等常见形式。

与`if`类似，*必须*在`elif`后使用`then`

`else`没有条件——它会捕获所有之前未匹配的情况。它也不需要`then`语句。最后，`fi`需放置在`else`代码块之后，表示整个复合语句的结束