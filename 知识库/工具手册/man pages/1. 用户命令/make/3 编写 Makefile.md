https://www.gnu.org/software/make/manual/make.html

## 3 编写 Makefile

告诉 `make` 如何重新编译系统的信息来自读取一个称为 *makefile* 的数据库。

- “Makefile 包含什么”
- “给 Makefile 取什么名字”
- “包含其他 Makefile”
- “变量 `MAKEFILES`”
- “Makefile 如何被重新生成”
- “覆盖另一个 Makefile 的一部分”
- “`make` 如何读取 Makefile”
- “Makefile 如何被解析”
- “二次展开”

---

### 3.1 Makefile 包含什么

Makefile 包含五类内容：*显式规则*、*隐式规则*、*变量定义*、*指令*和*注释*。规则、变量和指令将在后续章节中详细描述。

- *显式规则*说明何时以及如何重新生成一个或多个文件，这些文件称为规则的*目标*。它列出目标所依赖的其他文件，称为目标的*先决条件*，还可以给出用于创建或更新目标的配方。参见“编写规则”。

- *隐式规则*说明何时以及如何基于文件名重新生成一类文件。它描述目标如何依赖于一个名称与目标相似的文件，并给出用于创建或更新此类目标的配方。参见“使用隐式规则”。

- *变量定义*是一行，为变量指定一个文本字符串值，该值稍后可以替换到文本中。简单的 makefile 示例展示了 `objects` 的变量定义，它是所有目标文件的列表（参见“变量使 Makefile 更简单”）。

- *指令*是让 `make` 在读取 makefile 时执行某些特殊操作的指示。这些包括：
  - 读取另一个 makefile（参见“包含其他 Makefile”）。
  - 决定（基于变量的值）是使用还是忽略 makefile 的某一部分（参见“Makefile 的条件部分”）。
  - 从包含多行的逐字字符串定义变量（参见“定义多行变量”）。

- makefile 一行中的 `#` 开始一个*注释*。它以及该行其余内容会被忽略，但末尾的反斜杠如果没有被另一个反斜杠转义，则会将注释延续到多行。仅包含注释（前面可能有一些空格）的行实际上是空行，会被忽略。如果你想要字面量 `#`，请用反斜杠转义它（例如 `\#`）。注释可以出现在 makefile 的任何行中，尽管在某些情况下会受到特殊处理。

  你不能在变量引用或函数调用中使用注释：在变量引用或函数调用内部，任何 `#` 实例都会被按字面处理（而不是作为注释的开始）。

  配方中的注释会像其他配方文本一样传递给 shell。由 shell 决定如何解释它：它是否为注释取决于 shell。

  在 `define` 指令内部，定义变量时注释不会被忽略，而是完整保留在变量的值中。当变量被展开时，它们将被视为 `make` 注释或配方文本，具体取决于变量求值所在的上下文。

#### 3.1.1 拆分长行

Makefile 使用“基于行”的语法，其中换行符是特殊的，并标记语句的结束。GNU `make` 对语句行的长度没有限制，最多受计算机内存量限制。

然而，如果行太长而无法在不换行或滚动的情况下显示，就很难阅读。因此，你可以通过在语句中间添加换行符来格式化 makefile 以提高可读性：为此，用反斜杠（`\`）字符转义内部换行符。在需要区分时，我们将“物理行”称为以换行符结尾的单行（无论是否被转义），而“逻辑行”是完整语句，包括直到第一个未转义换行符之前的所有已转义换行符。

反斜杠/换行组合的处理方式取决于语句是配方行还是非配方行。配方行中反斜杠/换行的处理将在后面讨论（参见“拆分配方行”）。

在配方行之外，反斜杠/换行会被转换为单个空格字符。完成后，反斜杠/换行周围的所有空白会压缩为单个空格：这包括反斜杠之前的所有空白、反斜杠/换行之后行首的所有空白，以及任何连续的反斜杠/换行组合。

如果定义了 `.POSIX` 特殊目标，则反斜杠/换行处理会稍作修改以符合 POSIX.2：第一，反斜杠之前的空白不会被移除；第二，连续的反斜杠/换行不会被压缩。

##### 拆分而不添加空白

如果你需要拆分一行但*不*希望添加任何空白，可以利用一个巧妙的技巧：将反斜杠/换行对替换为三个字符：美元符号、反斜杠和换行符：

```makefile
var := one$\
       word
