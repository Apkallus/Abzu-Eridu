# JavaScript 参考

## 表达式和运算符

### 可选链运算符（?.）

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Optional_chaining

可选链运算符 `?.` 用于访问对象的属性或调用函数。如果使用此运算符访问的对象或调用的函数是 `undefined` 或 `null`，则表达式会短路并计算为 `undefined`，而不是抛出错误。

```js
obj.val?.prop
obj.val?.[expr]
obj.func?.(args)
```

### 空值合并运算符（`??`）

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing

空值合并运算符（`??`）是一个逻辑运算符，当左侧的操作数为 `null` 或者 `undefined` 时，返回其右侧操作数，否则返回左侧操作数。

```js
leftExpr ?? rightExpr
```

示例
```js
// 若元素存在，则访问属性，否则为空字符串
document.querySelector('h4')?.outerHTML ?? '';
```
### 展开语法（`...`）

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax

spread (`...`) 语法允许迭代数组或字符串等可迭代字符串在预期有零个或更多参数（用于函数调用）或元素（用于数组字面量）的地方进行扩展。在对象字面量中，扩展语法枚举对象的属性，并将键值对添加到正在创建的对象中。

```js
myFunction(a, ...iterableObj, b)
[1, ...iterableObj, '4', 'five', 6]
{ ...obj, key: 'value' }
```

#### 覆盖属性 —— 应用对象的重名属性中，之前的赋值被之后覆盖

当一个对象被展开到另一个对象中，或多个对象被展开到一个对象中时，如果遇到同名属性，该属性将采用最后赋值的值，同时保留其最初设置的位置。

```js
const obj1 = { foo: "bar", x: 42 };
const obj2 = { foo: "baz", y: 13 };

const mergedObj = { x: 41, ...obj1, ...obj2, y: 9 }; // { x: 42, foo: "baz", y: 9 }
```

### instanceof

`instanceof` 运算符用于检测构造函数的 `prototype` 属性是否出现在某个实例对象的原型链上。其返回值是一个布尔值。可以通过 `Symbol.hasInstance` 来自定义该运算符的行为。

## 语句和声明

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements

- `debugger` 语句
  调用任何可用的调试功能，例如设置断点。如果没有调试功能可用，则此语句不会产生任何效果。

### var —— 声明函数作用域或全局作用域的变量

`var` 语句用于声明一个函数作用域或全局作用域的变量，并且可以选择将其初始化为一个值。

### const —— 声明块作用域的局部变量

`const` 声明用于声明块作用域的局部变量。常量的值不能通过使用赋值运算符重新赋值来更改，但是如果常量是一个对象，它的属性可以被添加、更新或删除。

### let —— 声明可重新赋值的块级作用域局部变量

let 声明用于声明可重新赋值的块级作用域局部变量，并且可以选择将其初始化为一个值。

### function

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/function

function 声明创建一个绑定到给定名称的新函数。

```js
function name(param0) {
  statements
}
function name(param0, param1) {
  statements
}
function name(param0, param1, /* …, */ paramN) {
  statements
}
```

### try...catch

`try...catch` 语句由一个 `try` 块和一个 `catch` 块或 `finally` 块（或两者皆有）组成。首先执行 `try` 块中的代码，如果它抛出异常，则将执行 `catch` 块中的代码。`finally` 块中的代码将在控制流退出整个结构之前始终被执行。

```js
try {
  tryStatements
} catch (exceptionVar) {
  catchStatements
} finally {
  finallyStatements
}
```

### for...of

for...of 语句执行一个循环，该循环处理来自可迭代对象的值序列。

语法：
```js 
for (variable of iterable)
  statement
```

示例：
```js 
const array1 = ["a", "b", "c"];

for (const element of array1) {
  console.log(element);
}

// Expected output: "a"
// Expected output: "b"
// Expected output: "c"
```

### for...in

