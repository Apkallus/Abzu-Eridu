https://emscripten.org/docs/

## API Reference

### preamble.js

https://emscripten.org/docs/api_reference/preamble.js.html

[preamble.js] 中的 JavaScript API 提供了与编译后的 C 代码进行交互的编程访问方式，包括：调用编译后的 C 函数、访问内存、将指针转换为 JavaScript `Strings` 以及将 `Strings` 转换为指针（使用不同的编码/格式），以及其他便利函数。

我们称之为“`preamble.js`”，是因为 Emscripten 输出的 JS 在高层上包含 preamble（来自 `src/preamble.js`），然后是编译后的代码，最后是 postamble。（更详细地说，preamble 包含实用函数和设置，而 postamble 负责连接各部分并处理应用程序的运行。）

preamble 代码包含在输出的 JS 中，随后由编译器与您添加的任何 `--pre-js` 和 `--post-js` 文件，以及来自任何 JavaScript 库（`--js-library`）的代码一起整体优化。这意味着您可以直接调用 preamble 中的方法，编译器会识别出您需要它们，而不会将其作为未使用项移除。

如果您想从编译器无法看到的地方调用 preamble 方法，例如 HTML 上的另一个 script 标签，您需要**导出**它们。为此，请将它们添加到 `EXPORTED_RUNTIME_METHODS`（例如，`-sEXPORTED_RUNTIME_METHODS=ccall,cwrap` 将导出 `ccall` 和 `cwrap`）。一旦导出，您就可以在 `Module` 对象上访问它们（例如 `Module.ccall`）。

> **注意**
>
> 如果您尝试使用 `Module.ccall` 或其他运行时方法而未导出它，将会收到错误。在带有 `-sASSERTIONS` 的构建中，编译器会生成代码向您显示有用的错误消息，解释您需要导出它。通常，如果您看到奇怪的情况，使用断言构建会很有帮助。

#### cwrap

```javascript
cwrap(ident, returnType, argTypes)
```

返回 C 函数的原生 JavaScript 包装器。

这与 `ccall()` 类似，但返回一个可重复使用多次的 JavaScript 函数。C 函数可以定义在 C 文件中，也可以是使用 `extern "C"` 定义的 C 兼容 C++ 函数（以防止名称修饰）。

```javascript
// 从 JavaScript 调用 C
var c_javascript_add = Module.cwrap('c_add', // C 函数名称
  'number', // 返回类型
  ['number', 'number']); // 参数类型

// 正常调用 c_javascript_add
console.log(c_javascript_add(10, 20)); // 30
console.log(c_javascript_add(20, 30)); // 50
```

> **注意**
>
> - `cwrap` 使用 C 栈存储临时值。如果传递字符串，它只在调用完成前“存活”。如果被调用代码保存了指针以供后续使用，它可能指向无效数据。如果需要字符串永久存在，可以例如使用 `_malloc` 和 `stringToUTF8()` 创建它。但是，之后必须手动删除它！
> - 要包装函数，必须在调用 *emcc* 时将其添加到 `EXPORTED_FUNCTIONS` 列表中。如果函数未导出，优化可能会移除它，`cwrap` 在运行时将无法找到它。（在启用 `ASSERTIONS` 的构建中，`cwrap` 会在这种情况下显示错误；在没有断言的发布构建中，尝试包装不存在的函数将出错，具体取决于 `cwrap` 的优化方式，可能返回 `undefined` 或返回一个在调用时出错的函数。）
> - `cwrap` 实际上并不调用编译后的代码（只有调用它返回的包装器才会调用）。这意味着可以安全地提前调用 `cwrap`，在运行时完全初始化之前（但调用返回的包装函数当然必须等待运行时，就像一般调用编译后的代码一样）。
>
> ```text
> -sEXPORTED_FUNCTIONS=_main,_myfunc
> ```
>
> 导出的函数可以正常调用：
>
> ```javascript
> my_func = Module.cwrap('myfunc', 'number', ['number'])
> my_func(12)
> ```

**Arguments：**

- **ident** – 要调用的 C 函数名称。
- **returnType** – 函数的返回类型。可以是 `"number"`、`"string"` 或 `"array"`，分别对应相应的 JavaScript 类型（对于任何 C 指针使用 `"number"`，对于 JavaScript 数组和类型化数组使用 `"array"`；注意数组是 8 位的），对于 void 函数可以是 `null`（注意：是 JavaScript 的 `null` 值，不是包含单词 “null” 的字符串）。
- **argTypes** – 函数参数类型的数组（如果没有参数，可以省略）。类型与 `returnType` 中相同，但不支持 `array`，因为我们无法知道数组的长度。
- **opts** – 可选选项对象，参见 `ccall()`。

**Returns：**

- 可用于运行 C 函数的 JavaScript 函数。

### Module object

https://emscripten.org/docs/api_reference/module.html

`Module` 是一个全局 JavaScript 对象，其属性会被 Emscripten 生成的代码在执行过程的各个时间点调用。

开发者可以提供 `Module` 的实现来控制代码的执行。例如，为了定义 Emscripten 的通知消息如何显示，开发者实现 `Module.print` 属性。

当 Emscripten 应用程序启动时，它会查看 `Module` 对象上的值并应用它们。请注意，在启动*之后*更改这些值通常不会生效；在启用了 `ASSERTIONS` 的构建中，这种情况下会收到错误。

> **注意**
>
> `Module` 还用于以安全的方式提供对 Emscripten API 函数（例如 `ccall()`）的访问。任何导出的函数或运行时方法（编译后的函数使用 `EXPORTED_FUNCTIONS`，像 `ccall` 这样的运行时方法使用 `EXPORTED_RUNTIME_METHODS`）都可以在 `Module` 对象上访问，而不会被压缩改变名称，优化器也会确保保留该函数（而不会将其作为未使用项移除）。参见[相关 FAQ 条目]。

#### 创建 Module 对象

使用 emcc 的 `pre-js` 选项添加 JavaScript 代码，以定义（或扩展）具有所需行为的 `Module` 对象。

当仅生成 JavaScript（而非 HTML）时，默认不会创建 `Module` 对象，其行为完全由开发者定义。例如，使用以下代码创建 `Module` 对象，将导致程序的所有通知都变为对 `alert()` 的调用。

```javascript
var Module = {
  'print': function(text) { alert('stdout: ' + text) },
  'printErr': function(text) { alert('stderr: ' + text) }
};
```

> **重要**
>
> 如果对代码运行 Closure Compiler（这是可选的，可以通过 `--closure 1` 完成），则需要像上面的示例那样在 `Module` 的属性周围加上引号。此外，您需要对编译后的代码以及 `Module` 的声明一起运行 closure——对于 `--pre-js` 文件，这会自动完成。

当生成 HTML 时，Emscripten 会创建一个带有默认方法的 `Module` 对象（参见 `src/shell.html`）。在这种情况下，您应再次使用 `--pre-js`，但这次是向*现有*的 `Module` 对象添加属性，例如：

```javascript
Module['print'] = function(text) { alert('stdout: ' + text) };
```

请注意，一旦主 JavaScript 文件接收到 Module 对象，它将在那时查找 `Module['print']` 等属性，并相应地使用它们。之后更改它们的值可能不会被注意到。