```

在 `make` 移除反斜杠/换行并将下一行压缩为单个空格后，这等价于：

```makefile
var := one$ word
```

然后 `make` 将执行变量展开。变量引用 `$ ` 引用一个名称为“ ”（空格）的单字符变量，该变量不存在，因此展开为空字符串，最终赋值等价于：

```makefile
var := oneword
```

---

### 3.2 给 Makefile 取什么名字

默认情况下，当 `make` 查找 makefile 时，它会按以下顺序尝试这些名称：`GNUmakefile`、`makefile` 和 `Makefile`。

通常你应该将 makefile 命名为 `makefile` 或 `Makefile`。（我们推荐 `Makefile`，因为它会显眼地出现在目录列表开头附近，紧邻其他重要文件如 `README`。）首先检查的名称 `GNUmakefile` 不推荐用于大多数 makefile。如果你有一个特定于 GNU `make` 的 makefile，并且其他版本的 `make` 无法理解它，则应使用此名称。其他 `make` 程序会查找 `makefile` 和 `Makefile`，但不会查找 `GNUmakefile`。

如果 `make` 没有找到这些名称中的任何一个，它不会使用任何 makefile。然后你必须用命令参数指定一个目标，`make` 将尝试仅使用其内置隐式规则来弄清楚如何重新生成它。参见“使用隐式规则”。

如果你想为 makefile 使用非标准名称，可以使用 `-f` 或 `--file` 选项指定 makefile 名称。参数 `-f name` 或 `--file=name` 告诉 `make` 将文件 `name` 作为 makefile 读取。如果使用多个 `-f` 或 `--file` 选项，可以指定多个 makefile。所有 makefile 会按指定顺序有效连接。如果指定了 `-f` 或 `--file`，则不会自动检查默认 makefile 名称 `GNUmakefile`、`makefile` 和 `Makefile`。

---

### 3.3 包含其他 Makefile

`include` 指令告诉 `make` 暂停读取当前 makefile，并在继续之前读取一个或多个其他 makefile。该指令是 makefile 中的一行，如下所示：

```makefile
include filenames…
```

`filenames` 可以包含 shell 文件名模式。如果 `filenames` 为空，则不包含任何内容，也不打印错误。

行首允许并忽略额外空格，但第一个字符不能是制表符（或 `.RECIPEPREFIX` 的值）——如果行以制表符开头，它将被视为配方行。`include` 与文件名之间以及文件名之间需要空白；那里以及指令末尾的额外空白会被忽略。行尾允许以 `#` 开头的注释。如果文件名包含任何变量或函数引用，它们会被展开。参见“如何使用变量”。

例如，如果你有三个 `.mk` 文件：`a.mk`、`b.mk` 和 `c.mk`，并且 `$(bar)` 展开为 `bish bash`，则以下表达式

```makefile
include foo *.mk $(bar)
```

等价于

```makefile
include foo a.mk b.mk c.mk bish bash
```

当 `make` 处理 `include` 指令时，它会暂停读取包含该指令的 makefile，并依次读取每个列出的文件。完成后，`make` 恢复读取出现该指令的 makefile。

使用 `include` 指令的一种场合是：由不同目录中的各个 makefile 处理的多个程序需要使用一组公共变量定义（参见“设置变量”）或模式规则（参见“定义和重新定义模式规则”）。

另一种场合是你希望从源文件自动生成先决条件；可以将先决条件放入一个由主 makefile 包含的文件中。这种做法通常比传统上其他版本 `make` 所做的那样，以某种方式将先决条件追加到主 makefile 末尾更清晰。参见“自动生成先决条件”。

