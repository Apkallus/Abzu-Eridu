指南
- [官网](https://nodejs.org/learn)
    - 拥有到 github 的页面链接
- [github](https://github.com/nodejs/learn)

文档
- [官网](https://nodejs.org/api)
- [github](https://github.com/nodejs/node/tree/main/doc/api)
    - [安全](https://github.com/nodejs/node/blob/main/SECURITY.md)

[版本记录](https://github.com/nodejs/nodejs.org)

## 环境变量

### NODE_OPTIONS —— 以空格分隔的命令行选项列表

https://nodejs.cn/api/cli/node_options_options.html

```sh
NODE_OPTIONS='--require "./my path/file.js"'
```


## --inspect —— 调试代理

https://nodejs.org/learn/getting-started/debugging#command-line-options

```sh
node --inspect server.js
```

Table of contents Index Other versions Options 

## V8

https://nodejs.org/api/v8.html

### v8.writeHeapSnapshot() —— 内存快照

v11.13.0 新增

[内存快照指南](https://nodejs.org/learn/diagnostics/memory/using-heap-snapshot)

```js
v8.writeHeapSnapshot([filename[,options]])
```

参数
- `filename` [`<string>`]：V8 堆快照要保存到的文件路径。如果未指定，将生成文件名模式 `'Heap-${yyyymmdd}-${hhmmss}-${pid}-${thread_id}.heapsnapshot'`，其中 `{pid}` 是 Node.js 进程的 PID，当从主 Node.js 线程调用 `writeHeapSnapshot()` 时 `{thread_id}` 为 `0`，否则为工作线程的 id。
- `options` [`<Object>`]
  - `exposeInternals` [`<boolean>`]：如果为 true，则在堆快照中暴露内部对象。**默认值：** `false`。
  - `exposeNumericValues` [`<boolean>`]：如果为 true，则在人造字段中暴露数值。**默认值：** `false`。
- 返回：[`<string>`]：保存快照的文件名。

生成当前 V8 堆的快照，并将其写入 JSON 文件。该文件旨在与 Chrome DevTools 等工具配合使用。JSON schema 未文档化，且特定于 V8 引擎，可能随 V8 版本变化。

堆快照特定于单个 V8 isolate。使用[工作线程](https://nodejs.org/api/worker_threads.html)时，从主线程生成的堆快照不会包含任何工作线程的信息，反之亦然。

创建堆快照所需内存约为创建快照时堆大小的两倍。这会导致 OOM killer 终止进程的风险。

生成快照是同步操作，会阻塞事件循环，阻塞时长取决于堆大小。

示例

- **ESM（`.mjs`）**：

  ```mjs
  import { writeHeapSnapshot } from 'node:v8';
  import { Worker, isMainThread, parentPort } from 'node:worker_threads';
  import { fileURLToPath } from 'node:url';

  if (isMainThread) {
    const __filename = fileURLToPath(import.meta.url);
    const worker = new Worker(__filename);

    worker.once('message', (filename) => {
      console.log(`worker heapdump: ${filename}`);
      // 现在获取主线程的堆转储。
      console.log(`main thread heapdump: ${writeHeapSnapshot()}`);
    });

    // 告诉工作线程创建堆转储。
    worker.postMessage('heapdump');
  } else {
    parentPort.once('message', (message) => {
      if (message === 'heapdump') {
        // 为工作线程生成堆转储
        // 并将文件名返回给父线程。
        parentPort.postMessage(writeHeapSnapshot());
      }
    });
  }
  ```

- **CommonJS（`.cjs`）**：

  ```cjs
  const { writeHeapSnapshot } = require('node:v8');
  const { Worker, isMainThread, parentPort } = require('node:worker_threads');

  if (isMainThread) {
    const worker = new Worker(__filename);

    worker.once('message', (filename) => {
      console.log(`worker heapdump: ${filename}`);
      // 现在获取主线程的堆转储。
      console.log(`main thread heapdump: ${writeHeapSnapshot()}`);
    });

    // 告诉工作线程创建堆转储。
    worker.postMessage('heapdump');
  } else {
    parentPort.once('message', (message) => {
      if (message === 'heapdump') {
        // 为工作线程生成堆转储
        // 并将文件名返回给父线程。
        parentPort.postMessage(writeHeapSnapshot());
      }
    });
  }
  ```

## Modules: CommonJS modules

https://nodejs.org/api/modules.html

### The module scope

#### require(id)

- `id` `<string>` 模块名称或路径
- 返回值：`<any>` 导出的模块内容

用于导入模块、`JSON` 和本地文件。可以从 `node_modules` 导入模块。可以使用相对路径（例如 `./`、`./foo`、`./bar/baz`、`../foo`）导入本地模块和 JSON 文件，这些路径将相对于 `__dirname`（如果已定义）命名的目录或当前工作目录进行解析。POSIX 风格的相对路径以独立于操作系统的方式解析，这意味着上述示例在 Windows 上的工作方式与在 Unix 系统上相同。

```js
// Importing a local module with a path relative to the `__dirname` or current
// working directory. (On Windows, this would resolve to .\path\myLocalModule.)
const myLocalModule = require('./path/myLocalModule');

// Importing a JSON file:
const jsonData = require('./path/filename.json');

// Importing a module from node_modules or Node.js built-in module:
const crypto = require('node:crypto');
```

## Events

https://nodejs.org/api/events.html

### Class: EventEmitter

#### `emitter.on(eventName, listener)`

- `eventName` `<string>` | `<symbol>` 事件名称。
- `listener` `<Function>` 回调函数
- 返回值：`<EventEmitter>`

将 `listener` 函数添加到名为 `eventName` 的事件的监听器数组末尾。不会检查 `listener` 是否已被添加。多次调用并传入相同的 `eventName` 和 `listener` 组合将导致 `listener` 被多次添加和调用。

```js
server.on('connection', (stream) => {
  console.log('someone connected!');
});
```

返回对 `EventEmitter` 的引用，以便调用可以链式进行。

默认情况下，事件监听器按其添加顺序调用。`emitter.prependListener()` 方法可用作将事件监听器添加到监听器数组开头的替代方法。

## HTTP

### Class: http.ServerResponse

#### Event: `'finish'`

添加于：v0.3.6

当响应已发送时触发。更具体地说，当响应标头和主体的最后一段已交给操作系统以通过网络传输时，会触发此事件。这并不意味着客户端已经收到了任何内容。

#### response.getHeaders()

- 返回值：`<Object>`

返回当前传出标头的浅拷贝。由于使用的是浅拷贝，数组值可以被修改，而无需额外调用各种与标头相关的 http 模块方法。返回对象的键是标头名称，值是相应的标头值。所有标头名称均为小写。

`response.getHeaders()` 方法返回的对象*不*原型继承自 JavaScript `Object`。这意味着诸如 `obj.toString()`、`obj.hasOwnProperty()` 等典型的 `Object` 方法未定义，并且*不会工作*。

```js
response.setHeader('Foo', 'bar');
response.setHeader('Set-Cookie', ['foo=bar', 'bar=baz']);

const headers = response.getHeaders();
// headers === { foo: 'bar', 'set-cookie': ['foo=bar', 'bar=baz'] }
```

#### `response.statusCode`

- 类型：`<number>` **默认值：** `200`

当使用隐式标头（未显式调用 `response.writeHead()`）时，此属性控制标头被刷新时发送给客户端的状态码。

```js
response.statusCode = 404;
```

响应标头发送给客户端后，此属性表示已发送的状态码。

#### `response.statusMessage`

- 类型：`<string>`

当使用隐式标头（未显式调用 `response.writeHead()`）时，此属性控制标头被刷新时发送给客户端的状态消息。如果将其保留为 `undefined`，则将使用状态码的标准消息。

```js
response.statusMessage = 'Not found';
```

响应标头发送给客户端后，此属性表示已发送的状态消息。