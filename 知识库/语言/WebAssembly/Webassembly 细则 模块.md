https://webassembly.github.io/spec/core/syntax/modules.html

# 模块

WebAssembly 程序被组织为*模块*，模块是部署、加载和编译的单位。模块收集类型、标签和全局变量、内存、表、函数的定义。此外，它可以声明导入和导出，并以数据段和元素段或启动函数的形式提供初始化。

```
module ::= module
  list(type)
  list(import)
  list(tag)
  list(global)
  list(mem)
  list(table)
  list(func)
  list(data)
  list(elem)
  start?
  list(export)
```

每个列表——因此整个模块——都可以为空。

## 索引

定义通过从零开始的*索引*来引用。每一类定义都有自己的*索引空间*，由以下类别区分。

```text
idx ::= u32
typeidx ::= idx
funcidx ::= idx
globalidx ::= idx
tableidx ::= idx
memidx ::= idx
tagidx ::= idx
elemidx ::= idx
dataidx ::= idx
labelidx ::= idx
localidx ::= idx
fieldidx ::= idx
```

标签、全局变量、内存、表和函数的索引空间包括在同一模块中声明的相应导入。这些导入的索引位于同一索引空间中其他定义的索引之前。

数据索引引用数据段，元素索引引用元素段。

局部变量的索引空间只能在函数内部访问，并包括该函数的参数，这些参数位于局部变量之前。

标签索引引用指令序列中的结构化控制指令。

每个聚合类型为其字段提供一个索引空间。

### 约定

- 元变量 `l` 取值范围为标签索引。
- 元变量 `x`、`y` 取值范围为其他任何索引空间中的索引。
- 对于每个索引空间 `abcidx`，记号 `abcidx(A)` 表示该索引空间中在 `A` 中自由出现的索引集合。有时这个集合被重新解释为其元素的列表。

> **注意**
>
> 例如，如果 `instr*` 是 `(data.drop 1) (memory.init 2 3)`，那么 `dataidx_instrs(instr*) = 1 3`，或者等价地，集合 `{ 1, 3 }`。

## 类型

模块的 `type` 节定义递归类型的列表，每个递归类型由一系列子类型组成，这些子类型由各自的类型索引引用。模块中使用的所有函数、结构体或数组类型都必须在此节中定义。

```text
type ::= type rectype
```

## 标签

模块的 `tag` 节定义*标签*列表：

```text
tag ::= tag tagtype
```

标签的类型索引必须引用声明其标签类型的函数类型。

标签通过标签索引引用，从第一个不引用标签导入的最小索引开始。

## 全局变量

模块的 `global` 节定义*全局变量*（简称*全局变量*）列表：

```text
global ::= global globaltype expr
```

每个全局变量存储一个由全局类型指定类型的值。它还指定全局变量是不可变的还是可变的。此外，每个全局变量使用常量初始化表达式给定的值进行初始化。

全局变量通过全局索引引用，从第一个不引用全局变量导入的最小索引开始。

## 内存

模块的 `mem` 节定义*线性内存*（简称*内存*）列表，由它们的内存类型描述：

```text
mem ::= memory memtype
```

内存是原始未解释字节的列表。其内存类型的限制中的最小大小指定该内存的初始大小，而最大值（如果存在）限制其后续可以增长到的大小。两者都以页大小为单位。

内存可以通过数据段初始化。

内存通过内存索引引用，从第一个不引用内存导入的最小索引开始。大多数构造隐式引用内存索引 `0`。

## 表

模块的 `table` 节定义*表*列表，由它们的表类型描述：

```text
table ::= table tabletype expr
```

表是特定引用类型的不透明值的数组，该引用类型由表类型指定。每个表槽使用常量初始化表达式给定的值进行初始化。表还可以通过元素段进一步初始化。

表类型的限制中的最小大小指定该表的初始大小，而最大值限制其后续可以增长到的大小。

表通过表索引引用，从第一个不引用表导入的最小索引开始。大多数构造隐式引用表索引 `0`。

## 函数

模块的 `func` 节定义*函数*列表，结构如下：

```text
func ::= func typeidx local* expr
local ::= local valtype
```