如果指定的名称不以斜杠开头（或当 GNU Make 使用 MS-DOS / MS-Windows 路径支持编译时，不以驱动器号和冒号开头），并且当前目录中找不到该文件，则会搜索其他几个目录。首先搜索你使用 `-I` 或 `--include-dir` 选项指定的任何目录（参见“选项摘要”）。然后按以下顺序搜索以下目录（如果存在）：`prefix/include`（通常为 `/usr/local/include`）、`/usr/gnu/include`、`/usr/local/include`、`/usr/include`。

`.INCLUDE_DIRS` 变量将包含 `make` 搜索包含文件的当前目录列表。参见“其他特殊变量”。

你可以通过在命令行中添加带有特殊值 `-` 的命令行选项 `-I`（例如 `-I-`）来避免搜索这些默认目录。这会使 `make` 忘记任何已设置的包含目录，包括默认目录。

如果在这些目录中的任何一个都找不到包含的 makefile，这不会立即成为致命错误；包含该 `include` 的 makefile 的处理会继续。在完成 makefile 读取后，`make` 将尝试重新生成任何过时或不存在的 makefile。参见“Makefile 如何被重新生成”。只有在未能找到重新生成该 makefile 的规则，或者找到了规则但配方失败之后，`make` 才会将缺失的 makefile 诊断为致命错误。

如果你希望 `make` 简单地忽略不存在或无法重新生成的 makefile，并且不显示错误消息，请使用 `-include` 指令而不是 `include`，如下所示：

```makefile
-include filenames…
```

这在各方面都像 `include` 一样，区别在于如果任何 `filenames`（或任何 `filenames` 的任何先决条件）不存在或无法重新生成，则不会报错（甚至没有警告）。

为了与某些其他 `make` 实现兼容，`sinclude` 是 `-include` 的另一个名称。

---

### 3.4 变量 `MAKEFILES`

如果定义了环境变量 `MAKEFILES`，`make` 会将其值视为一个名称列表（用空白分隔），这些是应在其他 makefile 之前读取的附加 makefile。这很像 `include` 指令：会在各种目录中搜索这些文件（参见“包含其他 Makefile”）。此外，默认目标绝不会从这些 makefile（或它们包含的任何 makefile）中获取，并且如果 `MAKEFILES` 中列出的文件未找到，也不算是错误。

`MAKEFILES` 的主要用途是在 `make` 的递归调用之间通信（参见“`make` 的递归使用”）。通常不建议在顶层调用 `make` 之前设置该环境变量，因为通常最好不要从外部干扰 makefile。但是，如果你在没有特定 makefile 的情况下运行 `make`，`MAKEFILES` 中的 makefile 可以做一些有用的事情来帮助内置隐式规则更好地工作，例如定义搜索路径（参见“为先决条件搜索目录”）。

一些用户倾向于在登录时自动在环境中设置 `MAKEFILES`，并编写 makefile 期望这样做。这是一个非常糟糕的主意，因为如果由其他任何人运行，此类 makefile 将无法工作。最好在 makefile 中编写显式的 `include` 指令。参见“包含其他 Makefile”。

---

### 3.5 Makefile 如何被重新生成

有时 makefile 可以从其他文件重新生成，例如 RCS 或 SCCS 文件。如果 makefile 可以从其他文件重新生成，你可能希望 `make` 获取最新版本的 makefile 来读取。

为此，在读取所有 makefile 后，`make` 会按处理顺序将每个视为目标，并尝试更新它。如果启用了并行构建（参见“并行执行”），则 makefile 也会并行重建。

如果 makefile 有一条说明如何更新它的规则（可以在该 makefile 本身或另一个 makefile 中找到），或者有隐式规则适用于它（参见“使用隐式规则”），则在必要时会更新它。检查完所有 makefile 后，如果其中任何一个实际发生了变化，`make` 会从干净状态开始，并再次读取所有 makefile。（它还会再次尝试更新每个 makefile，但通常不会再改变它们，因为它们已经是最新的。）每次重新启动都会导致特殊变量 `MAKE_RESTARTS` 被更新（参见“其他特殊变量”）。

