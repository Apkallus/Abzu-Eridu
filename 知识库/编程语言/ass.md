## 字段

- `.incbin "path"`：把某个文件的原始字节直接塞进当前 section（不会当成汇编解析）
- `.include "path"`：按文本包含进来，会继续按汇编语法解析（容易报错/泄露）

```
.section .rodata
    .incbin "/flag"
    .byte 0
```
- 切到 `.rodata` 只读数据段，读取文件为字节并在末尾添加 `\00` 后使用 `strings` 提取字符串

### 系统调用

系统调用编号与参数表：
https://x64.syscall.sh/

编译的预定义头部对应值查找：
`grep -r SOCK_STREAM /usr/include/x86_64-linux-gnu`

汇编的网络部分见pwn.college
https://pwn.college/computing-101/building-a-web-server/

使用 `syscall`（即*系统调用*指令）来与操作系统交互（当然是通过 CPU）。

每个系统调用由一个*系统调用号*（从 0 开始向上计数）来指示，你的程序通过将其系统调用号移动到 `rax` 寄存器并调用 `syscall` 指令来调用特定的系统调用。
例如，如果我们想调用系统调用 42（一个你稍后会了解的系统调用！），我们会编写两条指令：

```assembly
mov rax, 42
syscall
```

系统调用编号：
- `exit`  60
- `alarm` 37`  
    在操作系统中设置一个定时器，当经过指定的秒数后，Linux 将终止该程序。

#### write

举一个更具体的例子，如果你想将内存地址 `1337000` 处的 10 个字符写入标准输出（文件描述符 1），这将是：

```c
write(1, 1337000, 10);
```

#### read

对于 `read` 来说，它会从提供的文件描述符中读取一定数量的字节，并将其存储在内存中。
其 C 语言风格的语法与 `write` 相同：

```c
read(0, 1337000, 5);
```

这将从文件描述符 `0`（标准输入）读取 `5` 个字节，存入从 `1337000` 开始的内存中。

### 参数传递

参数通过寄存器传递给系统调用，系统调用可以接受多个参数。
系统调用的第一个参数通过寄存器 `rdi` 传递。

`exit` 仅接受一个参数：退出码。

Linux 中约定的惯例是使用：
- `rsi` 寄存器传递第二个参数
- `rdx` 寄存器传递第三个参数。

### 构建可执行文件

要构建可执行二进制文件，您需要：

1. 将汇编代码写入文件（通常使用 `.S` 或 `.s` 后缀。本例中将使用 `program.s`）。
2. 将汇编文件汇编成*目标文件*（使用 `as` 命令）。
3. 将一个或多个可重定位目标文件链接成最终的可执行二进制文件（使用 `ld` 命令）！

**汇编**
通过在汇编代码开头添加一条伪指令 `.intel_syntax noprefix` 告诉汇编器您将使用Intel汇编语法，特别是无需为每条指令添加额外前缀的变体。

```sh
hacker@dojo:~$ as -o program.o program.s
```

此处，`as` 工具读取 `program.s`，将其汇编成二进制代码，并输出一个名为 `program.o` 的*目标文件*。

**链接**
在典型的开发工作流中，源代码被编译，汇编代码被汇编成目标文件，通常会有多个这样的文件（通常，程序中的每个源代码文件会编译成其自己的目标文件）。
然后将它们*链接*在一起形成一个可执行文件。
即使只有一个文件，我们仍然需要链接它，以准备最终的可执行文件。
这是通过 `ld`（源自术语"链接编辑器"）命令完成的，如下所示：

```sh
hacker@dojo:~$ ld -o program program.o
ld: warning: cannot find entry symbol _start; defaulting to 0000000000401000
```

这将创建一个名为 `program` 的文件，然后我们就可以运行它了！

`ld` 打印了一个关于 `entry symbol _start` 的警告。
`_start` 符号本质上是给 `ld` 的一个说明，指出当ELF文件被执行时，程序执行应从何处开始。
该警告表明，在未指定 `_start` 的情况下，执行将从代码的开头开始。

如果您想消除此错误，可以在代码中指定 `_start` 符号，如下所示：

```asm
.intel_syntax noprefix
.global _start
_start:
THE CODE
```

`.global _start` 指示 `as` 使 `_start` 标签在链接器级别*全局可见*，而不仅仅在目标文件级别局部可见。
`_start:` 添加了一个名为 `_start` 的*标签*，指向您代码的开头。

### 访问内存

```assembly
mov rdi, [31337] <=> 访问内存地址 31337 处的内容
mov rax, [rdi] <=> 以 rdi 寄存器中保存的值作为内存地址，读取地址储存的内容
mov [rax], rdi <=> 以 rax 寄存器中保存的值作为内存地址，向地址的储存空间写入内容
```

当 CPU 执行此指令时，它当然理解 `31337` 是一个*地址*，而不是原始值。

#### 指针与解引用

```assembly
mov rax, 133700
mov rdi, [rax]
```

在这里，我们正在访问内存，但不是像 `133700` 那样为内存读取指定一个固定地址，而是使用存储在 `rax` 中的值作为内存地址。
通过包含内存地址，`rax` 是一个*指针*，它*指向*我们想要访问的数据！
当我们使用 `rax` 来代替直接指定它存储的地址，以访问它引用的内存地址时，我们称之为*解引用*该指针。


#### 带偏移量的解引用

```assembly
mov rax, [rdi+1]
```

在内存术语中，我们称这些数字槽为*字节*：每个内存地址代表一个特定的内存字节。
上面的例子访问的是 `rdi` 所指向的内存地址之后 1 个字节处的内存。
在内存术语中，我们称这 1 个字节的差值为*偏移量*，所以在这个例子中，相对于 `rdi` 指向的地址有一个为 1 的偏移量。

### 运算

#### 加/减/乘

x86 架构包含多种指令，可支持对寄存器和内存执行所有常规数学运算。

为简化表述，当我们使用 `A += B` 时，实际含义为 `A = A + B`。

以下是一些实用指令：
- `add reg1, reg2` ⇔ `reg1 += reg2`
- `sub reg1, reg2` ⇔ `reg1 -= reg2`
- `imul reg1, reg2` ⇔ `reg1 *= reg2`

注意：无符号乘法 `mul` 与有符号乘法 `imul` 在使用寄存器时存在重要差异。

#### 除/模

x86 架构中的除法运算比常规数学中的除法更为特殊。此处的数学运算称为整数运算，意味着每个值都是整数。

例如：在整数运算中，`10 / 3 = 3`。

`3.33` 会被向下取整为整数。

注意：`div` 是一条特殊指令，它可以用一个寄存器作为操作数，将 128 位被除数除以 64 位除数，同时存储商和余数。

例如：
- `mov rax, reg1`
- `div reg2`

对于指令 `div reg`，会发生以下操作：
- `rax = rdx:rax / reg`
- `rdx = 余数`

`rdx:rax` 表示 `rdx` 作为 128 位被除数的高 64 位，`rax` 作为低 64 位。

在调用 `div` 前，必须注意 `rdx` 和 `rax` 中的当前值。

x86 架构允许您在 `div` 操作后获取余数。

例如：`10 / 3` 的余数为 `1`。

余数即等同于模运算，也称为 "mod" 运算符。

#### 高低位字节访问

x86 架构中另一个很酷的概念是能够独立访问寄存器的低位字节。

x86_64 架构中每个寄存器的大小为 64 位，在之前的关卡中，我们使用 `rax`、`rdi` 或 `rsi` 来访问完整的寄存器。

我们还可以通过不同的寄存器名称来访问每个寄存器的低位字节。
例如：`rax` 的低 32 位可通过 `eax` 访问，低 16 位通过 `ax` 访问，低 8 位通过 `al` 访问。

```
MSB                                    LSB
+----------------------------------------+
|                   rax                  |
+--------------------+-------------------+
                     |        eax        |
                     +---------+---------+
                               |   ax    |
                               +----+----+
                               | ah | al |
                               +----+----+