函数的类型索引通过引用模块中定义的函数类型来声明其签名。函数的参数通过函数体中的从 0 开始的局部索引引用；它们是可变的。

局部变量声明可变局部变量及其类型的列表。这些变量通过函数体中的局部索引引用。第一个局部变量的索引是不引用参数的最小索引。

函数的表达式是表示函数体的指令序列。终止时，它必须产生与函数类型的结果类型匹配的栈。

函数通过函数索引引用，从第一个不引用函数导入的最小索引开始。

## 数据段

模块的 `data` 节定义*数据段*列表，可用于从静态字节列表初始化内存范围。

```text
data ::= data byte* datamode
datamode ::= active memidx expr | passive
```

与元素段类似，数据段有一个模式，将其标识为*主动*或*被动*。被动数据段的内容可以使用 `memory.init` 指令复制到内存中。主动数据段在实例化期间将其内容复制到内存中，由内存索引和定义该内存中偏移量的常量表达式指定。

数据段通过数据索引引用。

## 元素段

模块的 `elem` 节定义*元素段*列表，可用于从静态元素列表初始化表的子范围。

```text
elem ::= elem reftype expr* elemmode
elemmode ::= active tableidx expr | passive | declare
```

每个元素段定义一个引用类型和相应的常量元素表达式列表。

元素段有一个模式，将其标识为*主动*、*被动*或*声明性*。被动元素段的元素可以使用 `table.init` 指令复制到表中。主动元素段在实例化期间将其元素复制到表中，由表索引和定义该表中偏移量的常量表达式指定。声明性元素段在运行时不可用，仅用于前向声明在代码中使用 `ref.func` 等指令形成的引用。偏移量由另一个常量表达式给出。

元素段通过元素索引引用。

## 启动函数

模块的 `start` 节声明*启动函数*的函数索引，该函数在模块实例化时、表和内存初始化后自动调用。

```text
start ::= start funcidx
```

> **注意**
>
> 启动函数用于初始化模块的状态。在此初始化完成之前，模块及其导出无法从外部访问。

## 导入

模块的 `import` 节定义实例化所需的一组*导入*。

```text
import ::= import name name externtype
```

每个导入由两级名称空间标记，包括*模块名*和该模块内实体的*项目名*。可导入的定义是标签、全局变量、内存、表和函数。每个导入由各自的外部类型指定，实例化期间提供的定义必须与之匹配。

每个导入在相应的索引空间中定义一个索引。在每个索引空间中，导入的索引位于模块本身包含的任何定义的第一个索引之前。

> **注意**
>
> 与导出名称不同，导入名称不一定是唯一的。可以多次导入相同的模块/项目名称对；此类导入甚至可以具有不同的类型描述，包括不同种类的实体。具有此类导入的模块仍然可以实例化，具体取决于嵌入器允许解析和提供导入的方式。但是，嵌入器不需要支持这种重载，并且 WebAssembly 模块本身不能实现重载名称。

## 导出

模块的 `export` 节定义一组*导出*，一旦模块被实例化，这些导出就可以被宿主环境访问。

```text
export ::= export name externidx
externidx ::= func funcidx | global globalidx | table tableidx | memory memidx | tag tagidx
```

每个导出由唯一名称标记。可导出的定义是标签、全局变量、内存、表和函数，它们通过各自的索引引用。

### 约定

以下辅助记号定义为用于导出序列，按保持顺序的方式过滤出特定种类的索引：

```text
funcs(ϵ) = ϵ
funcs((func x) xx*) = x funcs(xx*)
funcs(externidx xx*) = funcs(xx*)   否则

tables(ϵ) = ϵ
tables((table x) xx*) = x tables(xx*)
tables(externidx xx*) = tables(xx*)   否则

mems(ϵ) = ϵ
mems((memory x) xx*) = x mems(xx*)
mems(externidx xx*) = mems(xx*)   否则

globals(ϵ) = ϵ
globals((global x) xx*) = x globals(xx*)
globals(externidx xx*) = globals(xx*)   否则

tags(ϵ) = ϵ
tags((tag x) xx*) = x tags(xx*)
tags(externidx xx*) = tags(xx*)   否则
```