如果你知道一个或多个 makefile 无法重新生成，并且希望阻止 `make` 对它们执行隐式规则搜索（也许是出于效率原因），你可以使用任何阻止隐式规则查找的常规方法。例如，你可以编写一条显式规则，以该 makefile 为目标，并使用空配方（参见“使用空配方”）。

如果 makefile 指定了一条双冒号规则来重新生成带有配方但没有先决条件的文件，则该文件将始终被重新生成（参见“双冒号规则”）。对于 makefile 来说，如果某个 makefile 具有带配方但没有先决条件的双冒号规则，则每次运行 `make` 时都会重新生成它，然后在 `make` 重新开始并再次读取 makefile 后再次重新生成。这会导致无限循环：`make` 会不断重新生成 makefile 并重新启动，永远不做其他事情。因此，为了避免这种情况，`make` **不会**尝试重新生成被指定为带配方但没有先决条件的双冒号规则目标的 makefile。

伪目标（参见“伪目标”）具有相同的效果：它们永远不会被认为是最新的，因此标记为伪目标的包含文件会导致 `make` 不断重新启动。为了避免这种情况，`make` 不会尝试重新生成标记为伪目标的 makefile。

你可以利用这一点来优化启动时间：如果你知道不需要重新生成 `Makefile`，可以通过添加以下内容之一来阻止 `make` 尝试重新生成它：

```makefile
.PHONY: Makefile
```

或者：

```makefile
Makefile:: ;
```

如果你没有使用 `-f` 或 `--file` 选项指定任何要读取的 makefile，`make` 将尝试默认 makefile 名称；参见“给 Makefile 取什么名字”。与使用 `-f` 或 `--file` 选项显式请求的 makefile 不同，`make` 并不确定这些 makefile 应该存在。但是，如果默认 makefile 不存在但可以通过运行 make 规则创建，你可能希望运行这些规则，以便可以使用该 makefile。

因此，如果默认 makefile 都不存在，`make` 将尝试生成它们中的每一个，直到成功生成一个，或者尝试完所有名称。请注意，如果 `make` 找不到或无法生成任何 makefile，这不算错误；makefile 并不总是必需的。

当你使用 `-t` 或 `--touch` 选项（参见“代替执行配方”）时，你不会希望使用过时的 makefile 来决定要触摸哪些目标。因此，`-t` 选项对更新 makefile 没有影响；即使指定了 `-t`，它们也会真正更新。同样，`-q`（或 `--question`）和 `-n`（或 `--just-print`）不会阻止更新 makefile，因为过时的 makefile 会导致其他目标的输出错误。因此，`make -f mfile -n foo` 将更新 `mfile`，读取它，然后打印更新 `foo` 及其先决条件所需的配方而不运行它。为 `foo` 打印的配方将是更新后的 `mfile` 内容中指定的配方。

然而，有时你可能确实希望连 makefile 也不更新。你可以通过在命令行中将 makefile 指定为目标，同时也将其指定为 makefile 来实现。当 makefile 名称被显式指定为目标时，`-t` 等选项确实会应用于它们。

因此，`make -f mfile -n mfile foo` 将读取 makefile `mfile`，打印更新它所需的配方而不实际运行，然后打印更新 `foo` 所需的配方而不运行该配方。`foo` 的配方将由 `mfile` 的现有内容指定。

---

### 3.6 覆盖另一个 Makefile 的一部分

有时拥有一个与另一个 makefile 基本相同的 makefile 很有用。你通常可以使用 `include` 指令将一个包含到另一个中，并添加更多目标或变量定义。但是，两个 makefile 为同一目标给出不同配方是无效的。不过还有另一种方法。

在包含方 makefile（想要包含另一个 makefile 的那个）中，你可以使用匹配任意内容的模式规则，表示要重新生成任何无法根据包含方 makefile 中的信息生成的目标时，`make` 应查看另一个 makefile。关于模式规则的更多信息，参见“定义和重新定义模式规则”。