```

寄存器名称：
| 64-bit | 32-bit | 16-bit | 8-bit high | 8-bit low |
|--------|--------|--------|------------|-----------|
| rax    | eax    | ax     | ah         | al        |
| rbx    | ebx    | bx     | bh         | bl        |
| rcx    | ecx    | cx     | ch         | cl        |
| rdx    | edx    | dx     | dh         | dl        |
| rsi    | esi    | si     | —          | sil       |
| rdi    | edi    | di     | —          | dil       |
| rbp    | ebp    | bp     | —          | bpl       |
| rsp    | esp    | sp     | —          | spl       |
| r8     | r8d    | r8w    | —          | r8b       |
| r9     | r9d    | r9w    | —          | r9b       |
| r10    | r10d   | r10w   | —          | r10b      |
| r11    | r11d   | r11w   | —          | r11b      |
| r12    | r12d   | r12w   | —          | r12b      |
| r13    | r13d   | r13w   | —          | r13b      |
| r14    | r14d   | r14w   | —          | r14b      |
| r15    | r15d   | r15w   | —          | r15b      |

内存大小名称的细分：
- Quad Word = 8 Bytes = 64 bits
- Double Word = 4 bytes = 32 bits
- Word = 2 bytes = 16 bits
- Byte = 1 byte = 8 bits

##### 优化模运算

事实证明，使用 `div` 运算符计算模运算速度较慢！

我们可以使用数学技巧来优化模运算符（`%`）。编译器经常使用这种技巧。

如果存在 `x % y`，且 `y` 是 2 的幂次方（例如 `2^n`），则结果将是 `x` 的低 `n` 位。

因此，我们可以利用低位寄存器字节访问来高效实现模运算！


#### 位移

位移的一个额外好处是可以实现快速乘法（乘以 2）或除法（除以 2），还可用于计算模运算。
以下是重要指令：
- `shl reg1, reg2` <=> 将 `reg1` 左移 `reg2` 指定的位数
- `shr reg1, reg2` <=> 将 `reg1` 右移 `reg2` 指定的位数

注意：“reg2” 可由常量或内存位置替代。

#### 位与运算

x86 中的逻辑指令：`and`、`or`、`not`、`xor`。

汇编中的位逻辑操作是另一个有趣的概念！x86 允许您对寄存器执行逐位逻辑运算。

如果我们使用 `and rax, rbx` 指令对 `rax` 和 `rbx` 执行按位 AND 运算，结果将通过逐对进行 AND 运算得出，因此称为位逻辑运算。

### 内存地址

- 64 位  
    - `add qword ptr [0x404000], 0x1337`
    - `mov r/m64, imm32`  
        - 目的操作数可以是 64 位内存
        - 但立即数只能是 32 位，会在硬件里被符号扩展成 64 位写入。
- 32 位  
    `add dword ptr [0x404000], 0x1337`

`mov ecx, dword ptr [rdi]`
从地址rdi处取出双字保存到寄存器ecx中

`movsxd` 
根据最高位（符号位）填充高 32 位，这样负数就能正确保留。

`movsxd rax, DWORD PTR [rdi+4]`
从地址rdi+4处取出双字后进行符号扩展再保存到rax中

读取双字并进行符号扩展

### 内存偏移

内存的实际布局方式是逐字节存储（小端序）：

```
[0x1337] = 0xef
[0x1337 + 1] = 0xbe
[0x1337 + 2] = 0xad
...
[0x1337 + 7] = 0x00
```

这种布局对我们有何用处？
这意味着我们可以使用偏移量来访问相邻的数据，类似于上文展示的方式。
假设您需要访问某个地址的第 5 个*字节*，可以通过以下方式访问：

```
mov al, [address+4]
```

请注意：偏移量从 0 开始计数。


### 栈

读写栈数据，使用 `pop` 和 `push` 指令。  
通过栈指针寄存器（`rsp`）来获取栈的当前位置。

要将数值存入栈中，我们使用 `push` 指令；要取出数值，则使用 `pop` 指令。
栈采用后进先出（LIFO）的内存结构，这意味着最后压入的值将最先被弹出。

在 x86 架构中，栈指针存储在特殊寄存器 `rsp` 中。`rsp` 始终存储栈顶的内存地址，即最后压入值的内存地址。

### 跳转

跳转分为两种类型：
- 无条件跳转
- 条件跳转

所有跳转指令可分为三种类型：
- 相对跳转（Relative jumps）：从当前指令位置向前或向后跳转指定字节数。
- 绝对跳转（Absolute jumps）：跳转到某个固定的内存地址。
- 间接跳转（Indirect jumps）：跳转到寄存器或某个内存位置中存储的地址。

#### 绝对跳转
常数绝对跳转
```
jmp 常数
```

#### 间接跳转
**寄存器间接跳转**：
```
mov rax, 0x403000
jmp rax 
```

想要运行时把 RIP 直接设成某个常数地址，就必须用间接跳转。

**跳转表**
条件跳转，只能跳到“代码标签”，不能跳到“内存里存着的地址”。

使用跳转表时条件跳转到默认分支标签后使用无条件跳转到跳转表的默认地址：
```
cmp   rdi, 3            ;  此处rdi保存差异，rsi保存跳转表基地址
jg    default_label      ; 只决定走 case 还是 default
jmp   [rsi + rdi*8]      ; case 0–3
default_label:
jmp   [rsi + 4*8]        ; default，对应表中最后一项
```

跳转表：
```
section .rodata
jump_table:
    dq case0        ; 索引 0
    dq case1        ; 索引 1
    dq case2        ; 索引 2
    dq default_case ; 索引 3（当作 default）