`for...in` 语句迭代一个对象的**所有**可枚举字符串属性（除 `Symbol` 以外），包括继承的可枚举属性。

```js
for (variable in object)
  statement
```

## 模板字符串

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Template_literals

模板字面量是用反引号（`` ` ``）分隔的字面量，允许多行字符串、带嵌入表达式的字符串插值和一种叫带标签的模板的特殊结构。

模板字面量有时被非正式地叫作模板字符串，因为它们最常被用作字符串插值（通过替换占位符来创建字符串）。然而，带标签的模板字面量可能不会产生字符串——它可以与自定义标签函数一起使用，来对模板字面量的不同部分执行任何操作（常用载荷混淆手段）。

```js
`string text`

`string text line 1
 string text line 2`

`string text ${expression} string text`

tagFunction`string text ${expression} string text`
```

参数
- `string text`
  将成为模板字面量的一部分的字符串文本。几乎允许所有字符，包括换行符和其他空白字符。但是，除非使用了标签函数，否则无效的转义序列将导致语法错误。
- `expression`
  要插入当前位置的表达式，其值被转换为字符串或传递给 tagFunction。
- `tagFunction`
  如果指定，将使用模板字符串数组和替换表达式调用它，返回值将成为模板字面量的值。见`带标签的模板`。


## JavaScript 标准内置对象

### JSON

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/JSON

`JSON` 命名空间对象包含用于解析 [JavaScript 对象表示法]（JSON）和将值转换为 JSON 字符串的静态方法。

#### JSON.parse() —— 解析 JSON 字符串

静态方法 `JSON.parse()` 用来解析 JSON 字符串，构造由字符串描述的 JavaScript 值或对象。可以提供一个可选的 `reviver` 函数，用于在返回结果对象之前对其进行转换。

#### JSON.stringify() —— 构造 JSON 字符串

`JSON.stringify()` 方法将一个 JavaScript 对象或值转换为 JSON 字符串，如果指定了一个 replacer 函数，则可以选择性地替换值，或者指定的 replacer 是数组，则可选择性地仅包含数组指定的属性。

```js
JSON.stringify(value[, replacer [, space]])
```

### Promise

#### Promise.prototype.then()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/then

`Promise` 实例的 `then()` 方法最多接受两个参数：用于 `Promise` 兑现和拒绝情况的回调函数。它立即返回一个等效的 `Promise` 对象，允许你链接到其他 `Promise` 方法，从而实现链式调用。

```js
const promise1 = new Promise((resolve, reject) => {
  resolve("Success!");
});

promise1.then((value) => {
  console.log(value);
  // Expected output: "Success!"
});

```

### Number

**整数转换**

某些操作需要整数作为参数，尤其是那些与数组/字符串索引、日期/时间组件和数字进制相关的操作。在执行上述数值强制转换步骤后，结果将被截断为整数（即舍弃小数部份）。如果数值为 `±Infinity`，则按原样返回。如果数值是 `NaN` 或 `-0`，则返回为 `0`。因此，结果总是整数（不包括 `-0`）或 `±Infinity`。

值得注意的是，当转换到整数时，`undefined` 和 `null` 都会变成 `0`，因为 `undefined` 被转换为 `NaN`，`NaN` 也变成了 `0`。

#### Number() 构造函数

`Number()` 构造函数创建 `Number` 对象。当作为函数调用时，它返回 `Number` 类型的原始值。

```js
new Number(value)
Number(value)
```

示例
```js
// 字符串 "Infinity" 转为 Infinity
>>> Number("Infinity")
<<< Infinity 
```

### Infinity

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Infinity

全局属性 `Infinity` 是一个数值，表示无穷大。

- 是全局对象（global object）的一个属性，即它是一个全局变量。

- 初始值是 `Number.POSITIVE_INFINITY`。`Infinity`（正无穷大）大于任何值。

> ts 的模块 zod 在旧版时 `z.coerce.number()` 对 `"Infinity"` 返回 `Infinity`

### Date

### Date.now()

`Date.now()` 方法返回自 1970 年 1 月 1 日 00:00:00 (UTC) 到当前时间的毫秒数。

```js
var timeInMs = Date.now();
```

### Math

#### Math.sign()

`Math.sign()` 函数返回一个数字的符号，指示数字是正数，负数还是零。

```js
Math.sign(x);
```

此函数共有 5 种返回值，分别是 1, -1, 0, -0, NaN. 代表的各是正数，负数，正零，负零，NaN。

#### Math.cos()

Math.cos() 函数返回一个数值的余弦值。

```js
Math.cos(x)
```

```log
>>> Math.cos(Infinity)
<<< NaN 