例如，如果你有一个名为 `Makefile` 的 makefile，说明如何生成目标 `foo`（以及其他目标），你可以编写一个名为 `GNUmakefile` 的 makefile，其中包含：

```makefile
foo:
        frobnicate > foo

%: force
        @$(MAKE) -f Makefile $@
force: ;
```

如果你说 `make foo`，`make` 将找到 `GNUmakefile`，读取它，并看到要生成 `foo`，需要运行配方 `frobnicate > foo`。如果你说 `make bar`，`make` 在 `GNUmakefile` 中找不到生成 `bar` 的方法，因此它将使用模式规则中的配方：`make -f Makefile bar`。如果 `Makefile` 提供了更新 `bar` 的规则，`make` 将应用该规则。对于 `GNUmakefile` 未说明如何生成的任何其他目标，情况同样如此。

其工作方式是：模式规则的模式仅为 `%`，因此它匹配任何目标。该规则指定先决条件 `force`，以保证即使目标文件已经存在，配方也会运行。我们给 `force` 目标一个空配方，以防止 `make` 搜索构建它的隐式规则——否则它会对 `force` 本身应用相同的匹配任意内容规则，并创建先决条件循环！

---

### 3.7 `make` 如何读取 Makefile

GNU `make` 分两个不同阶段完成工作。在第一阶段，它读取所有 makefile、包含的 makefile 等，并内化所有变量及其值以及隐式和显式规则，并构建所有目标及其先决条件的依赖图。在第二阶段，`make` 使用这些内化数据来确定哪些目标需要更新，并运行更新它们所需的配方。

理解这种两阶段方法很重要，因为它直接影响变量和函数展开的发生方式；这通常是编写 makefile 时产生混淆的一个来源。下面是 makefile 中可能出现的不同构造的摘要，以及构造的每个部分发生展开的阶段。

如果展开发生在第一阶段，我们说展开是*立即的*：`make` 会在解析 makefile 时展开构造的该部分。如果展开不是立即的，我们说展开是*延迟的*。延迟构造部分的展开会推迟到使用展开时：要么是在立即上下文中引用它时，要么是在第二阶段需要它时。

你可能还不熟悉其中一些构造。在后续章节中逐渐熟悉它们时，可以参考本节。

#### 变量赋值

变量定义按如下方式解析：

```makefile
immediate = deferred
immediate ?= deferred
immediate := immediate
immediate ::= immediate
immediate :::= immediate-with-escape
immediate += deferred or immediate
immediate != immediate

define immediate
  deferred
endef

define immediate =
  deferred
endef

define immediate ?=
  deferred
endef

define immediate :=
  immediate
endef

define immediate ::=
  immediate
endef

define immediate :::=
  immediate-with-escape
endef

define immediate +=
  deferred or immediate
endef

define immediate !=
  immediate
endef
```

对于追加运算符 `+=`，如果变量之前被设置为简单变量（`:=` 或 `::=`），则右侧被视为立即的；否则为延迟的。

对于立即展开并转义的运算符 `:::=`，右侧的值会立即展开，然后转义（即展开结果中的所有 `$` 实例都替换为 `$$`）。

对于 shell 赋值运算符 `!=`，右侧会立即求值并交给 shell。结果存储在左侧命名的变量中，该变量被视为递归展开变量（因此每次引用时都会重新求值）。

#### 条件指令

条件指令会立即解析。这意味着，例如，自动变量不能用于条件指令，因为自动变量直到调用该规则的配方时才设置。如果你需要在条件指令中使用自动变量，你*必须*将条件移入配方中，并改用 shell 条件语法。

#### 规则定义

无论形式如何，规则总是以相同方式展开：

```makefile
immediate : immediate ; deferred
        deferred
```

也就是说，目标和先决条件部分会立即展开，而用于构建目标的配方总是延迟展开。对于显式规则、模式规则、后缀规则、静态模式规则和简单先决条件定义，都是如此。

---

### 3.8 Makefile 如何被解析

