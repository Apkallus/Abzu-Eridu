# vim - Vi 增强版，程序员文本编辑器

https://vimhelp.org/
- 官网即拥有搜索功能

https://github.com/vim/vim/tree/master/runtime/doc

```sh
vim [options] [file ..]
vim [options] -
vim [options] -t tag
vim [options] -q [errorfile]
```

vim 是一个向上兼容 Vi 的文本编辑器。它可以用来编辑各种纯文本文件。它特别适用于编辑程序。

```console
# 启动 shell
vim -c ':shell'

# 启动绝对路径 shell
vim -c ':!/bin/sh'

# 使用绝对路径设置变量 shell 后，再启动 shell
vim -c ':set shell=/bin/sh|:shell'
```

省略其他命令，见首页 [Interfaces 接口](#接口)。接口需被编译，且环境存在对应版本语言（使用版本信息查看 `--version`）
- `+python` 对应 Python 2.x
- `+python3` 对应 Python 3

```console
vim -c ':python print("Hello")'
vim -c ':lua print("Hello, Vim!")'
```

## 参数

https://vimhelp.org/starting.txt.html

### `+{command}` `-c {command}`

`{command}` 会在第一个文件读入后执行（并且在该文件的自动命令和模式行处理之后）。`command` 被解释为 Ex 命令。如果 `command` 包含空格，必须用双引号括起来（取决于所使用的 shell）。例如：

```sh
vim  "+set si"  main.c
vim  "+find stdio.h"
vim  -c "set ff=dos"  -c wq  mine.mak
```

注意：在一个 Vim 命令中最多可以使用 10 个 `+` 或 `-c` 参数。它们按给定顺序执行。`-S` 参数也算作一个 `-c` 参数。

### `--cmd {command}`

`{command}` 会在处理任何 vimrc 文件之前执行。除此之外，它像 `-c {command}` 一样工作。最多可以使用 10 个此类命令，独立于 `-c` 命令。

## 命令

https://vimhelp.org/various.txt.html

- `:sh[ell]`  
    启动一个 shell。当 shell 退出（执行 `exit` 命令后）时，你会返回 Vim。shell 命令的名称来自 `'shell'` 选项。  

- `:!{cmd}`  
    用 shell 执行 `{cmd}`。另请参见 `'shell'` 和 `'shelltype'` 选项。过滤命令请参见 `:range!`。



## 使用

波浪线（`~`）表示文件中没有的行。换句话说，当 Vim 没有文件内容可显示时，它会显示波浪线。

### 模式

Vim 编辑器是模态编辑器。两个基本模式称为“普通模式”和“插入模式”。 刚启动 Vim，会处于普通模式。

- 普通模式 -> 插入模式  
    输入 `i` 命令（i 代表 Insert）。文本会被插入到文件中。

- 插入模式 -> 普通模式
    按 `<Esc>` 键停止插入模式并返回普通模式。

### 移动

返回普通模式后，使用这些键移动（或常规箭头键）：

- `h` 左
- `j` 下
- `k` 上
- `l` 右


### 删除

普通模式
- 删除一个字符，将光标移到它上面并输入 `x`。
- 删除整行，使用 `dd` 命令。下一行会向上移动填补空缺

### 撤销

普通模式
- `u` 命令撤销上一次编辑。

### 恢复

普通模式
- `CTRL-R`（重做）来反转前一个命令。换句话说，它撤销撤销。
- 撤销行撤销命令 `U`，撤销最后编辑行上所做的所有更改。输入此命令两次会取消前一个 `U`。

### 追加

在行尾添加内容 `a`（追加）命令完成


### 打开新行

`o` 命令在光标下方创建一个新的空行，并将 Vim 置于插入模式。

### 退出

- `ZZ` 命令  
    写入文件并退出。

### 放弃更改

退出并丢弃更改

```vim
:q!
```

此命令的三个部分是：
- 冒号（`:`），进入命令行模式
- `q` 命令，告诉编辑器退出
- 以及覆盖命令修饰符（`!`）。需要覆盖命令修饰符，因为 Vim 不愿意丢弃更改。

### 接口

- [if_cscop.txt](https://vimhelp.org/if_cscop.txt.html#if_cscop.txt)  
  在 Vim 中使用 Cscope

- [if_lua.txt](https://vimhelp.org/if_lua.txt.html#if_lua.txt)  
  Lua 接口

- [if_mzsch.txt](https://vimhelp.org/if_mzsch.txt.html#if_mzsch.txt)  
  MzScheme 接口

- [if_perl.txt](https://vimhelp.org/if_perl.txt.html#if_perl.txt)  
  Perl 接口

- [if_pyth.txt](https://vimhelp.org/if_pyth.txt.html#if_pyth.txt)  
  Python 接口

- [if_tcl.txt](https://vimhelp.org/if_tcl.txt.html#if_tcl.txt)  
  Tcl 接口

- [if_ole.txt](https://vimhelp.org/if_ole.txt.html#if_ole.txt)  
  用于 Win32 的 OLE 自动化接口

- [if_ruby.txt](https://vimhelp.org/if_ruby.txt.html#if_ruby.txt)  
  Ruby 接口

- [debugger.txt](https://vimhelp.org/debugger.txt.html#debugger.txt)  
  与 a 调试器的接口

- [netbeans.txt](https://vimhelp.org/netbeans.txt.html#netbeans.txt)  
  NetBeans 外部编辑器接口

- [sign.txt](https://vimhelp.org/sign.txt.html#sign.txt)  
  调试标志