section .text
global _start
_start:
    ; 此处rdi保存差异
    cmp     rdi, 2          
    ja      use_default

    jmp     qword ptr jump_table[rdi*8]

use_default:
    lea     rax, [rel jump_table]
    jmp     qword [rax + 3*8]      

case0:
    foocode
    jmp end
case1:
    foocode
    jmp end
case2:
    foocode
    jmp end
default_case:
    foocode
end:
    foocode
```

跳转表跳转的两种指令：
- `jmp  qword ptr jump_table[rdi*8]`  
    使用跳转表基地址进行偏移后跳转到自定义标签
- `lea  rax, [rel jump_table]`  
    提取跳转表基地址  
    `jmp  qword [rax + rdi*8]`  
    由基地址计算偏移后跳转到自定义标签

**相对跳转**
- 标号相对跳转
    ```
    jmp <标号>
    中间代码
    <标号>:
    后续代码
    ```
- 当前位置符号`.`与立即数的计算
    ```
    jmp .+2+0x51
    ```
    在`jmp`占用的`2`字节后（当前位置+2），向后跳转`0x51`字节

要实现一个相对跳转，你需要用到以下几个工具：

- `labels`（标号）：你可以使用标号作为占位符，而无需手动计算地址。汇编器会自动计算你的跳转指令到该标号之间的偏移量。
- `nop`（No Operation，空操作）：一个单字节指令，本身不做任何事情。因为其大小可预测，可以作为填充，用来精确控制跳转距离。
- `.rept`（重复伪指令）：一种指示汇编器将给定指令重复多次的伪指令： [GNU Assembler Manual](https://ftp.gnu.org/old-gnu/Manuals/gas-2.9.1/html_chapter/as_7.html) 它非常适合用来生成一大段 `nop` 指令，而无需逐条手动输入。

    `.rept count`
    Repeat the sequence of lines between the `.rept` directive and the next `.endr` directive count times.

    For example, assembling：
    ```
    .rept   3
    .long   0
    .endr
    ```

    is equivalent to assembling：
    ```
    .long   0
    .long   0
    .long   0
    ```
    
### 函数

函数是一段可调用的代码片段，不会破坏控制流。

函数使用"call"和"ret"指令。

"call"指令将下一条指令的内存地址压入栈中，然后跳转到第一个参数中存储的值。

`ret` 从栈顶弹出一个值并跳转到该地址。

标签名就是函数名。

call 使用间接调用

### 函数栈帧

*函数栈帧*是一组被压入栈的指针和值，用于保存内容以备后用，并为函数变量在栈上分配空间。
首先，我们来谈谈特殊寄存器 `rbp`——*栈基指针*。

`rbp` 寄存器用于指示我们的栈帧最初开始的位置。举例来说，假设我们想要构造一个仅在函数内使用的列表（一段连续的内存空间）。该列表包含 5 个元素，每个元素是一个 `dword`。一个包含 5 个元素的列表会占用 5 个寄存器，因此，我们可以在栈上分配空间！

为了给栈提供更多空间，我们减去所需的空间。

使用后恢复栈

`[寄存器 - 值]` 的减法运算可能报错，可能需拆分步骤或转为加法

### 不常见的指令

#### `repne   scasb byte [rdi]` 

等效于：
`repnz scas al,BYTE PTR es:[rdi]`

```log
mov     rbp, qword [rsi+0x8]      ; rbp = argv[1]，指向整个文件名字符串

