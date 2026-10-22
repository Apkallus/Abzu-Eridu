
- 元素选择
    - `#ID {}` 
        id 属性

- `opacity` 点击劫持
    透明度

- `width` 
    宽
- `height` 
    高

- `z-index` 点击劫持
    Z轴堆叠顺序，从屏幕到观察者的距离，数值大在顶层

- `pointer-events` 点击劫持
    指定在什么情况下 (如果有) 某个特定的图形元素可以成为鼠标事件的 target。
    - `none`
        元素永远不会成为鼠标事件的 target。但是，当其后代元素的`pointer-events`属性指定其他值时，鼠标事件可以指向后代元素，在这种情况下，鼠标事件将在捕获或冒泡阶段触发父元素的事件侦听器。

文章
- [portswigger css 提取元素内容](https://portswigger.net/research/blind-css-exfiltration)

# CSS 参考

## CSS 选择器

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Selectors

CSS 选择器是 CSS 规则中定位并选取特定元素以应用样式的模式。

### 伪元素

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Selectors/Pseudo-elements

伪元素是一个附加至选择器末的关键词，允许你对被选择元素的特定部分修改样式。

```css
selector::pseudo-element {
    property: value;
}
```

一个选择器中只能使用一个伪元素。伪元素必须紧跟在语句中的简单选择器/基础选择器之后。

### `::first-letter`

`::first-letter` CSS 伪元素将样式应用于区块容器第一行的第一个字母，但仅当其前面没有其他内容（例如图像或行内表格）时才有效。

## 值

### `<url>`

`<url>` CSS 数据类型是指向资源的指针。

```css
<url> = url()
```

`<url()>`
- `url()` 函数接受一个 URL，可以写成带引号的字符串，也可以写成不带引号的 URL 标记。

### ⚔️ url()

`url()` CSS 函数用于包含文件。参数可以是绝对 URL、相对 URL、blob URL 或数据 URL。

```css
url( <string> <url-modifier>* )
```

`<string>`
- 可以指定一个 URL 或 SVG 形状的 ID 的字符串。
    - `url`
        为相对地址、绝对地址的 URL，或指向所包含的 web 资源的指针，或数据 URL，可选择使用单引号或双引号。如果 URL 包含括号、空白字符或引号（除非这些字符已转义），或者地址包含高于 0x7e 的控制字符，则需要使用引号。除非经过转义，否则双引号不能出现在双引号内，单引号不能出现在单引号内。以下内容均有效且等效：
            ```css
            <css_property>: url("https://example.com/image.png")
            <css_property>: url('https://example.com/image.png')
            <css_property>: url(https://example.com/image.png)
            ```
        如果选择不使用引号编写 URL，请在 URL 中的任何括号、空白字符、单引号（`'`）和双引号（`"`）前使用反斜线（`\`）。

        > 显式标注可省略引号

    - `path`
        引用 SVG 形状或 SVG 滤镜的 ID。

## 属性

### ⚔️ display

- `<display-box>`
    这些关键词定义一个元素到底是否产生 `display` 盒。

    - `none`
        使元素不再显示，其对布局不会有影响（文档渲染得好像这个元素并不存在）。所有的后代元素也不会再显示。为了使元素占据一个它通常占据的空间，但实际上没有渲染任何东西，应该使用 `visibility` 属性。


### ⚔️ text-transform —— 文本大小写

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/text-transform

`text-transform` CSS 属性指定如何将元素的文本大写。它可以用于使文本显示为全大写或全小写，也可单独对每一个单词进行操作。

> `.innerText` 读取的渲染文本，大小写可被 `text-transform` 修改。对于默认 `display: none` 而不参与渲染的元素，需修改 `display` 属性

```css
/* 关键字值 */
text-transform: none;
text-transform: capitalize;
text-transform: uppercase;
text-transform: lowercase;
text-transform: full-width;
text-transform: full-size-kana;

/* 全局值 */
text-transform: inherit;
text-transform: initial;
text-transform: revert;
text-transform: revert-layer;
text-transform: unset;
```
- `capitalize`
    强制每个单词的首字母转换为大写。其他的字符保留不变
- `uppercase`
    强制所有字符被转换为大写。
- `lowercase`
    强制所有字符被转换为小写。
- `none`
    这个关键字阻止所有字符的大小写被转换。


### content

CSS 的 `content` CSS 属性用于在元素的 `::before` 和 `::after` 伪元素中插入内容。使用 `content` 属性插入的内容都是匿名的[可替换元素]。

### animation

https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/Properties/animation

CSS `animation` 属性是 `animation-*` 属性的一个简写属性形式。

```css
/* @keyframes duration | easing-function | delay |
iteration-count | direction | fill-mode | play-state | name */
animation: 3s ease-in 1s 2 reverse both paused slidein;

/* @keyframes duration | easing-function | delay | name */
animation: 3s linear 1s slidein;

/* two animations */
animation:
  3s linear slidein,
  3s ease-out 5s slideout;
```

### position —— 指定一个元素在文档中的定位方式

值
- `relative`
    - 元素根据文档的正常流程定位，然后根据 `top`、`right`、`bottom` 和 `left` 的值相对于自身偏移。偏移量不会影响任何其他元素的位置
    
    - 当 `z-index` 的值不是 `auto` 时，该值会创建一个新的层叠上下文。

- `absolute`
    - 该元素将从正常文档流中移除，页面布局中不会为该元素创建任何空间。元素的位置是相对于其位置最近的祖先（如果有）或初始包含块。其最终位置由 `top`、`right`、`bottom` 和 `left` 的值决定。

    - 当 `z-index` 的值不是 `auto 时`，该值会创建一个新的层叠上下文。绝对定位盒子的边距不会与其他边距折叠。

## `@` 规则
### ⚔️ `@import`

<https://developer.mozilla.org/zh-CN/docs/Web/CSS/Reference/At-rules/@import>

`@import` CSS `@` 规则用于从其他样式表导入样式规则。这些规则必须先于所有其他类型的规则，`@charset` 规则除外；因为它不是一个嵌套语句，`@import` 不能在条件组的规则中使用。

> 当上下文位于其他规则后，无法使用 `@import` 导入载荷 css

# CSS 指南
## 语法

### 错误处理

#### CSS错误处理

https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Syntax/Error_handling

> [!warning] 与文档说明不匹配：
> 
> [挑战](https://hackropole.fr/en/challenges/web/fcsc2026-web-minimaliste/) 
> ```css
> body::after {
>     display: hidden;
>     background-image: url('/e7468967db96d6e2ffc996a844095925.svg');
> }
> ```
> 无效属性值 `display: hidden;` 之后的图片语句在 firefox 中并未被执行（无图片请求），而非文档描述的继续下一条有效语句。手动移除或修改 `display` 时浏览器立即触发图片加载