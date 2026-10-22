## Core

### jQuery()

`jQuery()` 简写 `$()`

```js
jQuery( selector [, context ] ) 
    Returns: jQuery 
```

示例
```js
// 元素选择
$( "div.foo" );
```

## Ajax 

### Shorthand Methods

#### jQuery.getJSON()

**描述：** 使用 GET HTTP 请求从服务器加载 JSON 编码的数据。

```js
jQuery.getJSON( url [, data ] [, success ] )
```

- **url**
  - **类型：** [String](http://api.jquery.com/Types/#String)
  - 包含要发送请求的 URL 的字符串。

- **data**
  - **类型：** [PlainObject](http://api.jquery.com/Types/#PlainObject) 或 [String](http://api.jquery.com/Types/#String)
  - 随请求一起发送到服务器的普通对象或字符串。

- **success**
  - **类型：** [Function](http://api.jquery.com/Types/#Function)
  - **回调函数签名：** `( [PlainObject](http://api.jquery.com/Types/#PlainObject) data, [String](http://api.jquery.com/Types/#String) textStatus, [jqXHR](http://api.jquery.com/Types/#jqXHR) jqXHR )`
  - 如果请求成功，则执行的回调函数。


## Miscellaneous
### Collection Manipulation | Traversing

#### .each()

对象元素迭代器

## Manipulation
### DOM Insertion, Inside

#### .append()

https://api.jquery.com/append/

```js
.append( content [, content ] )
```