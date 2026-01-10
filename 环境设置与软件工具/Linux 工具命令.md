## 功能



### docker

`docker run -d -p 127.0.0.1:3000:3000 getting-started`
[文档](https://docs.docker.com/get-started/workshop/02_our_app/)

- `docker run`
	运行容器，并指定镜像的名称
- `-p HOST:CONTAINER`
	用于在主机和容器之间创建端口映射，其中 HOST 是主机上的地址， CONTAINER 是容器上的端口

- `-ps`
	显示正在运行的容器。要查看所有容器，使用 --all （或 -a ）标志
- `docker exec [OPTIONS] CONTAINER COMMAND [ARG...]` 
	运行中的容器中执行新命令，[文档](https://docs.docker.com/reference/cli/docker/container/exec/)
	- `-i, --interactive`
		即使未附加也保持 STDIN 打开
	- `-t, --tty`		
		分配伪终端
	- `-u, --user`
		Username or UID，使用 `-u root` 或 `-u 0`以root权限进入
	
	例，`docker exec -u root -it 容器名或ID /bin/bash`


### man

man 是系统的手册分页程序。

手册页操作：
您可以使用方向键（以及 PgUp/PgDn 键）滚动手册页，并使用 `/` 进行搜索。
搜索后，可按 `n` 键跳至下一个结果，按 `N` 键跳至上一个结果。
除了 `/`，您还可以使用 `?` 进行反向搜索！

参数：
- `-k, --apropos [关键词]`  
	大约等同于 apropos。搜索关键词对应的手册概述并显示所有匹配结果。

### env

```sh
env [选项]... [-] [NAME=VALUE]... [命令 [参数]...]
```
在环境中将每个 NAME 设置为 VALUE，并运行 COMMAND。
单独使用等同于 `-i`。如果没有 COMMAND，则打印结果环境。

参数：
- `-i, --ignore-environment`  
	以空环境开始

### 文件与内容，字符串处理

#### head

```head [参数] [文件]```

默认查看文件前十行

参数
- ```n行数``` 或 ```n 行数```  
	显示设置的行数

#### cut

```sh
cut OPTION... [FILE]...
```

从每个 FILE 中打印选定行的一部分到标准输出。

参数：
- `-d, --delimiter=分隔符`
	指定分隔符代替 TAB 作为字段分隔符
- `-f, --fields=LIST`
	指定*字段*编号；如果未指定-s 选项，也会打印包含无分隔符字符的任何行


#### echo


参数
- `-n` 不输出尾随的换行符
- `-e` 启用反斜杠转义的解释

#### tr

```sh
tr [选项]... 集合 1 [集合 2]
```

从标准输入修改字符，并写入标准输出。

选项：
- `-d, --delete`
	删除 SET1 中的字符，不进行翻译

SETs 是用字符字符串指定的。大多数字符表示它们自己。解释序列有：
- `CHAR1-CHAR2`
	从 CHAR1 到 CHAR2 的所有字符按升序排列

- `[:lower:]`
    all lower case letters

- `[:upper:]`
   all upper case letters

例：
- 字符串大写转小写
	`tr [:upper:] [:lower:]`

#### grep

[手册](https://www.man7.org/linux/man-pages/man1/grep.1.html)

```sh
grep [OPTION]... PATTERNS [FILE]...
grep [OPTION]... -e PATTERNS ... [FILE]...
grep [OPTION]... -f PATTERN_FILE ... [FILE]...
```

`grep` 在每个`FILE`中搜索模式。  
在第一个形式中（如果没有 -e 或 -f 选项），第一个操作数模式是由换行符分隔的一个或多个模式，grep 会打印出与模式匹配的每一行。

参数
- `-r, --recursive`  
	递归搜索目录
- `-E, --extended-regexp` 
	将模式解释为扩展正则表达式。
- `-P, --perl-regexp`
	将模式解释为 perl 正则表达式。
	- `(?<=foo)`
		匹配 foo 但不包含在结果中
- `-o, --only-matching`
	仅打印匹配（非空）的行部分，每个这样的部分单独输出在一行上。

匹配控制：
- `-v, --invert-match`  
	反转匹配的意义，选择不匹配的行。(-v 由 POSIX 指定。)

上下文行控制：
- `-A NUM, --after-context=NUM`
    在匹配行后打印 NUM 行的后续上下文。

- `-B NUM, --before-context=NUM`
    在匹配行前打印 NUM 行的前导上下文。

- `-C NUM, -NUM, --context=NUM`
    打印 NUM 行的输出上下文。

#### diff

```sh
diff [OPTION]... FILES
```

逐行比较文件。

输出示例：
- `2a3` 在第一个文件的第2行后追加第二个文件的第3行
- `5c5` 第一个文件的第5行被替换为第二个文件的第5行

#### ls

`ls [OPTION]... [FILE]...`

列出参数所指定目录中的文件，若未提供参数则默认列出当前目录内容。

参数：
- `-a, --all`  
	不忽略以 . 开头的条目。
- `-l`  
	使用长列表格式
- `-R, --recursive`  
	递归列出子目录

#### touch

`touch [OPTION]... FILE...`

更新每个文件的访问和修改时间为当前时间。
如果不存在，一个不存在的文件参数会被创建为空文件，除非提供 -c 或 -h 选项。

#### mv

```sh
mv [OPTION]... [-T] SOURCE DEST
mv [OPTION]... SOURCE... DIRECTORY
mv [OPTION]... -t DIRECTORY SOURCE...
```

将 SOURCE 重命名为 DEST，或将 SOURCE(s) 移动到 DIRECTORY。

#### cp

```sh
cp [OPTION]... [-T] SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
cp [OPTION]... -t DIRECTORY SOURCE...
```

将 SOURCE 复制到 DEST，或将 SOURCE(s) 复制到 DIRECTORY。

#### namei

``` namei [options] pathname...```

递归列出目录中文件信息

#### mkdir

```sh
mkdir [OPTION]... DIRECTORY...
```

创建目录（如果它们尚不存在）。

#### find

`find [path...] [expression]`

如果未指定搜索条件，`find` 将匹配所有文件。  
如果未指定搜索位置，`find` 将使用当前工作目录（`.`）。  

参数：
- `-name pattern`  
	基础文件名匹配 pattern
- `type [类型]`  
	d 目录  
	f 普通文件  
	l 符号链接  
	p 命名管道  
	s 套接字  

#### ln

```sh
ln [选项]... [-T] 目标 链接名
ln [选项]... 目标
ln [选项]... 目标... 目录
ln [选项]... -t 目录 目标...
```

在第一种格式中，创建具有指定链接名且指向指定目标的链接。在第二种格式中，在当前目录创建指向目标位置的链接。在第三、四种格式中，在指定目录中创建指向指定目标的链接。默认创建硬链接，当使用 --symbolic 时创建符号链接。

参数：
- `-s, --symbolic`  
	创建符号链接而非硬链接

#### 文件名通配符

- `*` 多字符通配符，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `?` 单字符通配符，，可以匹配文件名中除 `/` 或开头的 `.` 字符之外的任何部分。
- `[]` 单字符限定匹配，匹配括号内指定的可能字符子集的通配符。
- `[!]`、`[^]` 排除符，如果方括号内的第一个字符是 `!` 或（在较新版本的 bash 中）`^`，该通配符模式将进行反向匹配，即该方括号实例会匹配*不*在所列出的字符范围内的字符。  
	当 `!` 字符不是 `[]` 通配符的首字符时，它在 bash 中具有不同的特殊含义！`^` 没有这个问题，但在较旧的 shell 中可能不兼容。

#### 操作符

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

进程替换：
- `命令B <(命令A)`  
	将命令A的输出连接到命令B的*参数*，即命令A的输出作为命令B的参数  
	当写入 `<(command)` 时，bash 将运行该命令并将其输出连接到一个它将创建的临时文件，它被称为*命名管道*
- `命令B >(命令A)`
	将命令B的输出连接到命令A的标准输入  
	当写入一个 `>(command)` 参数，bash 将运行 `command` 命令，但将其输入连接到一个临时命名管道文件。当命令B写入此文件时，数据会传送到命令A的标准输入

示例：
- `2>/dev/null`  
	丢弃错误信息


#### tee

`tee [选项]... [文件列表]...`

把标准输入的数据复制到文件列表中的每一个文件，同时送往标准输出。

参数：
- `-a, --append`  
	追加到给出的文件，而不是覆盖

#### mkfifo 

```bash
mkfifo [选项]... 名称...
```

使用指定的名称创建持久化命名管道（FIFO）。  
阻塞，读取前需写入，并且写入后阻塞到被读取为止。  
想象容量为1的栈，入栈后需出栈。

#### sort

```sh
sort [OPTION]... [FILE]...
sort [OPTION]... --files0-from=F
```

将所有 FILE(s) 的排序后连接结果写入标准输出。

参数：
- `-r`：反向排序（从Z到A）  
- `-n`：数值排序（针对数字）  
- `-u`：仅保留唯一行（*删除重复项*）  
- `-R`：随机顺序！

#### sed

```sh
sed [OPTION]... {script-only-if-no-other-script} [input-file]...
```
Sed 是一个流编辑器。流编辑器用于对输入流（文件或来自管道的输入）执行基本的文本转换。

- `s/regexp/replacement/`  
	尝试将 regexp 的匹配项替换为 replacement。

### 进程

#### ps

```sh
ps [选项]
```

`ps` 显示关于部分活动进程的信息

- `-o` 选项启用自定义 `stat` 列
	- `T`  表示进程因 `Ctrl-Z` 操作而被挂起
	- `S` 表示其正在等待输入时处于睡眠状态
	- `R` 表示该进程正在活跃运行
	- `+` 号代表其处于前台

**“标准”语法：**  
此语法中，`-e` 用于列出“所有”进程，`-f` 用于显示“完整格式”输出（包括参数）。二者可合并为单一参数 `-ef`。


**“BSD”语法：**  
此语法中，`a` 用于列出所有用户的进程，`x` 用于显示非终端运行的进程，`u` 用于“用户易读”格式输出。三者可合并为单一参数 `aux`。

`ps -ef` 额外输出*父进程 ID*（`ppid`），即启动该进程的父进程 pid；而 `ps aux` 则输出进程占用的系统总 CPU 和内存百分比。

`ps -ef` 和 `ps aux` 默认会根据终端宽度截断命令列表， 传递两次 `w` 参数（如 `ps -efww` 或 `ps auxww`）来禁用截断。

#### kill

```sh
kill [-s 信号|-p] [--] 进程 ID...
kill -l [信号]
```

命令 kill 向指定的进程或进程组发送指定的信号。如果没有指定信号，将发送 TERM 信号。TERM 信号会杀死那些不捕获此信号的进程。对于其他进程，可能需要使用 KILL（9）信号，因为该信号无法被捕获。

#### 终端快捷键与命令

`Ctrl-C`（即按住 `Ctrl` 键的同时按下 `C`）会向正在等待终端输入的应用发送"*中断*"信号，通常这将促使应用程序正常退出。

`Ctrl-Z` 将进程*挂起*至后台。

`fg` 命令——这是一个*内置命令*，它会获取被挂起的进程，将其恢复并放回你终端的*前台*。
`bg` 命令在*后台*恢复进程。

在命令末尾追加 `&` 符号可直接启动即进入*后台*运行！

使用特殊的 `?` 变量获取最近终止命令的退出码（注意读取值时需前缀 `$` 符号）

### 权限

```sh
-rw-r--r-- 1 hacker hacker    0 May 22 13:42 college_file
drwxr-xr-x 2 hacker hacker 4096 May 22 13:42 pwn_directory
```

第一个字符是文件类型。
接下来的九个字符是文件或目录的实际访问权限，分为三组：
1. 前三个字符表示所有者的权限
2. 中间三个字符表示所属组的权限
3. 最后三个字符表示所有其他访问（例如其他用户和其他组）对文件的权限

有两列显示拥有文件的*用户*（本例中为用户 `hacker`）和拥有文件的*组*（本例中同样为组 `hacker`）。

内核在检查权限时，只会使用“最具体”那一组位。
具体规则（从高到低优先级）：

1. 如果你是这个文件的所有者 → 只看 `u`（user） 那三位
2. 否则，如果你属于这个文件的组 → 只看 `g`（group） 那三位
3. 否则 → 只看 `o`（other） 那三位

SUID:

```sh
-rwsr-xr-x 1 root root 232416 Dec 1 11:45 /usr/bin/sudo
```

原本是可执行位`x`的位置出现的 `s` 表示该程序是*带有 SUID* 可执行的。
这意味着，无论哪个用户运行该程序（只要他们有执行权限），该程序都将以其所有者用户（在本例中为 `root` 用户）的身份执行。
作为文件的所有者，您可以使用 chmod 设置文件的 SUID 位

#### su

```sh
su [OPTION]... [-] [USER [ARG]...]
```

切换至目标 USER  
单独使用 `-` 表示 `-l`。
如果未给出 USER，则假设为 root。

`su` 是一个 setuid 二进制文件：

```sh
ls -l /usr/bin/su
-rwsr-xr-x 1 root root 232416 Dec 1 11:45 /usr/bin/su
```

由于设置了 SUID 位，`su` 会以 `root` 身份运行。以 `root` 身份运行时，它可以启动一个 `root` shell！当然，`su` 具有辨别能力：在允许用户将权限提升至 `root` 之前，它会验证用户是否知道 `root` 密码

#### sudo

`sudo` 默认以 `root` 身份运行命令.  
`sudo` 通过检查策略来确定用户是否被授权以 `root` 身份运行命令。这些策略在 `/etc/sudoers` 文件中定义

#### id

```sh
id [选项]... [用户名]
```

打印指定用户名的用户和组信息，或者（当省略用户名时）为当前用户打印。

#### chown

```sh
chown [选项]... [所有者][:[组]] 文件...
chown [选项]... --reference=RFILE 文件...
```

chown (**ch**ange **own**er，更改所有者) 更改每个给定文件的用户和/或组所有权:

- 如果只给出一个所有者（用户名或数字用户 ID），则该用户将成为每个给定文件的所有者，并且文件组不会改变。
- 如果所有者后面跟着一个冒号和一个组名（或数字组 ID），并且它们之间没有空格，则文件的组所有权也会改变。
- 如果用户名后面跟着一个冒号但没有组名，则该用户将成为文件的所有者，并且文件的组将更改为该用户的登录组。
- 如果给出了冒号和组，但省略了所有者，则只更改文件的组；在这种情况下，`chown` 执行与 `chgrp` 相同的功能。
- 如果只给出一个冒号，或者整个操作符为空，则既不改变所有者也不改变组。

通常，`chown` 只能由 `root` 用户调用。

#### chgrp

```sh
chgrp [OPTION]... GROUP FILE...
chgrp [OPTION]... --reference=RFILE FILE...
```

将每个文件的组改为 GROUP。使用--reference 选项时，将每个文件的组改为 RFILE 的组。

除非您是文件的所有者*并且*是新组的成员，否则这通常需要 `root` 访问权限

#### chmod

```sh
chmod [OPTION]... MODE[,MODE]... FILE...
chmod [OPTION]... OCTAL-MODE FILE...
chmod [OPTION]... --reference=RFILE FILE...
```

`chmod`根据mode修改每个给定文件的文件模式位，mode可以是表示要进行的更改的符号表示，也可以是表示新模式位的位模式的八进制数。
符号模式的格式为`[ugoa...][[+-=][perms...]...]`，其中perms是集合`rwxXst`中的零个或多个字母，或者是集合`ugo`中的一个字母。可以给出多个符号模式，用逗号分隔。
字母组合`ugoa`控制将更改哪个用户的文件访问权限：文件的所有者（`u`）、文件组中的其他用户（`g`）、文件组外的其他用户（`o`）或所有用户（`a`）。如果没有给出这些，效果就像给出了`a`一样，但umask中设置的位不会受到影响。

运算符：
- `+` 将选定的文件模式位添加到每个文件的现有文件模式位
- `-` 将它们移除
- `=` 将它们覆盖添加
	- `=-`  在覆盖运算符右侧使用 `-` 清除权限

通常，您需要是文件的所有者才能更改其权限。

注，使用使用 `,` 将多个模式链接到 `chmod` 命令，以同时修改多个模式。

#### which

```sh
which [options] [--] programname [...]   
```

which 接受一个或多个参数。对于它的每个参数，它会向标准输出打印出当这个参数在 shell 提示符下输入时将会被执行的可执行文件的完整路径。它通过在环境变量 PATH 列出的目录中搜索可执行文件或脚本

## 命令链

- `;`  
	命令链式组合的最简单方式是使用 `;`。在大多数上下文中，`;` 分隔命令的方式类似于用 Enter 键分隔行。

- `&&`  
	`&&` 运算符允许您仅在第一个命令成功时（遵循Linux惯例，即退出码为0）才运行第二个命令。这被称为"AND"运算符，因为需要同时满足两个条件：第一个命令必须成功*且*第二个命令才会运行。这对于需要特定操作依赖于其他操作成功执行的复杂命令行工作流非常有用。

- `||`  
	`||`运算符允许您在第一个命令失败（以非零代码退出）时才运行第二个命令。这被称为*OR*运算符，因为要么第一个命令成功*要么*第二个命令将运行。`||`运算符对于提供回退命令或错误处理非常有用！

- `bash [options] [file]`  
	Bash 是一个兼容 sh 的命令语言解释器，它执行从标准输入或文件中读取的命令。


## 文件

### /etc/pwd

Linux 系统上的完整用户列表定义在 `/etc/pwd` 文件中

```sh
root:x:0:0:root:/root:/bin/bash
hacker:x:1000:1000::/home/hacker:/bin/bash
```

每行内容按 `:` 分隔，依次包含：
1. 用户名
2. 密码*曾经*存储位置的占位符 `x`
3. 数字用户 ID
4. 数字默认组 ID
5. 用户详细信息
6. 主目录
7. 默认 shell

### /etc/shadow

由于 `/etc/passwd` 是全局可读文件，不利于密码安全，因此密码数据被移至 `/etc/shadow`

```sh
root:$6$s74oZg/4.RnUvwo2$hRmCHZ9rxX56BbjnXcxa0MdOsW2moiW8qcAl/Aoc7NEuXl2DmJXPi3gLp7hmyloQvRhjXJ.wjqJ7PprVKLDtg/:19921:0:99999:7:::
hacker::19916:0:99999:7:::
zardus:$6$bEFkpM0w/6J0n979$47ksu/JE5QK6hSeB7mmuvJyY05wVypMhMMnEPTIddNUb5R9KXgNTYRTm75VOu1oRLGLbAql3ylkVa5ExuPov1.:19921:0:99999:7:::
```

每行内容按 `:` 分隔：
1. 用户名
2. 密码。字段值为 `*` 或 `!` 实际表示该账户的密码登录功能已被禁用；空白字段表示未设置密码（某些配置下可能允许无密码 `su`，这是较常见的错误配置）；而长字符串是密码经过单向加密（哈希）后的结果。

### `#!`

```bash
#!/bin/bash

echo "Hello Hackers!"
```

程序有多种类型，但如果程序文件以字符`#!`开头（通常称为"[Shebang](https://en.wikipedia.org/wiki/Shebang_(Unix))"），Linux会将文件视为*解释型程序*，并将该行剩余内容视为*解释器*的路径。然后，内核会调用该解释器，并将程序文件的路径作为其唯一参数。

请注意，Shebang行必须位于文件的*第一行*——其前面不能有空行或空格！

常见Shebang：
- `#!/bin/bash` 用于bash脚本
- `#!/usr/bin/python3` 用于Python脚本
- `#!/bin/sh` 用于POSIX shell脚本——这是`bash`的一个功能较少但更兼容非Linux系统的原始前身！

## 工具

#### curl

```curl [options / URLs]```

[手册](https://curl.se/docs/manpage.html)

参数
- ```-d, --data <data>```
    (HTTP MQTT) Sends the specified data in a POST request to the HTTP server
- ```-I, --head```
	Fetch the headers only.
- ```-k, --insecure```
	(TLS SFTP SCP) 默认情况下，curl 建立的每个安全连接在传输之前都会验证其安全性。这个选项使 curl 跳过验证步骤，在不检查的情况下继续进行。
- ```-L, --location```
	(HTTP) 如果服务器报告请求的页面已移动到不同位置（通过 Location: 标头和 3XX 响应代码指示），此选项会使 curl 重新向新位置发起请求。如果与 --show-headers 或 --head 一起使用，则会显示所有请求页面的标头。
- ```-O，--remote-name``` 
	下载的文件名使用原文件名
- ```-s, --silent``` 
	静默下载
- ```-S, --show-error``` 
	失败时显示错误信息
- ```-x, --proxy [protocol://]host[:port]``` 
	Use the specified proxy.
- ```-X, --request <method>``` 
	Change the method to use when starting the transfer.

#### wget

``` wget [option]... [URL]...```

参数
- ```--no-verbose``` 关闭详细输出

#### Nmap

```nmap [Scan Type(s)] [Options] {target specification}```

[文档](https://nmap.org/book/man.html)

参数
- ```-Pn``` 将所有主机视为在线，跳过主机发现
- ```-sS/sT/sA/sW/sM``` 分别对应TCP SYN/Connect()/ACK/Window/Maimon scans
- ```-p<port ranges>``` 指定扫描的端口，如```-p22```,```-p0-65535```
- ```-sV``` 探测开放端口以识别服务/版本信息

#### Ncat

[手册](https://nmap.org/book/ncat-man.html)
参数：
- `-l, --listen`  
	绑定并监听传入连接

#### host

```host [-aCdilrTvVw] [-c class] [-N ndots] [-t type] [-W time] [-R number] [-m flag] [-p port] hostname [server]```

参数
- `-t <type>` 指定查询类型，如 `ns`为名字服务器
    - `host -t PTR <反向IP>.in-addr.arpa` 反向查询
        将IP地址转换为反向格式（如 192.168.1.100 → 100.1.168.192.in-addr.arpa）
- `-l <域名> [权威 DNS 服务器地址]` 使用 AXFR（区域传输）协议，列出一个域的所有主机记录
- `<server>` 指定本次查询的 DNS 服务器

#### nc

```nc [-46CDdFhklNnrStUuvZz] [-I length] [-i interval] [-M ttl]
	  [-m minttl] [-O length] [-P proxy_username] [-p source_port]
	  [-q seconds] [-s sourceaddr] [-T keyword] [-V rtable] [-W recvlimit]
	  [-w timeout] [-X proxy_protocol] [-x proxy_address[:port]]
	  [destination] [port]
```



#### dig

域名信息收集器（domain information groper）

参数
- `+short` 简洁信息

#### whois

查询对象的 whois 数据库



#### openssl

- `s_client`
	通用 SSL/TLS 客户端

##### openssl enc

`openssl enc|cipher [-cipher] [-help] [-list] [-ciphers] [-in filename] [-out filename] [-pass arg] [-e] [-d] [-a] [-base64] [-A] [-k password] [-kfile filename] [-K key] [-iv IV] [-S salt] [-salt] [-nosalt] [-z] [-md digest] [-iter count] [-pbkdf2] [-saltlen size] [-p] [-P] [-bufsize number] [-nopad] [-v] [-debug] [-none] [-skeymgmt skeymgmt] [-skeyopt opt:value] [-skeyuri uri] [-storepass arg] [-rand files] [-writerand file] [-provider name] [-provider-path path] [-provparam [name:]key=value] [-propquery propq]`

[文档](https://docs.openssl.org/master/man1/openssl-enc/)

- `-a` 或 `-base64`
	编码解码时处理换行符
- `-A`
	不处理换行符
- `-d`
	解密数据
- `-kfile filename`
	从指定文件读取密码
- `-加密算法-密钥长度-工作模式`
	- 例：`-aes-256-cbc`
		aes算法 256位密钥 密码块链接模式（cbc）

##### openssl x509

- `-noout`
	禁止其他输出

- `-pubkey`
	以PEM格式打印证书公钥

##### openssl rsa

`openssl rsa [-help] [-inform DER|PEM|P12|ENGINE] [-outform DER|PEM] [-in filename|uri] [-passin arg] [-out filename] [-passout arg] [-aes128] [-aes192] [-aes256] [-aria128] [-aria192] [-aria256] [-camellia128] [-camellia192] [-camellia256] [-des] [-des3] [-idea] [-text] [-noout] [-modulus] [-traditional] [-check] [-pubin] [-pubout] [-RSAPublicKey_in] [-RSAPublicKey_out] [-pvk-strong] [-pvk-weak] [-pvk-none] [-engine id] [-provider name] [-provider-path path] [-propquery propq]`

- `-in filename|uri` 
	指定了从何处读取密钥，如果未指定此选项，则使用标准输入。如果密钥是加密的，将提示输入密码短语。
- `-noout` 
- `-modulus`
	打印出密钥的模值。

##### openssl dgst

`openssl dgst|digest [-digest] [-list] [-help] [-c] [-d] [-debug] [-hex] [-binary] [-xoflen length] [-r] [-out filename] [-sign filename|uri] [-keyform DER|PEM|P12|ENGINE] [-passin arg] [-verify filename] [-prverify filename] [-signature filename] [-sigopt nm:v] [-hmac key] [-mac alg] [-macopt nm:v] [-fips-fingerprint] [-engine id] [-engine_impl id] [-rand files] [-writerand file] [-provider name] [-provider-path path] [-propquery propq] [file ...]`

- `-digest`
	指定要使用的支持的分 digest 的名称。见 `-list` 选项
- `-sign filename|uri`
	使用提供的私钥对摘要进行数字签名。
- `-out filename`
	输出文件名，或默认标准输出。
- `file ...`
	要处理的文件或文件列表。如果没有指定文件，则使用标准输入。



#### hashcat

[文档](https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_do_i_install_hashcat)


#### ssh-keygen

[文档](https://www.ssh.com/academy/ssh/keygen)

参数：
- `-f <filename>`
	选择存储密钥的文件
- `-N "新"` 	
	为密钥提供一个新的密码短语
- `-i "输入"` 	
	访问现有密钥文件

示例：
- `ssh-keygen -f key -N ''`	
	生成一个 以 `key` 为名称的 ssh 密钥，私钥 `key`，公钥 `key.pub`。密码为 `''`
	

#### 其他



- 如果你在 shell 中按 tab 键，它会尝试推断你将要输入的内容并自动补全。  
	默认情况下，`bash` 会在出现多个匹配选项时自动扩展到第一个分歧点（在此例中为 `fl`）。  
	当你*第二次*按下 tab 键时，它会列出这些匹配选项。  

	补全选项根据位置，即上下文不同，对应不同文件:
	- 命令位置：补的是“可执行命令”（过滤掉普通文件）。
	- 参数位置：补的是“文件名/路径”（不过滤普通文件）。

- `Ctrl + D`   
	发送文件结束（EOF）信号

## 参考

### 文档

https://www.gnu.org/software/bash/manual/

https://bash.cyberciti.biz/guide/Main_Page

### 手册

https://man.archlinux.org/

https://linux.die.net/man

### 文章

https://pwn.college/

[Linux Shell 中 I/O 重定向](https://web.archive.org/web/20220629044814/http://bencane.com:80/2012/04/16/unix-shell-the-art-of-io-redirection/)