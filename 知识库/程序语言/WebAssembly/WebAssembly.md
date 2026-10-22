[导航](https://webassembly.org/specs/)
- [规范](https://webassembly.github.io/spec/core/)
    - [速查表](https://webassembly.github.io/spec/core/appendix/index-rules.html)
- [JS 接口](https://webassembly.github.io/spec/js-api/index.html)

[MDN](https://developer.mozilla.org/en-US/docs/WebAssembly)
- [WAT 文本格式指南](https://developer.mozilla.org/zh-CN/docs/WebAssembly/Guides/Understanding_the_text_format)

[文本 <=> 二进制转换](https://webassembly.github.io/wabt/demo/)

## 指南
### 理解 WebAssembly 文本格式

WebAssembly 代码中的基本单元是一个模块。

在文本格式中，一个模块被表示为树的文本格式。因此，我们可以把一个模块想象为一棵由描述了模块结构和代码的节点组成的树。

树上的每个一个节点都有一对括号 `(` ... `)` 包围。括号内的第一个标签为该节点的类型，其后跟随的是由空格分隔的属性或孩子节点列表。

```wasm
;; 根节点为“模块（module）”的树，该树有两个孩子节点
;;; 属性为 1 的“内存（memory）”节点
;;; 一个“函数（func）”节点
(module 
    (memory 1) 
    (func)
)

;; 空模块
(module)
```

WebAssembly 模块中的所有代码都是划分到函数里面。函数具有下列的伪代码结构：

```wasm
( func <signature> <locals> <body> )
```
- 签名 
    声明函数需要的参数以及函数的返回值。
- 局部变量 
    像 JavaScript 中的变量，但是显式的声明了类型。
- 函数体 
    是一个低级指令的线性列表。

#### 签名和参数

签名是由一系列参数类型声明，及其后面的返回值类型声明列表组成。

参数格式为 `(param <类型>)`，返回值格式为 `(result <类型>)`。

```wasm
;; 接受两个 32 位整数，返回一个 64 位浮点数的函数
(func (param i32) (param i32) (result f64) ... )
```

在签名的后面是带有类型的局部变量，格式为 `(local <类型>)`。函数调用可以通过参数实参值对局部变量进行初始化。

#### 获取和设置局部变量和参数

局部变量和参数能够被函数体使用 `local.get` 和 `local.set` 指令进行读写。指向将被存取的条目的方式：

- 使用数字索引：按照它们的声明顺序，参数在前，局部变量在后。

    ```wasm
    (func (param i32) (param f32) (local f64)
    local.get 0
    local.get 1
    local.get 2)
    ```

- 使用别名：在类型声明的前面添加一个使用美元符号`$`作为前缀的名字。

    ```wasm
    (func (param $p1 i32) (param $p2 f32) (local $loc i32) …)
    ```

函数的区分使用相同方式

#### 栈式机器

虽然浏览器把 wasm 编译为某种更高效的东西，但是，wasm 的执行是以栈式机器定义的。也就是说，其基本理念是每种类型的指令都是在栈上执行数值的入栈出栈操作。

例如，`local.get` 被定义为把它读到的局部变量值压入到栈上，然后 `i32.add` 从栈上取出两个 `i32` 类型值（它的含义是把前面压入栈上的两个值取出来）计算它们的和（以 2^32 求模），最后把结果压入栈上。

当函数被调用的时候，它是从一个空栈开始的。随着函数体指令的执行，栈会逐步填满和清空。

```wasm
(func (param $lhs i32) (param $rhs i32) (result i32)
  local.get $lhs  ;; 读取参数 $lhs，并压栈
  local.get $rhs  ;; 读取参数 $rhs，并压栈
  i32.add       ;; 弹出栈中的两个值，读取并相加 $rhs + $lhs，最后压栈
  ;; 此时栈仅存一个值 $rhs + $lhs
)
```

#### 调用函数

wasm 函数必须通过模块里面的 `export` 语句显式地导出。

函数同样适用于索引与命名。命名时在关键字 `func` 的后面增加一个美元符号开头的名字：

```wasm
(func $add … )
```

增加一个导出声明：

```wasm
(export "add" (func $add))
```

当前示例模块

```wasm
(module
    (func $add (param $lhs i32) (param $rhs i32) (result i32)
        local.get $lhs
        local.get $rhs
        i32.add
    )
    (export "add" (func $add))
)
```

当前示例模块已可被转换为 `.wasm` 二进制文件，并在浏览器中调用
1. [文本转二进制](https://webassembly.github.io/wabt/demo/wat2wasm/index.html)，将其转换为名叫 `test.wasm` 的二进制文件。

- 直接使用 `wat2wasm demo` 内的演示功能

    ```js
    const wasmInstance = new WebAssembly.Instance(wasmModule, {});

    console.log(wasmInstance.exports.add(7, 2));
    ```

- 或运行本地服务器，从 URL 加载
    ```sh
    python -m http.server 9999 
    ```
    - 在浏览器控制台中编译并实例化示例模块
        ```js
        WebAssembly.instantiateStreaming(fetch("test.wasm")).then((obj) => {
            console.log(obj.instance.exports.add(1, 2)); // "3"
        });
        ```

#### 探索基本原则

##### 在同一模块里的函数调用其他函数成员

为函数给定一个索引或名字，使用 `call` 指令以调用它。

```wasm
(module
    (func $getAnswer (result i32)
        i32.const 42 ;; 压栈 42
    )
    (func (export "getAnswerPlus1") (result i32)
        call $getAnswer ;; 调用函数 $getAnswer
        i32.const 1 ;; 压栈 1
        i32.add ;; 弹出两个操作数后相加 1+42
    )
)
```

## 参考

### WebAssembly

#### WebAssembly.Instance

https://developer.mozilla.org/zh-CN/docs/WebAssembly/Reference/JavaScript_interface/Instance

`WebAssembly.Instance` 对象是 `WebAssembly.Module` 的一个有状态、可执行的实例。`Instance` 对象包含所有的、允许从 JavaScript 调用 WebAssembly 代码的导出的 WebAssembly 函数。

##### WebAssembly.Instance() 构造函数

`WebAssembly.Instance()` 构造函数创建一个新的 `Instance` 对象，该对象是 `WebAssembly.Module` 的有状态、可执行的实例。

```js
new WebAssembly.Instance(module, importObject)
```

##### WebAssembly.Instance.prototype.exports

`WebAssembly.Instance` 对象原型的 `exports` 只读属性返回一个对象，该对象将从 WebAssembly 模块实例中导出的所有函数作为其成员，让 JavaScript 能访问和使用这些函数。

#### WebAssembly.instantiateStreaming()

https://developer.mozilla.org/zh-CN/docs/WebAssembly/Reference/JavaScript_interface/instantiateStreaming_static

`WebAssembly.instantiateStreaming()` 静态方法直接从流式底层源编译并实例化 WebAssembly 模块。

```js
WebAssembly.instantiateStreaming(source)
WebAssembly.instantiateStreaming(source, importObject)
WebAssembly.instantiateStreaming(source, importObject, compileOptions)
```

返回值，兑现为含两个字段的 `ResultObject` 的 `Promise`：
- `module`
    表示已编译的 WebAssembly 模块的 `WebAssembly.Module` 对象。该 `Module` 能够再次被实例化或通过 `postMessage()` 共享。
- `instance`
    包含所有导出的 WebAssembly 函数的 `WebAssembly.Instance` 对象。

### WebAssembly definitions

#### data：Wasm 定义

`data` 定义用于定义一段可复制到线性内存中的字节。

```text
;; 主动形式，在实例化时写入内存
data name memory_identifier offset data_string

;; 被动形式，稍后通过 memory.init 写入
data name data_string
```

- `data`
    `data` 定义类型。必须始终放在最前面。
- `name`（可选）
    数据可选的标识名称。必须以 `$` 符号开头，例如 `$my_data`。如果省略，则可以通过索引来标识 `data`（例如调用 `memory.init` 时），例如 wasm 模块中第一个 `data` 的索引为 `0`，第二个为 `1`，依此类推。
- `memory_identifier`（可选）
    表示要将数据放入的 `memory` 实例的标识符，必须前置 `memory` 关键字才能被解释为 `memory_identifier`。该标识符可以是以下之一：

    - `name`
    首次定义 `memory` 时为其设置的标识名称。必须以 `$` 符号开头，并前置 `memory` 关键字，例如 `(memory $my_memory)`。
    - `index`
    表示内存索引号的 `i32` 值，例如 `(memory 0)` 表示模块中的第一个内存，`(memory 1)` 表示第二个，依此类推。

    > **注意**
    >
    > 编写主动形式的 `data` 定义时，必须包含 `offset`，但 `memory_identifier` 可以省略，此时默认为 `(memory 0)`。

- `offset`（可选）
    表示开始将数据写入 `memory` 的偏移量。该值可以是任何常量表达式，意味着它可以包含算术表达式以及数值等结构。

    s完整语法在值前包含 `offset` 关键字，例如 `(offset i32.const 0)`，不过在缩写形式中可以省略该关键字，例如 `(i32.const 0)`。

- `data_string`
    定义此 `data` 实例所表示数据的字面量字节字符串。

### WebAssembly memory instructions —— 内存指令

https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/Memory

#### load：Wasm 内存指令

弹栈并作为指针，从内存中加载一个数字压栈。

有用于从内存加载到 `i32`、`i64`、`f32` 和 `f64` 的 `load` 指令。对于整数，有单独的指令变体，用于从内存加载较窄的有符号数和无符号数，并将其扩展为更宽的类型。例如，可以使用 `i32.load8_u` 加载一个无符号 8 位数字并将其转换为 `i32`。

#### store：Wasm 内存指令

弹栈后依次得到数字与指针，将数字存储到指针所指的内存中（若支持多内存，则可设置特定内存）。即，消耗两个内存槽位

有用于将 `i32`、`i64`、`f32` 和 `f64` 存储到内存中的 `store` 指令。对于整数，有单独的指令变体，用于将宽类型的数字存储到内存中更窄的位置。例如，可以使用 `i32.store8` 将一个 32 位数字存储到内存中的 8 位槽位中。如果该数字无法放入更窄的数字类型，它将发生回绕。

### WebAssembly variable instructions

https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/Variables

#### local.get: Wasm 变量指令

将局部变量的值加载到栈上。

```wasm
;; load the value of a local variable onto the stack
local.get $val
```

#### local.set: Wasm 变量指令

设置局部变量的值。

```wasm
;; load the number 2 onto the stack
i32.const 2

;; store the number 2 in the variable $val
local.set $val
```

#### local.tee

`local.tee` 指令用于设置局部变量的值，并将该值加载到栈上。（即，弹栈一个值设置局部变量，并将其压栈。相当于不消耗栈槽位以设置局部变量）

该指令的名称来源于管道工程中使用的 T 型分流器。


### WebAssembly control flow instructions —— 控制流指令

https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/Control_flow

#### call：Wasm 文本指令

`call` 调用一个函数，`return_call` 则是其尾调用版本。`call_indirect` 调用一个表中的一个函数，`return_call_indirect` 则是其尾调用版本。

[细则](https://webassembly.github.io/spec/core/bikeshed/#function-calls%E2%91%A0)
- 使用类栈型函数传递，主调函数将参数压栈，被调函数自动弹栈并获取参数

#### if...else：Wasm 文本指令

`if` 语句在栈顶项为真（非零）时执行一条语句。当条件为假（0）时，执行另一条语句。

要想在栈上保留返回值，添加 `result` 语句。

```wasm
i32.const 0
(if (result i32)
  (then
    ;; 做点什么
    (i32.const 1)
  )
  (else
    ;; 做点其他的
    (i32.const 2)
  )
)
(drop)
```

#### loop：Wasm 文本指令

`loop` 语句创建一个标签，后面可以用 `br` 进行跳转。`loop` 指令自身并不会执行循环，你需要通过跳转到循环标签真正地创建循环。

`loop` 语句和 `block` 语句的表现相反，跳转到 `loop` 会回到循环的开头，而跳转到 `block` 会达到块尾，也就是跳出块。

```wasm
;; 对循环设置标签，使其可以被跳转
(loop $my_loop

  ;; 跳转到该循环
  ;; 大多数时候，你会想要将下面的指令放在 if 语句中，仅在符合条件时跳转，
  ;; 否则，会进入无限循环
  br $my_loop

)
```

#### block：Wasm 文本指令

创建一个标签，后面可以用 `br` 跳出该块。

`loop` 语句和 `block` 语句的表现相反，跳转到 `loop` 会回到循环的开头，而跳转到 `block` 会达到块尾，也就是跳出块。

#### br_if：Wasm 文本指令

基于布尔条件（`0` 或 `1`）分支到 `loop`、`block` 或 `if` 语句。

```wasm
;; Label the loop to enable branching to it later
(loop $my_loop

  ;; Add 1 (true) to the stack
  i32.const 1

  ;; Branch to the loop if the top of the stack is 1
  br_if $my_loop

)
```

#### end：Wasm 文本指令

`end` 用于终止 `block`、`loop`、`if` 或 `else`。在其他示例中，我们使用的是不需要 `end` 的 s 表达式，因此你不会在哪些示例中找到它。然而，浏览器的开发者工具将显示。

```wasm
i32.const 0
if
  ;; 做点什么
end
```

### WebAssembly numeric instructions

https://developer.mozilla.org/en-US/docs/WebAssembly/Reference/Numeric

#### eqz

The eqz numeric instruction checks if a number is equal to zero.

#### ne: Wasm numeric instruction

The ne numeric instruction, short for not equal, checks if two numbers are not equal.

#### sub: Wasm numeric instruction

`栈顶2` - `栈顶1`