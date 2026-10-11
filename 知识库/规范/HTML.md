https://html.spec.whatwg.org/multipage/


## 13 The HTML syntax 

https://html.spec.whatwg.org/multipage/syntax.html

### 13.2 Parsing HTML documents

https://html.spec.whatwg.org/multipage/parsing.html

#### 13.2.5 Tokenization —— HTML 标签解析

https://html.spec.whatwg.org/multipage/parsing.html#tokenization

## 15 Rendering

https://html.spec.whatwg.org/multipage/rendering.html

### 15.2 The CSS user agent style sheet and presentational hints

### 15.3 Non-replaced elements

https://html.spec.whatwg.org/multipage/rendering.html#non-replaced-elements

#### 15.3.1 Hidden elements

```css
area, base, basefont, datalist, head, link, meta, noembed,
noframes, param, rp, script, style, template, title {
  display: none;
}
```

> 一批元素的默认显示设置为 `none`，需修改 css 后才可渲染