>>> Math.cos(NaN)
<<< NaN 
```

#### Math.trunc()

将数字的小数部分去掉，只保留整数部分。

```js
Math.trunc(value)
```

#### Math.random()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Math/random

`Math.random()` 静态方法返回一个大于等于 0 且小于 1 的伪随机浮点数，并在该范围内近似均匀分布，然后你可以缩放到所需的范围。其实现将选择随机数生成算法的初始种子；它不能由用户选择或重置。

> 备注：`Math.random()` **不能**提供密码学安全的随机数。
>
> 工具：[v8_rand_buster](https://github.com/d0nutptr/v8_rand_buster)

```js
Math.random()
```

### eval()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/eval

`eval()` 函数会将传入的字符串当做 JavaScript 代码进行执行。

```js
eval(string)
```

`eval()` 是全局对象的一个函数属性。
> `otherWindow.eval()` 将在同源的其他窗口中执行 JS 代码

### unescape()

计算一个新的字符串，将其中的十六进制转义序列替换为它们所代表的字符（URL 编码）。转义序列可能是由 `escape()` 等函数引入的。

```js
unescape(str)
```

### parseInt()

`parseInt(string, radix)` 解析一个字符串并返回指定基数的十进制整数，`radix` 是 2-36 之间的整数，表示被解析字符串的基数。

### unescape()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/unescape

`unescape()` 函数计算一个新的字符串，将其中的十六进制转义序列替换为它们所代表的字符。转义序列可能是由 `escape()` 等函数引入的。

```js
unescape(str)
```

### decodeURI()

`decodeURI()` 函数能解码由 `encodeURI` 创建或其他流程得到的统一资源标识符（URI）。

> 注意，部分字符不解码。如：`=`

### String

- `String.prototype.split(separator[, limit])`
  接受一个模式，通过搜索模式将字符串分割成一个有序的子串列表，将这些子串放入一个数组，并返回该数组。

#### String.prototype.padStart()

`padStart()` 方法用另一个字符串填充当前字符串（如果需要会重复填充），直到达到给定的长度。填充是从当前字符串的开头开始的。

```js
padStart(targetLength)
padStart(targetLength, padString)
```

参数
- `targetLength`
  当前 str 填充后的长度。如果该值小于或等于 `str.length`，则会直接返回当前 str。
  
- `padString` 可选
  用于填充当前 str 的字符串。如果 `padString` 太长，无法适应 `targetLength`，则会从末尾被截断。默认值为 Unicode“空格”字符（U+0020）。


#### String.prototype.replace()

`replace()` 方法返回一个新字符串，其中一个、多个或所有匹配的 `pattern` 被替换为 `replacement`。

```js
replace(pattern, replacement)
```

参数
- `pattern`
  可以是字符串或者一个带有 `Symbol.replace` 方法的对象，典型的例子就是正则表达式。任何没有 `Symbol.replace` 方法的值都会被强制转换为字符串。

- `replacement`
  可以是字符串或函数。

  - 如果是字符串，它将替换由 `pattern` 匹配的子字符串。支持一些特殊的替换模式，请参阅下面的指定字符串作为替换项部分。

  - 如果是函数，将为每个匹配调用该函数，并将其返回值用作替换文本。下面的指定函数作为替换项部分描述了提供给此函数的参数。

返回值
- 一个新的字符串，其中一个、多个或所有的匹配项都被指定的替换项替换。

**指定字符串作为替换项**
- `$&`
  插入匹配的子字符串。

#### String.prototype.toLowerCase()

`String` 的 `toLowerCase()` 方法将该字符串转换为小写形式。不会影响字符串 str 本身的值。

[规范 22.1.3.28 String.prototype.toLowerCase ( )](https://tc39.es/ecma262/multipage/text-processing.html#sec-string.prototype.tolowercase)：

此方法将 String 值解释为 UTF-16 编码码点的序列，如 [6.1.4](ecmascript-data-types-and-values.html#sec-ecmascript-language-types-string-type) 所述。

调用时执行以下步骤：

1. 令 `thisValue` 为 `this` 值。
2. 执行 ? `RequireObjectCoercible`(`thisValue`)。
3. 令 `string` 为 ? `ToString`(`thisValue`)。
4. 令 `sText` 为 `StringToCodePoints`(`string`)。
5. 令 `lowerText` 为 `toLowercase`(`sText`)，根据 Unicode 默认大小写转换算法。
6. 令 `lowercaseString` 为 `CodePointsToString`(`lowerText`)。
7. 返回 `lowercaseString`。

结果必须根据 Unicode 字符数据库中的区域无关大小写映射推导（这明确不仅包括文件 [`UnicodeData.txt`](https://unicode.org/Public/UCD/latest/ucd/UnicodeData.txt)，还包括随附文件 [`SpecialCasing.txt`](https://unicode.org/Public/UCD/latest/ucd/SpecialCasing.txt) 中的所有区域无关映射）。

> **注意 1**
>
> 某些码点的大小写映射可能产生多个码点。在这种情况下，结果 String 的长度可能与源 String 不同。由于 `toUpperCase` 和 `toLowerCase` 都具有上下文相关行为，这些方法不是对称的。换句话说，`s.toUpperCase().toLowerCase()` 不一定等于 `s.toLowerCase()`。

> **注意 2**
>
> 此方法有意设计为通用的；它不要求其 `this` 值是 String 对象。因此，它可以转移到其他类型的对象上作为方法使用。

#### String.prototype.trim()

`String` 的 `trim()` 方法会从字符串的两端移除空白字符，并返回一个新的字符串，而不会修改原始字符串。

#### String.prototype.indexOf()

`String` 的 `indexOf()` 方法在字符串中搜索指定子字符串，并返回其第一次出现的位置索引。它可以接受一个可选的参数指定搜索的起始位置，如果找到了指定的子字符串，则返回的位置索引大于或等于指定的数字。

```js
indexOf(searchString)
indexOf(searchString, position)
```

#### String.prototype.includes()

执行区分大小写的搜索，以确定是否可以在一个字符串中找到另一个字符串，返回布尔值

```js
includes(searchString)
includes(searchString, position)
```

参数
- `position` 可选
  在字符串中开始搜索 `searchString` 的位置。默认值为 0。

#### String.prototype.match()

`match()` 方法检索字符串与正则表达式进行匹配的结果。

```js
match(regexp)
```

返回值
- 一个 `Array`，其内容取决于全局标志 (`g`) 的存在与否，如果没有找到匹配项，则返回 `null`。

### RegExp 

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/RegExp

对象用于将文本与一个模式匹配。

有两种方法可以创建一个 `RegExp` 对象：
- 字面量，由斜杠 (`/`) 包围而不是引号包围。
- 构造函数，由引号而不是斜杠包围。

```js
// 以下三种表达式都会创建相同的正则表达式：
/ab+c/i; //字面量形式
new RegExp("ab+c", "i"); // 首个参数为字符串模式的构造函数
new RegExp(/ab+c/, "i"); // 首个参数为常规字面量的构造函数
```

### Error

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Error

当运行时错误产生时，`Error` 对象会被抛出。`Error` 对象也可用于用户自定义的异常的基础对象。

实例属性
- `Error.prototype.message`
  错误消息
- `Error.prototype.name`
  错误名称
- `Error.prototype.cause`
  表示导致当前错误被抛出的原因——通常是另一个错误。

### Array

#### Array.prototype.includes()

`includes()` 方法用来判断一个数组是否包含一个指定的值，根据情况，如果包含则返回 `true`，否则返回 `false`。

#### Array.prototype.push()

`push()` 方法将指定的元素添加到数组的末尾，并返回新的数组长度。

```js
push(element0, element1, /* … ,*/ elementN)
```

#### Array.prototype.join()

`join()` 方法将一个数组（或一个类数组对象）的所有元素连接成一个字符串并返回这个字符串，用逗号或指定的分隔符字符串分隔。

```js
join(separator)
```

```js
const a = ["Wind", "Water", "Fire"];
a.join(); // 'Wind,Water,Fire'
a.join(", "); // 'Wind, Water, Fire'
a.join(" + "); // 'Wind + Water + Fire'
a.join(""); // 'WindWaterFire'
```

#### Array.prototype.map()

创建一个新数组，这个新数组由原数组中的每个元素都调用一次提供的函数后的返回值组成。

```js
map(callbackFn, thisArg)
```

#### Array.prototype.shift()

从数组中删除第一个元素，并返回该元素的值。此方法更改数组的长度。

#### Array.prototype.slice()

`slice()` 方法返回一个新的数组对象，这一对象是一个由 `start` 和 `end` 决定的原数组的浅拷贝（包括 `start`，不包括 `end`），其中 `start` 和 `end` 代表了数组元素的索引。原始数组不会被改变。

```js
slice()
slice(start)
slice(start, end)
```

返回值
- 一个含有被提取元素的新数组。

#### Array.prototype.reduce()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/reduce

`reduce()` 方法对数组中的每个元素按序执行一个提供的 `reducer` 回调函数，每一次运行 `reducer` 会将先前元素的计算结果作为参数传入，最后将其结果汇总为单个返回值。
- 即，并非对所有元素应用回调函数。而是计算累计值

第一次执行回调函数时，不存在“上一次的计算结果”。如果需要回调函数从数组索引为 0 的元素开始执行，则需要传递初始值。否则，数组索引为 0 的元素将被用作初始值，迭代器将从第二个元素开始执行（即从索引为 1 而不是 0 的位置开始）。

```js
reduce(callbackFn)
reduce(callbackFn, initialValue)
```

参数
- `callbackFn`
  为数组中每个元素执行的函数。该函数被调用时将传入以下参数：
  - `accumulator`
    上一次调用 `callbackFn` 的结果
  - `currentValue`
    当前元素的值。

返回值
- 使用“reducer”回调函数遍历整个数组后的结果。

### Object

- 🛡️ `Object.freeze()` 防御型静态方法
  使一个对象被冻结。冻结对象可以防止扩展，并使现有的属性不可写入和不可配置。（完全阻止）

- 🛡️ `Object.seal()` 防御型静态方法
  密封一个对象。密封一个对象会阻止其扩展并且使得现有属性不可配置。只要现有属性的值是可写的，它们仍然可以更改。（部分阻止）

- 🛡️ `Object.create()` 防御型静态方法
  以一个现有对象作为原型，创建一个新对象。

#### 🛡️ `Object.defineProperty()` 

`Object.defineProperty()` 静态方法会直接在一个对象上定义一个新属性，或修改其现有属性，并返回此对象。

> 潜在攻击用工具属性的防御型方法

```js
Object.defineProperty(obj, prop, descriptor)
```

参数
- `obj`
    要定义属性的对象。

- `prop`
    一个字符串或 Symbol，指定了要定义或修改的属性键。

- `descriptor`
    要定义或修改的属性的描述符。



#### Object.entries()

返回一个数组，包含给定对象**自有**的可枚举字符串键属性的键值对。

```js
Object.entries(obj)
```

例
```js
// 将对象的名值对格式化为换行符分割的字符串
const res_str = Object.entries(window).map(([key, value]) => `${key}=${value}`).join('\n');
```

#### Object.keys()

`Object.keys()` 静态方法返回一个由给定对象**自身**的可枚举的字符串键属性名组成的数组。

```js
Object.keys(obj)
```


#### `Object.prototype.__lookupGetter__()`

```javascript
Object.prototype.__lookupGetter__(prop)
```

> **已弃用**
> 避免在新项目中使用此特性。TC39 将访问器方法包含在 ECMAScript 规范的附录 B 中，该附录涵盖“具有一个或多个不良特性，并且在不存在遗留用法的情况下将被移除”的 JavaScript 特性。此特性可能成为从 Web 标准或浏览器中移除的候选。

> **备注：** 此特性已弃用，推荐使用 `Object.getOwnPropertyDescriptor()` API。此方法的行为仅为 Web 兼容性而规定，不要求在任何平台上实现。它可能无法在所有环境中工作。

`__lookupGetter__()` 方法返回绑定到指定属性的 getter 函数。

```javascript
__lookupGetter__(prop)
```

参数
- `prop`  
  一个字符串，包含应返回其 getter 的属性名称。

返回值
- 绑定到指定属性的 getter 函数。如果找不到这样的属性，或者该属性是一个 [数据属性]，则返回 `undefined`。

##### 描述

所有继承自 `Object.prototype` 的对象（即除 [null 原型对象] 之外的所有对象）都继承 `__lookupGetter__()` 方法。如果为对象的属性定义了 [getter]，则无法通过该属性引用 getter 函数，因为该属性引用的是该函数的返回值。`__lookupGetter__()` 可用于获取对 getter 函数的引用。

`__lookupGetter__()` 沿 [原型链] 向上查找指定的属性。如果原型链上的任何对象具有指定的 [自有属性]，则返回该属性的 [属性描述符] 的 `get` 属性。如果该属性是数据属性，则返回 `undefined`。如果沿整个原型链都找不到该属性，也会返回 `undefined`。

`__lookupGetter__()` 在规范中被定义为“规范性可选”，这意味着不要求实现此方法。然而，所有主流浏览器都实现了它，并且由于其持续使用，它不太可能被移除。如果浏览器实现了 `__lookupGetter__()`，它还需要实现 `__lookupSetter__()`、`__defineGetter__()` 和 `__defineSetter__()` 方法。

##### 示例

使用 `__lookupGetter__()`

```js
const obj = {
  get foo() {
    return Math.random() > 0.5 ? "foo" : "bar";
  },
};

obj.__lookupGetter__("foo");
// [Function: get foo]
```

###### 以标准方式查找属性的 getter

你应该使用 `Object.getOwnPropertyDescriptor()` API 来查找属性的 getter。与 `__lookupGetter__()` 相比，此方法允许查找 [symbol] 属性。`Object.getOwnPropertyDescriptor()` 方法也适用于 [null 原型对象]，它们不继承自 `Object.prototype`，因此没有 `__lookupGetter__()` 方法。如果 `__lookupGetter__()` 沿原型链向上查找的行为很重要，你可以使用 `Object.getPrototypeOf()` 自行实现。

### Function

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function

#### Function.prototype.call()

`Function` 实例的 `call()` 方法会以给定的 `this` 值和逐个提供的参数调用该函数。

#### Function.prototype.apply()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/apply

`Function` 实例的 `apply()` 方法会以给定的 `this` 值和作为数组（或类数组对象）提供的 `arguments` 调用该函数。

```js
apply(thisArg)
apply(thisArg, argsArray)
```