or      rcx, 0xffffffffffffffff   ; rcx = -1 (0xffffffffffffffff)
lea     rsi, [rel data_4020d3]    ; rsi = ".cimg"
mov     rdi, rbp                  ; rdi = argv[1]，扫描的起始地址

repne   scasb byte [rdi]          ; 用 AL 中的字节在 [rdi] 开始的串里查找
                                  ; （这里 AL=0，用来找 '\0' 终止符）
not     rcx
lea     rdi, [rbp+rcx-0x6]        ; 重新算一个指针 rdi，指向“末尾往前 6 字节”的位置
call    strcmp
```

- `scasb`：把内存 [rdi] 的一个字节和 `AL` 比较，每次比较后：
    - `rdi` 自动加 1（DF=0 时）
    - `rcx` 自动减 1
- `repne`：在 `ZF == 0` 且 `RCX != 0` 时重复

典型用法是：
事先把 AL 设成 0（查找字符串终止符 '\0'）
RCX 设成 -1，表示“无限大计数器”
执行完后：
rdi 指向字符串末尾的 '\0' 后面一个字节
rcx 变成 -(长度+2)，not rcx 后就变成 长度+1（回想二进制反转：-1反转为0，-2反转为+1）。
`rbp+rcx-0x6` 同样指向字符串末尾的 '\0' 后面一个字节

#### `rep stosb byte [rdi]`

等效于：
`rep stos BYTE PTR es:[rdi],al`

- `stosb`：把寄存器 `AL` 的值，写到内存地址 [rdi]，然后根据方向标志调整 rdi（一般是 rdi++）。
- `rep`：把 `stosb` 重复执行 `ecx` 次。

#### 函数参数

System V AMD64 调用约定下，前 6 个整数/指针参数放在寄存器里（后面的可变参数走栈 push）。
即，看到调用函数前的一堆push已经之后的 add rsp 即推测为函数参数操作

### 跳转表

跳转表：一块连续的内存区域，里面每一项都是一个代码位置的地址（或相对偏移）。

### `sendfile(输入，输出，偏移，长度)`

无 0x00 版 shellcode
```asm
.intel_syntax noprefix
.global _start
_start:

## read() 代码 2
# 设置字符串 /flag 为第一参数
# mov rdi, 0x0067616c662f

mov edi, 0x67616c66
shl rdi, 8
mov dil, 0x2f
push rdi
mov rdi, rsp

# 设置 O_RDONLY 为第二参数，对应数字 0
xor rsi, rsi
# 设置 read 的系统调用代码
# mov rax, 2
xor rax, rax
mov al, 2
syscall
# rax 得到文件描述符

## sendfile() 代码 40
# 设置标准输出为 sendfile 的输出
# mov rdi, 1
xor rdi, rdi
inc rdi
# 设置 /flag 文件描述符为输入
mov rsi, rax
# 设置第三参数偏移为0，第四参数长度为任意
xor rdx, rdx

xor r10, r10
inc r10
shl r10, 10

xor rax, rax
mov al, 40
syscall

## 退出 60
xor rdi, rdi
xor rax, rax
mov al, 60
syscall


```
