[github](https://github.com/mde/ejs) 
[官网](https://ejs.co/)


# 嵌入式 JavaScript 模板

## 安全性

安全专业人员在报告任何安全问题之前，请参阅本项目的 [SECURITY.md]，特别是以下内容：“EJS 实际上是一个 JavaScript 运行时。它的核心工作就是执行 JavaScript。如果您在调用 EJS 渲染方法时未自行检查输入，则需对结果负责。”

简而言之，请勿提交包含以下代码片段的“漏洞”：

```javascript
app.get('/', (req, res) => {
  res.render('index', req.query);
});
```

## 安装

```bash
$ npm install ejs
```

## 导入或引用

同时支持 CommonJS 和 ES Modules。

```javascript
import ejs from 'ejs';
// 或者
const ejs = require('ejs');
```

## 兼容性

-   服务端
    CommonJS 方式（`require`）至少支持 Node v0.12，可能也支持更早版本。ES Modules 方式（`import`）需要支持 ESM 的 Node 版本。
-   CLI
    需要 Node v8 或更高版本。
-   浏览器
    EJS 支持所有现代浏览器，并且极有可能在非常旧的浏览器中运行。实际效果可能因环境而异。
-   打包工具与替代运行时
    自 v6.0 起，发布的包可在 Rollup、Rolldown、tsdown、esbuild、Webpack、Vite、Browserify、Bun 和 Deno 下正常导入。早期版本在 ESM 源码内部通过 `module.exports = ejs;` 作为双模式垫片；现代 ESM 感知打包工具和 Bun 将其视为格式错误的 ESM。该垫片已从 `lib/esm/*.js` 中移除，并移至 `lib/cjs/*` 编译步骤中，因此发布的 CJS 接口（`require('ejs')`）保持不变。对于 Browserify，请传递 `--node` 参数，使其选择 `main` 入口而非 `browser` 字段指向的预构建 UMD 包。
-   浏览器端打包工具
    支持条件导出的浏览器端打包工具会通过 `browser` 导出条件选择预构建包。使用此包可编译和渲染模板字符串；若需使用 `renderFile` 从文件系统加载模板，则需要 Node 入口点。

## 特性

-   控制流
    使用 `<% %>`
-   转义输出
    使用 `<%= %>`（转义函数可配置）
-   非转义原始输出
    使用 `<%- %>`
-   换行修剪模式
    使用 `-%>` 结束标签（“换行吞噬”）
-   空白修剪模式
    使用 `<%_ _%>` 处理控制流（吞噬所有空白）
-   自定义分隔符
    例如使用 `[? ?]` 代替 `<% %>`
-   包含文件
    支持 Includes
-   客户端支持
    支持在浏览器端运行
-   静态缓存
    支持中间 JavaScript 函数的静态缓存
-   模板缓存
    支持模板的静态缓存
-   Express 兼容
    符合 [Express] 视图系统规范

## 示例

```ejs
<% if (user) { %>
  <h2><%= user.name %></h2>
<% } %>
```

## 基本用法

```javascript
const template = ejs.compile(str, options);
template(data);
// => 渲染后的 HTML 字符串

ejs.render(str, data, options);
// => 渲染后的 HTML 字符串

ejs.renderFile(filename, data, options, function(err, str){
    // str => 渲染后的 HTML 字符串
});
```

> **重要提示**
> 绝不应给予最终用户不受限制的 EJS 渲染方法访问权限。如果这样做，说明您正在以本质上不安全的方式使用 EJS。


## 标签

-   `<%`
    “脚本”标签，用于控制流，无输出。
-   `<%_`
    “空白吞噬”脚本标签，剥离其前面的所有空白。
-   `<%=`
    将值输出到模板中（已转义）。
-   `<%-`
    将未转义的值输出到模板中。 🎯
-   `<%#`
    注释标签，不执行，无输出。
-   `<%%`
    输出字面量 `<%`。
-   `%%>`
    输出字面量 `%>`。
-   `%>`
    普通结束标签。
-   `-%>`
    修剪模式（“换行吞噬”）标签，修剪随后的换行符。
-   `_%>`
    “空白吞噬”结束标签，移除其后面的所有空白。

## 转义与输出上下文

EJS 最常用于生成 HTML。`<%= %>` 反映了这一点，它对 HTML 内容和带引号的属性值进行转义。

EJS 也会为其他上下文生成任意字符串，但它并不知道输出最终会出现在哪里。您可以替换默认的转义函数。在 HTML 内容之外，您应该这样做。

```javascript
ejs.render(template, data, {escape: myEscapeFunction});
```

`escape` 必须放在 options 参数中。不能在全局 `ejs` 上设置，也不能随数据一起传入。对于混合上下文的模板，请使用 `<%- myEscapeFunction(name) %>` 对每个值单独转义。

常见的错误是在 `<script>` 块内使用 `<%= %>`。浏览器在那里不会解码 HTML 实体，因此默认转义既无法正确渲染也无法提供保护。请通过属性传递值并使用 `JSON.parse` 解析，而不是将其拼接到 JavaScript 源码中。（`JSON.stringify` 的输出在那里也不安全。数据中的任何 `</script>` 都会提前结束代码块。）

## 包含文件（Includes）

Include 必须是绝对路径，如果不是，则假定相对于调用 `include` 的模板。例如，如果从 `./views/users.ejs` 中包含 `./views/user/show.ejs`，应使用 `<%- include('user/show') %>`。

除非使用 `renderFile()`，否则必须为带有 `include` 调用的模板指定 `filename` 选项。

您可能希望使用原始输出标签（`<%-`）来引入 include，以避免对 HTML 输出进行双重转义。

```ejs
<ul>
  <% users.forEach(function(user){ %>
    <%- include('user/show', {user: user}) %>
  <% }); %>
</ul>
```

Include 在运行时插入，因此您可以在 `include` 调用中使用变量作为路径（例如 `<%- include(somePath) %>`）。顶层数据对象中的变量对所有 include 可用，但局部变量需要向下传递。

> **注意**
> Include 预处理指令（`<% include user/show %>`）在 v3.0+ 中不再受支持。

## 自定义分隔符

自定义分隔符可以按模板应用，也可以全局应用：

```javascript
import ejs from 'ejs';
const users = ['geddy', 'neil', 'alex'];

// 仅针对单个模板
ejs.render('<p>[?= users.join(" | "); ?]</p>', {users: users}, {delimiter: '?', openDelimiter: '[', closeDelimiter: ']'});
// => '<p>geddy | neil | alex</p>'

// 或者全局设置
ejs.delimiter = '?';
ejs.openDelimiter = '[';
ejs.closeDelimiter = ']';
ejs.render('<p>[?= users.join(" | "); ?]</p>', {users: users});
// => '<p>geddy | neil | alex</p>'
```

## 缓存

EJS 自带基本的进程内缓存，用于缓存渲染模板所用的中间 JavaScript 函数。使用 Node 的 [`lru-cache`] 库可以轻松接入 LRU 缓存：

```javascript
import ejs from 'ejs';
import { LRUCache } from 'lru-cache';
ejs.cache = LRUCache({max: 100}); // 限制为 100 项的 LRU 缓存
```

如需清除 EJS 缓存，请调用 [`ejs.clearCache()`]。如果使用 LRU 缓存且需要不同的限制，只需将 `ejs.cache` 重置为新的 LRU 实例即可。

## 自定义文件加载器

默认文件加载器为 `fs.readFileSync`。如需自定义，可设置 [`ejs.fileLoader`]。

```javascript
import ejs from 'ejs';
const myFileLoad = function (filePath) {
  return 'myFileLoad: ' + fs.readFileSync(filePath);
};
ejs.fileLoader = myFileLoad;
```

通过此功能，您可以在读取模板前对其进行预处理。

## 布局

EJS 本身不支持块（blocks），但可以通过包含页眉和页脚来实现布局，如下所示：

```ejs
<%- include('header') -%>
<h1>
  Title
</h1>
<p>
  My page
</p>
<%- include('footer') -%>
```

## 客户端支持

前往 [Latest Release] 下载 `./ejs.js` 或 `./ejs.min.js`。或者，您可以克隆仓库并运行 `jake build`（如果未全局安装 jake，则运行 `npx jake build`）自行编译。

在页面中引入上述任一文件，`ejs` 即可在全局范围内使用。

### 示例

```html
<div id="output"></div>
<script src="ejs.min.js"></script>
<script>
  let people = ['geddy', 'neil', 'alex'],
      html = ejs.render('<%= people.join(", "); %>', {people: people});
  // 使用 jQuery:
  $('#output').html(html);
  // 原生 JS:
  document.getElementById('output').innerHTML = html;
</script>
```

### 注意事项

大部分 EJS 功能都能按预期工作，但有几点需要注意：

-   由于无法访问文件系统，[`ejs.renderFile()`] 将无法工作。
-   同理，除非使用 include 回调，否则 `include` 无法工作。示例如下：

```javascript
let str = "Hello <%= include('file', {person: 'John'}); %>",
    fn = ejs.compile(str);
fn(data, null, function(path, d){ // include 回调
  // path -> 'file'
  // d -> {person: 'John'}
  // 在此处编写代码
  // 返回文件内容为字符串
}); // 返回渲染后的字符串
```

更多详情请参阅 [examples folder]。


### 使用示例

```bash
$ ejs -p [ -c ] ./template_file.ejs -o ./output.html
$ ejs -m $ ./test/fixtures/user.ejs name=Lerxst
$ ejs -n -l _ ./some_template.ejs -f ./data_file.json
```

### 参数规则

自 v7 起：

-   模板文件优先。任何 `name=value` 数据置于其后。
-   未知选项将被视为错误。
-   短选项可以组合（`-sdw`）并附带值（`-m$`）。
-   以 `-` 开头的值需要使用 `=`：`-o=-out.html`。
-   `--` 表示选项结束，例如当模板文件名以 `-` 开头时。
-   成功时退出状态为 0，用法错误为 2，运行时错误为 1。

### 数据输入

传递 JSON 数据的方式有三种：stdin、数据文件（`-f`）或命令行选项（`-i`）。同时使用 `-f` 和 `-i` 是错误的。仅当没有 `-f`、`-i` 或 `name=value` 数据时才读取 stdin。

-   Stdin
    ```bash
    $ cat ./test/fixtures/user_data.json | ejs -m $ ./test/fixtures/user.ejs
    $ ejs -m $ ./test/fixtures/user.ejs < test/fixtures/user_data.json
    ```
-   数据文件
    ```bash
    $ ejs -m $ ./test/fixtures/user.ejs -f ./test/fixtures/user_data.json
    ```
-   命令行选项（必须经过 URI 编码）
    ```bash
    ./bin/cli.js -m $ -i %7B%22name%22%3A%20%22foo%22%7D ./test/fixtures/user.ejs
    ```
-   模板后传递 `name=value` 对
    这些值会覆盖来自 `-f` 或 `-i` 的值，且始终为字符串：
    ```bash
    ./bin/cli.js -m $ ./test/fixtures/user.ejs name=foo
    ```

## IDE 集成与语法高亮

-   VSCode
    Javascript EJS by DigitalBrainstem

## 相关项目

EJS 有多种实现：

-   TJ 的实现
    本库的 v1 版本：[tj/ejs]
-   Google Code 上的 EJS Embedded JavaScript Framework
    [embeddedjavascript]
-   Sam Stephenson 的 Ruby 实现
    [ejs-rubygem]
-   Erubis
    一种同时也运行 JavaScript 的 ERB 实现：[erubis-javascript]
-   DigitalBrainstem EJS Language support
    [ejs-grammar]
