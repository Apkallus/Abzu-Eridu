# HTML 参考

## HTML 元素参考

### pre —— 预定义格式文本

在该元素中的文本通常按照原文件中的编排，以等宽字体的形式展现出来，文本中的空白符（比如空格和换行符）都会显示出来。
- 可用来格式化回显在乱码中的 php 载荷输出

### hr —— 水平分割线主题分割

表示段落级元素之间的主题转换
- 可用来格式化回显在乱码中的 php 载荷输出

### iframe

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/iframe

属性
- `sandbox` 
    控制 `<iframe>` 中的内容的限制。该属性的值可以为空以应用所有限制，也可以为空格分隔的标记以解除特定的限制：
    - `allow-forms` 点击劫持启用
        允许页面提交表单。

    - `allow-scripts` 点击劫持启用
        允许页面运行脚本（但不能创建弹窗）

    - `allow-top-navigation` 点击劫持不设置以应对框架破坏
        允许资源导航顶级（即名称为 `_top` 的）浏览上下文。

- `src`
    被嵌入的页面的 URL 地址。使用 `about:blank` 值可以嵌入一个遵从同源策略的空白页。
- `srcdoc` ⚔️
    要嵌入的内联 HTML，会覆盖 `src` 属性。

    ```html
    <iframe srcdoc='<script src="data:text/javascript,alert(document.domain)"></script>'></iframe>
    ```

### form 表单元素

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/form

属性
- `action` JS 伪协议注入点
    处理表单提交的 URL。这个值可被 `<button>`、`<input type="submit">` 或 `<input type="image">` 元素上的 `formaction` 属性覆盖。

### button

属性
- `formaction` JS 伪协议注入点 ⚔️
    表示程序处理 `button` 提交信息的 URI。如果指定了，将重写 `button` 表单拥有者的`action`属性。

### input

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/input

#### ⚔️ `<input type="image">`

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/input/image

`image` 类型的 `<input>` 元素用于创建图形化的提交按钮，即采用图像而非文本形式的提交按钮。

```html
<input type="image" src=x onerror=print() />
```

`<input type="image">` 元素不接受 `value` 属性。要显示的图像的路径在 `src` 属性中指定。

- `formaction`
    一个字符串，指示要将数据提交到的 URL。这优先于 `<form>` 元素上的 `action` 属性。

- `formmethod`
    一个字符串，指定提交表单数据时使用的 HTTP 方法；该值将会覆盖所属表单上的任何 `method` 属性。

- `src`
    一个字符串，指定将要在提交按钮上显示的图像的 URL。

### `<img>`：图像嵌入元素

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/img

`<img>` [HTML] 元素将一张图像嵌入文档。

```html
<img src onerror=print()>
```

#### 图像加载错误

如果在加载或渲染图像时发生错误，且设置了至少一个 onerror 事件处理器来处理 error 事件，那么设置的事件处理器就会被调用。

### SVG

#### `<use>` 废弃的 JS 数据注入点

https://developer.mozilla.org/zh-CN/docs/Web/SVG/Reference/Element/use

从 SVG 文档中获取节点，并将它们复制到其他地方。其效果与将这些节点深度克隆到一个不可导出的 DOM 中，然后粘贴到 use 元素所在的位置相同，这与克隆的模版元素类似。

- 使用方法：hash 符号后接元素id `<use href="#元素id"`

- 安全演化：出于安全原因，在 `href` 属性中使用数据 URI 加载资源已被弃用。这适用于 `<use href="data:...`，以及使用 `set` 或 `setAttribute` 方法设置 `href` 的情况。

### a 锚元素

属性
- `target`
    该属性指定在何处显示链接的 URL，作为浏览上下文的名称 `name`（标签、窗口或 `<iframe>`）。拥有特殊含义关键词