GNU `make` 逐行解析 makefile。解析过程使用以下步骤：

1. 读入一个完整的逻辑行，包括反斜杠转义的行（参见“拆分长行”）。

2. 移除注释（参见“Makefile 包含什么”）。

3. 如果该行以配方前缀字符开头且处于规则上下文中，则将该行添加到当前配方并读取下一行（参见“配方语法”）。

4. 展开该行中出现在*立即*展开上下文中的元素（参见“`make` 如何读取 Makefile”）。

5. 扫描该行以查找分隔符字符，例如 `:` 或 `=`，以确定该行是宏赋值还是规则（参见“配方语法”）。

6. 将结果操作内化并读取下一行。

这的一个重要结果是，宏可以展开为整个规则，*如果它只有一行*。这将起作用：

```makefile
myrule = target : ; echo built

$(myrule)
```

然而，这将不起作用，因为 `make` 在展开行后不会重新拆分它们：

```makefile
define myrule
target:
        echo built
endef

$(myrule)
```

上述 makefile 导致定义了一个目标 `target`，其先决条件为 `echo` 和 `built`，就像 makefile 包含 `target: echo built` 一样，而不是包含配方的规则。展开完成后行中仍存在的换行符会作为普通空白被忽略。

为了正确展开多行宏，必须使用 `eval` 函数：这会导致 `make` 解析器对展开宏的结果运行（参见“`eval` 函数”）。

---

### 3.9 二次展开

前面我们了解到 GNU `make` 分两个不同阶段工作：读入阶段和目标更新阶段（参见“`make` 如何读取 Makefile”）。GNU Make 还能够对 makefile 中定义的某些或所有目标的先决条件（仅先决条件）启用*二次展开*。为了发生这种二次展开，必须在第一个使用此功能的先决条件列表之前定义特殊目标 `.SECONDEXPANSION`。

如果定义了 `.SECONDEXPANSION`，那么当 GNU `make` 需要检查目标的先决条件时，先决条件会被*第二次*展开。在大多数情况下，这种二次展开不会产生效果，因为所有变量和函数引用在 makefile 的初始解析期间都已经展开。因此，为了利用解析器的二次展开阶段，有必要在 makefile 中转义变量或函数引用。在这种情况下，第一次展开仅仅取消引用转义，但不会展开它，展开留给二次展开阶段。例如，考虑这个 makefile：

```makefile
.SECONDEXPANSION:
ONEVAR = onefile
TWOVAR = twofile
myfile: $(ONEVAR) $$(TWOVAR)
```

在第一次展开阶段之后，`myfile` 目标的先决条件列表将是 `onefile` 和 `$(TWOVAR)`；第一个（未转义的）对 `ONEVAR` 的变量引用被展开，而第二个（已转义的）变量引用只是取消转义，而不会被识别为变量引用。现在在二次展开期间，第一个单词再次展开，但由于它不包含变量或函数引用，因此仍为值 `onefile`；而第二个单词现在是变量 `TWOVAR` 的普通引用，展开为值 `twofile`。最终结果是两个先决条件：`onefile` 和 `twofile`。

显然，这不是一个非常有趣的案例，因为只需让两个变量都不转义地出现在先决条件列表中，就可以更轻松地获得相同结果。如果变量被重置，一个差异就会显现；考虑这个示例：

```makefile
.SECONDEXPANSION:
AVAR = top
onefile: $(AVAR)
twofile: $$(AVAR)
AVAR = bottom
```

这里，`onefile` 的先决条件会立即展开并解析为值 `top`，而 `twofile` 的先决条件直到二次展开才会完全展开，并产生值 `bottom`。

这稍微更有趣一些，但只有当你发现二次展开总是在该目标的自动变量作用域内发生时，此功能的真正威力才会显现。这意味着你可以在二次展开期间使用 `$@`、`$*` 等变量，它们将具有预期值，就像在配方中一样。你所要做的就是通过转义 `$` 来延迟展开。此外，二次展开对显式规则和隐式（模式）规则都会发生。了解了这一点，此功能的可能用途会急剧增加。例如：

```makefile
.SECONDEXPANSION:
main_OBJS := main.o try.o test.o
lib_OBJS := lib.o api.o

main lib: $$($$@_OBJS)
```

这里，在初始展开之后，`main` 和 `lib` 两个目标的先决条件都将是 `$($@_OBJS)`。在二次展开期间，`$@` 变量被设置为目标名称，因此 `main` 目标的展开将产生 `$(main_OBJS)`，即 `main.o try.o test.o`；而 `lib` 目标的二次展开将产生 `$(lib_OBJS)`，即 `lib.o api.o`。

你还可以在这里混入函数，只要它们被正确转义：

```makefile
main_SRCS := main.c try.c test.c
lib_SRCS := lib.c api.c

.SECONDEXPANSION:
main lib: $$(patsubst %.c,%.o,$$($$@_SRCS))
```

此版本允许用户指定源文件而不是目标文件，但产生与上一个示例相同的先决条件列表。

在二次展开阶段对自动变量（尤其是目标名称变量 `$$@`）的求值行为类似于配方内的求值。但是，对于 `make` 理解的不同类型的规则定义，会有一些细微差异和“边界情况”发挥作用。下面描述使用不同自动变量的微妙之处。

#### 显式规则的二次展开

在显式规则的二次展开期间，`$$@` 和 `$$%` 分别求值为目标的文件名，以及当目标是归档成员时求值为目标成员名。`$$<` 变量求值为该目标第一条规则中的第一个先决条件。`$$^` 和 `$$+` 求值为同一目标*已经出现*的规则的所有先决条件列表（`$$+` 包含重复项，`$$^` 不包含）。以下示例有助于说明这些行为：

```makefile
.SECONDEXPANSION:

foo: foo.1 bar.1 $$< $$^ $$+    # 第 1 行

foo: foo.2 bar.2 $$< $$^ $$+    # 第 2 行

foo: foo.3 bar.3 $$< $$^ $$+    # 第 3 行
```

在第一个先决条件列表中，所有三个变量（`$$<`、`$$^` 和 `$$+`）都展开为空字符串。在第二个中，它们将分别具有值 `foo.1`、`foo.1 bar.1` 和 `foo.1 bar.1`。在第三个中，它们将分别具有值 `foo.1`、`foo.1 bar.1 foo.2 bar.2` 和 `foo.1 bar.1 foo.2 bar.2 foo.1 foo.1 bar.1 foo.1 bar.1`。

规则按 makefile 顺序进行二次展开，但带有配方的规则总是最后求值。

变量 `$$?` 和 `$$*` 不可用，会展开为空字符串。

#### 静态模式规则的二次展开

静态模式规则的二次展开规则与上面的显式规则相同，只有一个例外：对于静态模式规则，`$$*` 变量被设置为模式词干。与显式规则一样，`$$?` 不可用，会展开为空字符串。

#### 隐式规则的二次展开

当 `make` 搜索隐式规则时，它会替换词干，然后对每个具有匹配目标模式的规则执行二次展开。自动变量的值以与静态模式规则相同的方式推导。例如：

```makefile
.SECONDEXPANSION:

foo: bar

foo foz: fo%: bo%

%oo: $$< $$^ $$+ $$*
```

当对目标 `foo` 尝试隐式规则时，`$$<` 展开为 `bar`，`$$^` 展开为 `bar boo`，`$$+` 也展开为 `bar boo`，`$$*` 展开为 `f`。

请注意，如“隐式规则搜索算法”中所述，目录前缀（D）会在展开后附加到先决条件列表中的所有模式。例如：

```makefile
.SECONDEXPANSION:

/tmp/foo.o:

%.o: $$(addsuffix /%.c,foo bar) foo.h
        @echo $^
```

在二次展开和目录前缀重建之后，打印的先决条件列表将是 `/tmp/foo/foo.c /tmp/bar/foo.c foo.h`。如果你对这种重建不感兴趣，可以在先决条件列表中使用 `$$*` 代替 `%`。